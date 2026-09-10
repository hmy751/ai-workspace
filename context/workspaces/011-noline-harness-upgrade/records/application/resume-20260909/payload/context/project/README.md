# Noline Project context

이 디렉터리는 여러 Workspace가 공유하는 실제 Project-wide 판단 context를 소유한다. 기존 제품 문서의 복사본이나 링크 목록이 아니라, 다음 관련 작업이 제품 목적·사용자 문제·현재 현실과 관련 판단 기준을 다시 추론하지 않게 하는 내용 층이다.

## 물리 구조

```text
context/project/
├── README.md
├── common/                 # 여러 Work에 지속되는 제품·domain 의미
├── current/                # 교체되는 현재 구현·지원·proof 경계
├── guidance/               # 관련 작업에서만 적용하는 조건부 판단 기준
└── decisions/              # 중요한 선택의 이유와 재검토 신호
```

`common/`, `current/`, `guidance/`는 설명용 profile이 아니라 Project context의 필수 탐색 경계다. 각 폴더의 `README.md`는 그 층의 책임과 현재 문서 위치를 소유하며, 실제 본문 수는 Project에 맞게 달라질 수 있다. 적용할 guidance가 없어도 `guidance/README.md`에 그 사실과 추가 조건을 남겨 세 책임의 존재 여부를 다시 추측하게 하지 않는다.

`decisions/`는 네 번째 현재 책임 층이 아니다. 현재 답 자체보다 중요한 선택의 이유·기각안·재검토 신호를 보존하는 보조 경계다. Project context의 새 본문은 root에 평면 파일로 만들지 않고 주 책임에 맞는 폴더에 둔다. Root `README.md`만 전체 구조와 권위 관계를 연결한다.

## 읽는 경로

- 제품 목적·사용자 문제·domain 의미·Project-wide 제약은 [`common/README.md`](common/README.md)에서 찾는다.
- 지금 구현·지원되는 범위, 상세 Owner와 검증의 증명 상한은 [`current/README.md`](current/README.md)에서 찾는다.
- 특정 종류의 작업에만 적용할 반복 판단 기준은 [`guidance/README.md`](guidance/README.md)에서 찾는다.
- 현재 답보다 선택 이유와 재검토 신호가 필요하면 [`decisions/README.md`](decisions/README.md)에서 찾는다.

모든 Workspace의 `recover.json`은 이 root `README.md`를 안정된 routing anchor로 선택한다. README만으로 작업에 필요한 내용이 충분하다고 보지 않으며, 현재 goal의 판단을 바꾸는 `common/`, `current/`, `guidance/`, `decisions/`의 실제 문서만 이유와 함께 추가 선택한다. Project context 전체나 모든 층을 자동으로 읽지 않는다.

## 층별 책임

### `common/`

작업이 바뀌어도 계속 필요한 제품 목적, 사용자 장면, domain 관계·불변성, 제품 기준과 Project-wide 제약을 둔다. 구현 현황이나 한 Workspace의 목표를 섞지 않는다. 제품 의미를 바꾸는 주체가 갱신하며, 기존 상세 canonical을 옮기지 않은 경우에는 그 Owner와 충돌 우선순위를 함께 밝힌다.

### `current/`

현재 구현·지원·미지원 범위, 연결 구조, 위험과 proof boundary처럼 상세 Owner 변화에 맞춰 교체해야 하는 Project-level 지도를 둔다. 마지막 대조 시점·대상, 상세 코드·테스트 Owner, stale 신호와 갱신 책임을 찾을 수 있어야 한다. 현재 지도가 실제 Owner와 충돌하면 실제 Owner를 기준으로 claim 범위를 좁히고 이 층을 갱신한다.

### `guidance/`

특정 종류의 Work에서만 반복해서 판단이나 행동을 바꾸는 Project-wide 지침을 둔다. 각 지침은 적용 조건, 비적용 조건, 재검토 신호와 제거 조건을 밝힌다. 단지 유용해 보이는 조언이나 모든 작업이 이미 지키는 공통 의미를 guidance로 승격하지 않는다.

### `decisions/`

