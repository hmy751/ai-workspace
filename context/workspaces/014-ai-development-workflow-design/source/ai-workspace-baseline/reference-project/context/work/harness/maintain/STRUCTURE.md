# Maintain 구현과 테스트 찾기

Maintain은 명시적으로 연결한 Workspace의 대화 변화를 판단하고 허용된 Context 파일에 반영한다. 동작 계약은 [README](README.md), 연결과 generation 규칙은 [lifecycle 계약](SESSION-BINDING-AND-LIFECYCLE.md)이 소유한다. 이 문서는 그 책임이 코드와 테스트에서 어디에 있는지 안내한다.

## 실행 흐름

도구별 연결이 hook과 제어 명령을 받아 공통 runtime을 호출한다. Runtime은 prompt 접수 시 binding을 고정하고 응답 종료 시 event를 저장한다. 별도 worker가 저장 순서로 판단을 요청하고, 검증된 결정만 apply를 거쳐 반영한다.

```text
adapters/codex.py 또는 adapters/claude.py
  └─ runtime/engine.py: 구성과 공개 동작
      ├─ binding.py: Workspace 연결·해제
      ├─ events.py: prompt·응답 연결과 접수
      ├─ storage.py + storage_io.py: 경로·잠금·상태 저장과 조회
      ├─ status.py + notices.py: 상태 조회와 전달할 알림
      └─ worker.py: event 순서대로 판단과 반영
          ├─ semantic/prompt.py: 판단 입력 구성
          ├─ adapters/codex_session.py: 기존 판단 세션 실행·재개
          ├─ contracts/: 모델 응답과 적용 결정 검증
          └─ apply/: 허용 경로·변경 준비·파일 반영
```

각 runtime 구성요소는 필요한 다른 구성요소를 생성자로 전달받는다. 기능을 여러 상속 클래스에 나누거나 숨겨진 전역 객체에서 찾지 않는다. `runtime/context.py`에는 실행에 필요한 경로·시간·프로세스 실행·판단 세션 의존성이 있다.

## 변경할 위치

- Workspace 연결·전환: `runtime/binding.py`, `runtime/state.py`, `tests/runtime/test_binding.py`
- prompt·응답의 중복·누락: `runtime/events.py`, `tests/runtime/test_hooks.py`
- 실패 순서·background 처리: `runtime/worker.py`, `tests/runtime/test_failure_ordering.py`
- 기존 저장 상태 호환과 상태 조회: `runtime/state.py`, `runtime/status.py`, `tests/runtime/test_compatibility.py`
- 도구별 hook·환경변수·명령: `adapters/codex.py`, `adapters/claude.py`, `tests/adapters/`
- 판단 입력과 실행: `semantic/prompt.py`, `adapters/codex_session.py`, `tests/semantic/`, `tests/adapters/test_codex_session.py`
- 모델 응답 검증: `contracts/response.py`. 최종 반영 경계의 경로 표기·중복·비어 있는 근거 등 더 엄격한 검증은 `contracts/decision.py`가 소유한다.
- 파일 변경: `apply/policy.py`는 허용 기준, `apply/prepare.py`는 실제 파일과 링크 검사, `apply/transaction.py`는 stage와 쓰기 직전 조건, `apply/service.py`는 이 흐름의 연결을 소유한다. 대응 검사는 `tests/apply/`에 있다.

`bootstrap.py`는 기존 Recover 공개 API를 사용한다. Recover와 Verify의 내부 책임을 Maintain으로 옮기지 않는다. JSON schema와 role TOML은 기존 파일 경로를 유지하며 `resources.py`에서 기준 경로를 찾는다.

`host_adapter.py`, `codex_session.py`, `operation.py`는 기존 공개 import와 모듈 실행을 위한 연결 파일이다. 새 내부 구현은 해당 책임 모듈에 작성한다. 과거 대형 클래스의 private 속성은 호환 API가 아니다.

## Codex와 Claude 연결

두 도구는 같은 binding·event·apply 규칙을 사용한다. Codex는 `.codex/maintain.json`과 `.codex/maintain-runtime/`, Claude는 `.claude/maintain.json`과 `.claude/maintain-runtime/`을 사용하므로 같은 session id라도 상태가 섞이지 않는다. 별도 worker에도 원래 연결의 설정 경로와 runtime 경로를 전달한다.

현재 의미 판단은 두 호스트 모두 기존 Codex 실행기를 사용한다. Claude Code hook 지원은 Claude 모델로 의미 판단을 실행한다는 뜻이 아니다. 공통 입력 구성과 최소 세션 인터페이스는 도구 실행 코드에서 분리되어 있으며, 실행 도구를 바꿀 때도 binding·apply 규칙을 복제하지 않는다.

Claude hook은 공유 turn id가 없는 입력을 전용 `claude-hook-turn-state.json`으로 연결한다. 미연결 session·subagent hook·재귀 Stop은 조용히 반환한다. `SessionStart`에서 `CLAUDE_ENV_FILE`이 있으면 `MAINTAIN_CLAUDE_SESSION_ID`를 기록해 이후 명시적 control이 같은 session을 선택하도록 한다. 환경변수를 사용할 수 없으면 `--session-id`를 명시한다. Workspace는 대화 내용이나 active index로 추론하지 않는다.

프로젝트 root에서 Claude 연결을 직접 조회하는 명령은 다음과 같다.

```bash
python3 .claude/hooks/maintain.py status --session-id <session_id>
```

Claude wrapper는 `session-start`, `user-prompt`, `response-end`, `session-end`, `status`, `activate`, `deactivate`를 지원한다. 실제 Claude hook 설정에는 각각 `SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd`를 연결한다. 이 Reference는 wrapper와 admission 설정을 제공하지만 Claude의 실제 hook 등록·실행을 자동 활성화하지 않는다. 설치된 host의 실제 payload·호출 순서·notice 전달은 별도 acceptance로 확인한다.

## 검증

Python 3.11 이상, 표준 `unittest`를 사용한다. 프로젝트 root에서:

```bash
# Maintain 전체
python3 -B -m unittest discover -s context/work/harness/maintain/tests -t . -p 'test_*.py' -v

# 두 도구 연결
python3 -B -m unittest discover -s context/work/harness/maintain/tests/adapters -t . -p 'test_*.py' -v

# 제품과 Harness 전체 회귀
python3 -B -m unittest discover -s . -p 'test_*.py' -v
```

[테스트 안내](tests/README.md)에서 준비 코드와 시나리오 위치를 찾는다. 자동 테스트는 실제 모델의 의미 판단 품질이나 실제 host의 hook 신뢰·발견을 증명하지 않는다.
