# Current state

마지막 갱신: `2026-08-13`

## 현재 문제

`output/`에 구현하고 실제 검증한 첫 Project–Workspace reference가 목표와 합의한 경계를 충족하는지 사용자가 검토하고 수락할 단계다.

## 현재 상태

- `output/`에 request timeout config를 다루는 실제 Project 코드·문서·테스트와 `memory/state/records` Workspace, 선택적 복구·고정 검증·receipt/state 반영 harness를 구현했다. 상세 구성과 검증은 [`첫 output 구현 기록`](../records/2026-08-13-04-first-output-reference.md)에 있다.
- 의도적 불일치로 만든 실패와 코드 수정 뒤 성공이 각각 receipt와 state에 반영됐고, 후속 recovery가 갱신된 상태와 다음 행동을 복구했다.
- 독립 검증에서 발견한 receipt 연결 검증, subprocess 제한, 로컬 경로 보존 문제를 보완했다. 제품 7개와 harness 10개를 합친 17개 unittest가 통과했고, 보완된 runtime으로 fail→pass receipt와 recovery를 다시 확인했다.
- output Workspace는 검증 통과를 완료로 자동 승격하지 않았으며, 현재 사용자 수락을 기다린다.

## 현재 필요한 접근점

- Project–Workspace context 합의: [`../records/2026-08-13-03-project-workspace-context-agreement.md`](../records/2026-08-13-03-project-workspace-context-agreement.md)
- 첫 output 구현과 실제 검증: [`../records/2026-08-13-04-first-output-reference.md`](../records/2026-08-13-04-first-output-reference.md)
- 실행 가능한 output: [`../../output/README.md`](../../output/README.md)

## 불확실성과 검증 상한

- 사용자 원문에는 “context의 세 가지 역할”이라고 적혀 있지만 이름과 설명이 확인된 역할은 Project common context와 Work context 두 가지다. 저장 층위를 세 번째 역할로 만들지 않는다.
- 이번 reference는 Project docs, Workspace manifest와 `recover/verify` CLI라는 한 구현 형태를 사용했다. 이를 범용 구조로 채택할지와 실제 Project별 상위 context 구조·선택 표현·Workspace 수명주기는 아직 정하지 않았다.
- 이번 reference에서 `복구 → 선택 → 실제 코드 변경 → 검증 → records/state 반영 → 재진입`은 통과했지만, 실제 사용자 Project 도입과 운영 서비스 효과는 증명하지 않았다.
- Workspace 생성·전환·완료·보관, acceptance 기록, Project canonical 반영, concurrent verify는 구현하지 않았다.
- manifest는 저장소가 신뢰하는 운영 계약이며 악의적인 명령을 격리하는 sandbox가 아니다. receipt와 state는 각각 atomic하게 쓰지만 하나의 transaction으로 묶이지 않는다.
- maintainer 파일과 routing의 정합성은 로컬에서 확인했지만, 현재 런타임에서는 repo-local custom agent 이름을 직접 로드하지 못했다. 전역 trust를 추가하지 않았으며, 모든 새 세션이 agent를 자동 소비하고 행동을 바꾼다는 지속 효과는 별도 검증이 필요하다.

## 다음 행동

구현된 `output/`의 구조·동작·증명 상한을 사용자가 검토해 첫 reference를 수락할지 정한다. 수락 뒤에만 다음 Workspace 수명주기나 실제 Project 적용으로 범위를 넓힌다.
