## worker-A

`DrainWorker`는 **이미 접수된 응답 종료 이벤트를 세션별로 순서대로 처리하고, 각 이벤트의 결과를 기록하는 실행 담당자**입니다. 제공된 코드에서 흐름은 `이벤트 읽기 → 기존 결과·차단 여부 확인 → 판단 복원과 반영 → 결과 기록`으로 이어집니다.

### 어디서 시작하나요?

`MaintainRuntime`은 공통 경로와 실행 도구를 담은 `RuntimeContext`, 파일·잠금을 맡는 `RuntimeStore`, 알림을 맡는 `NoticeService`를 만들고 worker에 전달합니다. 공개 `drain()` 호출은 그대로 worker에 위임합니다 (`code/engine.py`).

```python
self.worker = DrainWorker(self.context, self.notices, self.store)
self.events = EventIntake(self.context, self.notices, self.store, self.worker)

def drain(self, session_key: str) -> dict[str, Any]:
    return self.worker.drain(session_key)
```

worker에는 별도 프로세스를 띄우는 `_start_detached_drain()`도 있습니다 (`code/worker.py`). 이 메서드는 Python 모듈의 `drain` 명령에 Project·runtime·설정 경로와 `session_key`를 넘깁니다. 시작 자체가 실패하면 실패 알림을 쓰며 완료를 주장하지 않습니다. 제공된 코드에는 `EventIntake` 내부가 없으므로 **어떤 접수 조건에서 이 메서드를 부르는지**까지는 확정할 수 없습니다.

### `drain()`은 어떤 순서로 처리하나요?

먼저 `session_key`로 세션 디렉터리를 찾고 설정을 검증합니다. 그다음 세션의 **drain 잠금**을 잡아 같은 세션의 worker 둘이 동시에 처리하지 못하게 합니다. 잠금은 기다리는 방식입니다. 그 안에서 잠시 **state 잠금**을 잡고 세션 상태와 접수된 이벤트 목록을 읽습니다 (`code/worker.py`). `RuntimeStore._events()`는 이벤트의 `sequence`와 `turn_key` 순서로 목록을 정렬합니다 (`code/storage.py`).

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

여기서 `binding`은 이벤트에 연결된 `workspace_id`와 `generation`을 제공하는 값입니다. `generation`은 이 코드에서 후속 이벤트 차단 범위를 가르는 데 쓰입니다. `_binding_snapshot()`의 내부 판정은 제공되지 않았으므로 그 이상의 연결 규칙은 단정할 수 없습니다.

각 이벤트에서는 먼저 `effects/<turn_key>.json`이 있는지 봅니다. **이미 effect가 있으면 다시 실행하지 않고** `already_resolved`를 올립니다. 그 effect가 후속 처리를 막는 실패라면 해당 generation을 차단 목록에 넣습니다. 아직 effect가 없는 이벤트라도 같은 generation이 차단돼 있으면 실행하지 않고 `blocked`를 올립니다. 따라서 `already_resolved`는 성공만 뜻하지 않고 *실패 effect가 이미 있는 경우도* 포함합니다.

실행 가능한 이벤트라도 `user_prompt`, `turn_id`, `main_response`가 모두 비어 있지 않은 문자열이어야 합니다. 하나라도 빠지면 실패 알림과 `status: failed` effect를 쓰고 `failed`를 올립니다. 이 실패에는 `blocks_later_events: False`를 기록하므로 같은 generation의 다음 이벤트까지 막지는 않습니다 (`code/worker.py`).

