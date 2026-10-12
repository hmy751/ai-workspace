# Workspace 내부 읽기본

이 파일은 [보존 원본](<../../../noline-evaluation/reviews/withdrawal-followup-comparison.md>)의 Markdown 링크를 보존된 내부 사본으로 연결한 파생본이다. 본문 주장은 당시 평가이며 현재 설계의 확정안이 아니다. 사본이 없는 링크는 원래 외부 경로로 남겼다.

---

# 9/17 철회 구현과 Ticket 06 후속 구현 비교

**결론: 9/17 철회를 ‘가독성 Spec 밖 동작 개선의 무단 확대’로 확정할 수 없다.** 당시 Main은 적용 항목과 제외 항목을 설명했고 사용자는 관련 Ticket·합의 확인을 재차 요구한 뒤 진행을 승인했다. 후속 Ticket 06은 폼 보존·대상 여행 라우팅·sync 보호를 실제 채택했고, 온라인 복구의 공개 조건과 실행 구조는 바꿨으며 복구 알림은 제외했다. 철회는 구현 전체의 일괄 부정이나 후속 구현의 동일성 증거가 아니다.

## 근거와 시간 경계

- 대화 원문: [9/17 corpus](<../../../noline-evaluation/corpus/01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30/messages.jsonl>), `source_line` 274·296·339의 합의 대조 요구 → 312의 채택·제외 설명 → 351 “좋아 작업 진행시켜” → 895·913·963의 완료·범위·작업물 설명 → 970의 철회.
- 철회 원문 최소 발췌: “작업의 범위가 너무 커진것 같아 다시 되돌려놓자 … 동작의 개선보다 가독성 응집도 뭐 파악쉬운 등의 spec 목표정도의 코드 퀄리티 … 계속 범위가 커질 것 같아”. 이 발화는 당시 범위 부담을 직접 보여 준다. 품질 불만·복잡성·일시적 축소 중 하나를 유일 원인으로 확정하지 않는다.
- 이번 사용자 인터뷰는 동작 개선을 많이 의도적으로 구현했다는 설명과 당시 철회 이유를 정확히 기억하지 못한다는 한계를 함께 포함한다. 인터뷰로 당시 철회 발화를 지우거나, 당시 발화로 인터뷰의 의도 설명을 무효화하지 않는다.
- 실제 철회안은 미커밋이다. [원본 위치](<../../../noline-evaluation/corpus/01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30/meta.json>)의 `path`가 가리키는 rollout에서 **물리행 639·932·940·949·958**의 도구 출력으로 아래 주요 소스를 직접 확인했다. 768은 `cancelRefetch: false` 적용 patch, 870은 Jest 20 suites·205 tests 통과 직접 출력, 995는 baseline 복원·byte 비교 PASS 출력이다.
- 후속 비교 기준은 Git의 `4fb309d2ba50afaca44019879d7161964b9b2328`(2026-10-06). `git show <commit>:<path>`로 지정 시점 소스를 읽었다. 아래 `apps/client/` 경로의 줄 번호는 해당 commit 기준이다. 9/29 기록에 나오는 별도 미커밋 복구안의 `required`·QueryCache 구독 구조를 9/17 구현과 동일시하지 않는다.

## 행동별 비교

### 1. offline/unknown → online 조회와 내용 공개: 목적 일부 채택, 공개 조건·상태 소유 변경

9/17 `shared/policy/useTripContentAccess.ts`는 Query와 별도로 `Recovery { tripId, blocked, hadOffline, phase }`, `requestVersion`, `notice`를 소유했다. 실제 offline/unknown을 겪은 비활성 여행은 online에서 refetch하고 성공 전 `loading`, 실패 후 `error`, 성공 후 `ready`로 공개했다. 여행 이동·다시 끊김·unmount의 늦은 결과도 별도로 배제했다(raw 639·940). raw 958의 실제 Query observer 테스트는 캐시가 남아 있어도 성공 전 두 소비자 내용을 숨기는 기대를 확인한다.

