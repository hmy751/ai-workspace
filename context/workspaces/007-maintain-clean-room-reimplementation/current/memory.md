# Maintain clean-room reimplementation memory

마지막 갱신: `2026-08-19`

## 목표

Workspace 005에서 사용자와 합의한 Maintainer 경험을 글로벌 책임 원칙으로 다시 배치해 `reference-project/`에 재사용 가능하게 구현한다. 이전 구현을 줄이는 작업도 분석으로 끝나는 작업도 아니며, reset된 baseline에서 새 계약·코드·검증을 실제로 만든다.

## 유지할 핵심

- 사용자 동작과 직접 근거는 [`record 01`](../records/2026-08-18-01-clean-room-source-and-behavior-contract.md)이 소유한다.
- Reset된 code baseline과 과거 topology의 근거·proof ceiling은 [`record 02`](../records/2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md)가 소유한다.
- 실제 구현 목표, 충분한 mental model과 clean-room 읽기 경계는 [`record 03`](../records/2026-08-19-03-implementation-goal-and-reading-boundary.md)이 소유한다.
- 여섯 장면의 직접 acceptance, 현재 host 제약과 첫 구현 책임은 [`record 04`](../records/2026-08-19-04-acceptance-and-first-implementation-slice.md)가 소유한다.
- Reference 구현, direct test·actual Codex 장면과 당시 독립 리뷰의 proof gap은 [`record 05`](../records/2026-08-19-05-reference-implementation-and-host-evidence.md)가 소유한다.
- Maintainer 목적 재기준화, 현재 유지·수정·보류와 root 연결 전 남은 범위는 [`record 06`](../records/2026-08-19-06-purpose-rebaseline-and-remaining-scope.md)이 소유한다.
- Semantic/apply failure 뒤 후속 event의 최소 안전 동작과 실제 Maintainer 연속 대화 acceptance는 [`record 07`](../records/2026-08-19-07-failure-ordering-and-semantic-acceptance.md)이 소유한다.
- Reference와 outer root의 Context 구조 차이, 단순 연결을 중단한 이유와 별도 적용 범위는 [`record 08`](../records/2026-08-19-08-root-connection-boundary.md)이 소유한다.
- Record 01의 여섯 장면은 구현을 시작하기에 충분한 mental model이다. Acceptance matrix는 이를 다시 논의하지 않고 관찰 조건과 구현 책임으로 번역한다.
- 005·006의 hook, queue, cursor, transaction, attention과 recovery topology는 자동 승계되는 요구사항도 금지 항목도 아니다. 같은 구조를 유지하거나 피해야 할 의무 없이 현재 조건에서 다시 선택한다.
- 설계 입력은 현재 사용자 의도, 007 behavior, 글로벌 AI-system references, reset된 `reference-project/`와 현재 host 계약 순서로 둔다. 005·006 과거 구현과 runtime은 exact 근거가 다시 필요할 때만 제한적으로 연다.
- 현재 선택된 구현은 Reference의 `explicit Recover bootstrap → persisted read-only semantic thread → structured decision → guarded apply → hook lifecycle adapter`다.
- 기본 의미 입력은 Workspace Context, 사용자 발화와 Main 응답이다. 이미 제공된 제한된 근거는 출처 강도를 보존해 사용할 수 있지만, host adapter나 Maintainer가 diff·Git 상태·test/eval evidence를 기본 수집하거나 새 검증을 실행하지 않는다.
- 새 Main session은 새 Maintainer와 bounded Recover로 시작한다. 살아 있는 session 내부 thread 자동 복구, 최초 grounding ambiguity 자동 재개, 완전한 CAS·transaction·strict effect-once와 종료 notice acknowledgment는 현재 보류한 한계다.
- Semantic/apply 실패는 뒤 event를 같은 Main session에서 적용하지 않고 pending으로 남긴다. Pairing 이전 실패는 뒤의 정상 event를 막지 않는다.
- 실제 Maintainer 한 thread가 no-change, 사용자 결정, Main의 미검증 보고, canonical·완료 ambiguity와 warm 후속 정정을 의도한 provenance 강도로 구분했다.
- Reference clean-room 구현은 완료다. Outer root automatic Maintain은 기존 canonical 보존 방식을 정하는 별도 target 적용 전까지 비활성이다.
