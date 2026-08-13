# Reference Project 운영 규칙

이 디렉터리는 Project의 canonical 문서·코드·테스트와, 한 작업을 복구하고 검증하는 Workspace를 함께 보여 주는 실행 가능한 reference다.

## 재진입

작업을 시작할 때 먼저 output root에서 다음 명령을 실행한다.

```bash
python3 harness/workspace.py recover
```

Workspace id를 생략하면 `workspaces/index.json`의 active workspace를 사용한다. `recover`는 index와 manifest를 선택용 제어 정보로 읽고, state가 receipt를 가리키면 해당 JSON의 존재와 schema·Workspace·결과·완료 시각 정합성도 검증한다. receipt 본문은 recovery context에 싣지 않는다. context 본문으로는 해당 Workspace의 `current/memory.md`, `current/state.md`, manifest가 이번 작업에 선택한 Project 문서만 순서대로 싣는다. recovery packet은 `control_paths`와 `loaded_context_paths`를 나눠 공개한다. `records/` 전체나 선택되지 않은 Project 문서를 재진입 기본 입력으로 읽지 않는다. 구조화된 입력이 필요하면 `recover --json`을 사용한다.

## 검증과 상태 반영

```bash
python3 harness/workspace.py verify
```

`verify`는 `workspace.json`의 `verification.argv` 배열을 output root에서 `shell=False`로 실행한다. `verification.timeout_seconds`와 `verification.max_output_chars`를 생략하면 각각 30초와 stream당 100,000문자를 적용한다. timeout은 exit `124`의 실패 receipt와 state로 남긴다. 저장하는 stdout·stderr는 상한을 적용하고 원래 관찰 길이와 truncation 여부를 함께 기록하며, output root 절대경로는 `<OUTPUT_ROOT>`로 정규화한다. 성공과 실패 모두 충돌하지 않는 JSON receipt를 해당 Workspace의 `records/`에 남기고, `current/state.md`의 machine-owned marker를 atomic하게 갱신한다.

- 성공 상태는 `verified_waiting_acceptance`다. 검증 통과만으로 `completed`가 되지 않는다.
- 실패 상태는 `verification_failed`다. 다음 재진입은 receipt와 `state.md`에 남은 실패 다음 행동에서 이어 간다.
- 사람이 쓰는 state 설명은 marker 밖에 둔다. marker 안은 harness가 소유한다.
- 검증 명령을 임의 명령으로 바꾸어 실행하지 않는다. 작업 계약이 바뀌면 manifest를 명시적으로 검토해 수정한다.

## Project와 Workspace 경계

`docs/`, `src/`, `tests/`는 Project의 canonical 기준과 구현이다. `workspaces/`는 이번 작업의 선택된 접근점, 현재 커서, 검증 receipt를 소유한다. Workspace 결과를 Project canonical 문서나 코드에 자동 반영하지 않는다. Project 변경은 일반적인 코드 수정과 리뷰를 거쳐 별도로 수행한다.

이 reference가 구현한 수명주기는 active Workspace의 복구와 반복 검증까지다. 다음 항목은 아직 구현하지 않았다.

- 새 Workspace 생성과 active 전환 명령
- 검증 뒤 사람의 acceptance를 기록하고 `completed`로 전이하는 명령
- 완료 Workspace의 close, archive, delete 정책
- Workspace 결과를 Project canonical에 승격하는 규칙과 자동화
- 동시에 실행한 여러 `verify`가 하나의 state cursor를 갱신할 때의 조정

따라서 receipt는 검증 명령의 실행 증거이지, 제품 동작 전체나 사람의 최종 수락을 증명하지 않는다.
