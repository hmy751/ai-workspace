# Recover

`recover`는 다음 세션이 바로 판단하고 행동할 수 있도록 active 또는 명시된 Workspace의 제한된 recovery packet을 만든다.

## 소유 계약

- `workspace.json`의 정체성과 `recover.json`의 `project_context`만 읽는다.
- `current/memory/`의 `index.md`와 direct-child Markdown을 파일명 순서로 싣는다.
- 사람용 `current/state/index.md`와 machine용 `current/state/status.json`을 함께 싣는다.
- status가 receipt를 연결하면 schema, Workspace id, result, finished time header만 대조한다. receipt 본문은 context에 싣지 않는다.
- 선택되지 않은 Project 문서, `records/` 전체, `verify.json`은 읽지 않는다.

output root에서 다음처럼 실행한다.

```bash
python3 -m harness recover
python3 -m harness recover 001-default-timeout --json
```

JSON packet schema는 `3`이며 `workspace_path`, `recover_contract_path`, 제어용 `control_paths`, 실제 context인 `loaded_context_paths`, `memory`, `state`, `project_context`를 구분해 공개한다.