중요한 선택이 왜 만들어졌고 어떤 조건에서 다시 열어야 하는지 보존한다. 기본적으로 `common/`, `current/`, `guidance/`의 현재 답을 대신하지 않는다. 문서가 특정 현재 값의 normative Owner임을 명시한 경우에만 그 범위의 현재 답을 소유한다.

## Noline의 현재 배치

- [`common/product.md`](common/product.md): 여행 중 일정·경비를 이어갈 사용자 목적, 활성화된 여행의 데이터 관계와 공통 제약
- [`current/architecture.md`](current/architecture.md): client·server·schema·UI의 현재 책임, 지원 경계와 검증 경로
- [`guidance/README.md`](guidance/README.md): 기존 Noline rule·guard·runbook Owner와 조건부 설명 기준의 소비 관계
- [`decisions/0001-selective-local-first.md`](decisions/0001-selective-local-first.md): Selective Local-First 선택의 근거 요약. 상세 결정은 `.claude/decisions/`가 유지한다.

기존 flat `overview.md`, `prd.md`, `architecture.md`는 최초 이식 당시 본문을 보존하며 현재 authority에서는 내려왔다. 원문을 삭제하거나 상세 제품 Owner를 이동하지 않았다.

## 내용 복원 완료 조건

다음 작업의 이해와 판단에 필요한 근거 있는 맥락은 일부가 불확실하다는 이유로 조용히 빼거나 전체 의미를 약화하지 않는다. 근거가 뒷받침하는 내용은 해당 책임 층에 분명하게 서술하고, 미정·미확인·충돌이 남은 부분은 그 대상과 근거를 구체적으로 밝힌다.

이 기준은 층위와 색인을 갖추고도 코드로 확인하기 쉬운 사실과 방어적 제한만 남겨, 제품 목적·사용자 문제·판단 이유를 다음 작업이 다시 추측하게 되는 실패를 막기 위해 둔다. 제품 의미의 근거는 코드에만 있지 않으며 채택된 제품 자료와 결정에도 있다.

`common/current/guidance`는 내용의 책임을 나누는 층이며 확실성의 등급이 아니다. 현재 사용하는 제품 이해와 그 안의 열린 선택을 함께 설명할 수 있다. 예를 들어 대표 사용자 장면은 구체적으로 남기면서 다음 개발 범위는 아직 정하지 않았다고 밝힌다. 결정되지 않은 선택과 근거를 아직 확인하지 못한 사실은 구분하고, 독자의 이해나 다음 행동을 바꾸는 부분에만 그 차이를 적는다. 모든 문장에 상태 표시를 붙이거나 불확실성을 이유로 별도 층을 만들지는 않는다.

Project context를 새로 만들거나 크게 재구성한 뒤에는 구조와 link만 확인하지 않는다. 관련 작업을 처음 보는 주체가 이 README와 그 작업이 선택한 실제 문서만으로 다음을 설명할 수 있어야 한다.

- 제품의 사용자 장면·목적과 성공 기준
- 현재 범위와 목표·미구현·범위 밖의 차이
- 판단을 바꾸는 주요 domain 관계나 불변성
- 현재 지원·미지원 경계, 상세 구현 Owner와 검증의 증명 상한
- 이번 작업에 적용되는 판단 기준과 현재 normative 결정

답하려면 상세 Owner를 새로 탐색해 제품 의미를 조립해야 하거나 선택 문서가 경로만 나열한다면 Project context는 미완성이다. 그 뒤 상세 Owner를 열어 재서술한 사실·범위·authority가 맞는지 대조한다. 이 의미 충분성은 Recover schema가 자동 판정하지 않는다.

## Authority와 변경 경계

기존 README·STATUS·docs가 상세 제품 사실을 소유하는 Project에서는 그 문서를 domain canonical로 유지한다. Project context는 여러 Workspace의 판단에 필요한 의미를 실제 내용으로 다시 서술하되 원문을 문단째 복제하거나 Owner를 이동하지 않는다. 기존 Owner를 `context/project/`로 완전히 옮기는 것은 별도의 승인된 Owner migration이다.

현재 답을 찾는 canonical에도 근거와 열린 판단이 함께 있을 수 있다. 초안·과거 기록·현재 구현의 존재만으로 제품 요구나 Project-wide 지침이 채택되지는 않는다. 과거 자료는 현재 뜻과 대체 관계를 대조할 근거로 사용하고, 당시 계획을 현재 작업 지시로 되살리지 않는다.

