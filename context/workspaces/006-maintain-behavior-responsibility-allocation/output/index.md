# Maintain behavior responsibility allocation output

마지막 갱신: `2026-08-18`

## Workspace goal

Workspace 005에서 합의한 Reference Maintain의 목적과 사용자 경험을 보존하면서, 현재 구현 topology를 재검토하고 내부 판단·보장·권한·실행 책임을 더 작은 구조로 개선한다.

## 판단 기준

- 글로벌 `ai-system_behavior-responsibility-allocation.md`와 연결 references

## 개선 대상 baseline

- [Reference Maintain 책임 계약](../../../../reference-project/context/work/harness/maintain/README.md)
- [Semantic prompts](../../../../reference-project/context/work/harness/maintain/prompts.py)과 [warm Codex runner](../../../../reference-project/context/work/harness/maintain/runner.py)
- [Maintain controller](../../../../reference-project/context/work/harness/maintain/controller.py), [runtime](../../../../reference-project/context/work/harness/maintain/runtime.py), [decision intent](../../../../reference-project/context/work/harness/maintain/intent.py), [guarded writer](../../../../reference-project/context/work/harness/maintain/writer.py)
- [Decision schema](../../../../reference-project/context/work/harness/maintain/decision.schema.json)과 [Maintain tests](../../../../reference-project/context/work/harness/maintain/tests/)
- [Workspace 005의 완료 구현·proof record](../../005-context-continuity-maintenance/records/2026-08-18-09-reference-maintain-runtime-implementation-and-proof.md)

## 현재 선택된 개선 결과

없다. 006의 implementation diff는 중단됐고 code baseline 복원 때 제거한다.

## 잠정 관찰

- [Self-check와 목적 우선 재정렬](../records/2026-08-18-03-self-check-and-purpose-first-reset.md): Workspace 005 records 01–09에서 사용자 목적, 실패한 Observe와 교체 가능한 기술 후보를 복원하고 기존 topology 보존 중심 접근을 중단했다.
- [Response-end 책임 지도와 국소 resolver 관찰](../records/2026-08-18-02-response-end-responsibility-map-and-first-slice.md): 기존 topology 안에서 report resolution의 correctness 빈틈을 확인했다. 이후 session report topology가 active protocol에서 제거돼 해당 resolver 구현은 superseded됐다.
- [Portable config test 수정](../../../../reference-project/context/work/harness/maintain/tests/test_config_forming.py): root의 가변 Workspace 선택값을 Reference invariant로 고정한 결합을 제거한다. 이 test 책임 수정은 구조 재검토와 독립적으로 유지 가치가 있다.

중단 직전 deterministic 결과는 Maintain test `207/207`, Reference 전체 test `265/265`, `git diff --check` 통과다. 이는 선택된 output이 아니라 폐기 예정 diff의 마지막 확인 지점이다. 최종 독립 재리뷰와 live host acceptance는 완료하지 않았다.

## 다음 canonical 경계

- Workspace 005 records와 commit `9553d0a`: 합의, 실패한 실험, 최종 구현과 proof ceiling의 역사적 근거
- Commit `2649e9b`: 새 구현 전 code baseline
- 새 Workspace: clean-room 구현의 goal, current, 선택 source와 실제 output을 소유할 예정
