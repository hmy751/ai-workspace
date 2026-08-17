# Workspace Harness

이 디렉터리는 Workspace Context를 다시 읽고, 작업 중 의미 변화를 기존 Owner에 반영하고, 이미 수행된 검증 evidence를 남기는 교체 가능한 관리 장치다. Context 자체의 의미와 책임 Owner는 [`Work context`](../README.md)와 [`Workspace collection`](../workspaces/README.md)에 남는다.

```bash
python3 -m context.work.harness recover [workspace_id] [--json]
python3 -m context.work.harness verify [workspace_id] --input-json path/to/evidence.json
```

## 책임 계층

작업 Context의 세 책임은 각각 자기 목적·규칙·실행 방식의 진입점을 가진다.

- **Recover**: 새 세션·새 작업 주체의 Workspace 재진입에서 읽기 전용 packet을 만든다. 결정적 `recover` CLI와 [`recover/`](recover/)가 소유한다.
- **Maintain**: Main 작업 세션마다 선택한 Workspace 이해를 유지하고, 매 사용자 대상 Main 응답 종료에서 durable 의미 변화만 기존 Context Owner에 반영한다. [`maintain/`](maintain/)이 의미 계약, session runtime adapter, [Codex agent 정의](maintain/workspace-context-maintainer.toml)와 검증을 함께 소유한다. 초기 grounding 뒤에는 Main을 기다리게 하지 않는다.
- **Verify**: 다른 주체가 이미 수행한 test·eval·수동 확인의 결과, 재접근 위치, 미검증 범위를 append-only evidence로 기록한다. 제품 검증 실행과 상태 전환은 소유하지 않는다. 결정적 `verify` CLI와 [`verify/`](verify/)가 소유한다.

**Harness validation**은 작업 흐름의 네 번째 단계가 아니라 위 관리 장치 자체의 회귀 검증 경계다. [`validation/`](validation/)이 임시 fixture에서 Recover, Verify evidence 기록, legacy 호환과 checked-in 제품 상태 격리를 검사한다. 사람의 목표·acceptance·완료 판단은 Harness 바깥에 남는다.

Maintain은 Context 의미 정합성, Verify는 이미 나온 검증 evidence의 선택적 보존, Harness validation은 관리 장치의 회귀를 담당한다. 하나의 인계 경계에서 Maintain과 Verify가 모두 필요할 수 있지만 한쪽의 동작이 다른 쪽이나 제품 검증·사람 acceptance를 대신하지 않는다.

구현 파일의 배치는 다음과 같다.

- [`workspace_contract.py`](workspace_contract.py): active/id 선택, identity-only `workspace.json`, Work root 내부의 안전한 파일 접근, `status.json`과 receipt 연결 필드의 최소 공통 계약
- [`recover/`](recover/): `recover.json`, current context 선택·로딩, 연결 receipt header와 선언된 snapshot freshness 확인, receipt 본문을 노출하지 않는 recovery packet과 사람용 출력
- [`maintain/`](maintain/): 세션 동안 Workspace 이해를 유지하고 response-end마다 durable 변화만 기존 Owner에 배치하는 계약, queue·cursor·warm runner·guarded writer를 가진 교체 가능한 runtime adapter와 Codex agent 정의
- [`verify/`](verify/): 이미 수행된 검증 evidence의 입력 검증과 Workspace `records/receipts/verify/evidence-*.json` append-only 기록
- [`validation/`](validation/): 임시 Workspace의 Recover·evidence-recording 순환, legacy 읽기 호환과 checked-in 제품 machine state 보존 검사
- [`testing.py`](testing.py): Recover·Verify·validation 테스트가 함께 사용하는 최소 fixture 기반
- [`cli.py`](cli.py): 두 책임으로 argument를 routing하고 결과를 출력
- [`__main__.py`](__main__.py): module 실행 진입점

공용 CLI는 Recover와 Verify evidence recorder를 routing한다. Maintain의 의미는 특정 command나 schema가 아니라 세션형 책임 계약이 소유하고, 현재 Codex hook·queue·checkpoint·warm `codex exec resume`·reporting 조합은 `maintain/` 안의 교체 가능한 adapter다. Verify는 `recover.json`, legacy `verify.json`, `status.json`을 읽거나 바꾸지 않으므로 그 파일의 오류가 evidence 기록을 막지 않는다.

Maintain adapter의 단위·통합 검사는 session 격리, response pairing, cursor, fake Codex process의 bootstrap/resume, guarded write와 retry/report 계약을 확인한다. 실제 Codex host와 별도 Codex session을 연결한 end-to-end 동작은 별도 live acceptance 전까지 검증됐다고 보지 않으며 Recover·Verify validation을 그 증거로 사용하지 않는다.

Harness는 자신의 설치 위치를 Project 의미의 기준으로 사용하지 않는다. Project context와 제품 코드·test의 Owner는 Project root에, Workspace index·current·source·output·records는 [`Work root`](../README.md)에 남는다. Recover는 Workspace source를 기본 입력으로 읽지 않고 Workspace `output/index.md`만 산출물 지도로 읽으며, 연결된 산출물 본문은 자동으로 읽지 않는다. Verify의 `source_refs`는 재접근 문자열일 뿐 Harness가 열거나 검증하는 경로가 아니다. 이 장치를 제거해도 Workspace의 의미와 원자료·산출물 지도·기록은 [`../workspaces/`](../workspaces/)에서 읽을 수 있다.

책임별 테스트까지 모두 실행하려면 Project root에서 다음 명령을 사용한다.

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Harness의 끝까지 연결만 집중해 확인할 때는 임시 fixture에서 `recover → evidence record → recover`를 실행하는 다음 검사를 쓴다.

```bash
python3 -m unittest \
  context.work.harness.validation.tests.test_ephemeral_workspace_state_preservation \
  -v
```

이 검사가 만든 evidence receipt는 임시 디렉터리와 함께 폐기되고 status는 바뀌지 않는다. 실제 active Workspace에 evidence를 기록하는 것은 지속 가치가 있고 미검증 범위를 함께 남길 때만 선택한다.
