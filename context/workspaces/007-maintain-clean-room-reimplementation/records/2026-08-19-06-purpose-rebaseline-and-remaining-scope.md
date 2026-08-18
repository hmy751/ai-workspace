# Maintain 목적 재기준화와 남은 범위

날짜: `2026-08-19`

상태: **사용자 결정 반영 / Reference 계약 갱신 기준**

후속 구현·검증: 아래에 남긴 failure ordering과 semantic acceptance의 결과는 [`record 07`](2026-08-19-07-failure-ordering-and-semantic-acceptance.md)이 소유한다.

## 이 기록의 역할

[구현과 actual host evidence](2026-08-19-05-reference-implementation-and-host-evidence.md) 뒤 독립 리뷰의 큰 문제를 모두 다음 구현 요구로 올리는 대신, 사용자와 Maintainer의 본래 목적을 다시 대조해 현재 구현을 `유지`, `수정`, `보류`, `추가 acceptance`로 재분류한다.

이 기록은 record 04의 최초 acceptance와 record 05의 당시 리뷰 사실을 삭제하지 않는다. 두 기록에서 이후 대화로 바뀐 현재 판단과 root 연결 전 남은 범위를 소유한다.

## 재기준화를 만든 사용자 판단

Maintainer가 검증 책임까지 흡수하는지에 대한 문제 제기는 다음 발화에서 시작했다.

> git diff, test 등 뭔가 음 이런걸 다 무조건 전달해야하나? 싶기도 하고 또 이게 책임을 벗어나는 느낌도 들거든? 마치 예전 verify 문제 처럼? 너무 많은걸 짊어진건가 싶기도 하고

큰 구조 문제 전체를 자동으로 다음 요구사항으로 삼지 않겠다는 범위도 확인했다.

> 그럼 기존에 큰범위 설계나 이런건 다 신경 쓰지 않아도 되는거지?

새 Main session의 정상 Recover와 살아 있는 session 내부의 드문 thread 소실을 구분하고, 후자의 자동 복구는 지금 깊게 다루지 않기로 했다.

> 일단 1번에서 음 이런 너무 딮한건 지금 하지말자 일이 너무 길어

일반 ambiguity는 새 요구가 아니라 기본 동작으로 이미 있어야 한다는 기대도 확인했다.

> 2번은 이건 아직 개발이 안된거야? 기본이라서 된줄 알았지 아직 안된건가?

## 다시 확정한 Maintain 책임

Maintainer의 목적은 제품 상태를 다시 증명하는 것이 아니라, 다음 session이 현재 작업의 목표·결정·상태·불확실성을 잘못 이해하지 않도록 Workspace Context를 유지하는 것이다.

- 기본 의미 입력은 기존 Workspace Context, 현재 사용자 발화와 Main의 사용자 대상 응답이다.
- 사용자 결정은 사용자 결정으로, Main의 완료·test 주장은 `Main이 보고한 상태`로 출처 강도를 보존한다.
- 이미 입력에 포함된 제한된 실제 근거나 기존 Verify 결과가 있으면 그 근거가 입증하는 범위까지만 사용할 수 있다.
- Maintainer나 host adapter가 repository 전체 diff·Git 상태·raw test log를 기본 수집하거나 제품 test·eval을 실행하지 않는다.
- Host adapter는 lifecycle, response-end 전달, 순서·중복과 실패 가시화를 맡고 의미 판단이나 evidence 선별을 맡지 않는다.
- Guard는 explicit Workspace, 허용된 Context Owner, path·symlink와 preimage 등 결정적 side-effect 경계를 맡는다.

`evidence` decision 필드는 제거하지 않는다. 사용자 발화, Main의 보고와 이미 제공된 확인을 서로 구분하고 각 입력보다 강한 사실을 쓰지 않게 하는 provenance 용도로 유지한다.

## 현재 구현에서 유지하는 것

- explicit Workspace의 bounded Recover bootstrap
- 같은 Main session에서 persisted semantic thread의 이해 재사용
- 모든 사용자 대상 response-end의 빠른 접수와 Main 비차단
- `no_change`, `quiet`, `important`, `needs_user_decision` 구분
- 일반 turn ambiguity의 zero-write와 다음 prompt 알림
- guarded apply의 Workspace binding, allowlist, preimage, path·symlink 거부
- ordinary duplicate의 중복 적용 방지와 실패를 완료·fresh로 가장하지 않는 runtime

