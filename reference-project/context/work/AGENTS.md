# Work context 운영 규칙

이 파일은 `context/work/` 아래의 Workspace와 Harness를 다루는 작업 지침이다. Work context의 의미와 관계는 [`README.md`](README.md), Workspace collection의 의미는 [`workspaces/README.md`](workspaces/README.md), Harness 책임의 관계는 [`harness/README.md`](harness/README.md)가 각각 소유한다.

## 재진입과 검증

명령은 Project root에서 실행한다.

```bash
python3 -m context.work.harness recover
python3 -m context.work.harness verify
```

- Recover의 목적·입력·출력·비소유 범위는 [`harness/recover/README.md`](harness/recover/README.md)가 정의한다.
- Maintain의 목적·활성 시점·Owner routing·비소유 범위는 [`harness/maintain/README.md`](harness/maintain/README.md)가 정의한다.
- Verify의 목적·입력·출력·상태 반영 범위는 [`harness/verify/README.md`](harness/verify/README.md)가 정의한다.
- Harness 자체 회귀 검증의 범위는 [`harness/validation/README.md`](harness/validation/README.md)가 정의한다.
- 지속 Workspace의 내부 관계는 [`workspaces/README.md`](workspaces/README.md)와 각 Workspace README가 정의한다.

## 책임과 활성 시점

- **Recover**: 새 세션이나 새 작업 주체가 선택한 Workspace에 재진입하거나 현재 context를 다시 구성해야 할 때 실행한다. 제한된 recovery packet을 읽기 전용으로 만들며 작업 중 context를 갱신하거나 제품 정합성을 입증하지 않는다.
- **Maintain**: 작업 중 목표·제약·현재 상태·판단·source 선택·output 경계의 의미가 바뀔 때 [`Maintain 계약`](harness/maintain/README.md)에 따라 명시한 Workspace의 기존 Owner만 갱신한다. Main은 사용자 정정과 관련 diff·파일·test 근거를 명시해 맡기고 실제 diff를 검토한다.
- **Verify**: Workspace 상태 전환이나 인계에 남길 지속적인 제품 증거가 필요할 때 실행한다. `verify.json`의 고정 명령을 실행하고 receipt와 machine status를 남기지만 context의 의미를 갱신하거나 사람의 acceptance를 결정하지 않는다.
- **Harness validation**: 작업 흐름의 단계가 아니라 Harness 자체 검증 경계다. Recover·Verify 계약이나 구현이 바뀔 때 임시 Project/Workspace fixture에서 결정적 회귀 검사를 실행하고 실제 active Workspace의 receipt나 status를 생성·변경하지 않는다.

## Maintain agent routing

Reference의 실제 Maintain agent 정의는 [`harness/maintain/workspace-context-maintainer.toml`](harness/maintain/workspace-context-maintainer.toml)이다. Project-scoped role `workspace_context_maintainer`는 Project root의 [`.codex/config.toml`](../../.codex/config.toml)이 이 파일을 `config_file`로 등록한다. Agent 정의와 Maintain 책임은 Work 아래에 두고, 루트 설정에는 발견에 필요한 경로만 둔다.

자연스러운 의미 변화 경계에서는 main이 현재 작업의 명시적 `workspace_id`, 사용자 정정, 관련 diff·파일·Git 상태, test 또는 Verify 결과와 허용 수정 범위를 `workspace_context_maintainer`에게 전달한다. Agent가 등록되지 않은 실행 환경이면 main이 [`Maintain 계약`](harness/maintain/README.md)을 같은 경계로 수행한다.

Maintain 실행 주체는 다른 Workspace나 active index를 기본 탐색하지 않고, raw source snapshot·제품 코드·machine 계약·Verify receipt와 status를 수정하지 않는다. 변경 뒤에는 main이 전달 근거와 실제 diff를 대조한다. Agent 보고나 정적 검사가 사용자 acceptance를 대신하지 않는다. 바깥 Project에 이름이 비슷한 maintainer가 있어도 이 Reference agent로 간주하지 않는다.

## 변경 배치