후속 `57d878f2`의 `screens/ScheduleScreen.tsx:67-75,275-283`은 표시 정책과 실제 정책 모두 허용될 때 Query를 켜되, **표시 정책이 허용하면 기존 Query 데이터를 즉시 공개**한다. 데이터가 있는 갱신 실패는 내용 유지와 별도 실패 안내, 데이터가 없는 최초 실패는 오류 화면이다. `b4db89dc`의 `shared/services/policy-query/usePolicyReadQuery.ts:22-31,45-65`는 Query 소유 상태를 `view`로 해석하고 정책을 적용한 `actions.refetch`를 별도로 제공하며 복구 성공 상태를 따로 저장하지 않는다. `useTripReadAccess.ts:19-35`는 소비처 enabled·표시 정책·실제 정책을 조합한다. `ed50ce1b`는 경비 목록·상세, `eec00e1`는 일정 상세·폼·홈으로 연결했다.

판단: 제한 중 캐시 보존과 실제 요청 차단은 이어졌다. ‘반드시 새 조회 성공 후 공개’는 제거됐다. [9/29 결정](</Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/002-code-readability-refactoring/records/2026-09-29-02-schedule-recovery-query-sync-decision.md>):5·54-58은 화면이 sync 종료를 기다리지 않고 Query 갱신과 추가 조회를 허용한 이유를 설명한다. 이는 후속에서 사용자가 복잡도를 재판단한 증거이며 9/17 철회 동기의 확정 근거는 아니다.

### 2. 열린 폼 입력 보존·실패 이유·명시적 재시도: 채택하되 단계별 보완

9/17 `screens/CreateExpenseScreen.tsx:44-59`는 제한 안내와 같은 `ExpenseForm`을 함께 유지했다. `shared/policy/mutationErrorMessage.ts:3-5`는 `OfflineError.message`와 일반 실패 문구를 구분했고 생성 실패에서 폼을 닫거나 자동 저장하지 않았다(raw 949; 당시 설명 963).

후속 `be2f5b9`는 제한 안내와 Local 입력·기존 일정 연결 보존을 연결했지만, 수정 Drawer에는 정책 제한 시 본문 대신 block 안내를 반환하는 구조가 남았다. 따라서 이 commit만으로 9/17과 같은 전체 폼 표시·보존 흐름이 완료됐다고 할 수 없다. `669aad1d`와 `eec00e1`은 조회를 열린 폼 수명·접근 정책에 연결했다. `78acff5`는 일정 생성 초안과 장소 검색 책임을, `a8e60a7`는 경비 생성·수정의 지속 입력·일정 연결·저장 실패를 별도로 보완했다.

최종 `features/expense/update-expense/UpdateExpenseDrawer.tsx:70-84,112-129`는 대상 ID 변경 시 reset, 실패 시 오류 상태만 갱신, 정책 변화에도 폼 본문 유지로 연결된다. `features/expense/expense-form/submit-error.ts:5-9`는 Offline·Auth·API 오류 이유와 일반 실패 문구를 구분한다. `screens/CreateScheduleScreen.tsx:75-102`는 검색·폼 단계와 제출 제한을 연결한다. 판단: 같은 사용자 가치가 후속 채택됐지만 오류 체계·제출 수명·초안 책임이 달라졌으며 영구 draft 저장이나 앱 재시작 복원을 입증하지 않는다.

### 3. sync 준비 조건·중복 방지·debug 연결: 채택, 중복 호출의 반환 의미 변경

9/17 `shared/services/sync/provider.tsx:44-108`은 DB 성공·auth 준비·로그인·실제 online·override 해제를 검사하고 Provider 안 `inFlightRef`로 진행 중 **동일 Promise를 공유**했다. Root가 DB 성공을 prop으로 넘겼고 debug는 Provider의 `triggerManualSync`를 사용했다(raw 932·958). `completed`는 engine 반환이며 queue 전체 반영 보장이 아니었다.

후속 `6efdfed`는 Provider·정책·Router를 정리했고 `029adb6`는 실행 소유를 별도 `sync/lifecycle.ts`로 옮겨 자동·수동 호출과 세션 종료를 연결했다. 최종 `shared/services/sync/lifecycle.ts:40-67,70-95`는 DB·auth·network·override·세션 종료 조건과 전역 `activeSync`를 검사하고, **중복 호출에는 기존 Promise 합류 대신 `skipped/already-running`을 반환**한다. `withSyncPaused`는 새 실행을 막고 기존 실행을 기다린 뒤 종료 작업을 한다. `sync/provider.tsx:45-56,79-80`은 조건 변경 계기와 수동 요청을 그 실행층에 연결한다.

판단: 보호 대상은 유사하지만 실행 Owner, 세션 전환 경계, 호출자에게 전달되는 결과가 다르다. ‘중복 방지 채택’을 ‘같은 구현 재채택’으로 쓰면 틀린다.

