# Reference Project instruction router

이 파일은 Project root에서 Codex를 시작할 때 하위 책임의 운영 지침을 발견하게 하는 최소 라우터다. Reference 전체 관계는 [`README.md`](README.md)와 [`context/README.md`](context/README.md)에서 시작한다.

## 범위별 지침

- `context/work/`의 Workspace·Harness·Recover·Maintain·Verify를 읽거나 변경하기 전에 [`context/work/AGENTS.md`](context/work/AGENTS.md)를 끝까지 읽는다. Work 운영 규칙과 Maintain agent routing은 그 파일이 소유한다.
- 이미 Context Harness가 설치된 이 Project에서 새 독립 Workspace를 만들거나 기존 작업을 후속 Workspace로 분리해 달라는 요청에는 [`.agents/skills/create-context-workspace/SKILL.md`](.agents/skills/create-context-workspace/SKILL.md)를 사용한다. 기존 Workspace 재진입·수정이나 최초 Context Harness 이식에는 사용하지 않는다.
- Maintain은 Project 안의 모든 대화에 자동 가입시키지 않는다. 단순한 session 연결·조회·해제는 [`Maintain session binding·lifecycle canonical`](context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md), Workspace 전환 여부와 predecessor·successor 의미는 [`생성·전환 canonical`](context/work/workspaces/CREATE-AND-TRANSITION.md)에서 시작한다. 사용자가 현재 작업에 Workspace 연결이나 전환을 명시한 경우에만 Main이 현재 `CODEX_SESSION_ID`를 대상으로 `python3 .codex/hooks/maintain.py activate <workspace_id>`를 실행한다. Main-only는 현재 CLI가 caller identity로 강제하는 권한 보장이 아니므로 subagent에게 control command를 위임하지 않는다. Active index, Project 기본값이나 대화 주제로 binding을 추론하지 않는다.
- 이미 만든 Workspace로 현재 작업을 전환해 달라는 요청에는 생성 skill을 다시 실행하지 않는다. 새 Main session을 보편적으로 강제하지 않으며, 같은 session에서는 생성·전환 canonical의 판단과 Maintain session lifecycle 계약을 함께 적용해 현재 turn을 predecessor binding으로 마감하고 activation이 성공한 뒤 다음 turn부터 successor를 사용한다. 설정 파일 변경만으로 actual activation이나 새 grounding을 완료했다고 주장하지 않는다.
- Project common context의 의미와 Owner는 [`context/project/README.md`](context/project/README.md)를 따른다.
- 제품 구현과 제품 테스트는 `src/`와 `tests/`가 소유한다. Work 문서나 Harness 아래에 복제하지 않는다.

명령은 별도 지시가 없으면 이 Project root에서 실행한다. 하위 `AGENTS.md`의 상세 규칙을 이 파일에 반복하지 않는다.
