# Context continuity maintenance Workspace

Main과 사용자의 실제 작업을 막지 않으면서 `current/records`를 다음 세션이 믿고 이어 갈 만큼 유지하는 운영 방식을 Reference의 실행 가능한 책임으로 완성하는 Workspace다. Recover·Verify·Maintain을 없애는 작업이 아니라, 각 책임을 분리한 채 세션형 Maintainer가 이미 얻은 이해를 재사용하고 durable 변화만 기존 Context Owner에 반영하게 한다.

상태는 **completed**이며 이번 구현 범위는 완료됐다. 재사용 가능한 Maintain runtime, semantic warm session, guarded writer와 축소 Verify evidence recorder는 `reference-project/`가 소유하고, 구현 commit 당시 root는 Workspace 005를 선택해 이를 dogfood하는 얇은 설정만 소유하도록 구성했다. 이전 root Observe runtime은 active 경로에서 제거했고 cross-session recovery wake, false-success·raw cleanup 결함과 전체 로컬 통합 재검증도 닫았다. 실제 nested Codex와 fresh host acceptance는 별도 승인 후에 proof ceiling을 좁히는 후속 검증이다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 사용자 우선순위와 구현이 보존해야 할 역할·동작 기준
2. [`current/state.md`](current/state.md): 완료된 구현 상태, 현재 proof ceiling과 별도 승인 뒤 가능한 후속 검증
3. [`output/index.md`](output/index.md): Reference canonical, root 연결 설정과 현재 선택된 기록의 위치
4. [Reference Maintain 구현과 proof](records/2026-08-18-09-reference-maintain-runtime-implementation-and-proof.md): 구현이 보존한 사용자 장면, recovery invariant와 아직 증명하지 않은 범위
5. [운영 지연과 역할 진단](records/2026-08-17-01-harness-operation-latency-and-role-diagnosis.md): 30분·26분 문제의 비용 분해, Recover·Verify·Maintain의 실제 동작과 flake
6. [Context continuity와 background maintenance framing](records/2026-08-17-02-context-continuity-and-background-maintenance-framing.md): 현업 자료 대조, 사용자 C/E 우선순위, 자동 기록 조건과 열린 질문
7. [응답 종료 점검과 갱신 계약](records/2026-08-17-03-response-end-maintenance-contract-and-verify-reopening.md): 매 응답 점검, 자동 갱신 범위와 ambiguity 처리
8. [Verify 증거 기록 경계](records/2026-08-17-04-verify-evidence-recording-boundary.md): 제품 검증 주체가 아닌 선택적 증거 기록 도구로 축소한 책임
9. [Maintainer retrieval·runtime·cursor 계약](records/2026-08-17-05-maintainer-retrieval-runtime-and-cursor-contract.md): 선택적 records 조회, 재사용 수명 경계, response-end event와 processing cursor
10. [Response-end Observe runtime과 live smoke](records/2026-08-17-06-response-end-observe-runtime-and-live-smoke.md): 첫 전달 실험, 내부 test와 실제 hook 실패 및 당시 proof ceiling
11. [Reference 소유권 정정과 재계획 handoff](records/2026-08-17-07-reference-ownership-correction-and-handoff.md): root-only 배치 오해와 Reference ownership 정정
12. [세션형 Maintainer 동작과 Reference 구현 계획](records/2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md): 자연스러운 지속 이해, 초기 sync·보고·복구와 승인된 구현 순서

## 범위

- 기존 Workspace의 bounded 초기 grounding과 같은 작업 세션 동안의 warm understanding
- 매 Main response-end의 background Maintain, no-write·조용한 반영·중요 반영 보고·ambiguity 질문
- forming Workspace의 no-write, 기존 Context Owner의 allowlist와 guarded multi-file write
- session별 event·cursor와 Workspace 전체 freshness·report handoff, retry·replay·rebootstrap·승인된 gap repair
- Main·제품 test·CI·eval·사람이 이미 수행한 확인만 기록하는 Verify와 legacy Recover 호환
- Reference Project의 재사용 구현과 root Workspace 005 연결 설정
- 새 Reference 구현을 다른 Project에 이식하는 `apply-context-harness` 갱신
- 실제 Codex host에서 확인해야 할 hook trust, warm thread, background·UI 전달의 proof ceiling

## 현재 범위 밖

- Recover·Verify·Maintain 제거
- 근거 없이 Recover의 의미 역할을 확대하거나 Maintain freshness를 machine status에 섞는 변경
- Product context 구조나 historical records 01–08의 재작성
- 자동 기록이나 evidence receipt가 사람 acceptance를 대신하게 만드는 것
- Maintainer가 Workspace 선택, Project canonical, stage·commit·push를 대신 결정하는 것
- Global `ai-system_*` shared reference 수정

Workspace 004는 Reference 책임 재배치와 skill 간소화 이력을 소유한다. 이 Workspace는 그 구현을 복제하지 않고, 일상 작업에서 지속 context를 신뢰 가능하게 유지하는 운영과 그 Reference 구현만 이어받는다.
