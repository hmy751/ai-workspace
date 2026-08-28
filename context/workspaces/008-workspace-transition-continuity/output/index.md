# Workspace transition continuity output

마지막 갱신: `2026-08-28`

## Workspace goal

후속 Workspace가 새 goal에 필요한 의미를 직접 소유하고 필요한 상세 근거만 단방향 참조하도록 하면서, bounded Recover와 독립 Workspace·Project context의 기존 경계를 보존하는 Reference 계약을 찾는 진입점이다.

## 현재 선택된 산출물

- [`reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md`](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md): 생성·전환의 시작 조건, 책임 배치, 의미 선별, bounded 재진입과 활성화 경계를 함께 소유하는 primary canonical
- [`reference-project/.agents/skills/create-context-workspace/SKILL.md`](../../../../reference-project/.agents/skills/create-context-workspace/SKILL.md): canonical을 읽고 새 Workspace를 구성·검토하는 교체 가능한 실행 adapter

## 연결된 운영 표면

- [`reference-project/context/work/workspaces/README.md`](../../../../reference-project/context/work/workspaces/README.md): Workspace collection과 내부 Owner의 상위 경계
- [`reference-project/AGENTS.md`](../../../../reference-project/AGENTS.md)와 [`Work AGENTS`](../../../../reference-project/context/work/AGENTS.md): 설치된 Project의 생성 요청을 skill과 canonical로 routing
- [`reference-project/context/work/harness/recover/README.md`](../../../../reference-project/context/work/harness/recover/README.md)와 [`Maintain README`](../../../../reference-project/context/work/harness/maintain/README.md): 생성·동기화 비소유와 실행 경계
- [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/SKILL.md): 새 운영 skill을 target에 설치·적응·제외하는 이식 책임
- [`reference-project/README.md`](../../../../reference-project/README.md): 사람용 진입점, 구조 지도와 proof ceiling

Skill 기반 실행 adapter와 한 격리 001→002 재진입은 검증했지만 자동 skill 선택, deterministic generator, 모든 goal의 자동 의미 선별·충분성 판정, actual target discovery·host 활성화, 실제 다른 Project 적용 효과나 사람 acceptance를 증명하지 않는다. 검증 상태와 남은 판단은 [`current/state.md`](../current/state.md), 상세 근거는 [`records/2026-08-28-03-canonical-cohesion-and-workspace-skill.md`](../records/2026-08-28-03-canonical-cohesion-and-workspace-skill.md)가 소유한다.
