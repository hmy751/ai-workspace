# Work context 운영 규칙

이 파일은 `context/work/` 아래의 Workspace와 Harness를 다루는 작업 지침이다. Work context의 의미와 관계는 [`README.md`](README.md), Workspace collection의 의미는 [`workspaces/README.md`](workspaces/README.md), Harness 책임의 관계는 [`harness/README.md`](harness/README.md)가 각각 소유한다.

## 재진입과 검증

명령은 Project root에서 실행한다.

```bash
python3 -m context.work.harness recover
python3 -m context.work.harness verify --input-json path/to/evidence.json
```

- Recover의 목적·입력·출력·비소유 범위는 [`harness/recover/README.md`](harness/recover/README.md)가 정의한다.
- Maintain의 목적·활성 시점·Owner routing·비소유 범위는 [`harness/maintain/README.md`](harness/maintain/README.md)가 정의한다.
- Verify의 목적·입력·출력·비소유 범위는 [`harness/verify/README.md`](harness/verify/README.md)가 정의한다.
- Harness 자체 회귀 검증의 범위는 [`harness/validation/README.md`](harness/validation/README.md)가 정의한다.
- 지속 Workspace의 내부 관계는 [`workspaces/README.md`](workspaces/README.md)와 각 Workspace README가 정의한다.

## 책임과 활성 시점

- **Recover**: 새 세션이나 새 작업 주체가 선택한 Workspace에 재진입하거나 현재 context를 다시 구성해야 할 때 실행한다. 제한된 recovery packet을 읽기 전용으로 만들며 작업 중 context를 갱신하거나 제품 정합성을 입증하지 않는다.
- **Maintain**: Main 작업 세션마다 선택한 Workspace를 이해하는 Maintainer 하나를 두고, 매 사용자 대상 Main 응답 종료에서 durable 의미 변화만 [`Maintain 계약`](harness/maintain/README.md)에 따라 기존 Owner에 반영한다. 기존 Workspace의 첫 grounding 뒤에는 Maintain 때문에 Main 응답이나 관련 없는 다음 작업을 기다리게 하지 않는다.
- **Verify**: 다른 Owner가 이미 수행한 test·eval·수동 확인 중 지속해서 인계할 가치가 있는 결과를 입력받아 evidence receipt로 기록한다. 제품 명령을 실행하거나 status를 전이하거나 evidence의 충분성·acceptance를 결정하지 않는다.
- **Harness validation**: 작업 흐름의 단계가 아니라 Harness 자체 검증 경계다. Recover·Maintain·Verify 계약이나 구현이 바뀔 때 임시 Project/Workspace fixture에서 결정적 회귀 검사를 실행하고 실제 active Workspace의 receipt나 status를 생성·변경하지 않는다.

## Maintain session routing

Reference의 Maintain 의미 판단 agent 정의는 [`harness/maintain/workspace-context-maintainer.toml`](harness/maintain/workspace-context-maintainer.toml)이다. Project-scoped role `workspace_context_maintainer`는 Project root의 [`.codex/config.toml`](../../.codex/config.toml)이 이 파일을 `config_file`로 등록한다. Agent 정의, session runtime adapter와 Maintain 책임은 `harness/maintain/` 아래에 함께 두고, 루트 설정에는 발견에 필요한 얇은 연결만 둔다.

세션 시작에서 Main은 선택한 기존 Workspace 또는 새 Workspace를 형성 중이라는 경계를 Maintainer와 맞춘다. 기존 Workspace라면 Maintainer가 Workspace README와 `current/` index 중심으로 bounded grounding한 뒤 목표·현재 상태·다음 행동을 한 번 짧게 보여 준다. 새 Workspace라면 세션 대화를 따라가되 identity·goal·Owner가 형성되기 전에는 지속 문서를 추측해 만들지 않는다.

같은 conversation task·Workspace·worktree에서는 같은 Maintainer 이해를 유지하며 Main compaction만으로 다시 bootstrap하지 않는다. Maintainer는 Main이 매번 evidence 묶음을 포장하기를 기다리지 않고 세션 대화, 대상 Workspace, 관련 Project canonical, 실제 diff·파일·Git 상태와 test·Verify 결과 중 필요한 근거를 스스로 좁게 대조한다. 두 번째 응답부터 전체 history·records·repository를 다시 조사하지 않는다.

매 사용자 대상 Main 응답 종료에서 Maintainer가 직전 활동 이후 변화를 판단한다. No-change와 사소한 명확 반영은 조용히 끝내고, 중요한 명확 반영은 수정 뒤 짧게 보고한다. 의미·Owner·장기성·사용자 의도가 애매하면 쓰기 전에 즉시 질문하고 해당 반영만 보류한다. 일시적 runtime 실패는 먼저 자동 복구하며, 외부 canonical과 실제 상태에서 freshness를 복원할 수 없을 때만 짧게 경고한다.

Maintain 실행 주체는 다른 Workspace나 active index를 기본 탐색하지 않고, raw source snapshot·제품 코드·machine 계약·Verify receipt와 status를 수정하지 않는다. 변경 뒤 main은 실제 evidence와 diff를 대조하되 매 응답의 선행 병목으로 만들지 않는다. Agent가 등록되지 않은 실행 환경에서는 main이 [`Maintain 계약`](harness/maintain/README.md)에 따라 같은 의미 판단을 수행하지만, 이는 session continuity 자동화를 증명하지 않는다. 바깥 Project에 이름이 비슷한 maintainer가 있어도 이 Reference agent로 간주하지 않는다.

