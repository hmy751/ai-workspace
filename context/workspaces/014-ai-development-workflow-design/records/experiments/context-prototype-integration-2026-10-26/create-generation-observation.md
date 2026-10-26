# Create 사용 시험 관찰

## 읽은 접근점

- 전달받은 전역·로컬 지침과 create/noline-demo/AGENTS.md, create/README.md, noline-demo/README.md에서 대상과 이번 생성 범위를 확인했다.
- create/skills/README.md와 create-context-workspace/SKILL.md를 읽고 context/README.md, USAGE.md, work/AGENTS.md, work/README.md, workspaces/README.md, CREATE-AND-TRANSITION.md, spec-and-tickets/README.md를 따라갔다.
- 문서 작성 시 전역 recall-document-guidance/SKILL.md와 대상 CONTENT-POLICY.md를 읽었다. Work는 기존 Spec·Ticket·current·source·output·records 구성을 유지한다는 조건을 적용했다.
- Project README·REFERENCE/reading.md에서 device-session, authentication-and-session, authentication-flow 본문을 골랐다. Personal 입구·development 안내에서 contracts-and-lifetime와 naming-and-completion 본문을 선택했다.
- 001 Work의 README·memory/선택 문서·state·output·source, 목표/제약 Spec과 실행 Ticket, 2026-10-19-03-execution.md를 읽었다. authentication Store·service·test 실제 본문과 examples README를 대조했다.
- create/viewer/README.md에서 표시 사본 갱신 방법과 제품 검사와의 차이를 확인했다.

## 수행한 변경

- create/noline-demo/context/work/workspaces/002-device-authentication-recovery/에 16개 Markdown 문서를 생성했다. README, 다섯 Spec, 선택한 Project·Personal, 첫 Ticket과 색인, state, source 요청/접근점, output, 생성 기록을 구성했다.
- workspaces/README.md에 새 Work와 실제 저장소 입력·연결·검증이 남았다는 상태를 연결했다. 일반 재개 기본 선택은 001로 유지했다.
- 기존 계약에서 이어받은 데이터 보존·저장 후 공개·조회 실패 분리를 현재 문장으로 썼다. 메모리 저장 전제·기존 검사 통과를 상속하지 않았고, 첫 Ticket에는 대상 플랫폼·실제 어댑터와 저장/복구 계약 확인을 배정했다.
- 제품 코드·Project·Personal·이전 Work·스킬은 수정하지 않았다. 커밋·패키지 설치·외부 서비스·원본 저장소·다른 Desktop 조사는 수행하지 않았다.
- 표시 HTML 갱신을 위해 node viewer/build.mjs를 한 번 실행했으나 로컬 marked 모듈 부재로 실패했다. 이를 생성 기록에 남겼다.

## 직접 확인

- 새 README, memory/Spec/선택 문서, state, output, 첫 Ticket, source에서 목표·보존 조건·완료 기준·현재 결과·핵심 미확인·첫 행동을 직접 읽어 복원했다. 별도 읽기 주체에 의한 독립 인수 시험은 아니다.
- 로컬 링크 45개가 실제 파일로 연결됨을 확인했다. 주변 설명은 직접 읽은 Project 계약·현재 코드·정확한 이전 실행 기록의 내용과 대조했다.
- 생성 전후 Noline demo 파일 내용을 비교했다. 기존 파일 중 변경은 workspaces/README.md 한 개이고 신규 파일은 새 Work의 16개뿐이다. 기본 선택은 001로 남았다.
- 테스트 본문에서 오류를 먼저 통과한 뒤 메모리 persistedSession을 바꾸므로 기존 저장 실패 시험이 실제 부분 기록을 재현하지 않는다는 점, Store가 저장 후 메모리 session을 바꾸고 초기 세션을 주입받는다는 점을 읽었다. 제품 테스트는 실행하지 않았다.

## 미확인

- 실제 플랫폼·저장소·어댑터·접근 범위는 주어진 복사본에 없으며, 부분 저장의 확정 여부·복구 정책·시작 시 상태 공개는 미정이다. 구현 및 실기기/프로세스 재시작 검증을 수행하지 않았다.
- 제품 실행 인수 준비 완료·제품 목표 완료·사용자 수락·host 전환으로 판정하지 않았다.
- viewer.html 재생성과 이후 표시 검사·화면 확인은 남았다. 필요한 모듈 설치나 다른 Desktop 탐색으로 범위를 넓히지 않았다.
