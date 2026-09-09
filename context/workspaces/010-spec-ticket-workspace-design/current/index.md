# Spec·Ticket 설계 current

마지막 갱신: 2026-09-09

현재는 `bc3d954` 통합 뒤 외부 연구 07 전체를 대조하고, 후속 사용자 요청으로 Decision의 생성·불확실성 보존 기준을 보완한 상태다. 사용자가 마무리 기록과 커밋을 요청했다. [전체 대조 기록](../records/2026-09-09-01-research-07-adoption-audit.md)과 state에서 반영 전 감사·후속 반영·실제 운영 미검증을 구분한다.

외부 연구 08의 네 스킬·Spec·Ticket 후속 합의를 Reference에 반영했다. 2026-09-09 사용자가 커밋을 요청해 앞선 보류를 해제했다. 통합 변경과 검증 결과는 state 및 [통합 기록](../records/2026-09-08-15-skills-spec-ticket-reference-integration.md)에서 이어간다. 적용 전 비교는 [분석 기록](../records/2026-09-08-14-skills-spec-ticket-reintegration-assessment.md)에 보존한다.

1. [memory.md](memory.md): 목적·조건, Spec 구성과 배치, Ticket·state·records 관계, 유지할 역할.
2. [state.md](state.md): 현재 단계, 남은 실제 적용 작업과 확인 범위.
3. [output/index.md](../output/index.md): 채택한 구성 설명과 구체적인 Spec 예시.

설계 기록을 `4fe8694`로 커밋하고 Reference에 적용했다. 후속 요청으로 `project-context.md`의 옛 번호를 제거하고 적용 변경을 `dcd3c6f`로 커밋했다. 연구 측이 선택 이유와 실제 구현·검증 범위를 함께 읽을 [종합 전달 문서](../output/research-feedback-spec-ticket-integration.md)도 구성했다. Spec과 Ticket은 memory에 두며, 기존처럼 Maintain은 기록·갱신을, Main은 작업 조율을 맡는다. 개별 실행자의 범위는 열어 둔다.

적용 결과와 검증 한계는 [Reference 적용 기록](../records/2026-09-08-12-reference-spec-ticket-implementation.md)에 있다. 적용 전 합의·열린 부분·남은 작업은 [설계 정리 기록](../records/2026-09-08-11-design-status-and-remaining-work.md)에 모았다. 원문과 판단 변화를 다시 볼 때는 [records 색인](../records/README.md)에서 해당 기록만 선택한다. 기본 재진입에 과거 기록 전체나 009의 current를 읽을 필요는 없다.
