# 실제 작업 기록

## 실행 범위

- 작업 루트: `/private/tmp/briefing-first-report-20261021/r42`
- 입력은 이 루트의 `environment.md`, `conversation.txt`, `repository/`만 접근했다. 두 입력을 첫 호출에서 원래 순서대로 읽었다. 원문을 요약으로 교체하지 않았다.
- repository는 제공 환경 설명상의 HEAD `0b3b167c8b8d15dc1a45d87da934dfc5efaed994` tracked snapshot이다. Git 메타데이터가 없으므로 branch·HEAD·working tree를 실제 Git 명령으로 확인했다고 주장하지 않았다.
- 모든 쓰기는 `output/`에만 했다. repository·바깥 workspace·다른 실행·원본 저장소·기존 메모리·네트워크·현재 앱에 접근하지 않았다. 추가 설치·서브에이전트 실행도 하지 않았다.
- 마지막 사용자 답변은 앞서 설명한 ② foreground 재확인 ③ 종합 UX ④ 날짜 차이 ⑤ 보류·후속 경계 네 편으로 범위를 확정했다. 앞선 시뮬레이터 화면·worker 실행·523개 통과는 과거 대화/기록이며 이번의 새 증거로 사용하지 않았다.

## 실제 읽은 지침·스킬·맥락

repository 기준 상대 경로다.

- `CLAUDE.md` (루트 `AGENTS.md`는 이 파일의 symlink), `apps/client/CLAUDE.md`
- `context/README.md`, `context/work/AGENTS.md`
- `context/work/workspaces/002-code-readability-refactoring/README.md`
- `.claude/skills/work-artifact-briefing/SKILL.md`: 읽었지만 이번 주목적이 새 조사 보고서 작성이라 자동 workflow로 따로 발동하지 않았다. 근거·원자료 구분을 참고했다.
- `.claude/skills/read-project-context/SKILL.md`: 실제 적용. 날짜 의미와 후속 책임에 필요한 본문을 선택해 대조했다.
- `context/project/README.md`, `context/project/REFERENCE/reading.md`, `context/project/guidance/explanation-and-evidence-criteria.md`
- `context/project/common/date-and-time.md`: 초기 큰 출력 일부가 잘려 후속 호출에서 관련 날짜 의미·UTC 범위·열린 Trip 의미 구간을 직접 재확인했다.
- `context/work/workspaces/002-code-readability-refactoring/current/state/index.md`
- 같은 Workspace `current/memory/tickets/06-app-startup-lifecycle.md`: 전체 읽기 시도에서 출력 일부가 잘림. 첫 범위·정책·startup·후반 구현·보류·검증·후속을 출력된 구간과 후속 제한 읽기로 확인했다. 잘린 중간 전부를 읽었다고 주장하지 않는다.
- 후속 티켓 실제 읽기: `08-date-selection-grouping.md`, `10-schedule-form-lifecycle.md`, `11-expense-form-lifecycle.md`, `13-schedule-route-preparation.md`, `14-local-mutation-router-transaction.md`, `15-sync-result-retry-pull-types.md`, `16-unsynced-data-cleanup.md`, `07-client-api-boundaries.md`, `17-server-data-route-boundaries.md`. 일부 묶음 출력은 잘려 실제 확인된 본문 구간과 state의 범위만 사용했다. 전체 구현 audit가 아니다.
- `.gitignore`: `/artifacts/ticket-06-simulator/` 제외 규칙 확인.
- 글로벌 스킬은 입력 접근 제한으로 새로 읽지 않았다. 추가 subagent 금지는 environment.md의 공통 제약을 따랐다. UI·시뮬레이터가 없어 start-app을 적용하거나 실행하지 않았다.

## 직접 확인한 주요 코드·검사 경로

