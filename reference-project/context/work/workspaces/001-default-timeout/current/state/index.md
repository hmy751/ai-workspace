# Workspace current state

## 현재 문제

config loader가 Project의 default-timeout 결정과 일치하는지 고정 검증으로 확인하고, 통과 결과를 사람이 수락할지 결정한다.

## 상태를 읽는 법

- 최근 검증 결과, receipt, 완료 시각의 기계 정본은 [`status.json`](status.json)이다.
- 검증의 claim, stdout·stderr, canonical basis·evidence hash는 status가 가리키는 `records/receipts/verify/` receipt에서 확인한다. Recover는 현재 schema receipt의 선언된 snapshot이 지금도 같은지 `fresh` 또는 `stale`로 요약하고, 과거 schema receipt는 `unknown_legacy`로 표시한다.
- 다음 행동과 사람의 해석은 이 문서가 소유하며 Harness가 자동으로 고치지 않는다.

## 해석 경계

검증 통과는 receipt에 snapshot된 canonical basis·evidence 조건에서 고정 argv가 exit `0`을 반환했다는 기계 사실이다. Claim의 의미적 충분성, 사람의 수락, Workspace 완료, 운영 서비스 효과를 뜻하지 않는다.

Project context가 `common/current/guidance` 물리 layer로 이동해 기존 receipt가 snapshot한 평면 Project 경로는 현재 존재하지 않는다. 따라서 Recover가 계산하는 현재 freshness는 `stale`이고, `status.json`의 `verification_passed`는 당시 마지막 실행 결과로 그대로 보존한다. 새 경로 기준의 durable 제품 Verify는 사람의 상태 전환·인계에 필요할 때 별도 실행한다.
