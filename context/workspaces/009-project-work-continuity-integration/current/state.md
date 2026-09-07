# Project·Work continuity integration state

마지막 갱신: `2026-09-07`

## 작업 분리와 현재 책임

사용자는 이번 세션의 첫 Spec·Ticket 조사 요청부터 이후 설계 논의 전체를 009와 분리해 기록하도록 요청했다. 현재 진행 중인 Spec·Ticket 설계와 다음 논의는 [010 state](../../010-spec-ticket-workspace-design/current/state.md)가 소유한다. 009는 기존 Project context 통합 결과와 그 작업의 미완료 검증을 유지한다. Workspace 전체를 완료로 전환한 것은 아니다.

이관한 세션의 초기 [09 비교](../records/2026-09-07-09-spec-ticket-current-assessment.md)와 [10 개발 영향 분석](../records/2026-09-07-10-spec-development-impact.md)은 작성 당시 근거로 보존한다. 10의 임시 fixture·5개 회귀 검사는 당시 코드 범위를 확인한 결과이며, 이후 Spec 배치와 공유 관계에 관한 사용자 정정 및 제3 리뷰는 010의 종합 기록에서 읽는다.

Project 갱신 skill의 앞선 변경은 실제 Git에서 `5e45310 feat: preserve project context and add update skill`로 확인했다. 아래 2026-09-06 구현·검증 결과와 이번 설계 의견은 구분한다.

## 현재 상태

- Project 물리 layer 반영은 `7bd5089 feat: adopt layered project context boundaries`로 commit됐다. 이전 current·output에 남아 있던 commit 전 표기는 이 실제 Git 상태에 맞춰 고쳤다.
- 사용자와 연구 01·02·03, 연구 Workspace 003의 실패·복원 판단, 실제 TripProof Project 계약과 관리 skill을 다시 대조했다. 이 재독과 합의의 근거는 [`08 보완 기록`](../records/2026-09-06-08-project-context-update.md)이 소유한다.
- Project README에 합의한 보존 문구를 우선 배치하고, 방어적 누락 실패 이유와 층위·미정 표현·변경·갱신 기준을 보완했다.
- `reference-project/.agents/skills/update-project-context/`를 추가하고 Reference root 지침·README·이식 절차에서 발견하도록 연결했다. 기존 Project 관리 skill이 다른 이름으로 존재해도 책임을 대조하게 했다.
- 지속 관리 기준은 Project README가 소유한다. Skill은 근거 선택·기존 문서 반영·확인·보고를 맡으며 Workspace Maintain과 분리된다.
- 사용자는 보완 결과를 확인한 뒤 “그래 커밋까지 하자”라고 요청했다. 이번 변경의 revision은 `git log -1 --oneline -- reference-project/.agents/skills/update-project-context/SKILL.md`에서 확인한다. 기존 untracked `.DS_Store`는 변경·commit 대상에서 제외한다.

## 유지·보류한 범위

- `common/current/guidance` 물리 layer, bounded Project 선택과 Recover schema `6`은 유지한다.
- Workspace·Spec 관계의 구체적인 설계는 010으로 분리했다. 009의 당시 보류를 후속 설계를 금지하는 규칙으로 사용하지 않는다.
- `decisions/` 기록 항목의 별도 보완은 이번에 확정하지 않았다.
- 제품 코드·test, Work Harness runtime·hook·machine 계약·receipt·status, 외부 TripProof와 연구 저장소는 수정하지 않았다.
- `claim-impact-review`, `direction-gap-review`, 제품 수렴·코드 평가 workflow와 실제 외부 target migration은 여전히 별도 작업이다.

## 이번 확인

- 새 `update-project-context`와 수정한 `apply-context-harness`는 공식 skill validator를 통과했다.
- `recover 001-default-timeout --json`과 id 없는 `recover --json`은 모두 exit `0`, schema `6`이며 같은 Workspace와 네 Project 문서를 선택한다. 수정한 Project README가 실제 packet에 포함된다.
- 기존 Verify receipt의 freshness는 이전 경로 이동 때문에 계속 `stale`이다. 새로운 제품 실행 결과나 acceptance로 바꾸지 않았다.
- 변경·추가된 Markdown 14개의 local link 132개, 새 skill UI metadata와 `git diff --check`를 통과했다. 정적 검사와 main의 문장·근거 대조는 실제 host skill discovery·자동 호출·장기 맥락 보존 효과를 증명하지 않는다.

## 바로 다음 행동

현재 세션의 Spec·Ticket 설계는 010에서 이어간다. 이 Workspace를 다시 작업 대상으로 선택할 때는 Project 관리 skill의 실제 discovery·호출·맥락 보존 확인, 외부 target 적용과 output에 남은 증명 범위 중 실제 요청된 항목을 고른다. 010 분리만으로 이 후속 확인을 실행하거나 완료한 것으로 기록하지 않는다.
