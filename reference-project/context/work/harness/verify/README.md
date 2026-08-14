# Verify

`verify`는 선택한 Workspace의 `verify.json`에 고정된 argv를 제한된 조건에서 실행하고, 다음 재진입이 확인할 receipt와 machine status를 남긴다.

## 소유 계약

- `workspace.json`의 정체성과 `verify.json`의 `verification`, `next_actions`만 읽는다.
- evidence 파일의 SHA-256과 byte size를 명령 실행 전에 모두 확보한다.
- argv는 shell 없이 실행하며 shell·`env` trampoline, 절대 경로, path traversal을 거부한다.
- timeout은 exit `124`의 실패로 남기고 stdout·stderr는 stream별 상한과 Project-root 정규화를 적용한다.
- 시작 전에 `records/receipts/verify/`가 symlink가 아닌 실제 디렉터리인지 확인한다.
- 성공과 실패 모두 기존 파일을 덮지 않는 receipt를 `records/receipts/verify/`에 추가하고 `current/state/status.json`만 atomic 교체한다.
- `current/state/index.md`와 `recover.json`은 읽거나 수정하지 않는다.

Project root에서 다음처럼 실행한다.

```bash
python3 -m context.work.harness verify
python3 -m context.work.harness verify 001-default-timeout
```

검증 성공 상태는 `verified_waiting_acceptance`다. `pass`는 사람의 acceptance나 `completed` 전이를 뜻하지 않는다.

`verify`는 Workspace 상태 전환이나 인계에 필요한 durable evidence를 남기는 명령이다. 단순 반복 개발 확인은 직접 test 명령을 사용한다. 실행한 verify receipt는 결과가 같아도 자동으로 덮거나 합치지 않으며, 이전 flat `records/*.json` receipt는 status/recover 호환을 위해 계속 읽을 수 있다.
