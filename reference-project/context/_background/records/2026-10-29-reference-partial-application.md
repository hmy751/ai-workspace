# Reference에 독립적인 context·설명 묶음을 먼저 적용

2026-10-29, 사용자는 “maintain 관련은 02에서 하는 걸로 두고, 먼저 가능한 부분부터 reference-project에 반영해봐. 기존 내용이랑 합의도 잘 지키고.”라고 범위를 정했다. 전체 개발 workflow 전환과 이번 부분 적용을 구별한다.

## 가져온 의미와 이 대상에 맞춘 선택

014의 development-workflow 프로토타입에서 로컬 Personal의 판단·조건별 사례·경험과 공통 읽기·본문 관리 방법, explain/shared, context-update를 가져왔다. 제품과 Work를 데모로 교체하지 않았다. 기존 Request policy 요구·구현·검사·5000ms 결정, Project 물리 층, Workspace의 실제 이력·선택·receipt는 기존 Owner에 남는다.

프로토타입의 development·improvement-loop와 새로운 work-discussion은 이번에 설치하지 않는다. 공통 읽기와 한정 반영에서 그 스킬의 필수 호출을 제거하고 현재 요청·Main의 위임·대상 관리 계약으로 연결했다. Work 반영은 기존 Main·Maintain 및 수동 fallback 관계를 따른다. Maintain 코드·등록·hook·binding·생성/전환과 Recover·Verify 계약은 바꾸지 않았다. 이 유보를 근거로 미래 구조를 확정하지 않는다.

기존 read-project-context는 USAGE와 Project 읽기 기준으로, update-project-context는 context-update로, 두 설명 스킬은 explain으로 교체했다. 공통 설명 기준은 제품 guidance에서 skills/shared로 옮겨 실제 소비자인 work-discussion·explain이 읽는다. 기존 create-context-workspace·reconsider-work와 work-discussion의 명시 호출 조건은 유지한다.

## 판본과 출처

적용 직전 저장소 commit은 `56643f48f355aca017554149687982d02af7d434`다. Reference 최근 변경은 `8d5f4267`, 프로토타입 최근 변경은 `f006a0e7`이며 실제 선택 파일은 그 뒤 작업 트리와 대조했다. 교체 전 네 스킬과 옛 guidance는 이 commit의 `reference-project/` 경로에서 복원할 수 있다. explain의 legacy 보존 파일은 과거 프로토타입 형성 판본이며 이번 Reference에서 제거한 파일과 동일한 snapshot이라고 취급하지 않는다.

현재 실행 본문은 Reference가 소유한다. 함께 가져온 날짜별 기록·원문·legacy 판본은 당시 프로토타입 설계의 근거이며 현재 설치 사실이나 Reference 제품 사건으로 바꾸지 않는다. Personal 경험도 014 설계와 그때 확인한 Noline 경험의 출처·관찰 한계·열린 후보 지위를 유지한다. 바깥 전체 기록은 재접근용이며 현재 실행 조건은 이 Reference 안에서 읽는다.

이번 설치와 직접 검사 결과는 014의 06-01 적용 기록에서 관리한다. 파일·연결의 설치, 이 세션의 본문 적용, 새 host의 자동 발견·호출과 일반적인 효과는 구별한다. 새 host 동작이나 전체 workflow 전환을 이번 문서로 완료 처리하지 않는다.
