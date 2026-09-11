# 05 — 서버 일정 응답의 날짜 변환

## 맡은 결과와 범위

`apps/server/src/routes/schedules.ts`의 생성·목록·단건·수정 응답에 반복되는 `scheduledAt`·`createdAt`·`updatedAt`·`deletedAt` 변환을 한 의미로 관리한다. CRUD 쓰기 값·소유권·조회 조건·삭제 응답·activation/sync endpoint 통합은 제외한다.

## 실행 맥락과 접근

[보존 계약](../spec/03-concepts-and-contracts.md)과 [품질 기준](../spec/04-quality-and-completion.md)을 적용한다. Main의 [조사 초안](../../../../../../../eval-inputs/noline-002-additional-research-and-ticket-drafts-2026-09-11.md)은 조사 당시 파일의 50·91·147·246행 주변에서 동일한 네 날짜 변환을 확인했다고 보고한다.

DB row 타입에서 응답 값으로의 변환을 좁게 다루며 새 `any`나 단언으로 넘기지 않는다. 기존 entity/envelope 검증과 오류 처리 분기는 서로 다르므로 통째로 합치거나 제거하지 않는다. 좌표 0 변환과 `updateData: any`는 별도 영향 범위다. client Ticket과 기술적 선행 관계는 없다.

## 완료 조건과 확인 방법

변경 전 실제 route handler에 고정 DB 반환 fixture를 공급하여 각 endpoint의 응답 JSON·status·날짜 문자열과 `deletedAt`의 null/값을 확인한다. 수정 후 같은 검사로 비교하며 오류 경로의 기존 응답·전파도 보존한다.

새 순수 변환 helper만 검사한 것을 변경 전 기준 검사로 제시하지 않는다. handler 검사에서 DB를 대체했다면 실제 인증·ownership·영속 저장을 검증했다고 하지 않는다. 해당 부분의 diff·사용처 영향 확인과 실행 증거를 구별한다.

같은 날짜 변환을 수정할 위치가 줄고 호출부에서 DB row를 응답으로 변환하는 역할을 이해할 수 있어야 한다. server 검사와 응답 검사를 범위에 맞게 선택하고 동작 보존과 개선 효과를 각각 남긴다.

## 현재 상태와 실제 결과

실행 전 초안이다. Main은 현재 코드에 반복 변환이 있음을 확인했다고 보고했다. 제품 수정·server 검사·응답 검사는 미실행이며 위 검증은 계획이다.
