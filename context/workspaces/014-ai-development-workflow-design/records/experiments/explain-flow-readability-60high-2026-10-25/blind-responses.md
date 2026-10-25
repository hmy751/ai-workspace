## worker-A

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


---

## worker-B

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


---

## scalar-A

네. 현재 함수가 **불리언을 제외한 양의 정수**만 받으려면 그 검사가 필요합니다. Python에서는 `bool`이 `int`의 하위 타입이라 `isinstance(True, int)`와 `isinstance(False, int)`가 모두 `True`입니다.

```python
if isinstance(request_timeout_ms, bool) or not isinstance(request_timeout_ms, int):
    raise TypeError("request_timeout_ms must be an integer")
```

앞의 `bool` 검사를 빼면 `True`는 뒤의 양수 검사까지 통과해 그대로 정책 값이 됩니다. `False`는 양수 검사에서 걸리지만 `TypeError`가 아닌 `ValueError`가 납니다. 현재 테스트는 둘 다 `TypeError`로 거절하도록 확인하므로, 이 검사는 그 동작을 지키는 역할을 합니다.


---

## scalar-B

네. **현재 규칙이 불리언 값을 거부하는 것이라면 필요합니다.** Python에서 `bool`은 `int`의 하위 클래스라서 `isinstance(True, int)`와 `isinstance(False, int)`가 모두 `True`입니다.

```python
if isinstance(request_timeout_ms, bool) or not isinstance(request_timeout_ms, int):
    raise TypeError("request_timeout_ms must be an integer")
if request_timeout_ms <= 0:
    raise ValueError("request_timeout_ms must be greater than zero")
```

첫 조건을 빼면 `True`는 양수 `1`처럼 취급되어 그대로 반환됩니다. `False`는 `0`처럼 취급되어 뒤의 양수 조건에서 `ValueError`가 납니다. 현재 테스트는 둘 다 `TypeError`로 거부하도록 확인하므로, `bool` 검사는 값의 허용 여부와 오류 종류를 지킵니다.
