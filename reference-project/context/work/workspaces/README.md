# Workspaces

이 디렉터리는 [`Work context`](../README.md) 안에서 실제 작업을 복구하고 이어 가는 Workspace들의 지속 상태를 소유한다.

- [`index.json`](index.json): 명령에 Workspace id를 주지 않았을 때만 사용할 active 기본값을 선택한다. 명시한 id는 이 index와 독립적인 선택 권위다.
- 각 Workspace 디렉터리: 하나의 작업 정체성, 책임별 실행 계약, 현재 context, 선택한 원자료, goal 산출물 지도, 누적 기록을 함께 둔다.

각 Workspace의 내부 관계는 해당 `README.md`에서 시작한다. Harness는 이 자료를 읽고 갱신하는 관리 장치이며 Workspace의 목표, Project 기준, 사람의 판단을 소유하지 않는다.

## Workspace 내부 경계

- `workspace.json`: Workspace id와 schema를 가진 machine identity
- `recover.json` schema `4`: Project-root 상대 경로로 Recover가 읽을 `context/project/` 아래 regular Markdown 문서와 선택 이유. Project 공통 진입점인 `context/project/overview.md`를 포함하되 문서 순서는 Workspace가 정한다.
- `verify.json` schema `2`: Verify가 연결할 구체적인 claim, 그 claim의 Project canonical basis, 고정 argv, evidence와 실행 제한. 사람의 다음 행동은 두지 않는다.
- `current/`: 다음 작업자가 이어받을 현재 유효 context와 machine status. `current/memory/`는 `index.md`, `01-goal.md`, `02-constraints.md`, `03-project-context.md`를 최소 구성으로 가진다. 현재 status schema `3`은 최근 제품 검증의 기계 결과와 receipt cursor만 소유하며, 과거 schema `2`는 기존 기록 복구를 위해 읽기 호환한다.
- `source/`: 이 Workspace가 작업 입력으로 선택한 원문, 변경하지 않은 snapshot, provenance를 분리·보존하는 층. `source/index.md`를 최소 inventory로 두며 별도 원자료가 없으면 그 사실과 Project canonical을 복제하지 않은 경계를 적는다. 원자료의 저자와 정본 권위는 원래 출처에 남으며, Workspace는 선택 범위·사용 시점·무결성·재접근 경로를 관리한다. 현재 판단, 분석, 결정, 실행·검증 기록은 두지 않는다.
- `output/`: Workspace goal을 위해 선택된 현재 산출물을 찾는 층. `output/index.md`를 최소 산출물 지도로 두고, 실제 산출물이 Project root의 코드·문서·테스트에 있으면 복제하지 않고 canonical 상대 경로를 연결한다. Workspace 안에서만 소유하는 goal 산출물은 이 폴더에 직접 둘 수 있다. 아직 선택된 산출물이 없으면 index에 없다고 명시한다.
- `records/`: source와 실제 작업을 바탕으로 만든 분석·결정·실행·검증 기록의 누적층. 분석 메모·후보·비교·탈락안·선택 근거처럼 goal 산출물을 만들고 고른 사람이 읽는 기록은 이 폴더 바로 아래에 날짜와 내용을 드러내어 둔다.
- `records/receipts/`: 기계가 만든 append-only 증거를 종류별로 격리하는 층. 제품 검증은 `verify/`, Harness 자체 검증은 `harness-tests/`, 이식 전 상태 캡처는 `preflight/`를 사용한다. 새 제품 Verify는 `records/receipts/verify/verify-*.json`에 쓰며 `status.json`의 receipt 경로는 Work root 상대다. 이전 flat `records/verify-*.json`만 기존 제품 Verify 증거의 읽기 호환 경로로 허용하고 다른 receipt 종류는 product status에 연결하지 않는다.

## 새 Workspace 생성과 전환

새 Workspace는 이전 Workspace의 후속이어도 자기 goal과 current를 소유하는 독립된 지속 단위다. Active 기본값을 바꾸는 것만으로 이전 Workspace의 내용이 옮겨지지는 않으며, 서로 무관한 새 작업에는 선행 Workspace 관계를 만들지 않는다.

