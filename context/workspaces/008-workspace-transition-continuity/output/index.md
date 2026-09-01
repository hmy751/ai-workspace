# Workspace transition continuity output

마지막 갱신: `2026-09-01`

## Workspace goal

후속 Workspace가 새 goal에 필요한 의미를 직접 소유하고 필요한 상세 근거만 단방향 참조하도록 하면서, bounded Recover와 독립 Workspace·Project context의 기존 경계를 보존하는 Reference 계약을 찾는 진입점이다.

## 현재 선택된 산출물

- [`reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md`](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md): 생성·전환의 시작 조건, 의미 선별과 successor 선택, bounded 재진입과 같은 session 지속·격리 판단을 소유하는 Workspace canonical
- [`reference-project/context/work/harness/maintain/README.md`](../../../../reference-project/context/work/harness/maintain/README.md): Maintain 전체 정체성·범위와 semantic 판단·guarded apply·session lifecycle의 내부 관계를 소유하는 canonical
- [`reference-project/context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md`](../../../../reference-project/context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md): Maintain 내부 explicit admission, binding generation, hook·worker·notice, 민감 runtime과 actual-host 증명 상한을 소유하는 authoritative subcanonical
- [`reference-project/.agents/skills/create-context-workspace/SKILL.md`](../../../../reference-project/.agents/skills/create-context-workspace/SKILL.md): canonical을 읽고 새 Workspace를 구성·검토하는 교체 가능한 실행 adapter
- [`reference-project/context/work/harness/maintain/host_adapter.py`](../../../../reference-project/context/work/harness/maintain/host_adapter.py): default-unbound, session별 activation과 generation 전환, event snapshot·legacy compatibility를 집행하는 host adapter
- [`reference-project/context/work/harness/maintain/tests/test_host_adapter.py`](../../../../reference-project/context/work/harness/maintain/tests/test_host_adapter.py): unbound·동시 session·A→B→A·rollback·late worker·legacy migration 회귀

## 연결된 운영 표면

- [`reference-project/context/work/workspaces/README.md`](../../../../reference-project/context/work/workspaces/README.md): Workspace collection과 내부 Owner의 상위 경계
- [`reference-project/AGENTS.md`](../../../../reference-project/AGENTS.md)와 [`Work AGENTS`](../../../../reference-project/context/work/AGENTS.md): 설치된 Project의 생성 요청을 skill과 canonical로 routing
- [`reference-project/context/work/harness/recover/README.md`](../../../../reference-project/context/work/harness/recover/README.md): 생성·동기화 비소유와 bounded grounding 경계
- [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/SKILL.md): 새 운영 skill을 target에 설치·적응·제외하는 이식 책임
- [`reference-project/README.md`](../../../../reference-project/README.md): 사람용 진입점, 구조 지도와 proof ceiling

Skill 기반 생성과 격리 001→002 재진입, session binding 상태 전이와 target의 직접 hook payload no-op은 검증했다. 자동 skill 선택, deterministic generator, 모든 goal의 자동 의미 선별·충분성 판정, 실제 Codex scheduler·UI에서의 multi-task binding·same-session 전환과 사람 acceptance는 증명하지 않는다. 검증 상태와 남은 판단은 [`current/state.md`](../current/state.md), 기존 skill 검증은 [`record 03`](../records/2026-08-28-03-canonical-cohesion-and-workspace-skill.md), 전환 규칙 보정은 [`record 04`](../records/2026-08-31-04-activation-rule-recalibration.md), 구현·적용은 [`record 05`](../records/2026-09-01-05-session-scoped-binding-and-rebind.md), lifecycle Owner 재정렬은 [`record 06`](../records/2026-09-01-06-maintain-session-lifecycle-canonical.md)가 소유한다.
