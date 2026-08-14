# Default timeout Workspace

설정에서 `request_timeout_ms`가 빠졌을 때 Project가 정한 기본값 `5000`밀리초를 사용하도록 확인하는 작업 공간이다.

## 사람이 읽는 순서

1. [`current/memory/index.md`](current/memory/index.md)에서 작업이 진행되는 동안 계속 유효한 맥락을 찾는다.
2. [`current/state/index.md`](current/state/index.md)에서 지금 확인할 문제와 상태의 의미를 읽는다.
3. [`current/state/status.json`](current/state/status.json)에서 최근 검증 결과와 다음 행동을 확인한다.
4. [`output/index.md`](output/index.md)에서 이 goal을 위해 선택된 현재 산출물과 canonical 위치를 찾는다.
5. 상세 분석 과정이나 실행 결과가 필요할 때만 [`records/README.md`](records/README.md)의 날짜별 기록 또는 status가 가리키는 기계 receipt를 연다.
6. 원문이나 snapshot을 다시 대조해야 할 때만 [`source/index.md`](source/index.md)에서 이 Workspace가 보존한 source와 provenance를 찾는다.

다음 명령은 위 파일과 이번 작업에 선택된 Project 문서를 읽기 좋은 순서로 보여 준다. 이 Workspace 디렉터리가 아니라 [Project root](../../../..)에서 실행한다.

```sh
python3 -m context.work.harness recover
```

Machine 계약은 책임별로 분리되어 있다.

- [`workspace.json`](workspace.json): Workspace 정체성
- [`recover.json`](recover.json): Project root를 기준으로 이번 작업에 선택한 `context/project/` 문서
- [`verify.json`](verify.json): Project root에서 실행할 고정 검증 명령, evidence, 실행 제한, 결과별 다음 행동

사람이 읽는 현재 문서와 machine 계약은 분리되어 있다. 각 책임의 동작과 경계는 [`Harness recover`](../../harness/recover/README.md)와 [`Harness verify`](../../harness/verify/README.md)에서 시작한다.

## Workspace가 소유하는 내용 층

- [`current/`](current/): 지금도 유효하여 다음 행동에 필요한 목표, 제약, Project 선택 경계와 최근 상태
- [`source/`](source/): 이 Workspace가 선택한 원문, 변경하지 않은 snapshot, provenance만 보존하는 층. 현재 판단, 분석, 결정, 실행·검증 기록은 두지 않는다.
- [`output/`](output/): goal을 위해 선택된 현재 제품 구현의 canonical 위치를 보여 주는 산출물 지도. Project root의 실제 파일은 복제하지 않는다.
- [`records/`](records/README.md): source와 실제 작업을 바탕으로 만든 분석, 결정, 실행·검증 기록. 분석 메모·후보·비교·탈락안·선택 근거는 바로 아래 날짜별 Markdown에, 기계 증거는 [`receipts/`](records/receipts/README.md) 아래 종류별로 남긴다.

이 sample Workspace는 자신의 `source/` 선택·snapshot·provenance와 분리 유지 책임을 가진다. 원자료의 저자와 정본 권위는 원래 출처에 남으며 Reference 상위 구조나 Harness가 이를 넘겨받지 않는다. `recover`는 source를 기본 입력으로 읽지 않고 `output/index.md`만 산출물 지도로 읽으며 연결된 제품 파일 본문은 자동으로 읽지 않는다.