후속 Workspace를 만들 때는 문서나 폴더를 상속하지 않고 새 goal을 기준으로 계속 필요한 의미를 다시 선별한다.

1. 사용자가 정한 새 goal, 완료 장면, 범위와 하지 않을 것을 먼저 고정한다.
2. 현재 Project context와, 새 goal에 실제로 이어지는 이전 Workspace의 current·선택된 output·정확한 source·필요한 record만 확인한다. 관련 이유가 없는 다른 Workspace를 넓게 탐색하지 않는다.
3. 후보마다 그것을 모르면 새 goal, 계속 지킬 제약, 첫 판단, 현재 산출물의 의미 또는 다음 행동이 달라지는지 판단한다. 지금도 유효한지, 원문을 다시 읽어야 하는지, 실제 canonical과 Owner가 어디인지도 함께 확인한다.
4. 다음 재진입에 계속 적용되는 의미는 링크로 대신하지 않고 새 Workspace의 적절한 current Owner에 직접 서술한다. Goal에 관한 의미는 goal에, 계속 지킬 제약은 constraints에, 현재 열린 판단과 다음 행동은 state에 둔다.
5. 원문 전체가 기본 current에는 불필요하지만 특정 판단 전에 직접 읽어야 한다면 `source/index.md`에 원래 canonical과 provenance를 선택한다. Recover가 읽는 current에도 그 exact canonical 경로나 직접 링크, 문서의 역할, 필요한 이유와 읽을 시점을 함께 남긴다. `source/index.md`의 링크나 current의 링크만으로 필수 재진입 의미 자체를 대신하지 않는다.
6. 이전 Workspace만 소유하는 당시 선택 이유나 상세 과정은 복제하지 않고 exact output·record·source를 단방향으로 가리킨다. 새 Workspace 생성 때 무엇을 선택하고 제외했는지 나중에 재검토할 필요가 있으면 그 판단만 새 Workspace record에 남긴다.
7. 관련 있어도 새 goal의 판단과 행동을 바꾸지 않는 과거 상태, 세부 과정, 후보와 실행 기록은 이전 Workspace에 그대로 둔다. 다만 과거의 특정 범주가 후속 Workspace에도 계속 적용된다고 오해할 가능성이 있고 그 오해가 현재 판단을 바꾼다면, 빠진 파일을 전부 열거하지 않고 그 범주와 지금 적용하지 않는 이유·현재 영향만 successor current에 적는다.

새 Workspace를 실제 작업 대상으로 전환하기 전에는 그 Workspace의 bounded Recover만 받은 새 주체를 기준으로 다음을 확인한다.

- 현재 goal, 제약, 실제 상태와 다음 판단을 설명할 수 있는가.
- 이전 작업에서 현재 의미로 이어받은 것과, 계속 적용된다고 오해할 수 있지만 의도적으로 이어받지 않은 범주를 구분할 수 있는가.
- 추가 원문이 필요하다면 무엇을 왜 어느 판단 전에 읽어야 하는지 알 수 있는가.
- 과거 Workspace 전체를 다시 Recover하거나 연쇄적으로 거슬러 올라가지 않고 시작할 수 있는가.

부족하면 Recover가 과거를 더 읽게 하지 않고 새 Workspace의 current와 source 선택을 보완한다. 이 확인은 의미 충분성에 대한 사람과 모델의 검토이며, 파일 존재와 schema validation만으로 통과했다고 주장하지 않는다.

Workspace 생성과 실제 활성화는 별도 결정이다. 새 Workspace를 만들었다는 이유만으로 `index.json`이나 host의 explicit binding을 바꾸지 않는다. 현재 작업을 새 Workspace로 전환하기로 정했으면 이전 Main session에서 binding만 바꾸고 계속하지 않는다. 이전 session을 끝낸 뒤 새 session을 시작하기 전에 active 기본값과 host binding을 successor에 맞추고, 새 Main session이 explicit Workspace id의 bounded Recover로 다시 grounding한다. 이 경계는 이전 session의 background Maintain event가 모두 반영됐다고 보장하지 않으므로, 전환 판단에 필요한 미반영 상태가 보이면 전달 완료로 간주하지 않고 이전 Workspace의 current를 먼저 확인하거나 보완한다.

