# Context continuity maintenance output

마지막 갱신: `2026-08-17`

## Workspace goal

작업을 막지 않는 속도와 다음 세션이 믿을 수 있는 지속 context 사이의 운영 경계를 정한다.

## 현재 선택된 산출물

- [운영 지연과 역할 진단](../records/2026-08-17-01-harness-operation-latency-and-role-diagnosis.md): 긴 실행 시간의 실제 구성, 역할별 동작과 정상 activation boundary
- [Context continuity와 background maintenance framing](../records/2026-08-17-02-context-continuity-and-background-maintenance-framing.md): 사용자 우선순위, 현업 대조, background 분류·쓰기·보고 후보
- [응답 종료 점검과 갱신 계약](../records/2026-08-17-03-response-end-maintenance-contract-and-verify-reopening.md): 확정된 Maintain activation·allowlist·ambiguity 처리와 다시 열린 Verify 질문
- [Verify 증거 기록 경계](../records/2026-08-17-04-verify-evidence-recording-boundary.md): Verify를 제품 검증 주체가 아닌 선택적 증거 수집·기록 보조로 낮춘 결정
- [Maintainer retrieval·runtime·cursor 계약](../records/2026-08-17-05-maintainer-retrieval-runtime-and-cursor-contract.md): current 우선 retrieval, 동일 주체 재사용, response-end event와 replay 가능한 cursor 경계
- [지속 기준](../current/memory.md): 이후 설계에서 유지해야 할 사용자 판단과 역할 경계
- [현재 설계 커서](../current/state.md): 채택 전인 항목, 마지막 질문과 다음 결정 순서

## 현재 상태

진단, Maintain·retrieval·runtime 의미 계약과 축소 Verify 책임은 선택했다. Background maintainer의 hook, event delivery, cursor 저장 위치·schema, queue·locking, compaction 감지, memory index 구조, Verify evidence helper와 평가 방법은 아직 구현하지 않았다. 이 output 등재는 구현 완료나 운영 효과를 뜻하지 않는다.
