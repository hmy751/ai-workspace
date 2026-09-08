# Spec·Ticket 설계 current

마지막 갱신: 2026-09-08

1. [memory.md](memory.md): 목적·조건, Spec 구성과 배치, Ticket·state·records 관계, 유지할 역할.
2. [state.md](state.md): 현재 단계, 남은 실제 적용 작업과 확인 범위.
3. [output/index.md](../output/index.md): 채택한 구성 설명과 구체적인 Spec 예시.

설계 기록을 `4fe8694`로 커밋하고 Reference에 적용했다. 후속 요청으로 `project-context.md`의 옛 번호를 제거하고 적용 변경을 커밋하는 단계다. Spec과 Ticket은 memory에 두며, 기존처럼 Maintain은 기록·갱신을, Main은 작업 조율을 맡는다. 개별 실행자의 범위는 열어 둔다.

적용 결과와 검증 한계는 [Reference 적용 기록](../records/2026-09-08-12-reference-spec-ticket-implementation.md)에 있다. 적용 전 합의·열린 부분·남은 작업은 [설계 정리 기록](../records/2026-09-08-11-design-status-and-remaining-work.md)에 모았다. 원문과 판단 변화를 다시 볼 때는 [records 색인](../records/README.md)에서 해당 기록만 선택한다. 기본 재진입에 과거 기록 전체나 009의 current를 읽을 필요는 없다.
