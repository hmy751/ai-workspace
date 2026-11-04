# Records

이 폴더는 Default timeout Workspace에서 결과를 만들고 판단한 과정과 지속 검증 근거를 보존한다.

## 사람이 읽는 기록

- [2026-11-04 재개 안내 전환](2026-11-04-recovery-guide-transition.md): 직접 검사·기존 증거 보존과 이전 실행기 아카이빙.

날짜가 있는 Markdown은 분석, 후보 비교, 탈락 사유, 결정, migration, 검증 해석을 사람이 다시 판단할 수 있게 남긴 기록이다.

- [`2026-08-13-01-default-timeout-verification-cycle.md`](2026-08-13-01-default-timeout-verification-cycle.md)
- [`2026-08-13-02-current-folder-migration.md`](2026-08-13-02-current-folder-migration.md)
- [`2026-08-13-03-harness-responsibility-boundary-refactor.md`](2026-08-13-03-harness-responsibility-boundary-refactor.md)
- [`2026-08-13-04-project-work-context-boundary-migration.md`](2026-08-13-04-project-work-context-boundary-migration.md)
- [`2026-08-14-05-machine-receipt-boundary.md`](2026-08-14-05-machine-receipt-boundary.md)

## 기계 receipt

[receipts](receipts/README.md)는 이전 실행에서 생성한 append-only 증거다. 과거 Verify 결과와 현재 확인을 구별하며, 현재 결과·다음 판단은 [state](../current/state/index.md)가 연결한다.

새 검증은 직접 검사로 수행하고 필요한 명령·대상·결과·한계를 해당 Ticket이나 날짜별 기록에 남긴다. 이미 실행한 receipt는 결과가 같아도 자동으로 삭제하거나 합치지 않는다.
