# Clean-room 재시작 결정

날짜: `2026-08-18`

상태: **결정됨**

## Trigger

사용자는 “이미 있던 코드를 개선하려니까 이미 선입견이 묶인 것 같다”고 정정했다. 006에서 기존 파일과 protocol을 유지한 채 책임을 줄이려 하자, 제거한 상태를 위한 migration·compatibility·delivery state가 다시 생겼다. Test를 더 추가해 내부 일관성을 높일 수는 있지만, 그것이 Workspace 005에서 합의한 Maintainer 경험의 최소 구현이라는 근거는 되지 않았다.

## 결정

1. Workspace 006 구현은 중단하고 선택된 Reference output으로 취급하지 않는다.
2. 006의 분석·self-check·실패와 마지막 deterministic 결과는 records로 커밋한다.
3. Workspace 005 최종 구현 commit `9553d0a`가 바꾼 live implementation·adapter·연결 문서는 부모 `2649e9b` 상태로 path-scoped 복원한다.
4. Workspace 005 README·current·output·records, 특히 records 01–09는 역사적 원자료로 보존한다.
5. 별도 Workspace에서 Workspace 005의 합의와 글로벌 AI-system references를 직접 입력으로 삼아 새 구현을 도출한다.
6. 006의 completed-pair, attention store, migration과 crash protocol은 새 architecture 후보로 넘기지 않는다. 새 세션이 같은 결론을 독립적으로 도출할 수는 있지만 기존 diff를 출발점으로 삼지 않는다.

## Reset 경계

- Repository history를 rewrite하거나 전체 worktree를 hard reset하지 않는다.
- Commit `9553d0a`의 변경 중 Workspace 005 historical Context를 제외한 live code·adapter·routing surface를 부모 상태로 복원하고 새 commit으로 남긴다.
- 이후 commit과 다른 Workspace 문서, 사용자 소유 untracked 파일은 보존한다.
- Root hook처럼 code와 함께 움직이는 live 설정은 존재하지 않는 구현을 가리키지 않도록 code baseline과 함께 정합화한다.

## 중단 시점의 verified와 unknown

- verified: Maintain test `207/207`, Reference project test `265/265`, `git diff --check` 통과
- verified: 최초 독립 리뷰의 P1 네 건을 재현하고 보정 test를 추가함
- unknown: 보정 뒤 마지막 독립 재리뷰 결과. 사용자의 중단 지시로 reviewer를 종료함
- unknown: 실제 Codex host의 warm continuity, background nonblocking, UI 전달과 semantic 문서 품질

이 검증은 폐기 예정 diff의 상태 기록이지 새 Workspace가 상속할 acceptance가 아니다.

## 새 Workspace가 가져갈 최소 근거

- Workspace 005에서 확정한 사용자 장면과 책임 경계
- Record 06의 실제 Observe delivery 실패와 global FIFO gap
- Record 08의 “hook·queue·storage·cursor·CLI는 교체 가능한 기술 후보”라는 경계
- Record 09의 최종 구현 범위와 proof ceiling
- 글로벌 behavior responsibility allocation, context ownership, responsibility cohesion, human-readable structure와 harness rippability 판단 질문
- Code baseline commit `2649e9b`와 005 구현 commit `9553d0a`의 차이

새 Workspace는 이 근거를 읽을 수 있는 자체 records와 handoff를 만들되, 005 전체 문서를 복제하거나 006 구현 상세를 current로 승격하지 않는다.
