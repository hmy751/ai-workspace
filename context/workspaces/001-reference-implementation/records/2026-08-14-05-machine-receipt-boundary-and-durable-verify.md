# Machine receipt 경계와 durable verify 운용

날짜: `2026-08-14`

## 작업 목적

Workspace의 사람이 읽는 작업 기록과 반복 실행으로 늘어나는 기계 JSON을 같은 `records/` root에서 분리한다. Receipt 생성 코드의 위치와 증거의 보존 책임을 구분하고, 단순 개발 확인과 다음 상태로 넘길 durable verification의 실행 기준을 명시한다.

## 확정한 책임

- Receipt가 증명하는 작업과 보존 수명주기의 Owner는 해당 Workspace다. Harness와 helper는 receipt producer이며 공용 Harness 폴더가 Workspace별 증거를 소유하지 않는다.
- `records/` 바로 아래에는 날짜가 있는 사람이 읽는 분석·결정·migration·검증 해석을 둔다.
- 기계가 만든 append-only JSON은 `records/receipts/` 아래 `verify/`, `harness-tests/`, `preflight/`로 종류를 분리한다.
- 새 product verify는 `records/receipts/verify/`에만 쓴다. 이전 flat `records/*.json` 경로는 기존 status와 receipt를 읽기 위한 호환 경계로 유지하되 새로 만들지 않는다.
- 반복 개발 확인은 직접 test 명령으로 수행한다. Product `verify`는 Workspace 상태 전환이나 다음 사람·세션에 검증 근거를 인계할 때 durable receipt를 남기기 위해 실행한다.
- 실행된 성공·실패 receipt는 하나의 사건이므로 같은 결과나 evidence hash라는 이유로 자동 삭제·병합하지 않는다.

## 실제 reference 변경

- Default timeout Workspace에 사람이 읽는 [`records/README.md`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/README.md)와 기계 receipt용 [`receipts/README.md`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/receipts/README.md)를 추가했다.
- 기존 product verify JSON 10개를 `records/` root에서 `records/receipts/verify/`로 이동했다. Staged Git diff는 10개를 모두 `R100`으로 판정해 내용 바이트가 바뀌지 않았음을 확인했다.
- Verify는 `records/receipts/verify/`가 symlink가 아닌 실제 디렉터리인지 제품 명령 전에 확인하고, 성공과 실패 receipt를 그 경로에만 append한다.
- Status와 recover의 same-Workspace `records/` containment는 nested 경로를 허용한다. Recover 회귀 테스트는 새 nested receipt와 기존 flat receipt를 모두 읽을 수 있음을 확인한다.
- Receipt schema `1`, status schema `2`, recover contract schema `4`, recovery packet schema `5`는 의미와 shape가 바뀌지 않아 유지했다.
- repo-local `apply-context-harness` skill은 preflight, target-specific Harness tests, product verify receipt를 각각 `preflight/`, `harness-tests/`, `verify/`에 보존하도록 같은 경계를 반영했다.

Reference 내부의 상세 결정과 migration은 [`Machine receipt 경계 분리`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/2026-08-14-05-machine-receipt-boundary.md)에서 다시 확인할 수 있다.

## Git 경계

- 루트 기준 Project의 `output/` → `reference-project/` 이름 변경은 commit `d442c20`에 반영됐다.
- 이 record가 다루는 receipt 배치·호환·운용 변경은 점검 시점 HEAD `d442c20` 뒤의 작업 트리와 index에 있으며 아직 commit되지 않았다.

## 검증

### 전체 reference와 skill

`reference-project/` root에서 다음 명령을 실행했다.

```bash
python3 -B -m unittest discover -s . -p 'test_*.py' -v
```

총 40개가 통과했다.

- recover 책임 테스트: 22개
- verify 책임 테스트: 11개
- 제품 config loader 테스트: 7개

Repo-local application skill helper 테스트 7개도 통과했고, PyYAML이 설치된 Python `3.11.15`로 실행한 skill validator 결과는 `Skill is valid!`였다.

### 실제 verify와 재복구

- 최신 nested receipt: [`verify-20260814T070729765148Z-4de3a77434444335b088d4944631e94f.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260814T070729765148Z-4de3a77434444335b088d4944631e94f.json)
- receipt result: `pass`
- 제품 unittest: 7개 통과
- evidence: 제품 코드와 테스트 2개를 실행 전에 hash
- machine status: 같은 nested receipt를 가리키는 `verified_waiting_acceptance`
- 완료 시각: `2026-08-14T07:07:29.764Z`

후속 `python3 -B -m context.work.harness recover --json`은 packet schema `5`로 통과했다. Current context 6개, Workspace output index 1개, Project 문서 2개를 loaded context로 복구했고, 새 nested receipt는 control path로만 연결해 본문을 context에 싣지 않았다.

## 검증 상한

- 직접 test 통과는 현재 코드의 반복 확인이며 그 자체로 durable receipt나 Workspace 상태 전환을 만들지 않는다.
- 폴더 분리와 직접 test·durable verify 구분은 불필요한 생성을 줄이는 운용 기준이다. 자동 retention, 오래된 receipt 삭제·압축·병합 정책은 구현하지 않았다.
- Concurrent verify 조정과 receipt/status의 단일 transaction은 여전히 구현하지 않았다.
- 기존 flat 경로 읽기 호환은 기존 target을 자동으로 nested layout으로 migration하지 않는다. 대상별 기존 canonical과 사용자 변경을 고정한 별도 적용 판단이 필요하다.
- 검증 통과는 사람 acceptance, Workspace 완료, 실제 네트워크나 운영 서비스 효과를 뜻하지 않는다.
