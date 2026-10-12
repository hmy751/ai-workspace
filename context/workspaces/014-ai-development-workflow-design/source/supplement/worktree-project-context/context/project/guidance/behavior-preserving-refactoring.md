# 동작을 보존하는 코드 리팩터링

기존 제품 동작을 유지하면서 이름·조건·변환·흐름·내부 책임과 여러 소비 지점의 수정 부담을 줄일 때 읽는다. 명시적인 결함 수정이나 새 기능이 주목적이면 해당 작업의 제품 기준을 먼저 정하고, 이 가이드를 버그를 그대로 고정하는 근거로 사용하지 않는다.

이 본문은 Workspace 002에서 반복 확인한 리팩터링 판단을 Project 기준으로 통합한다. Ticket의 진행·수락·실행 수치와 시행착오는 Workspace에 남고, 다음 관련 작업이 적용할 계약은 여기서 소유한다. 중괄호·빈 줄·이름·주석·로그의 구체적인 표현은 새 기능에도 적용하는 [코드 표현 기준](code-readability.md)을 따른다.

## 수정 목록보다 맡을 결과를 먼저 정한다

**어떤 이해·수정 부담을 줄이고 어떤 동작을 보존할지 먼저 정한다.** 로그 삭제·helper 추출 같은 활동 목록으로 완료를 정의하지 않는다. 이름·조건·기본값·변환에서 문제를 찾는 것은 시작 순서이며 개선 깊이의 상한이 아니다.

| 범위를 판단할 때 | 적용할 기준 |
| --- | --- |
| 함수·파일 하나로 끝낼 수 있는가 | 같은 의미의 consumer·실패/상태 연결·schema·저장 경계까지 필요한 범위를 확인한다. |
| 가까운 코드도 함께 고칠 것인가 | 코드가 가깝다는 이유로 공개 동작 변경이나 별도 결함을 포함하지 않는다. |
| 일부만 먼저 정리할 것인가 | 그 단계의 결과, 남은 수정 부담과 후속 책임을 밝힌다. |
| Review가 개선을 제안했는가 | 원래 목표·합의·승인 범위와 대조한다. 제품 정책에 맞아도 가독성 작업의 필수 선행으로 자동 추가하지 않는다. |

발견한 오류는 숨기지 않고 필요한 수정과 별도 제품 작업을 구별해 이유를 설명한다.

## 보존할 계약은 관찰 가능한 관계다

입력과 반환값뿐 아니라 오류 전달, 저장 결과, 화면 변화, 부분 실패 뒤 남는 값, 부작용의 횟수와 순서, 비동기 응답의 최신성, 인증·삭제 필터도 변경에 관련되면 보존 계약에 포함한다. 모든 내부 호출 순서를 테스트로 고정하지 않고 결과를 갈라놓는 조건을 고른다.

변경 전 버그나 제품 의미가 불명확한 동작은 자동으로 정답이 아니다. 먼저 현재 결과를 재현하고, 의도된 계약·알려진 결함·열린 제품 선택을 구별한다. 결함을 고치거나 방어 동작을 새로 넣었다면 동작 보존과 의도한 변경을 따로 설명하고 검증한다.

## 변경 전후와 개선 효과를 따로 확인한다

가능하면 제품 코드를 바꾸기 전에 현재 경계를 특성화하고, 변경 후 같은 조건으로 비교한다. 테스트가 없다면 영향과 위험에 맞는 fixture·정적 대조·수동 관찰을 선택한다. 테스트가 구현 helper의 존재나 호출 순서를 그대로 복제해 내부 정리만으로 깨지지 않게 한다.

동작 보존이 확인돼도 가독성 개선이 자동으로 입증되지는 않는다. 변경 전 무엇을 여러 위치에서 추적해야 했는지 정하고, 변경 후에는 다음을 직접 비교한다.

- 값·조건·책임의 실제 의미가 이름·타입·가까운 흐름에서 읽히는가.
- 같은 의미의 수정 위치가 줄고 필요한 차이의 이유는 남았는가.
- helper나 범용 옵션이 간접 호출과 숨은 상태를 늘려 부담을 다른 곳으로 옮기지 않았는가.
- 완료 조건을 이미 고른 수정 목록에 맞춰 낮추지 않았는가.

긴 action을 줄일 때에는 한 요청의 Promise·timer·최신성·완료 책임이 흩어지지 않는지도 확인한다. Network Store처럼 공개 action은 흐름을 보여 주고 runtime 자원은 가까운 factory closure가 함께 소유할 수 있다. 짧아진 본문 뒤에 범용 manager·옵션·다른 파일 탐색이 늘었다면 부담이 줄었다고 단정하지 않는다.

## 영향에 맞는 검증 경계를 고른다

| 변경 대상 | 결과를 확인할 경계 |
| --- | --- |
| 이름·주석·저위험 표현 | Diff·사용처·관련 lint/type으로 충분할 수 있다. |
| 조건·계산·변환 | 결과를 나누는 입력·경계값의 변경 전후 비교 |
| React hook·비동기 | 실제 hook의 부분 실패·refresh·겹친 요청·unmount 뒤 결과. Native mock과 실기기는 구별 |
| Client API | HTTP 전 request 검증, 반환 전 response 검증, network/schema 오류의 호출부 전달 |
| Server serializer·route | 단위 변환과 실제 route 소비를 각각 확인. Ownership·soft-delete SQL은 격리 DB로 보완 |

결과를 가르는 입력은 독립적으로 둔다. 예를 들어 전역 활성 여행 존재와 대상 여행 활성 여부가 항상 같은 fixture면 잘못된 Router도 통과한다. 한쪽만 활성인 사례와 Local에 대상이 없는 Remote 경로를 실제 repository 진입에서 확인한다. 필요한 경우 잘못된 조건을 넣었을 때 검사가 실패하는지도 대조하되 모든 표현 수정에 별도 mutation test를 요구하지 않는다.

