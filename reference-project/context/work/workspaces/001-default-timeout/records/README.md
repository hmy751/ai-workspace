# Records

이 폴더는 Default timeout Workspace에서 결과를 만들고 판단한 과정, 과거 제품 검증 기록, 이미 수행된 test·eval·수동 확인의 evidence를 보존한다.

## 사람이 읽는 기록

날짜가 있는 Markdown은 분석, 후보 비교, 탈락 사유, 결정, migration, 검증 해석을 사람이 다시 판단할 수 있게 남긴 기록이다.

- [`2026-08-13-01-default-timeout-verification-cycle.md`](2026-08-13-01-default-timeout-verification-cycle.md)
- [`2026-08-13-02-current-folder-migration.md`](2026-08-13-02-current-folder-migration.md)
- [`2026-08-13-03-harness-responsibility-boundary-refactor.md`](2026-08-13-03-harness-responsibility-boundary-refactor.md)
- [`2026-08-13-04-project-work-context-boundary-migration.md`](2026-08-13-04-project-work-context-boundary-migration.md)
- [`2026-08-14-05-machine-receipt-boundary.md`](2026-08-14-05-machine-receipt-boundary.md)

## 기계 receipt

[`receipts/`](receipts/README.md)는 기계가 만든 append-only JSON을 종류별로 격리한다. 과거 제품 검증의 최신 연결은 `current/state/status.json`이 가리키지만, 새 `evidence-*` receipt는 status를 바꾸거나 Recover 입력이 되지 않는다. 어느 receipt도 이 폴더에 있다는 사실만으로 사람의 수락이나 Workspace 완료가 되지 않는다.

실제 확인은 test runner, eval 도구, 사람이 직접 수행한다. 다시 찾을 가치가 있는 결과와 미확인 범위만 Verify로 기록하며, 결과가 같아도 기존 receipt를 자동으로 삭제하거나 합치지 않는다.
