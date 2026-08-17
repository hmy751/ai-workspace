# Context continuity maintenance Workspace

Main과 사용자의 실제 작업을 막지 않으면서 `current/records`를 다음 세션이 믿고 이어 갈 만큼 유지하는 운영 방식을 구체화하는 Workspace다. Recover·Verify·Maintain을 없애는 작업이 아니라, 각 책임을 언제 어떤 강도로 실행하고 background maintainer에 어디까지 직접 쓰기 권한을 줄지 정한다.

상태는 **active**다. 이 작업은 사용자가 “수정 작업들이 30분, 26분처럼 오래 걸린 이유”를 물은 시점부터 시작한다. 진단과 사용자 판단은 보존했지만 background agent나 새 runtime은 아직 구현하지 않았다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 사용자 우선순위, 유지할 역할 경계와 이미 선택된 방향
2. [`current/state.md`](current/state.md): 현재 설계 커서, 미결정점과 바로 이어서 물을 질문
3. [`output/index.md`](output/index.md): 현재 선택된 진단·설계 산출물과 구현되지 않은 경계
4. [운영 지연과 역할 진단](records/2026-08-17-01-harness-operation-latency-and-role-diagnosis.md): 30분·26분 문제의 비용 분해, Recover·Verify·Maintain의 실제 동작과 flake
5. [Context continuity와 background maintenance framing](records/2026-08-17-02-context-continuity-and-background-maintenance-framing.md): 현업 자료 대조, 사용자 C/E 우선순위, 자동 기록 조건과 열린 질문
6. [응답 종료 점검과 갱신 계약](records/2026-08-17-03-response-end-maintenance-contract-and-verify-reopening.md): 매 응답 점검, 자동 갱신 범위, ambiguity 보고와 다시 열린 Verify 논의
7. [Verify 증거 기록 경계](records/2026-08-17-04-verify-evidence-recording-boundary.md): 기존 Verify의 목적 재검토와 가벼운 증거 수집·기록 보조로 축소한 책임
8. [Maintainer retrieval·runtime·cursor 계약](records/2026-08-17-05-maintainer-retrieval-runtime-and-cursor-contract.md): 선택적 records 조회, 재사용 수명 경계, response-end event와 processing cursor

## 범위

- Recover·Verify·Maintain의 일상 활성 시점과 비용 상한
- `current/records` freshness가 세션 인계에 미치는 영향
- background maintainer의 관찰 입력, 자동 쓰기 allowlist, memory 승격·압축, 애매한 항목 보고 방식
- Main이 수행한 test·eval·수동 확인 중 지속할 증거를 Verify가 가볍게 보존하는 경계
- response-end event, Maintainer 재사용·rebootstrap 경계, delta 전달과 processing cursor
- timing flake와 중복 검증을 별도 운영 결함으로 다루는 방법

## 현재 범위 밖

- background daemon·hook·agent runtime 구현
- Recover·Verify·Maintain 제거
- Workspace 004의 최신 `apply-context-harness` 교정 재시험
- Product context 구조나 기존 historical record의 재작성
- 자동 기록이 사람 acceptance를 대신하도록 만드는 것

Workspace 004는 Reference 책임 재배치와 skill 간소화 이력을 소유한다. 이 Workspace는 그 구현을 복제하지 않고, 일상 작업에서 지속 context를 신뢰 가능하게 유지하는 운영 문제만 이어받는다.
