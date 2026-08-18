# Completed response와 Workspace attention 구조 개선

날짜: `2026-08-18`

상태: **중단된 구현 시도**. Deterministic test는 통과했지만 선택된 architecture나 output이 아니며 code baseline 복원 때 제거한다.

## 선택 이유

Workspace 005에서 보존하기로 한 것은 bounded grounding, warm continuity, response-end마다 하는 의미 판단, no-change·quiet update·important notice·write 전 question, Main 비차단과 false freshness 방지다. Hook 조합, queue·storage·cursor schema, report acknowledgement와 repair CLI는 이 경험을 위한 교체 가능한 adapter였다.

기존 구현은 사용자 prompt 시 processing sequence를 예약했다. Stop이 오지 않으면 gap이 생겼고, 그 내부 선택을 복구하기 위해 partial·orphan·ledger·control 승인과 gap repair가 필요해졌다. Important notice와 unresolved question도 생성 session checkpoint에 함께 저장해, 다음 session이 모든 checkpoint를 훑고 recipient별 delivery·resolution을 조율해야 했다. 완료 알림과 사람 판단이 필요한 상태가 같은 report protocol을 공유한 결과였다.

첫 구조 개선 시도는 두 원인을 직접 바꿨다.

1. Processing 순서는 완성된 user·assistant response pair에만 부여한다.
2. 사용자에게 남은 상호작용 의미는 session report가 아니라 Workspace attention 한 곳이 소유한다.

## 새 책임 배치

### Completed response capture

`UserPromptSubmit`은 prompt와 identity를 보존하지만 processing sequence를 예약하지 않는다. 같은 turn의 `Stop`이 도착해 assistant response와 pair가 완성된 시점에만 queue sequence를 부여한다.

Incomplete capture는 전달 누락 가능성을 보존하는 evidence지만 Workspace 전체의 다음 sequence를 막는 권한은 없다. 뒤의 completed response와 다른 session은 계속 처리할 수 있다. Differing replay, malformed completed event와 checkpoint identity 모순은 계속 fail-closed다.

이에 따라 active `control.json`, missing-Stop gap 판별, gap repair API·CLI와 새 abandonment 권한을 제거했다. 이전 version이 이미 만든 exact abandoned ledger는 terminal history로만 읽고 덮어쓰지 않는다. Queue publish와 ledger update 사이처럼 durable completed pair가 이미 존재하는 좁은 crash residue는 selector가 exact identity를 확인한 뒤 복구한다.

### Workspace attention

새 `attention.py`는 한 Workspace의 pending interaction만 소유한다.

- `notice`: 이미 반영한 중요한 변화의 짧고 self-contained한 결과다. Hook JSON이 stdout에 실제로 flush된 뒤 제거한다.
- `question`: 관련 write 전에 사람이 결정해야 하는 의미 상태다. Delivery, restart나 Main session 전환으로 제거하지 않고, 이후 response를 본 Maintainer가 exact ID를 semantic하게 해결했을 때만 제거한다.

Attention은 freshness나 event history가 아니다. 미해결 question이 있어도 무관한 work와 response 처리는 계속한다. Status는 processing freshness와 notice·question count를 분리한다.

Active runtime에서 session별 `pending_reports`, recipient/origin/delivery 배열, Workspace report scan·acknowledgement·resolver와 `report_pending` freshness branch를 제거했다. `resolved_report_ids`는 active decision에서 `resolved_question_ids`로 바꿨다.

### Commit과 replay

Response 하나의 부작용 순서는 다음과 같다.

1. Guarded writer가 허용 Workspace Owner와 baseline을 확인하고 Context write를 완료한다.
2. Attention mutation을 atomic apply한다.
3. Runtime checkpoint v3가 exact event identity와 outcome을 commit한다.
4. Attention의 applied replay bridge를 confirm한다.

Attention apply 뒤 checkpoint 전 crash가 나면 decision intent가 exact mutation을 재적용한다. Store는 같은 event·같은 mutation을 no-op replay로 받아들이고, 다른 mutation이면 conflict로 막는다. Checkpoint 뒤 confirm 전 crash는 다음 재진입이 이미 commit된 identity를 확인하고 bridge만 제거한다. 두 경우 모두 모델을 다시 호출하거나 notice·question을 부활시키지 않는다.

Applied bridge는 처리 history가 아니며 임의 개수 기반 prune을 하지 않는다. Checkpoint가 durable한 뒤에만 명시적으로 confirm한다. Bound를 넘는 미확정 mutation은 오래된 항목을 버리지 않고 fail-closed한다.

### Legacy migration과 delivery

Checkpoint v2의 `pending_reports`를 바로 버리거나 계속 session scan하지 않았다. Migration 전용 exact ensure 뒤 v2 report를 하나씩 제거해 cap 안에서 전진하고, 모든 established session이 전환된 뒤에만 완료 marker를 남겼다. Question이 전달 상한 앞부분을 영구 점유하지 않도록 Workspace delivery cursor와 stdout 이후 acknowledgement도 추가됐다.

