# Machine receipts

이 폴더는 Default timeout Workspace를 대상으로 기계가 생성한 append-only 증거를 종류별로 보존한다. 생성 코드는 Harness에 있지만 receipt의 의미와 수명주기는 이 Workspace가 소유한다.

- [`verify/`](verify/): 과거 `verify-*` 제품 실행 receipt와 새 `evidence-*` 기록을 함께 보존한다. 새 receipt는 이미 수행된 test·eval·수동 확인의 생산자, 대상, 방법, 보고 결과, source reference, 미확인 범위를 담는다.
- `harness-tests/`: 이식 과정에서 별도의 durable Harness 검증 증거가 필요할 때 사용. Reference 자체 회귀는 임시 fixture test가 맡으므로 active 제품 Workspace에 만들지 않는다.
- `preflight/`: 이식 직전 target 상태를 캡처한 원본 receipt를 보존할 때 사용

빈 종류 폴더는 미리 만들지 않아도 된다. Verify evidence recorder는 이 실제 `receipts/` parent 아래에 자기 소유 `verify/` leaf가 없으면 안전하게 만든다. 기존 `verify/`가 symlink면 기록을 거부한다. `current/state/status.json`은 호환을 위해 과거 `verify-*` 제품 receipt만 Work-root 상대 경로로 가리킬 수 있고, 새 `evidence-*` receipt를 가리킬 수 없다. 과거 schema v1·v2 receipt와 status는 그대로 보존하며 새 evidence 기록으로 다시 쓰지 않는다.
