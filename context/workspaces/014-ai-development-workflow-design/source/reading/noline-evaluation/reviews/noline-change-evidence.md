# Workspace 내부 읽기본

이 파일은 [보존 원본](<../../../noline-evaluation/reviews/noline-change-evidence.md>)의 Markdown 링크를 보존된 내부 사본으로 연결한 파생본이다. 본문 주장은 당시 평가이며 현재 설계의 확정안이 아니다. 사본이 없는 링크는 원래 외부 경로로 남겼다.

---

# Noline 세 구현 흐름: 대화와 Git 변경 대조

평가 기준 HEAD는 `4fb309d2`다. 아래의 발화는 [원문 corpus](<../../../noline-evaluation/corpus>)의 `messages.jsonl`에서 확인했고, 장면 ID는 [장면 색인](<../scene-evidence.md>)과 연결한다. 확정 코드 변화는 지정 커밋의 `git show`로, Ticket 03의 미커밋 초안은 [원본 rollout 위치](<../../../noline-evaluation/corpus/01a08ff3-0e91-7921-afe4-69f0968638ef/meta.json>)의 도구 호출·출력으로 확인했다. 당시 실행 성공은 직접 출력과 대화 보고를 구별한다.

## 1. Ticket 03: 최초 범위 판단 → React 생명주기 개선 ([B01-S07](<../scene-evidence.md#b01-s07>), [B01-S08](<../scene-evidence.md#b01-s08>), [B02-S03](<../scene-evidence.md#b02-s03>))

사용자는 첫 수정 후 “니가 작업한거 커밋 해 문서 갱신하고”(`01a08ff3-0e91-7921-afe4-69f0968638ef:2580`)라고 했으나 곧 “티켓 범위 안에서 더 개선 해봐 코드 개찔끔이네”(`01a08ff3-0e91-7921-afe4-69f0968638ef:2645`), “리액트 적으로도 고려해야지”(`01a08ff3-0e91-7921-afe4-69f0968638ef:2767`), “프로덕션 수준의 퀄리티로 개선한다 생각해봐 이 파일 안에서”(`01a08ff3-0e91-7921-afe4-69f0968638ef:2819`)라고 처음 결과가 기대에 못 미친다며 파일 안에서 검토할 책임과 개선 깊이를 구체적으로 다시 요구했다. 후속 지침에 대해서는 “이 지금 상황을 모르는 main이 해결할정도의 변경”(`01a08e25-7e2b-7022-9d3a-d5b1c4e4f5fb:635`)을 요구했다. 첫 커밋 지시를 최종 품질 수락으로 읽을 수 없다.

실제 바뀐 경계·동작은 다음과 같다.

1. `653f8b8a`는 `apps/client/jest.config.cjs`, `package.json`, 환경 smoke test에 Jest 기반을 추가했다. 그 커밋의 `context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/03-storage-stats.md`는 stats 조립 중복 제거와 부분 실패 보존을 맡기고 병렬 조회·새 실패 상태·새 단위 체계는 제외했다. 제품 훅 변경은 이 커밋에 없다. **첫 제품 패치는 원본 rollout의 물리적 2472행 `apply_patch` 호출과 2537행 diff 출력에 남아 있다.** `formatBytes`를 hook 밖으로 옮기고 `createStorageStats(dbSizeBytes, mapSizeBytes)`를 만들었으며, 성공·catch의 `setStats` 두 곳을 `finally { setStats(createStorageStats(dbSizeBytes, mapSizeBytes)); }` 한 곳으로 바꿨다. DB·Mapbox 조회 흐름, effect, `refresh`와 겹친 요청 처리는 그대로였다. 이 패치는 2573행의 최초 완료 보고 전에 적용됐고 독립 커밋은 없다.
2. `a147a42c:apps/client/src/features/profile/hooks/useStorageStats.ts:24-115`는 이후 DB·Mapbox 집계, byte 검증, 실패 시 부분 합계, 최종 표시 객체 생성을 다시 분리했다. Git diff는 직전 확정 커밋의 원래 훅과 비교되므로, 1항의 미커밋 초안에서 바뀐 정도는 위 원본 patch와 함께 봐야 한다.
3. 같은 커밋 `useStorageStats.ts:117-139`는 `latestRequestId`와 effect cleanup으로 겹친 refresh의 오래된 결과 및 unmount 뒤 결과의 상태 반영을 막는다. 테스트 파일도 함께 추가됐지만 네이티브 런타임의 모든 생명주기 동작까지 입증하지는 않는다.
4. `d7223b7b:context/work/workspaces/spec-and-tickets/EXECUTION-CRITERIA.md:11-60`은 수정 목록과 맡은 결과를 구별하고, 코드 개선의 주요 흐름·완료 근거·미해결을 검토하도록 공통 기준을 바꿨다. `c902230`은 같은 기준 문서를 후속 보완했다. 문서 변경이 새 Main의 실제 실행 품질을 바꿨는지는 이 코드 diff만으로 판정할 수 없다.

