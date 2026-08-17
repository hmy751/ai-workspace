# Context continuity maintenance Workspace

Main과 사용자의 실제 작업을 막지 않으면서 `current/records`를 다음 세션이 믿고 이어 갈 만큼 유지하는 운영 방식을 구체화하는 Workspace다. Recover·Verify·Maintain을 없애는 작업이 아니라, 각 책임을 언제 어떤 강도로 실행하고 background maintainer에 어디까지 직접 쓰기 권한을 줄지 정한다.

상태는 **active**다. 이 작업은 사용자가 “수정 작업들이 30분, 26분처럼 오래 걸린 이유”를 물은 시점부터 시작한다. Workspace 005 전용 root Observe runtime은 실제 `async Stop` 취소로 end-to-end pairing에 실패했고 최종 architecture로 acceptance되지 않았다. 이후 사용자와 Maintainer의 세션 수명·초기 동기화·background 활동·판단·보고·복구 동작을 다시 맞췄으며, 재사용 가능한 전체 구현은 `reference-project/`, root는 thin dogfood adapter가 소유하는 단계형 계획을 확정했다. 다음 단계는 Reference Harness·Maintain 계약 수정이다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 사용자 우선순위, 유지할 역할 경계와 이미 선택된 방향
2. [`current/state.md`](current/state.md): 확정된 구현 순서, 기술 후보와 바로 이어 갈 Reference 작업
3. [`output/index.md`](output/index.md): 현재 선택된 진단·설계 산출물과 구현되지 않은 경계
4. [운영 지연과 역할 진단](records/2026-08-17-01-harness-operation-latency-and-role-diagnosis.md): 30분·26분 문제의 비용 분해, Recover·Verify·Maintain의 실제 동작과 flake
5. [Context continuity와 background maintenance framing](records/2026-08-17-02-context-continuity-and-background-maintenance-framing.md): 현업 자료 대조, 사용자 C/E 우선순위, 자동 기록 조건과 열린 질문
6. [응답 종료 점검과 갱신 계약](records/2026-08-17-03-response-end-maintenance-contract-and-verify-reopening.md): 매 응답 점검, 자동 갱신 범위, ambiguity 보고와 다시 열린 Verify 논의
7. [Verify 증거 기록 경계](records/2026-08-17-04-verify-evidence-recording-boundary.md): 기존 Verify의 목적 재검토와 가벼운 증거 수집·기록 보조로 축소한 책임
8. [Maintainer retrieval·runtime·cursor 계약](records/2026-08-17-05-maintainer-retrieval-runtime-and-cursor-contract.md): 선택적 records 조회, 재사용 수명 경계, response-end event와 processing cursor
9. [Response-end Observe runtime과 live smoke](records/2026-08-17-06-response-end-observe-runtime-and-live-smoke.md): repo-local event protocol 구현, 내부 test와 실제 hook 실패, proof ceiling과 다음 결정
10. [Reference 소유권 정정과 재계획 handoff](records/2026-08-17-07-reference-ownership-correction-and-handoff.md): 사용자의 `ai-system` reference 정정, root-only 배치 오해, 현재 미커밋 상태와 다음 세션의 재계획 커서
11. [세션형 Maintainer 동작과 Reference 구현 계획](records/2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md): 자연스럽게 이해를 유지하는 세션 agent, 초기 sync·보고·복구와 Reference 전체 구현 순서

## 범위

- Recover·Verify·Maintain의 일상 활성 시점과 비용 상한
- `current/records` freshness가 세션 인계에 미치는 영향
- background maintainer의 관찰 입력, 자동 쓰기 allowlist, memory 승격·압축, 애매한 항목 보고 방식
- Main이 수행한 test·eval·수동 확인 중 지속할 증거를 Verify가 가볍게 보존하는 경계
- response-end event, Maintainer 재사용·rebootstrap 경계, delta 전달과 processing cursor
- Reference Project의 세션형 Maintainer·conditional write·축소 Verify 구현과 root dogfood
- 새 Reference 구현을 다른 Project에 이식하는 `apply-context-harness` 갱신
- timing flake와 중복 검증을 별도 운영 결함으로 다루는 방법

## 현재 범위 밖

- Recover·Verify·Maintain 제거
- 근거 없이 Recover의 역할 자체를 확대하는 변경
- Product context 구조나 기존 historical record의 재작성
- 자동 기록이 사람 acceptance를 대신하도록 만드는 것
- Global `ai-system_*` shared reference 수정

Workspace 004는 Reference 책임 재배치와 skill 간소화 이력을 소유한다. 이 Workspace는 그 구현을 복제하지 않고, 일상 작업에서 지속 context를 신뢰 가능하게 유지하는 운영 문제만 이어받는다.
