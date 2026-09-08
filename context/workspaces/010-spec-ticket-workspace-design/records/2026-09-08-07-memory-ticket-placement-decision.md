# memory 유지와 Ticket 정의·진행 함께 관리 결정

날짜: 2026-09-08

## 사용자 선택

[memory 유지·제거 제3 리뷰](2026-09-08-05-memory-ticket-independent-review.md)와 [Ticket 기록 보존의 배치 후보](2026-09-08-06-ticket-preservation-placement-candidate.md)를 논의한 뒤 사용자는 다음과 같이 정했다.

> 그래 일단 memory 에 두고 그렇다고현 재상태 이런걸 너무 억지로 분리하려한다깁보다 아까 말한대로 ticket안에서 그냥 정의랑 같이 적어서 자연스레 남기고 뭐 필요하면 records에두고 하는 식으로 하자

## 이번에 정한 방향

- memory를 유지하고 Ticket을 `current/memory/tickets/`에 둔다. Spec의 기존 `memory/spec/` 배치와 project-context 유지도 이어간다.
- Ticket의 작업 정의와 진행 상태를 같은 Ticket 안에서 함께 관리한다. 진행·막힘·결과처럼 그 작업을 이해하는 데 필요한 내용을 변경 빈도나 ‘현재 상태’라는 이유만으로 state에 떼어내지 않는다.
- state는 Workspace 전체의 현재 상황·판단·다음 행동을 맡는다. 종합 판단에 필요한 Ticket 상황을 언급할 수 있지만 같은 Ticket 상태를 별도의 정본으로 다시 관리할 필요는 없다.
- Ticket은 작업 문서로 유지하며 필요하면 수정하고 결과를 남긴다. 상세 과정·변경 이유·보존할 내용은 필요에 따라 records에 둔다. 완료 여부나 현재 영향 유무만으로 자동 이동·삭제하는 규칙은 정하지 않는다.
- 직전 예시의 `records/tickets/` 폴더, 반드시 이동할 시점, 매 수정의 사본·revision 발행은 이번 결정에 포함하지 않는다. 필요한 기록을 남기는 구체적 방식은 실제 작업과 후속 설계에서 정할 수 있다.

## 기존 역할과의 관계

이 선택은 memory를 변경이 적은 문장만 담는 곳으로 엄격히 해석하지 않는다. 해당 Workspace에서 유지하며 사용하는 Ticket 문서에 정의·진행을 함께 적을 수 있게 한다. 제3 리뷰에서 지적했듯 기존 memory/state의 내용 구분을 일부 조정하는 선택이며, 기존 계약이 이미 이 배치를 허용했다고 소급해 설명하지 않는다.

records에서 지금 적용할 의미를 골라 현재 문서에 반영하는 역할은 유지한다. 다만 Ticket을 함께 읽고 갱신하는 데 필요한 내용을 억지로 나누거나, 현재 영향이 약해졌다는 이유로 매번 파일을 옮기는 운영 의무를 만들지 않는다. Workspace별 독립 스냅샷과 필요할 때 내부 수정 가능하다는 조건도 유지한다.

## 남은 작업과 적용 범위

Ticket의 구체적인 구성, 새 세션·개별 실행자에게 읽힐 내용, Spec·Ticket·state 갱신 책임과 실제 Reference 적용이 남아 있다. memory 유지 여부와 Ticket의 정의·진행 통합을 다시 미결정 후보로 돌리지 않는다.

이번에는 010의 결정 기록과 재진입 문서를 갱신했다. 연구 Workspace 자체의 memory.md/state.md 구조, 실제 Reference 파일·Recover·Maintain·Verify·schema·hook은 변경하지 않았다.

## 후속 선택: Matt Ticket을 기본으로 삼되 구성을 열어 둔다

Main이 다음 단계로 Ticket의 네 부분(할 일, 필요한 입력·선행 작업, 완료 판단, 진행·결과)을 제안하자 사용자는 다음과 같이 정했다.

> 이건 너무 확정하진말고 matt ticket 정도 따르고 좀 열어놓자

Ticket은 Matt의 `to-tickets` 구성을 기본 참고로 삼되 고정된 필수 항목이나 별도 schema로 확정하지 않는다. 직전 Main의 네 부분 역시 확정 목록이 아니다. 제목·만들 동작·완료 조건·선행 Ticket·상태 등을 출발점으로 두고, 실제 작업에 따라 필요한 맥락과 결과를 보완하거나 구성을 조정한다.

참고한 것은 사용자가 지정한 한국어 독해본과 그 원본 commit `068b6e0c62393147daf03530149cdce209c93da8`의 [to-tickets](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/skills/engineering/to-tickets/SKILL.md)다. 로컬 template의 What to build·Blocked by·Status·acceptance checklist를 확인했다. 이번 선택을 tracker 게시, 특정 저장 경로·상태 이름, 한 세션 크기 등 해당 skill의 모든 운영 규칙 채택으로 확대하지 않는다.

memory에 두고 정의·진행을 함께 적으며 필요하면 records를 사용하는 결정은 유지한다. Ticket 항목을 모두 확정하는 절차를 다음 설계의 선행 조건으로 두지 않고, 다음에는 읽기·갱신 책임을 논의할 수 있다.
