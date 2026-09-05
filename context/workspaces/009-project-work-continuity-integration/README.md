# Project·Work continuity integration Workspace

`memory-harness-research`의 TripProof spec-driven continuity 연구를 현재 `reference-project/`와 대조해, Project common context와 Work 운영에 어떤 의미를 가져오고 무엇은 먼저 시험하거나 보류할지 결정하는 작업이다.

현재 상태는 **사용자 정정에 따른 Project 물리 layer 반영과 검증 완료, 사용자 acceptance와 commit 전**이다. `context/project/`에 `common/current/guidance`를 실제 탐색 경계로 만들고 `decisions`를 별도 이유 기록 경계로 유지했다. Workspace는 root README와 task-specific 실제 layer 문서만 선택하며, Project 변경 뒤 영향을 받는 live consumer의 실제 Recover·의미적 target까지 확인하는 acceptance를 유지한다. Work가 Spec/Ticket을 조건부 실행 산출물로 품는 관계와 판단 영향 review는 아직 pilot 전 설계라 Reference에 채택하지 않았다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 계속 유지할 판단과 조사 경계
2. [`current/state.md`](current/state.md): 확인한 상태, 1차 결론과 다음 판단
3. [`records/2026-09-04-01-source-intake.md`](records/2026-09-04-01-source-intake.md): 읽은 자료, working-tree 지위와 근거 상한
4. [`records/2026-09-04-02-adoption-assessment.md`](records/2026-09-04-02-adoption-assessment.md): 현재 Reference와의 차이, 정정 전 채택·pilot·보류 판정
5. [`records/2026-09-04-04-tripproof-application-assessment.md`](records/2026-09-04-04-tripproof-application-assessment.md): 실제 TripProof 적용·소비 drift와 정정 전 이식 판단
6. [`records/2026-09-04-05-tripproof-application-review.md`](records/2026-09-04-05-tripproof-application-review.md): 정정 전 실제 적용 평가의 독립 교차검토와 당시 `PASS`
7. [`records/2026-09-04-06-reference-project-implementation.md`](records/2026-09-04-06-reference-project-implementation.md): 정정 전 Reference diff, 검증, 독립 review와 증명 상한
8. [`records/2026-09-04-07-project-context-physical-layers.md`](records/2026-09-04-07-project-context-physical-layers.md): profile-only 전제를 폐기한 사용자 정정, 물리 layer 이식과 검증
9. [`output/index.md`](output/index.md): 현재 선택된 Workspace 산출물과 아직 없는 것

## 경계

- 최초 범위는 지정한 `/Users/hammyeong-yeon/Desktop/memory-harness-research` 안의 분석·source·관련 Workspace였다. 사용자의 후속 지시로 실제 적용 target `/Users/hammyeong-yeon/Desktop/10_work/tripproof`의 현재 tracked 파일·Git 이력·보존된 공개 receipt와 private payload를 제외한 runtime metadata를 read-only로 추가 대조했다.
- 외부 연구 저장소는 사용자가 진행 중인 dirty working tree이므로 수정하지 않는다. 현재 읽은 내용의 지위와 핵심 파일 hash를 source intake에 남긴다.
- 실제 TripProof target도 수정하지 않는다. branch·HEAD·working-tree 상태와 main 반영 여부를 실제 적용 평가에 남긴다.
- 외부 연구에서 이미 채택한 방향, 내부 검토를 통과한 설계 후보, 실제 적용 효과를 구분한다. 연구 문서의 `ADOPT`를 이 Reference의 채택이나 사람 acceptance로 바꾸지 않는다.
- 현재 Reference에 이미 있는 Project/Work 분리, bounded Recover, `current/source/output/records`, Verify의 기계 증거와 acceptance 분리를 다시 만들지 않는다.
- TripProof의 제품 이름, 수치와 사건을 Reference의 보편 trigger나 schema로 옮기지 않는다.
- 이 Workspace의 1차 분석만으로 새 skill·hook·reviewer·상태 schema를 설치하거나 제품 수렴·코드 성장 효과를 주장하지 않는다.
- 이번에 선택한 Reference 변경은 working tree에 반영했다. 후속 pilot, 사람 acceptance와 commit은 각각 별도 판단이다.
