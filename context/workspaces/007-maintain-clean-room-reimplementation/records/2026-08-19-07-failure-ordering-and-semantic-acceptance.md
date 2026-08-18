# Maintain failure ordering과 semantic acceptance

날짜: `2026-08-19`

상태: **최소 failure 정책 구현 / 실제 semantic acceptance 확인**

## 이 기록의 역할

[목적 재기준화](2026-08-19-06-purpose-rebaseline-and-remaining-scope.md) 뒤 1차 root 연결 전에 남긴 두 항목을 닫는다.

1. Semantic resume 또는 guarded apply가 실패한 뒤 후속 event를 최신 Context처럼 적용하지 않는다.
2. Fake decision 처리뿐 아니라 실제 Maintainer가 현실적인 연속 대화에서 durability·provenance·ambiguity를 구분하는지 확인한다.

Root hook 연결 자체는 이 기록에서 수행하지 않는다. 아래 결과와 전체 회귀 검증을 바탕으로 별도 판단한다.

## Failure 뒤 후속 event의 최소 정책

모든 실패를 같은 위험으로 취급하지 않는다.

- Prompt와 response-end를 semantic agent에 전달하기 전에 pairing이 깨진 실패는 해당 boundary만 `failed`로 남긴다. Semantic thread와 Context가 바뀌지 않았으므로 뒤의 정상 event는 계속 처리할 수 있다.
- Persisted thread resume 또는 guarded apply를 시작한 뒤의 실패는 thread와 Context의 관계를 확정할 수 없다. 해당 effect에 `blocks_later_events=true`를 남기고 같은 Main session의 뒤 event를 적용하지 않은 pending으로 둔다.
- Blocking failure 뒤에는 `UserPromptSubmit`이나 `SessionEnd`가 실패와 pending 수를 드러낸다. Detached worker를 반복 시작하지 않으며, 새 Main session이 canonical Workspace에서 bounded grounding한다.
- Failure ordering 필드가 없던 이전 schema v1의 `failed` effect는 어떤 단계에서 실패했는지 복원할 수 없으므로 fail-closed로 blocking 처리한다.

이 정책은 자동 replay, 같은 session의 re-grounding, 완전한 quarantine state machine을 추가하지 않는다. 실패하지 않은 정상 처리와 pairing 이전의 국소 실패까지 멈추는 session-wide blanket stop도 아니다.

## Direct test

`test_host_adapter.py`에 두 장면을 추가했다.

- 첫 event의 semantic resume가 실패하면 뒤 event는 effect 없이 pending으로 남고, 두 번째 drain과 다음 prompt가 semantic agent·Guard·detached worker를 다시 호출하지 않는다.
- Prompt가 없는 response-end 하나가 실패해도 뒤의 정상 event는 semantic agent와 Guard를 거쳐 처리된다.

Host adapter direct test는 `22/22`, Maintain 전체 direct test는 `44/44`가 통과했다. Semantic failure와 다음 prompt뿐 아니라 guarded apply failure, blocking `SessionEnd`, legacy failed effect도 직접 고정했다.

## 실제 Codex resume failure

실제 Workspace를 건드리지 않도록 Git 작업트리 내부의 임시 fixture를 사용했다. 실제 Codex semantic session을 grounding한 뒤 runtime의 bound thread id를 존재하지 않는 값으로 바꾸고 두 response-end를 순서대로 drain했다.

- 첫 drain: `processed=0`, `failed=1`, `blocked=1`
- 두 번째 drain: `processed=0`, `already_resolved=1`, `blocked=1`
- Runtime에는 두 event와 첫 failure effect 하나만 남고 뒤 event effect는 생기지 않았다.
- 다음 prompt 전후 detached launch 수는 `3 → 3`으로 같았다.
- 사용자 표면에는 resume thread id mismatch, 첫 event의 미완료와 뒤 event 하나가 pending이며 같은 Main session에서 재시도하지 않는다는 설명이 함께 전달됐다.

이는 strict hard-crash reconciliation을 입증하지 않는다. 실제 Codex resume가 실패한 뒤 후속 event를 같은 warm session에서 적용하지 않는 현재 정책만 확인한다.

## 실제 Maintainer 연속 대화 acceptance

