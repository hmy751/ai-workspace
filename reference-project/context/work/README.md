# Work context

이 디렉터리는 Project 안에서 여러 작업을 지속 가능한 Workspace로 운영하는 상위 경계다.

- [`workspaces/`](workspaces/): 각 작업의 identity, 선택 계약, 현재 context, 원자료와 provenance, goal 산출물 지도, 누적 records
- [`harness/`](harness/): active Workspace를 복구하고 Project 검증 결과를 Workspace 상태로 되돌리는 공용 관리 장치

Harness는 개별 Workspace에 속한 내용이 아니다. 여러 Workspace가 공유하는 교체 가능한 장치이며, Workspace의 목표·사람의 판단·`current/source/output/records` 의미를 독점하지 않는다. Harness를 제거해도 각 Workspace는 해당 README에서 독립적으로 읽을 수 있어야 한다.

## Root 관계

- Project root: [`../..`](../..) — Project context, 제품 코드·테스트, verify 실행과 evidence 경로의 기준
- Work root: 이 디렉터리 — Workspace index·계약·current·source·output·records와 `records/receipts/` 경로의 기준
- Harness root: [`harness/`](harness/) — 실행 코드의 위치일 뿐 Project 또는 Workspace 의미의 기준이 아님

기본 명령은 Project root에서 실행한다.

```bash
python3 -m context.work.harness recover
python3 -m context.work.harness verify
```

Project context와 Work context의 상위 관계는 [`../README.md`](../README.md), 개별 Workspace collection의 계약은 [`workspaces/README.md`](workspaces/README.md), Harness 내부 책임은 [`harness/README.md`](harness/README.md)에서 시작한다.
