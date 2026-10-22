# 작업 기록

## 실행 범위와 산출물

- 입력 루트: `/private/tmp/briefing-first-report-20261021/r88`.
- `environment.md`, `conversation.txt`를 첫 호출에서 순서대로 읽었다. 대화 마지막 요청은 앞서 정리한 2~5번 각각의 HTML 보고서 작성이며, 이전 스크린샷 보고서와 같은 방식의 수집·조사를 원했다.
- repository는 제공된 0b3b167 tracked snapshot으로 다뤘다. Git 메타데이터가 없어 branch·working tree·commit 자체를 독립 확인하지 않았다.
- 모든 쓰기는 `output/`에만 했다. repository·외부 원본·다른 실험·바깥 워크스페이스·네트워크·현재 앱에 접근하지 않았다. 추가 subagent를 만들지 않았다.
- 산출물: `index.html`, `02-foreground.html`, `03-ux.html`, `04-dates.html`, `05-scope.html`, 첫 결과 응답 전체 `response.md`.
- 보조 근거: `date-check.json`, `date-check.stderr.txt`, `report-source-manifest.json`, `validation.json`. 생성/재실행 스크립트 `build_reports.py`, `check-dates.mjs`도 output에 있다.

## 실제 읽은 지침·스킬·Project 문서

아래 경로는 repository 기준이다. 전체 출력이 도구 한도를 넘긴 일부 긴 배치는 필요한 구간을 후속 targeted read로 재확인했다. 전체 문서·모든 history를 읽었다고 주장하지 않는다.

- `CLAUDE.md` (AGENTS.md symlink의 원천), `apps/client/CLAUDE.md`, `apps/server/CLAUDE.md`, `context/work/AGENTS.md`.
- `.claude/runbooks/first-result-report.md`와 `context/project/guidance/explanation-and-evidence-criteria.md`: 생성 사실만으로 검토 종료를 주장하지 않고 현재 결론·근거·남은 행동을 응답에 종합.
- `.claude/skills/read-project-context/SKILL.md`: 적용. `context/project/README.md`, `context/project/REFERENCE/reading.md`를 통해 관련 날짜 canonical 선택.
- `.claude/skills/work-artifact-briefing/SKILL.md`: 읽었으나 이번 주목적은 새 검토·보고서 생성이어서 별도 briefing workflow로 확대하지 않았다.
- `context/project/common/date-and-time.md`: Trip datetime/달력 날짜의 열린 의미와 공통 UTC 범위 대조.
- `.claude/guards/README.md`, `.claude/runbooks/README.md`의 관련 진입 구간, `.claude/rules/policy-ui.md`.
- `.gitignore`, `apps/client/package.json`: ignored artifact 경로·의존성·검사 명령 확인.
- 외부 글로벌 skill 파일은 허용 입력 범위 밖이므로 읽지 않았다. HTML 신규 작성은 시각 원자료 변환이 아니므로 visual-source skill은 적용하지 않았다.

## 실제 조사한 Ticket

`context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/` 아래:

- `06-app-startup-lifecycle.md`: 맡은 결과, 정책, 구현·검증 기록, 보류와 마지막 다음 경계. 긴 파일의 최초 출력은 일부 잘려 필요한 첫 125행과 마지막 결과 구간을 대조했다.
- `08-date-selection-grouping.md`, `13-schedule-route-preparation.md`, `15-sync-result-retry-pull-types.md`, `16-unsynced-data-cleanup.md`: 본문과 현재 상태.
- `07-client-api-boundaries.md`, `10-schedule-form-lifecycle.md`, `11-expense-form-lifecycle.md`, `14-local-mutation-router-transaction.md`, `17-server-data-route-boundaries.md`: 관련 범위·현재 상태 검색 결과와 발췌.
- 003 보고서 전체는 다시 읽지 않았다. 해당 담당 관계는 002 Ticket의 명시적 연결로 한정했다.

## 주요 코드·검사 입력

`apps/client/src/` 아래:

- `application/AppInitialization.tsx`: mount init/cleanup, DB/auth 준비. 앱 복귀 AppState 연결 없음.
- `shared/store/network.ts`: refresh 공유 Promise, session/revision 방어, unknown 안내·timeout, real/override 분리.
- `shared/services/policy-query/useTripReadAccess.ts`, `usePolicyReadQuery.ts`: 실제/표시 정책, enabled/refetch 차단, blocked/ready/error 표시 순서.
- `features/schedule/read-schedules/useTripSchedulesReadQuery.ts`, `features/expense/read-expenses/useTripExpensesReadQuery.ts`: entity 조회 연결.
- `shared/services/sync/provider.tsx`: realStatus 변화와 eligibility의 sync 소비.
- `screens/HomeScreen/MainTripSection.tsx`: 현지 날짜 formatter와 개별 요약 feedback.
- `screens/ScheduleScreen.tsx`: UTC 범위와 현지 일정 날짜 grouping, 제한·Drawer 유지.
- `screens/ExpensesScreen.tsx`: UTC 범위·오류·삭제 실패 일반 Alert 관련 구간.
- `screens/ExpenseDetailScreen.tsx`: 대상 부재·오류 분기와 retry canFetch 경계.
- `screens/CreateScheduleScreen.tsx`: 단계와 draft의 수명, 단일 폼.
- `features/expense/create-expense/useCreateExpenseForm.ts`: defaultCurrency 최초 defaultValues, submit 실패 후 초안.
- `features/schedule/create-schedule/useSubmitSchedule.ts`: 저장 후 500ms, route projection의 0 좌표 truthy 처리.
- `features/schedule/update-schedule/UpdateScheduleDrawer.tsx`: 500ms와 projection 검색 결과.
- `shared/lib/datetime.ts`: 실제 UTC 범위·현지 날짜 helper.
- `entities/trip/api/trips.ts`: PATCH 관련 발췌.
- `shared/services/sync/queue.ts`, `cleanup-job.ts`: PENDING 중심 여행 조회, processedCount 관련 검색 발췌.
- `apps/server/src/routes/trips.ts`: PUT route 발췌.

