# Target machine receipt 경계 계약

기록일: `2026-08-14`

## 작업 범위

Repo-local `apply-context-harness` skill이 새 target Workspace의 사람이 읽는 records와 machine receipt를 분리하도록 이식 계약을 갱신했다. 이번 작업에서는 원본 Payment target이나 격리 평가 target을 열거나 재이식하지 않았고, 기존 payment 적용 기록과 당시 flat receipt 경로도 변경하지 않았다.

## 새 이식 계약

- Target Workspace의 `records/` 바로 아래에는 날짜가 있는 사람이 읽는 분석·결정·migration·검증 해석을 둔다.
- 기계가 만든 append-only JSON은 `records/receipts/` 아래 `preflight/`, `harness-tests/`, `verify/`로 종류를 분리한다.
- Harness와 helper는 receipt producer다. Receipt가 증명하는 작업과 보존 수명주기의 Owner는 해당 target Workspace다.
- 새 product verify는 `records/receipts/verify/`에만 쓴다. 이전 target의 flat `records/*.json`은 status와 recover가 읽을 수 있게 호환하되 새로 만들지 않는다.
- 반복 개발 확인은 직접 test 명령으로 수행한다. Product `verify`는 Workspace 상태를 전환하거나 다음 사람·세션에 durable evidence를 인계할 때 실행한다.
- 실행된 성공·실패 receipt는 하나의 사건이므로 같은 결과나 evidence hash라는 이유로 자동 삭제·병합하지 않는다.

## Skill과 reference 반영

- Dry-run manifest는 target에 만들 `records/README.md`, `records/receipts/README.md`와 세 receipt 종류를 밝힌다.
- Preflight 임시 receipt는 target의 `records/receipts/preflight/`에 byte-identical copy로 보존한다.
- Target-specific Harness test helper는 `records/receipts/harness-tests/`에 source hash와 unittest 결과를 남긴다.
- Product verify 전에는 `records/receipts/verify/`가 symlink가 아닌 실제 디렉터리인지 확인한다.
- Reference verify는 새 receipt를 nested `verify/`에 쓰고, recover는 nested 경로와 기존 flat 경로를 모두 읽는다.

## 검증

### Reference와 helper

- `reference-project/` 전체 unittest: 40개 통과
  - recover: 22개
  - verify: 11개
  - 제품 config loader: 7개
- Skill helper unittest: 현재 Python `3.14.3`에서 7개 통과
- Skill helper unittest: `/usr/bin/python3` Python `3.9.6`에서 7개 통과
- Skill validator: `Skill is valid!`

### Live nested reference cycle

- Product verify: 제품 테스트 7개 통과, exit `0`, 제품 코드와 테스트 2개를 실행 전에 hash
- 최신 nested receipt: [`verify-20260814T070729765148Z-4de3a77434444335b088d4944631e94f.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260814T070729765148Z-4de3a77434444335b088d4944631e94f.json)
- Machine status: 같은 receipt를 가리키는 `verified_waiting_acceptance`
- 후속 recover: packet schema `5`, current 6개·output index 1개·Project 문서 2개를 loaded context로 복구하고 nested receipt는 control path로만 연결

## Payment target 경계

- 원본 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`의 마지막 직접 확인 상태는 branch `feat/payment-recovery-mvp`, HEAD `9519a43`, clean·Harness 미설치다. 이번 skill 변경에서는 이를 다시 열어 갱신하지 않았다.
- 첫 적용 snapshot commit `eaacec7`과 격리 blind 평가가 보존한 machine receipt는 당시 계약의 flat `records/*.json` 또는 `records/` root 배치다.
- 이번 변경은 기존 payment 기록이나 target 파일을 nested layout으로 자동 migration하지 않았다. Flat path를 적은 historical record는 당시 사실이므로 그대로 유지한다.
- 격리 target의 마지막 관찰 상태도 이번에 재확인하지 않았다. 새 receipt 계약의 target 적용 증거로 해석하지 않는다.

## 검증 상한

- Reference의 nested cycle은 새 producer 경계와 호환을 확인하지만 Payment target의 현재 설치 상태나 target-specific 경로를 검증하지 않는다.
- 실제 Payment target에 새 `context/project/`·schema `4`·nested receipts를 적용한 `recover → verify → recover`는 수행하지 않았다.
- Direct helper tests는 반복 확인이며 Payment Workspace의 durable receipt나 상태 전환을 만들지 않는다.
- 자동 retention, concurrent verify, receipt와 status의 단일 transaction, 사람 acceptance는 구현하거나 확인하지 않았다.
