# 실제 수행 기록

## 입력과 실행 경계

- `/private/tmp/briefing-first-report-20261021/r63/environment.md`와 `conversation.txt`를 먼저 읽었다. 대화는 처음부터 마지막 확인 응답까지 순서대로 읽었으며, 마지막 요청의 대상은 앞서 합의한 ② foreground 재확인 ③ 종합 UX ④ 날짜 차이 ⑤ 보류·후속 경계다.
- `repository/`는 제공된 HEAD `0b3b167c8b8d15dc1a45d87da934dfc5efaed994`의 tracked snapshot이라는 environment 설명에 기준을 뒀다. `.git`이 없으므로 branch·HEAD·working tree를 Git으로 확인했다고 주장하지 않는다.
- 입력은 위 두 파일과 이 repository만 사용했다. 네트워크, 바깥 저장소·스킬, 현재 앱, 과거 worker 내부 로그에 접근하지 않았다. 쓰기는 이 `output/` 안에서만 했다. 추가 subagent는 만들지 않았다. 환경의 단독 실행 제약이 원래 사용자 요청의 병렬 운영을 제한했다.
- 원본 홈 HTML과 gitignored 캡처는 없었다. 원본 디자인을 보았거나 스크린샷을 새로 수집·열람했다고 주장하지 않는다.

## 실제 읽은 지침·스킬·맥락

아래 경로는 모두 `repository/` 기준이다. 긴 출력 일부에는 도구 truncation이 있었으므로 모든 문서의 전 내용을 정독했다고 주장하지 않는다. 보고서의 주요 결론은 아래 직접 읽은 코드·작은 발췌로 재확인했다.

- `AGENTS.md`, `context/work/AGENTS.md`, `apps/client/CLAUDE.md`
- `.claude/runbooks/first-result-report.md`와 연결된 `context/project/guidance/explanation-and-evidence-criteria.md`: 첫 결과에서 원래 질문·결론·근거·남은 행동을 함께 설명하도록 적용.
- `.claude/skills/read-project-context/SKILL.md`: 읽기 기준에 따라 날짜 의미의 정본과 코드의 실제 차이를 대조했다. `context/project/README.md`, `context/project/REFERENCE/reading.md`, `context/project/common/date-and-time.md`를 읽어 날짜 의미·열린 Trip 결정을 보고서에 반영했다.
- `.claude/skills/work-artifact-briefing/SKILL.md`: 호출 조건을 읽었으나 이번 작업은 새 검토 보고서 작성이 주목적이므로 별도 workflow로 적용하지 않았다.
- `.claude/rules/policy-ui.md`, `.claude/rules/iso-time.md`
- `context/README.md`, `context/work/workspaces/002-code-readability-refactoring/README.md`
- 해당 Workspace `current/memory/index.md`, `current/state/index.md`, `output/index.md`, `current/memory/spec/05-constraints-design-assumptions.md` (큰 출력의 일부만 확보)
- 해당 Workspace `current/memory/tickets/06-app-startup-lifecycle.md`: 범위·채택 정책·실행 접근·현재 상태와 뒤의 일정/경비 결과를 나눠 읽음. 문서 자체에 남은 전체 완료·native 미확인을 유지.
- 같은 tickets의 `07-client-api-boundaries.md`, `08-date-selection-grouping.md`, `10-schedule-form-lifecycle.md`, `11-expense-form-lifecycle.md`, `13-schedule-route-preparation.md`, `14-local-mutation-router-transaction.md`, `15-sync-result-retry-pull-types.md`, `16-unsynced-data-cleanup.md`, `17-server-data-route-boundaries.md` (일부 긴 결합 출력은 잘렸고 주요 14·15·16은 다시 작은 범위로 읽음)

## 실제 확인한 주요 코드·검사 경로

`repository/` 기준. 전체 파일 또는 표시한 관련 구간/검색 일치를 읽었다.

