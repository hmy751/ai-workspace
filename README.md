# context-harness

사람과 AI가 프로젝트 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 지속 상태에 다시 반영할 수 있게 하는 context+harness 운영 구조를 만드는 저장소다.

현재는 source intake를 마치고 context의 현재 상태와 작업 이력을 분리한 단계다.

- context 작업대: [`context/`](./context/)
- 현재 유지되는 맥락: [`context/active/`](./context/active/)
- 작업·판단 이력: [`context/history/`](./context/history/)
- source 원본과 색인: [`context/source/`](./context/source/)
- context 유지 subagent: [`.codex/agents/context-maintainer.toml`](./.codex/agents/context-maintainer.toml)
- agent 등록: [`.codex/config.toml`](./.codex/config.toml)
- 호출 조건과 책임 경계: [`AGENTS.md`](./AGENTS.md)

agent 정의와 routing은 이 저장소 안에서만 관리한다. 전역 agent·skill·프로젝트 색인·runtime 설정에는 등록하지 않는다.
