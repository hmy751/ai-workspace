# 05 — 서버 일정 응답의 날짜 변환

## 맡은 결과와 범위

`apps/server/src/routes/schedules.ts`의 생성·목록·단건·수정 응답에서 반복되는 `scheduledAt`·`createdAt`·`updatedAt`·`deletedAt` 변환을 한 의미로 관리한다. CRUD 쓰기 값·소유권·조회 조건·삭제 응답·activation/sync endpoint 통합은 제외한다.

## 실행 맥락과 접근

[보존 계약](../spec/03-concepts-and-contracts.md)과 [품질 기준](../spec/04-quality-and-completion.md)을 적용한다. Main은 네 날짜 변환이 조사 HEAD의 50·91·147·246행 주변에 반복됨을 보고했다. DB row 타입에서 응답 값으로의 변환을 좁게 다루며 새 `any`나 단언으로 넘기지 않는다.

기존 entity/envelope 검증과 오류 처리 분기가 다르므로 검증을 통째로 합치거나 제거하지 않는다. 좌표 0 변환과 `updateData:any`는 별도 영향 범위다. [추가 조사 기록](../../../records/2026-09-11-01-additional-research.md)에 출처와 한계가 있다.

## 완료 조건과 확인 방법

변경 전 실제 route handler에 고정 DB 반환 fixture를 공급해 각 endpoint의 응답 JSON·status·날짜 문자열·`deletedAt` null/값을 확인하고 수정 후 비교한다. 오류 경로의 기존 응답·전파도 유지해야 한다.

새 pure helper만 검사한 것을 변경 전 기준 검사로 제시하지 않는다. DB를 대체한 handler 검사는 실제 인증·ownership·영속 저장 보존을 입증하지 않으며 해당 부분의 diff·사용처 영향 확인과 구분한다. 변경에 맞는 server 검사도 선택한다.

개선 효과는 동일 날짜 변환의 수정 위치가 줄고 호출부에서 DB row를 응답으로 바꾸는 역할이 읽히는지 전후 코드로 판단한다. sync의 단언이나 mutation 타입 전반의 해결을 이 Ticket 결과로 확대하지 않는다.

## 현재 상태와 실제 결과

Main이 제안한 실행 전 초안이다. 반복 변환의 소스 확인 보고가 있으며 제품 수정·server 검사·응답 검사는 미실행이다. 위 내용은 확인 계획이다. client Ticket과 기술적 선행 관계는 없다.
