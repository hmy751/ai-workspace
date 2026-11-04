# Workspace Harness

이 디렉터리는 Workspace Context를 다시 읽고, 상태 전환에 필요한 제품 증거를 남기는 교체 가능한 관리 장치다. Context 자체의 의미와 책임 Owner는 [`Work context`](../README.md)와 [`Workspace collection`](../workspaces/README.md)에 남는다.

```bash
python3 -m context.work.harness recover [workspace_id] [--json]
python3 -m context.work.harness verify [workspace_id]
```

## 책임 계층

Harness의 두 책임은 각각 자기 목적·규칙·실행 방식의 진입점을 가진다.

- **Recover**: 새 세션·새 작업 주체의 Workspace 재진입에서 읽기 전용 packet을 만든다. 결정적 `recover` CLI와 [`recover/`](recover/)가 소유한다.
- **Verify**: Workspace 상태 전환·인계에 필요한 지속적 제품 증거를 남긴다. 결정적 `verify` CLI와 [`verify/`](verify/)가 소유한다.

**Harness validation**은 작업 흐름의 추가 단계가 아니라 위 관리 장치 자체의 회귀 검증 경계다. [`validation/`](validation/)이 임시 fixture에서 Recover·Verify 연결과 checked-in 제품 상태 격리를 검사한다. 사람의 목표·acceptance·완료 판단은 Harness 바깥에 남는다.

Work의 의미 갱신은 [record-work](../../../.agents/skills/record-work/SKILL.md)가 대상 작성 기준으로 수행한다. Verify는 제품 확인의 기계 증거, Harness validation은 관리 장치의 회귀를 담당한다. 기록 반영·검증 통과·사람 수락은 서로 다른 판단이다.

구현 파일의 배치는 다음과 같다.

- [`workspace/`](workspace/README.md): active/id 선택, identity-only `workspace.json`, 안전한 파일 접근, `status.json`과 receipt 연결 필드의 최소 공통 계약. 기존 [`workspace_contract.py`](workspace_contract.py)는 같은 공개 객체를 재노출하는 호환 경로다.
- [`recover/`](recover/): `recover.json`, current context 선택·로딩, 연결 receipt header와 선언된 snapshot freshness 확인, receipt 본문을 노출하지 않는 recovery packet과 사람용 출력
- [`verify/`](verify/): `verify.json`, evidence 선확보, 제한 실행, Workspace `records/receipts/verify/`의 append-only receipt, atomic status 갱신
- Recover의 코드·테스트 관계는 [Recover 구현 안내](recover/README.md#코드와-테스트를-읽는-순서), Verify는 [Verify 구현 안내](verify/README.md#코드와-테스트를-읽는-순서)에서 시작한다. 기존 `operation.py` 경로는 얇은 연결 파일로 유지한다.
- [`validation/`](validation/): 임시 Workspace 순환과 checked-in 제품 machine state 보존 검사
- [`testing.py`](testing.py): Recover·Verify·validation이 함께 사용하는 최소 fixture 기반. Verify 전용 subprocess 시나리오는 [Verify test support](verify/tests/support.py)가 소유한다.
- [`cli.py`](cli.py): Recover·Verify로 argument를 routing하고 결과를 출력
- [`__main__.py`](__main__.py): module 실행 진입점

Recover는 `verify.json`을 읽지 않고 Verify는 `recover.json`을 읽지 않으므로 한쪽 전용 계약 오류가 다른 명령의 실행을 막지 않는다.

Harness는 자신의 설치 위치를 Project 의미의 기준으로 사용하지 않는다. Project context·제품 evidence·검증 cwd는 Project root를, Workspace index·current·source·output·records는 [`Work root`](../README.md)를 기준으로 해석한다. Recover는 Workspace source를 기본 입력으로 읽지 않고 Workspace `output/index.md`만 산출물 지도로 읽으며, 연결된 산출물 본문은 자동으로 읽지 않는다. 이 장치를 제거해도 Workspace의 의미와 원자료·산출물 지도·기록은 [`../workspaces/`](../workspaces/)에서 읽을 수 있다.

책임별 테스트까지 모두 실행하려면 Project root에서 다음 명령을 사용한다.

```bash
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Harness의 끝까지 연결만 집중해 확인할 때는 임시 fixture에서 `recover → verify → recover`를 실행하는 다음 검사를 쓴다.

```bash
python3 -m unittest \
  context.work.harness.validation.tests.test_ephemeral_workspace_state_preservation \
  -v
```

이 검사가 만든 receipt와 status는 임시 디렉터리와 함께 폐기된다. 실제 active Workspace에서 durable verify를 실행하는 것은 Harness 회귀 검사가 아니라, 그 Workspace의 상태 전환이나 인계 증거가 필요할 때만 한다.