**확인 수준·조건.** 첫 초안의 구체적 변경은 rollout 2472·2537행, 최종 코드는 Git으로 확인됨. 같은 rollout 2513행의 도구 출력은 변경 후 Jest 2 suites·7 tests 통과를 직접 보여주지만 전체 client `test:typecheck`는 기존 오류로 실패했다. 실제 native 동작과 최종 훅 품질의 인과, 공통 지침이 이후 새 Main의 실행 깊이를 바꿨는지는 추가 사례가 필요하다.

## 2. Ticket 05: 응답 변환·Zod·소유권, 그리고 별개의 DB 작업 직렬화 ([B02-S05](<../scene-evidence.md#b02-s05>)–[B02-S08](<../scene-evidence.md#b02-s08>), [B05-S11](<../scene-evidence.md#b05-s11>))

사용자는 “실제 코드와 컨텍스트랑 어떻게 구성되어 있나 그래야 내가 판단을 할거잖아”(`01a08ff3-bde0-7bd3-bd92-0dde7abc883d:676`)라며 기존 계약 확인을 요구했다. 테스트 도구 비교 후 “그래 좋아 그럼 이렇게 하고 문서좀 남겨줘”(`01a08ff3-bde0-7bd3-bd92-0dde7abc883d:1260`), “1,2,3 다 하자 이 티켓에서”(`01a08ff3-bde0-7bd3-bd92-0dde7abc883d:1512`)로 단계와 범위를 승인했다. serializer와 Zod에 대해서도 “겹치는게 있어보이기도 하고 근데 다른 역할인것 같은데”(`01a08ff3-bde0-7bd3-bd92-0dde7abc883d:2327`)라고 책임 경계를 재검토했다. B05-S11에서는 별개 로컬 DB 변경을 이해한 뒤 “아 애초에 catch가 전파를 막고 잡은거니 전파 안되겠구나”(`01a0b4fc-3afa-7462-ae9e-6052b5a9e3c0:3588`), 변수명 수정과 커밋을 지시했다(`01a0b4fc-3afa-7462-ae9e-6052b5a9e3c0:3598`).

1. `fe5722a0`은 서버 `vitest.config.ts`, Supertest 앱 지원 코드와 Schedule GET 응답 계약 테스트를 도입했다. 이는 후속 변경을 관찰할 기반이지, 자체로 실제 API 결함 수정은 아니다.
2. `7dd25211:apps/server/src/serializers/schedule.ts:7-16`의 `serializeSchedule`은 DB `Date`를 ISO 문자열로 변환한다. `schedules.ts`, `trips.ts`, `sync.ts`에 흩어진 날짜 변환을 호출로 바꿨다. 이어 `9d48b954:apps/server/src/routes/schedules.ts:73-94,246-271`, `trips.ts:329-347,418-471`은 Entity와 최종 응답을 중복 파싱하던 경로를 응답 Zod 검증 한 번으로 정리하고 DELETE·activation 응답도 schema로 검사한다. 값 변환과 계약 검증은 별도 책임으로 남았다.
3. `d7bf5ffb:apps/server/src/routes/schedules.ts:24-58,196-258`, `trips.ts:315-355,392-431`은 생성 시 부모 Trip 소유·삭제 상태를 확인하고, UPDATE/DELETE의 실제 SQL 조건에 사용자·soft-delete를 포함하며, Trip 하위 일정·activation 자식 조회에도 소유권 조건을 건다. `apps/server/tests/integration/schedules.access-boundary.test.ts:117-195`는 PostgreSQL용 네 경계 테스트를 포함한다.
4. B05-S11의 “직렬화”는 위 응답 serializer와 다르다. `9936662:apps/client/src/shared/db/index.ts:31-57`은 로컬 SQLite 작업을 Promise 체인에 순서대로 놓고, async 작업을 `BEGIN/COMMIT/ROLLBACK` 안에서 기다리게 했다. `utils.ts`의 `withTransaction`도 이 함수로 연결됐다. 실패를 흡수하는 `catch`는 **다음 작업을 진행시키는 내부 체인**에 붙고, 호출자가 받는 `result`의 실패는 유지된다.

**확인 수준·조건.** 경로별 SQL 조건·변환·검증·테스트 코드는 확인됨. “실제 PostgreSQL 14에서 4개 통과”, 클라이언트 254개 통과는 corpus의 당시 실행 보고이며 여기서 재실행하지 않았다. mock 테스트와 통합 테스트의 존재만으로 운영 DB의 모든 권한 경계가 안전하다거나 사용자의 DB 이해가 장기 유지된다고 말할 수 없다. B05-S11을 Ticket 05 서버 serializer의 후속 수정으로 합치면 원인이 잘못 연결된다.

## 3. Ticket 06: 온라인 복구 단순화 → 사용처 증가에 따른 조합 ([B07-S05](<../scene-evidence.md#b07-s05>)–[B07-S09](<../scene-evidence.md#b07-s09>))