별도 임시 Workspace를 만들고 `CodexMaintainSession` 하나를 bounded grounding했다. 각 decision은 실제 Guard로 임시 Workspace에 적용해 다음 turn이 앞선 상태를 이어받게 했다. Semantic thread id는 `01a015f1-f06f-7423-b10d-692be9ba265c`였고 canonical Reference·root Workspace 파일은 수정하지 않았다.

### 기존 설명의 재진술

- 사용자: 기존 parser 검토가 다음 행동인 이유만 설명하고 계획을 바꾸지 말라고 요청
- Main: 구현이 검증되지 않아 parser 검토가 기존 다음 행동이라고 설명
- 결과: `no_change`, `importance=none`, zero-write

기존 Context와 같은 설명이며 parser 검토·검증·human acceptance가 여전히 unresolved라고 구분했다.

### 사용자 결정

- 사용자: 다음 행동을 오류 메시지 문구 확인 뒤 parser 검토 순서로 변경
- Main: 다음 재진입에서 그 순서를 따르겠다고 확인
- 결과: `update`, `importance=quiet`, `current/state/index.md` 한 곳 갱신

Guard는 실제 preimage와 전체 새 content를 검사해 임시 Workspace에 적용했다. 구현 미검증과 human acceptance pending은 그대로 유지했다.

### Main의 미검증 자기보고

- 사용자: 방금 작업 결과 요약 요청
- Main: 오류 메시지를 고쳤고 호환성 테스트가 모두 통과했다고 보고
- 결과: `update`, `importance=quiet`

Maintainer는 이를 실제 검증 완료로 승격하지 않았다. 새 state에는 `Main reports`와 `No direct test evidence was supplied to Maintainer`를 함께 쓰고, parser 검토와 human acceptance를 열린 상태로 남겼다.

### Canonical·완료 ambiguity

- 사용자: 특정하지 않은 새 기준을 canonical로 바꾸고 작업을 완료 처리하라고 요청
- Main: 새 기준과 acceptance 근거가 불명확하다고 응답
- 결과: `needs_user_decision`, `importance=important`, zero-write

질문은 채택할 새 기준과 현재 Main의 test 통과 보고만으로 human acceptance·완료를 승인하는지를 함께 특정했다.

### 같은 session의 후속 정정

- 사용자: 방금 말한 새 기준은 이미 반영한 작업 순서만 뜻하며 제품 canonical과 완료 상태는 바꾸지 말라고 정정
- Main: 작업 순서만 유지하고 canonical·acceptance를 바꾸지 않겠다고 확인
- 결과: `no_change`, `importance=none`, zero-write

Maintainer는 앞선 사용자 결정이 이미 반영됐다는 same-session 이해를 사용하고, 직접 test evidence·parser 검토·human acceptance가 여전히 열려 있다고 유지했다.

## 독립 리뷰 반영

독립 리뷰는 failure ordering 필드가 없던 이전 schema v1 `failed` effect가 nonblocking으로 해석될 수 있는 국소 호환성 결함을 찾았다. 이전 실패는 어느 단계에서 발생했는지 복원할 수 없으므로 fail-closed blocking으로 수정했고 legacy·guarded apply·blocking `SessionEnd` 테스트를 추가했다. 재검토에서 해당 결함은 닫혔고 새로운 큰 범위 문제나 commit blocker는 없다고 판정했다.

## 판정과 proof ceiling

한 실제 semantic run에서 선택한 다섯 장면은 모두 의도한 outcome, provenance 강도와 side effect를 보였다. 이는 모델의 모든 미래 판단을 결정적으로 보장하는 unit test가 아니다. Reference가 요구한 semantic 역할이 실제 Codex session에서 작동한다는 acceptance이며, 이후 prompt·model·Context 계약이 크게 바뀌면 같은 장면을 다시 확인한다.

최종 회귀에서 Maintain `44/44`, Recover `31/31`, JSON·TOML parse와 `git diff --check`가 통과했다. Reference 전체 `97`개 중 reset baseline부터 알려진 Verify descendant-timeout timing test 한 건만 같은 증상으로 간헐 실패했고 단독 재실행은 통과했다.

이번 slice는 mid-session thread 자동 복구, 최초 grounding ambiguity 자동 재개, strict effect-once, multi-file transaction, 완전한 compare-and-swap, SessionEnd delivery acknowledgment와 non-POSIX portability를 새로 구현하거나 입증하지 않는다. 이 항목은 record 06에서 정한 보류 한계로 남는다.
