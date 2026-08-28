# Reference Project instruction router

이 파일은 Project root에서 Codex를 시작할 때 하위 책임의 운영 지침을 발견하게 하는 최소 라우터다. Reference 전체 관계는 [`README.md`](README.md)와 [`context/README.md`](context/README.md)에서 시작한다.

## 범위별 지침

- `context/work/`의 Workspace·Harness·Recover·Maintain·Verify를 읽거나 변경하기 전에 [`context/work/AGENTS.md`](context/work/AGENTS.md)를 끝까지 읽는다. Work 운영 규칙과 Maintain agent routing은 그 파일이 소유한다.
- 이미 Context Harness가 설치된 이 Project에서 새 독립 Workspace를 만들거나 기존 작업을 후속 Workspace로 분리해 달라는 요청에는 [`.agents/skills/create-context-workspace/SKILL.md`](.agents/skills/create-context-workspace/SKILL.md)를 사용한다. 기존 Workspace 재진입·수정이나 최초 Context Harness 이식에는 사용하지 않는다.
- Project common context의 의미와 Owner는 [`context/project/README.md`](context/project/README.md)를 따른다.
- 제품 구현과 제품 테스트는 `src/`와 `tests/`가 소유한다. Work 문서나 Harness 아래에 복제하지 않는다.

명령은 별도 지시가 없으면 이 Project root에서 실행한다. 하위 `AGENTS.md`의 상세 규칙을 이 파일에 반복하지 않는다.
