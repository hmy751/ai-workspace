# Reference implementation state

마지막 갱신: `2026-08-14`

## 현재 상태

이 Workspace의 reference 구현과 책임 경계 재구성은 완료 상태다. 후속 실제 Project 적용은 이 Workspace를 이어 쓰지 않고 [`002-project-application`](../../002-project-application/)에서 진행한다.

- 이전 구조 변경의 기준점은 Workspace current 폴더화 commit `df2ce77`, 책임 중심 Harness commit `80635ad`, Project·Work context 경계 commit `2b110a3`, 당시 문서 기록 commit `e3c237b`다. 이후 변경의 현재 근거는 아래 날짜 record에서 찾는다.
- Project common context를 `reference-project/context/project/`, Harness와 Workspace collection을 `reference-project/context/work/` 아래에 둔다.
- 루트 기준 Project는 Workspace별 goal 결과 지도 `output/`과 구분되도록 `output/`에서 `reference-project/`로 이름을 바꿨다. 이름 변경 기준점은 commit `d442c20`이며 Project·Work·Workspace·Harness의 내부 책임 계약은 바꾸지 않았다.
- 각 Workspace에 `current/`, `source/`, `output/`, `records/`를 형제로 두고 `source/index.md`를 source inventory, `output/index.md`를 goal 산출물 지도의 최소 진입점으로 정했다.
- `current/memory/`의 `01-goal.md`, `02-constraints.md`, `03-project-context.md`를 recover가 요구하는 최소 memory 계약으로 고정했다. Recover는 Workspace source의 존재나 내용을 검사하거나 기본 recovery packet에 싣지 않는다.
- Recover는 Workspace output에서 `output/index.md`만 읽고 연결된 artifact 본문은 기본 recovery packet에 싣지 않는다.
- 실행 계약을 `project_root`와 `work_root`로 분리했다.
- Project common context의 최소 진입점은 실제 내용의 `context/project/README.md`와 `overview.md`다. 기존 상세 Owner는 유지하고, overview는 링크 목록이나 복제본이 아니라 여러 Workspace에 필요한 공통 맥락과 Owner 우선순위를 담는다.
- Recover contract schema `4`, recovery packet schema `5`, status schema `2`다. Recover는 `context/project/` 아래 regular Markdown만 허용하고 overview를 첫 항목으로 요구한다. Packet shape와 verify contract·receipt schema는 유지했다.
- Workspace의 사람이 읽는 records는 root의 날짜별 Markdown, 기계 JSON은 `records/receipts/{verify,harness-tests,preflight}/`가 소유한다. 새 product verify는 nested `verify/`에만 쓰고, 이전 flat receipt는 읽기 호환을 유지한다.
- Receipt 배치·호환 변경은 점검 시점 HEAD `d442c20` 뒤의 작업 트리와 index에 있으며 아직 commit되지 않았다.
- Receipt 경계 변경 뒤 전체 40개 unittest와 실제 `recover -> verify -> recover`가 통과했다. 최신 receipt는 `records/receipts/verify/verify-20260814T070729765148Z-4de3a77434444335b088d4944631e94f.json`이고 machine status도 같은 receipt를 가리키는 `verified_waiting_acceptance`다. 후속 recover는 current 6개, output index 1개, Project overview와 결정 2개를 packet schema `5`로 복구하고 nested receipt는 control path로만 연결했다.
- repo-local application skill helper 테스트 7개와 skill validator도 통과했다.

## 근거 접근점

- Workspace current 폴더화와 검증: [`../records/2026-08-13-05-workspace-current-folder-migration.md`](../records/2026-08-13-05-workspace-current-folder-migration.md)
- Harness 책임 경계 재구성: [`../records/2026-08-13-06-harness-responsibility-boundary-refactor.md`](../records/2026-08-13-06-harness-responsibility-boundary-refactor.md)
- Project·Work context 상위 경계 재구성: [`../records/2026-08-13-07-project-work-context-boundary.md`](../records/2026-08-13-07-project-work-context-boundary.md)
- 저장소 context의 Workspace 분리: [`../records/2026-08-13-08-outer-context-workspace-separation.md`](../records/2026-08-13-08-outer-context-workspace-separation.md)
- Workspace source와 최소 memory 계약: [`../records/2026-08-14-01-workspace-source-layer-and-minimum-memory.md`](../records/2026-08-14-01-workspace-source-layer-and-minimum-memory.md)
- Workspace output 지도와 records 경계: [`../records/2026-08-14-02-workspace-output-layer-and-record-boundary.md`](../records/2026-08-14-02-workspace-output-layer-and-record-boundary.md)
- 실제 Project overview와 recover 계약: [`../records/2026-08-14-03-project-overview-and-recover-contract.md`](../records/2026-08-14-03-project-overview-and-recover-contract.md)
- 기준 Project 루트 이름 변경과 재검증: [`../records/2026-08-14-04-reference-project-root-rename.md`](../records/2026-08-14-04-reference-project-root-rename.md)
- Machine receipt 경계와 durable verify 운용: [`../records/2026-08-14-05-machine-receipt-boundary-and-durable-verify.md`](../records/2026-08-14-05-machine-receipt-boundary-and-durable-verify.md)
- 실행 가능한 기준 Project: [`../../../../reference-project/README.md`](../../../../reference-project/README.md)

## 검증 상한

- 이번 reference는 한 예시 Project 안에서만 검증했다. 다른 실제 Project의 기존 상세 Owner에서 실제 overview를 구성하고 migration하는 과정은 아직 이 Workspace에서 검증하지 않았다.
- 저장소 작업대의 공유 `context/source/`는 reference 설계 원자료이고 `reference-project/` Workspace source의 seed가 아니다. 기존 적용 target도 이번 기준 Project·skill 변경만으로 자동 migration되지 않는다.
- 테스트는 source가 기본 recover 입력이 아니라는 경계를 확인한다. 실제 source snapshot의 provenance 품질, 원래 출처의 가용성, 의미 정확성을 검증하지 않는다.
- 테스트는 Project overview-first·Markdown-only와 output index의 필수 존재·로딩, artifact 본문 비로딩 경계를 확인하지만, overview나 연결된 산출물의 의미 정확성·freshness·사람 acceptance를 검증하지 않는다.
- Workspace 생성·전환·완료·보관, acceptance 기록, Project canonical 반영, automatic receipt retention과 concurrent verify는 구현하지 않았다.
- `verify.json`은 저장소가 신뢰하는 운영 계약이며 악의적인 명령을 격리하는 sandbox가 아니다. receipt와 status는 하나의 transaction으로 묶이지 않는다.
- CLI의 고정 설치 위치와 기존 `context` Python package가 있는 Project의 결합은 검증하지 않았다.

## 다음 행동

이 Workspace에는 예정된 다음 행동이 없다. reference 자체를 다시 변경해야 할 때만 별도 지시로 재개한다. 기존 target의 source·output·receipt 층 migration은 대상별 적용 작업에서 별도로 판단한다.
