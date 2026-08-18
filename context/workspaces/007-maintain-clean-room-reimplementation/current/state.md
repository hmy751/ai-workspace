# Maintain clean-room reimplementation state

마지막 갱신: `2026-08-19`

## 현재 상태

- Active Workspace는 007이다. Reference에 Maintain core, persisted Codex session bridge, host lifecycle adapter, hook wiring·CLI·schema·tests를 구현하고 독립 리뷰의 국소 지적과 failure ordering 최소 정책을 반영했다.
- 006 중단 기록은 `0952b1d`, code reset은 `b508d80`에 있다.
- `reference-project/`와 적용 skill의 복원 대상은 preimplementation commit `2649e9b`와 일치한다.
- Root hook은 빈 설정이며 Maintain agent·Workspace binding은 없다. Reference 구현은 root에 연결하지 않았다.
- `.context-harness/runtime/`의 과거 005·006 runtime 잔재 전체는 inactive이고 현재 설계 근거·canonical·migration 입력으로 선택되지 않았다. 다시 사용할 필요가 생기면 의미와 처리 권한을 별도로 판단한다.
- 사용자 소유 untracked `.DS_Store`는 범위 밖이다.

Reset 기준은 [`record 02`](../records/2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md), 구현·초기 actual host evidence는 [`record 05`](../records/2026-08-19-05-reference-implementation-and-host-evidence.md), 책임 재분류는 [`record 06`](../records/2026-08-19-06-purpose-rebaseline-and-remaining-scope.md), 남은 항목의 구현·acceptance는 [`record 07`](../records/2026-08-19-07-failure-ordering-and-semantic-acceptance.md), outer root 적용 경계는 [`record 08`](../records/2026-08-19-08-root-connection-boundary.md)이 소유한다.

## 검증 상한

- Maintain `44/44`, Recover `31/31`, JSON/TOML parse·diff check가 통과했다.
- Reference 전체 suite는 `97`개 중 기존 Verify descendant-timeout timing test 1건만 실패했고 isolated retry는 통과했다. Reset baseline부터 알려진 timing instability로 분리한다.
- 실제 Codex에서 새 session grounding, 두 turn warm reuse, stable response pairing, no-change, ambiguity zero-write·다음 prompt 전달, quiet guarded update와 failure 전달을 확인했다.
- Broad evidence 자동 수집은 누락 구현이 아니라 Maintain·Host 책임에서 제거했다. 기본 의미 입력은 Workspace Context, 사용자 발화와 Main 응답이며 이미 제공된 제한된 확인만 출처 강도를 보존해 사용할 수 있다.
- Semantic resume 또는 guarded apply가 실패하면 뒤 event를 같은 Main session에서 적용하지 않고 pending으로 남긴다. Pairing 이전 실패는 뒤 정상 event를 막지 않는다. Direct test와 실제 Codex resume failure에서 확인했다.
- 실제 Maintainer 한 thread가 일회성 설명, 사용자 결정, Main의 미검증 보고, canonical·완료 ambiguity와 warm 후속 정정을 의도한 outcome과 provenance 강도로 구분했다.
- Mid-session thread 자동 re-grounding, grounding ambiguity 자동 재개, strict crash effect-once, multi-file transaction, 완전한 compare-and-swap, SessionEnd delivery acknowledgment와 non-POSIX lock은 구현됐다고 주장하지 않는 보류 한계이며 1차 root 연결의 자동 blocker는 아니다.

## 다음 시작점

Reference 계약에서 broad evidence 의무와 같은 outer session의 자동 thread re-grounding 보장을 제거했다. 기존 queue·lock·effect marker·persisted thread와 Guard 경계는 현재 행동을 지지하므로 구조가 있다는 이유만으로 철거하지 않는다. Record 01의 여섯 장면과 record 06이 남긴 1차 acceptance 범위는 충족했다.

Reference clean-room 구현은 완료로 판정한다. Outer root는 `context/workspaces/`를 canonical로 쓰지만 Reference adapter는 `context/work/workspaces/`와 별도 identity·Recover 계약을 전제로 하므로 단순 hook 연결을 하지 않는다. 기존 canonical을 보존하는 target mapping을 먼저 정하는 별도 적용 작업으로 넘긴다.

과거 구현 diff·runtime·records를 더 읽어 해법을 고르지 않는다. 현재 Reference와 actual host evidence에서만 미해결 책임을 좁힌다.
