`DrainWorker`는 **접수된 response-end event를 세션별로 순서대로 처리하고, 처리 결과를 effect 파일과 notice로 남기는 구성요소**입니다. 흐름을 잡을 때는 `event`(처리할 입력), `binding`(그 입력이 속한 Workspace·thread·세대), `effect`(처리 결과)를 구별하면 됩니다.

```text
접수된 event들 → 순서대로 읽기 → 각 event의 binding 확인
                                      ├─ 기존 effect가 있으면 건너뜀
                                      ├─ 같은 세대의 앞선 실패가 막으면 보류
                                      └─ SemanticSession 복원·resume
                                           → decision 반영 → notice → effect 기록
```

**1. 실행 시작과 입력 읽기.** `MaintainRuntime`은 `DrainWorker`를 만들고 `drain(session_key)` 호출을 그 객체에 위임합니다. 별도 프로세스를 시작하는 `_start_detached_drain()`도 `DrainWorker`에 있습니다. 이 메서드는 Python에 `drain`, Project·runtime·config 경로, `session_key`를 전달하며 시작에 실패하면 실패 notice를 씁니다. 제공된 코드에는 이 메서드를 호출하는 `EventIntake` 내부가 없으므로, 어떤 접수 조건에서 호출되는지는 여기서 확정할 수 없습니다. 프로세스 시작은 작업 완료를 뜻하지 않습니다.

실제 `drain()`은 설정을 검증한 다음 해당 세션의 `_drain_lock`을 얻습니다. 이 잠금은 같은 세션의 drain 실행을 직렬화하며, 다른 drain이 진행 중이면 기다립니다. 잠금 안에서 `_state_lock`을 잠시 얻어 세션 상태와 event 목록을 읽습니다. `RuntimeStore._events()`는 event의 `sequence`와 파일 키 순으로 정렬하므로 이후 반복은 그 순서를 따릅니다. 상태 잠금은 이 읽기 이후 풀리고, drain 잠금은 반복이 끝날 때까지 유지됩니다.

```python
with self.store._drain_lock(session_directory):
    with self.store._state_lock(session_directory):
        state = self.store._read_session_state(session_directory)
        events = self.store._events(session_directory)
    blocked_generations: set[int] = set()
    for turn_key, event in events:
        binding = _binding_snapshot(
            event, state, "Maintain runtime response-end event"
        )
```

여기서 `events`는 읽은 시점의 목록입니다. 나중에 접수된 event까지 이 반복에 자동으로 추가되는 구조는 아닙니다. `RuntimeStore`의 drain 잠금 주석은 그래서 후속 worker가 잠금을 기다리도록 한다고 설명합니다.

**2. 각 event를 처리할 수 있는지 가릅니다.** `binding`에서 `workspace_id`와 `generation`을 얻습니다. 해당 `turn_key`의 effect 파일이 이미 있으면 다시 처리하지 않고 `already_resolved`를 올립니다. 그 effect가 후속 event를 막는 실패라면 해당 세대를 `blocked_generations`에 넣습니다. 아직 effect가 없는 event도 같은 세대가 막혀 있으면 `blocked`만 올리고 처리하지 않습니다. 즉, 실패 하나가 항상 모든 Workspace·세대의 event를 중단시키는 것은 아닙니다.

입력의 `user_prompt`, `turn_id`, `main_response`가 비어 있거나 문자열이 아니면 안정적인 한 턴으로 묶을 수 없다고 보고 실패 notice와 **후속을 막지 않는 실패 effect**를 기록합니다. 이후 event는 계속 살핍니다. 이 분기는 `blocks_later_events: False`이고, 실제 실행 중 예외가 난 뒤의 실패 분기는 `True`라는 차이가 있습니다.

**3. 처리 가능한 event를 실행하고 결과를 확정합니다.** 다음 호출들이 핵심입니다.

```python
semantic_session = session_type.restore(
    self.context.project_root,
    workspace_id,
    thread_id=binding["thread_id"],
    runner=self.context.runner,
)
decision = semantic_session.resume(
    {
        "workspace_id": workspace_id,
        "turn_id": turn_id,
        "user_prompt": user_prompt,
        "main_response": main_response,
    }
)
result = self.context.apply_decision(
    self.context.project_root,
    self.context.work_root,
    workspace_id,
    decision,
)
```

저장된 binding의 Workspace와 thread로 의미 판단 세션을 복원하고, 해당 턴의 입력과 응답을 `resume()`에 넘겨 `decision`을 받습니다. 그 판단을 `apply_decision()`에 넘겨 실제 Context에 반영하도록 요청합니다. 두 의존성의 내부 동작은 제공되지 않았으므로 판단 내용이나 반영 세부 절차까지 이 코드만으로 설명할 수는 없습니다. 반환된 `result`로 notice를 만든 뒤 `status: "resolved"`인 effect를 기록하고 `processed`를 올립니다. 이 순서상 **resolved effect는 반영 호출과 notice가 끝난 뒤에만** 기록됩니다.

복원·resume·반영·notice·effect 기록 중 예외가 나면 실패 notice와 `blocks_later_events: True`인 실패 effect를 쓰고, 그 세대의 뒤 event를 막습니다. 이 처리는 앞선 event의 판단·반영이 불확실한 상태에서 같은 세대의 후속 변경을 이어가지 않으려는 동작으로 읽힙니다. 다만 예외가 반영 호출 *이후*에 났다면 이미 반영된 내용이 있을 수 있으므로, 실패 effect만 보고 Context가 전혀 바뀌지 않았다고 단정하면 안 됩니다. 오류 문구도 재시도 전에 실제 Context를 확인하라고 합니다.

마지막 반환값은 이번 `drain()`의 `processed`, `failed`, `already_resolved`, `blocked` 건수와 세션 키를 담은 요약입니다. 이 숫자는 event별 경로를 알려 주지만, `DrainWorker` 밖의 판단·반영 내부가 무엇을 바꿨는지까지 증명하지는 않습니다.
