# Payment Recovery Project 적용·검증 기록

날짜: `2026-08-13`
대상: `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`
적용 원본: `/Users/hammyeong-yeon/Desktop/context-harness/output`
결과: 구조 적용·고정 자동 검증·재진입 완료, 사람의 acceptance와 브라우저 검증 대기

## 근거의 권위

- 사용자 선택: 적용 대상과 원본, 기존 untracked `context/code-map.md`의 직접 삭제
- 대상 Project canonical: 루트 `README.md`, `docs/product-brief.md`, `docs/architecture.md`, `docs/failure-scenarios.md`, `docs/roadmap.md`, `STATUS.md`
- machine evidence: Workspace `status.json`, recover 출력, 네 개의 append-only verify receipt와 별도 Harness test receipt
- 적용 설명: 대상 Workspace의 `records/2026-08-13-01-context-harness-application.md`; Project canonical이나 사용자 판단을 대신하지 않는다.
- 사용자 판단 대기: 실제 브라우저 결과에 따른 acceptance와 이후 commit·Project canonical 반영 여부

## 적용 전 경계

- 대상 기준 branch는 `feat/payment-recovery-mvp`, 적용 전·점검 시 HEAD는 `76d8e2f7072f9e428446b828293b768e1be95106`다.
- `apps/checkout-web/src/App.tsx`, `apps/checkout-web/src/styles.css`는 적용 전에 존재한 미커밋 사용자 작업이며 Harness 적용에서 수정하지 않았다.
- `context/code-map.md`도 적용 전에는 untracked 개인 이해용 파일이었다. 사용자가 적용 진행 중 직접 삭제했고 점검 시 실제 파일이 없음을 확인했다. 이는 Harness가 삭제한 파일이나 복구할 손실이 아니다.
- 적용 원본 기준 commit은 대상 migration record에 `3efc1abb6d57099d939efc1688c9345228a4b68b`로 기록돼 있다.

## 대상에 맞춘 배치

- 기존 Project canonical이 공통 기준을 계속 소유하며 `context/project/` 복제본을 만들지 않았다.
- repo-local `AGENTS.md`와 `context/README.md`에서 Project context Owner, Work context, 재진입·검증 경계를 찾게 했다.
- `context/work/workspaces/001-payment-recovery-mvp/`가 현재 Checkout 작업의 memory, state, records를 소유한다.
- `context/work/harness/`는 공용 recover·verify 장치이며 Project 기준이나 Workspace 의미를 소유하지 않는다.
- `.gitignore`에는 Python Harness가 만드는 `__pycache__/`, `*.py[cod]`를 제외하는 규칙을 추가했다.
- Reference recover schema `2`의 `context/project/` 고정을 대상용 schema `3`으로 바꿨다. Project-root 상대 경로 중 선언된 Project context인 루트 `README.md`, `STATUS.md`, `docs/` 아래 Markdown만 선택할 수 있고, `context/work/` records를 포함한 그 밖의 Markdown은 거부한다. 상대 경로·일반 파일·Markdown 제약과 symlink·path traversal 거부도 유지했다.

## 복구와 Harness 계약 검증

- 이 Project context 허용 경계를 강화한 뒤 Harness 계약 테스트는 recover 13개와 verify 9개, 총 22개가 다시 통과했다.
- `harness-test-20260813T145527463Z.json`은 Harness Python source 14개의 SHA-256과 byte size를 실행 전에 캡처하고 같은 source에 대한 unittest 22개의 exit `0`과 요약 `OK`를 보존했다. 이 receipt는 대상의 `context/work/workspaces/001-payment-recovery-mvp/records/`에 있다.
- 강화 후 점검 시 `python3 -B -m context.work.harness recover --json`을 다시 실행한 결과 Workspace memory 4개, state 2개와 다음 Project 문서 3개만 `loaded_context_paths`에 포함됐다.
  - `docs/product-brief.md`
  - `docs/architecture.md`
  - `docs/failure-scenarios.md`