`apps/client/tests/` 아래:

- `shared/store/network.test.ts`: 검사명 목록과 222~380행의 공유·지연·timeout·cleanup 검사 본문.
- `shared/services/policy-query/read-query.test.tsx`: 검사명·조건 검색. 전체 실행 없음.
- `screens/read-query-consumers.test.tsx`: mock 설정과 상세·홈·보조조회·폼 보존 검사 본문.
- `screens/schedule-recovery.test.tsx`: mock 설정, 유효/stale 복귀, 재조회 실패·재시도, 최초 실패 본문 및 기타 검사명.
- `screens/expense-recovery.test.tsx`: mock 설정, 복귀·최초 실패·부재·재조회 실패·제한·여행 전환 본문.
- `screens/create-schedule-flow.test.tsx`: 전체 검사명, 단일 폼·Local 호출·비활성 명시적 재시도 본문.
- `screens/create-expense-flow.test.tsx`: 전체 검사명과 활성 연결/날짜·비활성 초안·pending 실패 검사 본문.
- `app/layout.test.tsx`: init/cleanup 관련 검색. foreground 검사 실행으로 간주하지 않음.

보고서에 실제 포함한 28개 발췌의 경로·줄 범위는 `report-source-manifest.json`에 기록했다. 위 목록에는 검색으로만 확인한 항목을 본문 정독과 구별했다.

## 실제 수행한 확인과 결과

1. 앱 전체에서 AppState 사용 검색: 일치 없음. foreground 재확인 연결 부재를 source 범위로 판정. NetInfo 자체 전달이나 stale 현상 발생을 실행 확인한 것은 아니다.
2. 의존성·artifact 디렉터리 확인: root/client node_modules 및 artifacts 없음. Jest·native 환경이 제공됐다고 가정하지 않음.
3. Node v23.11.0으로 저장소 `datetime.ts`를 직접 import해 예제 start/end를 Asia/Seoul·UTC·America/Los_Angeles에서 계산.
   - 서울: 현지 날짜 2026-09-30~10-02, UTC 목록 2026-09-29~10-01.
   - UTC/LA: 예제의 현지 범위 2026-09-29~10-01.
   - 예상값 assertion 6개 통과. 특정 일정의 현지 날짜와 UTC 범위 포함 여부도 출력.
   - 홈 화면 자체를 실행한 것이 아니라, 소스로 현지 formatter를 대조한 뒤 같은 Date 현지 해석의 helper와 실제 UTC helper를 실행했다.
   - 원본 여행 DB 값이 아니며 과거 버그 재현으로 보고하지 않음.
   - 최초 즉석 계산 후 보존 가능한 script/JSON을 만들기 위해 실행을 반복. 설치·repository 쓰기 없음. Node type stripping 경고는 stderr 파일에 보존.
4. HTML 4편과 index 생성. 코드·검사 발췌를 HTML 내부에 넣어 외부 소스 링크 없이도 읽을 수 있게 함.
5. HTMLParser로 5페이지 파싱, 로컬 링크 존재·한국어 lang·이미지 태그 없음 및 발췌 줄 범위 확인: 통과. 모든 링크는 output 내부 페이지/JSON으로 연결.
6. 과거 523 passed / 1 skipped는 Ticket/대화 기록으로만 취급. 이번 Jest 통과라고 주장하지 않음. 과거 Sync 초기 지적과 같은 Ticket의 최신 개선 기록을 구분.

## 실행하지 못한 확인과 추가 자료

- 시뮬레이터 수집, native picker·키보드·취소 경고, 실제 통신 단절 Local 저장, DB·큐·서버 반영: 환경 미제공. 같은 여행의 활성 여부·ID, 실제/override 상태, 전환 전후 캡처와 로그가 필요하다.
- 기존 홈 HTML/9월 30일 캡처와 동일한 시각 형식의 정합성: gitignored 원본이 없음. 이전 report.html·원본 캡처를 받아야 비교 가능하다. 이를 임의 UI 이미지로 대체하지 않았다.
- 날짜 과거 장면 확정: 당시 Trip startDate/endDate와 기기 시간대, 여행 ID가 일치하는 홈/목록 캡처가 필요하다. 날짜 의미 변경에는 Trip form·대표 여행·활성 만료·API/DB 영향 대조가 필요하다.
- Jest·typecheck·native/DB 통합 검사: 의존성이 없고 추가 설치 금지. 기존 의존성을 갖춘 원래 환경에서 관련 검사 실행과 foreground 결합 검사를 추가해야 한다.
- HTML 브라우저 렌더링·화면별 시각 QA·미리보기 열기: 현재 앱 접근 금지이므로 미수행. 정적 검사를 시각 검사로 표현하지 않았다.
- 추가 6.1 sol 워커 구성: environment.md의 추가 subagent 금지에 따라 미실행. 3명 병렬 조사 또는 시뮬레이터 수집 수행을 주장하지 않았다.
- Ticket/Workspace 상태 갱신과 제품 수정은 실행 권한 범위 밖이므로 하지 않았다. 06 완료·acceptance를 기록하지 않았다.
