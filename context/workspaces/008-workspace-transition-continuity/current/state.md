# Workspace transition continuity state

마지막 갱신: `2026-08-31`

## 현재 상태

- 이전 단계의 생성·전환 원칙을 `reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md` 하나로 이동해 시작 조건, 책임 배치, workflow, 단방향 참조, bounded 재진입과 활성화 경계를 함께 찾게 했다.
- Workspace collection README는 상위 경계와 내부 Owner, Workspace 독립·비동기화 관계와 새 canonical 진입만 남겼다.
- Reference 안에 repo-local `create-context-workspace` skill과 implicit invocation metadata를 만들고 root·Work AGENTS에서 생성 요청을 routing했다.
- `apply-context-harness`에는 target의 기존 skill·root routing을 보호하며 운영 skill을 설치·적응·제외하고 discovery proof를 분리하는 책임을 추가했다.
- Recover·Maintain은 자기 비소유 경계와 새 canonical 링크만 유지하고, Reference root proof ceiling은 skill adapter와 미구현 deterministic 보장을 구분한다.
- 초기 008 구현에서는 Harness machine code, schema, hook, sample Workspace와 `memory-harness-research`를 변경하지 않았다. 2026-08-31 재보정에서는 두 저장소의 규칙 문서와 skill만 변경했고 machine/runtime과 작업별 current는 수정하지 않았다.
- 수정·추가 Markdown local link, JSON·YAML metadata와 `git diff --check`를 확인했다. Python skill validator는 두 Python 환경 모두 `PyYAML`이 없어 시작하지 못했고 같은 검사 조건의 Ruby fallback과 별도 YAML parse를 통과했다.
- `apply-context-harness` helper test `7`개와 Reference 전체 unit test `97`개가 최종 실행에서 모두 통과했다.
- 격리한 001→002 forward test에서 predecessor, active index와 binding이 해시상 불변인 채 successor를 생성했고, explicit Recover packet만 받은 별도 주체가 핵심 의미와 원문 접근점·비상속·증명 한계를 복원했다.
- Canonical·Owner·proof ceiling 독립 검토는 새 P1·P2·P3 없이 통과했다. Trigger 검토에서 찾은 default prompt의 독립 Workspace 편향과 설치 전제 누락은 metadata 문구에 반영했다.
- `memory-harness-research`의 실제 004 전환 대화와 008 원대화·Git 이력을 다시 대조해, 새 Main session 강제가 사용자 원칙이 아니라 현재 adapter 제약을 문서 범위에서 닫은 선택이었음을 확인했다. 대상 Project에 먼저 조건부 전환 규칙을 반영한 뒤 Reference canonical·routing·skill·Maintain 비소유와 proof ceiling을 같은 의미로 갱신했다. Machine code·schema·hook·runtime은 변경하지 않았다.
- 대상과 Reference의 변경 Markdown 링크, diff 형식과 skill frontmatter·placeholder 대체 검사가 통과했다. 제공된 Python skill validator는 환경에 `PyYAML`이 없어 시작하지 못했다. Reference 전체 `97`개 테스트는 기존 descendant-timeout timing test가 첫 실행에서 한 번 실패했지만 같은 test 단독 실행과 다음 전체 실행에서 통과했다.

초기 skill 결과는 [`record 03`](../records/2026-08-28-03-canonical-cohesion-and-workspace-skill.md), 현재 전환 규칙 보정은 [`record 04`](../records/2026-08-31-04-activation-rule-recalibration.md)에 남겼다.

## 남은 외부 확인

- 새 target-root session에서 skill discovery와 implicit invocation을 확인한다. 현재 session의 registry 갱신은 증명하지 않는다.
- 실제 활성화에서는 현재 binding과 미처리 Maintain 상태의 successor 영향을 확인하고, same-session 재결합을 선택하면 host가 새 grounding을 실제로 만들었는지 별도 검증한다. 현재 Reference adapter의 config-only 변경은 이를 증명하지 않는다.
- 모든 goal에서 의미 누락이 없다는 보장과 사람 acceptance는 자동화하지 않는다.

## 다음 행동

Repository 변경과 로컬 검증은 끝났다. 사용자가 diff를 검토해 수락하거나 별도 commit을 요청할 때까지 현재 working tree에 유지한다.
