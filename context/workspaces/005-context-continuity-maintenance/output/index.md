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
- [Response-end Observe runtime과 live smoke](../records/2026-08-17-06-response-end-observe-runtime-and-live-smoke.md): first Observe 구현, 내부 test와 실제 async Stop 취소, 다음 protocol 결정
- [Reference 소유권 정정과 재계획 handoff](../records/2026-08-17-07-reference-ownership-correction-and-handoff.md): root-only 배치가 최종 architecture가 아닌 이유와 다음 세션의 소유권 재계획 커서
- [세션형 Maintainer 동작과 Reference 전체 구현 계획](../records/2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md): 초기 sync, 세션 동안의 지속 이해, 판단·보고·복구와 승인된 전체 구현 순서
- [Repo-local Observe runtime](../../../../.codex/context_maintainer/): Workspace 005에 고정된 event·queue·cursor dogfood 구현. 현재 실험 근거이며 재사용 가능한 최종 canonical로 acceptance되지 않았다.
- [지속 기준](../current/memory.md): 이후 설계에서 유지해야 할 사용자 판단과 역할 경계
- [현재 설계 커서](../current/state.md): 확정된 구현 순서, 기술 후보와 다음 Reference 작업

## 현재 상태

진단, Maintain·retrieval·runtime 의미 계약과 축소 Verify 책임에 더해 세션형 Maintainer의 초기 sync·지속 이해·background 활동·판단·보고·복구 동작과 Reference 전체 구현 순서를 선택했다. Root Observe는 내부 test와 live async Stop 실패를 남긴 실험 근거일 뿐 최종 architecture가 아니다. 다음 산출물은 Reference Harness·Maintain 계약 수정과 Reference 내부 runtime spike다. Hook·queue·storage·CLI·schema와 고정 성능 수치는 아직 구현 후보다.