비동기 검사는 반복 microtask flush 횟수로 “충분히 기다렸다”고 추정하지 않는다. cleanup pause 진입·DB 저장 접수처럼 검증하려는 실제 사건을 관찰하는 Promise로 순서를 제어한다. React 반영 helper의 이름도 준비 전체가 완료된 것처럼 과장하지 않는다.

DB transaction은 호출 모양보다 adapter 경계를 확인한다. Async callback을 기다리는지, queue 실패 rollback이 entity에 적용되는지, 그 사이의 독립 DB 작업까지 취소하지 않는지가 실제 결과다. Drizzle query와 Node SQLite의 실패 주입은 SQL·순서에 근거를 주지만 Expo native 동작 전체를 대신하지 않는다.

실행하지 않은 native·외부 서비스·실제 인증·배포 경계를 통과한 것으로 넓히지 않는다. 전체 lint나 typecheck가 실패하면 변경 대상에서 새로 생긴 문제와 기존 실패를 구별하고, 우회한 규칙과 그에 따른 증명 상한을 남긴다.

## 혼합 변경을 나눌 때에는 각 결과를 따로 확인한다

한 파일에 서로 다른 동작 변경이 섞였으면 파일 단위만으로 검토·커밋 범위를 정하지 않는다. 각 묶음이 어떤 동작을 완성하는지, 필요한 consumer와 문서가 함께 들어가는지 설명하고 diff를 나눈다. 연결된 상태·저장 계약을 억지로 분리하기 위한 임시 호환 코드가 이해 부담을 더하지 않는지도 본다.

전체 작업 트리에서 통과한 검사는 그 안의 일부 변경만 담은 후보의 성립을 보장하지 않는다. 여러 미커밋 변경이 서로 의존할 수 있는 상태를 분리한다면 기준 commit에 해당 후보 diff만 반영한 별도 상태에서 필요한 검사를 실행하고, 실제 커밋할 tree와 검사한 대상이 같은지 확인한다. 모든 작은 커밋에 별도 tree를 요구하는 규칙은 아니다.

일부 범위의 검토·커밋 승인을 관련 소비부 전체 승인으로 확대하지 않는다. 고정된 다섯 단계 순서나 파일별 승인 절차를 모든 작업에 추가하지 않고, 현재 합의한 범위와 실행할 결과에 맞춘다. 검사 통과, 정책 채택, 커밋과 전체 사용자 수락은 각각 다른 판단이다.

## 완료된 사례에서 적용할 판단

| 사례 | 다음 작업에 적용할 판단 | 그대로 일반화하지 않을 것 |
| --- | --- | --- |
| 경비 합계 | 강조·라벨이 공유하는 첫 그룹 조건과 통화 자릿수 위치를 드러낸다. | 첫 그룹을 baseCurrency와 같은 뜻으로 이름 붙이거나 반올림 정책까지 결정하지 않는다. |
| [도시 검색](../current/city-search.md) | 요청·응답의 허용 code, 수도 예외·인구 경계·변환 책임을 함께 읽게 한다. | 실패 시 빈 배열을 동작 보존 중 throw로 바꾸지 않는다. |
| [저장 용량](../current/storage-statistics.md) | SQLite·Mapbox 집계, 부분 실패와 React 최신 결과 반영을 읽을 수 있는 책임으로 나눈다. | 당시 byte 방어·늦은 응답 차단을 모든 hook의 공통 제품 요구로 올리지 않는다. |
| Expense API | Request parse·HTTP·response parse·반환을 직접 드러낸다. | 재전파 catch 제거를 전역 fetcher·Query/UI 오류 책임 제거로 확대하지 않는다. |
| Schedule 응답 | 같은 시간 변환의 일곱 소비자를 함께 맞춘다. | Serializer·response schema·접근 query를 한 책임으로 합치지 않는다. |

저장 용량의 최초 helper 추출은 표시 조립 중복만 줄이고 내부 I/O·실패·React 연결 부담은 남겼다. 후속 정정 뒤 개선이 확대된 사례이므로, 작은 수정의 완료를 맡은 개선 결과 전체의 완료로 바꾸지 않는다.

작성 근거는 Workspace 002의 [Spec](../../work/workspaces/002-code-readability-refactoring/current/memory/spec/01-problem-goal-scope.md), [Ticket 01~05](../../work/workspaces/002-code-readability-refactoring/current/memory/tickets/index.md), [저장 용량 실행](../../work/workspaces/002-code-readability-refactoring/records/2026-09-11-04-storage-stats-refactor.md)·[최초 범위 재확인](../../work/workspaces/002-code-readability-refactoring/records/2026-09-12-01-ticket-03-initial-scope-reanalysis.md), [Schedule 실행](../../work/workspaces/002-code-readability-refactoring/records/2026-09-14-01-schedule-serialization-and-response-contract.md)이다.

비동기 수명·책임 배치와 혼합 변경의 분리 기준은 2026-09-25 [Network 품질 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-17-01-network-quality-review-and-handoff.md), [인증 책임 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-21-04-auth-responsibilities-and-regression-fixes.md), [인증 커밋 경계](../../work/workspaces/002-code-readability-refactoring/records/2026-09-22-01-auth-commit-boundary.md), [단계별 분리 검증](../../work/workspaces/002-code-readability-refactoring/records/2026-09-22-02-five-stage-commits-and-verification.md)의 채택 기준을 통합했다. 철회된 구조와 과거 검사 수치를 현재 구현의 증거로 재사용하지 않는다.
