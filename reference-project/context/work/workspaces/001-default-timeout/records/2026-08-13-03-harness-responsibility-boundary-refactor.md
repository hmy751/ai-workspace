# Harness recover·verify 책임 경계 재구성

날짜: `2026-08-13`

## 작업 목적

기존 `harness/workspace.py`와 통합 Harness test에 섞여 있던 `recover`, `verify`, 공통 Workspace 인계 계약을 실제 문서·코드·설정·테스트 경계에서도 구분한다.

Project canonical과 Workspace `current/records`는 Harness 아래로 옮기지 않고, Harness가 참조하고 갱신하는 외부 Owner 경계로 유지한다.

## 실제 변경

- `harness/README.md`: Harness 상위 경계와 recover·verify 관계
- `harness/workspace_contract.py`: active/id 선택, output-root 내부 안전한 접근, status·receipt 인계의 최소 공통 계약
- `harness/recover/`: recover 전용 정의, 구현, 11개 테스트
- `harness/verify/`: verify 전용 정의, 구현, 8개 테스트
- `harness/cli.py`, `harness/__main__.py`: `python3 -m harness`의 얇은 명령 routing
- `workspace.json`: Workspace identity만 유지
- `recover.json`: 선택한 Project context와 선택 이유
- `verify.json`: 고정 argv, evidence, 실행 제한, 결과별 다음 행동
- 제품 테스트는 `tests/test_config_loader.py`에 유지

기존 `harness/workspace.py`와 `tests/test_workspace_harness.py`는 책임별 구현과 테스트로 대체했다.

## 책임 간 독립성

- malformed `verify.json`을 둔 fixture에서도 recover가 성공하고 해당 내용을 읽거나 출력하지 않았다.
- malformed `recover.json`을 둔 fixture에서도 verify가 실행됐고 recover 계약을 수정하지 않았다.
- recovery packet schema를 `3`으로 올리고 verify argv와 verify 전용 설정을 packet에서 제거했다.
- 각 artifact의 schema version을 하나의 공통 상수에 묶지 않고 Workspace index·identity, recover contract·packet, verify contract, status, receipt별로 소유하게 했다.

## 자동 테스트

`output/` root에서 다음 명령을 실행했다.

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

총 26개가 통과했다.

- recover 책임 테스트: 11개
- verify 책임 테스트: 8개
- 제품 config loader 테스트: 7개

path traversal·절대경로·symlink 거부, receipt 본문 비노출, evidence 선확보, timeout exit `124`, 출력 상한과 root 정규화, append-only receipt, atomic status 갱신, 사람용 state 불변, pass의 `completed` 비승격을 포함한다.

## 실제 reference 순환

새 CLI로 active Workspace의 `recover → verify → recover`를 실행했다.

- 사전 recovery: 기존 pass receipt와 `verified_waiting_acceptance` 복구
- verify 결과: 제품 테스트 7개 통과, exit `0`
- 책임 분리 구현의 첫 실제 pass receipt는 `verify-20260813T124912507712Z-d2e85f3cf26a4372a2fc5bf476ebd245.json`으로 남겼다. 이후 receipt를 기존 파일 비덮어쓰기와 완전 작성 뒤 공개를 함께 지키도록 보강하고 같은 검증을 다시 실행했다.
- 최종 receipt: [`verify-20260813T125144640368Z-5dd549bd4b3244ba97787b7bdc80b503.json`](verify-20260813T125144640368Z-5dd549bd4b3244ba97787b7bdc80b503.json)
- 후속 recovery: packet schema `3`, identity·recover contract·새 receipt를 control path로 복구
- context 본문: memory index와 주제 문서, state index와 status, 선택된 Project 문서 두 개만 로드
- `state/index.md` SHA-256: 실행 전후 모두 `3360a031e6054e594d94ace6b4007dafad422e83883241017b94c1aacbe81ead`
- receipt의 source와 product test SHA-256은 실행 후 실제 파일과 일치

독립 read-only 검토에서도 책임 응집, 계약 오류 독립성, Project·Workspace Owner 보존, 기존 안전 계약, 사람용 진입 경로에 P1·P2·P3 결함이 발견되지 않았다.

## 검증 상한

확인한 것은 한 reference Project에서 책임 중심 구조와 기존 동작 보존, 책임별 계약 독립성, 실제 상태 재진입이다.

Workspace 생성·전환·acceptance·완료·보관, Project canonical 반영, concurrent verify, receipt와 status의 단일 transaction은 구현하거나 증명하지 않았다.
