# Harness maintenance bottleneck memory

마지막 갱신: `2026-08-14`

## 목표

Context+harness의 안전성과 재진입 가능성은 유지하면서, 작은 변경이 과도한 문서 갱신·Workspace 정합화·검증·review로 번지는 유지보수 비용을 줄인다.

## 유지할 기준

- 실제 실행 계약의 Owner와 이식 절차, 적용 이력의 Owner를 구분한다.
- 확인하지 않은 의미 정확성, 외부 동작, 사람 acceptance를 구조 테스트만으로 증명했다고 말하지 않는다.
- 사용자 변경, 기존 canonical, append-only evidence를 속도 개선을 이유로 덮어쓰거나 삭제하지 않는다.
- Current는 다음 행동에 필요한 현재 정보만 유지하고, 상세 과정은 records에 남긴다.
- Historical record는 당시 사실로 보존하며 현재 계약을 다시 설명하는 정본으로 사용하지 않는다.
- 검증 강도는 변경 위험에 비례시킨다. 반복 개발 확인과 상태 전환용 durable verify를 구분한다.
- Context 이동·링크·설명 정리처럼 실행 의미를 바꾸지 않는 작업은 필요한 경로·링크·diff만 확인한다. 모든 이동에 full runtime test, durable verify, 독립 review를 일괄 적용하지 않는다.
- Schema, 실행 코드, evidence 범위, path 방어, 사용자 파일 보존처럼 실패 영향이 큰 변경만 검증 범위를 단계적으로 넓힌다. Main이 변경 성격을 판단해 가장 작은 충분한 확인부터 시작한다.

## 현재 범위

- 기준 Project의 실행 계약이 어디서 canonical이어야 하는지
- Skill에 반드시 남겨야 하는 이식 판단과 reference를 가리키기만 해도 되는 내용
- Outer Workspace current·records가 실제 현재 상태만 소유하도록 줄일 수 있는 중복
- Context maintainer와 독립 review를 언제 병렬화하거나 생략할 수 있는지
- Runtime 변경, 문서·경로 변경, historical link migration에 필요한 검증 강도의 차이

## 범위 밖

- Recover·verify 제거
- Receipt 증거 또는 path 안전성 약화
- 사람 acceptance 자동화
- 현재 Payment target 재적용
- Workspace 전체 lifecycle을 한 번에 새로 설계하는 작업

## 접근점

- 실행 가능한 기준 Project: [`reference-project/README.md`](../../../../reference-project/README.md)
- 이식 절차: [`apply-context-harness/SKILL.md`](../../../../.agents/skills/apply-context-harness/SKILL.md)
- 직전 machine receipt 변경 기록: [`001 record`](../../001-reference-implementation/records/2026-08-14-05-machine-receipt-boundary-and-durable-verify.md)
- 실제 target 이식 계약 기록: [`002 record`](../../002-project-application/records/2026-08-14-07-target-machine-receipt-boundary-contract.md)
