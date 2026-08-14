# Machine receipt 경계 분리

- 기록일: 2026-08-14
- 대상: Default timeout Workspace의 사람용 records와 기계 receipt 저장 경계

## 문제

기존 `records/` 바로 아래에는 날짜가 있는 사람이 읽는 기록 4개와 product verify JSON 10개가 함께 있었다. Recover가 records 전체를 context로 읽지는 않았지만, 같은 제품 evidence를 반복 검증한 receipt가 사람용 기록보다 많아져 폴더 탐색과 Git 변경 확인이 어려워졌다.

Harness가 receipt를 생성한다는 이유로 공용 `context/work/harness/` 아래로 옮기면 Workspace별 증거가 섞이고, 교체 가능한 Harness를 제거할 때 작업 증거의 수명주기도 함께 흔들린다. 생성 주체와 보존 Owner를 분리해야 했다.

## 결정

- Receipt가 증명하는 작업과 보존 수명주기의 Owner는 해당 Workspace로 유지한다.
- 사람이 읽는 분석·결정·migration·검증 해석은 `records/` 바로 아래 날짜별 Markdown에 둔다.
- 기계 JSON은 [`receipts/`](receipts/README.md) 아래 `verify/`, `harness-tests/`, `preflight/`로 종류를 분리한다.
- Product verify의 새 receipt는 `records/receipts/verify/`에만 쓴다.
- 이전 flat `records/*.json` 경로는 기존 target과 receipt를 읽기 위한 호환 경계로 유지한다.
- 반복 개발 확인은 직접 test 명령을 사용하고, durable verify는 Workspace 상태 전환이나 다음 사람·세션에 근거를 인계할 때 실행한다.

이 변경은 실행된 receipt를 자동 삭제하거나 같은 hash끼리 합치지 않는다. 폴더 분리는 탐색 책임을 바로잡고, 직접 test와 durable verify의 운용 구분은 불필요한 새 receipt 생성을 줄인다. Retention 자동화는 별도 문제로 남긴다.

## 구현과 migration

- 기존 verify JSON 10개는 내용 변경 없이 [`receipts/verify/`](receipts/verify/)로 이동했다.
- Verify는 새 목적지 디렉터리가 없거나 symlink면 제품 명령을 실행하기 전에 실패한다.
- Status와 recover의 same-Workspace `records/` containment는 중첩 경로를 그대로 허용한다.
- 기존 flat 경로와 새 nested 경로를 각각 recover하는 회귀 테스트를 유지한다.
- Receipt schema `1`, status schema `2`, recover contract schema `4`, recovery packet schema `5`는 의미와 shape가 바뀌지 않아 유지했다.

## 검증

- Reference 전체 unittest: 40개 통과
- Skill helper unittest: 7개 통과
- Skill validator: valid
- 이동 직후 사전 recover: 기존 status가 옮겨진 receipt를 nested path에서 다시 확인
- Live verify: 제품 테스트 7개 통과, exit `0`, evidence 2개를 실행 전에 hash하고 [새 nested receipt](receipts/verify/verify-20260814T070729765148Z-4de3a77434444335b088d4944631e94f.json)에 보존
- 후속 recover: packet schema `5`, current 6개, output index 1개, Project 문서 2개를 로드하고 새 receipt를 control path로 연결

## 증명 상한

이 검증은 새 receipt 목적지, 이전 flat 경로 호환, missing·symlink 목적지의 명령 실행 전 거부, status와 recover 연결을 확인한다. Concurrent verify와 receipt/status의 단일 transaction, 자동 retention, 사람의 acceptance, 실제 네트워크나 운영 서비스 효과는 확인하지 않는다.
