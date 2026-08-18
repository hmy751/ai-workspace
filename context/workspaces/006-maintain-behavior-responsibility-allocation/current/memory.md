# Maintain behavior responsibility allocation memory

마지막 갱신: `2026-08-18`

## 목표

Workspace 005에서 구현한 Reference Maintain의 기능을 기본적으로 유지하면서, 내부 동작의 책임이 모델 판단, 명시적 규칙과 실행 장치, 사람 권한, 기록·검증 사이에 왜 그렇게 배치됐는지 이해하고 더 단순하고 응집된 코드·지침·prompt·문서 구조로 개선한다.

## 적용 기준

- 글로벌 [`ai-system_behavior-responsibility-allocation.md`](/Users/hammyeong-yeon/.claude/references/ai-system_behavior-responsibility-allocation.md)를 현재 판단 기준으로 사용한다.
- 구현 방식을 먼저 고르지 않고 운영상 하나인 동작의 시작 조건, 입력과 맥락, 결과와 부작용, 비목표와 반드시 지킬 약속을 먼저 식별한다.
- 각 책임을 해석·선택, 보장·거부, 권한·승인, 실행·기록으로 구분한다.
- 의미가 맥락에 따라 달라지는 선택은 모델 판단에 남길 이유를 검토하고, 명확한 predicate와 반복 가능한 거부가 필요한 약속은 schema·validator·permission·code 같은 집행 장치를 검토한다.
- 가치·정책·중요한 예외·되돌리기 어려운 결과·acceptance는 자동화 가능성만으로 모델이나 코드의 권한으로 올리지 않는다.
- 지침은 준수를 표현하고, schema는 허용 형태를 정의하며, validator·code는 실행 시 거부를 집행하고, test·eval은 구현이나 행동의 증거라는 차이를 유지한다.
- 장치를 추가하거나 유지할 때 얻는 보장과 함께 새 상태·실패·복구·검증 책임을 비교한다.
- 책임을 옮기거나 제거할 때 무엇이 달라지는지 일반적인 진입점에서 다시 찾을 수 있어야 한다.

## 현재 경계

- 주 대상은 [`reference-project/context/work/harness/maintain/`](../../../../reference-project/context/work/harness/maintain/)이 소유한 Maintain 계약과 구현이다.
- Root `.codex/`는 선택 Workspace와 Reference 구현을 연결하는 얇은 adapter로 유지하며 semantic contract를 복제하지 않는다.
- Workspace 005의 완료 구현과 proof는 baseline이지 이 Workspace의 current가 아니다. 필요한 결론은 링크로 선택하고 상세 이력을 복제하지 않는다.
- 사용자-facing 기능 변경은 기본 목표가 아니다. 현재 동작을 바꿔야 한다는 판단이 생기면 근거와 영향을 먼저 드러내고 사용자와 별도로 결정한다.
- 구체적인 개선 대상, 우선순위, acceptance와 변경 단위는 아직 정하지 않았다.

## 소유권

- 실제 재사용 가능한 코드·계약·prompt·schema·test 개선은 `reference-project/`가 소유한다.
- Workspace 006의 `current/`는 현재 판단과 커서, `records/`는 분석·결정·검증 과정, `output/index.md`는 선택된 실제 canonical을 연결한다.
- 사용자는 목표, 정책, 중요한 예외, 기능 변화와 acceptance를 결정한다. Main은 근거를 대조하고 개선안을 구현·검증하며, Maintainer는 확정된 durable 변화만 기존 Workspace Owner에 반영한다.
