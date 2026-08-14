# Reference Project 운영 규칙

이 디렉터리는 Project context, Work context, 제품의 책임 경계를 함께 보여 주는 실행 가능한 reference다. 전체 관계와 사람용 시작점은 먼저 [`README.md`](README.md)와 [`context/README.md`](context/README.md)에서 확인한다.

## 재진입과 검증

`reference-project/` root에서 다음 명령을 사용한다.

```bash
python3 -m context.work.harness recover
python3 -m context.work.harness verify
```

- Project context와 Work context의 관계는 [`context/README.md`](context/README.md)가 정의한다.
- Recover의 목적·입력·출력·비소유 범위는 [`context/work/harness/recover/README.md`](context/work/harness/recover/README.md)가 정의한다.
- Verify의 목적·입력·출력·상태 반영 범위는 [`context/work/harness/verify/README.md`](context/work/harness/verify/README.md)가 정의한다.
- Harness와 Workspace collection의 관계는 [`context/work/README.md`](context/work/README.md)가 정의한다.
- 지속 Workspace의 내부 관계는 [`context/work/workspaces/README.md`](context/work/workspaces/README.md)와 각 Workspace README가 정의한다.

## 변경 배치

- Recover 전용 규칙·구현·검증은 `context/work/harness/recover/`에서 함께 변경한다.
- Verify 전용 규칙·구현·검증은 `context/work/harness/verify/`에서 함께 변경한다.
- 두 책임에서 실제로 같은 의미로 사용하는 Workspace 식별·안전한 접근·status 인계 계약만 `context/work/harness/workspace_contract.py`에 둔다.
- 한 책임만 사용하는 코드를 공유 영역으로 올리지 않는다.
- Project 기준은 `context/project/`, 제품 코드·테스트는 `src/`와 `tests/`에 두고 Harness 아래로 옮기거나 복제하지 않는다.
- `context/project/README.md`와 `overview.md`는 실제 Project common context의 최소 진입점이다. 기존 제품 문서를 그대로 복사하거나 링크만 나열하지 않고, 여러 Workspace가 공유할 목적·구조·제약·채택 결정과 상세 Owner의 우선순위를 실제 내용으로 유지한다.
- 상세 제품 Owner, 코드나 채택 결정이 바뀌면 `context/project/overview.md`를 다시 대조한다. 충돌한 overview를 최신 사실처럼 두지 않는다.
- Workspace `current/`, `source/`, `output/`, `records/`의 의미를 Harness 코드가 독점 정의하지 않는다. 사람이 읽는 날짜별 records와 `records/receipts/<종류>/`의 기계 증거를 분리하고, Harness가 생성하더라도 receipt의 보존 Owner는 해당 Workspace로 유지한다.
- 작업별 Project context 선택은 `recover.json`, 고정 검증과 결과별 다음 행동은 `verify.json`에서 변경한다. Recover가 선택하는 Project context는 `context/project/` 아래 regular Markdown으로 제한한다.
- Project 문서·제품 evidence·검증 cwd는 Project root 기준, Workspace index·current·source·output·records는 `context/work/` 기준으로 해석한다.
- 분석 메모·후보·비교·탈락안·선택 근거는 `records/` 바로 아래 날짜별 기록에 누적하고, 제품 검증 JSON은 `records/receipts/verify/`에 둔다. Goal을 위해 선택된 현재 산출물은 Workspace `output/index.md`에서 찾게 한다.
- 실제 산출물이 Project root의 코드·문서·테스트라면 Workspace `output/`에 복제하지 않고 `output/index.md`에서 canonical 상대 경로를 연결한다.

## 검증

전체 제품·Harness 검증은 다음 명령으로 실행한다.

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

책임 재배치 뒤에는 실제 active Workspace에서 `recover → verify → recover`도 실행해 packet, `records/receipts/verify/` receipt, `current/state/status.json`의 연결을 확인한다. 반복 개발 확인은 먼저 직접 test 명령을 사용하고, durable verify는 상태 전환이나 인계에 필요한 경계에서 실행한다.

검증 통과는 `verified_waiting_acceptance`이며 사람의 수락이나 Workspace 완료를 뜻하지 않는다. Acceptance와 완료 전이는 verify 책임에 암묵적으로 추가하지 않는다.
