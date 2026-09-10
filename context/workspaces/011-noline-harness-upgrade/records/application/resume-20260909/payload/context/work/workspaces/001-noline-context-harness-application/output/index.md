# Goal output

이 Workspace의 선택된 결과는 Noline root에 설치한 Context Harness와 이를 연결한 기존 Noline harness 문서다. 실제 산출물은 Workspace 안에 복제하지 않는다.

- [`context/project/`](../../../../../context/project/): Noline의 common/current/guidance와 Decision
- [`context/work/`](../../../../../context/work/): Workspace collection과 Recover·Maintain·Verify·validation Harness
- [`.claude/harness/README.md`](../../../../../.claude/harness/README.md): 기존 Noline AI harness와 새 운영 층의 관계
- [`.claude/skills/create-context-workspace/SKILL.md`](../../../../../.claude/skills/create-context-workspace/SKILL.md): 설치 이후 새 Workspace를 구성하는 Claude source skill
- [`.agents/skills/create-context-workspace`](../../../../../.agents/skills/create-context-workspace): Codex skill bridge symlink
- [`.codex/maintain.json`](../../../../../.codex/maintain.json): Codex·Claude Code가 함께 읽는 default-unbound explicit admission 설정
- [`.codex/hooks.json`](../../../../../.codex/hooks.json), [`.claude/settings.json`](../../../../../.claude/settings.json): 각 host lifecycle entrypoint
- [`.codex/hooks/maintain.py`](../../../../../.codex/hooks/maintain.py), [`.claude/hooks/maintain.py`](../../../../../.claude/hooks/maintain.py): host payload adapter wrapper

이 지도는 설치 산출물을 찾게 할 뿐, 실제 Codex·Claude Code host activation, 제품 acceptance, commit 또는 Workspace 완료를 뜻하지 않는다.

- [운영 skill 색인](../../../../../.claude/skills/README.md): 여섯 Reference skill과 기존 dispatcher의 원본·호출 조건·bridge
- [Spec·Ticket 계약](../../SPEC-AND-TICKETS.md): Work 정의·실행·유지 책임의 canonical

현재 설치 결과와 검증 범위는 [적용 기록](../records/2026-09-09-01-reference-upgrade.md)이 연결한다.
