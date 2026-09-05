# Project context

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

## 이 Reference sample의 현재 배치

- [`common/prd.md`](common/prd.md): 지속되는 제품 목적·사용자 장면·완료 기준·범위의 normative Owner
- [`current/architecture.md`](current/architecture.md): 교체되는 현재 구현 구조·지원 경계·검증 경로의 지도
- [`guidance/README.md`](guidance/README.md): 현재 별도 조건부 guidance가 없다는 명시적 상태와 추가 조건
- [`decisions/0001-default-timeout.md`](decisions/0001-default-timeout.md): 기본 timeout의 선택 이유이면서 해당 값의 명시적 normative Owner

## 내용 복원 완료 조건

Project context를 새로 만들거나 크게 재구성한 뒤에는 구조와 link만 확인하지 않는다. 관련 작업을 처음 보는 주체가 이 README와 그 작업이 선택한 실제 문서만으로 다음을 설명할 수 있어야 한다.

- 제품의 사용자 장면·목적과 성공 기준
- 현재 범위와 목표·미구현·범위 밖의 차이
- 판단을 바꾸는 주요 domain 관계나 불변성
- 현재 지원·미지원 경계, 상세 구현 Owner와 검증의 증명 상한
- 이번 작업에 적용되는 판단 기준과 현재 normative 결정

답하려면 상세 Owner를 새로 탐색해 제품 의미를 조립해야 하거나 선택 문서가 경로만 나열한다면 Project context는 미완성이다. 그 뒤 상세 Owner를 열어 재서술한 사실·범위·authority가 맞는지 대조한다. 이 의미 충분성은 Recover schema가 자동 판정하지 않는다.

## Authority와 변경 경계

기존 README·STATUS·docs가 상세 제품 사실을 소유하는 Project에서는 그 문서를 domain canonical로 유지한다. Project context는 여러 Workspace의 판단에 필요한 의미를 실제 내용으로 다시 서술하되 원문을 문단째 복제하거나 Owner를 이동하지 않는다. 기존 Owner를 `context/project/`로 완전히 옮기는 것은 별도의 승인된 Owner migration이다.

한 Workspace에만 해당하는 목표·현재 상태·분석·후보·검증 이력은 이 층으로 올리지 않는다. 첫 Workspace의 작업 장면도 상세 Owner가 Project 전체에 적용됨을 뒷받침할 때만 Project context로 일반화한다.

개별 Workspace는 이 디렉터리 전체를 기본 입력으로 읽지 않는다. [`../work/workspaces/`](../work/workspaces/)의 각 `recover.json`이 이 README와 현재 작업에 필요한 실제 문서, 선택 이유를 Project-root 상대 경로로 명시한다.

제품 코드와 테스트는 이 경계의 내용이 아니며 각각 [`../../src/`](../../src/)와 [`../../tests/`](../../tests/)가 소유한다. Harness와 skill은 이 계약을 선택·적용·검사하는 교체 가능한 관리 장치이며 Project 의미나 사람의 acceptance를 소유하지 않는다.