세 값이 갖춰졌다면 실제 처리로 들어갑니다. 다음 코드는 핵심 호출을 원래 순서대로 보여 줍니다 (`code/worker.py`).

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
self.notices._notification_for_result(
    session_directory, turn_key, result
)
```

즉, 저장된 Workspace·thread 연결로 `semantic_session`을 복원하고, 그 응답의 입력과 출력을 넘겨 `decision`을 받습니다. 이어 `apply_decision`에 그 판단을 넘겨 반영한 뒤 결과 알림을 만듭니다. 이 호출들이 성공하면 `status: resolved`, 완료 시각, `context_status`, `importance`, binding 정보를 effect에 기록하고 `processed`를 올립니다. `restore`, `resume`, `apply_decision`의 내부 동작과 `context_status` 값의 구체적 의미는 제공된 코드만으로 설명할 수 없습니다.

### 실패하면 뒤의 이벤트는 어떻게 되나요?

위의 복원·판단·반영·알림·성공 effect 기록 중 예외가 나면, worker는 실패 알림과 `status: failed`, `blocks_later_events: True`인 effect를 쓰고 **같은 generation의 뒤 이벤트**를 차단합니다. 이미 일부 반영이 이뤄진 뒤 실패했을 가능성도 있으므로 오류 문구는 재시도 전에 실제 Context를 확인하라고 합니다. 다른 generation까지 일괄 차단하는 코드는 아닙니다.

마지막 반환값의 `processed`, `failed`, `already_resolved`, `blocked`는 이번 `drain()` 순회에서 각각 어떻게 분류됐는지를 나타냅니다. 접수된 이벤트 전체가 성공했다는 단일 완료 표시는 아닙니다.


---

## worker-B

`DrainWorker`는 **접수된 response-end 이벤트를 세션별 순서대로 처리하고, 각 이벤트의 결과를 기록하는 구성요소**입니다. `MaintainRuntime`은 `response_end()`를 `EventIntake`에, `drain()`을 `DrainWorker`에 연결합니다. 따라서 이벤트를 받는 일과 그 이벤트에 대한 판단·반영을 끝내는 일은 서로 다른 단계입니다. 제공된 코드에는 `EventIntake` 내부가 없으므로, 접수 단계의 세부 조건은 여기서 단정할 수 없습니다.

```text
response_end 접수 → 저장된 event
                        ↓
                DrainWorker.drain(session_key)
                        ↓
          판단 재개 → Context 반영 → effect 기록
```

`_start_detached_drain()`은 별도 Python 프로세스에 `drain` 명령과 Project·runtime·설정 경로, `session_key`를 전달하는 시작 함수입니다. 프로세스 시작에 실패하면 실패 알림을 남기며 완료를 주장하지 않습니다. 실제로 **어느 접수 조건에서 이 함수를 호출하는지**는 제공된 호출부에 없으므로 위 그림은 두 단계의 관계를 나타냅니다. 공개 `MaintainRuntime.drain(session_key)`는 `self.worker.drain(session_key)`로 그대로 넘깁니다.

`drain()`의 첫 단계는 해당 세션의 작업을 **한 번에 하나씩** 수행할 준비입니다.

```python
with self.store._drain_lock(session_directory):
    with self.store._state_lock(session_directory):
        state = self.store._read_session_state(session_directory)
        events = self.store._events(session_directory)
    blocked_generations: set[int] = set()
    for turn_key, event in events:
```

`session_key`로 세션 디렉터리를 찾고 설정을 검증한 뒤 이 구간으로 들어갑니다. `_drain_lock`은 같은 세션의 worker들이 동시에 처리하지 않도록 기다리는 잠금입니다. 그 안에서 `_state_lock`을 잠깐 잡아 세션 상태와 이벤트 목록을 읽습니다. `RuntimeStore._events()`는 저장된 이벤트를 `sequence`, 이어서 `turn_key` 순으로 정렬합니다. 상태 잠금을 놓은 뒤에도 drain 잠금은 반복 처리가 끝날 때까지 유지됩니다. 따라서 이 반복문은 **읽어 온 목록**을 순서대로 처리하며, 읽은 뒤 새로 접수된 이벤트까지 이 목록에 자동으로 추가하지는 않습니다.

각 이벤트에서 `_binding_snapshot(event, state, ...)`으로 그 이벤트의 `workspace_id`와 `generation`을 얻습니다. `generation`은 세션의 Workspace 연결 세대를 구분하는 값입니다. 이미 `effect` 파일이 있으면 처리 결과가 기록된 이벤트로 보고 다시 실행하지 않습니다. 그 effect가 후속 이벤트를 막는 실패라면 같은 세대를 `blocked_generations`에 넣습니다. 이후 **같은 세대**의 아직 처리되지 않은 이벤트는 건너뛰지만, 다른 세대까지 일괄 차단하지는 않습니다.

```python
if effect_path.exists():
    summary["already_resolved"] += 1
    effect = _read_json_object(effect_path, "Maintain runtime effect")
    if effect.get(
        "status"
    ) == "failed" and self.store._effect_blocks_later_events(effect):
        blocked_generations.add(generation)
    continue
