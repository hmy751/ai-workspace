# Maintain

Maintain은 작업 중 생긴 의미 있는 변화를 선택한 Workspace의 지속 Context에 맞게 반영하는 Harness 관리 책임이다. Context의 의미나 책임 Owner를 새로 정하지 않으며, [`Work context`](../../README.md)와 [`Workspace collection`](../../workspaces/README.md), 선택한 Workspace의 README가 소유한 기존 경계를 적용한다.

Codex에서 이 책임을 수행하는 현재 adapter는 [`workspace-context-maintainer.toml`](../../../../.codex/agents/workspace-context-maintainer.toml)이다. 이 adapter는 교체 가능한 실행 장치이며 Maintain 계약이나 Workspace Context의 정본이 아니다.

## 활성 시점

Maintain은 새 세션이 시작될 때 자동으로 실행하는 복구 절차가 아니다. 작업을 이어 가는 동안 다음과 같은 의미 변화가 생겼고, 그 변화가 다음 행동이나 이후 재진입에 영향을 주는 자연스러운 작업 경계에서 한 번 수행한다.

- 목표·제약·현재 문제·불확실성·작업 cursor·다음 행동이 달라졌다.
- 이후 다시 사용할 분석·결정·실패·검증 해석이 생겼다.
- 작업에 선택한 source와 provenance 또는 현재 goal 산출물의 선택 관계가 달라졌다.
- 사용자 정정, 실제 diff, 파일 상태, test 결과 때문에 기존 Context가 낡았을 가능성이 생겼다.

일회성 명령이나 반복 test가 끝날 때마다 실행하지 않는다. 새 작업 주체의 재진입은 Recover가, 상태 전환·인계에 남길 제품 검증 증거는 Verify가 담당한다. 같은 작업 경계에서 Maintain과 Verify가 모두 필요할 수 있지만 서로를 대신하지 않는다.

## 호출 입력

호출하는 main은 다음 입력을 경계가 분명한 작업 묶음으로 제공한다.

- 대상 `workspace_id`. 명시 입력이 필수이며 active 기본값으로 추정하지 않는다.
- 이번 경계에 영향을 주는 사용자 정정과 이미 내려진 결정, 아직 열려 있는 판단.
- 관련 diff·파일·Git 상태와 실제 산출물 위치.
- 관련 test 또는 Verify 결과와 그 결과가 입증하는 범위.
- 이번 호출에서 허용한 수정 범위와 보존해야 할 사용자 변경.

대상 Workspace가 빠졌거나 입력끼리 충돌하거나 새로운 목표·canonical·acceptance를 결정해야 한다면 임의로 보완하지 않고 `unresolved`로 main에 돌려보낸다.

## 읽기와 갱신 경계

Maintain은 이 문서가 연결한 Work·Workspace 계약을 관리 기준으로 읽은 뒤, **명시된 Workspace와 main이 제공한 근거만** 대조한다. 다른 Workspace, active index, 저장소 주변 자료를 기본 탐색하지 않는다.

변경이 필요한 의미만 기존 Owner에 한 번 반영한다.

- `current/`: 지금도 유효하여 다음 행동에 필요한 목표·제약·현재 상태·불확실성·cursor를 해당 memory 또는 state 문서에 둔다. 끝난 과정과 상세 증거를 누적하지 않는다.
- `records/`: 이후 다시 판단할 가치가 있는 분석·결정·실패·검증 해석을 사람이 읽는 날짜별 기록으로 남긴다. Verify receipt를 만들거나 고치지 않는다.
- `source/`의 provenance와 index: 선택한 원자료의 범위·출처·시점·무결성·재접근 경로만 갱신한다. 보존한 raw snapshot의 본문은 절대 다시 쓰지 않는다.
- `output/index.md`: 현재 goal을 위해 선택된 산출물과 실제 canonical 위치만 연결한다. 산출물을 복제하거나 선택을 acceptance로 해석하지 않는다.

모든 층을 매번 수정하지 않는다. 같은 사실을 여러 층에 반복하지 않고 상세 근거는 records나 실제 canonical을 연결한다. 각 층의 세부 의미와 내부 관계는 [`Workspace collection`](../../workspaces/README.md)과 선택한 Workspace README에서 확인한다.

## 소유하지 않는 것

Maintain은 다음을 수행하거나 결정하지 않는다.

- Project 제품 코드·제품 문서·제품 test 수정
- `workspace.json`, `recover.json`, `verify.json` 같은 machine 실행 계약 변경
- Verify receipt 또는 `current/state/status.json` 생성·수정·삭제
- `workspaces/index.json` 조회·active 선택·active 변경
- 사용자 대신 목표·source 권위·설계 기준·acceptance·완료를 결정하는 일
- 파일 stage, commit, push 또는 외부 쓰기
- Maintain용 Python CLI, 별도 schema, machine status 생성

허용 범위 밖의 변경이 필요해 보이면 그 필요와 근거만 `unresolved`로 보고한다.

## 결과와 main 검토

실행 주체는 수정 뒤 로컬 링크와 Markdown 줄 끝 공백을 확인하고 다음 필드를 짧게 반환한다.

- `context_status`: `current`, `updated`, `needs_user_decision` 중 하나
- `workspace`: 실제로 점검한 명시적 Workspace id
- `changed`: 수정·추가한 파일과 각 변경 이유
- `evidence`: 각 판단에 사용한 사용자 정정, diff·파일, test·Verify 결과와 입증 범위
- `unresolved`: 입력 충돌, 누락 근거, main이나 사용자가 결정할 사항

이 보고는 acceptance가 아니다. Main은 제공한 사용자 결정과 실제 evidence를 기준으로 범위, diff, 링크, 과장된 검증 주장이 없는지 검토한 뒤 적용 여부와 다음 행동을 결정한다.

## 교체와 제거

Maintain의 지속 기준과 Workspace의 의미는 이 agent adapter 안에 있지 않다. Adapter를 제거하거나 다른 사람·AI·도구로 교체해도 이 README에서 시작해 Work·Workspace canonical을 적용하면 같은 책임을 수행할 수 있다. 따라서 adapter 교체를 위해 Context 구조나 각 Workspace의 의미를 다시 만들 필요가 없다.