Project root의 `.codex/config.toml`, `.codex/context-maintain.json`, `.codex/hooks.json`은 선택한 Workspace와 Reference-owned Maintain 구현을 잇는 얇은 adapter다. Runtime 단위·통합 검사는 queue·cursor·warm runner·guarded write·restart 계약을 확인하지만, 실제 Codex host에서의 자동 시작과 별도 Codex session resume는 live acceptance 전까지 검증됐다고 보지 않는다.

## 변경 배치

- Recover 전용 규칙·구현·검증은 `harness/recover/`에서 함께 변경한다.
- Maintain 전용 의미 계약, session runtime adapter, Codex agent 정의와 검증은 `harness/maintain/`에서 함께 변경한다. `.codex/config.toml`은 발견에 필요한 얇은 연결만 두며 Maintain 규칙을 복제하지 않는다.
- Verify evidence 계약·구현·검증은 `harness/verify/`에서 함께 변경한다.
- Harness 자체 회귀 검증은 `harness/validation/`에서 변경한다. 공통 test fixture는 `harness/testing.py`에만 둔다.
- Recover와 Verify에서 실제로 같은 의미로 사용하는 Workspace 식별·안전한 접근만 `harness/workspace_contract.py`에 둔다. Legacy status 인계 검증은 Recover 읽기 호환으로만 유지한다.
- 한 책임만 사용하는 코드를 공유 영역으로 올리지 않는다.
- Project 기준은 `../project/`, 제품 코드·테스트는 Project root의 `src/`와 `tests/`에 두고 Harness 아래로 옮기거나 복제하지 않는다.
- `../project/README.md`와 `../project/overview.md`는 실제 Project common context의 최소 진입점이다. 기존 제품 문서를 그대로 복사하거나 링크만 나열하지 않고 여러 Workspace가 공유할 목적·구조·제약·채택 결정과 상세 Owner의 우선순위를 실제 내용으로 유지한다.
- 상세 제품 Owner, 코드나 채택 결정이 바뀌면 `../project/overview.md`를 다시 대조한다. 충돌한 overview를 최신 사실처럼 두지 않는다.
- Workspace `current/`, `source/`, `output/`, `records/`의 의미를 Harness가 독점 정의하지 않는다. 사람이 읽는 날짜별 records와 `records/receipts/<종류>/`의 기계 증거를 분리하고, Harness가 생성하더라도 receipt의 보존 Owner는 해당 Workspace로 유지한다.
- 작업별 Project context 선택은 `recover.json`에서 변경한다. 새 Verify evidence는 호출 시점의 입력이 소유하며 Workspace `verify.json`을 요구하지 않는다. 사람의 다음 행동은 machine evidence가 아니라 사람용 current가 소유한다. Recover가 선택하는 Project context는 `context/project/` 아래 regular Markdown으로 제한한다.
- Project 문서·제품 evidence·검증 cwd는 Project root 기준, Workspace index·current·source·output·records는 이 Work root 기준으로 해석한다.
- 분석 메모·후보·비교·탈락안·선택 근거는 `records/` 바로 아래 날짜별 기록에 누적하고, 선택적으로 기록한 검증 evidence JSON은 `records/receipts/verify/`에 둔다. Goal을 위해 선택된 현재 산출물은 Workspace `output/index.md`에서 찾게 한다.
- 실제 산출물이 Project root의 코드·문서·테스트라면 Workspace `output/`에 복제하지 않고 `output/index.md`에서 canonical 상대 경로를 연결한다.

## 검증

전체 제품·Harness 검증은 Project root에서 다음 명령으로 실행한다.

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Harness 책임 재배치 뒤의 `recover → evidence record → recover` 연결은 실제 active Workspace가 아니라 임시 fixture를 쓰는 다음 Harness validation으로 확인한다.

```bash
python3 -m unittest \
  context.work.harness.validation.tests.test_ephemeral_workspace_state_preservation \
  -v
```

이 검사는 임시 Workspace에서 recovery packet과 `records/receipts/verify/evidence-*.json` 기록을 확인하고 기존 `current/state/status.json`과 두 recovery packet의 의미가 바뀌지 않았음을 검증한 뒤 모두 폐기한다. 제품 test·eval·수동 확인은 해당 Owner가 직접 수행하고, Verify recorder는 그 결과 중 지속 가치가 있는 evidence만 선택적으로 남긴다.

정적 설정·링크 검사와 현재 Harness validation은 Maintain agent의 등록과 수정 가능 범위만 확인할 수 있다. 세션 수명, response-end 활동, background 비차단, restart 복구와 사용자 보고는 별도 live acceptance가 필요하며, 어떤 의미를 지속 Context에 남겨야 하는지와 작성 내용의 충분성은 실제 Maintain 결과를 evidence·diff와 대조해야 확인된다.

Evidence의 `outcome: pass`는 입력받은 확인 결과일 뿐 Verify가 제품을 다시 검증했거나 충분성을 판정했다는 뜻이 아니다. Acceptance와 완료 전이는 Verify 책임에 암묵적으로 추가하지 않는다.
