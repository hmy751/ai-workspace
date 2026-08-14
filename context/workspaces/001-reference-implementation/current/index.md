# Reference implementation current

마지막 갱신: `2026-08-14`

이 폴더는 reference 구현 Workspace에서 지금도 유효한 내용과 최종 상태의 입구다. 긴 작업 이력이나 원자료를 복제하지 않는다.

## 재진입 순서

1. [`memory.md`](./memory.md)에서 이 작업의 목표·기준·결정·제약·지속 효과를 확인한다.
2. [`state.md`](./state.md)에서 완료 상태·근거·검증 상한을 확인한다.
3. [`../output/index.md`](../output/index.md)에서 이 Workspace goal의 현재 산출물과 실제 canonical 위치를 확인한다.
4. 더 자세한 이유나 실행 결과가 필요할 때 `state.md`가 가리키는 `../records/` 기록을 읽는다.
5. 판단 근거를 다시 확인해야 할 때만 [`../../../source/`](../../../source/)를 연다.

## 유지 담당

이 Workspace를 다시 수정하는 작업의 자연스러운 경계에서는 repo-local [`context_maintainer`](../../../../.codex/agents/context-maintainer.toml)가 실제 변경과 current/records/source를 대조한다. 호출 시점은 [`../../../../AGENTS.md`](../../../../AGENTS.md)가 정하며, main이 agent의 diff와 현재 상태 판단을 최종 검토한다.

## 유지 규칙

- 완료 과정과 상세 결과는 records에 남기고, 지금도 유효한 효과·제약만 memory에 남긴다.
- 완료된 Workspace를 새 작업의 current처럼 갱신하지 않는다.
- 실제 reference를 다시 변경해 이 Workspace의 유효한 결론이나 검증 상한이 달라졌을 때만 current를 갱신한다.
- current가 실제 파일·source·test·사용자 정정과 어긋나면 근거를 확인한 뒤 바로잡는다.
