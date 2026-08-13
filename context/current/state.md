# Current state

마지막 갱신: `2026-08-13`

## 현재 문제

사용자가 수락한 Project context와 Work context 상위 경계를 실제 구조와 실행 계약에 반영하고 commit했다. 현재는 구현 결과와 검증 상한에 대한 사용자 수락을 기다리는 단계다.

## 현재 상태

- Workspace current 폴더화의 수락 기준점은 commit `df2ce77`, 책임 중심 Harness 구조의 수락 기준점은 commit `80635ad`, Project·Work context 경계 구현 기준점은 commit `2b110a3`이다.
- Project common context를 `output/context/project/`, Harness와 Workspace collection을 `output/context/work/` 아래로 이동했다. `workspaces` 이름은 유지했다.
- `output/context/README.md`, `context/project/README.md`, `context/work/README.md`에서 상위 경계와 Owner 관계를 찾을 수 있다. Harness는 Work context의 공용 관리 장치이며 Project 기준이나 Workspace 의미를 소유하지 않는다.
- 실행 계약을 `project_root`와 `work_root`로 분리했다. Recover의 Project context와 verify의 evidence·실행 cwd는 Project root, Workspace index·current·records·receipt는 Work root 기준이다.
- 경로 의미 변경을 드러내기 위해 recover contract schema는 `2`, recovery packet은 `4`, status는 `2`로 올렸다. verify contract와 기존 receipt schema·내용은 유지했다.
- 전체 29개 unittest와 실제 `recover → verify → recover`가 통과했다. 새 pass receipt는 `verify-20260813T135739719409Z-2c773fcd8f4f4409b9a7c394194b3b13.json`이며, 후속 recovery가 두 path base와 최신 상태를 복구했다.
- 사람용 Workspace `state/index.md`의 SHA-256은 verify 전후 모두 `3360a031e6054e594d94ace6b4007dafad422e83883241017b94c1aacbe81ead`다.
- 독립 read-only 재검토에서 검증 주장 여섯 개가 모두 근거와 일치했고 남은 P1·P2·P3 결함은 없었다. 상세 결과와 검증 상한은 [`Project·Work context 상위 경계 재구성`](../records/2026-08-13-07-project-work-context-boundary.md)에 있다.

## 현재 필요한 접근점

- Workspace current 폴더화와 검증: [`../records/2026-08-13-05-workspace-current-folder-migration.md`](../records/2026-08-13-05-workspace-current-folder-migration.md)
- Harness 책임 경계 재구성: [`../records/2026-08-13-06-harness-responsibility-boundary-refactor.md`](../records/2026-08-13-06-harness-responsibility-boundary-refactor.md)
- Project·Work context 상위 경계 재구성: [`../records/2026-08-13-07-project-work-context-boundary.md`](../records/2026-08-13-07-project-work-context-boundary.md)
- 실행 가능한 output: [`../../output/README.md`](../../output/README.md)

## 불확실성과 검증 상한

- 사용자 원문에는 “context의 세 가지 역할”이라고 적혀 있지만 이름과 설명이 확인된 역할은 Project common context와 Work context 두 가지다. 저장 층위를 세 번째 역할로 만들지 않는다.
- 이번 reference는 `context/project/`, Workspace identity와 책임별 계약, `context/work/harness` CLI라는 한 구현 형태를 사용했다. 다른 실제 Project의 기존 문서 배치와 migration은 아직 검증하지 않았다.
- 이번 reference에서 `복구 → 선택 → 실제 코드 변경 → 검증 → records/state 반영 → 재진입`은 통과했지만, 실제 사용자 Project 도입과 운영 서비스 효과는 증명하지 않았다.
- memory의 direct-child Markdown은 모두 기본 recovery에 들어가며 문서 수·전체 byte 상한이 없다. 과거를 records로 보내고 현재성 기준으로 memory를 관리해야 하며, 규모가 커졌을 때의 추가 선택 정책은 아직 검증하지 않았다.
- Workspace 생성·전환·완료·보관, acceptance 기록, Project canonical 반영, concurrent verify는 구현하지 않았다.
- `verify.json`은 저장소가 신뢰하는 운영 계약이며 악의적인 명령을 격리하는 sandbox가 아니다. receipt와 status는 각각 안전하게 쓰지만 하나의 transaction으로 묶이지 않는다.
- repo-local `context_maintainer`는 이번 런타임에서 직접 로드·실행할 수 있음을 확인했다. 다만 모든 새 세션의 지속적인 routing 효과까지 증명한 것은 아니다.
- CLI는 현재 `context/work/harness` 설치 위치에서 Project root와 Work root를 유도한다. 다른 배치나 이미 `context` Python package를 사용하는 Project와의 결합은 아직 검증하지 않았다.

## 다음 행동

사용자가 commit `2b110a3`의 구조 변경과 검증 결과를 검토하고 수락 여부를 결정한다.
