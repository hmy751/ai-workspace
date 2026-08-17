# Context continuity maintenance current

마지막 갱신: `2026-08-17`

이 폴더는 다음 세션이 긴 대화 전체를 다시 읽지 않고도 context continuity 운영 설계를 이어 가는 데 필요한 최신 상태를 소유한다.

## 재진입 순서

1. [`memory.md`](memory.md)에서 사용자 우선순위와 유지할 역할 경계를 확인한다.
2. [`state.md`](state.md)에서 확정·제안·미결정을 구분하고 마지막 질문부터 이어 간다.
3. [`../output/index.md`](../output/index.md)에서 현재 선택된 진단과 설계 framing을 확인한다.
4. 실제 시간·workflow 근거가 필요할 때만 [운영 지연 진단 record](../records/2026-08-17-01-harness-operation-latency-and-role-diagnosis.md)를 읽는다.
5. 사용자 발화 근거·현업 자료·background 설계 후보가 필요할 때만 [설계 framing record](../records/2026-08-17-02-context-continuity-and-background-maintenance-framing.md)를 읽는다.
6. 매 응답 점검과 자동 갱신 범위가 확정된 과정을 확인할 때만 [응답 종료 점검 record](../records/2026-08-17-03-response-end-maintenance-contract-and-verify-reopening.md)를 읽는다.
7. Verify를 제품 검증 주체에서 증거 기록 보조로 낮춘 이유가 필요할 때만 [Verify 증거 기록 record](../records/2026-08-17-04-verify-evidence-recording-boundary.md)를 읽는다.
8. Maintainer의 선택적 조회, 재사용 수명과 event·cursor 판단 경계가 필요할 때만 [retrieval·runtime 계약 record](../records/2026-08-17-05-maintainer-retrieval-runtime-and-cursor-contract.md)를 읽는다.

Workspace 004의 구현 상세나 Workspace 002의 target 적용 이력은 이 설계 판단에 필요한 링크가 명시된 경우에만 연다.
