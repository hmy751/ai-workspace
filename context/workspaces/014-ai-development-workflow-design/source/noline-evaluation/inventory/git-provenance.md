# Noline Context Harness Git 경계

이 파일은 적용 및 후속 작업의 **출처와 시점**을 정리한다. 효과 판정은 여기서 하지 않는다. 기계식 전체 목록은 [`git-commits.json`](git-commits.json)에 있다. [`git_inventory.py`](../scripts/git_inventory.py)를 Noline 저장소에서 다시 실행하면 지정한 두 커밋 사이의 first-parent 85개 커밋을 재추출한다. JSON은 양 끝을 포함하며 각 커밋의 부모, 작성·커밋 시각, 제목, 첫 부모 대비 파일 상태와 numstat을 담는다.

## 도입 기준

- 직전 기준: `74926b8e33f87c04ec11a25991733f1b8bc3cbdc` (2026-05-11 15:13:33 +09:00, `refactor(server): centralize 500 error envelope in sendInternalError`).
- 첫 Context Harness 적용: `b4ed41f6e4bbae26fd45827b3b9063097a2c1ea4` (2026-09-04 16:50:00 +09:00, `feat: apply context harness to noline`). 이 커밋의 첫 부모가 바로 위 기준이다. `context/project/`, `context/work/`, Workspace 001, Recover·Maintain·Verify 구현과 hook, `create-context-workspace` skill을 추가했다. 전체 `git show --shortstat` 기준 91개 파일, 13,487줄 추가·8줄 삭제다.
- 도입 전에도 root `CLAUDE.md`/`AGENTS.md` bridge, `.claude` guide·rules·guards·runbooks·deep context, `noline-work` dispatcher, report-only agent가 존재했다. 이번 도입은 최초 AI 하네스 구축이 아니다. `git ls-tree -r --name-only 74926b8e -- .claude .agents .codex CLAUDE.md AGENTS.md`와 `.claude/decisions/2026-09-04-context-harness-application.md:7-22`가 경계를 보여 준다. 첫 적용의 원본·대상 기준과 제외 범위는 `context/work/workspaces/001-noline-context-harness-application/records/2026-09-04-01-initial-application.md:3-24`에 있다.

## 이후 지침과 실행층의 변화

| 시점 (+09:00) | 커밋 | Git에서 확인할 변화 |
| --- | --- | --- |
| 2026-09-10 15:08 | `aa2314cd9c1400420ea8d22f5ea39f9d76ceca21` | Context Harness 갱신, Project context 재구성, 설명·논의·재판단·Project 갱신 skill 추가. |
| 2026-09-10 21:24 | `34f1a04fa7ee5f87ff7664a2c2e1d61756cc8bd7` | 선택적 개인 증거 수집 연결과 host adapter 변경. 수집 연결이 효과 증명을 뜻하지는 않는다. |
| 2026-09-10 21:56 | `e7c113440289ff2fa477a4897ed6057488fdf5e7` | 기존 `noline-work` dispatcher deprecated. |
| 2026-09-11 22:07 | `309b9e6733e4322e70c65c7febeb381e0bcfe94a` | Workspace 문서 작성 기준과 Maintainer 설정·지침 반영. |
| 2026-09-12 14:57 | `d7223b7b6622f625e26f7e7457f6eb1373cf91d9` | 공통 Spec·Ticket 실행 기준 도입. 현재 진입 구조는 `context/work/workspaces/spec-and-tickets/README.md:1-44`. |
| 2026-09-12 15:23 | `c90223012b7135d2a221cf4a97036872111f6df0` | Ticket 결과·분리한 일·선행 관계 판단 보완. 당시 결과와 검증 한계는 `context/work/workspaces/002-code-readability-refactoring/output/index.md:19-21`. |
| 2026-09-14 14:42–21:20 | `26350d6b04763f8276314187087f8c0d6d45ea27`, `3baa7b701a3f3eec5f2f1a27081a50212036e75c`, `2937c252a735ecc6edbe1d3516659fcf459da970`, `33bde333bdd6168e6dc8bc0621e17bf432320b79` | 주제별 Project Owner 이동, Project 구성·읽기 경로·계약 수정. 현행 문구를 9월 4일 최초 적용 상태로 소급하면 안 된다. |
| 2026-10-01 14:59 | `ee1c005219467f7cd8fd55e5b5b44a6c96a79300` | `start-app` 로컬 skill 추가. |

## Workspace 002의 Ticket 01–06 저장 경계

