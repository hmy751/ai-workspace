# Project·Work continuity integration state

마지막 갱신: `2026-09-06`

## 현재 상태

- Project 물리 layer 반영은 `7bd5089 feat: adopt layered project context boundaries`로 commit됐다. 이전 current·output에 남아 있던 commit 전 표기는 이 실제 Git 상태에 맞춰 고쳤다.
- 사용자와 연구 01·02·03, 연구 Workspace 003의 실패·복원 판단, 실제 TripProof Project 계약과 관리 skill을 다시 대조했다. 이 재독과 합의의 근거는 [`08 보완 기록`](../records/2026-09-06-08-project-context-update.md)이 소유한다.
- Project README에 합의한 보존 문구를 우선 배치하고, 방어적 누락 실패 이유와 층위·미정 표현·변경·갱신 기준을 보완했다.
- `reference-project/.agents/skills/update-project-context/`를 추가하고 Reference root 지침·README·이식 절차에서 발견하도록 연결했다. 기존 Project 관리 skill이 다른 이름으로 존재해도 책임을 대조하게 했다.
- 지속 관리 기준은 Project README가 소유한다. Skill은 근거 선택·기존 문서 반영·확인·보고를 맡으며 Workspace Maintain과 분리된다.
- 사용자는 보완 결과를 확인한 뒤 “그래 커밋까지 하자”라고 요청했다. 이번 변경의 revision은 `git log -1 --oneline -- reference-project/.agents/skills/update-project-context/SKILL.md`에서 확인한다. 기존 untracked `.DS_Store`는 변경·commit 대상에서 제외한다.

## 유지·보류한 범위

- `common/current/guidance` 물리 layer, bounded Project 선택과 Recover schema `6`은 유지한다.
- Workspace·Spec 관계의 추가 규칙화는 보류한다. 기존 구조·표현과 Verify 계약·필수 여부를 이번에 바꾸지 않는다.
- `decisions/` 기록 항목의 별도 보완은 이번에 확정하지 않았다.
- 제품 코드·test, Work Harness runtime·hook·machine 계약·receipt·status, 외부 TripProof와 연구 저장소는 수정하지 않았다.
- `claim-impact-review`, `direction-gap-review`, 제품 수렴·코드 평가 workflow와 실제 외부 target migration은 여전히 별도 작업이다.

## 이번 확인

- 새 `update-project-context`와 수정한 `apply-context-harness`는 공식 skill validator를 통과했다.
- `recover 001-default-timeout --json`과 id 없는 `recover --json`은 모두 exit `0`, schema `6`이며 같은 Workspace와 네 Project 문서를 선택한다. 수정한 Project README가 실제 packet에 포함된다.
- 기존 Verify receipt의 freshness는 이전 경로 이동 때문에 계속 `stale`이다. 새로운 제품 실행 결과나 acceptance로 바꾸지 않았다.
- 변경·추가된 Markdown 14개의 local link 132개, 새 skill UI metadata와 `git diff --check`를 통과했다. 정적 검사와 main의 문장·근거 대조는 실제 host skill discovery·자동 호출·장기 맥락 보존 효과를 증명하지 않는다.

## 바로 다음 행동

이후 실제 Project 작업에서 관리 skill의 discovery·호출과 맥락 보존을 확인할 수 있다. 외부 target 적용과 후속 수정은 사용자 지시에 따른다. Workspace·Spec과 Verify의 보류 결정을 다시 구현 과제로 올리지 않는다.
