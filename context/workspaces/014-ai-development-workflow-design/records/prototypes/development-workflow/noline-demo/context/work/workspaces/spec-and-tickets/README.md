# Work의 Spec·Ticket·state

작업 정의·개별 실행·전체 상황을 구별해 다음 행동에 필요한 내용을 찾는다. 각 Workspace의 `current/memory/spec/` 다섯 파일이 하나의 Spec이다. 파일 수가 다섯이라는 이유로 작업을 다섯 Ticket으로 나누지는 않는다.

- `01-problem-goal-scope.md`: 해결할 문제, 얻을 결과, 포함·제외 범위
- `02-behavior-and-cases.md`: 요구 동작과 결과가 달라지는 대표 사례
- `03-concepts-and-contracts.md`: 함께 이해해야 할 의미·입출력·오류 계약
- `04-quality-and-completion.md`: 결과를 이뤘다고 판단할 근거. 동작 보존과 개선 효과를 구별한다.
- `05-constraints-design-assumptions.md`: 지킬 제약, 현재 선택과 이유, 아직 확인할 가정

Ticket은 그 목표 안에서 한 번의 실행이 맡는 결과, 필요한 맥락·접근, 완료 조건·확인 방법, 현재 상태·실제 결과를 함께 남긴다. 같은 본문의 현재 상태를 갱신하고 상세 이력은 records에서 찾게 한다. 색인은 위치와 맡은 일을 안내하며 별도의 진행 상태 정본이 되지 않는다.

`current/state/index.md`는 Work 전체의 현재 상황과 다음 행동을 종합한다. 모든 Ticket의 정의와 상세 이력을 복제하지 않는다. 작업 담당자는 새 근거가 목표·계약·선택을 바꾸는지 판단해 해당 Owner를 고친다. 완료된 동작과 사용자 수락·제품 통합은 같은 상태가 아니다.

이번 예시는 [로그인 완료 표현 Work](../001-login-completion-names/README.md)에서 이 역할별 내용을 확인할 수 있다.
