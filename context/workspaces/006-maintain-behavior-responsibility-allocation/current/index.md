# Maintain behavior responsibility allocation current

마지막 갱신: `2026-08-18`

이 폴더는 Workspace 006이 중단됐다는 현재 상태와 이관 경계만 소유한다. 다음 세션은 006 구현을 이어 가지 않는다.

## 재진입 순서

1. [`state.md`](state.md)에서 중단 이유, 검증 상한과 다음 이관 행동을 확인한다.
2. [`../records/2026-08-18-05-clean-room-restart-decision.md`](../records/2026-08-18-05-clean-room-restart-decision.md)에서 clean-room 재시작 결정을 확인한다.
3. 006의 구현 세부가 왜 새 architecture의 입력이 아닌지 필요할 때만 [`../records/`](../records/)를 읽는다.

Workspace 005의 필요한 합의와 근거는 새 Workspace가 자기 records에 선택해 둔다. 006 current를 새 작업의 current처럼 사용하지 않는다.
