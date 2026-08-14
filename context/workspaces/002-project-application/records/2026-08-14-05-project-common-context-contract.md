# Project common context와 recover 계약 변경

기록일: `2026-08-14`

## 변경 이유

첫 Payment Recovery 적용과 격리 blind 평가는 기존 루트 `README.md`, `STATUS.md`, `docs/`를 Project common Owner로 두고 별도 `context/project/`를 만들지 않았다. 이 배치는 기존 상세 문서를 보존했지만, 여러 Workspace가 공통 맥락을 실제 내용으로 복구하는 물리 진입점을 target에 남기지 않았다.

사용자 정정에 따라 현재 [`reference-project/`](../../../../reference-project/)는 이식 뒤 도착해야 할 책임을 실행하는 기준 Project, repo-local [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/) skill은 target을 그 상태로 옮기는 절차, target의 `context/project/`는 해당 Project의 실제 공통 맥락을 소유하는 것으로 역할을 다시 분리했다.

## 채택한 Project context 계약

완료된 target에는 다음 두 파일이 있어야 한다.

- `context/project/README.md`: Project context 층의 책임, 기존 상세 Owner, 충돌 우선순위와 overview 갱신 조건
- `context/project/overview.md`: 실제 사용자 장면과 제품 목적, 범위와 범위 밖, 주요 시스템 흐름·구성요소, 여러 Workspace에 계속 적용되는 제약·채택 결정, 검증·사람 acceptance 경계와 근거 path

기존 루트 `README.md`, `STATUS.md`, `docs/`, 코드와 테스트는 상세 사실의 domain canonical로 보존한다. Overview는 기존 문단의 복사본이나 링크 목록으로 끝내지 않고 여러 Owner에서 Workspace 공통 판단에 필요한 내용을 target 사실로 구성한다. 상세 Owner와 충돌하면 상세 Owner가 우선하며 overview는 stale로 판정해 다시 대조한다. 기존 Owner 자체를 `context/project/`로 옮기는 것은 별도 승인된 Owner migration이다.

Exact baseline commit과 dirty state는 overview가 아니라 preflight receipt와 migration record가 소유한다. 한 Workspace의 현재 목표·상태·검증 이력을 Project 전체 사실로 승격하지 않는다.

이 계약은 [`application-contract.md`](../../../../.agents/skills/apply-context-harness/references/application-contract.md)와 [`SKILL.md`](../../../../.agents/skills/apply-context-harness/SKILL.md)에 이식 기준·완료 조건·독립 review 항목으로 반영됐다.

## Recover 계약

- Fresh target은 recover schema `4`를 사용한다.
- Project context 선택은 Project root의 `context/project/` 아래 regular Markdown으로 제한한다.
- `context/project/overview.md`를 첫 Project context 항목으로 요구한다.
- Recovery packet shape는 바뀌지 않아 packet schema `5`를 유지한다.
- Reference schema `2`와 첫 Payment Recovery 적용의 target-local schema `3`을 재해석하지 않는다. Schema `3`은 루트 `README.md`, `STATUS.md`, `docs/` Markdown을 직접 선택한 과거 계약이다.

구현과 실행 경계는 [`recover operation`](../../../../reference-project/context/work/harness/recover/operation.py)과 [`Project context README`](../../../../reference-project/context/project/README.md)에서 확인한다.

## 현재 검증

Source reference working tree에서 다음을 확인했다.

- 현재 `reference-project/`로 이름을 바꾼 당시 source root의 `python3 -m unittest discover -s . -p 'test_*.py' -v`: Harness와 제품 전체 37개 통과
- live verify: 제품 테스트 7개 통과, exit `0`, evidence 2개를 실행 전에 hash하고 [새 receipt](../../../../reference-project/context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260814T063043445861Z-0b38bf91d06f4edcb3d86d9ee1cb1bcd.json)에 보존
- 후속 recover: `context/project/overview.md`를 첫 Project context로 선택하고 decision 문서만 추가해 packet schema `5` 반환

이는 reference의 schema `4` validation, Markdown-only 경계, overview-first 선택과 기존 packet shape의 실행을 지지한다. Overview 내용이 임의 target 원자료와 의미상 맞는지, 이후 상세 Owner 변경에 따라 갱신되는지는 구조 테스트만으로 증명하지 않는다.

## 과거 평가와 새 계약의 경계

[첫 적용 기록](2026-08-13-01-payment-recovery-project-application.md)과 [blind 평가 기록](2026-08-14-04-blind-apply-context-harness-skill-evaluation.md)의 성공은 schema `3`과 기존 문서 직접 선택 계약에 대한 과거 증거다. 격리 target의 28개 Harness test, 제품 11개 task·31개 test·build, 독립 review가 통과했더라도 새 `context/project/README.md`·`overview.md`와 schema `4` 이식을 검증한 것으로 쓰지 않는다.

현재 원본 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`는 branch `feat/payment-recovery-mvp`, HEAD `9519a43`의 clean 상태이며 `AGENTS.md`와 `context/`가 없다. 따라서 현재 검증은 source reference에 한정되고 다음은 미검증이다.

- Payment Recovery 원자료에서 실제 Project common overview를 구성하고 상세 Owner와 대조하는 과정
- 원본 또는 격리 target에 새 계약을 적용한 `recover → verify → recover`
- target-specific 독립 review, commit, 사람 acceptance
- 다른 실제 Project portability와 외부 결제 동작·운영 효과

원본 재적용과 격리 파일 처리는 사용자 결정을 기다린다. 재적용한다면 이전 schema `3` 결과를 이어 쓰지 않고 새 preflight, migration record, Harness receipt와 product receipt를 만든다.
