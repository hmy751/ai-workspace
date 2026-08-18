# context-harness

사람과 AI가 프로젝트 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 지속 상태에 다시 반영할 수 있게 하는 context+harness 운영 구조를 만드는 저장소다.

첫 실행 가능한 Project–Workspace reference는 `reference-project/`에 구현·검증을 마쳤다. 저장소 자체의 작업 context는 기존 reference 구현과 다음 실제 Project 적용이 섞이지 않도록 Workspace별로 분리했다.

- context 경계와 재진입: [`context/`](./context/)
- Workspace 목록과 active 작업: [`context/workspaces/`](./context/workspaces/)
- 완료된 reference 구현 Workspace: [`001-reference-implementation`](./context/workspaces/001-reference-implementation/)
- active Maintain clean-room Workspace: [`007-maintain-clean-room-reimplementation`](./context/workspaces/007-maintain-clean-room-reimplementation/)
- 보류된 적용 Workspace: [`002-project-application`](./context/workspaces/002-project-application/)
- 준비된 적용 Workspace: [`003-project-application`](./context/workspaces/003-project-application/)
- 공유 source 원본과 색인: [`context/source/`](./context/source/)
- 실행 가능한 기준 Project: [`reference-project/`](./reference-project/)
- 실제 Project 이식 절차: [`.agents/skills/apply-context-harness/`](./.agents/skills/apply-context-harness/)
- clean-room 출발점인 Maintain 경계 문서: [`reference-project/context/work/harness/maintain/`](./reference-project/context/work/harness/maintain/)
- 비활성 자동 hook 설정: [`.codex/hooks.json`](./.codex/hooks.json)
- 비활성 agent 등록 설정: [`.codex/config.toml`](./.codex/config.toml)
- 호출 조건과 책임 경계: [`AGENTS.md`](./AGENTS.md)

Workspace 005의 최종 Maintain 구현은 새 clean-room 재구현을 위해 구현 직전 기준으로 복원했다. 자동 hook과 agent 연결은 새 행동 계약과 실제 host 검증이 끝날 때까지 비활성으로 둔다. Workspace 005와 006은 근거와 실패 이력으로 보존하며 active runtime으로 사용하지 않는다.

agent 정의, repo-local skill과 routing은 이 저장소 안에서만 관리한다. 전역 agent·skill·프로젝트 색인·runtime 설정에는 등록하지 않는다.
