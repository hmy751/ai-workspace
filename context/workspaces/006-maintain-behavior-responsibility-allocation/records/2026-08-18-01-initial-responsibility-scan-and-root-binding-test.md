# 착수 기준선과 Maintain 개선 범위

날짜: `2026-08-18`

## 다시 고정한 작업 범위

초기 정적 점검에서는 `changed_paths`를 가장 작은 후속 개선 후보로 너무 일찍 올리고, root Workspace binding test 정리를 첫 개선 완료로 표현했다. 사용자 확인 뒤 Workspace 005의 전체 작업 범위와 글로벌 `ai-system_behavior-responsibility-allocation.md` 및 연결 reference, Reference Project의 Maintain canonical과 구현을 다시 읽고 범위를 바로잡았다.

- 실제 개선 대상은 Workspace 005에서 만든 `reference-project/context/work/harness/maintain/` 구현이다.
- Workspace 005의 문서와 commit `9553d0a`는 기존 의도·동작·proof ceiling을 복원하는 근거이며 수정 대상이 아니다.
- 글로벌 `ai-system_*` reference는 모델·규칙 기반 장치·사람 사이의 책임 배치를 평가하는 렌즈이며, 독립된 새 목표나 구현 대상으로 올리지 않는다.
- Root `.codex/`는 active Workspace와 Reference runtime을 연결하는 얇은 dogfood adapter로 유지한다.
- Workspace 006은 분석, 결정, 변경 이유와 검증 결과를 추적한다. 실제 canonical 구현은 Reference Maintain에 둔다.

## 이전 작업에서 유지할 동작 계약

Workspace 005에서 사용자와 확정한 핵심은 한 Main session 동안 같은 Maintainer가 bounded grounding 뒤 warm understanding을 유지하고, 매 user-facing response end에서 Context 변화 여부를 판단하는 것이다.

- 지속할 변화가 없으면 파일을 쓰거나 보고하지 않는다.
- 명확하고 사소한 변화는 안전하게 반영하되 사용자에게 별도 보고하지 않는다.
- 명확하고 중요한 변화는 안전하게 반영한 뒤 보고한다.
- 내용이나 Owner가 모호하면 쓰기 전에 사용자에게 묻고, 무관한 Main 작업은 계속 진행한다.
- 복구 가능한 실패는 먼저 조용히 복구하고, freshness를 회복할 수 없을 때만 사용자에게 경고한다.
- Verify는 제품 검증 주체가 아니라 이미 실행된 직접 증거를 append-only로 기록한다.
- 정적·fake-process test는 deterministic 경계를 증명할 뿐 live nested Codex, fresh host, UI delivery와 semantic 품질 acceptance를 대신하지 않는다.

이번 작업은 이 user-facing 결과를 기본적으로 보존하면서 내부 판단·보장·권한·실행 책임의 중복과 빈틈을 줄인다.

## 현재 기준선과 portable test 결합

현재 HEAD `ffa8cdf`는 root Maintain binding을 Workspace 005에서 006으로 바꿨지만, `reference-project/context/work/harness/maintain/`의 구현과 test는 baseline commit `9553d0a` 이후 바뀌지 않았다.

- `9553d0a` archive에서 Maintain test `165/165` 통과를 재현했다.
- 변경 전 현재 HEAD에서는 같은 165개 중 1개만 실패했다.
- 실패한 `test_manual_fallback_is_portable_and_root_connection_stays_thin`은 root `workspace_id`를 과거 선택값 `005-context-continuity-maintenance`로 고정했다.
- 현재 root config를 실제 loader로 읽으면 Workspace 006이며 `workspace_bound: true`다. Production runtime 회귀가 아니라 가변 root 선택값을 portable Reference invariant로 둔 test 결합이다.

