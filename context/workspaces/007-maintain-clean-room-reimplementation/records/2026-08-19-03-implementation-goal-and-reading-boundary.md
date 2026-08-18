# 구현 목표와 clean-room 읽기 경계 재확인

날짜: `2026-08-19`

상태: **사용자 정정 반영 / 구현 착수 기준**

## 이 기록의 역할

Workspace 007의 clean-room이 과거 구현을 더 분석하는 작업이나 글로벌 reference를 정리하는 문서 작업으로 오해되지 않게 한다. Workspace 005에서 형성된 Maintainer 경험, Workspace 006을 거쳐 007로 전환한 이유, reset된 `reference-project/`에 실제 구현해야 하는 목표와 더 읽지 않을 과거 범위를 고정한다.

이 기록은 [behavior contract](2026-08-18-01-clean-room-source-and-behavior-contract.md)나 [code baseline](2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md)을 대체하지 않는다. 이번 대화에서 사용자가 바로잡은 두 기록의 해석과 다음 작업 경계만 소유한다.

## 사용자 정정의 최소 원문

문제가 실제 사용 뒤 발견된 동작 실패가 아니라 구현 전 구조 판단에 있었다는 점은 다음 발화로 확인됐다.

> 사용 전에 이미 구조나 이런거 였어 그래서 글로벌 레퍼런스를 다시 준거고 이전 작업들에서는 명시된 글로벌 레퍼런스를 참조하지 않았거든

Reset은 구현을 없애기 위한 결론이 아니라 새 구현을 위한 출발점이라는 점도 명시됐다.

> 그러니까 구현해야되는건 맞아 왜냐면 이미 refence-project를 부모 커밋 그때 상황으로 되돌려놨으니 구현도 해야하는게 맞는데 그 레퍼런스 관점도 잇어야 된다 이거지

Workspace 005에서 넘어온 사용자-facing mental model은 다시 발굴할 후보가 아니라 구현에 사용할 거의 확정된 기준이다.

> 근데 중요한건 005에서 넘어온 멘탈모델은 충분해? 그건 거의 확정이고 구현할때 필요할거잖아

과거 자료를 더 읽어 새 설계의 암묵적 기준으로 만드는 것도 피해야 한다.

> 하여튼 이미 상황을 인지하거면 더 읽지 말고 또 기준삼을까 우려되네

## 바로잡은 작업 해석

### 005 → 006 → 007의 관계

- Workspace 005에서는 Maintain의 문제와 사용자-facing 경험을 논의하고 구현까지 진행했다.
- Workspace 006에서는 이미 완결된 형태의 기존 구현을 개선하려 했지만, 그 구현이 만든 구조·migration·compatibility가 계속 판단을 구속했다.
- Workspace 007은 구현을 포기한 분석 Workspace가 아니다. Live `reference-project/`를 구현 전 baseline으로 되돌린 뒤, 005의 mental model과 글로벌 책임 기준에서 Reference Maintain을 실제로 다시 구현하는 Workspace다.

따라서 과거 구현이 실제 사용에서 실패했다는 서사를 새 설계의 출발점으로 삼지 않는다. 실제 host에서 확인된 negative evidence는 proof ceiling으로 유지하지만, 007로 전환한 직접 이유는 사용 전에 이미 구조와 책임 배치가 목적을 충분히 반영하지 못했다고 판단한 데 있다.

### 글로벌 reference의 역할

글로벌 `ai-system_*` reference는 구현 대신 제출할 분석 산출물이나 완성 뒤 붙이는 감사표가 아니다. 다음을 구현 전에 다시 도출하는 판단 기준이다.

- 자연어 의미 판단, deterministic 보장과 사람 권한의 배치
- Maintain이라는 하나의 책임과 하위 구성의 응집
- Workspace Context canonical·실제 내용·관리 장치·책임 Owner의 분리
- 사람이 현재 문제·상태·판단 지점에 진입하는 경로
- Hook·agent·runtime을 제거해도 지속 의미가 남는 구조

Reference 적용은 코드를 미루는 이유가 아니다. 이 관점으로 최소 책임을 정한 뒤 계약·구현·검증을 `reference-project/`의 해당 책임 경계에 함께 둔다.

### 보존할 mental model

[Record 01의 여섯 장면](2026-08-18-01-clean-room-source-and-behavior-contract.md#구조-독립적인-behavior-contract)은 구현을 시작하기에 충분한 사용자-facing mental model이다.

- Maintainer는 event 전달기가 아니라 해당 작업 세션을 이해하며 따라가는 agent다.
- 기존 Workspace의 새 세션은 필요한 current만 bounded하게 읽고 시작 상태를 한 번 맞춘다.
- 같은 세션은 이미 얻은 이해를 재사용한다.
- 모든 사용자 대상 Main response-end에서 durable 변화 여부를 점검한다.
- No-change, 조용한 반영, 중요한 반영 후 보고와 write 전 ambiguity 질문을 구별한다.
- 초기 grounding 뒤 Main을 기다리게 하지 않고 stale·failure를 fresh나 completed로 가장하지 않는다.

Acceptance matrix는 이 mental model을 재논의하는 문서가 아니다. 각 장면을 관찰 조건, 책임 배치, 최소 direct test와 actual host acceptance로 번역하는 구현 준비물이다. 새로운 사용자 행동 선택이 드러날 때만 질문한다.

## 이후 읽기와 판단 우선순위

새 설계와 구현의 입력 우선순위는 다음과 같다.

1. 현재 사용자가 바로잡은 의도와 승인
2. Workspace 007의 behavior contract와 이 기록
3. 글로벌 AI-system references
4. Reset된 현재 `reference-project/`와 현재 Codex host의 공식 계약
5. Workspace 005·006은 007이 특정 근거 확인을 요구할 때만 사용하는 역사적·negative evidence

Workspace 005·006의 과거 코드·diff·runtime residue와 records를 넓게 다시 읽지 않는다. 이미 확인한 queue, cursor, transaction, attention, recovery 이름은 새 acceptance나 architecture의 기본 항목으로 사용하지 않는다. 현재 근거에서 같은 장치가 독립적으로 다시 필요해지면 여섯 장면 중 지키는 약속, 더 단순한 대안, 새 실패·복구 비용으로 정당화한다.

## 다음 작업 경계

1. 여섯 장면의 acceptance matrix를 확정한다.
2. Matrix와 글로벌 reference에서 최소 책임 경계와 첫 vertical slice를 선택한다.
3. `reference-project/`에 계약·구현·직접 검증을 함께 만든다.
4. Static·fake proof와 실제 Codex host·semantic acceptance를 구분한다.
5. Reference actual acceptance 뒤에만 root automatic Maintain 연결을 다시 선택한다.

현재 architecture와 구현 topology는 아직 선택되지 않았다. 첫 산출물은 과거 구조 비교표가 아니라 acceptance matrix이며, 그 다음 단계는 실제 Reference 구현이다.
