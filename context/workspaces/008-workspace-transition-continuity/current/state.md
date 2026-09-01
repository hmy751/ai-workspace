# Workspace transition continuity state

마지막 갱신: `2026-09-01`

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
- Project-wide `.codex/maintain.json`이 같은 저장소의 모든 새 Codex session을 Workspace 004에 자동 binding한 사건을 확인했다. 실제 hook `session_id` 격리는 존재했지만 session별 Workspace admission과 safe rebind 경로가 없었다.
- Reference adapter를 schema v2 generation history로 바꾸고 새 session default-unbound, `status|activate|deactivate`, prompt/event binding snapshot, A→B→A, grounding rollback, late predecessor worker 격리와 v1 lazy compatibility를 구현했다.
- 독립 diff review에서 최초 unbound turn 안에서 activation하면 그 turn의 Stop이 successor로 들어갈 수 있는 경계를 찾았다. V2 response-end는 matching prompt snapshot이 없으면 no-op으로 고쳐 다음 prompt부터만 activation되게 했고 회귀 테스트를 추가했다.
- Reference focused host adapter `40`개와 전체 `115`개 테스트가 최종 실행에서 통과했다. Project 밖 cwd에서 wrapper `status`를 실행해 unbound zero-write도 확인했다.
- `memory-harness-research`에는 v2 호환 adapter를 config보다 먼저 적용했고 최종 focused `40`개가 통과했다. 사고 session을 `status → deactivate → status`로 좁게 해제한 뒤 config를 schema v2 explicit mode로 바꾸고 문서·routing을 반영했다.
- Target에서 임의의 무관한 session에 `SessionStart → UserPromptSubmit → Stop` payload를 실행했을 때 모두 `continue: true`로 조용히 끝났고 해당 runtime directory가 생기지 않았다. Target 전체 `108`개 테스트는 기존 descendant-timeout test가 병렬·첫 실행에서 한 번씩 실패했으나 단독 통과 뒤 독립 전체 실행에서 모두 통과했다.
- Target의 기존 runtime을 삭제·이동·일괄 retarget하지 않았고, 사용자 소유 `context/analysis/` 변경을 건드리지 않았다. Workspace 004에도 이 Harness 사건을 기록하지 않았으며 최종 scoped status가 clean이다.
- Session binding을 새 Harness peer로 분리할지 전체 구조에서 다시 검토한 결과, runtime과 event가 Maintain의 시작·response-end·비동기 반영에만 소비되고 독립된 cross-Harness lifecycle은 없음을 확인했다. 따라서 Maintain README를 전체 정체성·내부 관계 Owner로 유지하고, 상세 admission·binding generation·hook·worker·notice·runtime retention·actual-host proof ceiling만 uppercase 내부 canonical `SESSION-BINDING-AND-LIFECYCLE.md`로 분리했다.
- `CREATE-AND-TRANSITION.md`에는 새 Workspace 생성·전환의 의미 결정과 같은 session을 이어 갈지 격리할지 판단하는 책임을 남기고, 결정 뒤 generation commit과 event 귀속의 실행 계약은 새 Maintain 내부 canonical로 연결했다. 기존 schema v2 구현, runtime 위치, `maintain` 코드·CLI 이름과 target 동작은 바꾸지 않았다.

초기 skill 결과는 [`record 03`](../records/2026-08-28-03-canonical-cohesion-and-workspace-skill.md), 전환 규칙 보정은 [`record 04`](../records/2026-08-31-04-activation-rule-recalibration.md), session별 binding 구현과 target 적용은 [`record 05`](../records/2026-09-01-05-session-scoped-binding-and-rebind.md), Maintain 내부 lifecycle canonical 책임 정렬은 [`record 06`](../records/2026-09-01-06-maintain-session-lifecycle-canonical.md)에 남겼다.

## 남은 외부 확인

- 새 target-root Codex task에서 hook trust 뒤 무관한 session이 계속 unbound인지 확인한다. 현재 직접 payload 검사는 실제 host가 hook을 호출했다는 증거는 아니다.
- 별도의 의도된 Workspace task에서 explicit activation, 후속 prompt/Stop과 detached semantic worker, important notice의 UI 전달을 확인한다.
- 실제 host의 여러 task로 S1:A, S2:B, S3:unbound 병행과 같은-session A→B 전환·재개를 확인한다. Unit test와 직접 wrapper 호출은 host scheduler·UI acceptance를 대신하지 않는다.
- 모든 goal에서 의미 누락이 없다는 보장과 사람 acceptance는 자동화하지 않는다.

## 다음 행동

사용자가 Reference와 target 변경을 수락하고 commit을 승인했다. Target 적용분은 commit `08a1f0b`로 보존됐고 Reference 변경은 이 current·records와 함께 commit한다. 실제 Codex multi-task acceptance는 별도 경계로 남는다.
