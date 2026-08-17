# Work context

이 디렉터리는 Project 안에서 여러 작업을 지속 가능한 Workspace로 운영하는 상위 경계다.

이 영역을 수정하는 AI 작업 지침과 Maintain agent routing은 [`AGENTS.md`](AGENTS.md)에서 찾는다.

- [`workspaces/`](workspaces/): 각 작업의 identity, 선택 계약, 현재 context, 원자료와 provenance, goal 산출물 지도, 누적 records
- [`harness/`](harness/): 선택한 Workspace를 Recover·Maintain·Verify하고 관리 장치 자체를 별도로 검증하는 교체 가능한 실행 경계

Harness는 개별 Workspace에 속한 내용이 아니다. 여러 Workspace가 공유하는 교체 가능한 장치이며, Workspace의 목표·사람의 판단·`current/source/output/records` 의미를 독점하지 않는다. Harness를 제거해도 각 Workspace는 해당 README에서 독립적으로 읽을 수 있어야 한다.

Workspace Context의 의미와 관리 기준은 [`workspaces/`](workspaces/)가 계속 소유한다. Harness의 [`Maintain`](harness/maintain/)은 Main 작업 세션 동안 선택한 Workspace 이해를 유지하고, 매 사용자 대상 Main 응답 종료에서 durable 의미 변화만 그 기준에 맞춰 반영하는 관리 책임이다. 같은 책임 디렉터리가 [Reference 전용 agent](harness/maintain/workspace-context-maintainer.toml)와 교체 가능한 session runtime adapter를 함께 소유한다. Adapter를 제거하거나 교체해도 Workspace의 의미와 관리 기준은 남는다.

Harness 계약·구현 변경은 실제 active Workspace에 durable receipt를 남기는 방식으로 자기 검증하지 않는다. [`harness/validation/`](harness/validation/)의 임시 Project/Workspace fixture 검사가 Harness 회귀를 소유한다.

## Root 관계

- Project root: [`../..`](../..) — Project context와 제품 코드·테스트의 Owner, Harness 실행 기준
- Work root: 이 디렉터리 — Workspace index·계약·current·source·output·records와 `records/receipts/` 경로의 기준
- Harness root: [`harness/`](harness/) — 실행 코드의 위치일 뿐 Project 또는 Workspace 의미의 기준이 아님

기본 명령은 Project root에서 실행한다.

```bash
python3 -m context.work.harness recover
python3 -m context.work.harness verify --input-json path/to/evidence.json
```

Project context와 Work context의 상위 관계는 [`../README.md`](../README.md), 개별 Workspace collection의 계약은 [`workspaces/README.md`](workspaces/README.md), Harness 내부 책임은 [`harness/README.md`](harness/README.md)에서 시작한다.
