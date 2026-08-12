# Current context

마지막 갱신: `2026-08-13`

이 폴더는 **지금 유효한 내용만 유지하는 현재 상태의 입구**다. 긴 작업 이력이나 원자료를 복제하지 않고, 다음 작업을 시작하는 데 필요한 맥락과 접근점만 둔다.

## 재진입 순서

1. [`project.md`](./project.md)에서 장기간 유지되는 목표·기준·제약을 확인한다.
2. [`work.md`](./work.md)에서 현재 문제·상태·불확실성·다음 행동을 확인한다.
3. 더 자세한 이유나 실행 결과가 필요할 때 `work.md`가 가리키는 `../records/` 기록을 읽는다.
4. 판단 근거를 다시 확인해야 할 때만 [`../source/`](../source/)를 연다.

## 유지 담당

자연스러운 작업 경계에서는 repo-local [`context_maintainer`](../../.codex/agents/context-maintainer.toml)가 실제 변경과 current/records/source를 대조한다. 호출 시점은 [`../../AGENTS.md`](../../AGENTS.md)가 정하며, main이 agent의 diff와 현재 상태 판단을 최종 검토한다.

## 유지 규칙

- 다음 세션이 모르면 현재를 잘못 이해하거나 잘못 행동할 내용만 둔다.
- 확인된 사실뿐 아니라 미확인 상태와 사용자 판단 대기도 필요하면 상태를 드러내고 둔다.
- 완료 과정은 records에 남기고, 완료 뒤에도 유지되는 효과·제약만 project에 남긴다.
- 지금 이어갈 후속 작업만 work에 남기며, 더 이상 행동에 영향을 주지 않는 내용은 current에서 내린다.
- 같은 현재 내용을 project와 work에 중복하지 않고, 상세 분석이나 검증 결과는 records를 가리킨다.
- current가 실제 파일·source·test·사용자 정정과 어긋나면 current가 낡은 것이므로 근거를 확인한 뒤 갱신한다.
