# Workspace current state

## 현재 문제

config loader가 Project의 default-timeout 결정과 일치하는지 고정 검증으로 확인하고, 통과 결과를 사람이 수락할지 결정한다.

## 상태를 읽는 법

- 최근 검증 결과, receipt, 완료 시각, 다음 행동의 정본은 [`status.json`](status.json)이다.
- 검증의 stdout·stderr와 evidence hash는 status가 가리키는 `records/receipts/verify/` receipt에서 확인한다. 이전 flat `records/*.json`도 과거 호환 경로다.
- 이 문서는 사람이 현재 문제와 해석 경계를 읽도록 유지하며 harness가 자동으로 고치지 않는다.

## 해석 경계

검증 통과는 구현과 선택된 Project 기준이 현재 테스트에서 일치한다는 뜻이다. 사람의 수락, Workspace 완료, 운영 서비스 효과를 뜻하지 않는다.
