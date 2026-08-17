# Workspace current state

## 현재 문제

config loader가 Project의 default-timeout 결정과 일치하는지 실제 테스트 근거를 확인하고, 현재 결과를 사람이 수락할지 결정한다.

## 상태를 읽는 법

- [`status.json`](status.json)은 과거 제품 검증 실행기가 남긴 최근 결과, receipt, 완료 시각의 기계 정본이다. 새 Verify evidence 기록은 이 파일을 갱신하지 않는다.
- 과거 검증의 claim, stdout·stderr, canonical basis·evidence hash는 status가 가리키는 `verify-*` receipt에서 확인한다. Recover는 해당 receipt의 선언된 snapshot이 지금도 같은지 `fresh` 또는 `stale`로 요약하고, 과거 schema receipt는 `unknown_legacy`로 표시한다.
- 새 `evidence-*` receipt에는 이미 수행된 test·eval·수동 확인의 보고 결과와 확인하지 못한 범위가 들어간다. 이는 status의 제품 검증 근거가 아니며 Recover가 자동으로 읽지 않는다.
- 다음 행동과 사람의 해석은 이 문서가 소유하며 Harness가 자동으로 고치지 않는다.

## 해석 경계

과거 제품 검증 통과는 receipt에 snapshot된 canonical basis·evidence 조건에서 당시 고정 argv가 exit `0`을 반환했다는 역사적 기계 사실이다. 새 evidence의 `pass`는 생산자가 보고한 관찰 결과다. 어느 쪽도 의미적 충분성, 사람의 수락, Workspace 완료, 운영 서비스 효과를 뜻하지 않는다.