기존 queue·lock·effect marker와 persisted thread는 현재 행동을 지지하고 Workspace canonical을 대체하지 않으므로, 구조가 있다는 이유만으로 삭제하지 않는다. Markdown 품질과 memory·record index pairing도 현재 human-readable 진입점을 보호하므로 유지하되 완전한 cross-file transaction까지 새 보장으로 올리지 않는다.

## 현재 수정하는 계약

1. 모든 response-end에 관련 diff·파일·Git 상태·test/eval 근거를 반드시 전달한다는 문장을 제거한다. 기본 입력과 선택적으로 이미 제공된 근거를 구분한다.
2. 같은 outer session에서 semantic thread가 사라지면 자동으로 재-grounding한다고 보장하지 않는다. 실패를 warm·current로 가장하지 않고, 새로운 Main session은 평소처럼 canonical Workspace에서 새 Maintainer를 grounding한다.
3. record 05의 모든 proof gap을 root 연결 blocker로 승계하지 않는다. 아래 남은 범위와 명시적으로 보류한 한계로 나눈다.

## 실제로 남은 범위

### 실패 뒤 후속 event

현재 adapter는 semantic resume 또는 guarded apply가 실패한 event를 `failed`로 남기지만, 같은 drain의 뒤 event를 계속 처리할 수 있다. Pairing 이전의 단순 입력 실패와 semantic thread·Context 상태가 어긋났을 수 있는 처리 실패를 구분한 뒤, 후자의 뒤 boundary가 최신 Context인 것처럼 적용되지 않게 하는 최소 정책과 direct test가 필요하다.

모든 실패 뒤 session 전체를 무조건 영구 정지시키는 정책은 확정하지 않았다. 자동 replay·re-grounding과 완전한 quarantine도 이번 slice에 넣지 않는다.

### Semantic acceptance

Fake semantic decision을 처리하는 unit test와 실제 Codex의 no-change·ambiguity·quiet update 장면은 확인했지만, 현실적인 연속 대화에서 Maintainer가 durability와 provenance 강도를 제대로 판단하는지는 더 직접 확인해야 한다.

- 일회성 설명과 durable 변화 구분
- 사용자 결정과 Main의 미검증 자기보고 구분
- 명확한 update와 사람 판단이 필요한 ambiguity 구분
- 같은 session 후속 발화에서 이전 이해 재사용
- quiet와 important 보고 경계

이 acceptance는 제품 test나 Verify가 아니라 Maintainer 의미 판단 자체의 검증이다.

### Writer 전제와 실제 host 재확인

Automatic mode의 background Context writer는 guarded Maintain 하나로 둔다. Main이나 사용자가 같은 Owner를 직접 수정하면 현재 preimage 검사가 일반 충돌을 거부하지만 hash 확인과 replace 사이의 완전한 compare-and-swap은 주장하지 않는다.

계약과 최소 실패 정책을 반영한 뒤 실제 host에서 연속 대화와 실패 뒤 후속 boundary를 다시 확인하고 root 연결 여부를 판단한다.

## 이번 범위에서 보류하는 한계

- 살아 있는 Main session 내부 semantic thread의 자동 부활·re-grounding
- 최초 grounding ambiguity를 같은 outer session에서 자동 재개하는 경로
- hard-crash strict effect-once와 multi-file atomic transaction
- 완전한 concurrent-writer compare-and-swap
- SessionEnd background notice의 delivery acknowledgment
- non-POSIX process lock portability

이 항목은 구현됐다고 주장하지 않지만 Reference 1차 동작의 자동 blocker로도 올리지 않는다. 전제가 바뀌거나 실제 실패가 반복되면 record 01의 여섯 장면 중 깨지는 약속과 더 단순한 대안을 다시 확인한다.

## 현재 root 연결 기준

Root automatic Maintain은 계속 비활성이다. 다음 세 항목 뒤에만 연결을 다시 판단한다.

1. broad evidence와 mid-session 자동 복구 과장을 Reference 계약에서 제거한다.
2. semantic/apply 실패 뒤 후속 event가 최신인 척 반영되지 않는 최소 동작과 direct test를 확정한다.
3. 작은 semantic acceptance 묶음과 해당 actual host 장면을 확인한다.