현재 diff는 exact Workspace ID assertion을 제거하고 안전한 binding과 thin connection 검증을 유지한다. Targeted config test `8/8`, Maintain test `165/165`, Reference 전체 test `223/223`가 통과했다. 이는 검증된 기준선 test 책임 수정이며 Production Maintain behavior 개선과는 구분한다.

## 본격 분석할 하나의 동작

첫 분석 단위는 파일이나 개별 필드가 아니라 `response-end 의미 판단 → guarded write → report/checkpoint commit`의 전체 흐름이다.

- 시작 조건: Main이 user-facing 응답을 마치고 Stop evidence가 durable queue에 들어온다.
- 입력과 맥락: session grounding, 사용자 발화와 응답, tool evidence, Workspace canonical, 현재 Git·파일 상태, 이전 checkpoint와 미완료 intent다.
- 결과: `no_change`, 조용한 write, write 후 report, clarification, 또는 freshness 복구 결과 중 계약에 맞는 상태가 된다.
- 부작용: 허용된 Workspace context 파일 변경, intent·checkpoint·report·runtime state 기록이 생길 수 있다.
- 비목표: 사용자 목표나 새 정책을 Maintainer가 대신 결정하는 것, 제품 test를 대신 실행하는 것, 다른 Workspace를 갱신하는 것, root adapter에 의미 판단을 복제하는 것.
- 불변식: write 전 허용 경로·baseline·link를 검증하고, 모호할 때는 쓰지 않으며, crash 뒤 같은 요청을 중복 적용하지 않고, 성공하지 않은 결과를 checkpoint로 확정하지 않는다.

## 확인할 책임 배치

아래는 결론이 아니라 코드와 characterization test로 확인할 작업 지도다.

- 모델: 변화의 지속성, 적절한 Owner, 중요도와 갱신 내용을 맥락적으로 판단한다.
- prompt: 이전 동작 계약과 판단 절차를 모델에 표현한다.
- schema/parser: 결과 형태와 outcome-write 조합 같은 기계적 일관성을 검증한다.
- controller: event evidence, Workspace binding과 모델 결정을 연결하고 실행 가능한 요청만 writer로 넘긴다.
- intent: 판단 완료와 write/report 완료 사이 crash window에서 요청 identity와 재개 상태를 보존한다.
- writer: 허용 경로, baseline, symlink·link, transaction과 실제 changed path를 강제한다.
- runtime: event 순서, worker 수명, retry, checkpoint, report와 freshness 상태 전이를 소유한다.
- 사람: 목표·정책·예외·모호성 해소와 live/semantic acceptance를 소유한다.

## 아직 선택하지 않은 관찰

- `changed_paths`는 agent decision, parser, controller, intent/report와 writer 결과에 반복되며 순서 차이가 retry로 이어질 가능성이 있다.
- `freshness_failed`는 schema outcome에 있지만 prompt trigger와 runtime commit 의미가 분명히 맞물리는지 확인이 필요하다.
- Warm `codex exec resume`의 read-only 경계는 host/session 동작에 의존하므로 정적 refactor만으로 acceptance할 수 없다.

이 셋은 조사 단서일 뿐 다음 개선으로 선택하지 않았다.

## 착수 순서

1. 완료: binding-test diff에 대해 Reference 전체 test `223/223`를 통과했다.
2. response-end 흐름의 기존 user-facing 결과와 crash/retry 경계를 characterization test로 고정한다.
3. 위 책임 지도를 실제 호출·상태 전이·검증 코드와 대조한다.
4. 책임 중복이나 빈틈이 확인된 최소 세로 슬라이스 하나를 선택한다.
5. Targeted test, Maintain 전체 test, Reference 전체 test와 필요한 정적 검증을 통과시킨다.
6. 실제 결과가 생긴 뒤에만 `current/`와 `output/`을 완료 상태로 갱신한다.

Live nested Codex나 host acceptance가 필요해지는 변경은 deterministic test와 구분하고, 실행 전에 범위와 관찰할 결과를 드러낸다.