## Workspace 사이의 참조 경계

- 후속 Workspace는 이전 Workspace의 `current/` 전체를 live dependency로 삼지 않는다. 현재 적용되는 의미는 자기 current에 직접 소유하고, 상세 근거만 정확한 canonical이나 이전 Workspace의 exact artifact로 연결한다.
- 이전 Workspace와 후속 Workspace 사이에 자동 전파, 상호 갱신이나 역전파를 만들지 않는다. 이전 Workspace는 당시 작업의 지속 단위로 남고, 후속 Workspace는 자기 goal에 따라 갱신된다.
- 이전 Workspace가 나중에 자기 goal로 다시 활성화되어 바뀌어도 후속 Workspace가 자동으로 따라가지 않는다. 영향이 생기면 후속 Workspace가 원래 canonical과 현재 사실을 다시 대조해 자기 current를 갱신한다.
- Workspace 밖 Project 전체에도 적용될 수 있는 현재 사실은 Project context 후보로만 다루고 Workspace끼리 복제하거나 동기화하지 않는다. 실제 반영은 [`Project context`](../../project/README.md)의 기존 Owner와 domain canonical, source 권위가 Project 전체 적용을 뒷받침하는지 별도로 판단한 뒤 그 Owner가 결정한다. 여러 Workspace가 사용했다는 사실만으로 Project context에 승격하지 않는다.
- 과거 Workspace의 상세 근거를 읽을 수는 있지만, 새 Workspace가 다른 Workspace의 current를 차례로 복구해야만 이해되는 계승 사슬은 만들지 않는다.
- 이 관계를 표현하기 위해 필수 `parent_workspace_id`, 공통 handoff 문서나 동기화 장치를 전제하지 않는다. 의미는 기존 current·source·output·records Owner에 나누고, 관리 장치는 이 canonical을 참조한다.

`source/`는 Project 전체가 공유하는 실제 공통 맥락인 [`context/project/`](../../project/)를 복제하는 곳이 아니다. Project context의 최소 진입점과 내용 계약은 [`context/project/README.md`](../../project/README.md)가 소유한다. 원자료를 다시 확인해야 할 때 사람이 필요한 항목만 선택해서 읽으며, `recover`는 `source/` 전체나 inventory를 기본 recovery packet에 싣지 않는다.

Source 항목에는 가능한 범위에서 원래 위치나 URL, 확보 시각과 방법, commit·version·SHA-256 같은 안정적인 식별 근거를 함께 둔다. 해석이나 결론이 생기면 source를 고치지 않고 `current/` 또는 `records/`에 분리한다.

`output/`은 `records/`에서 일부 파일을 자동 승격하거나 복제하는 archive가 아니다. 사람이 goal의 현재 결과로 선택한 산출물과 canonical 위치를 보여 주며, 선택 이유와 이전 후보는 `records/`에 남긴다. `output/`에 있다는 사실만으로 검증 통과, 사람의 수락, Workspace 완료가 되지 않는다. `recover`는 `output/index.md`만 기본 packet에 싣고 연결된 산출물 본문은 필요할 때 선택해서 읽게 한다.

작업 중 반복 확인은 가능한 한 직접 test 명령으로 수행한다. Durable `verify` receipt는 Workspace 상태를 바꾸거나 다음 사람·세션에 검증 근거를 인계할 때 만든다. 작업 중 생긴 목표·판단·다음 행동의 의미 변화는 agent나 main의 Maintain 흐름이 사람용 current·records에 반영하고 main이 검토한다. 실행된 verify는 성공·실패 모두 사건이므로 자동 삭제하거나 같은 hash라는 이유로 합치지 않는다. 이 구분은 사람용 탐색과 불필요한 누적을 줄이는 운용 기준이며, retention 자동화는 아직 제공하지 않는다.

관리 장치의 책임별 목적·입력·출력은 [`Recover`](../harness/recover/), [`Maintain`](../harness/maintain/), [`Verify`](../harness/verify/)가 각각 정의한다. Harness 자체 회귀 검증은 [`Harness validation`](../harness/validation/)이 소유한다.
