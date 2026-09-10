# Noline 기존 이식본 현황

사용자 요청: “지금 noline 보면 예전 작업 기준으로 이식을 진행했었어 … 차이점을 분석할래? 아니면 그냥 서브 호출 시켜서 이식 스킬 대로 하면 보완 되려나? 일단 현황 파악해봐”

이번 범위는 최신 Reference 변화가 기존 Noline 이식본에 어떤 보완을 요구하는지 읽기 전용으로 확인하는 것이다. Noline 파일 수정·activation·Verify receipt 생성·commit과 subagent 실행은 하지 않았다. 별도 이식 작업의 시작·완료를 뜻하지 않는다.

## 확인한 판본과 상태

- Source: `/Users/hammyeong-yeon/Desktop/context-harness`, `main`의 `87d2102`. Reference tracked diff 없음. 앞선 사용자 요청으로 `main`을 이 커밋까지 병합 커밋 없이 이동했다.
- Target: `/Users/hammyeong-yeon/Desktop/10_work/noline`, `feat/noline-context-harness`, HEAD `b4ed41f` (`feat: apply context harness to noline`).
- Target 최초 적용 기록 `context/work/workspaces/001-noline-context-harness-application/records/2026-09-04-01-initial-application.md`는 source를 `f0bada9a0398e19721ae252b5e283eeed7e33237`로 명시한다. 이는 Source main에 이번에 이어 붙인 커밋 10개의 직전 기준이다.
- Target tracked·staged 변경 없음. Untracked `.claude/sessions/2026-09-06-codebase-analysis.md`, 같은 이름의 디렉터리, `context/` 아래 Python cache가 있다. 내용은 이번 조사에 필요하지 않아 읽지 않았으며 이후 이식 때 보호해야 한다.
- Active Workspace는 최초 이식을 다루는 `001-noline-context-harness-application` 하나다. Codex·Claude Maintain runtime 디렉터리는 관찰 시점에 모두 없다. 설정은 이미 schema v2 explicit/default-unbound다.

## 최신 Reference와의 차이

1. **Project context**: Target에는 `overview.md`, `prd.md`, `architecture.md`, `decisions/`가 있고 실제 Noline 제품·구조 설명도 있다. 그러나 최신 `common/current/guidance` 물리 경계와 갱신·내용 복원 기준이 없다. 기존 상세 `.claude/context`, rules·guards·runbooks와 flat Project 문서의 책임을 대조해 적응해야 한다. 내용이 전혀 없다는 진단이나 기계적 파일 이동은 부적절하다. Decision의 생성 조건·중요 불확실성 보존 기준도 후속 보완 대상이다.
2. **Spec·Ticket**: Target memory는 `01-goal.md`, `02-constraints.md`, `03-project-context.md`이며 Spec·Ticket 폴더와 상위 계약이 없다. 최신 Work당 Spec 하나·다섯 본문, Ticket 정의·진행 통합, Main 조율·Maintain 갱신 관계가 미반영이다.
3. **Recover·Maintain 실행**: Target Recover 계약은 schema 4, 최신은 schema 6이며 필수 Project 진입점과 memory 파일도 바뀌었다. `recover/operation.py`, `maintain/operation.py`, `maintain/codex_session.py`의 target bytes는 모두 `f0bada9` 원본과 같고 최신 Source와 다르다. 최신 Maintain은 Spec·Ticket 경로의 guarded apply와 해당 계약의 semantic 입력을 추가한다. 실행 파일만 교체하면 기존 Workspace가 새 Recover 필수 조건을 만족하지 못하므로 문서·machine 계약·실행을 함께 전환해야 한다.
4. **스킬**: Target `.claude/skills/`에는 `noline-work`, `create-context-workspace`가 있고 `.agents/skills/`는 이 두 원본의 상대 symlink다. 최신 Reference의 `update-project-context`, `work-discussion`, `reconsider-work`, `work-artifact-briefing`, `explanation-recovery`는 없다. 생성 스킬도 기존 기준이다. 공동 설명 기준·색인·root routing을 기존 dispatcher 및 bridge에 적응해야 한다.
5. **Noline 고유 적응**: Reference에 없는 `maintain/claude_hook.py`와 해당 test, Claude wrapper·settings routing을 추가했다. 원본 복사로 지우거나 Codex 전용 구성으로 바꾸면 안 된다. `scripts/check-harness.mjs`는 skill 실행면을 두 스킬로 제한하고 옛 `context/project/overview.md`를 필수로 검사하므로 새 스킬·경로와 함께 좁게 갱신해야 한다.
6. **증거 범위**: Target Verify는 `node scripts/check-harness.mjs`를 실행하지만 선언 evidence는 파일 11개다. 검사 코드는 그 밖의 전체 context Markdown, rules·guards·runbooks, app guide, agent·skill·bridge 등을 읽는다. 현재 receipt freshness는 선언 snapshot 16개만 비교하므로 실제 검사 입력 전체의 신선함을 증명하지 않는다. 최신 이식의 input closure 기준으로 검증 입력과 claim을 다시 맞춰야 한다.

## 이번에 직접 확인한 동작과 상한

