# Maintain clean-room reimplementation memory

마지막 갱신: `2026-08-18`

## 목표

Workspace 005에서 사용자와 합의한 Maintainer 경험을 `reference-project/`에 재사용 가능하게 구현한다. 이전 구현을 줄이는 작업이 아니라, 사용자 장면과 글로벌 책임 원칙에서 필요한 구조를 다시 도출하는 작업이다.

## 보존할 사용자 장면

1. 기존 Workspace의 새 세션은 필요한 current만 bounded하게 읽고 목표·현재 상태·다음 행동을 한 번 맞춘다.
2. 같은 작업 세션에서는 Maintainer가 이미 얻은 이해를 이어 쓰며 매 응답마다 전체 history·records·repository를 다시 조사하지 않는다.
3. 매 사용자 대상 Main 응답 종료에는 그동안 생긴 변화를 점검한다.
4. Durable 변화가 없으면 persistent write도 사용자 보고도 하지 않는다.
5. 명확한 durable 변화는 올바른 기존 Owner에 반영한다. 사소하면 조용히 끝내고 중요하면 반영 뒤 짧게 알리며, 의미·Owner·장기성·사용자 의도가 애매하면 관련 write 전에 묻는다.
6. 초기 grounding 뒤 Main은 Maintain 완료를 기다리지 않는다. 실패하거나 뒤처진 상태를 fresh·completed로 가장하지 않으며, 다음 세션도 stale current를 정상 handoff로 오해하지 않는다.

이 장면은 구현 기술명이 아니라 관찰 가능한 계약이다. 특정 hook, queue, storage, cursor schema, CLI, process lifetime이나 UI 채널을 요구하지 않는다.

## 책임 배치

- 모델은 대화와 실제 근거를 종합해 durability, 기존 Context Owner, ambiguity와 사용자에게 보고할 중요도를 판단한다.
- 규칙 기반 장치는 명시적으로 표현 가능한 경계만 반복 가능하게 집행한다. 최소 후보는 선택된 Workspace와 허용된 write 대상, path traversal·symlink, stale baseline, 실패의 false success 거부다. 후보마다 실제로 지키는 약속과 더 단순한 대안이 있는지 다시 증명한다.
- 사람은 Workspace 선택, 목표·정책, 중요한 예외, 되돌리기 어려운 권한, 기능 변화와 acceptance를 소유한다.
- Main과 실제 제품 Owner는 코드·문서 작업과 필요한 test·eval·수동 확인을 수행한다. Verify는 보존 가치 있는 기존 증거를 기록할 수 있지만 제품 검증 주체가 아니다.
- Hook·runtime·warm thread는 Maintainer 동작을 돕는 제거 가능한 adapter 또는 cache다. 이 장치의 내부 상태는 Workspace 의미의 canonical이 아니다.

## Canonical과 구조 경계

- Workspace의 정체성·범위와 `current`·`output`·`records` 관계는 Workspace README가 정의한다.
- 현재 의미는 Workspace README·current, 상세 이유는 선택된 records, 실제 구현 사실은 실제 파일·Git·test 결과가 소유한다.
- 재사용 가능한 Maintain 책임·구현·검증은 Reference에서 함께 발견되어야 한다. Root는 실제 acceptance 뒤 선택한 Workspace와 Reference를 연결하는 얇은 adapter만 가질 수 있다.
- 사람이 내부 machine state부터 역추적하지 않고 현재 문제·판단 지점·근거·다음 지시 대상을 찾을 수 있어야 한다.
- Adapter를 제거해도 Workspace 의미, 관리 기준과 사람의 권한이 남아야 한다.

## 설계 금지선

- `9553d0a` 또는 006 diff의 파일·state machine을 보존 조건으로 삼지 않는다.
- Queue·ledger·journal·completion marker·report acknowledgement·migration을 사용자 장면과 같은 수준의 요구사항으로 올리지 않는다.
- 모호한 의미 정책을 enum·schema·분기로 숨겨 정확한 보장인 것처럼 만들지 않는다.
- Unit test와 fake process만으로 actual host delivery, warm continuity, background 비차단이나 semantic 품질을 acceptance하지 않는다.
- 새 구현을 실제 host에서 확인하기 전에 root automatic hook·agent를 다시 활성화하지 않는다.

## 구현을 고르는 질문

- 이 구성요소가 없으면 위 여섯 장면 중 무엇이 실제로 깨지는가?
- 기존 platform 제약이나 더 단순한 schema·permission·검사로 같은 보장을 얻을 수 있는가?
- 이 장치가 만든 내부 상태를 관리하기 위해 또 다른 복구 장치를 추가하는 것은 아닌가?
- 책임을 제거·교체해도 지속 의미와 사람의 권한을 찾을 수 있는가?
- 구현·검증 산출물이 하나의 책임을 이해하기 위해 다시 조립해야 할 만큼 흩어지지는 않았는가?
