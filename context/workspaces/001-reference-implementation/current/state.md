# Reference implementation state

마지막 갱신: `2026-08-13`

## 현재 상태

이 Workspace의 reference 구현과 책임 경계 재구성은 완료되어 commit됐다. 후속 실제 Project 적용은 이 Workspace를 이어 쓰지 않고 [`002-project-application`](../../002-project-application/)에서 진행한다.

- Workspace current 폴더화 기준점은 commit `df2ce77`, 책임 중심 Harness 구조 기준점은 commit `80635ad`, Project·Work context 경계 구현 기준점은 commit `2b110a3`, 최종 문서 기록은 commit `e3c237b`다.
- Project common context를 `output/context/project/`, Harness와 Workspace collection을 `output/context/work/` 아래로 이동했다.
- 실행 계약을 `project_root`와 `work_root`로 분리했다.
- recover contract schema `2`, recovery packet schema `4`, status schema `2`로 경로 기준 변경을 명시했다. verify contract와 기존 receipt schema·내용은 유지했다.
- 전체 29개 unittest와 실제 `recover -> verify -> recover`가 통과했다.
- 독립 read-only 재검토에서 검증 주장 여섯 개가 모두 근거와 일치했고 남은 P1·P2·P3 결함은 없었다.

## 근거 접근점

- Workspace current 폴더화와 검증: [`../records/2026-08-13-05-workspace-current-folder-migration.md`](../records/2026-08-13-05-workspace-current-folder-migration.md)
- Harness 책임 경계 재구성: [`../records/2026-08-13-06-harness-responsibility-boundary-refactor.md`](../records/2026-08-13-06-harness-responsibility-boundary-refactor.md)
- Project·Work context 상위 경계 재구성: [`../records/2026-08-13-07-project-work-context-boundary.md`](../records/2026-08-13-07-project-work-context-boundary.md)
- 저장소 context의 Workspace 분리: [`../records/2026-08-13-08-outer-context-workspace-separation.md`](../records/2026-08-13-08-outer-context-workspace-separation.md)
- 실행 가능한 output: [`../../../../output/README.md`](../../../../output/README.md)

## 검증 상한

- 이번 reference는 한 예시 Project 안에서만 검증했다. 다른 실제 Project의 기존 문서 배치와 migration은 아직 검증하지 않았다.
- Workspace 생성·전환·완료·보관, acceptance 기록, Project canonical 반영, concurrent verify는 구현하지 않았다.
- `verify.json`은 저장소가 신뢰하는 운영 계약이며 악의적인 명령을 격리하는 sandbox가 아니다. receipt와 status는 하나의 transaction으로 묶이지 않는다.
- CLI의 고정 설치 위치와 기존 `context` Python package가 있는 Project의 결합은 검증하지 않았다.

## 다음 행동

이 Workspace에는 예정된 다음 행동이 없다. reference 자체를 다시 변경해야 할 때만 별도 지시로 재개한다.