- `apps/client/src/application/AppInitialization.tsx`: DB→auth 준비와 네트워크 init/cleanup. AppState 연결 없음.
- `apps/client/src/shared/store/network.ts`: refresh Promise 공유, session·revision으로 늦은 응답 억제, timeout·실패·cleanup.
- `apps/client/src/shared/services/sync/provider.tsx`: 실제 네트워크·인증·override 조건 변화로 자동 요청, 이미 eligible이면 반복 실행하지 않음.
- `apps/client/src/shared/lib/queryClient.ts`: window focus와 reconnect 자동 refetch false.
- `apps/client/src/shared/services/policy-query/usePolicyReadQuery.ts`, `useTripReadAccess.ts`, `index.ts`: 표시 제한과 실행 가능성, ready/refetch error, 최신 commit 기준 refetch.
- `apps/client/src/features/schedule/read-schedules/useTripSchedulesReadQuery.ts`, `apps/client/src/features/expense/read-expenses/useTripExpensesReadQuery.ts`: entity query와 policy-query 조합.
- `apps/client/src/screens/HomeScreen/MainTripSection.tsx`: 기기 현지 날짜 표시, 독립 요약 피드백. `SummaryFeedback`은 blocked에 PolicyErrorDisplay를 사용.
- `apps/client/src/screens/ScheduleScreen.tsx` 관련 구간: UTC dateRange와 일정의 local date grouping. `ScheduleListView.tsx`의 날짜 그룹 렌더·추가 입력 경로.
- `apps/client/src/shared/lib/datetime.ts` 관련 구간: UTC 일자 순회 helper·현지 날짜 helper 위치.
- `apps/client/src/screens/CreateScheduleScreen.tsx`, `CreateExpenseScreen.tsx`: 조건부 UI 위의 초안과 단계, 취소·pending 경계.
- `apps/client/src/features/expense/create-expense/useCreateExpenseForm.ts`: 최초 defaultValues 통화와 submit.
- `apps/client/src/features/schedule/create-schedule/useSubmitSchedule.ts` 관련 구간: 저장 요청 null 병합과 성공 후 500ms/truthy 좌표 projection의 차이.
- `apps/client/src/screens/ScheduleQueryFeedback.tsx`, `ExpenseQueryFeedback.tsx`: 최초 실패와 갱신 실패의 서로 다른 안내.
- `apps/client/src/screens/ExpenseDetailScreen.tsx`: canFetch 조건부 retry와 대상 부재+이전 오류 경로. `ExpensesScreen.tsx` 삭제 onError 검색 일치.
- `apps/client/src/entities/trip/api/trips.ts`, `apps/server/src/routes/trips.ts`: 수정 method PATCH/PUT 검색 일치·해당 발췌.
- `apps/client/src/entities/trip/utils/selectMainTrip.ts`: 날짜 기반 대표 선택의 검색 일치.
- `apps/client/src/shared/services/sync/cleanup-job.ts`: hasPendingTasksForTrip 확인과 soft delete 분기 구간.
- `apps/client/tests/shared/store/network.test.ts`: 재확인·실패·늦은 응답·cleanup assertion 구간을 읽음.
- `apps/client/tests/app/layout.test.tsx`: RootLayout은 실제 연결하되 native·DB·sync 대체하는 설정을 읽음.
- `apps/client/tests/screens/read-query-consumers.test.tsx`: native picker 대체와 상세/홈 캐시·최초 실패·부분 실패·폼 보조조회 assertions.
- `apps/client/tests/screens/create-schedule-flow.test.tsx`: 테스트 항목과 단일 폼/연결 보존 관련 구간.
- `apps/client/tests/screens/create-expense-flow.test.tsx`: 활성 Local 경로, 비활성 차단·명시적 재시도·연결 해제·pending·실패 관련 assertions. Local/Remote는 mock임을 유지.
- `apps/client/tests/screens/schedule-recovery.test.tsx`, `expense-recovery.test.tsx`: 관련 테스트 항목 검색 결과.
- `apps/client/tests/shared/lib/datetime.test.ts`: 전체 작은 본문을 읽음. DST 범위 검사와 조건부 skipped 시각 검사.
- `apps/client/package.json`: Jest·typecheck 명령과 의존성 선언 확인.
- `src`, `app`, `tests`에서 AppState/network refresh/focusManager 사용 검색. AppState·focusManager 일치 없음. library/OS 내부의 자동 관측 부재까지 입증하지 않음.