if generation in blocked_generations:
    summary["blocked"] += 1
    continue
```

처리 가능한 이벤트라면 `user_prompt`, `turn_id`, `main_response`가 모두 비어 있지 않은 문자열인지 확인합니다. 셋을 안정적으로 짝지을 수 없으면 실패 알림과 `status: failed`, `blocks_later_events: False`인 effect를 기록합니다. 이 실패는 해당 이벤트를 끝내지만 같은 세대의 다음 이벤트를 막지는 않습니다.

입력이 갖춰지면 핵심 처리로 들어갑니다. 저장된 연결의 `workspace_id`와 `thread_id`로 semantic session을 복원하고, 해당 턴의 세 값을 `resume()`에 넘겨 `decision`을 받습니다. 이어 `apply_decision()`에 Project, `context/work`, Workspace, 그 판단을 넘겨 결과를 얻습니다. 결과 알림을 만든 다음에야 `status: resolved`인 effect를 기록하고 `processed`를 올립니다.

```python
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

복원·판단·반영·결과 알림·effect 기록 중 예외가 나면 실패 알림과 `blocks_later_events: True`인 실패 effect를 기록하고, 같은 `generation`의 후속 이벤트를 막습니다. 이미 무엇이 반영됐는지는 이 예외 처리만으로 확정하거나 되돌리지 않습니다. 그래서 오류 메시지도 재시도 전에 실제 Context를 확인하라고 안내합니다. `drain()`은 마지막에 `processed`, `failed`, `already_resolved`, `blocked` 등의 집계를 반환합니다.

요약하면, **접수는 처리할 이벤트를 남기는 단계이고, drain은 저장된 이벤트를 순서대로 판단·반영해 effect로 마감하는 단계**입니다. effect는 중복 실행을 피하는 기준이자, 실패 뒤 같은 연결 세대의 처리를 계속할지 결정하는 기준입니다. `resume()`과 `apply_decision()` 내부에서 어떤 판단·파일 변경이 일어나는지는 제공된 코드만으로 더 설명할 수 없습니다.


---

## scalar-A

네. 현재 의도대로 불리언을 거부하려면 `int` 검사와 별도로 걸러야 합니다. Python에서 `bool`은 `int`의 하위 타입이라 `isinstance(True, int)`와 `isinstance(False, int)`가 모두 참입니다.

```python
if isinstance(request_timeout_ms, bool) or not isinstance(request_timeout_ms, int):
    raise TypeError("request_timeout_ms must be an integer")
if request_timeout_ms <= 0:
    raise ValueError("request_timeout_ms must be greater than zero")
```

첫 조건에서 `bool` 검사를 빼면 `True`는 정수 검사를 통과하고 양수 `1`처럼 취급되어 설정값으로 반환됩니다. `False`도 정수 검사는 통과하지만 다음의 양수 검사에서 `ValueError`가 납니다. 현재 테스트는 둘 다 `TypeError`로 거부하도록 요구하므로, 별도의 `bool` 배제는 필요합니다. 꼭 이 표현이어야 하는 것은 아니지만, `int` 검사만으로는 같은 동작을 만들 수 없습니다.


---

## scalar-B

네, **불리언을 거부하려면 필요합니다.** Python에서는 `bool`이 `int`의 하위 클래스라서 `isinstance(True, int)`와 `isinstance(False, int)`가 모두 참입니다.

```python
if isinstance(request_timeout_ms, bool) or not isinstance(request_timeout_ms, int):
    raise TypeError("request_timeout_ms must be an integer")
```

앞의 `bool` 검사만 없애면 `True`는 뒤의 양수 검사(`request_timeout_ms <= 0`)도 통과해 타임아웃 값으로 저장됩니다. `False`는 양수 검사에서 걸리지만 `TypeError` 대신 `ValueError`가 납니다. 현재 함수의 “불리언은 정수 값으로 받지 않는다”는 규칙과 두 값 모두 `TypeError`를 기대하는 테스트를 지키려면 이 검사가 있어야 합니다.
