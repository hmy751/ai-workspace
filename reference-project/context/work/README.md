# Work context

Work는 작업별 Workspace의 목표·현재 상태·입력·선택한 산출물·과정 기록과 이를 읽고 관리하는 관계를 소유한다. Project 공통 의미와 제품 코드는 이 층에 복제하지 않는다.

| 구성 | 책임과 진입 |
| --- | --- |
| [Workspace collection](workspaces/README.md) | 작업별 current·source·output·records와 기계 계약의 의미·보존 경계 |
| [Spec·Ticket](workspaces/spec-and-tickets/README.md) | 작업 정의·개별 실행·전체 상황과 작성·갱신 기준 |
| [record-work](../../.agents/skills/record-work/SKILL.md) | 필요할 때 같은 기록 담당자를 호출해 원문 판단·직접 갱신을 수행 |
| [Harness](harness/README.md) | Recover의 읽기 전용 복구와 Verify의 기계 증거 기록 |
| [생성·전환](workspaces/CREATE-AND-TRANSITION.md) | 독립 목표의 초기 구성·재진입 확인·작업 대상 전환 |

Main은 작업을 조율하고 기록 담당자는 지정 Work의 문서를 갱신한다. 기록 내용은 [문서 작성 기준](workspaces/DOCUMENT-WRITING.md)을 따른다. 기록 스킬을 교체해도 Workspace의 의미·원자료·기록은 남는다. 자동 response-end Maintain·session binding과 별도 agent role은 제거했으며 기존 runtime을 임시 연결하지 않는다.

## Root 관계

- Project root: `../..` — 제품·Project 맥락·검증 실행의 기준.
- Work root: 이 디렉터리 — Workspace index·current·source·output·records의 기준.
- Harness root: `harness/` — Recover·Verify 실행 코드의 위치.

상위 관계는 [context](../README.md), AI 작업 지침은 [AGENTS](AGENTS.md)에서 시작한다. 명령은 Project root에서 실행한다.

```bash
python3 -m context.work.harness recover
python3 -m context.work.harness verify
```

Harness 자체 확인은 [임시 fixture 검증](harness/validation/README.md)을 사용하며 실제 active Workspace의 증거를 변경하지 않는다.
