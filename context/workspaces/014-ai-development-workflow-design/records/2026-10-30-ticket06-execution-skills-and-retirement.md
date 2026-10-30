# Maintain과 분리한 실행 스킬 반영·옛 경로 정리

2026-10-30 Reference에 development·improvement-loop를 설치하고 work-discussion·create-context-workspace의 비충돌 보완을 반영한 뒤, Noline 고유 계약에 적응했다. Noline의 임시 호환 스킬4개와 bridge도 현재 참조를 전환한 뒤 제거했다. **파일 설치·직접 검사까지의 결과이며 전체06 완료·실제 host 수행 확인은 아니다.**

## 남은 일을 통합 테스트로만 묶었던 안내를 바로잡았다

현재 대화에서 사용자는 “뭔가 이상하네 development 생기지도 않았고 또 기존 스킬중에 지워야 한느게 있을수도 잇고 등등”이라고 지적했다. 이어 “06-01, 06-02 티켓부터 실제 남은 작업에 맞게 보완하고, Maintain이랑 분리해서 지금 반영할 수 있는 것부터 진행해봐. 기존 합의 잘 지키고”라고 요청했다.

[최초 전환안](2026-10-29-ticket06-01-reference-transition-proposal.md)은 비충돌 본문·경로 준비가 가능하다고 구별했고, 임시 변형판의 재작업 비용 때문에 운영 활성화 유보를 권고했다. Main이 이를 모든 실행 스킬·삭제 작업의02 대기로 넓힌 안내는 부정확했다. 두 티켓에 실제 미설치·부분 교체·제거·보존을 먼저 명시하고 이번 사용자 요청에 따라 현행 Work 계약으로 적응했다.02의 새 기록 방식이나 Work 구성을 대신 확정하지 않았다.

## 실제 전환

| 대상 | Reference와 Noline에서 반영한 결과 |
| --- | --- |
| development | 본체·구현·개선 검토·검증/근거·실행 배치와 형성 자료를 함께 설치했다. 구현 완성·별도 검증·수정·결과 설명의 기존 강도를 유지했다. |
| improvement-loop | 사용자 요청으로 대화와 경험을 검토하고 선택한 개선·한정 시도·종료를 이어가는 실행 본문과 상세·형성 자료를 설치했다. 자동 마무리 루프로 만들지 않았다. |
| work-discussion | 기존 정의의 충분성과 실제 보완을 구별하고 요청에 맞춰 반환하는 최소 보완을 반영했다. 명시 호출·기존 Main→Maintain 전달 계약을 유지했다. |
| create-context-workspace | 사용자 지정 대상 확인·유효한 맥락 재사용·새 의미 구성·인수 공백 판단을 보완했다. JSON·명시 Recover·generation/activation은 기존 계약 그대로다. |
| Noline 옛4개 | read-project-context → USAGE, update-project-context → context-update, work-artifact-briefing/explanation-recovery → explain으로 현재 사용처를 옮기고 실행 폴더·bridge를 제거했다. |
| 유지 | reconsider-work의 재판단 역할, Noline start-app, 명시적 보존 결정이 있는 deprecated noline-work를 유지했다. |

prototype의 Main 직접 Work 기록·자동 Maintain 미연결 문장을 설치 대상에 그대로 넣지 않았다. development·improvement-loop의 Work 반영·시도 종료는 기존 Work 관리 계약과 수동 fallback으로 연결했고, work-discussion은 기존 담당 문장을 보존했다. 새로운 기록 Owner나 activation 장치는 추가하지 않았다.02에서 새 계약을 채택하면 이 적응 부분을 다시 대조한다.

Reference는 `.agents/skills/` 원본과 Claude/Codex 상대 연결을, Noline은 `.claude/skills/` 원본과 `.agents/skills/` 연결을 사용한다. 원형의 background·원문은 함께 두고 각 스킬에 이번 적응 이유를 연결했다. 실행 링크는 설치 경로로 바꿨고 긴 바깥 형성 원자료는 기존 provenance로 남겼다. 원문 `.txt`는 내용 그대로 보존했다. Prototype의 기존 앵커3곳은 설치본의 실제 제목에 맞췄으며 prototype 정본은 수정하지 않았다.

## Noline에서 달리 적용한 것

제품 불변식과 경로별 지침·rules·guards·runbooks를 development에서 연결했고, Personal의 일반 기준이 더 엄격한 Noline 규약을 해제하지 않게 했다. 기존 등록 agent는 report-only 역할을 유지하며 구현 담당 배정으로 그 권한을 넓히지 않는다.

Noline 생성 canonical은 관련 layer README에서 goal에 필요한 본문을 고르는 계약을 유지하고 있다. Reference의 주제별 선택 문장을 그대로 복사하면 충돌하므로 Noline 생성 스킬의 해당 선택 문장은 기존 계약을 보존했다. 공통 보완인 대상 확인·읽기 재사용·의미 구성·인수는 반영했다.

옛 스킬의 과거 본문은 Noline `4fb309d2`의 실제 Git blob을 실행 목록 밖 `.claude/_archive/skill-transition-2026-10-30/*.txt`로 보존했다. 교체 직전 판본이며 각 역사 기록 작성일의 판본과 동일하다고 주장하지 않는다. Decision의 역사 링크는 이 보존판으로,004의 current/output 진입은 새 Owner로 옮겼다.004의 목표·진행·결과는 바꾸지 않았다.

