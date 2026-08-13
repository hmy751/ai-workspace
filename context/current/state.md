# Current state

마지막 갱신: `2026-08-13`

## 현재 문제

첫 Project–Workspace reference의 current를 폴더화하고 사람용 문서와 machine 상태를 분리한 결과가 사용자의 읽기·축적 의도에 맞는지 검토할 단계다.

## 현재 상태

- 최초 실행 가능한 reference와 당시 검증 상태는 commit `40f9116`에 기준점으로 남겼다. 상세 구성과 검증은 [`첫 output 구현 기록`](../records/2026-08-13-04-first-output-reference.md)에 있다.
- `output/` Workspace의 current를 `memory/`와 `state/` 폴더로 옮겼다. Workspace README와 memory/state index는 사람이 읽고, `state/status.json`만 harness가 갱신한다.
- memory는 번호가 붙은 주제별 현재 문서로 나눴고, recovery는 index 뒤에 direct-child Markdown을 파일명 순으로 읽는다. records와 중첩 폴더는 기본 context에 넣지 않는다.
- 제품 7개와 harness 15개를 합친 22개 unittest가 통과했다. 실제 post-migration `recover → verify → recover`도 통과했고 새 pass receipt와 `verified_waiting_acceptance`를 복구했다.
- 검증 전후 사람용 `state/index.md`의 SHA-256이 같아 harness가 사람 문서를 덮어쓰지 않았음을 확인했다. 상세 변경과 증명은 [`폴더화 기록`](../records/2026-08-13-05-workspace-current-folder-migration.md)에 있다.
- 이번 폴더화 변경은 아직 commit하지 않았으며 사용자 검토를 기다린다.

## 현재 필요한 접근점

- Project–Workspace context 합의: [`../records/2026-08-13-03-project-workspace-context-agreement.md`](../records/2026-08-13-03-project-workspace-context-agreement.md)
- 첫 output 구현과 실제 검증: [`../records/2026-08-13-04-first-output-reference.md`](../records/2026-08-13-04-first-output-reference.md)
- Workspace current 폴더화와 검증: [`../records/2026-08-13-05-workspace-current-folder-migration.md`](../records/2026-08-13-05-workspace-current-folder-migration.md)
- 실행 가능한 output: [`../../output/README.md`](../../output/README.md)

## 불확실성과 검증 상한

- 사용자 원문에는 “context의 세 가지 역할”이라고 적혀 있지만 이름과 설명이 확인된 역할은 Project common context와 Work context 두 가지다. 저장 층위를 세 번째 역할로 만들지 않는다.
- 이번 reference는 Project docs, Workspace manifest와 `recover/verify` CLI라는 한 구현 형태를 사용했다. 실제 Project별 상위 context 구조·선택 표현·Workspace 수명주기는 아직 정하지 않았다.
- 이번 reference에서 `복구 → 선택 → 실제 코드 변경 → 검증 → records/state 반영 → 재진입`은 통과했지만, 실제 사용자 Project 도입과 운영 서비스 효과는 증명하지 않았다.
- memory의 direct-child Markdown은 모두 기본 recovery에 들어가며 문서 수·전체 byte 상한이 없다. 과거를 records로 보내고 현재성 기준으로 memory를 관리해야 하며, 규모가 커졌을 때의 추가 선택 정책은 아직 검증하지 않았다.
- Workspace 생성·전환·완료·보관, acceptance 기록, Project canonical 반영, concurrent verify는 구현하지 않았다.
- manifest는 저장소가 신뢰하는 운영 계약이며 악의적인 명령을 격리하는 sandbox가 아니다. receipt와 status는 각각 atomic하게 쓰지만 하나의 transaction으로 묶이지 않는다.
- maintainer 파일과 routing의 정합성은 로컬에서 확인했지만, 현재 런타임에서는 repo-local custom agent 이름을 직접 로드하지 못했다. 전역 trust를 추가하지 않았으며, 모든 새 세션이 agent를 자동 소비하고 행동을 바꾼다는 지속 효과는 별도 검증이 필요하다.

## 다음 행동

폴더화된 Workspace의 사람용 진입점, memory 축적 규칙, state 분리가 의도에 맞는지 사용자가 검토한다. 수락 뒤에만 다음 Workspace 수명주기나 실제 Project 적용으로 범위를 넓힌다.
