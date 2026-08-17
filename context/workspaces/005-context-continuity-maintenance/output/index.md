# Context continuity maintenance output

마지막 갱신: `2026-08-18`

## Workspace goal

같은 세션에서 이미 이해한 Maintainer를 재사용해 Main을 막지 않으면서, 다음 세션이 믿을 수 있는 지속 context와 검증 evidence의 책임 경계를 실행 가능한 Reference로 제공한다.

## 현재 구현 canonical

- [Reference Maintain 계약과 운영 진입점](../../../../reference-project/context/work/harness/maintain/README.md): 초기 grounding, warm continuity, response-end 활동, 판단·write·보고·복구와 교체·제거 경계
- [Reference Maintain hook 진입점](../../../../reference-project/context/work/harness/maintain/hook.py), [controller](../../../../reference-project/context/work/harness/maintain/controller.py), [runtime](../../../../reference-project/context/work/harness/maintain/runtime.py), [guarded writer](../../../../reference-project/context/work/harness/maintain/writer.py): host capture부터 semantic 판단, session·Workspace recovery와 실제 Context write까지의 reusable implementation
- [Maintainer decision schema](../../../../reference-project/context/work/harness/maintain/decision.schema.json)와 [수동 fallback agent](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml): semantic output 경계와 hook 미사용 환경의 동일 역할 진입점
- [Reference Verify 계약](../../../../reference-project/context/work/harness/verify/README.md)과 [evidence recorder](../../../../reference-project/context/work/harness/verify/operation.py): 이미 수행된 확인만 append-only로 보존하는 축소 Verify
- [Reference Harness 책임 지도](../../../../reference-project/context/work/harness/README.md): Recover·Maintain·Verify와 Harness validation의 상위 관계
- [Reference Project hook 설정](../../../../reference-project/.codex/hooks.json)과 [Workspace binding](../../../../reference-project/.codex/context-maintain.json): 다른 Project에서 적응할 수 있는 실행 연결 예시
- [Apply Context Harness skill](../../../../.agents/skills/apply-context-harness/SKILL.md): target canonical과 사용자 변경을 보존하면서 현재 Reference 책임을 이식하는 절차

## Workspace 005 연결 설정

- [Root Workspace binding](../../../../.codex/context-maintain.json): `005-context-continuity-maintenance`와 root ignored runtime을 선택하는 값
- [Root hooks](../../../../.codex/hooks.json): root에서 Reference `hook.py`를 호출하는 thin 연결
- [Root agent discovery](../../../../.codex/config.toml)와 [agent config](../../../../.codex/workspace-context-maintainer.toml): hook 미사용 시 수동 fallback을 찾는 연결
- [Root 운영 routing](../../../../AGENTS.md): 정상 hook과 fallback의 중복을 피하고 Workspace 005만 갱신하는 local contract

Root 연결 설정은 Workspace 선택·path·hook discovery만 소유한다. Maintain의 prompt, queue·checkpoint, semantic runner, writer와 test는 Reference에만 있으며 이전 `.codex/context_maintainer/` Observe runtime은 active output이 아니다.

## 판단과 proof 기록

- [운영 지연과 역할 진단](../records/2026-08-17-01-harness-operation-latency-and-role-diagnosis.md)
- [Context continuity와 background maintenance framing](../records/2026-08-17-02-context-continuity-and-background-maintenance-framing.md)
- [응답 종료 점검과 갱신 계약](../records/2026-08-17-03-response-end-maintenance-contract-and-verify-reopening.md)
- [Verify 증거 기록 경계](../records/2026-08-17-04-verify-evidence-recording-boundary.md)
- [Maintainer retrieval·runtime·cursor 계약](../records/2026-08-17-05-maintainer-retrieval-runtime-and-cursor-contract.md)
- [첫 Observe runtime과 live smoke](../records/2026-08-17-06-response-end-observe-runtime-and-live-smoke.md)
- [Reference 소유권 정정](../records/2026-08-17-07-reference-ownership-correction-and-handoff.md)
- [세션형 Maintainer 동작과 Reference 구현 계획](../records/2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md)
- [Reference Maintain 구현과 proof](../records/2026-08-18-09-reference-maintain-runtime-implementation-and-proof.md)
- [지속 기준](../current/memory.md)과 [현재 커서](../current/state.md)

## 현재 상태

Reference-first 구현과 root 연결 설정 전환, cross-session recovery wake와 로컬 통합 재검증까지 완료해 현재 변경 묶음으로 보존했고 이전 Observe 실험은 historical evidence로만 남겼다. Maintain `165/165`, Reference 전체 `223/223`, apply skill helper `7/7`과 정적 연결 검사는 통과했다. 실제 nested `codex exec`, fresh Codex host의 hook trust·background 동작·UI notice·semantic write 품질은 live acceptance 전까지 현재 output의 증명 범위가 아니다. 전달 evidence가 없는 외부 branch·worktree 전환의 자동 감지도 이번 output의 증명 범위가 아니다.
