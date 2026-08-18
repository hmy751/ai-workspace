# Maintain clean-room reimplementation state

마지막 갱신: `2026-08-19`

## 현재 상태

- Active Workspace는 007이다. Reference에 Maintain core, persisted Codex session bridge, host lifecycle adapter, hook wiring·CLI·schema·tests를 구현하고 독립 리뷰의 국소 지적을 반영했다.
- 006 중단 기록은 `0952b1d`, code reset은 `b508d80`에 있다.
- `reference-project/`와 적용 skill의 복원 대상은 preimplementation commit `2649e9b`와 일치한다.
- Root hook은 빈 설정이며 Maintain agent·Workspace binding은 없다. Reference 구현은 root에 연결하지 않았다.
- `.context-harness/runtime/`의 과거 005·006 runtime 잔재 전체는 inactive이고 현재 설계 근거·canonical·migration 입력으로 선택되지 않았다. 다시 사용할 필요가 생기면 의미와 처리 권한을 별도로 판단한다.
- 사용자 소유 untracked `.DS_Store`는 범위 밖이다.

Reset 기준은 [`record 02`](../records/2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md), 구현·actual host evidence는 [`record 05`](../records/2026-08-19-05-reference-implementation-and-host-evidence.md), 현재 책임 재분류와 남은 범위는 [`record 06`](../records/2026-08-19-06-purpose-rebaseline-and-remaining-scope.md)이 소유한다.

## 검증 상한

- Maintain `40/40`, Recover `31/31`, compile·JSON/TOML parse·diff check가 통과했다.
- Reference 전체 suite는 `93`개 중 기존 Verify descendant-timeout timing test 1건만 실패했고 isolated retry는 통과했다. Reset baseline부터 알려진 timing instability로 분리한다.
- 실제 Codex에서 새 session grounding, 두 turn warm reuse, stable response pairing, no-change, ambiguity zero-write·다음 prompt 전달, quiet guarded update와 failure 전달을 확인했다.
- Broad evidence 자동 수집은 누락 구현이 아니라 Maintain·Host 책임에서 제거했다. 기본 의미 입력은 Workspace Context, 사용자 발화와 Main 응답이며 이미 제공된 제한된 확인만 출처 강도를 보존해 사용할 수 있다.
- Semantic resume 또는 guarded apply가 실패한 뒤 같은 session의 후속 event가 최신 Context인 것처럼 적용되지 않는 최소 동작은 아직 확정·검증되지 않았다.
- 현실적인 연속 대화에서 일회성 설명, 사용자 결정, Main의 미검증 보고, 명확한 update와 ambiguity를 구분하는 semantic acceptance가 더 필요하다.
- Mid-session thread 자동 re-grounding, grounding ambiguity 자동 재개, strict crash effect-once, multi-file transaction, 완전한 compare-and-swap, SessionEnd delivery acknowledgment와 non-POSIX lock은 구현됐다고 주장하지 않는 보류 한계이며 1차 root 연결의 자동 blocker는 아니다.

## 다음 시작점

Reference 계약에서 broad evidence 의무와 같은 outer session의 자동 thread re-grounding 보장을 제거했다. 기존 queue·lock·effect marker·persisted thread와 Guard 경계는 현재 행동을 지지하므로 구조가 있다는 이유만으로 철거하지 않는다.

다음 slice는 semantic/apply 실패 뒤 후속 event의 최소 안전 동작과 direct test를 먼저 확정하고, 작은 semantic acceptance 묶음을 실제 Maintainer로 확인한다. 그 결과를 actual host에서 재확인한 뒤 root 연결을 판단한다.

과거 구현 diff·runtime·records를 더 읽어 해법을 고르지 않는다. 현재 Reference와 actual host evidence에서만 미해결 책임을 좁힌다.
