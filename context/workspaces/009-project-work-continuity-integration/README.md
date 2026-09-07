# Project·Work continuity integration Workspace

`memory-harness-research`의 TripProof spec-driven continuity 연구를 현재 `reference-project/`와 대조해, Project common context와 Work 운영에 어떤 의미를 가져오고 무엇은 먼저 시험하거나 보류할지 결정하는 작업이다.

Project 물리 layer 반영은 `7bd5089`, Project 관리 기준과 `update-project-context` skill 보완은 `5e45310`으로 commit됐다. 실제 Project 관리 기준과 구현 근거는 [`08 보완 기록`](records/2026-09-06-08-project-context-update.md)이 소유한다. 실제 host 호출·외부 target 적용 등 남은 확인은 이 Workspace의 current와 output에서 구분하며 전체 완료로 표시하지 않는다.

2026-09-07 사용자의 요청으로 **이번 세션의 Spec·Ticket 조사·설계 논의 전체를 [Workspace 010](../010-spec-ticket-workspace-design/README.md)으로 분리했다.** [`09 비교 기록`](records/2026-09-07-09-spec-ticket-current-assessment.md)과 [`10 개발 영향 분석`](records/2026-09-07-10-spec-development-impact.md)은 작성 당시 근거로 이곳에 보존한다. 이후 사용자 조건·후보의 지위·정정·제3 리뷰와 다음 설계 판단은 010이 소유하며, 이 두 초기 기록의 제안을 확정 방향으로 사용하지 않는다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 계속 유지할 판단과 조사 경계
2. [`current/state.md`](current/state.md): 확인한 상태, 1차 결론과 다음 판단
3. [`records/2026-09-04-01-source-intake.md`](records/2026-09-04-01-source-intake.md): 읽은 자료, working-tree 지위와 근거 상한
4. [`records/2026-09-04-02-adoption-assessment.md`](records/2026-09-04-02-adoption-assessment.md): 현재 Reference와의 차이, 정정 전 채택·pilot·보류 판정
5. [`records/2026-09-04-04-tripproof-application-assessment.md`](records/2026-09-04-04-tripproof-application-assessment.md): 실제 TripProof 적용·소비 drift와 정정 전 이식 판단
6. [`records/2026-09-04-05-tripproof-application-review.md`](records/2026-09-04-05-tripproof-application-review.md): 정정 전 실제 적용 평가의 독립 교차검토와 당시 `PASS`
7. [`records/2026-09-04-06-reference-project-implementation.md`](records/2026-09-04-06-reference-project-implementation.md): 정정 전 Reference diff, 검증, 독립 review와 증명 상한
8. [`records/2026-09-04-07-project-context-physical-layers.md`](records/2026-09-04-07-project-context-physical-layers.md): profile-only 전제를 폐기한 사용자 정정, 물리 layer 이식과 검증
9. [`records/2026-09-06-08-project-context-update.md`](records/2026-09-06-08-project-context-update.md): 보존 기준의 실패 근거·사용자 합의, Project 갱신 skill과 검증
10. [`output/index.md`](output/index.md): 현재 선택된 Workspace 산출물과 아직 없는 것

## 경계

- 최초 범위는 지정한 `/Users/hammyeong-yeon/Desktop/memory-harness-research` 안의 분석·source·관련 Workspace였다. 사용자의 후속 지시로 실제 적용 target `/Users/hammyeong-yeon/Desktop/10_work/tripproof`의 현재 tracked 파일·Git 이력·보존된 공개 receipt와 private payload를 제외한 runtime metadata를 read-only로 추가 대조했다.
- 외부 연구 저장소는 사용자가 진행 중인 dirty working tree이므로 수정하지 않는다. 현재 읽은 내용의 지위와 핵심 파일 hash를 source intake에 남긴다.
- 실제 TripProof target도 수정하지 않는다. branch·HEAD·working-tree 상태와 main 반영 여부를 실제 적용 평가에 남긴다.
- 외부 연구에서 이미 채택한 방향, 내부 검토를 통과한 설계 후보, 실제 적용 효과를 구분한다. 연구 문서의 `ADOPT`를 이 Reference의 채택이나 사람 acceptance로 바꾸지 않는다.
- 현재 Reference에 이미 있는 Project/Work 분리, bounded Recover, `current/source/output/records`, Verify의 기계 증거와 acceptance 분리를 다시 만들지 않는다.
- TripProof의 제품 이름, 수치와 사건을 Reference의 보편 trigger나 schema로 옮기지 않는다.
- 새 장치를 1차 분석만으로 설치하지 않는다. Project 맥락 갱신 skill은 후속 원문 재독과 사용자 합의로 도입이 확정됐으며, 새 hook·reviewer·상태 schema와 제품 수렴·코드 성장 효과는 포함하지 않는다.
- 물리 layer commit 뒤 합의한 Project 관리 보완은 `5e45310`에 반영됐다. 이번 Spec·Ticket 공개 조사와 의견 제시는 별도 구현 합의가 아니다. 외부 target 이식과 실제 host 검증은 수행하지 않았다.
