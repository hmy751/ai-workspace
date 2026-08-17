# Project application Workspace

`reference-project/`에서 검증한 context+harness 책임을 기존 Project에 적용하고, 대상의 기존 canonical을 보존하면서 반복 이식 절차가 실제 장면과 검증 근거를 다시 구성하는지 확인하는 Workspace다.

상태는 **paused**다. 원본 적용, 과거 blind 평가, Project common context가 충분하지 않았던 v2와 v3를 서로 다른 증거로 보존한다. 현재 skill은 공통 제품 기준·구조·채택 결정의 Owner closure까지 다시 보강했지만 재시험하지 않았고 v3 target도 보정하지 않았다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 적용 목표·대상 구분·지속 기준·검증 상한
2. [`current/state.md`](current/state.md): skill 재보강·재시험 없음·v3 미보정 상태
3. [`output/index.md`](output/index.md): 현재 절차와 미완료 v3 결과의 역할
4. [Owner closure 정정 기록](records/2026-08-16-03-project-context-owner-closure-correction.md): v3 누락과 추가된 skill 규칙
5. v2·v3 실행 자체는 앞선 날짜별 records에서 확인한다.

이 Workspace는 `reference-project/context/work`의 전체 내용을 정답처럼 복제하지 않는다. 대상 Project의 기존 canonical과 사용자 변경을 먼저 고정하고, 선택한 Workspace 장면을 복구·검증하는 데 필요한 책임만 추가한다.

반복 이식 절차의 source는 repo-local [`apply-context-harness`](../../../.agents/skills/apply-context-harness/) skill이다. Skill은 절차를 소유하고, 실제 target 내용·적용 상태·receipt와 acceptance 여부는 각 target과 이 Workspace의 기록이 소유한다.
