# 수행 기록

## 실행 경계와 산출물

- 입력 루트: `/private/tmp/briefing-first-report-20261021/r17`.
- `environment.md`와 `conversation.txt`를 첫 호출에서 순서대로 읽었다. 마지막 요청은 앞서 설명한 ②~⑤ 각각의 HTML 보고서 작성이며, 사용자 답변으로 그 범위가 확정돼 있다.
- repository는 environment가 HEAD `0b3b167c8b8d15dc1a45d87da934dfc5efaed994`의 tracked snapshot이라고 명시한 복사본이다. Git 메타데이터가 없어 브랜치·working tree·실제 HEAD를 별도로 검증하지 않았다.
- repository는 읽기만 했으며 모든 생성물은 output에 썼다. 다른 실행 루트·원본 저장소·바깥 워크스페이스 문서·현재 앱·네트워크에 접근하지 않았다. 추가 설치와 subagent 실행도 하지 않았다.
- 결과: `index.html`, `02-foreground.html`, `03-ux-flows.html`, `04-dates.html`, `05-scope.html`.
- 사용자에게 보낼 첫 결과 응답 전체는 `response.md`에 별도 저장했다.

## 실제 읽은 지침·스킬·맥락

경로는 repository 기준이다. 아래 파일을 직접 읽거나 주제에 맞는 본문을 추출했다. 긴 결합 출력 일부는 도구 한도로 잘렸으므로 모든 파일의 전 문장을 완독했다고 주장하지 않는다. 주장에 필요한 핵심은 이후 개별 본문·행 범위로 다시 확인했다.

- 루트 `CLAUDE.md`, `apps/client/CLAUDE.md`, `context/work/AGENTS.md`.
- `context/README.md`, `context/work/workspaces/002-code-readability-refactoring/README.md`.
- `.claude/skills/README.md`, `.claude/skills/read-project-context/SKILL.md`를 읽고 날짜·정책 맥락 선택에 적용했다.
- `.claude/skills/work-artifact-briefing/SKILL.md`를 읽었다. 이번 작업을 새 코드 구현으로 확대하지 않고 근거를 구별하는 참고로 사용했다.
- `context/project/README.md`, `REFERENCE/reading.md`, `guidance/explanation-and-evidence-criteria.md`, `common/date-and-time.md`.
- `.claude/rules/policy-ui.md`, `.claude/rules/iso-time.md`.
- Workspace 002의 `current/memory/tickets/06-app-startup-lifecycle.md`, `08-date-selection-grouping.md`, `10-schedule-form-lifecycle.md`, `11-expense-form-lifecycle.md`, `13-schedule-route-preparation.md`, `14-local-mutation-router-transaction.md`, `15-sync-result-retry-pull-types.md`, `16-unsynced-data-cleanup.md`, `17-server-data-route-boundaries.md`의 관련 본문.
- `records/2026-10-02-03-expense-time-decisions-and-verification.md`의 523개 검사 기록과 실앱 범위·제한·후속을 검색 추출해 대조했다.
- 초기에 `current/state.md`를 조회했으나 없었다. 실제 state는 디렉터리 구조인 것을 파일 목록으로 확인했으며 이번 산출물 작성에 Workspace 상태 갱신은 하지 않았다.

## 실제 조사한 주요 코드·검사

- `apps/client/src/application/AppInitialization.tsx`: network init/cleanup, DB·인증 준비 수명.
- `apps/client/src/shared/store/network.ts`: init/cleanup/refresh, 진행 중 Promise 공유, observationRevision, timeout, 표시 override/실제 관측 분리.
- `apps/client/src/shared/services/policy-query/usePolicyReadQuery.ts`, `useTripReadAccess.ts`: blocked/ready/error 표시, 기존 data 유지, 최신 접근 조건의 refetch.
- `apps/client/src/screens/HomeScreen/MainTripSection.tsx`: 현지 getMonth/getDate, 개별 요약 feedback.
- `apps/client/src/screens/ScheduleScreen.tsx`, `ExpensesScreen.tsx`: 공통 UTC 범위와 일정 현지 날짜 grouping, 경비 삭제의 일반 onError 문구.
- `apps/client/src/screens/ExpenseDetailScreen.tsx`: 대상 경비 부재·조회 오류·진행 중 분기, canFetch가 false인 retry 종료.
- `apps/client/src/shared/lib/datetime.ts`: getUTCDateRange, 현지 표시와 날짜·시각 결합.
- `apps/client/src/features/schedule/create-schedule/useSubmitSchedule.ts`: 저장 뒤 500ms timer 및 truthy 좌표 변환.
- `apps/client/src/features/expense/create-expense/useCreateExpenseForm.ts`: 비동기 trip 기본 통화와 useForm defaultValues.
- `apps/client/src/shared/services/sync/engine.ts`, `queue.ts`, `cleanup-job.ts`: 검색으로 SyncIncompleteError/FAILED/IN_PROGRESS/pull schema와 여행별 PENDING 조회·processed 경계를 대조했다. 전 sync 동작을 실행 검증한 것은 아니다.
- `apps/client/tests/shared/store/network.test.ts`: 동시 refresh·최신 관측·cleanup 검사 본문.
- `apps/client/tests/shared/lib/datetime.test.ts`: Date 비변경·DST·범위 검사 본문.
- `apps/client/tests/screens/schedule-recovery.test.tsx`, `expense-recovery.test.tsx`, `read-query-consumers.test.tsx`, `create-schedule-flow.test.tsx`, `create-expense-flow.test.tsx`: 테스트 이름·관련 assertion·mock 경계. 일정 및 경비 flow의 DB/HTTP/native 대체를 직접 확인했다.
- `apps/client/package.json`: Jest 등 실행 의존성 확인.
- 저장소 source·tests에서 AppState/refresh 사용을 검색했다. src AppState 참조를 찾지 못했고 제품 코드 NetInfo.refresh 호출은 Store 안에 있었다. 이것으로 실제 기기 복귀 실패를 재현했다고 주장하지 않았다.
- HTML/observations/이미지 파일 목록을 검색했다. 해당 simulator 보고서·캡처는 없고 일반 앱 자산만 나왔다. 일반 자산을 요청 화면의 캡처로 사용하지 않았다.

