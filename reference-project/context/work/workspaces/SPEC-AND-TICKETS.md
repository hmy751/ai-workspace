# Workspace의 Spec과 Ticket

이 문서는 Workspace 안에서 Spec·Ticket의 내용, state와의 관계, 읽기·유지 기준을 정의한다. Workspace 전체의 범위와 source·output·records 관계는 [Workspace collection](README.md)이 소유한다. 실제 작업 내용은 각 Workspace의 `current/`에 두며, 이 운영 문서를 작업별 Spec에 복제하지 않는다.

Spec은 이번 작업이 이루려는 결과와 판단 기준을 정의한다. Ticket은 그 결과를 위해 실행할 일을 식별하고 정의·진행·결과를 함께 남긴다. Workspace는 이 문서들과 전체 상황, 원자료, 산출물과 기록을 함께 유지하는 작업 범위다.

## 현재 구성과 진입

일단 Workspace에서 Spec 하나를 구성하는 형태를 사용한다. 이는 Spec 개수 제한이나 새 Spec마다 새 Workspace를 강제하는 정책이 아니다.

```text
current/
├── memory/
│   ├── index.md
│   ├── spec/
│   │   ├── 01-problem-goal-scope.md
│   │   ├── 02-behavior-and-cases.md
│   │   ├── 03-concepts-and-contracts.md
│   │   ├── 04-quality-and-completion.md
│   │   └── 05-constraints-design-assumptions.md
│   ├── tickets/
│   │   ├── index.md
│   │   └── <ticket>.md
│   └── project-context.md
└── state/
    ├── index.md
    └── status.json
```

`memory/index.md`는 다섯 Spec 파일, Ticket 색인, Project context 선택과 필요한 추가 memory를 연결한다. Spec이 기존 `01-goal.md`와 작업별 `02-constraints.md`를 대체하므로 같은 작업 정의를 따로 유지하지 않는다. `project-context.md`는 이번 작업에 선택한 Project 맥락과 그 이유를 계속 맡는다.

일반 Workspace 재진입은 memory 색인, Spec 전체, Project context 선택과 추가 memory, Ticket 색인, state, output 색인, 선택한 Project 본문을 읽는다. Ticket 색인에서 지금 판단에 필요한 본문을 골라 이어 읽는다. 색인은 제목·하는 일·본문 경로를 안내하며 개별 진행 상태의 두 번째 정본으로 만들지 않는다. Ticket이 없으면 없다고 적는다. 실행할 Ticket을 정하거나 그 결과를 판단할 때는 본문을 직접 확인한다.

이것은 일반 재진입의 기본값이다. 개별 Ticket 실행자에게 읽힐 Spec 범위와 자료, 직접 갱신할 문서는 실제 위임에 맞게 정한다. 모든 Ticket을 위임하거나 새 세션에서 실행하는 절차를 강제하지 않는다. [Recover](../harness/recover/README.md)는 위 기본 packet을 만들고, 필요한 본문의 추가 선택은 작업 주체가 한다.

## Spec의 다섯 구성요소

### 문제·목표·범위

`01-problem-goal-scope.md`에는 해결하려는 문제, 사용자가 얻을 결과, 포함·제외 범위와 중요한 선행 조건을 적는다. 이 파일이 Workspace의 작업 목표를 맡는다. 기반 코드나 일부 Ticket의 완료가 전체 기능의 완료로 바뀌지 않도록 실제로 이루려는 결과를 드러낸다.

### 요구 동작과 대표 사례

`02-behavior-and-cases.md`에는 요구 동작과 제품에서 보존해야 할 의미를 적고, 그 의미를 구별하는 대표 사례를 둔다. 가능한 상황을 모두 열거하기보다 비슷해 보이지만 결과가 달라야 하는 경우를 보여 준다. 작은 작업은 몇 문장으로 충분할 수 있다.

### 핵심 개념·입출력 계약

`03-concepts-and-contracts.md`에는 작업을 나누고 전달할 때 같은 뜻으로 다뤄야 할 대상, 입력과 결과의 관계를 적는다. 필요한 오류·부분 결과도 포함한다. 모든 작업에 JSON이나 상세 데이터 모델을 요구하거나 내부 클래스까지 미리 고정하지 않는다.

### 품질·완료 판단

