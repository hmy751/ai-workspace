# Response-end 책임 지도와 첫 개선 선택

날짜: `2026-08-18`

상태: **superseded된 잠정 관찰**. 이 기록은 당시 topology 안에서 발견한 correctness 빈틈과 구현 결과를 보존하지만, 목적에서 resolver·session checkpoint·intent protocol 자체의 필요성을 다시 도출하지 않았다. [`self-check와 목적 우선 재정렬`](2026-08-18-03-self-check-and-purpose-first-reset.md) 뒤에는 Workspace 006의 선택된 개선 결과나 다음 구조의 전제로 사용하지 않는다. 이후 [`completed response와 Workspace attention 개선`](2026-08-18-04-completed-response-and-workspace-attention.md)이 session별 pending report와 cross-session resolver를 active protocol에서 제거했으므로 이 resolver 구현도 최종 canonical에는 남지 않는다.

## 분석한 전체 동작

운영상 하나인 동작은 Main의 user-facing response가 끝난 뒤 그 delta를 판단하고, 필요할 때 Workspace Context를 안전하게 갱신한 다음 보고와 처리 cursor를 확정하는 흐름이다.

- 시작 조건: `UserPromptSubmit`과 `Stop`이 한 turn의 immutable response event로 pair된다.
- 입력과 맥락: warm Maintainer understanding, response evidence, 좁게 고른 tool evidence, 선택한 Workspace canonical, 현재 파일 baseline, 이전 질문과 runtime checkpoint다.
- 결과: `no_change`, `updated_quiet`, `updated_report`, `needs_decision` 또는 복구가 필요한 미완료 상태다.
- 부작용: 허용된 Workspace Markdown 교체, decision intent·writer journal/completion·agent state·checkpoint·pending report 기록과 raw event cleanup이다.
- 비목표: 사용자 목표·Owner·acceptance를 대신 결정하는 것, 제품 파일·test·machine contract·active Workspace·외부 시스템을 수정하는 것, runtime 상태를 Workspace truth로 만드는 것.
- 반드시 지킬 약속: 모호하면 write 전에 묻고, 모든 write는 allowlist·baseline·link 검증을 통과하며, report와 cursor는 같은 event checkpoint에 commit되고, crash 뒤 같은 semantic decision을 재실행 없이 이어가며, 완료를 확인하지 못한 단계의 복구 증거를 지우지 않는다.

## 현재 책임 배치

- 사람은 목표·정책·예외·Owner 의미·acceptance와 모호성에 대한 최종 선택을 소유한다.
- 모델은 자연어 맥락에서 durability, 올바른 기존 Owner, 사용자에게 보고할 중요도, 해결된 질문과 갱신 내용을 판단한다.
- Prompt는 이 의미 계약을 모델이 수행할 절차로 표현하지만 보장 자체를 소유하지 않는다.
- Schema와 parser는 decision 형태, outcome과 write·question 조합, identity 형식을 반복 가능하게 거부한다.
- Controller는 event·Workspace identity와 binding을 대조하고 semantic decision, durable intent, guarded writer와 runtime processor result의 순서를 연결한다.
- Intent는 의미 판단 완료 뒤 runtime checkpoint 전까지 exact decision과 report·agent state를 보존한다.
- Writer는 허용 경로·baseline·symlink·Markdown link·transaction과 실제 changed path를 강제한다.
- Runtime은 event FIFO, lease, retry, checkpoint, pending report, 질문 resolution과 content-free freshness를 소유한다.
- Test는 이 배치와 구현의 증거이며 runtime 보장이나 semantic 품질 자체가 아니다.

이 배치는 `ai-system_behavior-responsibility-allocation.md`의 구분과 맞는다. 의미가 필요한 선택은 모델과 사람에게 남기고, 동일 상태에서 동일한 허용·거부와 실제 부작용 완료는 규칙 기반 장치가 보장해야 한다.

## 기존에 고정된 user-facing 결과

