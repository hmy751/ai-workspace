# Active context

마지막 갱신: `2026-08-12`

이 폴더는 **지금 유효한 내용만 유지하는 현재 상태의 입구**다. 긴 작업 이력이나 원자료를 복제하지 않고, 다음 작업을 시작하는 데 필요한 맥락과 접근점만 둔다.

## 재진입 순서

1. [`project.md`](./project.md)에서 장기간 유지되는 목표·기준·제약을 확인한다.
2. [`work.md`](./work.md)에서 현재 문제·상태·불확실성·다음 행동을 확인한다.
3. 더 자세한 이유가 필요할 때 `work.md`가 가리키는 `../history/` 기록을 읽는다.
4. 판단 근거를 다시 확인해야 할 때만 [`../source/`](../source/)를 연다.

## 유지 담당

의미 있는 작업 경계에서는 repo-local [`context_maintainer`](../../.codex/agents/context-maintainer.toml)가 실제 변경과 active/history/source를 대조한다. 호출 시점은 [`../../AGENTS.md`](../../AGENTS.md)가 정하며, main이 agent의 diff와 승격 판단을 최종 검토한다.

## 유지 규칙

- history에서 현재도 유효하다고 확인된 내용만 반영한다.
- 완료되거나 대체된 상태는 active에 누적하지 않고 history에서 찾게 한다.
- 같은 현재 판단을 여러 active 문서에 중복해서 쓰지 않는다.
- active와 history가 충돌하면 active가 현재 상태를 소유한다. 다만 source나 실제 코드·test가 active와 어긋나면 active가 낡은 것이므로 확인 후 바로 갱신한다.
