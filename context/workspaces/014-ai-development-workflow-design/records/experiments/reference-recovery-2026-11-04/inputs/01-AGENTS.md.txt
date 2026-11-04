# Reference Project instruction router

이 파일은 Project root에서 Codex나 Claude Code를 시작할 때 하위 책임의 운영 지침을 발견하게 하는 최소 라우터다. `CLAUDE.md`는 이 파일의 symlink로, 두 tool이 같은 내용을 읽는다. Reference 전체 관계는 [`README.md`](README.md)와 [`context/README.md`](context/README.md)에서 시작한다.

## 범위별 지침

- 작업 기록 요청이나 작업·논의 정리에는 [record-work](.agents/skills/record-work/SKILL.md)를 사용한다. 같은 대화의 기록 담당자를 재사용하며 원문 판단과 직접 Work 갱신을 맡긴다.
- 기존 Workspace 전환은 [생성·전환 계약](context/work/workspaces/CREATE-AND-TRANSITION.md)을 따른다. 기록 담당자의 입력·미반영 범위와 기본 Workspace 선택을 구별하며 자동 session activation은 사용하지 않는다.

- 기능 구현·버그 수정·리팩터링·개발 결과 검토·개발 작업 재개에는 [development](.agents/skills/development/SKILL.md)를 사용한다. 이번 요청의 범위에서 수행하며 제품 기준·작업의 기록·전환은 각 Owner의 기존 계약을 따른다.
- 사용자가 대화를 돌아보고 체계의 개선을 찾자고 요청하면 [improvement-loop](.agents/skills/improvement-loop/SKILL.md)를 사용한다. 작업 종료만으로 자동 실행하지 않는다.

- `context/work/`의 Workspace·재개 안내·기록 기준을 읽거나 변경하기 전에 [`context/work/AGENTS.md`](context/work/AGENTS.md)를 끝까지 읽는다. Work 운영 규칙과 기록 담당 연결은 그 파일이 소유한다.
- 작업 논의·재판단·작업물 설명·앞선 설명 복구에는 [Project skill 색인](.agents/skills/README.md)에서 관련 스킬을 찾고 그 호출 조건을 따른다. Spec·Ticket의 의미와 Main·기록 담당자의 반영 관계는 [Workspace 운영 기준](context/work/workspaces/spec-and-tickets/README.md)이 소유한다. 스킬 설치·호출을 기록 수행이나 실제 문서 반영으로 간주하지 않는다.
- 이 Project에서 새 독립 Workspace를 만들거나 기존 작업을 후속 Workspace로 분리해 달라는 요청에는 [`.agents/skills/create-context-workspace/SKILL.md`](.agents/skills/create-context-workspace/SKILL.md)를 사용한다. 기존 Workspace 재진입·수정이나 최초 context 체계 이식에는 사용하지 않는다.
- 필요한 맥락의 선택·대조·재사용은 [`context/USAGE.md`](context/USAGE.md)를 따른다. 개인 판단 기준은 [`Personal`](context/personal/README.md), 제품 의미·현재 구조·계약은 [`Project`](context/project/README.md)에서 질문별로 고른다. 이미 확보한 맥락으로 충분한 작업에 전체 재독을 요구하지 않는다.
- 작업 중 지속할 변화가 명확해지거나 Personal·Project의 갱신·누락 복원·승인된 이동을 요청받으면 [`context-update`](.agents/skills/context-update/SKILL.md)를 사용한다. Personal의 채택·편집 권한은 [Personal 안내](context/personal/README.md), Project의 권한·영향·완료는 [관리 계약](context/project/MAINTENANCE.md), 내용 구성은 [Project 작성 기준](context/project/REFERENCE/composition.md)이 소유한다. Work 기록은 Main·기록 담당자의 갱신 계약으로 연결한다.
- Personal·Project의 본문이나 구성을 바꿀 때는 [CONTENT-POLICY](context/CONTENT-POLICY.md)를 읽고, 본문을 작성·수정할 때는 [WRITING-FORMAT](context/WRITING-FORMAT.md)의 적용 범위와 형식 기준을 확인한다. 체계 지침의 범위·진입·분할을 바꿀 때는 [SYSTEM-GUIDANCE](context/SYSTEM-GUIDANCE.md)를 읽는다. 스킬을 만들거나 의미·구성을 바꿀 때는 [스킬 관리 정책](.agents/skills/SKILLS-CONTENT-POLICY.md)을 읽는다. Work의 기존 관리 계약에 이 정책을 자동 확장하지 않는다.
- 제품 구현과 제품 테스트는 `src/`와 `tests/`가 소유한다. Work 문서 아래에 복제하지 않는다.

명령은 별도 지시가 없으면 이 Project root에서 실행한다. 하위 `AGENTS.md`의 상세 규칙을 이 파일에 반복하지 않는다.