Migration 도중 malformed state가 있으면 marker를 만들지 않고 fail-closed한다. Marker가 있으면 정상 interaction path는 legacy report를 찾기 위해 session을 다시 훑지 않는다. 이전 intent의 `resolved_report_ids`는 loader에서 exact하게 새 이름으로 normalize하고, migrated question은 기존 opaque report ID를 유지해 resolution target을 잃지 않는다.

## 글로벌 책임 배치 기준과의 대조

- 모델은 durability, 기존 Owner, ambiguity와 notice 중요도를 계속 판단한다.
- Schema·parser는 outcome과 question·write 조합, nonblank self-contained notice 같은 기계 형태를 거부한다.
- Writer는 Workspace allowlist, baseline, path traversal·symlink와 실제 write 성공을 집행한다.
- Runtime은 completed-response 전달과 processing cursor를 소유하지만 session별 사용자 의미를 소유하지 않는다.
- Attention은 다음 safe point까지 남아야 하는 Workspace 상호작용 상태만 소유한다.
- 사람은 question의 답, 목표·정책·중요 예외와 acceptance를 결정한다.

이 배치는 “모델이 판단했으므로 write가 안전하다”거나 “코드로 구현할 수 있으므로 코드가 의미를 결정한다”는 식으로 책임을 섞지 않는다. 또한 host adapter를 제거해도 Workspace canonical과 수동 Maintain 책임은 남는다.

## 검토 중 발견해 함께 막은 경계

독립 검토는 새 구조뿐 아니라 기존 upgrade·recovery 경계를 다시 공격했다.

- Cursor보다 낮은 queued residue를 정상 cleanup으로 오인해 processor 없이 폐기할 수 있던 경로를 checkpoint 모순으로 차단했다.
- 이전 gap repair의 approved abandoned ledger를 v3가 malformed로 만들거나 late Stop이 되살리던 경로를 immutable terminal compatibility로 고쳤다.
- Queue publish 뒤 ledger update 전 crash와 Stop-before-User pair publish crash가 selector에서 보이지 않던 경로를 exact completed-pair recovery로 연결했다.
- Attention replay가 resolution 뒤 question을 되살리거나 동일 event의 notice·question 결과를 둘 다 보존할 수 있던 초기 store 설계를 canonical mutation bridge로 바꿨다.
- Applied bridge의 개수 기반 prune, empty mutation tombstone과 unreadable self-resolution state를 제거했다.

이 항목은 새 사용자 기능이 아니라 false freshness와 replay 오류를 막기 위한 보정이다.

## 검증 결과

다음 deterministic 검증이 통과했다.

- Maintain 전체: `207/207`
- Reference project 전체: `265/265`
- `git diff --check`: 통과

실제 root status는 Workspace `006-maintain-behavior-responsibility-allocation`, established session `0`, notice `0`, question `0`, attention `ready`를 반환했다. 현재 root runtime에는 migration할 established v2 session이 없다.

## 정직한 비용과 남은 과제

이번 변경은 active state·API 일부를 줄였지만 source와 복구 책임을 줄이지 못했다. Attention store, v2 migration, legacy compatibility와 delivery cursor가 추가됐다. 따라서 결과를 “Maintain overdesign 제거”로 보고하지 않는다.

특히 `decision intent → writer journal → completion marker → runtime checkpoint`의 multi-file crash bridge는 남아 있다. Guarded Context apply와 semantic outcome commit을 하나의 더 작은 Workspace transaction으로 합칠 수 있는지가 다음 주요 구조 검토 대상이다. Legacy migration과 abandoned compatibility도 제거 조건 없이 영구 architecture로 굳혀서는 안 된다.

이번 test는 fake runner와 local filesystem의 deterministic 경계를 검증한다. 실제 Codex host의 hook trust, nested warm session, detached worker process kill, 다음 prompt UI 전달, 모델의 question resolution과 실제 문서 품질은 fresh-task acceptance 전에는 증명됐다고 보지 않는다.

## 중단 판정

최초 독립 리뷰는 unresolved question 전달 starvation, 128개를 넘는 legacy migration 정지, 구 intent의 blank summary 호환, checkpoint 뒤 legacy resolution 유실을 P1으로 재현했다. 각 반례를 보정하고 위 전체 test를 통과했지만, 그 보정은 migration-only API, delivery cursor와 추가 legacy 분기를 만들었다. 마지막 독립 재리뷰는 사용자의 중단 지시로 완료되지 않았다.

사용자는 “이미 있던 코드를 개선하려니까 이미 선입견이 묶인 것 같다”고 판단했다. 이 구현을 더 고치는 대신 Workspace 005의 합의와 글로벌 AI-system references에서 구조를 새로 도출하기로 했다. 따라서 이 record는 성공 후보가 아니라, 기존 topology를 출발점으로 삼을 때 compatibility가 다시 설계를 지배한 사례로만 사용한다.
