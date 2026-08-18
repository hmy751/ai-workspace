# Records

이 폴더는 clean-room Maintain 재구현의 선택 근거, 구조 후보와 탈락 이유, 실패·검증과 handoff를 보존한다. Workspace 005·006 원문 전체를 복제하지 않고 현재 판단에 필요한 최소 발췌와 locator만 둔다.

- [`2026-08-18-01-clean-room-source-and-behavior-contract.md`](2026-08-18-01-clean-room-source-and-behavior-contract.md): Workspace 005의 직접 사용자 근거, 여섯 행동 장면, 글로벌 책임 기준과 topology 비승계 경계
- [`2026-08-18-02-code-reset-baseline-and-excluded-topologies.md`](2026-08-18-02-code-reset-baseline-and-excluded-topologies.md): 복원 commit·exact path manifest, root 비활성화, 검증 결과와 반복하지 않을 구조
- [`2026-08-18-03-clean-room-implementation-handoff.md`](2026-08-18-03-clean-room-implementation-handoff.md): same-workspace fresh agent가 source에서 현재 상태를 재현하고 첫 행동을 수행하기 위한 prepared handoff

새 설계 record는 fresh session이 acceptance matrix와 최소 vertical slice를 실제로 도출한 뒤에만 추가한다. 이 records에 있다는 이유만으로 후보가 current 또는 output이 되지는 않는다.
