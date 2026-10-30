# 06-02 — 최신 Reference의 독립 묶음을 Noline에 반영

**결과:** [재점검한 적용안](2026-10-30-ticket06-02-reference-refresh-review.md)에 따라 Noline에 Personal·공통 읽기·한정 갱신·설명과 관련 관리·형식 기준을 반영하고 정적·읽기 전용 검사를 마쳤다. 실제 적용 결과의 정본은 [Noline001 기록](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/001-noline-context-harness-application/records/2026-10-30-01-reference-context-refresh.md)이다.06-02 전체 완료나 실제 host·제품 효과의 확인은 아니다. Maintain·Work 기록/전환과 통합 확인은 계속02에 둔다.

사용자 승인:

> 그래 그럼 그 적용안대로 Noline에 반영하고 확인해봐. Noline 고유 기준 잘 확인하고 Maintain 관련은 계속 02에 두자. 기존 artifacts랑 병렬 작업 변경은 건드리지 말고.

## 기준판과 보존

Source는 clean Reference `f5082bc30ab3470a3e3a4a895cfcb6cb50b3af81`, Noline baseline은 `main @ 4fb309d2ba50afaca44019879d7161964b9b2328`다. [반영 manifest](receipts/noline-reapplication/2026-10-30-phase1-application.json)는153개 exact path의 전후 상태·source 해시·검증을 연결한다. 실제 반영 직전 preflight를 다시 확보해 예약 receipt 이름만 바꿨고, 관찰 원본은 Noline001 source와014 receipt에 같은 바이트로 보존했다. 이전 계획·관찰 JSON은 수정하지 않았다.

Noline의 제품 불변식, React Native Form·UI 책임, TypeScript의 더 엄격한 명명·중괄호·console 규약, API 오류 전달과 열린 서버 오류 정책, 동작 보존 리팩터링 기준은 유지했다. Project의 구성·읽기·관리 문서는 Noline 본문에서 필요한 연결만 병합했다. 기존26개 수정 경로 외 tracked954개, untracked976개와 별도 확인한 artifacts·양쪽 Maintain runtime2106개 파일/링크의 hash·kind가 같다. 이 숫자는 보호 대조 범위이며 서로 중복될 수 있다.

## 적용 중 구체화한 적응

새 context-update·explain은 Noline의 `.claude/skills/` 원본과 `.agents/skills/` bridge를 사용한다. 옛 네 스킬과 공통 기준의 경로는 실제 verify evidence·Decision·output 소비가 남아 있어 안내로 전환하고 자동 선택을 비활성화했다. 과거 실행 본문은 Git 이력이 소유한다. 제품 Owner와 report-only agent 권한은 옮기지 않았다.

Reference sample의 제품 링크는 Noline 제품 의미·Selective Local-First 결정으로 바꿨다. Reference 자체 반영 기록은 source 근거로 연결하며 Noline 적용 결과로 복사하지 않았다. 외부 형성 링크는 원래 출처와 판본으로 이어지고 가까운 핵심 발췌를 유지했다. 경험 자료도 이번 설치에서 새로 관찰한 사건으로 표시하지 않는다.

기존 검사기는 fenced 원문에 들어 있는 옛 Markdown 표기까지 실제 링크로 판단했다. 새 형성 자료를 반영하면서 이 오탐이 드러나, 코드 블록의 원문을 그대로 보존하고 검사에서 fenced block만 제외하도록 좁게 보완했다. 실제 본문 링크·bridge·agent·Maintain 검사는 유지했다. Source 네 개발 주제 INDEX와 두 legacy 원문 evidence의 바이트 동일성도 확인했다. Reference 자체의 같은 검사 문제로 일반화하거나 추가 공통 변경을 수행하지 않았다.

## 확인과 후속

변경 Markdown의 로컬 링크992개·앵커226개와 frontmatter/호출 설정12개, 새 상대 bridge2개를 확인했다. 검사기의 fenced/실제 링크 경계5조건도 통과했다. Noline 자체 검사는 적용 전후 같은 과거 링크8건에서 실패했고 새 실패는 없다. 전체 통과라고 기록하지 않는다.

기본001·명시001 Recover는 같은15개,002는20개 context를 읽었고 선택은 바뀌지 않았다. Metadata에는002의 current-generation binding이 남아 있으나 관련 session-end 파일이 있어 현재 실행 생존으로 단정하지 않는다. 이를 보수적으로 확인 범위에 포함했다.001의 기존 Verify는 stale(125 snapshot,57 changed,missing0),002는 not_applicable이며 machine 결과·receipt는 그대로다.

대표 읽기에서는 폼/UI 공통화, API 오류 전파, 코드 표현, Project current의 독립 가치 질문에서 새 진입과 기존 Owner를 대조했다. 실제 제품 시험·durable Verify·host 발견/호출·자동 갱신·activation·통합 흐름은 수행하지 않았다. Maintain·Work 계약 연결과 그 뒤 통합 확인은02에서 진행하고, 제품 가이드의 기존 예시 모호함과 미결정 서버 오류 정책은 해당 제품 책임으로 남긴다.

적용·검증을 마친 시점에는 Noline과 ai-workspace 모두 stage·commit·push를 하지 않았다. 후속으로 사용자가 두 저장소에서 이번 변경만 각각 커밋하도록 요청했다.014에서는06-02의 적용 결과와 재진입만 갱신하고 병렬02 문서·합의는 보존한다. 복구가 필요하면 manifest의 exact path·전후 hash를 대조해 이번 신규 파일과 변경만 되돌리며 이후 사용자 변경을 덮어쓰지 않는다. Noline tracked 원본의 기준은 위 target commit이고 기존 untracked·runtime·artifacts는 복구 대상에 포함하지 않는다.

커밋 범위에서는 Noline의 기존 `.gitignore` 추가 변경과 `.pnpm-store/`·artifacts를 제외한다. ai-workspace의 병렬02 Ticket·비교 기록과 공유 기록 색인의02 추가·재배치는 그대로 작업 트리에 남긴다.

Noline 반영은 `2839d467dfa999911385e1920fa482d0377dcbe5` (`docs(context): Reference 개인 기준과 설명·갱신 경로 반영`)로 커밋했다. 적용 manifest의153개 경로와 commit 경로가 정확히 같고, 기존 `.gitignore` 변경·`.pnpm-store/`·artifacts는 포함하지 않았다. Push는 하지 않았다.
