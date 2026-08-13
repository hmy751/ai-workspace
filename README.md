# context-harness

사람과 AI가 프로젝트 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 지속 상태에 다시 반영할 수 있게 하는 context+harness 운영 구조를 만드는 저장소다.

source intake와 context 운영 경계 정리를 마쳤고, `output/`에 첫 실행 가능한 Project–Workspace reference를 구현해 실제 실패·수정·성공·재진입 순환까지 검증했다. 현재는 Project common context를 `output/context/project/`, Harness와 Workspace collection을 `output/context/work/`에 묶고 Project root와 Work root를 실행 계약에서도 분리한 결과를 검토하는 단계다.

- context 작업대: [`context/`](./context/)
- 현재 상태의 진입점: [`context/current/`](./context/current/)
- 작업 중 만든 지속 기록: [`context/records/`](./context/records/)
- source 원본과 색인: [`context/source/`](./context/source/)
- 실행 가능한 첫 목표 산출물: [`output/`](./output/)
- context 유지 subagent: [`.codex/agents/context-maintainer.toml`](./.codex/agents/context-maintainer.toml)
- agent 등록: [`.codex/config.toml`](./.codex/config.toml)
- 호출 조건과 책임 경계: [`AGENTS.md`](./AGENTS.md)

agent 정의와 routing은 이 저장소 안에서만 관리한다. 전역 agent·skill·프로젝트 색인·runtime 설정에는 등록하지 않는다.