`04-quality-and-completion.md`에는 목표를 이뤘다고 판단할 실제 결과와 근거를 적는다. 제품 원자료가 요구하는 의미와 실제 동작을 비교하고, 이번 목표에 관련된 변경 전후 코드에서 책임·중복·미룬 핵심 동작을 살핀다. 개별 Ticket이나 테스트 통과만으로 전체 완료를 판단하지 않는다. 확인한 사실, 보고받은 내용, 미확인 범위를 구별한다. 모든 Ticket마다 제품 전체를 다시 검토하는 의무는 아니다.

### 제약·현재 설계·가정

`05-constraints-design-assumptions.md`에는 지킬 조건, 현재 선택한 방법과 이유, 아직 확인이 필요한 전제를 구별해 적는다. 다음 주체가 현재 설계나 가정까지 고정 제약으로 받아들이지 않게 한다. 새로운 사실이 선택 이유를 흔들면 다시 판단한다. 구현이 빠졌다는 사실만으로 목표를 낮추거나 기존 구현에 Spec을 맞추지 않는다.

## Ticket의 내용과 유지

Ticket은 제목, 만들 동작, 완료 조건, 선행 작업·막힘, 진행 상태·결과를 필요에 맞게 담는다. 이 항목은 Matt Pocock의 작업 분해 skill [to-tickets](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/skills/engineering/to-tickets/SKILL.md)를 참고한 구성 방향이며, 고정 필드나 상태 이름, 특정 tracker를 요구하지 않는다. Spec의 관련 부분과 실행에 필요한 원자료·코드·결과를 연결한다.

정의와 진행을 같은 Ticket 본문에 함께 적고 필요한 때 갱신한다. 새 Ticket은 `tickets/index.md`에서 찾을 수 있게 한다. 상태가 바뀐다는 이유로 정의와 진행을 서로 다른 문서로 강제 분리하지 않는다. state는 전체 Workspace의 현재 상황·판단·다음 행동을 맡고 필요한 Ticket 상황을 종합한다. `status.json`은 제품 Verify의 기계 결과만 맡으며 Ticket 상태 저장소가 아니다.

완료한 Ticket도 자연스럽게 남길 수 있다. 상세 이력·변경 이유·과정을 보존할 필요가 있으면 records를 사용한다. 완료나 현재 영향 유무만으로 자동 이동·삭제하지 않으며 매번 불변 사본을 만들지 않는다.

## 갱신과 작업의 연속성

Spec·Ticket은 memory에 유지하며 작업 중 필요하면 고친다. Workspace와 함께 스냅샷처럼 남고, 후속 Workspace나 Project의 변화에 맞춰 계속 최신화할 의무는 없다. 다른 Workspace에서 필요한 의미를 새로 구성해도 서로 자동 전파하거나 공유 정본에 매달리지 않는다. 이 독립성은 작업 중 수정을 막는 불변성 규칙이 아니다.

기존처럼 Main은 필요한 설계·작업 분해·위임·결과 확인·다음 행동을 조율한다. [Maintain](../harness/maintain/README.md)은 대화와 결과를 이해해 무엇을 남길지 판단하고 Spec·Ticket·state와 필요한 records를 기록·갱신한다. 기록은 단순 전사나 records 작성에 한정되지 않는다. Main만 문서를 작성할 수 있다는 규칙도 아니다.

실행 결과로 판단이 바뀌면 영향받는 요구·설계·가정과 Ticket, 전체 state에 그 의미를 반영한다. 목표나 source 권위에 대한 미해결 선택을 완료 보고로 덮지 않는다. 중요한 변경 이유와 실제 근거는 필요에 따라 records에 남긴다. 유지 방식이 제품 검증이나 사용자 acceptance를 대신하지 않는다.

다른 실행자의 결과가 Main에게 도착한 것만으로 Maintain에 전달된 것은 아니다. Main은 다음 판단에 필요한 결과·출처·미확인 범위 또는 정확한 로컬 결과 문서를 대화에 연결한다. 문서를 실행자에게 읽히기 전에는 필요한 내용이 실제 파일에 반영됐는지 확인한다. 비동기 접수와 문서 준비를 구별하되 모든 갱신에 새 승인이나 조율 절차를 만들지 않는다.
