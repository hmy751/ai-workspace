# Records

이 폴더에는 작업 중 만든 지속 가능한 문서, 분석, 중간 산출물, 시도, 결정, 실패, 검증 기록을 누적한다. records는 작업을 다시 검토하고 이어 갈 재료를 보존하는 곳이며, 여기에 있다는 이유만으로 현재 상태가 되지는 않는다.

## 기록 규칙

- 파일명은 `YYYY-MM-DD-NN-주제.md` 형식을 사용한다.
- 후속 작업에서 다시 사용할 수 있는 하나의 작업 산출물이나 작업 묶음을 한 문서로 남긴다.
- 원자료, 확인한 사실, 분석·제안, 사용자 결정, 검증 결과, 남은 불확실성을 가능한 한 구분한다.
- 일회성 명령 출력과 임시 탐색은 그대로 쌓지 않되, 이후 판단 근거가 되면 요약이나 검증 기록으로 보존한다.
- 완료된 기록의 의미를 나중 상태에 맞춰 다시 쓰지 않는다. 정정이나 후속 작업은 새 record로 남긴다.
- 비공개 대화 원문이나 대용량 원자료를 복제하지 않고 shared [`../../../source/`](../../../source/)의 canonical 자료를 가리킨다. 이 shared source는 reference 설계 작업대의 원자료이며, 실행 산출물인 `output/`의 Workspace별 `source/`와 같은 저장 층이 아니다.
- 분석 초안, 후보 비교, 탈락 사유, 시행착오, 결정 근거, 중간 검증은 날짜가 있는 record로 남긴다.
- 분석 문서라도 이 Workspace goal의 결과로 선택됐다면 [`../output/index.md`](../output/index.md)에서 찾게 한다. 선택 전 후보와 선택 이유, 교체된 이전 결과는 records에 유지한다.
- 파일 형식이나 완성도만으로 records와 output을 나누지 않고, Workspace goal에서 맡는 역할로 구분한다.
- 사람이 읽는 날짜별 기록은 `records/` 바로 아래에 두고, 기계 JSON은 `records/receipts/<종류>/`로 분리한다. Harness와 helper는 receipt producer이고 의미·수명주기의 Owner는 해당 Workspace다.
- 반복 개발 확인은 직접 test 명령으로 수행하고, 상태 전환이나 인계에 필요한 실행만 durable receipt로 남긴다.

## Current와의 관계

records의 문서를 current로 통째로 복사하지 않는다. 다음 세션이 알아야 할 현재 상태와 정확한 접근점만 [`../current/`](../current/)의 해당 owner 문서에 반영한다.

완료된 작업의 상세 과정은 records에 남는다. 그 결과가 이후에도 유지되는 효과·제약이면 `current/memory.md`, 아직 이어갈 작업이면 `current/state.md`에 압축해 남긴다. 더 이상 현재 행동에 영향을 주지 않으면 current에서 제거한다.

재진입 시에는 records 전체를 읽지 않는다. [`../current/index.md`](../current/index.md)에서 현재 질문에 필요한 기록만 선택해 들어온다.

## Output과의 관계

[`../output/`](../output/)에는 Workspace goal을 위해 선택된 현재 산출물과 실제 canonical 위치만 둔다. 산출물을 만들며 검토한 후보·선택 근거·실패·검증 과정은 records가 계속 보존한다. Output에 있다는 사실은 사람의 acceptance나 Workspace 완료를 자동으로 뜻하지 않는다.

## 최근 책임 경계 기록

- [`2026-08-14-01-workspace-source-layer-and-minimum-memory.md`](2026-08-14-01-workspace-source-layer-and-minimum-memory.md): Workspace source 층과 기본 recovery에 필요한 최소 memory 계약
- [`2026-08-14-02-workspace-output-layer-and-record-boundary.md`](2026-08-14-02-workspace-output-layer-and-record-boundary.md): goal output 지도, records와의 역할 경계, recovery packet schema `5` 검증
- [`2026-08-14-03-project-overview-and-recover-contract.md`](2026-08-14-03-project-overview-and-recover-contract.md): 실제 Project common context의 최소 진입점, overview-first·Markdown-only recover 계약과 최신 검증
- [`2026-08-14-04-reference-project-root-rename.md`](2026-08-14-04-reference-project-root-rename.md): 루트 `output/`을 `reference-project/`로 이름 변경한 이유, 범위와 재검증
- [`2026-08-14-05-machine-receipt-boundary-and-durable-verify.md`](2026-08-14-05-machine-receipt-boundary-and-durable-verify.md): 사람용 records와 종류별 machine receipt 배치, Owner, 호환과 durable verify 운용