- `node scripts/check-harness.mjs`: exit 0, `Harness check passed.`
- `python3 -B -m context.work.harness recover --json`: exit 0.
- 같은 Recover의 명시 `001-noline-context-harness-application`: exit 0. 기본과 명시 실행 모두 기존 memory와 overview·architecture·Decision 세 문서를 읽었다.
- Recover machine result는 `verification_passed`, receipt freshness는 `fresh`, snapshot 16개 중 변경·누락·확인 불가 0개다. 이는 구계약의 선언 입력 범위에 한정된다.
- 조사 전후 Target `git status --short --branch`의 변경 목록은 같다. Python에는 `-B`를 써 추가 cache 쓰기를 억제했다.
- 전체 Harness test, 실제 hook trust·event delivery·skill discovery, 제품 기능과 외부 환경 검증은 실행하지 않았다. 기존 기록에는 descendant-timeout test의 반복 timing failure와 actual-host 미검증이 남아 있다. 이번에 원인이나 해결 여부를 재판정하지 않았다.

## 다음 작업에 대한 판단

별도의 대규모 차이 연구를 먼저 만들 필요는 없다. 최신 `apply-context-harness`는 기존 Owner 조사·보호, 책임별 install/adapt/exclude, live consumer 전환, 검증 입력 재구성과 독립 검토를 이미 요구하므로 **기존 설치의 보완 작업으로 적용**하는 것이 맞다.

서브에이전트에 맡긴다면 우선 최신 skill에 따른 target preflight와 변경 manifest를 만들게 하고 Main이 검토한다. Scope에는 Noline 고유 Claude adapter·bridge·기존 스킬·사용자 untracked 보존, active 구형 Workspace의 호환 전환, 새 다섯 스킬과 기존 생성 스킬·검사기 조정을 명시한다. 현재 skill은 manifest 승인 후 쓰도록 하므로 단순 호출만으로 최종 설치·activation까지 자동 완료되는 작업은 아니다. 이 조사에서 실제 manifest 작성이나 새 Workspace 선택을 대신 확정하지 않았다.

## 후속: 리팩토링 평가 전 Project context 정비 시점

사용자는 이식 뒤 리팩토링 작업으로 개선안을 평가할 예정이라고 설명하고, 기존 Project context를 먼저 모두 정비할지 리팩토링 뒤에 할지의 비용·평가 영향을 물었다. 지정한 자료는 `/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/09-improvement-evaluation/`이다. README·01 평가 구조·05 개입 근거, 06 성과안과 02의 설계·기여·비교·비용 절을 읽었다. 03 외부 출처 전체와 다른 저장소 원대화는 이번 질문에 필요하지 않아 확장 조사하지 않았다.

평가안이 이미 명시한 기준:

- 02는 Workspace·Project context와 Main·Maintain 전달을 평가 대상에 포함한다. “전체 작업 방식의 기여는 여러 조건이 함께 바뀐 실제 작업에서도 관찰할 수 있다.” 특정 스킬의 단독 효과는 추가 비교가 필요하다.
- 02는 “초기 하네스 구축 비용과 매 작업에서 읽기·갱신·검토에 쓴 비용도 구분한다.” 초기 비용을 제외한 비교는 도입 후 운영 비교로 범위를 밝힌다.
- 06은 코드·문서의 시작 revision과 개입 판본을 고정하고, 실제 발생한 후속 요구·재진입을 관찰하도록 제안한다. 옛 조건을 현재 조건으로 전달하는 것은 반대 근거이며, 문서 읽기 성공만으로 후속 개발 효과를 주장하지 않는다.

이에 따른 Main의 **미채택 제안**은 다음과 같다. Project context의 책임 층·실제 본문·읽기 경로는 이식 계약에 맞게 구성하되, 기존 상세 문서 전체의 완전 최신화를 리팩토링 선행 조건으로 만들지 않는다. 먼저 실제 리팩토링 목표·범위를 고르고, 제품 목적·도메인 의미·보존할 동작·현재 책임과 소비처·관련 제약·검증 한계 등 그 작업의 판단을 바꾸는 맥락을 원자료와 대조한다. 필요한 의미를 링크나 ‘미확인’ 표기만으로 대신하지 않는다. 확인되지 않은 부분과 실제 충돌은 범위를 명시하고, 코드의 현재 사실과 채택된 요구를 구별한다. 구형 파일 배치라는 관찰만으로 제품 설명이 틀렸다고 단정하지 않는다.

리팩토링 중 발견·채택한 변화는 관련 Project·Workspace Owner에 반영해 다음 실행자가 사용하게 하고 그 실제 흐름을 관찰한다. 무관한 상세 문서 정리는 이후로 미룰 수 있다. 작업 범위가 Project 전반이면 선행 대조 범위도 넓어져야 하며 아직 구체 리팩토링 범위는 선택되지 않았다.

평가에는 정비 전 코드·문서 상태, 이식·필요 맥락 정비 뒤의 시작 상태, 리팩토링 결과를 구별해 남긴다. 맥락 정비로 얻은 사전 코드 이해와 초기 시간도 기여·비용에 포함한다. 최종 문서를 과거 실행이 읽었던 입력처럼 소급해 사용하지 않는다. 최신화와 스킬을 함께 적용한 결과는 그 구성 전체의 사례로 설명하고, 개별 스킬 단독 효과라고 주장하지 않는다. 사전 정비를 했다는 이유로 평가가 무효가 되는 것은 아니며, 처음부터 모든 기존 부채를 제거해야 한다는 요구도 평가안에 없다.

확인한 02 SHA-256: `6dc32e02dac7ca8070ee5149cedc6fdb96e72be6b442473996f2719dd8ec0c09`. 06 SHA-256: `c86b6ac91e5c997bcbde78654ae990dbcf188cfc000d4d591858bb5cd439a468`. 문서의 후속 변경이 판단에 영향을 주면 위 의존 절을 다시 대조한다. 평가안 수용·Noline 정비·이식·리팩토링은 이번 읽기 요청으로 실행하지 않았다.