Ticket 01–05는 기존 번호를 유지했고, 새 06은 2026-09-14의 앱 사용 흐름 재배치에서 들어왔다. 이 번호 체계와 이후 Ticket의 관계는 `context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/index.md:3-20,39-47`을 따른다. 아래 커밋은 작업 결과의 Git 경계이며 각 Ticket의 전체 acceptance나 하네스 효과를 단독 증명하지 않는다.

아래 표의 `output`은 `context/work/workspaces/002-code-readability-refactoring/output/index.md`, `state`는 `context/work/workspaces/002-code-readability-refactoring/current/state/index.md`, `closure record`는 `context/work/workspaces/002-code-readability-refactoring/records/2026-10-06-03-ticket-06-closure-and-followups.md`를 가리킨다.

| Ticket | 커밋 경계 |
| --- | --- |
| 01 경비 합계 | `a51b7592eb71576dc617a01a79e3b9f6cb3e390a` (2026-09-11 17:40). 앞선 `1cc6696`을 amend로 대체한 최종 커밋이라는 기록은 output `:24-30`에 있다. |
| 02 도시 검색 | `33348de4b7a63fcd8212f2fa0bed85ba5e3bd472` (2026-09-11 19:51); output `:32-40`. |
| 03 저장 용량 | Jest 기반 `653f8b8ad11c18d6c7eaa4da71ea4bdfcc956225` (2026-09-11 21:52), 제품 수정 `a147a42c29271d90ae16b55d9c83487a6f66993e` (22:40). 최초 범위는 다음 날 `d7223b7b`의 Spec·Ticket 보강 과정에서 재분석됐다. |
| 04 경비 API | 제품 `dce576fa4f595671296c602c61f474efa65ec0ba` (2026-09-11 22:49), 완료 기록 `c97ad51aa57129b6e4d520e460acfd1d169f6e6b` (22:55); output `:42-49`. |
| 05 서버 Schedule | 테스트 기반 `fe5722a0da4dc8234827d5e0da6dee9375c43298` (2026-09-13 23:23), 날짜 직렬화 `7dd25211d18bcb100850295670e566c432f64da8` (09-14 00:06), response schema `9d48b954231025f080a91383370d117215a3c056` (10:09), 접근·soft-delete 경계 `d7bf5ffb62a64fcd94cce61158198c94ba348d82` (12:21). `fd1db2615c6f1490e0ce888b863816c2c1c962ea`의 Trip·Expense 직렬화는 후속 Ticket 17의 선행 조각이다. 근거와 각 단계 한계는 output `:51-78,120-123`. |
| 06 앱 준비·인증·네트워크·후속 UX | 범위 기록 `7cfa7db7f4a56f05f618163b80c77848032e28a3` (2026-09-16 19:57), 첫 네트워크 제품 커밋 `c5784461979186c25203c4d08aca52dbcdb3c9a2` (09-18 10:31), 마지막 제품 커밋 `3ab8f555e9c45c6c361b2cefd6b2482a4e7d4caf` (10-06 23:08), 합의 범위 종료 기록 `4fb309d2ba50afaca44019879d7161964b9b2328` (23:25). 중간에 인증·로컬 접근·sync·화면 정책, 온라인 복구, 폼·날짜·시간대·선택창까지 여러 결과가 들어갔다. 단일 커밋이나 연속된 작은 diff 하나로 환원할 수 없다. state `:3-28`과 closure record `:1-20,36-54`에 종료 범위와 미확인을 구분한다. |

## 비교에 쓸 Git 범위와 한계

전체 순서는 `git log --first-parent --reverse 74926b8e33f87c04ec11a25991733f1b8bc3cbdc^..4fb309d2ba50afaca44019879d7161964b9b2328`로 읽는다. 도입만 보면 `git diff 74926b8e33f87c04ec11a25991733f1b8bc3cbdc b4ed41f6e4bbae26fd45827b3b9063097a2c1ea4 -- context .claude .agents .codex CLAUDE.md AGENTS.md`, Ticket 단계는 해당 경계의 첫 부모와 커밋을 좁은 경로로 비교하는 편이 적절하다.

직전 기준과 첫 적용 사이에 약 네 달이 있고, 이전 `.claude` 하네스가 이미 존재한다. 또한 첫 적용 뒤 9월 10–14일에 구조·skill·Spec·Ticket 지침이 다시 바뀌었으며 제품 Ticket은 그 변화와 함께 진행됐다. 따라서 기준 `74926b8e`와 최신 `4fb309d2`의 전체 diff를 단일한 하네스 처치 전후 비교로 해석할 수 없다. 기록의 테스트·수락 문장은 해당 당시 Main 또는 Maintain 보고 범위일 수 있으므로 Git 사실과 별도로 확인해야 한다.
