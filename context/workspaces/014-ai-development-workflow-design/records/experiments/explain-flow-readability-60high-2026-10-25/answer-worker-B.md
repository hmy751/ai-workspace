`DrainWorker`는 **이미 접수되어 저장된 response-end event를 순서대로 처리하고, 각 event의 결과를 기록하는 역할**입니다. 핵심 흐름은 `event 조회 → 판단 세션 재개 → Context에 판단 반영 → 알림과 effect 기록`입니다. 여기서 *event*는 처리할 입력이고, *effect*는 그 event가 해결됐는지 실패했는지 남기는 결과 파일입니다.

```text
저장된 events
    ↓ sequence 순서로 조회
DrainWorker.drain
    ├─ 이전 effect 확인: 이미 처리했으면 건너뜀
    ├─ 입력 확인: prompt·turn_id·응답이 없으면 실패 기록
    └─ 판단 세션 복원·resume → 판단 반영 → 알림 → resolved effect
                                  └─ 예외가 나면 failed effect와 후속 차단
```

**시작과 실제 처리는 구별됩니다.** `MaintainRuntime`은 `DrainWorker`를 만들고 공개 `drain(session_key)` 호출을 그 객체에 넘깁니다(`code/engine.py`). `DrainWorker._start_detached_drain()`은 별도 Python 프로세스에 `drain` 명령과 Project·runtime·config 경로, `session_key`를 전달하도록 구성합니다. 프로세스를 시작하지 못하면 실패 알림을 남깁니다. 제공된 코드에는 이 메서드를 *누가 언제 호출하는지*가 없으므로, 모든 response-end에서 별도 프로세스가 시작된다고까지 단정할 수는 없습니다.

**`drain()`이 시작되면 한 session의 작업을 직렬로 잡습니다.** `session_key`로 저장 폴더를 찾고 설정을 검증한 뒤, `_drain_lock`을 획득합니다. 이 잠금은 다른 drain이 끝나기를 기다리므로 같은 session의 drain 실행이 겹치지 않습니다. 그 안에서 `_state_lock`을 잠깐 잡아 session 상태와 event 목록을 읽고, 잠금을 풀고 나서 목록을 처리합니다. `RuntimeStore._events()`는 event의 `sequence`와 `turn_key` 순으로 정렬합니다(`code/storage.py`). 따라서 이 drain은 **읽은 시점의 목록**을 그 순서로 훑습니다. 그 뒤에 접수된 event까지 같은 반복문이 자동으로 읽는다는 뜻은 아닙니다.

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

여기서 `binding`은 event에 대응하는 Workspace와 `generation`을 얻는 데 쓰입니다. `generation`은 뒤에서 실패의 차단 범위를 구분합니다. `_binding_snapshot`의 내부 규칙은 제공되지 않았으므로 이보다 구체적인 선택 방식은 알 수 없습니다.

**각 event는 먼저 처리 여부와 입력의 완전성을 확인합니다.** 해당 `turn_key`의 effect 파일이 이미 있으면 다시 판단하거나 반영하지 않고 `already_resolved`에 셉니다. 단, 그 effect가 후속 처리를 막는 실패였다면 해당 generation을 차단 목록에 넣습니다. 아직 effect가 없는 event가 차단된 generation에 속하면 `blocked`에 세고 넘깁니다. 차단되지 않았다면 `user_prompt`, `turn_id`, `main_response`가 모두 공백이 아닌 문자열인지 확인합니다. 하나라도 없으면 실패 알림과 `blocks_later_events: False`인 failed effect를 남깁니다. 이 입력 누락은 그 event의 실패로 끝나며 같은 generation의 뒤 event를 차단하지 않습니다.

**입력이 갖춰진 event는 판단을 얻어 반영합니다.** 다음은 `code/worker.py`에서 실제 호출이 이어지는 부분입니다.

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
self.notices._notification_for_result(session_directory, turn_key, result)
```

즉 저장된 binding의 Workspace·thread로 판단 세션을 복원하고, 이 turn의 prompt와 응답을 `resume()`에 전달합니다. 나온 `decision`을 `apply_decision()`에 넘겨 실제 Context에 반영하도록 호출합니다. 그 반환값 `result`로 알림을 만든 다음, `status: resolved`, 완료 시각, `context_status`, `importance`, binding 정보를 effect 파일에 기록하고 `processed`를 올립니다. 판단 세션 내부와 반영 함수 내부의 세부 동작은 제공된 코드만으로 설명할 수 없습니다.

**처리 중 예외는 성공으로 기록하지 않습니다.** 복원·resume·반영·알림·effect 기록을 묶은 `try`에서 예외가 나면 실패 알림과 `blocks_later_events: True`인 failed effect를 남기고 `failed`를 올립니다. 이어 같은 generation을 `blocked_generations`에 넣어 뒤 event의 처리를 막습니다. 다른 generation은 이 차단 집합 때문에 자동으로 막히지 않습니다. 이미 저장된 failed effect도 다음 drain에서 다시 읽어 같은 차단을 복원합니다. 이 실패 경로의 메시지가 실제 Context를 확인하라고 하는 이유는, 예외가 나기 전에 반영이 일부 진행됐을 가능성을 이 코드만으로 배제할 수 없기 때문입니다.

마지막으로 `drain()`은 `processed`, `failed`, `already_resolved`, `blocked` 등의 개수를 담은 요약을 반환합니다. 이 값들은 **이번에 읽은 event 목록을 어떻게 처리했는지** 보여 주며, `resolved` effect가 없는 event가 남지 않았다는 보장이나 현재 설치·활성화 상태를 뜻하지는 않습니다.
