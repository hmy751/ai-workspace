# Maintain behavior responsibility allocation output

마지막 갱신: `2026-08-18`

## Workspace goal

Reference Maintain의 사용자 기능을 기본적으로 유지하면서, 내부 동작의 판단·보장·권한·실행 책임과 이를 표현·집행·검증하는 코드·지침·prompt·문서의 배치를 근거 있게 개선한다.

## 판단 기준

- [Global AI 동작의 판단·보장·권한 배치 reference](/Users/hammyeong-yeon/.claude/references/ai-system_behavior-responsibility-allocation.md)

## 개선 대상 baseline

- [Reference Maintain 책임 계약](../../../../reference-project/context/work/harness/maintain/README.md)
- [Semantic prompts](../../../../reference-project/context/work/harness/maintain/prompts.py)과 [warm Codex runner](../../../../reference-project/context/work/harness/maintain/runner.py)
- [Maintain controller](../../../../reference-project/context/work/harness/maintain/controller.py), [runtime](../../../../reference-project/context/work/harness/maintain/runtime.py), [decision intent](../../../../reference-project/context/work/harness/maintain/intent.py), [guarded writer](../../../../reference-project/context/work/harness/maintain/writer.py)
- [Decision schema](../../../../reference-project/context/work/harness/maintain/decision.schema.json)과 [Maintain tests](../../../../reference-project/context/work/harness/maintain/tests/)
- [Workspace 005의 완료 구현·proof record](../../005-context-continuity-maintenance/records/2026-08-18-09-reference-maintain-runtime-implementation-and-proof.md)

## 현재 선택된 개선 결과

아직 없다. 구체적인 책임 배치 문제와 개선안을 합의한 뒤 실제 canonical 변경과 선택된 분석·검증 기록을 이 index에서 연결한다.

## Root 연결

- [현재 Workspace binding](../../../../.codex/context-maintain.json): Workspace 006을 Reference Maintain runtime에 연결한다.
- [Root hooks](../../../../.codex/hooks.json): host event와 Reference Maintain의 thin connection이다.

Root 연결은 실행 대상을 선택할 뿐 이 Workspace의 개선 결론이나 Maintain 의미 계약을 소유하지 않는다.