현재 test는 다음을 이미 직접 고정한다.

- `no_change`: write·report 없이 cursor를 전진시키고 warm thread를 유지한다.
- `updated_quiet`: guarded write 뒤 report 없이 intent를 정리한다.
- `updated_report`: 실제 write 뒤 summary와 path만 pending notice로 만들고 stdout flush 뒤 acknowledge한다.
- `needs_decision`: write 없이 질문과 cursor를 한 checkpoint에 commit하고, 전달 후에도 semantic resolution 전까지 session 사이에 보존한다.
- 복구: stale baseline·runner failure·write/checkpoint crash를 완료로 가장하지 않고 replay하며 세 번째 ordinary failure 전까지 조용히 복구한다.

이 증거는 fake runner/process와 임시 filesystem의 deterministic 경계를 다룬다. 실제 모델 분류 품질, nested `codex exec/resume`, host hook trust, detached process와 UI delivery는 별도 acceptance 없이는 증명되지 않는다.

## 확인된 첫 보장 빈틈

Model이 response evidence가 이전 `needs_decision` 질문에 답했다고 판단하면 `resolved_report_ids`를 반환한다. Controller는 이 ID가 판단 시점의 unresolved 질문 집합에 속하는지 검증하고 decision intent에 보존한다. 새 response event가 checkpoint된 뒤 `_reconcile_committed_intent()`가 runtime resolver를 호출한 다음 writer completion marker와 intent를 정리한다.

현재 `resolve_workspace_reports()`는 session metadata·layout·checkpoint를 읽을 수 없거나 신뢰할 수 없으면 해당 session을 조용히 건너뛴다. 반환한 `resolved_report_ids`에는 이번 호출에서 실제로 제거한 ID만 들어가지만 controller는 결과를 확인하지 않고 cleanup을 계속한다.

따라서 판단 당시 유효했던 질문이 reconcile 시점의 손상이나 읽기 실패 때문에 제거되지 않아도 exact decision과 재시도 근거인 intent가 사라질 수 있다. 이후 session이 복구되면 이미 답한 질문이 다시 unresolved로 나타날 수 있다. `no_change` checkpoint 자체에는 resolved ID가 남지 않으므로 intent 삭제 뒤에는 같은 resolution을 재구성할 durable 근거도 없다.

## 첫 세로 슬라이스 결정

첫 개선은 report resolution을 fail-closed로 만든다.

- 모델 책임은 바꾸지 않는다. 어떤 질문이 답변됐는지는 계속 semantic judgment다.
- Runtime은 요청된 질문의 제거 또는 이미 없는 상태를 검증할 수 있을 때만 정상 반환한다.
- Resolution 중 unreadable·malformed session이 있으면 성공처럼 skip하지 않고 명시적 runtime failure로 중단한다.
- 앞선 session에서 이미 일부 제거했더라도 재호출이 안전해야 한다.
- Runtime이 실패하면 controller cleanup도 중단되므로 intent와 writer completion evidence가 남는다.
- Session 상태가 복구된 뒤 같은 intent를 다시 reconcile하면 모델 재판단 없이 resolution과 cleanup을 끝낸다.

이 변경은 새 runtime state나 사람 승인 절차를 추가하지 않는다. 정상 경로의 질문 선택·보고·해결 결과도 바꾸지 않고, 확인할 수 없는 실패 경로에서만 복구 증거를 보존한다.

## 뒤로 둔 후보

- `changed_paths`는 `writes[].path`에서 결정적으로 파생할 수 있는데 모델 output·parser·controller·intent/report·writer에 반복된다. 두 목록의 순서만 다르면 의미와 write 내용이 맞아도 retry될 수 있어 다음 책임 단순화 후보다.
- `evidence_paths`는 필수 model output이지만 현재 판단·guard·report·복구에서 소비되지 않는다. 감사 근거가 필요하면 model 자기신고가 아니라 실제 read/tool evidence와 연결해야 한다.
- `expected_sha256`도 정확한 기계 값이지만 현재는 모델이 읽은 snapshot과 write를 묶는 stale-read guard다. 신뢰 가능한 mediated read snapshot 없이 controller가 대신 계산하면 보장이 약해지므로 유지한다.
- `freshness_failed`는 semantic canonical 대조 실패와 runtime 복구 실패 중 Owner가 더 명확해져야 하므로 이번 slice에서 바꾸지 않는다.

