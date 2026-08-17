# Context continuity maintenance current

마지막 갱신: `2026-08-18`

이 폴더는 다음 세션이 긴 대화나 구현 전체를 다시 읽지 않고도 Workspace 005의 현재 Maintain·Verify 구현과 남은 커서를 이어 가는 데 필요한 최신 상태를 소유한다.

## 재진입 순서

1. [`memory.md`](memory.md)에서 사용자 우선순위, 역할 경계와 구현이 계속 지켜야 할 동작 기준을 확인한다.
2. [`state.md`](state.md)에서 완료된 구현 상태, 현재 proof ceiling과 별도 승인 뒤 가능한 후속 검증을 확인한다.
3. [`../output/index.md`](../output/index.md)에서 Reference Maintain·Verify canonical과 root 연결 설정 위치를 확인한다.
4. 이번 구현의 선택 이유, recovery invariant와 proof ceiling을 대조할 때 [Reference Maintain 구현과 proof record](../records/2026-08-18-09-reference-maintain-runtime-implementation-and-proof.md)를 읽는다.
5. 이전 Observe 실패와 ownership 정정이 필요한 경우에만 [records 06–08](../records/)을 선택해 읽는다.
6. 운영 지연, C/E 우선순위, Verify 축소와 cursor 의미의 최초 근거가 필요한 경우에만 [records 01–05](../records/)를 선택해 읽는다.

Workspace 004의 구현 상세나 다른 Workspace의 current·output·records는 이 작업의 현재 링크가 명시한 경우에만 연다.