- `apps/client/src/application/AppInitialization.tsx`: mount init, unmount cleanup, DB→auth 준비; AppState 연결 없음.
- `apps/client/src/shared/store/network.ts`: session, refresh Promise 공유, 늦은 결과 revision 방어, timeout, 실제/표시 상태 구분.
- `apps/client/src/shared/services/sync/provider.tsx`: eligibility 변화 기반 시작; online 유지 복귀 자체의 강제 sync는 아님.
- `apps/client/src/shared/services/policy-query/usePolicyReadQuery.ts`, `useTripReadAccess.ts`: 표시 제한 우선, 캐시 ready/refreshFailed, 실제 재조회 guard.
- `apps/client/src/screens/HomeScreen/index.tsx`, `MainTripSection.tsx`, `TripsSection.tsx`: 현지 날짜, 별도 일정·경비 요약, 자동 대표 여행 선택.
- `apps/client/src/screens/ScheduleScreen.tsx` 관련 구간: UTC 범위 소비, 현지 날짜의 일정 그룹.
- `apps/client/src/screens/ExpensesScreen.tsx` 관련 구간: UTC 범위와 일반 삭제 오류.
- `apps/client/src/screens/ExpenseDetailScreen.tsx`: ID 없는 캐시+오류 feedback와 canFetch guard.
- `apps/client/src/screens/CreateScheduleScreen.tsx`: 사용자 단계·상위 draft·단일 폼·picker callback.
- `apps/client/src/features/schedule/create-schedule/useSubmitSchedule.ts`: 저장 후 500ms timer, capture한 목록, 정상 숫자 0의 route projection truthy 분기.
- `apps/client/src/features/expense/create-expense/useCreateExpenseForm.ts`: 최초 기본 통화, 초안·제출 잠금·오류 보존.
- `apps/client/src/features/expense/expense-form/ExpenseScheduleField.tsx`: 기존 연결 설명 기억, 날짜별 후보, 제한 중 연결 해제.
- `apps/client/src/shared/lib/datetime.ts`: `getUTCDateRange`, local 표시·변환, UTC 자정 helper 관련 구간.
- `apps/client/src/entities/trip/api/trips.ts`, `apps/server/src/routes/trips.ts` 관련 검색·발췌: PATCH/PUT 정적 불일치. server 전체 분석은 하지 않음.
- `apps/client/tests/shared/store/network.test.ts`: test 이름·선택 본문, refresh·late result·cleanup 시나리오.
- `apps/client/tests/shared/services/sync/provider-network.test.tsx`: 시나리오 이름 검색.
- `apps/client/tests/shared/services/policy-query/read-query.test.tsx`: 시나리오 이름 검색.
- `apps/client/tests/screens/read-query-consumers.test.tsx`: 전체 시나리오 이름·상세/홈 회귀 본문.
- `apps/client/tests/screens/schedule-recovery.test.tsx`, `expense-recovery.test.tsx`: 시나리오 이름과 선택 구간.
- `apps/client/tests/screens/create-schedule-flow.test.tsx`, `create-expense-flow.test.tsx`: 시나리오 이름·mock 구간 및 보고서에 보존한 테스트 발췌.
- `apps/client/package.json`: test 및 의존성 구성. 실제 설치는 없음.

## 실제 수행한 확인과 결과