## 직접 실행한 확인과 결과

1. 날짜 계산: 실제 getUTCDateRange 함수를 source에서 추출하고 export·TypeScript 타입 표기만 제거한 `date-check.js`를 output에 생성했다. 홈 getMonth/getDate 계산을 같이 실행했다.
   - 설명용 입력: `2026-09-29T15:00:00Z` ~ `2026-10-01T15:00:00Z`. 당시 DB 값이 아니다.
   - `TZ=Asia/Seoul`: 홈 9월 30일~10월 2일, 목록 9월 29일~10월 1일.
   - `TZ=America/Los_Angeles`: 홈 9월 29일~10월 1일, 목록도 같은 날짜 범위.
   - 2026년 3월 7~10일 UTC 범위는 두 시간대 모두 네 날짜. assert 통과.
   - 결과는 `date-seoul.json`, `date-la.json`에 보존했다. Jest 전체/React 화면 실행이 아니다.
2. HTML: Python 표준 라이브러리 HTMLParser로 5개 파일의 한국어 lang, h1 한 개, 모든 로컬 링크 대상 존재를 확인했다. 깨진 링크 0개, img 0개. `validation.json`에 결과를 남겼다.
3. 보고서에는 source 발췌를 HTML escape해 넣고, 코드·과거 기록·이번 계산·미확인을 구별했다. 독립 파일마다 내부 CSS와 responsive/print 규칙을 포함했다. `build_reports.py`는 output 내부 생성 도구다.
4. source snapshot과 기존 기록을 대조해 sync의 최초 조사 결함이 전부 미해결이라는 오해를 피했다. FAILED 재시도·불완전 결과 오류 전달·pull schema는 이미 있는 부분으로, cleanup·재개·전체 원자성 등은 남은 부분으로 작성했다.

## 실행하지 못한 확인과 필요한 추가 자료

- 환경 지침이 추가 subagent를 금지하므로 사용자가 원한 6.1 sol 병렬 워커는 실제 실행하지 않았다. 가상의 worker 결과를 만들지 않았다.
- DB·시뮬레이터·개발 의존성·기존 gitignored 보고서/스크린샷·과거 worker 내부 로그가 입력에 없다. 설치나 외부 환경 접근은 금지돼 있다.
- 루트/client node_modules가 없음을 확인했다. Jest/typecheck/lint를 실행하지 않았으며 기존 대화의 523 통과/1 제외 수를 이번 결과로 제시하지 않았다.
- 시뮬레이터/foreground 조작, 실제 통신 단절, 서버 실패, Local 저장 및 서버 반영, native picker·keyboard·cancel 경고 검증은 미실행이다.
- HTML을 브라우저로 렌더링해 시각 QA하거나 미리보기를 열지는 못했다. 구조·링크 검사만 완료했으며, 실제 화면을 열었다고 응답하지 않았다.
- 원래 홈 보고서와 같은 캡처 포함 결과를 완성하려면 기존 `artifacts/ticket-06-simulator/...` HTML·이미지 또는 앱·계정·여행·DB가 준비된 시뮬레이터와 실행 허용이 필요하다. 날짜 재현에는 실제 startDate/endDate 및 기기 timezone이 필요하다.
- 보고서마다 후속 캡처 장면과 검증 범위를 적었다. 산출물 작성과 Ticket 06 종료·사용자 최종 acceptance는 구별했다.
