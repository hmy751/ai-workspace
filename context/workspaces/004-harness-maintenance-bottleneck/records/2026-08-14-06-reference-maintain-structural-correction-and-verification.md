# Reference Maintain 구조 교정과 최종 검증

기록일: `2026-08-14`
상태: 교정 구현·독립 review 완료, 사람 acceptance와 commit 대기

## 완료 판단 철회와 진단

직전 [`record 05`](2026-08-14-05-reference-recover-verify-implementation-and-verification.md)는 Recover·Verify 개선과 Maintain workflow 설명을 구현 완료로 기록했다. 사용자는 Maintain이 문장으로만 있고 Harness 안에서 독립 책임으로 발견되지 않는다는 이유로 완료를 거절했다. Record 05는 이 교정 전 상태를 보여 주는 historical record로 그대로 보존한다.

Main은 global `ai-system_context-ownership-boundary`, `ai-system_responsibility-cohesion`, `ai-system_human-readable-structure`, `ai-system_harness-rippability`, `reasoning-allocation` 기준으로 이 문제를 다시 진단했다. 지속되는 Workspace 의미·규칙의 Owner와 tool-specific 실행 adapter를 분리하되, Maintain이라는 독립 책임의 정의와 진입점은 실제 Harness 구조에서 찾을 수 있어야 한다는 결론이었다.

## 교정된 구조

현재 [`Harness canonical`](../../../../reference-project/context/work/harness/README.md)은 책임을 기준으로 다음 경계를 드러낸다.

- [`recover/`](../../../../reference-project/context/work/harness/recover/README.md): 명시한 Workspace의 현재 맥락을 read-only로 복구한다.
- [`maintain/`](../../../../reference-project/context/work/harness/maintain/README.md): 의미 변화가 생긴 자연스러운 작업 경계에서 current·records·source provenance·output 선택을 정합화하는 책임을 정의한다.
- [`verify/`](../../../../reference-project/context/work/harness/verify/README.md): bounded verification과 durable receipt·status를 소유한다.
- [`validation/`](../../../../reference-project/context/work/harness/validation/README.md): Harness 자체 회귀를 ephemeral fixture에서 검사한다. 네 번째 작업 workflow 단계가 아니다.
- [`testing.py`](../../../../reference-project/context/work/harness/testing.py): 책임 디렉터리가 함께 쓰는 test fixture만 제공한다.

지속되는 Workspace 의미와 관리 규칙은 Work·Workspace canonical에 남는다. [`workspace-context-maintainer.toml`](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml)은 그 규칙을 실제 작업 경계에서 수행하는 교체 가능한 Reference adapter다. Maintain을 위한 Python CLI나 schema는 추가하지 않았고, outer [repo-local `context-maintainer`](../../../../.codex/agents/context-maintainer.toml)는 별도 Workspace와 권위를 유지한다.

## 독립 review와 수정

첫 독립 review는 P2 두 건과 package 설명 P3 한 건을 찾았다.

- Status가 Harness test receipt를 durable Verify 결과로 가리킬 수 있던 문제를 고쳐, [`공통 Workspace contract`](../../../../reference-project/context/work/harness/workspace_contract.py)는 nested `records/receipts/verify/verify-*.json`과 legacy direct `records/verify-*.json`만 받는다.
- Verify timeout이 같은 process group의 descendant를 남길 수 있던 문제를 고쳐, [`Verify 구현`](../../../../reference-project/context/work/harness/verify/operation.py)은 POSIX에서 일반적인 동일 process-group descendant까지 종료하고 `124`와 `timed_out`을 기록한 뒤 정리한다.
- [`Validation test package 설명`](../../../../reference-project/context/work/harness/validation/tests/__init__.py)을 현재 책임 구조에 맞췄다.

## 검증 결과

- 최신 worker full suite: 53/53 통과
- 독립 re-review: 두 P2 수정 재현, P1·P2·P3 없음, 최종 verdict `accept`
- Review acceptance는 구현 결함 판정이며 사람의 결과 acceptance나 commit 승인은 아니다.

## 증명 상한

이번 검증은 실제 Maintain agent가 의미 변화를 선택하고 current·records를 쓰는 동작이나 그 adapter의 runtime 호출을 실행하지 않았다. Detached/new-session process와 non-POSIX 환경의 descendant-wide 종료, concurrent Verify, 악의적 verification의 sandboxing도 증명하지 않았다.

## 다음 상태

교정 구현과 독립 review는 완료됐다. 사용자가 구조와 proof ceiling을 검토해 결과 acceptance와 commit 여부를 결정해야 한다.