- Recover 전용 규칙·구현·검증은 `harness/recover/`에서 함께 변경한다.
- Maintain 전용 실행 계약과 Codex agent 정의는 `harness/maintain/`에서 함께 변경한다. `.codex/config.toml`은 role의 발견 경로만 등록하며 Maintain 규칙을 복제하지 않는다.
- Verify 전용 규칙·구현·검증은 `harness/verify/`에서 함께 변경한다.
- Harness 자체 회귀 검증은 `harness/validation/`에서 변경한다. 공통 test fixture는 `harness/testing.py`에만 둔다.
- Recover와 Verify에서 실제로 같은 의미로 사용하는 Workspace 식별·안전한 접근·status 인계 계약만 `harness/workspace_contract.py`에 둔다.
- 한 책임만 사용하는 코드를 공유 영역으로 올리지 않는다.
- Project 기준은 `../project/`, 제품 코드·테스트는 Project root의 `src/`와 `tests/`에 두고 Harness 아래로 옮기거나 복제하지 않는다.
- `../project/README.md`와 `../project/overview.md`는 실제 Project common context의 최소 진입점이다. 기존 제품 문서를 그대로 복사하거나 링크만 나열하지 않고 여러 Workspace가 공유할 목적·구조·제약·채택 결정과 상세 Owner의 우선순위를 실제 내용으로 유지한다.
- 상세 제품 Owner, 코드나 채택 결정이 바뀌면 `../project/overview.md`를 다시 대조한다. 충돌한 overview를 최신 사실처럼 두지 않는다.
- Workspace `current/`, `source/`, `output/`, `records/`의 의미를 Harness가 독점 정의하지 않는다. 사람이 읽는 날짜별 records와 `records/receipts/<종류>/`의 기계 증거를 분리하고, Harness가 생성하더라도 receipt의 보존 Owner는 해당 Workspace로 유지한다.
- 작업별 Project context 선택은 `recover.json`, 검증 claim·canonical basis·고정 argv·evidence·실행 제한은 `verify.json`에서 변경한다. 사람의 다음 행동은 machine 계약이 아니라 사람용 current가 소유한다. Recover가 선택하는 Project context는 `context/project/` 아래 regular Markdown으로 제한한다.
- Project 문서·제품 evidence·검증 cwd는 Project root 기준, Workspace index·current·source·output·records는 이 Work root 기준으로 해석한다.
- 분석 메모·후보·비교·탈락안·선택 근거는 `records/` 바로 아래 날짜별 기록에 누적하고, 제품 검증 JSON은 `records/receipts/verify/`에 둔다. Goal을 위해 선택된 현재 산출물은 Workspace `output/index.md`에서 찾게 한다.
- 실제 산출물이 Project root의 코드·문서·테스트라면 Workspace `output/`에 복제하지 않고 `output/index.md`에서 canonical 상대 경로를 연결한다.

## 검증

전체 제품·Harness 검증은 Project root에서 다음 명령으로 실행한다.

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Harness 책임 재배치 뒤의 `recover → verify → recover` 연결은 실제 active Workspace가 아니라 임시 fixture를 쓰는 다음 Harness validation으로 확인한다.

```bash
python3 -m unittest \
  context.work.harness.validation.tests.test_ephemeral_workspace_state_preservation \
  -v
```

이 검사는 임시 Workspace에서 packet, `records/receipts/verify/` receipt, `current/state/status.json`의 연결을 확인하고 종료 시 모두 폐기한다. 반복 개발 확인은 직접 test 명령을 사용하고 durable Verify는 상태 전환이나 인계에 필요한 제품 검증 경계에서만 실행한다.

정적 설정·링크 검사와 Harness validation은 Maintain agent의 등록과 수정 가능 범위만 확인할 수 있다. 어떤 의미를 지속 Context에 남겨야 하는지와 그 내용의 충분성은 실제 Maintain 결과를 main이 근거·diff와 대조해야 확인된다.

검증 통과는 `verification_passed`라는 기계 사실이며 사람의 수락이나 Workspace 완료를 뜻하지 않는다. Acceptance와 완료 전이는 Verify 책임에 암묵적으로 추가하지 않는다.
