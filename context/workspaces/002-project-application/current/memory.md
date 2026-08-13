# Project application memory

마지막 갱신: `2026-08-13`

## 목표

실제 기존 Project 하나에서 사람과 AI가 Project 공통 맥락과 진행 중인 작업 상태를 복구하고, 필요한 정보만 선택해 행동하며, 검증 결과를 다시 지속 상태에 반영하는 흐름을 적용·검증한다.

## 대상과 적용 결정

- 적용 원본은 이 저장소의 [`output/`](../../../../output/)이고, 대상 Project는 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`다.
- 대상의 기존 `README.md`, `docs/product-brief.md`, `docs/architecture.md`, `docs/failure-scenarios.md`, `docs/roadmap.md`, `STATUS.md`가 Project common context를 계속 소유한다. 별도 `context/project/` 복제본을 만들지 않는다.
- 대상에는 repo-local `AGENTS.md`, `context/README.md`, 교체 가능한 `context/work/harness/`, `context/work/workspaces/001-payment-recovery-mvp/`를 적용했다.
- 대상용 recover schema `3`은 Project-root 상대 경로 중 선언된 Project context인 루트 `README.md`, `STATUS.md`, `docs/` 아래 Markdown만 선택할 수 있다. `context/work/` records를 포함한 그 밖의 Markdown은 거부한다. 기본 복구 대상은 `docs/product-brief.md`, `docs/architecture.md`, `docs/failure-scenarios.md` 세 개다.
- 적용 전 미커밋 사용자 작업 `App.tsx`, `styles.css`는 수정하지 않았다. 적용 전 존재하던 untracked `context/code-map.md`는 사용자가 적용 진행 중 직접 삭제해 현재 없으며, Harness가 삭제했거나 복구할 손실이 아니다.
- Harness가 없어져도 기존 Project canonical과 Workspace의 README·current·records 의미가 남아야 한다.

## 검증 상한

- 구조와 선택적 복구, 고정 typecheck·test·Checkout build, receipt 누적, machine status 갱신과 후속 재복구까지 확인했다.
- Harness 계약 22개 통과는 실행 전 Python source 14개의 SHA-256·byte size와 함께 별도 receipt에 보존됐다. 제품 고정 검증은 실제 Turbo 대상 5개 package의 source·manifest·설정과 root 실행 설정 40개의 실행 전 hash를 포함한다. 이로써 Harness source와 고정 검증 입력에 대한 durable 증거 부족은 해소됐다.
- 최종 자동 검증 통과는 로컬 Mock PG vertical slice의 고정 evidence snapshot에 한정된다. 실제 브라우저 승인·취소·focus 복귀·모바일 표시, 실제 PG·영속 DB·Android WebView·웹훅·운영 효과, 사람의 acceptance는 증명하지 않는다.
- 자동 검증 통과 상태 `verified_waiting_acceptance`는 Workspace 완료나 사용자 수락을 뜻하지 않는다.

## 접근점

- 이 Workspace의 상세 적용·검증 기록: [`2026-08-13-01-payment-recovery-project-application.md`](../records/2026-08-13-01-payment-recovery-project-application.md)
- 대상 진입점: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio/AGENTS.md`
- 대상 current: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio/context/work/workspaces/001-payment-recovery-mvp/current/`
- 대상 migration record: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio/context/work/workspaces/001-payment-recovery-mvp/records/2026-08-13-01-context-harness-application.md`
- 대상 Harness test receipt: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio/context/work/workspaces/001-payment-recovery-mvp/records/harness-test-20260813T145527463Z.json`
- 대상 최종 verify receipt: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio/context/work/workspaces/001-payment-recovery-mvp/records/verify-20260813T145622224711Z-3ae6506658144b86a437c45d9d39e4e1.json`
