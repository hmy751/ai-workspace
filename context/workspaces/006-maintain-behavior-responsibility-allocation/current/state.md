# Maintain behavior responsibility allocation state

마지막 갱신: `2026-08-18`

## 현재 상태

Workspace 006 작업은 사용자 결정으로 중단됐다. 기존 구현의 파일과 protocol을 개선 대상으로 둔 순간부터 판단이 그 topology에 묶였고, 구조를 줄이려던 첫 시도도 legacy migration·replay bridge·delivery cursor와 추가 crash recovery를 만들었다. 이 diff는 선택된 개선이 아니며 새 Workspace가 이어서 고치지 않는다.

## 확인된 시작점

- Workspace 005 records 01–09는 운영 지연 진단, background framing, response-end 계약, Verify 축소, runtime cursor 계약, 실패한 Observe 실험, Reference 소유권 정정, 세션형 Maintainer 동작, 최종 구현과 proof를 시간순으로 보존한다.
- 사용자에게 보존해야 할 핵심은 bounded grounding, warm continuity, 매 response-end 점검, no-change·quiet update·important report·write 전 ambiguity, Main 비차단과 false freshness 방지다.
- Record 02는 역할 구분과 고정 topology를 같게 보지 말라고 경고했고, record 06의 root Observe는 `async Stop` 취소와 global FIFO gap 때문에 live smoke에서 실패했다.
- Record 08은 hook 조합, queue·locking·storage·transaction, cursor schema, CLI·JSON, raw 보존과 UI 전달 방식을 승인된 architecture가 아닌 교체 가능한 기술 후보로 명시했다.
- Record 09의 Reference-first 구현과 로컬 검증은 commit `9553d0a`에 보존돼 있지만, 실제 nested Codex warm resume·background 비차단·UI notice·semantic 문서 품질은 여전히 proof ceiling 밖이다.
- 개선 대상의 canonical은 `reference-project/context/work/harness/maintain/`이며 root에 semantic code나 prompt를 복제하지 않는다.
- 변경 전 production Python은 약 8,800줄이고 `runtime.py`만 4,603줄이었다. Runtime은 capture·pairing·queue·scheduling·session state·report·freshness·gap repair·metrics를 한 파일에 모으면서, 하나의 Context 반영 transaction은 controller·intent·writer·runtime에 흩어져 있었다.
- 글로벌 reference는 판단 렌즈이며 수정 대상이 아니다.
- 최소 mental model에서 모델은 durability·Owner·ambiguity·보고 중요도를 판단하고, 규칙 장치는 Workspace allowlist·symlink/path escape·최신 baseline·false success만 보장하며, 사람은 goal·정책·acceptance와 자동 복원 불가능한 누락을 결정한다.
- [`self-check와 목적 우선 재정렬 record`](../records/2026-08-18-03-self-check-and-purpose-first-reset.md)가 방향 어긋남, 005 원문 근거와 다음 구조 판단 기준을 소유한다.
- [`completed response와 Workspace attention record`](../records/2026-08-18-04-completed-response-and-workspace-attention.md)는 중단된 구현 시도와 deterministic proof만 소유한다.
- [`clean-room 재시작 결정`](../records/2026-08-18-05-clean-room-restart-decision.md)이 이 Workspace의 종료와 다음 code baseline을 소유한다.

## 중단 시점의 확인 결과

- `UserPromptSubmit`은 prompt를 보존하지만 processing sequence를 예약하지 않는다. `Stop`까지 있어 완성된 response pair가 된 시점에만 순서를 부여한다.
- Active missing-Stop gap, `control.json`, gap repair API·CLI를 제거했다. Incomplete tail은 전달 누락 가능성으로 남지만 뒤 completed response나 다른 session을 막지 않는다.
- `attention.py`가 한 Workspace의 pending notice·question을 소유한다. Session별 `pending_reports`, recipient/origin/delivery 배열, cross-session resolver와 `report_pending` freshness branch는 active 경로에서 제거했다.
- Context write 뒤 attention mutation을 적용하고 runtime checkpoint를 commit한 다음 replay bridge를 confirm한다. Attention 뒤 checkpoint 전 crash와 checkpoint 뒤 confirm 전 crash는 exact intent 재진입으로 모델 재호출 없이 수렴한다.
- Checkpoint v3와 Workspace attention, bounded legacy migration, post-flush delivery cursor까지 구현했다.
- Freshness와 Workspace attention을 status에서 분리했다. Malformed attention이나 migration 실패를 config 오류나 fresh 상태로 바꾸지 않는다.
- 이전 gap repair가 만든 exact abandoned state와 capture publish crash residue는 새 repair 권한을 만들지 않는 제한된 compatibility·recovery 경로로만 읽는다.

## 생성·연결 검증

- Root `.codex/context-maintain.json`은 `006-maintain-behavior-responsibility-allocation`을 선택한다.
- Reference Maintain config loader에서 새 Workspace가 `workspace_bound: true`로 판정됐다.
- Maintain status 진입은 Workspace 006 identity, session `0`, notice `0`, question `0`, attention `ready`인 runtime 상태를 반환했다.
- Root Maintain JSON·TOML 설정 parse와 `git diff --check`가 통과했다.
- 글로벌 reference는 수정하지 않았다. Reference Maintain README·prompt·schema·controller·runtime·intent·hook과 관련 test를 새 책임 배치에 맞게 수정했다.
- 중단 직전 Maintain 전체 test `207/207`, Reference 전체 test `265/265`, `git diff --check`가 통과했다.
- 최초 독립 리뷰가 P1 네 건을 찾았고 회귀 test와 보정이 추가됐다. 그 보정에 대한 마지막 독립 재리뷰는 사용자의 중단 지시로 완료되지 않았다.
- 이 검증은 deterministic code·filesystem 경계의 증거다. 실제 Codex host trust, nested warm resume, detached worker kill, UI 전달과 semantic 문서 품질 acceptance는 아니다.

## 정직한 구조 평가

- Active surface 일부를 없앴지만 새 attention store, migration, compatibility와 delivery state가 추가됐다. 기존 구현을 보존하면서 줄이려는 접근이 오히려 새 복구 책임을 만드는 징후였다.
- `decision intent → writer journal → completion marker → runtime checkpoint`도 그대로 남았다.
- Test 통과는 구현 내부의 deterministic 일관성만 보이며, 목적에 맞는 최소 구조나 실제 host 경험을 acceptance하지 않는다.

## 다음 행동

1. 006 문서와 records만 커밋해 중단 판단을 보존한다.
2. Commit `9553d0a`가 바꾼 live implementation·adapter·연결 문서를 부모 `2649e9b` 상태로 path-scoped 복원하되 Workspace 005 records는 보존한다.
3. 새 Workspace에 필요한 005 근거, 글로벌 책임 배치 기준, 금지선과 handoff를 독립적으로 구성한다.
4. 새 세션은 code baseline과 새 Workspace source만 읽고 첫 구조를 다시 도출한다. 006 diff를 후보 구현으로 읽지 않는다.
