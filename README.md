# context-harness

사람과 AI가 프로젝트 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 지속 상태에 다시 반영할 수 있게 하는 context+harness 운영 구조를 만드는 저장소다.

첫 실행 가능한 Project–Workspace reference는 `reference-project/`에 구현·검증을 마쳤다. 저장소 자체의 작업 context는 기존 reference 구현과 다음 실제 Project 적용이 섞이지 않도록 Workspace별로 분리했다.

- context 경계와 재진입: [`context/`](./context/)
- Workspace 목록과 active 작업: [`context/workspaces/`](./context/workspaces/)
- 완료된 reference 구현 Workspace: [`001-reference-implementation`](./context/workspaces/001-reference-implementation/)
- active context continuity Workspace: [`005-context-continuity-maintenance`](./context/workspaces/005-context-continuity-maintenance/)
- 보류된 적용 Workspace: [`002-project-application`](./context/workspaces/002-project-application/)
- 준비된 적용 Workspace: [`003-project-application`](./context/workspaces/003-project-application/)
- 공유 source 원본과 색인: [`context/source/`](./context/source/)
- 실행 가능한 기준 Project: [`reference-project/`](./reference-project/)
- 실제 Project 이식 절차: [`.agents/skills/apply-context-harness/`](./.agents/skills/apply-context-harness/)
- 재사용 가능한 Maintain 계약·runtime·agent: [`reference-project/context/work/harness/maintain/`](./reference-project/context/work/harness/maintain/)
- Workspace 005 dogfood 선택값: [`.codex/context-maintain.json`](./.codex/context-maintain.json)
- response-end hook 연결: [`.codex/hooks.json`](./.codex/hooks.json)
- Reference agent 발견 연결: [`.codex/config.toml`](./.codex/config.toml)
- 호출 조건과 책임 경계: [`AGENTS.md`](./AGENTS.md)

root는 Workspace 005를 선택하는 설정과 hook·agent 발견 경로만 소유한다. 의미 판단, 쓰기 제약, session runtime과 test의 canonical은 Reference에 있다. 이전 Observe 실험은 Workspace 005 records 06–08과 Git 이력에 남지만 active runtime으로 사용하지 않는다.

agent 정의, repo-local skill과 routing은 이 저장소 안에서만 관리한다. 전역 agent·skill·프로젝트 색인·runtime 설정에는 등록하지 않는다.