- recover는 최종 receipt와 machine status도 control path와 state로 연결했다. `context/code-map.md`, `STATUS.md`, `docs/roadmap.md`, `verify.json`, records 전체는 기본 recovery context에 포함되지 않았다.

## Verify 시도와 보존 증거

1. `verify-20260813T143912287127Z-74eb79792d5947d7b4a217ec29f329fe.json`
   - 실행 환경에서 `pnpm`을 찾지 못해 exit `127`로 실패했다.
   - 제품 검증 실패가 아니라 argv 실행 전 환경 실패이며, 13개 evidence 파일은 실행 전에 보존됐다.
2. `verify-20260813T143935744895Z-3e0c54278b6f4393bd49c5d6ad76b321.json`
   - exit `0`, Turbo task 11개가 통과했다.
   - 11개 중 10개가 cache replay여서 fresh 실행 증거로는 부족했다.
3. `verify-20260813T144012148214Z-eb3ac3f5a7464ac3adffc09cc55c40a9.json`
   - `verify.json`의 argv에 `--force`를 추가한 뒤 exit `0`으로 통과했다.
   - Turbo task 11개 전부 실제 실행했고 cache는 `0/11`이었다.
   - 5개 test file의 31개 test, typecheck와 Checkout production build가 통과했다.
   - 13개 evidence 파일을 실행 전에 SHA-256과 byte size로 보존했다.
   - timeout이 없고 stdout·stderr truncation도 없었다.
   - 이후 독립 검토에서 13개 evidence가 11개 Turbo task 전체 입력을 대표하지 못한다고 확인돼 최종 증거로 삼지 않았다.
4. `verify-20260813T145622224711Z-3ae6506658144b86a437c45d9d39e4e1.json`
   - `verify.json`의 `evidence_paths`를 실제 Turbo 대상 5개 package의 source·README·package manifest·TypeScript/Vite 설정과 root package·lock·workspace·Turbo·TypeScript 설정을 합친 40개로 확대했다.
   - 40개 파일의 SHA-256과 byte size를 실행 전에 보존했다.
   - Turbo task 11개 전부 실제 실행했고 cache는 `0/11`이었다.
   - 5개 test file의 31개 test, typecheck와 Checkout production build가 통과했다.
   - exit `0`, timeout 없음, stdout·stderr truncation 없음이 확인됐다.

최종 receipt는 대상의 `context/work/workspaces/001-payment-recovery-mvp/records/verify-20260813T145622224711Z-3ae6506658144b86a437c45d9d39e4e1.json`에 있다. 최종 status는 `verified_waiting_acceptance`이고, 후속 recover가 이 receipt와 갱신 상태를 다시 불러왔다. Harness source와 제품 고정 검증 입력에 대한 durable 증거 부족은 이 Harness test receipt와 네 번째 verify receipt로 해소됐다.

## 증명한 범위와 남은 판단

이번 적용은 기존 Project canonical의 선택적 복구, 실행 전 source hash가 연결된 Harness 계약 검증, 40개 입력 snapshot에 대한 고정 typecheck·test·Checkout build, 실패·성공 receipt 누적, machine status 갱신과 갱신 상태의 재복구를 확인했다.

다음 범위는 아직 증명하지 않았다.

- 실제 브라우저에서 외부 결제 화면 승인·취소, focus 복귀, 모바일 표시와 승인 응답 유실 자동 복구
- 실제 PG, 영속 DB, Android WebView, 웹훅, 운영 서비스 효과
- Workspace 생성·전환·완료·보관, 결과의 Project canonical 반영 승인, concurrent verify, receipt와 status의 단일 transaction
- 사람의 acceptance와 이후 commit 여부

다음 안전 행동은 최종 receipt의 evidence 범위를 검토한 뒤 브라우저 동작을 직접 실행하고, 그 결과로 사용자가 acceptance를 결정하는 것이다. 자동 검증 통과만으로 완료나 수락을 선언하지 않는다.
