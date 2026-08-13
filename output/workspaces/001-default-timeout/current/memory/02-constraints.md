# 유지할 결정과 제약

- Python 표준 라이브러리만 사용한다.
- 기본 timeout의 canonical 결정은 Workspace가 아니라 Project 문서가 소유한다.
- 검증은 [`verify.json`](../../verify.json)에 고정된 argv만 사용한다.
- Workspace records는 실행 이력을 보존하지만 현재 상태를 대신하지 않는다.
- `memory/`에는 과거를 쌓지 않고 현재도 유효하며 기본 재진입에 필요한 주제만 둔다.
