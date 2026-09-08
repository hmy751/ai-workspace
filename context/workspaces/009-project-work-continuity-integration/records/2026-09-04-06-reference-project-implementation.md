# 2026-09-04 Reference Project 반영과 검증

## 결과

사용자가 TripProof 실제 적용에서 확인한 채택 범위를 현재 `reference-project/`와 이식 workflow에 반영하고, commit하지 않은 working tree로 남겼다. 반영한 핵심은 Project context의 내용 복원 계약과 Project 변경 뒤 live consumer까지 확인하는 acceptance다. 근거가 아직 pilot 수준인 Work/Spec 관계, 새 reviewer·maintainer·runtime은 추가하지 않았다.

> 현재성 메모: 이 기록의 profile-only Project 배치와 schema `5`는 이후 사용자 정정으로 폐기됐다. 현재 구조와 검증은 [`07 물리 layer 정정 기록`](2026-09-04-07-project-context-physical-layers.md)이 소유하며, 아래 내용은 정정 직전의 중간 결과로 읽는다.

## 반영한 책임

### Project context

- [`Project context README`](../../../../reference-project/context/project/README.md)를 안정된 routing anchor로 만들었다. 모든 Workspace가 이 README를 선택하되 README만 충분한 내용 payload로 보지 않고 goal에 필요한 실제 Project 문서를 별도로 선택한다.
- 지속되는 제품 의미, 교체되는 현재 현실, 조건부 판단 기준을 물리 디렉터리가 아닌 책임 profile로 정의했다. 각 문서나 section에서 읽기 조건, authority·상세 Owner, 갱신 책임, stale·재검토 신호를 찾게 했다.
- 다음 관련 Work가 제품 목적·현재 경계·판단 기준을 다시 추론해야 한다면 구조와 link가 맞아도 미완성이라는 content recoverability를 완료 조건에 넣었다.
- 당시 `reference-project/context/project/overview.md`는 선택적 derived summary로 낮추고, 평면 `prd.md`는 지속 제품 기준의 normative Owner, 평면 `architecture.md`는 상세 code/test Owner에 대조하는 교체 가능한 current 지도로 역할을 분명히 했다. 이 세 경로는 07 정정에서 삭제·이동됐으므로 현재 링크로 사용하지 않는다.
- default-timeout Decision은 일반적인 이유 기록 역할과 달리 현재 기본값의 normative Owner임을 명시한 예외로 정리했다.

### Recover와 sample consumer

- Recover contract의 필수 Project anchor를 `context/project/overview.md`에서 `context/project/README.md`로 바꾸고 의미 변경을 schema `4 → 5`로 표시했다. Recovery packet shape는 바뀌지 않아 schema `6`을 유지했다.
- 공통 fixture는 README와 task-specific 실제 문서를 함께 선택하고, 존재하지만 선택하지 않은 overview가 packet에 들어오지 않는지 검사한다. Schema `4` 거부, README 필수·순서 비강제, overview 부재 허용 회귀 test를 추가했다.
- Reference의 유일한 active/default consumer인 `001-default-timeout`은 [`recover.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/recover.json)과 사람용 [`03-project-context.md`](../../../../reference-project/context/work/workspaces/001-default-timeout/current/memory/project-context.md)를 함께 reconcile했다. README, 선택적 overview, normative Decision을 같은 이유로 가리키며 [`output/index.md`](../../../../reference-project/context/work/workspaces/001-default-timeout/output/index.md)는 실제 `src/config_loader.py`로 풀린다.
- `.codex/maintain-runtime/`이 없어 current generation에 explicit session-bound된 Workspace는 발견되지 않았다. 따라서 이번 live consumer 집합은 active/default `001-default-timeout` 하나였다. Binding 확인을 위해 private `turns/`·`events/` payload를 열지 않았다.

### 적용 acceptance와 Verify 경계

- [`Workspace collection 계약`](../../../../reference-project/context/work/workspaces/README.md)과 [`생성·전환 계약`](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md)에 active/default, current-generation explicit binding, 이번 변경 대상을 live consumer로 정의했다. 각 consumer는 current·Project 선택·output target을 reconcile하거나 successor 전환·deactivation한 뒤 explicit Recover와 active/default Recover를 실행한다.
- Local link의 존재·root boundary를 결정적으로 검사하고, label·설명이 실제 Owner를 가리키는지는 fresh semantic review로 별도 판정한다. 역사 Workspace는 live consumer에서 내려온 뒤에만 비동기화 대상으로 둔다.
- [`Verify 계약`](../../../../reference-project/context/work/harness/verify/README.md)은 routing README가 아니라 claim의 normative Owner를 basis로 선택하고, arbitrary argv가 실제로 읽는 tracked input closure를 evidence가 설명하도록 보강했다. Closure를 닫지 못하면 argv 또는 claim·proof ceiling을 좁힌다.
- Sample [`verify.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/verify.json)은 normative PRD와 Decision만 basis로 두고, 명시 test가 import하는 `src/__init__.py`, 제품 코드, `tests/__init__.py`, 제품 test를 evidence에 포함한다.
- Root [`apply-context-harness` skill](../../../../.agents/skills/apply-context-harness/SKILL.md), 그 [`application contract`](../../../../.agents/skills/apply-context-harness/references/application-contract.md), Reference의 [`create-context-workspace` skill](../../../../reference-project/.agents/skills/create-context-workspace/SKILL.md)에 같은 live consumer·semantic target·residue·evidence closure·큰 복원의 cold/blind review artifact 경계를 연결했다. 의미는 canonical 문서가 소유하고 skill은 적용 절차만 소유한다.

