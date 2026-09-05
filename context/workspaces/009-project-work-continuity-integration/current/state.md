# Project·Work continuity integration state

마지막 갱신: `2026-09-04`

## 현재 상태

- 지정한 TripProof 판단 연속성 연구, 실제 TripProof 적용 branch와 live `reference-project/`를 대조했고 근거·branch·proof ceiling은 records에 보존했다.
- 첫 Reference 반영에서는 `common/current/guidance`를 물리 폴더가 아닌 책임 profile로만 채택했다. 사용자가 이 표현이 계속 혼동을 만든다고 정정했으므로 그 선택은 현재 계약에서 폐기하고 [`물리 layer 정정 기록`](../records/2026-09-04-07-project-context-physical-layers.md)으로 후속 변경을 남긴다. 당시 구현과 검토는 [`06 기록`](../records/2026-09-04-06-reference-project-implementation.md)의 역사로만 유지한다.
- 현재 `reference-project/context/project/`는 root `README.md` 아래 `common/`, `current/`, `guidance/`, `decisions/`를 실제 탐색 경계로 가진다. 평면 `prd.md`와 `architecture.md`는 각각 `common/prd.md`, `current/architecture.md`로 이동했고 중복 합본인 `overview.md`는 삭제했다.
- `common/current/guidance`와 각 layer README는 필수다. Guidance 본문이 없을 수는 있지만 그 사실과 추가·재검토·제거 조건은 `guidance/README.md`에 명시한다. `decisions/`는 현재 답의 네 번째 층이 아니라 선택 이유와 재검토 신호를 보존한다.
- Recover contract schema는 `6`이다. Root `context/project/README.md`만 평면 예외로 허용하고, 그 밖의 선택은 `common/`, `current/`, `guidance/`, `decisions/` 아래 Markdown으로 제한한다. 모든 layer를 자동 주입하지 않고 Workspace goal에 필요한 실제 문서만 이유와 함께 선택한다.
- Active/default sample `001-default-timeout`의 machine `recover.json`, 사람용 Project 선택, Verify basis와 현재 state를 새 경로에 맞췄다. 기존 Product Verify receipt와 `status.json`은 다시 쓰지 않았으며, 경로 이동 뒤 Recover freshness가 `stale`인 것이 정상이다.
- 이식·Workspace 생성 절차는 target에서 세 layer를 구성하고, 기존 flat canonical을 자동 이동하지 않으며, live consumer와 semantic target을 함께 reconcile하도록 정렬했다.
- 전체 Harness·제품 suite `119`개가 통과했고 explicit/default Recover는 모두 schema `6` packet으로 같은 네 Project 문서를 선택했다. 기존 receipt freshness는 예상대로 `stale`이다. 물리 구조·Recover 경계·sample 정합성의 독립 diff review도 열린 P1/P2/P3 finding 없이 통과했다.
- 별도 재진입 표면 검토가 정정 전 records `02/04/05`가 현재 산출물처럼 보이는 혼동을 찾아냈다. 기록 본문은 보존하고 현재성 메모와 index routing을 `07` 정정 기록 우선으로 보완했으며 재검토에서 `PASS`를 받았다.

## 현재 결론

### Reference에 반영한 것

- Project의 지속 의미, 교체되는 현재 현실, 조건부 판단 기준을 `common/current/guidance` 물리 layer로 고정하는 구조
- Root README와 layer README가 책임·Owner·읽기 조건·갱신 및 stale 신호를 연결하고, 실제 내용은 target 원자료에서 구성하는 계약
- Root의 포괄 overview를 두지 않고 Workspace가 goal별 실제 layer 문서만 선택하는 bounded Recover
- Project context 변경 뒤 active/default와 current-generation explicit binding을 포함한 live consumer의 선택·사람용 current·output target을 실제 Recover와 fresh semantic review로 대조하는 acceptance
- 다음 관련 Work가 제품 목적·사용자 문제·domain 관계·현재 구현 경계와 관련 판단 기준을 재추론하지 않게 하는 content recoverability
- Verify의 normative basis와 실행 입력 closure를 구분하고 국소 기계 근거를 사람 acceptance나 넓은 완료로 승격하지 않는 경계

### 이번에 반영하지 않은 것

- 모든 Project 문서를 자동 주입하거나 모든 Workspace가 세 layer를 전부 선택하는 동작
- TripProof 제품 내용·수치·파일명과 Project maintainer 구현의 복제
- `claim-impact-review`, `direction-gap-review` 역할과 고정 trigger·cadence
- 의미적 모순 자동 gate, Project-wide dependency graph와 역사 Workspace 상시 재작성
- Spec/Ticket 기본 배제나 Work-first의 보편적 우월성

### 후속 pilot 후보

- 안정된 실행 구간의 Spec·Ticket·bounded brief를 Work continuity 안에서 조건부로 연결하는 관계
- 동일 대상·범위·revision까지만 완료 claim을 닫고, 상위 전제 변경 뒤 관련 기존 결과만 제한적으로 재판정하는 방식
- 일반 Project 계약과 실제 반복 변경 근거가 생긴 뒤의 얇은 Project-level 관리 skill

## 바로 다음 행동

사용자가 검증된 no-commit working tree를 보고 구조를 수정하거나 수락할지 결정한다. 새 경로 기준의 durable Product Verify, Workspace 완료와 commit은 각각 별도 필요가 생기거나 사용자가 요청할 때만 수행한다.
