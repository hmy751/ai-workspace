# Reference 소유권 정정과 재계획 handoff

날짜: `2026-08-17`

## Trigger와 사용자 정정

Workspace 005 구현 계획을 설명하는 과정에서 global `ai-system_*` shared reference 검토가 계획의 중심처럼 보이자 사용자는 “그냥 래퍼런스 신경쓰지말고 아까 정해진 계획 다시 보여줘보ㅓ”라고 정정했다. Main은 이를 실행 원형인 루트 [`reference-project/`](../../../../reference-project/)까지 구현 범위에서 제외하라는 뜻으로 오해했다.

사용자는 이후 다음과 같이 의미를 다시 고정했다.

> 아니 바보야 ai-system 그거 계획 이상하게 세워서 그렇게 말한거지

여기서 “reference를 신경 쓰지 말라”는 말은 global `ai-system_*` shared reference가 계획을 과도하게 끌고 가지 않게 하라는 뜻이었다. 이 저장소가 만드는 재사용 가능한 실행 원형인 `reference-project/`를 최종 구현 범위에서 빼라는 결정은 아니었다. 따라서 root-only Observe 배치는 사용자 의도에 맞는 최종 architecture로 acceptance되지 않았다.

## 현재 미커밋 구현과 검증

- root [`.codex/context_maintainer/`](../../../../.codex/context_maintainer/)와 [`.codex/hooks.json`](../../../../.codex/hooks.json)에 Workspace 005 고정 dogfood Observe runtime이 있다.
- `UserPromptSubmit`, `Stop`, `SessionStart`, partial·queue·inflight·cursor·hash ledger와 crash reconciliation을 구현했다. LLM 판단이나 Context write는 하지 않는다.
- unit test **28개 중 28개**, Python 3.9 compile, hook JSON과 whitespace 검사가 통과했다.
- 독립 검토는 partial-first reservation, content conflict와 malformed `user: null` 보정 뒤 새 P0–P2 회귀가 없다고 판정했다.
- 실제 Terra read-only smoke에서는 `SessionStart`와 User event만 도달하고 `async Stop`이 session 종료와 함께 취소됐다. Runtime에는 sequence 1 `waiting_stop`, cursor 0이 남아 end-to-end pairing은 실패했다.
- 이 전체 slice는 아직 commit되지 않았다. root `.DS_Store`도 별도 untracked 파일로 존재하므로 다음 세션은 이를 구현 산출물로 포함하거나 되돌리지 않는다.

상세 protocol과 live failure는 [앞선 Observe record](2026-08-17-06-response-end-observe-runtime-and-live-smoke.md)가 소유한다.

## 바뀌지 않은 범위

- [`reference-project/`](../../../../reference-project/)의 Harness·Maintain 구조에는 Observe runtime을 설치하지 않았다.
- `apply-context-harness` skill, Verify 구현·schema, memory folder migration은 수정하지 않았다.
- Background semantic Maintainer와 Context conditional write도 구현하지 않았다.
- `async Stop`을 synchronous capture로 바꾸는 안과 missing Stop을 `abandoned` 처리하는 manual repair 안은 제안일 뿐 승인·구현되지 않았다.

## 다음 세션의 재계획 커서

다음 세션은 sync/manual repair 구현부터 시작하지 않는다. 먼저 다음 두 현재 구조를 실제 파일 기준으로 대조한다.

- `reference-project/context/work/harness/`와 그 아래 `maintain/`: 재사용 가능한 Reference Project Harness와 교체 가능한 Maintain adapter의 현재 책임·발견 경로
- root `.codex/context_maintainer/`와 `.codex/hooks.json`: Workspace 005에 고정된 dogfood Observe protocol과 hook integration

그 대조를 바탕으로 **재사용 가능한 canonical은 `reference-project/`가 소유하고 root는 이 저장소에서 시험하는 dogfood adapter가 되는 방향**으로 배치 계획을 다시 세운다. 다만 exact 파일 경로, 어떤 코드를 이동·공유·복제할지, hook 설정을 Reference에 어떤 형식으로 둘지는 아직 사용자 승인된 결정이 아니다.

재배치 계획이 승인된 뒤에만 코드 변경 순서와 migration을 정한다. Durable Stop capture, manual repair, session 격리와 live acceptance gate는 사라진 문제가 아니라 새 소유권 계획 안에서 다시 배치할 후속 protocol 결정이다.

## 후속 상태

이 handoff 뒤 사용자는 Reference 수정과 전체 구현 범위를 다시 확정했고, Maintainer의 세션 시작·지속 이해·background 활동·판단·보고·복구 동작과 단계형 구현 계획을 승인했다. 따라서 위 “소유권 재배치 계획을 먼저 제시한다”는 커서는 완료됐으며, 현재 커서는 [세션형 Maintainer 동작과 Reference 구현 계획](2026-08-17-08-session-maintainer-behavior-and-reference-implementation-plan.md)의 Reference Harness·Maintain 계약 수정이다.
