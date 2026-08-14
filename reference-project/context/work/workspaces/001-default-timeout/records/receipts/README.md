# Machine receipts

이 폴더는 Default timeout Workspace를 대상으로 기계가 생성한 append-only 증거를 종류별로 보존한다. 생성 코드는 Harness에 있지만 receipt의 의미와 수명주기는 이 Workspace가 소유한다.

- [`verify/`](verify/): 제품 고정 검증의 실행 전 evidence hash, argv, exit, 제한된 stdout·stderr
- `harness-tests/`: 이식 과정에서 target-specific Harness source와 unittest 결과를 보존할 때 사용
- `preflight/`: 이식 직전 target 상태를 캡처한 원본 receipt를 보존할 때 사용

빈 종류 폴더는 미리 만들지 않아도 된다. Product `verify`를 실행하려면 `verify/`가 symlink가 아닌 실제 디렉터리로 존재해야 한다. `current/state/status.json`은 최신 제품 verify receipt를 Work-root 상대 경로로 가리킨다.