현재 권위가 확인되었거나 사용자가 재구성을 허용한 기존 의미는 출처를 추적할 수 있게 복원한다. 근거 있는 내용의 재서술, 확인된 구현 변화에 따른 현재 요약 갱신, 미정·미확인·충돌의 구체적 보존은 새로운 제품 결정을 내리는 것과 구분한다. 새로운 제품 목적·핵심 domain 의미·중요 제약이나 상충하는 근거 사이의 선택은 사용자 또는 명시된 책임자가 결정한다. 이미 승인된 범위의 반영을 위해 같은 결정을 다시 요청하지 않는다. 미해결 부분이 있으면 그 부분의 확정만 남겨 두고, 근거가 지지하는 나머지 맥락은 보존한다.

한 Workspace에만 해당하는 목표·현재 상태·분석·후보·검증 이력은 이 층으로 올리지 않는다. 첫 Workspace의 작업 장면도 상세 Owner가 Project 전체에 적용됨을 뒷받침할 때만 Project context로 일반화한다.

개별 Workspace는 이 디렉터리 전체를 기본 입력으로 읽지 않는다. [`../work/workspaces/`](../work/workspaces/)의 각 `recover.json`이 이 README와 현재 작업에 필요한 실제 문서, 선택 이유를 Project-root 상대 경로로 명시한다.

Noline의 상세 의미는 root [`CLAUDE.md`](../../CLAUDE.md), [`.claude/context/`](../../.claude/context/), [rules](../../.claude/rules/), [guards](../../.claude/guards/), [runbooks](../../.claude/runbooks/)가 소유한다. 제품 코드와 테스트는 [`apps/`](../../apps/)·[`packages/`](../../packages/)가 소유하며, 충돌 시 상세 Owner와 실제 코드를 대조해 이 층을 갱신한다. Harness와 skill은 이 계약을 선택·적용·검사하는 교체 가능한 관리 장치이며 Project 의미나 사람의 acceptance를 소유하지 않는다.

## 갱신 시점과 관리 장치

현재 작업에서 여러 Workspace의 이해·판단·행동에 계속 영향을 줄 변화가 명확해지거나, 사용자가 누락된 기존 Project 맥락의 복원을 요청하면 [`update-project-context`](../../.agents/skills/update-project-context/SKILL.md)를 사용한다. 일시적인 작업 방법이나 후보 전체를 올리지 않고, 현재도 필요한 의미와 근거를 기존 내용 Owner에 반영한다. 작업 중 변화가 명확해진 경계에서 수행하며 Workspace 종료까지 기다리지 않는다.

현재 Workspace와 그 변화에 필요한 source·record·output, 관련 Project 문서와 상세 Owner만 읽는다. Archive·source는 허용된 조사 범위에서 근거로 다루고 원본을 수정하지 않는다. 중요한 선택 이유를 별도로 남길지는 [`decisions/` 계약](decisions/README.md)에 따른다. 반영한 현재 내용과 근거, 아직 남은 판단, 근거가 있어도 반영하지 못한 내용과 이유를 보고한다.

이 skill은 위 관리 기준을 실행하는 절차를 맡으며 Workspace Maintain과 별개다. Workspace Maintain의 쓰기 범위를 Project 문서로 넓히지 않는다. 현재 Workspace의 Project 선택을 바꿀 필요가 있으면 그 Owner에게 연결하고, Project path·책임·authority 변경으로 live consumer가 영향을 받으면 [`Workspace collection의 reconciliation 계약`](../work/workspaces/README.md)을 따른다. 소비 경로에서 내려온 과거 Workspace는 역동기화하지 않는다.

Skill을 교체하거나 제거해도 사람이 이 README와 각 내용 Owner의 계약을 따라 같은 갱신 책임을 수행할 수 있어야 한다. Skill의 호출 경로는 root [`AGENTS.md`](../../AGENTS.md)가 연결하며, 정적 설치 확인은 실제 session의 discovery·invocation이나 의미 판단의 충분성을 증명하지 않는다.