사용자는 “무조건 다 구현도 아니고 그렇다고 억지로 다 간단하게 대충 하는것도 아니고”라며 기존 sync·정책까지 보라고 했다(`01a0ec21-e59e-7370-8432-8434271aa669:350`). 복구 조건을 줄이는 선택에는 “그래 그게 낫겟다 복잡도도 줄이고”(`01a0ec21-e59e-7370-8432-8434271aa669:666`)라고 응답했다. 중간 훅에는 “`useScheduleContent` 이게 상태를 가지는데 정책과 뭐가 다른지 잘 모르겠어”(`01a0ec21-e59e-7370-8432-8434271aa669:1046`)라고 의문을 제기했고, 뒤에는 정책을 거치는 `refetch`를 query 밖에 두자고 제안했다(`01a0ec21-e59e-7370-8432-8434271aa669:2633`). 적용은 “일단 다 적용하진말고 한군데 적용하고 마쳐봐”(`01a0ec21-e59e-7370-8432-8434271aa669:2740`)라는 선행 범위 제한을 받았다.

1. `57d878f2:apps/client/src/screens/ScheduleScreen.tsx:61-103,269-315`은 기존의 무조건 조회·로딩 중심 표시에서, 화면 정책과 실제 네트워크 정책으로 조회를 켜고, 캐시가 있으면 재조회 실패 중에도 내용과 오류 안내를 함께 보이는 흐름으로 바꿨다. `useAppPolicy.ts:19-42`는 화면 시뮬레이션용 `display`와 조회 가능성용 `real`을 구별한다. 이전 세션의 **미커밋 복구 시도**는 확정 Git 커밋이 없지만, 후속 원본 조사에서 실제 hook·화면·테스트 코드와 당시 테스트 출력이 확인됐다. “새 조회 성공까지 숨김” 조건도 직접 확인했으며, 후속 확정 구현은 그 조건을 제거했다. [철회안과 후속 비교](<withdrawal-followup-comparison.md>)를 따른다.
2. 같은 커밋 `apps/client/src/shared/services/sync/engine.ts:36-42,71-140,228`은 서버 변경 후 Query를 취소·무효화해 오래된 GET 결과가 남는 경로를 줄인다. `669aad1d:apps/client/src/shared/lib/query-refresh.ts:1-9`는 이 연산을 공통 함수로 빼고 수정 폼 조회를 열렸을 때만 활성화했다. `ed50ce1b`은 경비 목록·상세에도 제한, 캐시, 오류·재시도 흐름을 연결했다.
3. 처음 한 화면에서는 별도 `useScheduleContent`를 유지하지 않았고, 사용처가 일정·경비로 늘자 `b4db89dc:apps/client/src/shared/services/policy-query/useTripReadAccess.ts:1-36`, `usePolicyReadQuery.ts:22-65`가 접근 조건, 원본 Query 상태, 정책 적용 `actions.refetch`, 표시 `view`를 조합하도록 바뀌었다. 일정·경비 세 화면이 해당 조합을 썼다. `ffe022cc`는 남은 사용처를 Workspace 기록으로 남긴 문서 커밋이며, 다음 세션의 `eec00e1`이 상세·폼·홈의 추가 소비처로 확장했다.
4. 복구 토스트는 `c5d42697`에서 코드가 아니라 Workspace 결정 기록만 바뀌었다. 사용자 “그래 그렇게 하자”(`01a0ed7a-8db9-7883-a1fe-34e4390535ec:2580`)는 당시 토스트 제외 선택에 대한 수락이다. 추가가 필요해지는지는 뒤의 종합 UX 관찰 조건으로 남았다.

**확인 수준·조건.** 확정 커밋의 Query·Policy 경계와 추가 소비처는 확인됨. 354/406개 자동 테스트 통과, 시뮬레이터의 일부 복구 관찰은 당시 보고로 구별한다. 특히 폼이 열린 상태에서 입력 보존은 B07-S08 당시 남은 검증이었다. 토스트 제외를 전체 온라인 복구 검증 완료나 사용자 침묵에 의한 만족으로 읽지 않는다.

세 흐름 모두 사용자 개입 뒤 실제 변경은 확인되지만, 개입이 유일한 원인인지는 확정하지 않는다.  
Ticket 03의 최초 미커밋 패치는 원본 도구 기록으로 복원됐고 Ticket 06의 미커밋 복구안은 Git 전후 비교의 빈 구간이다.  
Ticket 05의 두 “직렬화”는 서버 값 변환과 클라이언트 DB 작업 순서로 분리해야 한다.  
커밋된 테스트 코드는 검증 설계의 증거다. Ticket 03 첫 변경의 실행 출력은 직접 확인했고, 그 외 여기 인용한 통과 수치는 당시 보고로 구분했다.  
후속 판단은 명시적 사용자 조건, 코드 경계, 미완료 검증을 함께 봐야 한다.