## 실제 수행한 확인과 결과

1. 파일 목록·로컬 지침·대화·관련 문서·코드를 읽고 보고서 4개와 진입 HTML을 작성했다. 제품 파일·Workspace 상태·Git을 변경하지 않았다.
2. root/client `node_modules` 부재를 확인했다. Node 실행 파일은 있었다. 추가 설치나 Jest 실행은 하지 않았다. 523 passed / 1 skipped는 기존 기록의 보고 수치이며 이번 검사 수치가 아니다.
3. `date-check.cjs`로 실제 `getUTCDateRange` 본문에서 TypeScript 표기만 제거해 Node VM에서 실행했다. 홈·local grouping은 동일한 Date 구성요소 방식의 독립 예시로 계산했다. 앱·DB의 실제 실행이 아니다.
4. 가정 입력은 start `2026-09-30T00:00:00+09:00`, end `2026-10-02T00:00:00+09:00`, 일정 `2026-10-02T09:00:00+09:00`. 원본 DB 값으로 가장하지 않았다. Seoul/UTC/LA 각각의 결과를 `date-check.json`에 보존했다. UTC 범위 9/29~10/1, Seoul 홈 9/30~10/2, Seoul 10/2 일정이 범위 밖임을 assertion으로 확인했다.
5. `validate_reports.py`로 HTMLParser 구문 처리·한국어 lang·문서당 h1 1개·모든 로컬 href 존재·이미지 위조 없음(이미지 태그 0개)을 확인한다. 실행 결과는 `html-check.json`에 남겼다. 이는 브라우저 렌더 품질 검사가 아니다.
6. 첫 사용자 결과 응답은 `response.md`, 실제 조사 기록은 이 `worklog.md`로 구분했다. HTML에서 각 주장 관련 코드/문서 발췌와 원문 경로를 열 수 있게 했다.

## 실행하지 못한 확인과 필요한 추가 자료

- 시뮬레이터와 새 스크린샷 수집: 당시 앱·런타임·DB가 필요하다. 원래 홈 HTML 디자인·캡처를 전달받아야 동일한 형식과 이미지 배치를 대조할 수 있다.
- 6.1 sol 워커 병렬 운영: 이번 환경은 단독 실행이며 추가 subagent 금지다. 병렬 실행을 했다고 보고하지 않는다.
- 앱 Jest/typecheck: snapshot에 의존성이 없다. 승인된 기존 의존성 환경이 필요하며 이 실행에서는 설치·네트워크 접근을 하지 않았다.
- foreground 네트워크 호출/화면/sync 관찰: app 수명 listener 구현 뒤, 복귀 전후 상태와 시각·호출 로그가 필요하다.
- native picker·키보드·취소 경고, 실제 단절 Local 저장·복구 sync: 실제 앱, Local DB와 격리된 API/DB가 필요하다. Debug override는 쓰기를 막으므로 실제 단절을 대신하지 못한다.
- 원래 날짜 문제의 재현: Trip·Schedule 원문 시각, 기기 시간대와 같은 여행의 홈/목록 캡처가 필요하다. 독립 예시는 당시 사건 재현이 아니다.
- HTML 시각 검증: 현재 앱/브라우저에 접근하지 않는 제약에서 정적 검사만 수행했다. 실제 브라우저 렌더·모바일 폭·스크린샷 검증은 미실행이다.
- 보류·후속 티켓의 runtime 결함 전수 재현은 요청 범위를 넘겨 실행하지 않았다. 필요한 자료·검사 책임을 ⑤에 연결했으며, 원래 보류를 해제하거나 완료를 선언하지 않았다.

## 탐색 중 존재하지 않았던 경로

`current/index.md`, `shared/services/policy-query/read-query.ts`, `read-view.ts`, `shared/db/sync-queue.ts`, `SchedulesScreen*`는 해당 snapshot에 없었다. 실제 `current/memory/index.md`, `current/state/index.md`, `usePolicyReadQuery.ts`, `ScheduleScreen.tsx`와 cleanup 실제 caller로 조사 경로를 바로잡았다. 없는 파일을 읽었다고 보고하지 않는다.
