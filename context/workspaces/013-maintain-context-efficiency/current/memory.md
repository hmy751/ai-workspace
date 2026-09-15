# 목표와 기준

마지막 갱신: `2026-09-15`

## 목표

Maintain이 이전 대화에서 형성한 목표·결정·열린 문제를 이어 가는 능력은 유지하면서, 그 연속성을 무제한 Codex transcript 재생에 의존하지 않게 한다. 공통 개선은 Reference Maintain에 구현하고, 같은 계약을 Noline의 host 차이와 기존 연결을 보존해 적용한다.

## 성공 기준

- 이전 판단의 의미와 provenance를 잃지 않고 새 semantic thread가 후속 `no_change`, `updated`, `needs_user_decision` 판단을 이어 갈 수 있다.
- 과거 shell 출력, 완료된 decision JSON, 반복된 계약 본문은 rollover 뒤 기본 입력에서 제외한다.
- 잘못된 Workspace write, 허용되지 않은 Owner write, ambiguity 누락은 0건이어야 한다.
- 한 response-end의 자료 탐색이 반복 모델 cycle로 무한히 늘지 않는다. 필요한 Owner를 한 번에 요청·제공하고 제한 안에 판단하지 못하면 성공으로 가장하지 않는다.
- raw prompt·Main response와 event ordering은 비용 제한 때문에 삭제하지 않는다. 모델 해석을 지연하거나 thread를 교체해도 원자료에서 재현할 수 있어야 한다.
- 사용량 receipt가 호출 수, raw·cached·uncached input, output·reasoning token, tool cycle과 rollover 이유를 보여 준다.
- Reference replay와 Noline 적용 검증을 구별하고, source 통과만으로 target 동작 완료를 주장하지 않는다.

## 유지할 결정

- 연속성의 정본은 전체 대화 transcript가 아니라 Workspace Context와 검증 가능한 semantic checkpoint다.
- Codex 자동 compact는 context window 소진을 막는 fallback이다. 비용 최적화의 주 장치로 채택하지 않는다.
- 초기 구조 후보는 전용 instruction isolation, batched Owner read, response-end당 모델 cycle 상한, host가 검증하는 semantic checkpoint와 bounded thread rollover다.
- rollover 기준의 `64k 누적 입력` 또는 `8 response-end`는 실측에서 출발한 시험값일 뿐 확정 계약이 아니다. replay 결과로 조정한다.
- 현재 `gpt-5.6-sol`과 `high` 설정은 구조 비교의 baseline으로 유지한다. medium 비교는 구조 개선 뒤 별도 평가한다.
- AI-native moment reviewer 비활성 상태와 Workspace 012의 active 표기는 이번 작업과 독립적으로 보존한다.

## 대상과 소유권

- Source: [`reference-project/context/work/harness/maintain/`](../../../../reference-project/context/work/harness/maintain/)
- Target: Noline 저장소의 `context/work/harness/maintain/`
- Source의 이전 동작 계약: [Workspace 007](../../007-maintain-clean-room-reimplementation/)
- Target 적용·평가 이력: [Workspace 011](../../011-noline-harness-upgrade/)

이 Workspace는 과거 기록을 다시 canonical로 만들지 않는다. 구현 시점에는 현재 Source와 Target 코드를 직접 읽고, 과거 record는 선택 이유와 검증 상한을 복원하는 근거로만 사용한다.
