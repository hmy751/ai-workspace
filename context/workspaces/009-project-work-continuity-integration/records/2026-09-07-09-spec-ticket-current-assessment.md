# Spec·Ticket과 Work current의 책임 비교

확인일: 2026-09-07. 로컬 기준 revision: `5e45310`. 공개 공식 문서와 live Reference를 읽은 설계 검토이며, 도입 합의나 구현·효과 검증이 아니다.

## 다시 열린 질문

사용자는 “spec, ticket 개념이 필요해보여 이건 외부 레퍼런스 찾아봐”, “work내 current 와 너무 겹쳐서”라고 하며 특히 goal을 포함한 구조 변경 규모에 대한 의견을 요청했다. 이전의 Workspace·Spec 논의 보류를 이번 공개 자료 조사와 의견 제시까지 연 것으로 해석한다. 새 구조 설치나 외부 target 변경을 요청한 것으로 해석하지 않는다.

## 외부에서 확인한 역할

- [Kiro Specs](https://kiro.dev/docs/specs/): AI 개발 도구 Kiro는 요구와 수락 기준, 기술 설계, 실행 항목을 각각 `requirements.md`, `design.md`, `tasks.md`로 나눈다. 여기서 Spec은 문서 묶음도 가리킨다. 문서 표기 갱신일은 2026-08-27이다.
- [GitHub Spec Kit](https://github.com/github/spec-kit/blob/main/spec-driven.md): AI 명세 개발 도구의 공식 설명은 feature specification, implementation plan, executable task list를 구분한다. 기능별 폴더 안에 관련 산출물을 묶는다. `main`에서 열람했으며 revision은 고정하지 않았다. 문서가 주장하는 자동화 효과를 실증 결과로 채택하지 않는다.
- [OpenSpec Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md): 명세 중심 변경 관리 도구 OpenSpec은 합의된 시스템 동작을 나타내는 `specs/`와 변경 제안을 담는 `changes/`를 나눈다. 변경 폴더는 proposal·design·tasks·변경 명세를 포함하고, archive 시 변경 명세를 본 명세에 반영하는 구조다. `main`에서 열람했으며 revision은 고정하지 않았다.
- [GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues): 저장소의 작업 추적 기능이다. 구현 항목뿐 아니라 버그·아이디어·논의를 추적하고, 담당자·하위 항목·작업 간 차단 관계를 표현한다. Ticket을 정식 Spec 뒤에만 만들 수 있는 구현 조각으로 제한할 근거는 없다.

이 사례들에서 가져올 구분은 기대 동작·수락 조건, 기술적 접근, 독립적으로 추적할 실행 항목이다. Spec이라는 단어의 범위와 보존 수명은 도구마다 다르므로 하나의 폴더 계층을 보편 규칙으로 가져오지 않는다. 특히 Spec을 안정된 구현 구간에만 쓰고 버리는 임시 문서로 제한할 이유는 없다.

## 현재 Reference와 실제 겹침

- [Project 제품 기준](../../../../reference-project/context/project/common/prd.md)은 이미 여러 Work에 지속되는 제품 목적·사용자 장면·완료 기준의 정본이다. 파일 이름이 PRD여도 명세 역할 일부를 수행한다.
- [Workspace goal](../../../../reference-project/context/work/workspaces/001-default-timeout/current/memory/01-goal.md)은 이번 작업 목표와 완료 기준을 직접 담는다. 예시에는 timeout 동작뿐 아니라 receipt 복구와 사람 수락도 포함되어 있다. 별도 Spec에 같은 상세 요구를 독립적으로 쓰면 정본이 겹친다.
- [사람용 state](../../../../reference-project/context/work/workspaces/001-default-timeout/current/state/index.md)는 지금 문제·근거 해석·다음 행동을 소유한다. Spec과 Ticket이 있어도 이 재진입 책임은 남는다.
- [machine status 계약](../../../../reference-project/context/work/harness/workspace_contract.py)의 상태와 필드는 최근 검증 및 receipt에 한정된다. 조사한 live Workspace·Project·생성 계약에는 담당자·backlog·작업별 의존·진행을 소유하는 독립 Ticket 체계가 없다. 검증 JSON을 Ticket 상태로 확장하면 다른 책임이 섞인다.

## Main의 제안 — 미채택

Spec과 Ticket의 역할을 사용할 수 있도록 하고, 별도 정본을 두는 경우 current가 소유하던 중복 책임을 넘기는 방향이 타당하다. 현재 구조 위에 같은 내용을 추가하기만 하면 관리 부담이 커진다.

- Spec은 해당 기능이나 변경이 만족해야 할 동작·범위·수락 조건을 소유한다. 기존 Project 정본이 그 역할을 충분히 수행하면 재사용한다. 장기 시스템 명세와 이번 변경 제안의 권위를 구분한다.
- Ticket은 별도로 맡기고 보류하고 완료를 추적해야 하는 작업의 범위·담당·의존·상태·완료 근거를 소유한다. 간단한 단일 작업은 별도 Spec 없이 Ticket 안에 조건을 담을 수 있다.
- Work goal은 이번 Workspace가 달성할 결과와 책임 범위를 소유한다. 상세 기능 조건은 필요한 Spec 부분을 가리키되, 재진입에 필요한 핵심 의미와 이번 Work의 완료 판단은 직접 설명한다.
- Current는 적용하는 요구·선택한 작업·현재 판단·막힌 이유·다음 행동을 복원한다. Ticket 목록 전체나 상세 요구를 독립 편집하는 두 번째 정본으로 만들지 않는다. 핵심을 요약해 적는 것과 원본을 중복 소유하는 것은 구분한다.

예를 들어 같은 기능 명세를 두고 한 Workspace는 설계를 결정하고, 다른 Workspace는 일부 구현과 검증을 맡을 수 있다. 반대로 작은 변경에서는 하나의 Ticket과 Workspace가 같은 범위를 가질 수 있다. `Workspace = Ticket`이나 `Project > Spec > Ticket > Workspace` 같은 고정 관계는 아직 필요하지 않다. Ticket을 모두 닫았다는 사실만으로 Spec 조건 성립이나 Work 전체 수락이 되지도 않는다.

## 변경 규모를 가르는 실제 경계

1. **기존 경로에서 책임을 정리하는 경우:** `01-goal.md`를 유지하고 적용 명세·이번 범위·완료 판단을 분명히 한다. Markdown 본문을 runtime이 구조 파싱하지 않으므로 이 수준은 runtime 변경 없이 시도할 수 있다. 다만 current를 링크 목록으로만 바꾸면 기존의 독립 재진입 계약을 만족하지 못한다.
2. **정본을 따로 만드는 경우:** Spec 수명과 Ticket 관리 위치, 원본 수정 주체, current 요약을 갱신할 조건을 함께 정해야 한다. 작업 중인 Spec을 무조건 Project 공통 맥락으로 올리지 않으며, 외부 issue tracker가 정본이면 로컬 복제본을 다시 관리하지 않는다.
3. **자동 읽기·갱신까지 통합하는 경우:** [Recover](../../../../reference-project/context/work/harness/recover/operation.py)는 `01-goal.md` 등 필수 파일과 memory 바로 아래 Markdown을 읽고, [Maintain](../../../../reference-project/context/work/harness/maintain/operation.py)은 허용된 경로만 갱신한다. 별도 `specs/`·`tickets/`의 자동 선택·갱신, goal 파일 제거는 runtime·계약·검증 변경이 필요하다. 모든 Ticket을 memory에 넣는 우회는 재진입 때 전체를 읽는 비용을 만든다.

권장 다음 판단은 실제 변경 하나를 같은 입력으로 놓고 기존 current만 쓴 배치와 Spec·Ticket을 분리한 배치를 비교하는 것이다. 상세 요구 수정이 한 정본에서 끝나는지, 별도 실행자가 범위와 완료 조건을 복원하는지, 다음 Recover에서 현재 판단과 미완료 이유를 잃지 않는지를 확인한다. 이를 거쳐 필수 구조와 자동화 범위를 결정한다. 이번에는 비교·의견만 제시했으며 이 배치를 구현하거나 동작 검증하지 않았다.
