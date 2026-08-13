# Current state

마지막 갱신: `2026-08-13`

## 현재 문제

첫 Project–Workspace reference의 `recover`와 `verify`를 책임 중심 경계로 재구성하고 실제 순환까지 검증한 뒤 사용자가 수락했다. 이 구조를 기준점으로 남겼으며 다음 workflow 책임이나 Workspace 수명주기 작업을 정할 단계다.

## 현재 상태

- Workspace current 폴더화의 수락 기준점은 commit `df2ce77`이고, 그 위에 책임 중심 Harness 구조를 반영한 commit `80635ad`가 현재 수락된 output 기준점이다.
- Project canonical과 Workspace `current/records`는 Harness 아래로 흡수하지 않고 기존 Owner 경계에 유지한다.
- 책임 재구성을 구현했다. `workspace.json`은 identity, `recover.json`과 `verify.json`은 각 책임 계약을 소유하며, 구현·테스트·README도 `harness/recover/`와 `harness/verify/`에 묶었다.
- 전체 26개 unittest와 실제 `recover → verify → recover`가 통과했다. reference Workspace의 machine status는 새 receipt를 가리키는 `verified_waiting_acceptance`이며, 이는 제품 검증 cursor로서 이미 끝난 Harness 구조 수락과 별개다. 후속 recovery는 packet schema `3`을 복구했고 사람용 `state/index.md` hash는 바뀌지 않았다.
- 독립 read-only 검토에서도 P1·P2·P3 결함이 발견되지 않았다. 정확한 명령, 테스트 구성, receipt, hash와 검증 상한은 [`Harness 책임 경계 재구성`](../records/2026-08-13-06-harness-responsibility-boundary-refactor.md)에 있다.

## 현재 필요한 접근점

- Workspace current 폴더화와 검증: [`../records/2026-08-13-05-workspace-current-folder-migration.md`](../records/2026-08-13-05-workspace-current-folder-migration.md)
- Harness 책임 경계 재구성: [`../records/2026-08-13-06-harness-responsibility-boundary-refactor.md`](../records/2026-08-13-06-harness-responsibility-boundary-refactor.md)
- 실행 가능한 output: [`../../output/README.md`](../../output/README.md)

## 불확실성과 검증 상한

- 사용자 원문에는 “context의 세 가지 역할”이라고 적혀 있지만 이름과 설명이 확인된 역할은 Project common context와 Work context 두 가지다. 저장 층위를 세 번째 역할로 만들지 않는다.
- 이번 reference는 Project docs, Workspace identity와 책임별 계약, `recover/verify` CLI라는 한 구현 형태를 사용했다. 실제 Project별 상위 context 구조·선택 표현·Workspace 수명주기는 아직 정하지 않았다.
- 이번 reference에서 `복구 → 선택 → 실제 코드 변경 → 검증 → records/state 반영 → 재진입`은 통과했지만, 실제 사용자 Project 도입과 운영 서비스 효과는 증명하지 않았다.
- memory의 direct-child Markdown은 모두 기본 recovery에 들어가며 문서 수·전체 byte 상한이 없다. 과거를 records로 보내고 현재성 기준으로 memory를 관리해야 하며, 규모가 커졌을 때의 추가 선택 정책은 아직 검증하지 않았다.
- Workspace 생성·전환·완료·보관, acceptance 기록, Project canonical 반영, concurrent verify는 구현하지 않았다.
- `verify.json`은 저장소가 신뢰하는 운영 계약이며 악의적인 명령을 격리하는 sandbox가 아니다. receipt와 status는 각각 안전하게 쓰지만 하나의 transaction으로 묶이지 않는다.
- repo-local `context_maintainer`는 이번 런타임에서 직접 로드·실행할 수 있음을 확인했다. 다만 모든 새 세션의 지속적인 routing 효과까지 증명한 것은 아니다.

## 다음 행동

commit `80635ad`의 책임 중심 구조를 기준으로 사용자의 다음 지시를 받는다. 아직 미구현인 acceptance·완료 전이와 Workspace 생성·전환·보관 중 무엇을 다음 책임으로 다룰지는 정하지 않았다.