### 4. 대상 여행 Router와 inactive child Local 선조회 제거: 실제 후속 채택, 목록 계약은 추가 변화

9/17은 Trip 수정·삭제를 대상 tripId로 분기하고 Expense 수정·삭제·일정별 조회에 tripId를 명시해 비활성 데이터의 Local 선조회 실패를 제거했다. raw 940의 `router.ts:71-88`, `expense-repository.ts:36-78`와 당시 설명 963이 같은 호출 경계를 보여 준다.

후속 `f0f680eb`(2026-09-19)는 repository·mutation hook·화면·회귀 테스트 14파일에 이 경계를 연결했다. 최종 `shared/services/offline-prep/router.ts:60-93`과 `entities/expense/repository/expense-repository.ts:37-78`에서도 대상 여행과 명시 tripId가 유지된다. 이후 인증·소유권 조건이 더해졌으며 최종 `routeTripQuery:38-57`는 실제 online의 서버 목록 우선과 제한·서버 접근 실패 시 Local fallback을 갖는다. 이는 9/17 설명의 ‘활성 여행이 있으면 Local 목록 유지’와 다르다.

판단: 선조회 제거와 대상 여행 쓰기 분기는 명확한 후속 채택이다. 전체 Router 동작이 같거나 당시 광범위한 소비 연결을 한 번에 수행하는 선택까지 적절했다는 증거는 아니다.

### 5. 복구 성공 알림: 제외

9/17 복구 hook은 offline을 실제 겪은 경우 성공 후 `notice`를 만들고 3.5초 뒤 지웠다(raw 639·940). 화면은 `TripRecoveryNotice`를 렌더했다(raw 958). 초기 unknown 해소와 단순 재확인은 알림 대상에서 제외했다.

후속 `c5d42697`는 제품 코드 추가 없이 [9/30 결정 기록](</Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/002-code-readability-refactoring/records/2026-09-30-02-recovery-toast-and-ux-review.md>):5-19에 현재 복구 토스트 제외를 남겼다. 캐시 즉시 공개·상단 상태·제한 안내 소멸·일반 조회 오류가 이미 복귀와 실패를 전달한다는 판단이며, UX 관찰에서 부족함이 드러나면 재검토하는 조건이다. 이 항목을 ‘구현 완료’나 ‘알림이 영구 불필요함’으로 올리지 않는다.

## 평가를 바꿀 사실과 남은 한계

1. 9/17에는 Main의 범위 대조 설명 이후 명시적 진행 승인이 있다. 가독성이라는 Spec 명칭만으로 동작 개선 전체가 무단이었다는 판정을 철회해야 한다.
2. 철회안 주요 코드는 원본 도구 출력·patch로 확인된다. 기존 [코드 대조](<noline-change-evidence.md>)의 ‘Git에 없어서 복구안 검증 불가’는 **확정 commit 없음 / 주요 실제 미커밋 코드 확인 가능**으로 좁혀야 한다.
3. 폼 보존·대상 여행 라우팅·sync 보호는 후속 실제 채택됐다. 철회 전체를 기능 방향의 거부로 코딩하면 후속 근거와 충돌한다.
4. 복구 공개는 성공 대기에서 캐시 즉시 공개·Query 상태 재사용으로 바뀌었고 sync 중복 결과도 달라졌다. 유사 기능의 후속 채택은 당시 구현 품질·복잡성·적절성을 자동 증명하지 않는다.
5. 복구 알림은 별도 후속 결정으로 제외됐다. 최종 Ticket 06은 철회안을 단순 복원한 결과가 아니라 채택·수정·제외와 소비처 확장을 거친 결과다.

현재 비교는 제품 코드·사용자 선택·Work 기록만 다뤘고 Maintain 하네스 성능은 평가하지 않았다. 205개 테스트 통과는 당시 직접 출력으로 확인했으나 native 네트워크·실서버·SQLite·navigation stack 전체 검증이나 제품 품질 수락을 뜻하지 않는다. 이번 조사에서 제품 실행을 재현하지 않았다. 당시 원래 범위 대비 증가량 전체와 사용자가 철회한 단일 동기는 이 근거만으로 확정할 수 없다. 이후 단계별 채택이 더 나은 작업 순서였다는 관찰과, 그것이 철회의 원인이었다는 추론도 구별한다.
