# Workspaces

이 디렉터리는 [`Work context`](../README.md) 안에서 실제 작업을 복구하고 이어 가는 Workspace들의 지속 상태를 소유한다.

- [`index.json`](index.json): 명령에 Workspace id를 주지 않았을 때만 사용할 active 기본값을 선택한다. 명시한 id는 이 index와 독립적인 선택 권위다.
- 각 Workspace 디렉터리: 하나의 작업 정체성, 책임별 실행 계약, 현재 context, 선택한 원자료, goal 산출물 지도, 누적 기록을 함께 둔다.

각 Workspace의 내부 관계는 해당 `README.md`에서 시작한다. Harness는 이 자료를 읽고 갱신하는 관리 장치이며 Workspace의 목표, Project 기준, 사람의 판단을 소유하지 않는다.

## Workspace 내부 경계

- `workspace.json`: Workspace id와 schema를 가진 machine identity
- `recover.json` schema `4`: Project-root 상대 경로로 Recover가 읽을 `context/project/` 아래 regular Markdown 문서와 선택 이유. Project 공통 진입점인 `context/project/overview.md`를 포함하되 문서 순서는 Workspace가 정한다.
- `current/`: 다음 작업자가 이어받을 현재 유효 context와 필요하면 보존된 legacy machine status. `current/memory/`는 `index.md`, `01-goal.md`, `02-constraints.md`, `03-project-context.md`를 최소 구성으로 가진다. 기존 status schema `2`·`3`은 과거 제품 Verify 기록 복구를 위해 읽기 호환하며 새 evidence recorder는 이를 생성·변경하지 않는다.
- `source/`: 이 Workspace가 작업 입력으로 선택한 원문, 변경하지 않은 snapshot, provenance를 분리·보존하는 층. `source/index.md`를 최소 inventory로 두며 별도 원자료가 없으면 그 사실과 Project canonical을 복제하지 않은 경계를 적는다. 원자료의 저자와 정본 권위는 원래 출처에 남으며, Workspace는 선택 범위·사용 시점·무결성·재접근 경로를 관리한다. 현재 판단, 분석, 결정, 실행·검증 기록은 두지 않는다.
- `output/`: Workspace goal을 위해 선택된 현재 산출물을 찾는 층. `output/index.md`를 최소 산출물 지도로 두고, 실제 산출물이 Project root의 코드·문서·테스트에 있으면 복제하지 않고 canonical 상대 경로를 연결한다. Workspace 안에서만 소유하는 goal 산출물은 이 폴더에 직접 둘 수 있다. 아직 선택된 산출물이 없으면 index에 없다고 명시한다.
- `records/`: source와 실제 작업을 바탕으로 만든 분석·결정·실행·검증 기록의 누적층. 분석 메모·후보·비교·탈락안·선택 근거처럼 goal 산출물을 만들고 고른 사람이 읽는 기록은 이 폴더 바로 아래에 날짜와 내용을 드러내어 둔다.
- `records/receipts/`: 기계가 만든 append-only 증거를 종류별로 격리하는 층. 이미 수행된 검증의 선택적 evidence는 `verify/evidence-*.json`, Harness 자체 검증은 `harness-tests/`, 이식 전 상태 캡처는 `preflight/`를 사용한다. 기존 `verify-*.json`, 이전 flat `records/verify-*.json`, 연결된 status는 과거 제품 Verify의 읽기 호환 자료로만 보존한다. 새 `evidence-*`는 product status에 연결하지 않는다.

`source/`는 Project 전체가 공유하는 실제 공통 맥락인 [`context/project/`](../../project/)를 복제하는 곳이 아니다. Project context의 최소 진입점과 내용 계약은 [`context/project/README.md`](../../project/README.md)가 소유한다. 원자료를 다시 확인해야 할 때 사람이 필요한 항목만 선택해서 읽으며, `recover`는 `source/` 전체나 inventory를 기본 recovery packet에 싣지 않는다.

Source 항목에는 가능한 범위에서 원래 위치나 URL, 확보 시각과 방법, commit·version·SHA-256 같은 안정적인 식별 근거를 함께 둔다. 해석이나 결론이 생기면 source를 고치지 않고 `current/` 또는 `records/`에 분리한다.

`output/`은 `records/`에서 일부 파일을 자동 승격하거나 복제하는 archive가 아니다. 사람이 goal의 현재 결과로 선택한 산출물과 canonical 위치를 보여 주며, 선택 이유와 이전 후보는 `records/`에 남긴다. `output/`에 있다는 사실만으로 검증 통과, 사람의 수락, Workspace 완료가 되지 않는다. `recover`는 `output/index.md`만 기본 packet에 싣고 연결된 산출물 본문은 필요할 때 선택해서 읽게 한다.

작업 중 확인은 제품·eval·수동 검증 Owner가 직접 수행한다. 그중 다음 사람·세션에 남길 가치가 있는 결과만 Verify recorder로 기록하며, 실패·부분 결과도 숨기지 않고 미검증 범위를 함께 둔다. Main 작업 세션마다 선택한 Workspace를 이해하는 Maintainer 하나가 매 사용자 대상 Main 응답 종료에서 durable 의미 변화만 사람용 `current/`·`records/` 등의 기존 Owner에 반영한다. 기존 Workspace의 첫 grounding 뒤에는 같은 Maintainer 이해를 재사용하며 Maintain 때문에 Main 응답이나 관련 없는 다음 작업을 기다리게 하지 않는다. 기록된 evidence는 자동 삭제하거나 결과가 같다는 이유로 합치지 않으며 retention 자동화는 아직 제공하지 않는다.

관리 장치의 책임별 목적·입력·출력은 [`Recover`](../harness/recover/), [`Maintain`](../harness/maintain/), [`Verify`](../harness/verify/)가 각각 정의한다. Harness 자체 회귀 검증은 [`Harness validation`](../harness/validation/)이 소유한다.
