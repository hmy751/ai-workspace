# Workspace Harness

이 package는 한 Workspace를 다시 읽는 `recover`와 고정 검증을 실행하는 `verify`를 공통 CLI 아래 연결한다.

```bash
python3 -m harness recover [workspace_id] [--json]
python3 -m harness verify [workspace_id]
```

## 책임 배치

- [`workspace_contract.py`](workspace_contract.py): active/id 선택, identity-only `workspace.json`, output-root 내부의 안전한 파일 접근, `status.json`과 receipt 연결 필드의 최소 공통 계약
- [`recover/`](recover/): `recover.json`, current context 선택·로딩, 연결 receipt header 확인, recovery packet과 사람용 출력
- [`verify/`](verify/): `verify.json`, evidence 선확보, 제한 실행, append-only receipt, atomic status 갱신
- [`cli.py`](cli.py): 두 책임으로 argument를 routing하고 결과를 출력
- [`__main__.py`](__main__.py): module 실행 진입점

Recover는 `verify.json`을 읽지 않고 verify는 `recover.json`을 읽지 않는다. 따라서 한쪽 전용 계약 오류가 다른 명령의 실행을 막지 않는다.

책임별 테스트까지 모두 실행하려면 output root에서 다음 명령을 사용한다.

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```
