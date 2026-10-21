# 대화에서 보고한 Git 상태

[noline-0b3b167.tar.gz](noline-0b3b167.tar.gz)는 Noline 저장소의 커밋 `0b3b167c8b8d15dc1a45d87da934dfc5efaed994`를 Git archive로 추출한 원본이다. [commit.txt](commit.txt)는 커밋 메타데이터, [tracked-files.txt](tracked-files.txt)는951개 tracked 항목의 mode·object·size·경로, [recent-history.txt](recent-history.txt)는 해당 커밋과 앞선7개 커밋이다. 최신 checkout의 파일이나 뒤의 수정은 압축본에 넣지 않았다. 원 저장소는 checkout·수정·실행하지 않았다.

기준은 날짜상 가까운 커밋이라는 추정만이 아니라, [대화 원문](../input/conversation.txt)의84가 이 HEAD와 추적 파일의 미커밋 변경 없음을 직접 보고한 데 있다. Git 객체의 존재·내용과 당시 AI 보고는 구별한다.619 시점까지 실제 working tree가 계속 동일했다는 독립된 전체 도구 증거는 확보하지 못했다.

코드 탐색 때 필요한 파일을 원래 경로로 열 수 있도록 압축본에는 tracked 트리를 통째로 보존했다. 이는 저장소 전체를 읽어 시험 프롬프트에 넣거나 전수 분석했다는 뜻이 아니다. `.git`, 설치된 의존성, 실제 DB, 시뮬레이터, Git 비추적 보고서는 포함하지 않는다. 안의 과거 AGENTS·skills·설정은 보존된 당시 지침이며 현재 작업 환경에 설치하지 않는다.

## 같은 커밋에서 바로 읽을 작업 기록

아래는 압축본의 대응 파일과 바이트가 같은 사본이다. 원문을 요약하거나 현재 내용으로 고치지 않았다.

- [Ticket 06](reading/context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/06-app-startup-lifecycle.md)
- [당시 state](reading/context/work/workspaces/002-code-readability-refactoring/current/state/index.md)
- [당시 output](reading/context/work/workspaces/002-code-readability-refactoring/output/index.md)
- [일정 작성 책임·검증 기록](reading/context/work/workspaces/002-code-readability-refactoring/records/2026-10-02-01-schedule-create-boundaries-and-verification.md)
- [정책 소비 검토 연속성 기록](reading/context/work/workspaces/002-code-readability-refactoring/records/2026-10-02-02-policy-consumer-review-continuity.md)
- [경비·시간 결정과 검증 기록](reading/context/work/workspaces/002-code-readability-refactoring/records/2026-10-02-03-expense-time-decisions-and-verification.md)

이 읽기 목록은 출처 탐색 편의를 위한 것이다. 실제 실행자에게 여섯 문서를 모두 미리 읽힌 조건으로 자동 고정하지 않는다.
