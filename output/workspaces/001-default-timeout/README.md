# Default timeout Workspace

설정에서 `request_timeout_ms`가 빠졌을 때 Project가 정한 기본값 `5000`밀리초를 사용하도록 확인하는 작업 공간이다.

## 사람이 읽는 순서

1. [`current/memory/index.md`](current/memory/index.md)에서 작업이 진행되는 동안 계속 유효한 맥락을 찾는다.
2. [`current/state/index.md`](current/state/index.md)에서 지금 확인할 문제와 상태의 의미를 읽는다.
3. [`current/state/status.json`](current/state/status.json)에서 최근 검증 결과와 다음 행동을 확인한다.
4. 상세 실행 결과가 필요할 때만 status가 가리키는 [`records/`](records/) receipt를 연다.

다음 명령은 위 파일과 이번 작업에 선택된 Project 문서를 읽기 좋은 순서로 보여 준다. 이 Workspace 디렉터리가 아니라 [`output/` root](../..)에서 실행한다.

```sh
python3 harness/workspace.py recover
```

[`workspace.json`](workspace.json)은 Project context 선택, 고정 검증 명령, 결과별 다음 행동을 소유하는 실행 계약이다. 사람이 읽는 현재 문서와 분리되어 있지만 `recover`와 `verify`는 이 계약을 사용한다.