## 직접 검증

- 관련 Recover·Verify·ephemeral validation `47`개를 먼저 실행했다. 기존 descendant-timeout timing test가 한 번 일시 실패했지만 단독 재실행은 통과했다.
- Project root 전체 `python3 -m unittest discover -s . -p 'test_*.py' -v`는 `116`개가 통과했다. 이 안에 제품 test `7`개가 포함된다.
- `recover 001-default-timeout --json`과 id 없는 `recover --json`이 모두 exit `0`, packet schema `6`으로 같은 active Workspace와 README·overview·Decision을 읽었다.
- 두 Recover는 이전 Product Verify receipt를 `stale`로 판정했다. Snapshot된 Project basis 문서가 바뀐 결과다. Sample evidence manifest도 actual tracked import에 맞게 고쳤지만 Recover freshness는 현재 `verify.json`의 manifest·claim·argv 동일성을 비교하지 않으므로 그 변경까지 탐지했다고 해석하지 않았다. 과거 receipt나 machine status를 새 결과처럼 다시 쓰지 않았고, 이번 변경은 직접 test로 검증했으며 durable Product Verify는 실행하지 않았다.
- `git diff --check`, 변경 JSON parse, Python compile이 통과했다.
- `reference-project/`와 `apply-context-harness` 아래 Markdown local link `219`개를 확인해 missing·root escape가 `0`개였다. Sample current의 세 Project target과 output target은 각각 실제 README, overview, Decision, 제품 코드로 풀렸다.
- TripProof 제품명, 실제·stale Project 파일명과 sample Workspace id를 fixed-string으로 검사했으며 Reference와 이식 skill의 현재 표면에서 잔재가 나오지 않았다.
- 공식 `quick_validate.py`는 실행 환경에 `PyYAML`이 없어 시작하지 못했다. 같은 allowed frontmatter key, hyphen-case name, description 길이·금지 문자, TODO 조건을 Ruby 표준 YAML parser로 대조해 두 skill이 통과했고, 독립 reviewer도 skill routing을 직접 검토했다.

## 독립 검토

Fresh read-only reviewer에게 구현자의 결론을 정답으로 주지 않고 TripProof 적용 평가, live canonical과 현재 diff를 대조하게 했다.

첫 판정은 `REVISE(P2)`였다. 새 Verify 계약은 basis가 normative Owner여야 하는데 sample `verify.json`이 current 지도인 `architecture.md`를 basis에 남긴 충돌을 찾았다. Architecture를 제거하고 normative PRD와 default-timeout Decision만 남긴 뒤 같은 reviewer가 schema, sample consumer, link target, skill·acceptance, test와 비도입 범위를 다시 확인했다.

최종 판정은 **`PASS`**, 열린 P1·P2·P3 finding은 없다.

## 의도적으로 반영하지 않은 것

- `common/current/guidance` 물리 디렉터리 강제
- Work/Spec/Ticket/bounded brief의 새 schema나 보편 관계
- `claim-impact-review`, `direction-gap-review` 역할과 고정 trigger
- 새 Project maintainer, Maintain hook·runtime·lifecycle 변경
- contract digest, 자동 semantic gate와 역사 Workspace 전체 재작성
- TripProof 제품 내용·수치·Workspace·receipt의 복제

## 증명 상한과 working tree

이번 결과는 Reference 계약·Recover 구현·sample live consumer와 이식 절차가 선택한 TripProof 교훈을 정합적으로 반영하고 현재 test를 통과했다는 데까지 증명한다. 실제 외부 target의 schema `4 → 5` migration, 실제 bound Codex host session, 장기 Project context 유지 효과, 사람 acceptance를 증명하지 않는다. Semantic target과 content recoverability는 bounded 사람·AI 검토이며 runtime이 자동 보장하지 않는다.

사용자 지시에 따라 stage·commit하지 않았다. 기존 untracked `.DS_Store`는 건드리지 않았다.
