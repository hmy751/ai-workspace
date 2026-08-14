# 유지할 결정과 제약

- Python 표준 라이브러리만 사용한다.
- 기본 timeout의 canonical 결정은 Workspace가 아니라 Project 문서가 소유한다.
- 검증은 [`verify.json`](../../verify.json)에 고정된 argv만 사용한다.
- Workspace `source/`에는 원문·snapshot·provenance만 두며 현재 판단, 분석, 결정, 실행·검증 기록을 섞지 않는다.
- Workspace `records/`에는 분석 메모·후보·비교·탈락안·선택 근거와 실행 이력을 누적하지만 현재 상태를 대신하지 않는다.
- 사람이 읽는 날짜별 records는 `records/` 바로 아래에, 기계 receipt는 `records/receipts/<종류>/`에 분리한다. Product verify는 상태 전환이나 인계에 필요한 durable evidence를 남길 때 사용한다.
- Workspace `output/index.md`는 goal을 위해 선택된 현재 산출물의 canonical 위치만 보여 주며 Project root의 실제 파일을 복제하지 않는다.
- `memory/`에는 과거를 쌓지 않고 현재도 유효하며 기본 재진입에 필요한 주제만 둔다.
