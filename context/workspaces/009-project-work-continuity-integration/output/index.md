# Project·Work continuity integration output

마지막 갱신: `2026-09-06`

## Workspace goal

외부 TripProof 판단 연속성 연구를 live Reference와 대조해, Project·Work 계약에 가져올 의미와 pilot 뒤에만 판단할 장치를 구분하는 진입점이다.

## 현재 선택된 산출물

- [`Project 맥락 보존·갱신 보완 기록`](../records/2026-09-06-08-project-context-update.md): 방어적 누락 실패의 근거, 사용자 합의, 관리 skill 도입과 이번 검증. 관리 skill을 pilot 후보로 남겼던 이전 판정보다 우선한다.
- [`Project 맥락 갱신 skill`](../../../../reference-project/.agents/skills/update-project-context/SKILL.md): Project README의 보존·변경·관리 기준을 적용하는 실행 절차
- [`1차 채택 판단`](../records/2026-09-04-02-adoption-assessment.md): 현재 Reference의 기존 책임과 후보를 대조한 정정 전 판단. 비물리 배치 판정은 현재 계약이 아니다.
- [`TripProof 실제 적용 평가`](../records/2026-09-04-04-tripproof-application-assessment.md): target 적용 사실과 소비 drift의 근거. 비물리 배치·선택적 overview 판정은 정정 전 기록이다.
- [`TripProof 적용 평가 독립 검토`](../records/2026-09-04-05-tripproof-application-review.md): 실제 target·live Reference 교차검토와 당시 `PASS`. 현재 물리 구조를 검증한 결과는 아니다.
- [`Reference 반영·검증 기록`](../records/2026-09-04-06-reference-project-implementation.md): 정정 전 profile-only 구현, live consumer reconciliation과 당시 검증의 역사
- [`Project 물리 layer 정정 기록`](../records/2026-09-04-07-project-context-physical-layers.md): profile-only 전제를 폐기한 이유, 구조 이동, Recover schema와 최종 검증
- [`Project context canonical`](../../../../reference-project/context/project/README.md): `common/current/guidance` 물리 layer, bounded 읽기, content recoverability와 authority 경계가 반영된 실제 Owner
- [`Common 제품 기준`](../../../../reference-project/context/project/common/prd.md)과 [`current architecture`](../../../../reference-project/context/project/current/architecture.md): sample에서 지속 의미와 교체되는 현재 현실을 분리한 실제 내용 Owner
- [`Guidance layer`](../../../../reference-project/context/project/guidance/README.md): 현재 active guidance가 없다는 상태와 새 guidance의 lifecycle 조건
- [`Workspace collection canonical`](../../../../reference-project/context/work/workspaces/README.md): Project 변경 뒤 live consumer reconciliation을 소유하는 실제 Owner
- [`적용 판단 계약`](../../../../.agents/skills/apply-context-harness/references/application-contract.md): target 이식의 semantic target·residue·input-closure acceptance
- [`source intake`](../records/2026-09-04-01-source-intake.md): 읽은 외부 working-tree snapshot, 범위와 근거 상한
- [`bounded 재진입 검토`](../records/2026-09-04-03-bounded-reentry-review.md): 기본 진입점만으로 목표·판정·다음 행동을 복원하는지 확인한 최종 `PASS`

물리 layer 반영은 `7bd5089`로 commit됐다. 후속 Project 보존 기준·관리 skill·호출·이식 경로 보완은 문서 검증을 마쳤고 사용자가 commit을 요청했다. 해당 revision은 새 skill의 Git 이력에서 확인한다. 역사 기록의 당시 PASS를 이번 skill의 실제 호출·행동 검증으로 사용하지 않는다.

## 아직 없는 것

- claim-scope bounded replay brief와 결과
- 새 review 역할이 필요한지에 대한 행동 차이·비용·오탐 근거
- 실제 외부 target의 recover schema `4 → 6` migration과 bound Codex host acceptance
- 이번 보완의 실제 host skill discovery·invocation과 반복 작업에서의 맥락 보존 증거
- 실제 제품 acceptance와 Workspace 전체 완료

## 증명 상한

자료, 실제 TripProof working tree와 live Reference의 구조 대조는 도입 후보의 중복·충돌·과적합 위험과 적용 acceptance의 누락을 판단하게 했다. 구현·test·bounded review는 선택한 계약이 현재 Reference와 sample consumer에서 정합적으로 작동한다는 데까지 증명한다. 실제 target migration, 장기 유지 효과, 새 원칙의 invocation reliability, 제품 수렴·코드 성장 개선과 사람 acceptance를 증명하지 않는다.
