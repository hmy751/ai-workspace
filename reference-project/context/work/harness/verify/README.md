# Verify

`verify`는 이미 다른 주체가 수행한 test, eval, 수동 확인의 결과와 확인하지 못한 범위를 선택한 Workspace에 append-only evidence로 기록한다. 제품 명령을 실행하거나 결과의 충분성을 판정하는 verifier가 아니다.

## 소유 계약

- 입력 evidence의 schema와 선택한 `workspace_id`를 검증한다.
- Project-root 상대 JSON 파일 또는 stdin에서 입력을 받는다.
- 기존 `records/receipts/`가 symlink가 아닌 실제 디렉터리인지 확인한다. 자기 소유 `verify/` leaf가 없으면 안전하게 만들고, 기존 파일을 덮지 않는 `evidence-*.json` receipt를 추가한다.
- `source_refs`는 이미 수행된 확인으로 돌아갈 수 있는 위치를 기록할 뿐이다. Verify는 locator를 열거나 원자료의 진위를 다시 판정하지 않는다.
- `outcome`의 `pass`, `fail`, `partial`은 evidence 생산자가 보고한 결과다. 세 결과 모두 유효하게 기록되면 CLI는 exit `0`을 반환한다.
- 제품 코드·테스트를 실행하지 않고, 제품 파일을 snapshot하거나 hash하지 않는다.
- `verify.json`, 기존 `verify-*.json` receipt, `current/state/status.json`, `recover.json`을 읽거나 수정하지 않는다.
- Workspace 상태 전환, Recover 입력, 다음 행동, 사람 acceptance, 작업 완료를 결정하지 않는다.

## Evidence 입력

입력은 다음 필드를 정확히 가진 schema v1 JSON object다.

- `observed_at`: evidence가 관찰된 시각. timezone을 포함한 RFC 3339 timestamp
- `producer`: test runner, Main task, 사람 등 evidence를 만든 주체
- `subject`: 무엇을 확인했는지
- `method`: 실제로 수행한 test, eval, 수동 확인 방법
- `outcome`: `pass`, `fail`, `partial` 중 하나
- `result_summary`: 관찰된 결과의 짧은 요약
- `source_refs`: 원래 결과로 돌아가기 위한 `kind`와 `locator` 목록. 재접근 경로가 없으면 빈 배열
- `unverified_scope`: 이 evidence로 확인하지 않은 범위. 최소 한 항목이 필요하다.

예시는 다음과 같다.

```json
{
  "schema_version": 1,
  "observed_at": "2026-08-17T20:30:45+09:00",
  "producer": "Main task",
  "subject": "default timeout unit tests",
  "method": "python3 -m unittest tests.test_config_loader -v",
  "outcome": "pass",
  "result_summary": "7 tests completed successfully",
  "source_refs": [
    {
      "kind": "task-transcript",
      "locator": "verification command 1"
    }
  ],
  "unverified_scope": [
    "운영 서비스의 실제 timeout 동작은 확인하지 않았다."
  ]
}
```

Project root에서 파일 또는 stdin으로 기록한다.

```bash
python3 -m context.work.harness verify 001-default-timeout --input-json evidence.json
python3 -m context.work.harness verify 001-default-timeout --input-json - < evidence.json
```

성공 summary의 `recorded: true`는 입력 evidence receipt가 append-only 경로에 기록됐다는 뜻이다. `evidence_outcome: pass`도 제품이 충분히 검증됐거나 Workspace가 완료됐다는 뜻이 아니다. Verify는 빠진 Workspace나 `records/receipts/` 상위 구조를 대신 만들지 않는다.

## 과거 제품 검증과의 경계

기존 `verify.json`, `verify-*.json` receipt와 schema v2·v3 status는 과거 제품 검증 기록과 Recover 호환을 위해 다시 쓰지 않고 보존할 수 있다. 새 Verify는 이 파일들을 입력으로 사용하거나 새 형식으로 이관하지 않는다.

Recover는 status가 가리키는 과거 `verify-*.json` product receipt만 기존 규칙으로 복구한다. 새 `evidence-*.json`은 독립적인 evidence 기록이며 status의 제품 검증 근거로 연결할 수 없고, Recover가 자동으로 읽거나 최신 evidence로 선택하지 않는다.
