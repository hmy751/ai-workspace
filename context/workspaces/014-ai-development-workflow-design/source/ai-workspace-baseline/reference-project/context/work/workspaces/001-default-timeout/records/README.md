# Records

이 폴더는 Default timeout Workspace에서 결과를 만들고 판단한 과정과 지속 검증 근거를 보존한다.

## 사람이 읽는 기록

날짜가 있는 Markdown은 분석, 후보 비교, 탈락 사유, 결정, migration, 검증 해석을 사람이 다시 판단할 수 있게 남긴 기록이다.

- [`2026-08-13-01-default-timeout-verification-cycle.md`](2026-08-13-01-default-timeout-verification-cycle.md)
- [`2026-08-13-02-current-folder-migration.md`](2026-08-13-02-current-folder-migration.md)
- [`2026-08-13-03-harness-responsibility-boundary-refactor.md`](2026-08-13-03-harness-responsibility-boundary-refactor.md)
- [`2026-08-13-04-project-work-context-boundary-migration.md`](2026-08-13-04-project-work-context-boundary-migration.md)
- [`2026-08-14-05-machine-receipt-boundary.md`](2026-08-14-05-machine-receipt-boundary.md)

## 기계 receipt

[`receipts/`](receipts/README.md)는 기계가 만든 append-only JSON을 종류별로 격리한다. 최신 제품 검증은 `current/state/status.json`이 가리키며, 이 폴더에 있다는 사실만으로 사람의 수락이나 Workspace 완료가 되지 않는다.

반복 개발 확인은 직접 test 명령으로 수행하고, Workspace 상태 전환이나 인계에 필요한 검증만 durable `verify`로 남긴다. 이미 실행한 receipt는 결과가 같아도 자동으로 삭제하거나 합치지 않는다.
