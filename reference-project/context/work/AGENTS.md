# Work context 운영 규칙

이 파일은 `context/work/` 아래의 Workspace와 Harness를 다루는 작업 지침이다. Work context의 의미와 관계는 [`README.md`](README.md), Workspace collection의 의미는 [`workspaces/README.md`](workspaces/README.md), Harness 책임의 관계는 [`harness/README.md`](harness/README.md)가 각각 소유한다.

## 재진입과 검증

명령은 Project root에서 실행한다.

```bash
python3 -m context.work.harness recover
python3 -m context.work.harness maintain bootstrap <workspace_id>
python3 -m context.work.harness verify
```

- Recover의 목적·입력·출력·비소유 범위는 [`harness/recover/README.md`](harness/recover/README.md)가 정의한다.
- Maintain의 목적·활성 시점·Owner routing·비소유 범위는 [`harness/maintain/README.md`](harness/maintain/README.md)가 정의한다.
- Verify의 목적·입력·출력·상태 반영 범위는 [`harness/verify/README.md`](harness/verify/README.md)가 정의한다.
- Harness 자체 회귀 검증의 범위는 [`harness/validation/README.md`](harness/validation/README.md)가 정의한다.
- 지속 Workspace의 내부 관계는 [`workspaces/README.md`](workspaces/README.md)와 각 Workspace README가 정의한다.

## 책임과 활성 시점

- **Recover**: 새 세션이나 새 작업 주체가 선택한 Workspace에 재진입하거나 현재 context를 다시 구성해야 할 때 실행한다. 제한된 recovery packet을 읽기 전용으로 만들며 작업 중 context를 갱신하거나 제품 정합성을 입증하지 않는다.
- **Maintain**: 새 작업 session에서 explicit Workspace의 bounded Recover packet으로 semantic agent를 한 번 grounding한다. 그 뒤 모든 사용자 대상 Main response-end를 같은 agent가 점검하며, 명확한 변화만 guarded apply를 거쳐 기존 Owner에 반영한다. No-change는 write·report 없이 끝내고 ambiguity는 관련 write 전에 사용자에게 돌린다.
- **Verify**: Workspace 상태 전환이나 인계에 남길 지속적인 제품 증거가 필요할 때 실행한다. `verify.json`의 고정 명령을 실행하고 receipt와 machine status를 남기지만 context의 의미를 갱신하거나 사람의 acceptance를 결정하지 않는다.
- **Harness validation**: 작업 흐름의 단계가 아니라 Harness 자체 검증 경계다. Recover·Verify 계약이나 구현이 바뀔 때 임시 Project/Workspace fixture에서 결정적 회귀 검사를 실행하고 실제 active Workspace의 receipt나 status를 생성·변경하지 않는다.

## 새 Workspace 생성과 전환

새 Workspace를 만들거나 현재 작업을 후속 Workspace로 분리하는 요청에는 repo-local [`create-context-workspace` skill](../../.agents/skills/create-context-workspace/SKILL.md)을 사용한다. Skill과 main은 [`생성·전환 canonical`](workspaces/CREATE-AND-TRANSITION.md)을 적용하며, 상세 의미를 이 운영 파일에 다시 정의하지 않는다.

기존 Workspace의 단순 재진입·수정이나 이미 만든 Workspace로의 전환에는 생성 skill을 다시 사용하지 않는다. 생성과 actual activation은 별도 경계다. 전환 요청에서는 canonical에 따라 현재 binding과 Maintain의 처리 중·pending·failed 상태가 successor 판단에 미치는 영향을 확인하고, 같은 Main session을 이어 갈지 새 session으로 격리할지 정한다.

## Maintain agent routing

Main이 자동 lifecycle 없이 수동 fallback으로 호출할 Maintain role 정의는 [`harness/maintain/workspace-context-maintainer.toml`](harness/maintain/workspace-context-maintainer.toml)이다. Project-scoped role `workspace_context_maintainer`는 Project root의 [`.codex/config.toml`](../../.codex/config.toml)이 이 파일을 `config_file`로 등록한다. 자동 경로는 이 등록 role을 시작하는 것이 아니라 `codex_session.py`가 같은 Maintain 계약을 읽는 별도 persisted thread를 시작하고 hook adapter가 lifecycle을 연결한다. Agent 계약과 Maintain 책임은 Work 아래에 두고, 루트 설정에는 수동 role 발견에 필요한 경로만 둔다.

새 session에서 main 또는 host adapter는 현재 작업의 명시적 `workspace_id`와 explicit Recover packet을 `workspace_context_maintainer`에게 한 번 전달한다. 같은 session의 모든 사용자 대상 Main response-end에는 이번 사용자 발화와 Main response를 같은 agent identity에 전달한다. 이미 입력에 포함된 제한된 실제 근거나 기존 Verify 결과가 있으면 그 입증 범위도 보존할 수 있지만, host adapter나 Maintainer가 repository 전체 diff·Git 상태·test/eval evidence를 기본 수집하거나 새 검증을 실행하지 않는다. 새 Main session은 다시 bounded grounding하며, 살아 있는 session에서 warm identity가 사라지면 warm이라고 가장하지 않고 실패로 드러낸다. 같은 outer session의 자동 re-grounding은 보장하지 않는다.

Maintain semantic agent는 read-only이며 다른 Workspace나 active index를 기본 탐색하지 않는다. Structured decision의 수정 후보는 guarded apply만 실행하며 raw source snapshot·제품 코드·machine 계약·Verify receipt·status와 active index를 거부한다. Important 결과는 실제 apply 성공 뒤에만 보고하고, agent 보고나 정적 검사가 사용자 acceptance를 대신하지 않는다. 바깥 Project에 이름이 비슷한 maintainer가 있어도 이 Reference agent로 간주하지 않는다.

Project agent role 등록만으로 자동 session·warm reuse·매 response-end·비차단이 생기지는 않는다. 이 Reference의 [hook 설정](../../.codex/hooks.json)과 [`host_adapter.py`](harness/maintain/host_adapter.py)는 [explicit binding](../../.codex/maintain.json)을 `SessionStart → UserPromptSubmit → Stop → SessionEnd`에 연결한다. Hook이 없거나 trusted·actual acceptance되지 않은 환경에서는 main이 같은 흐름을 수동으로 수행하며 automatic Maintain을 주장하지 않는다.

## 변경 배치

- Recover 전용 규칙·구현·검증은 `harness/recover/`에서 함께 변경한다.
- Maintain 전용 실행 계약, guarded boundary, session bridge, host adapter, test와 Codex agent 정의는 `harness/maintain/`에서 함께 변경한다. `.codex/config.toml`은 role의 발견 경로, `.codex/maintain.json`은 explicit Workspace binding, `.codex/hooks.json`은 lifecycle command 경로만 소유하며 Maintain 의미 규칙을 복제하지 않는다.
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

정적 설정·링크 검사와 unit test는 Maintain의 등록, bounded bootstrap과 guarded side-effect 범위만 확인할 수 있다. 어떤 의미를 지속 Context에 남겨야 하는지, 같은 session 이해·response-end cadence·Main 비차단과 사용자 보고가 실제로 성립하는지는 semantic eval과 actual host acceptance로 따로 확인한다.

검증 통과는 `verification_passed`라는 기계 사실이며 사람의 수락이나 Workspace 완료를 뜻하지 않는다. Acceptance와 완료 전이는 Verify 책임에 암묵적으로 추가하지 않는다.
