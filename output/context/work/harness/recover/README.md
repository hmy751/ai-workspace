# Recover

`recover`는 다음 세션이 바로 판단하고 행동할 수 있도록 active 또는 명시된 Workspace의 제한된 recovery packet을 만든다.

## 소유 계약

- `workspace.json`의 정체성과 `recover.json`의 `project_context`만 읽는다.
- `current/memory/`의 `index.md`와 direct-child Markdown을 파일명 순서로 싣는다. `01-goal.md`, `02-constraints.md`, `03-project-context.md`는 recovery에 필요한 최소 memory 계약이므로 하나라도 없으면 실패한다.
- 사람용 `current/state/index.md`와 machine용 `current/state/status.json`을 함께 싣는다.
- Workspace `output/index.md`를 goal 산출물 지도로 싣는다. index가 연결하는 코드·문서·테스트나 같은 폴더의 다른 산출물 본문은 자동으로 읽지 않는다.
- status가 receipt를 연결하면 schema, Workspace id, result, finished time header만 대조한다. receipt 본문은 context에 싣지 않는다.
- 선택되지 않은 Project 문서, Workspace `source/` 전체, Workspace output artifact 본문, `records/` 전체, `verify.json`은 읽지 않는다.

Project root에서 다음처럼 실행한다.

```bash
python3 -m context.work.harness recover
python3 -m context.work.harness recover 001-default-timeout --json
```

JSON packet schema는 `5`다. schema `4`에 Workspace `output.index`와 그 loaded context path를 추가했다. Workspace 자료가 Work root 상대이고 Project context가 Project root 상대라는 `path_base`를 각 경로에 명시하며, 제어용 경로와 실제로 읽은 context 경로를 구분해 공개한다.