1. 입력과 repository 로컬 지침을 읽고 파일 검색으로 대상 범위를 찾았다. 몇몇 후속 티켓명과 policy-query 파일명을 처음 추정해 읽으려다 없는 경로 오류가 났고, 파일 목록에서 실제 이름을 확인해 수정했다. 존재하지 않는 자료를 근거로 쓰지 않았다.
2. client `src`, `app`, tests에서 AppState/refresh 및 날짜 사용처를 검색했다. client 제품 코드에서 AppState 사용을 발견하지 못했고 AppInitialization의 mount/unmount 수명만 확인했다. NetInfo 내부 플랫폼 동작 부재까지 주장하지 않았다.
3. 네트워크 Store와 sync·조회 소비를 직접 읽었다. foreground 연결 부재와 이미 있는 refresh 기능을 구분했다. 새 코드 수정 없음.
4. 날짜 함수 확인: `output/date-probe.cjs`가 제공 source에서 `getUTCDateRange`와 홈 `formatDate` 본문을 추출하고 TS 타입만 제거해 Node에서 실행했다. UTC·Asia/Seoul·America/Los_Angeles × offset 예시·UTC 자정 예시·DST 경계 예시 = 9개 입력/시간대 조합 결과를 `date-probe.json`에 저장했다. 서울 offset 예시는 홈 9/30~10/2, 목록 9/29~10/1; LA UTC 자정 예시는 홈 9/29~10/1, 목록 9/30~10/2. 실제 앱·DB·Jest 테스트가 아니다.
5. HTML은 외부 의존성 없이 네 편과 index로 생성했다. 각 보고서에 확인·미확인·다음 수집·코드 발췌를 포함했다. 없는 screenshot을 그리거나 이미지 파일로 꾸미지 않았다.
6. 보고서 생성 중 코드 발췌의 끝행을 실제 파일 길이보다 크게 지정한 3개 assertion을 만나 범위를 실제 길이로 고쳤다. 최종 생성은 성공했다.
7. HTMLParser로 다섯 HTML의 ko 언어·title·ID 중복 없음·내부 anchor·상대 파일 링크 존재를 확인했다. 결과 `output/validation.json`. 모두 성공. 이미지 태그는 0개로 확인해 가짜·깨진 screenshot 연결이 없음을 확인했다. 브라우저 렌더·시각 QA는 하지 않았다.
8. `repository/node_modules`, `repository/apps/client/node_modules`, `repository/artifacts`가 없음을 경로 확인했다. 제품 test는 실행하지 않았다. 과거 테스트 통과 숫자를 이번에 다시 센 것으로 쓰지 않았다.

## 산출물

- `response.md`: 이 환경에서 사용자에게 보낼 첫 결과 응답 전체.
- `index.html`: 네 편 진입점.
- `02-foreground.html`, `03-ux.html`, `04-dates.html`, `05-scope.html`: 독립 HTML 보고서 네 편.
- `date-probe.cjs`, `date-probe.json`: 이번 실제 날짜 함수 실행 방식·결과.
- `build_reports.py`: 보고서 생성 및 원자료 행번호 발췌.
- `validation.json`: HTML 정적 링크·구조 확인 결과.
- `worklog.md`: 이 실행 기록.

## 실행하지 못한 확인과 필요한 추가 자료

- 시뮬레이터·앱 UI 조작, native picker/keyboard/취소 React 경고 확인, 앱 background→active 로그, 실제 통신 단절 Local 저장, sync·서버 DB 반영: 당시 실행 환경과 격리된 계정·여행 fixture, 접근 가능한 시뮬레이터/API/DB가 필요하다.
- Git 제외 HTML와 screenshot 원본이 없다. 9/30 UX 보고서와 10/4 home-review의 HTML/이미지 파일을 제공받아야 실제 이미지와 함께 보고서를 완성할 수 있다. 제공 대화의 과거 보고를 원본 캡처처럼 사용하지 않았다.
- 날짜 과거 원인 확정: 동일 tripId의 당시 raw start/end, 기기 시간대, 홈/목록 첫날·마지막날 캡처 필요. 예시 함수 결과는 그 대체물이 아니다.
- Jest·typecheck·빌드: 당시 의존성 환경이 필요. 추가 설치를 금지한 환경이므로 설치/실행 시도하지 않았다.
- 시뮬레이터 수집자가 반환할 최소 자료: 조작 순서, tripId·활성 여부·real/override 상태, 화면 문구·입력 값·캡처, 실패/재시도의 실제 요청 결과. foreground는 상태 전환/refresh 시작·종료·횟수 로그가 추가로 필요.
- 이번 실행은 병렬 worker를 만들지 않았으며 과거 worker 내부 로그도 읽지 않았다. 보고서 네 편 작성은 완료했지만 스크린샷 동반 실앱 확인 및 티켓 완료는 남는다.
