# Machine receipts

이 폴더는 Default timeout Workspace를 대상으로 기계가 생성한 append-only 증거를 종류별로 보존한다. 생성 코드는 Harness에 있지만 receipt의 의미와 수명주기는 이 Workspace가 소유한다.

- [`verify/`](verify/): 제품 고정 검증의 claim, 실행 전 canonical basis·evidence snapshot, argv, bounded runtime, exit, 제한된 stdout·stderr
- `harness-tests/`: 이식 과정에서 별도의 durable Harness 검증 증거가 필요할 때 사용. Reference 자체 회귀는 임시 fixture test가 맡으므로 active 제품 Workspace에 만들지 않는다.
- `preflight/`: 이식 직전 target 상태를 캡처한 원본 receipt를 보존할 때 사용

빈 종류 폴더는 미리 만들지 않아도 된다. Product `verify`를 실행하려면 `verify/`가 symlink가 아닌 실제 디렉터리로 존재해야 한다. `current/state/status.json`은 최신 제품 verify receipt를 Work-root 상대 경로로 가리키며 사람의 다음 행동은 소유하지 않는다. 과거 schema v1 receipt는 그대로 보존하고, 새 schema v2 receipt부터 claim과 declared snapshot freshness를 다시 확인할 수 있다.
