# 날짜와 시각의 데이터 의미

저장·전송 필드가 한 시점을 나타내는지 달력 날짜만 나타내는지 판단할 때 읽는다. 이 본문은 이 주제의 현재 Project 기준을 소유한다. 기존 [Time context](../../../.claude/context/time.md)는 구현 helper와 이전 경로를 연결하는 호환 진입점으로 남는다.

## 필드의 의미를 먼저 구별한다

**한 시점과 달력 날짜를 먼저 구별한다.** 한 시점은 timezone을 포함한 ISO 8601 datetime으로 저장·전송한다. Schedule의 scheduledAt, entity의 createdAt·updatedAt·deletedAt, 동기화 기준 시각이 해당한다. Locale 표시 문자열은 저장·전송에 사용하지 않는다.

Expense date는 현재 form·request·entity·DB가 같은 계약을 쓰지 않는다. “모든 날짜는 datetime”이나 “Expense는 모든 경계에서 date-only”로 설명하면 실제 차이를 놓친다.

| 현재 충돌 | 아직 필요한 결정 |
| --- | --- |
| Root 불변식·[ISO Time rule](../../../.claude/rules/iso-time.md)은 저장·전송 시간을 timezone 포함 datetime으로 설명한다. Expense API entity는 date-only를 요구한다. | Datetime 정책에 구현을 맞출지, date-only domain 예외를 승인하고 compact rule을 고칠지 사용자와 결정한다. |

어느 한쪽을 이 문서 편집으로 폐기하거나 새로운 예외를 승인하지 않는다.

## Schedule 응답의 시간 계약

PostgreSQL Schedule row는 `Date` 값을 사용하고 API Schedule entity는 timezone offset이 있는 문자열을 요구한다. [Schedule serializer](../../../apps/server/src/serializers/schedule.ts)가 `scheduledAt`, `createdAt`, `updatedAt`, nullable `deletedAt`을 ISO 문자열로 바꾼다. 생성·전체 목록·단건·수정·Trip 하위 목록·Trip activation·sync pull의 일곱 응답 경로가 같은 serializer를 사용한다.

이 공통성은 시간 변환 책임에만 적용한다. 각 endpoint의 envelope schema, 조회·소유권·soft-delete와 오류 처리는 route가 맡는다. 자세한 변경 기준은 [API 계약과 변경 가이드](../guidance/api-contracts.md)에 있다.

## Expense `date`의 확인된 현재 차이

| 경계 | 현재 표현·검증 | 이어지는 결과 |
| --- | --- | --- |
| [API entity](../../../packages/schema/src/entities/expense.ts) | `YYYY-MM-DD` | 응답의 date-only 계약 |
| [Create request](../../../packages/schema/src/requests/expense.ts) | 비어 있지 않은 문자열로 재정의 | Entity와 같은 날짜 형식 검사를 하지 않음 |
| Update request | Entity의 date-only 검사 유지 | Datetime 입력을 거부할 수 있음 |
| [Create form](../../../apps/client/src/features/expense/create-expense/useCreateExpenseForm.ts)·[update picker](../../../apps/client/src/features/expense/update-expense/UpdateExpenseDrawer.tsx) | 선택 날짜를 UTC 자정의 ISO datetime으로 만듦 | Remote update의 request parse와 충돌 가능 |
| [Client DB](../../../apps/client/src/shared/db/schema.ts)·[Local 저장](../../../apps/client/src/entities/expense/lib/expense-local.ts) | 제약 없는 text에 받은 문자열을 저장 | Remote와 같은 형식 거절을 보장하지 않음 |
| [Server DB](../../../apps/server/src/db/schema.ts) | Timezone-aware timestamp | API entity와 다른 물리 표현 |
| [Expense serializer](../../../apps/server/src/serializers/expense.ts) | Date를 UTC ISO로 바꾼 뒤 날짜 부분 반환 | 현재 response 표현에 맞춤 |

**미정인 것은 Expense 날짜의 제품 의미다.** 사용자의 현지 달력 날짜인지, 절대 시각에서 파생한 날짜인지 장기 domain 선택이 확인되지 않았다.

- **Date-only를 선택한다면:** create/update form·request를 맞추고 server 저장·timezone 변환으로 날짜가 바뀌지 않도록 의미를 정해야 한다.
- **Datetime으로 통일한다면:** entity response·client DB·sync·표시의 영향을 함께 결정해야 한다.

현재 serializer가 응답을 맞춘다는 사실만으로 어느 쪽도 새 제품 기준으로 채택하지 않는다.

Trip startDate·endDate는 공유 schema·저장에서 ISO datetime이고 UI에서는 시작일·종료일로 사용한다. 최초 편입은 Ticket 01–05에 필요한 경계만 대조했으므로 Trip의 장기 의미도 새로 결정하지 않았다. 변경할 때는 Trip form·주요 여행 선택 계산·두 DB·API를 따로 대조한다.

## 적용과 재확인

새 필드나 변환을 만들 때에는 이름에 `date`가 있다는 이유로 표현을 고르지 말고, 그 값이 한 시점인지 달력 날짜인지 먼저 정한다. datetime은 shared helper와 offset-aware schema를 사용하고, date-only는 timezone 변환으로 날짜가 이동하지 않는지 request·DB·response를 함께 확인한다.

Schedule의 일곱 소비 경로, Expense form·request·entity·두 DB와 serializer 중 하나가 바뀌면 이 본문의 사실 범위를 다시 대조한다. 관련 근거는 Workspace 002의 [Ticket 05](../../work/workspaces/002-code-readability-refactoring/current/memory/tickets/05-schedule-response.md)와 [Schedule 실행 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-14-01-schedule-serialization-and-response-contract.md)에 있다. Mock route 검사는 실제 PostgreSQL·JWT·배포를 입증하지 않는다. 2026-10-01 편집은 해당 기록과 이 브랜치의 Expense form·request·DB·serializer 대조이며 새 제품 실행 검증은 아니다.
