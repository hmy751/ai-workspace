# Reference Recover·Verify 책임 재배치 구현과 검증

기록일: `2026-08-14`
상태: 사용자 승인 구현·검증 완료, 사람 acceptance와 commit 대기

## 범위와 채택한 책임 경계

사용자가 승인한 첫 구현 slice는 `reference-project`의 Recover·Verify 병목 개선으로 제한했다. Project common context와 Workspace `current/source/output/records` 구조는 유지했고, `apply-context-harness` skill과 다른 Project는 변경하지 않았다. Historical records와 기존 receipt도 현재 설계에 맞춰 다시 쓰지 않았다.

채택한 책임 경계는 다음과 같다.

- **Recover**: 명시된 Workspace의 현재 맥락과 선언된 verification snapshot freshness를 안전하고 제한적으로 복구하는 read-only 책임
- **Verify**: 검증 대상 claim과 canonical basis·evidence를 실제 제한 실행 및 durable machine evidence에 연결하는 책임
- **Maintain**: 자연스러운 작업 경계에서 agent와 main이 의미 변화를 current·records·source provenance·output index에 반영하고 main이 diff를 검토하는 workflow
- **Harness check**: fixture의 `recover → verify → recover`로 Harness 자체 회귀를 확인하되 checked-in 제품 Workspace의 status·receipt를 바꾸지 않는 ephemeral 검사
- **Human**: acceptance, completed 전이와 commit 여부 결정

Maintain은 새 Python CLI·module·schema나 새 agent 설치가 아니다. Outer repo-local `context_maintainer`를 Reference로 가져온 것도 아니다.

## 구현 결과

### Workspace 선택

명시한 `workspace_id`가 실행 권위다. Global active index는 id가 생략된 경우에만 fallback으로 읽으며, explicit Recover의 `control_paths`에는 index가 포함되지 않는다.

### Recover

현재 [`Recover 계약`](../../../../reference-project/context/work/harness/recover/README.md)은 read-only를 유지한다.

- 최소 memory 파일과 Project `overview.md` 포함은 hard entry requirement로 유지
- `overview.md`가 project context의 첫 항목이어야 한다는 순서 제약은 제거
- recovery packet schema `6`에서 status가 연결한 receipt의 declared snapshot freshness를 요약
- receipt schema `1`은 `unknown_legacy`로 표시
- receipt schema `2`는 receipt에 선언된 canonical basis와 evidence 파일의 현재 hash·size를 다시 계산해 `fresh` 또는 `stale` 판정
- 선언 파일의 변경·누락은 recovery를 막지 않고 요약에 남김
- traversal·symlink는 계속 거부
- receipt 경로와 body는 recovery context에 노출하지 않음

Freshness는 receipt가 선언한 snapshot과 현재 파일의 기계적 일치 여부이며 의미 충분성이나 전체 Project freshness가 아니다.

### Verify

현재 [`Verify 계약`](../../../../reference-project/context/work/harness/verify/README.md)과 [sample `verify.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/verify.json)은 schema `2`에서 다음을 소유한다.

- 이번 검사로 확인하려는 `claim`
- claim의 기준인 `canonical_basis`
- bounded argv와 evidence paths

Verify는 canonical basis와 evidence를 실행 전에 snapshot하고, receipt schema `2`에 combined snapshot id와 bounded runtime 결과를 남긴다. Contract의 `next_actions`는 제거했다. Machine-only status schema `3`은 `verification_passed` 또는 `verification_failed`와 receipt cursor만 소유한다.

Status schema `2`와 receipt schema `1` 읽기 호환은 유지한다. 사람용 current·records의 의미 갱신과 acceptance는 Verify가 수행하지 않는다.

### Harness check와 문서

[`Harness check`](../../../../reference-project/context/work/harness/validation/tests/test_ephemeral_workspace_state_preservation.py)는 임시 fixture에서 `recover → verify → recover`를 실행하고 checked-in active Workspace의 status와 receipt 목록이 전후 동일한지 확인한다. Harness 회귀 확인이 더 이상 실제 제품 Workspace의 durable cursor를 바꾸지 않는다.

Canonical Harness·Recover·Verify 문서와 sample contract는 현재 동작에 맞췄다. Historical records와 이전 receipt는 보존했고 skill과 다른 Project는 건드리지 않았다.

## 검증 결과

- 전체 integration test는 처음 50개 통과
- Legacy status migration 회귀 test 추가 뒤 독립 reviewer가 51개를 `4.602`초에 실행해 모두 통과
- 독립 review 결과 P1·P2·P3 없음
- Git staged·unstaged diff check 통과
- 마지막 소규모 link-safe 문서 수정 전 changed-doc 로컬 링크 84개 검사에서 누락 0

Harness 자체 검증 뒤에는 제품 상태 인계를 위해 explicit durable Verify를 한 번 실행했다.

- Workspace: `001-default-timeout`
- result: `pass`
- receipt: [`verify-20260814T103703075846Z-a1cde45907164974a19c22564a956127.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/receipts/verify/verify-20260814T103703075846Z-a1cde45907164974a19c22564a956127.json)
- 후속 explicit Recover: packet schema `6`, status schema `3`, freshness `fresh`
- declared snapshot: 5개 파일
- changed·missing·unavailable: 모두 없음
- explicit recovery `control_paths`: global index 없음

## 증명 상한과 남은 제약

- Freshness는 선언한 canonical basis·evidence의 hash와 size만 다룬다. 현재 `verify.json`, claim·argv 자체, 목록 밖 의존성, 의미 충분성, VCS revision은 포함하지 않는다.
- Recover 비용은 선택한 파일 수와 byte 크기에 선형이며 별도 상한이 없다.
- Receipt append와 status 교체는 하나의 transaction이 아니다.
- Concurrent verify는 지원하지 않는다.
- Test와 reviewer 통과는 사람 acceptance, Workspace 완료, commit을 대신하지 않는다.

## 다음 상태

승인한 Reference 구현과 기계 검증은 완료됐다. 사용자가 결과와 proof ceiling을 검토해 acceptance와 commit 여부를 결정해야 한다.