## 검증 순서

1. Malformed checkpoint가 있는 Workspace에서 question resolution이 성공으로 반환되지 않는 regression test를 추가한다.
2. 정상 상태 복구 뒤 같은 resolution을 재호출해 완료할 수 있음을 검증한다.
3. Controller가 checkpoint 뒤 resolution 실패 시 intent를 보존하고, 재진입에서 모델 호출 없이 cleanup하는 integration test를 추가한다.
4. Targeted runtime/controller test, Maintain 전체 test, Reference 전체 test와 `git diff --check`를 실행한다.

Live Codex나 host behavior를 바꾸지 않으므로 이번 slice의 acceptance는 deterministic test 범위에서 닫을 수 있다.

## 구현과 검증 결과

`runtime.py`의 `resolve_workspace_reports()` 계약을 강화했다.

- 요청된 ID가 있으면 sessions root와 모든 established session의 metadata·layout·checkpoint를 검사한다.
- 비세션 이름과 metadata가 한 번도 만들어지지 않은 read-created ghost는 valid report를 소유할 수 없으므로 건너뛴다.
- Established session을 읽거나 검증할 수 없으면 `RuntimeProtocolError`로 중단한다.
- 앞선 session에서 이미 제거한 report는 그대로 두고, 상태 복구 뒤 같은 요청을 다시 실행해 나머지를 제거한다.
- 성공 반환은 검사 가능한 established session에 요청된 `needs_decision` report가 더 이상 남지 않았다는 뜻이다.

추가한 test는 다음 경계를 고정한다.

- Malformed checkpoint가 있을 때 resolution이 정상 반환되지 않고, checkpoint 복구 뒤 같은 요청이 완료된다.
- 두 session 중 앞선 report를 제거한 뒤 다음 session 손상으로 실패해도 재호출이 나머지를 제거하며 반복 호출은 no-op이다.
- Response event checkpoint 뒤 resolution이 실패하면 decision intent가 남고, 재진입에서 모델을 다시 호출하지 않고 질문 제거와 cleanup을 끝낸다.

첫 regression test는 변경 전 resolver가 예외를 내지 않아 실패했고, runtime 수정 뒤 통과했다. 독립 검토에서 multi-session partial progress test가 빠졌다는 지적을 반영해 세 번째 경계를 추가했다. 최신 결과는 다음과 같다.

- Targeted config test: `8/8`
- Maintain 전체 test: `168/168`
- Reference 전체 test: `226/226`
- `git diff --check`: 통과

독립 검토에서 최신 diff의 actionable finding은 없었다. 남은 proof ceiling은 실제 다중 process 경쟁, resolver write 도중 process kill·fsync 장애, 실제 모델의 질문 해결 판단 품질, Codex host와 UI 전달이다. 이번 deterministic slice는 이 항목들을 acceptance한 것으로 해석하지 않는다.

## 이후 지위

이 개선의 핵심 교훈은 “해결됐다고 증명하지 못했는데 retry 근거를 지우면 안 된다”는 commit postcondition이다. 다만 그 보장을 session들을 훑는 resolver로 계속 구현할 필요는 없었다. 새 구조는 question을 Workspace attention 한 곳에 두고 response event의 attention mutation을 checkpoint 전 exact replay bridge로 보존한다. 따라서 당시 resolver code와 해당 topology 전용 test는 제거됐고, 교훈만 새 crash-window test와 Workspace attention 계약으로 이어졌다.
