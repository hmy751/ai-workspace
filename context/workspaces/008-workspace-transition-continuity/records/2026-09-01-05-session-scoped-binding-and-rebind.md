# Session별 Maintain binding과 same-session rebind

날짜: `2026-09-01`

## 사건과 원인

`memory-harness-research` 안에서 Workspace 004와 무관한 영상 분석 대화가 004의 Maintain agent에 연결돼 Context를 갱신했다. Hook payload의 `session_id`와 runtime directory, semantic thread는 대화마다 분리돼 있었지만 Project 공통 `.codex/maintain.json`이 하나의 `workspace_id`를 모든 새 session의 binding으로 사용했다. 따라서 문제는 session identity 부재가 아니라 **session별 Workspace admission 부재**였다.

사고 session `01a05864-3539-7f92-91fa-71734ed867d0`은 첫 사용자 prompt 전 Workspace 004로 grounding돼 있었다. 반면 과거 002→003 전환에서는 같은 outer session의 runtime을 수동 교체해 전환 요청 prompt는 predecessor에, Stop은 successor에 들어간 pairing failure가 확인됐다. Default-unbound만 추가하고 binding을 영구 고정하면 이 이동 문제가 다른 형태로 재발한다.

## 선택한 책임 배치

- 사람과 Main은 현재 작업을 어떤 Workspace에 연결·전환할지 명시적으로 결정한다. Active index, Project 기본값이나 대화 의미로 추론하지 않는다.
- `CODEX_SESSION_ID`가 outer Main session identity다. Subagent도 이를 공유할 수 있으므로 control command는 Main만 실행한다.
- Deterministic adapter는 grounding 성공, binding generation, prompt·Stop pairing, worker의 exact Workspace·thread 귀속과 guarded apply 경계를 집행한다.
- Semantic Maintainer는 이미 선택된 Workspace 안에서 durable 의미와 기존 Owner를 판단할 뿐 session admission이나 전환을 결정하지 않는다.
- `.codex/maintain.json`은 schema v2 `mode: explicit`만 선언하고 Workspace id를 소유하지 않는다.

## 구현한 상태 전이

- 새 session은 unbound이며 `SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd`가 runtime·grounding·Workspace write·경고 없이 no-op한다.
- `activate <workspace_id>`는 bounded Recover와 새 semantic grounding이 성공한 뒤에만 새 generation을 commit한다. 실패하면 이전 binding 또는 unbound를 보존한다.
- 이미 prompt가 접수된 turn 안에서 activate해도 그 prompt와 Stop은 predecessor generation에 남는다. 최초 unbound turn은 prompt snapshot이 없으므로 그 Stop도 successor로 소급하지 않고 다음 prompt부터 활성화한다.
- Event는 `binding_generation`, `workspace_id`, `thread_id` snapshot을 가지며 worker는 Project config나 현재 binding을 다시 읽어 retarget하지 않는다.
- 한 generation의 blocking failure는 같은 generation의 뒤 event만 막는다. 다른 generation의 관련 없는 pending·failure는 이동을 막지 않는다.
- `deactivate`는 `current_generation`만 null로 만들고 binding history, event, effect와 delivery truth를 보존한다.
- Schema v1 Project config는 migration 중 읽기만 하며 새 session 자동 binding에 사용하지 않는다. 기존 v1 session state와 event는 generation 1로 lazy 해석한다.

## Target 적용

Target에는 v2 호환 adapter와 테스트·wrapper를 config보다 먼저 적용했다. Focused test가 통과한 뒤 사고 session status에서 Workspace 004 generation 1, unresolved·blocking·open prompt `0`을 확인하고 그 session만 deactivate했다. 이후 `.codex/maintain.json`을 schema v2 explicit mode로 바꾸고 hook message, root routing, Harness README, 생성·전환 canonical과 repo-local skill을 같은 의미로 맞췄다.

기존 ignored runtime은 삭제·이동·일괄 변환하지 않았다. Target의 연구 문서 변경과 Workspace 004 내용도 수정하지 않았다. 이번 Harness 사건을 004에 기록하면 오연결을 다시 반복하므로 Reference 변경의 Owner인 Workspace 008에만 남겼다.

## 검증과 상한

- Reference host adapter focused test `40/40` 통과
- Reference 전체 unit test `115/115` 통과
- Target host adapter focused test `40/40` 통과
- Target에서 임의 unbound session의 `SessionStart → UserPromptSubmit → Stop` 직접 payload가 모두 조용히 통과하고 runtime directory를 만들지 않음
- 사고 session은 deactivate 전 active Workspace 004, 후 unbound로 확인됨
- Target 전체 unit test는 기존 descendant-timeout timing test가 첫 실행과 병렬 실행에서 한 번씩 실패했고 단독 재실행이 통과한 뒤 독립 전체 `108/108` 통과
- 두 저장소의 JSON parse와 `git diff --check` 통과

이 결과는 상태 전이와 직접 wrapper·hook handler 동작을 입증한다. 새 target-root Codex task의 실제 hook trust와 scheduler event 전달, 여러 task의 A/B/unbound 병행, same-session rebind 뒤 UI notice와 detached worker 동작은 별도 actual-host acceptance로 남는다.
