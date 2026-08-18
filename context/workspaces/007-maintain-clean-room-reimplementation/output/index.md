# Maintain clean-room reimplementation output

마지막 갱신: `2026-08-19`

## 목표

Workspace 005의 사용자-facing Maintain 동작을 글로벌 책임 기준으로 다시 배치해 `reference-project/`가 소유하는 재사용 가능한 구현과 검증으로 만든다.

## 현재 선택된 구현

[`reference-project/`](../../../../reference-project/)의 다음 세로 흐름을 선택했다.

- `context/work/harness/maintain/operation.py`: explicit bootstrap과 guarded apply
- `context/work/harness/maintain/codex_session.py`: persisted read-only semantic thread
- `context/work/harness/maintain/host_adapter.py`: hook lifecycle, ignored runtime와 result delivery
- `.codex/hooks.json`, `.codex/hooks/maintain.py`, `.codex/maintain.json`: Reference host 연결과 explicit binding
- `context/work/harness/maintain/tests/`: core·session·host·CLI direct tests

선택 근거와 actual proof는 [`record 04`](../records/2026-08-19-04-acceptance-and-first-implementation-slice.md)와 [`record 05`](../records/2026-08-19-05-reference-implementation-and-host-evidence.md)가 소유한다. 이후 목적 재기준화와 현재 남은 범위는 [`record 06`](../records/2026-08-19-06-purpose-rebaseline-and-remaining-scope.md)이 소유한다.

실패 뒤 후속 event의 최소 안전 동작과 실제 Maintainer 연속 대화 acceptance는 [`record 07`](../records/2026-08-19-07-failure-ordering-and-semantic-acceptance.md)이 소유한다.

Reference와 outer root의 구조 차이, 단순 hook 연결을 진행하지 않은 이유는 [`record 08`](../records/2026-08-19-08-root-connection-boundary.md)이 소유한다.

독립 리뷰의 국소 결함과 실패 뒤 후속 event의 최소 정책은 선택된 구현에 반영했다. Broad evidence pipeline, 자동 thread 복구와 완전한 transaction은 1차 필수 구현에서 제외했다. Reference 산출물은 완료이며 outer root 적용은 별도 target mapping이 필요한 후속 작업이다.