002의 기존 날짜별 기록2개는 append-only이므로 원문을 바꾸지 않았다. 기록 색인에서 보존판을 찾게 하고, 검사에서는 정확한 기록 파일·원문 해시·옛 target·보존판 고정 해시가 모두 맞는2건만 역사 참조로 구별한다. 현재 broken link를 면제하지 않는다.001 verify.json은 제거된 스킬의 evidence 경로를 새 regular 입력으로 옮겼고 직접 검사에 쓰는 보존판도 포함했다. schema·claim·argv·실행 제한, 기존 receipt·status·Recover 선택은 유지했다. 전체 동적 입력 closure 완성이나 새 Verify pass를 주장하지 않는다.

## 확인과 한계

- Reference: 변경한47개 파일의 로컬 링크263개·앵커32개 확인, 새 bridge4개 확인, 기본 Recover 성공(001-default-timeout,15개 context).
- Noline: 설치 파일64개·삭제12개 경로·새 bridge2개 대조. 당시 스킬 원문4개의 Git blob·해시 일치. 변경한 문서의 링크527개·앵커39개 누락 없음.
- 두 대상의 스킬 frontmatter·호출 설정32개 parse 성공. history 검사 정상2건·거부5건의 직접 assertion7개 통과. 원문 변경·보존판 변경/누락·다른 현재 문서·다른 target을 거부했다.
- Noline 구조 검사: 기존 실패8건이 변경 전과 동일하다. 제거된 스킬을 가리키는 보존 역사 참조2건은 별도로 출력하며 새 현재 경로 실패는 없다.
- Noline Recover: 기본001·명시001 각각15개,002는20개,004는16개 context로 성공. 선택 계약을 바꾸지 않았다. 실제 host discovery·호출·activation·제품 효과는 실행하지 않았다.
- Noline Harness 전체124개 중123개 통과, `test_timeout_covers_descendant_after_group_leader_exits`1개에서 descendant.pid 생성 전 timeout으로 실패했다. 해당 검사의 현재판 단독 실행과 같은 Git 기준판의 격리 실행은 각각 통과했다. 첫 기준판 준비는 fixture 문서 누락으로 실행 오류였으며 필요한 기존 fixture를 갖춘 뒤 확인했다. 관련 코드·테스트는 변경하지 않았다. 타이밍에 민감한 관찰로 남기며 원인을 확정하거나 전체124개 통과로 바꾸지 않는다.
- 독립 읽기 전용 검토에서 verification 상세의 자동 Maintain 배제 잔재와 Noline 생성 계약의 선택 순서 차이를 발견해 수정했다. 최종 설치판에서 미해결 차단 결함을 찾지 못했다. 정적 의미 대조와 메모리에서의 함수 확인이며 host 통합 테스트의 대체가 아니다.

적용 직후 기준선 대조에서 Noline의 이번 범위 밖 기존34,618개 파일/연결과 artifacts1,055개가 동일했고 예상 밖 변경은 없었다. ai-workspace의 당시 범위 밖9,692개도 동일했다. 이후 이 기록·재진입 갱신은 이번 범위에 추가한다. 기존 `.gitignore`·`.pnpm-store/`와014의02 Ticket·02 기록·공유 기록 색인 병렬 변경, 제품·Maintain·수집기·기존 receipt·status를 보존한다. 상세 경로·해시는 [적용 receipt](receipts/skill-transition/2026-10-30-application.json)에 둔다.

## 다음 연결

[06-01](../current/tickets/06-framework-transition/06-01-reference-project-application.md)·[06-02](../current/tickets/06-framework-transition/06-02-noline-reapplication.md)는 계속 진행 중이다. 지금 남은 것은02가 소유하는 Work 기록·생성/전환·Maintain/수집기 선택을 채택 판본으로 연결하고, 기존 선택대로02에서 실제 host의 발견·호출·중복 표시·기록·재개를 함께 확인하는 일이다. 원문 접근의 실제 가능 범위와 improvement-loop의 사용·부담·효과 관찰은05/07의 확인 상한과 연결한다. Noline 결과의 정본은 [대상001의 적용 기록](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/001-noline-context-harness-application/records/2026-10-30-02-development-skill-transition.md)이다.

반영·검증 직후에는 stage·commit·push·Workspace 완료 처리를 하지 않았다. 아래는 이후 사용자 요청으로 진행한 커밋 경계다.

## 후속 기록 정리와 커밋

사용자가 “이번 변경 기록 정리하고 커밋하자. 여기랑 Noline 각각 이번 변경만 묶고”라고 요청했다. Noline은 `41170efd8fef7c1e7b95bc4ab54f47386048e409`(`docs(harness): 개발 수행 스킬을 반영하고 옛 실행 경로 정리`)로 이번79개 경로만 커밋했다. `.gitignore`·`.pnpm-store/`와 기존 artifacts는 제외했다.

이 저장소는 Reference 실행 스킬·연결과06 티켓·재진입·본 적용 기록/receipt의60개 경로만 같은 커밋으로 묶는다. 병렬02 Ticket·02 비교 기록·공유 records 색인의 기존 변경은 포함하지 않는다. 공유 current 문서에서도06 관련 변경만 대조했다. 적용 receipt는 검사 당시 source/target 해시를 보존하며 후속 커밋 안내 문단의 추가와 구별한다. 실제 이 저장소의 커밋 식별자는 이 문서를 포함한 Git 이력에서 확인한다. Push·Workspace 완료·host 통합 확인은 수행하지 않는다.
