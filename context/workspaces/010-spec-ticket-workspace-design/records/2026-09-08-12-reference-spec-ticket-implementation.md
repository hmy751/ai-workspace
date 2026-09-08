# Reference Spec·Ticket 적용과 검증

## 요청과 변경 경계

사용자 요청:

> 그럼 커밋하고 작업 시작하자 reference 에 거기 결과는 커밋하진 말고

이 요청으로 이전 Reference 구현 보류를 해제했다. 먼저 010의 설계·리뷰·역할 합의·기록 정리를 commit `4fe8694` (`docs: consolidate spec ticket design and maintenance decisions`)로 남겼다. 이 커밋은 010 문서만 포함하며 `.DS_Store`는 제외했다. 그 뒤 Reference와 이번 적용 상태를 변경했으며 추가 커밋·stage는 하지 않았다.

## 적용한 구성과 이유

[Workspace Spec·Ticket canonical](../../../../reference-project/context/work/workspaces/SPEC-AND-TICKETS.md)에 실제 구성·내용·관계·읽기·갱신 기준을 두었다. 기존 합의인 Spec 다섯 부분과 이유를 실제 작업의 작성 기준으로 연결했으며, 운영 문서 자체를 각 Spec에 복제하지 않는다.

- `memory/spec/01-problem-goal-scope.md`: 문제·목표·범위
- `memory/spec/02-behavior-and-cases.md`: 요구 동작·대표 사례
- `memory/spec/03-concepts-and-contracts.md`: 개념·입출력 계약
- `memory/spec/04-quality-and-completion.md`: 품질·완료 판단
- `memory/spec/05-constraints-design-assumptions.md`: 제약·현재 설계·가정
- `memory/tickets/index.md`와 필요한 Ticket 본문: 작업 정의와 진행·결과
- 유지하는 `memory/03-project-context.md`, Workspace 전체 상황을 맡는 `state/index.md`

기존 [default-timeout 샘플](../../../../reference-project/context/work/workspaces/001-default-timeout/current/memory/index.md)의 goal·constraints 내용을 Project 제품 기준·결정과 실제 코드·테스트에 대조해 다섯 Spec 파일로 옮겼다. 반복되던 Workspace 공통 source·records·output 관리 규칙은 기존 운영 Owner가 계속 맡는다. 아직 없던 Ticket의 상태를 추정하지 않고 색인에 별도 Ticket이 없다고 적었다. 외부 여행 답변 예시의 API·숫자·정책을 이 샘플에 가져오지 않았다.

일반 Workspace 재진입의 미정 선택에는 **Spec 전체와 Ticket 색인을 먼저 읽고 필요한 Ticket 본문을 추가로 읽는 기본값**을 적용했다. 이는 Main의 이번 구현 선택이며 앞선 사용자가 본문 전체·일부 정책을 이미 확정했다고 기록하지 않는다. 오래 남는 Ticket 본문을 매번 전부 입력하는 비용을 피하고 제목·하는 일·본문 경로에서 필요한 작업으로 들어갈 수 있게 했다. 색인에는 개별 진행 상태의 별도 정본을 만들지 않는다. 개별 실행자의 Spec 범위나 쓰기 정책은 그대로 열어 둔다.

## Recover·Maintain과 생성 경로

[Recover](../../../../reference-project/context/work/harness/recover/README.md)는 memory 색인, Spec 폴더 바로 아래 Markdown 전체, memory 바로 아래 나머지 Markdown, Ticket 색인을 읽는다. 다섯 Spec·Project context 선택·Ticket 색인을 필수 구성으로 확인하고, 다른 하위 폴더를 재귀 탐색하거나 Ticket 본문을 자동 입력하지 않는다. JSON의 기존 `memory.entries`와 경로 목록을 그대로 사용하므로 packet 및 Project 선택용 recover contract schema `6`을 유지했다. 이전 goal·constraints만 있는 Workspace를 위한 이중 정의나 자동 migration은 추가하지 않았다.

[Maintain](../../../../reference-project/context/work/harness/maintain/README.md)은 Spec·Ticket 하위 Markdown까지 guarded write를 허용한다. 새 Ticket은 같은 decision에서 Ticket 색인을 갱신해 연결하고, 새 Spec·기타 memory 문서는 memory 색인에서 연결한다. Existing SHA-256·경로·symlink·local link와 zero-write outcome 검사를 유지한다. 필요한 폴더는 Workspace 생성에서 준비하며 삭제·보관·이동 자동화는 만들지 않았다. 파일별 preimage 검사는 전체 읽기 의존성의 일관성이나 여러 파일의 atomic transaction을 보장하지 않는다.

의미 판단의 규칙을 다음 주체가 실제 읽을 수 있도록 Codex Maintain bridge가 Spec·Ticket canonical을 Maintain README와 함께 제공한다. 일반 Workspace payload는 bounded Recover 입력으로 유지한다. 문서에 링크만 남기고 grounding 중 추가 읽기를 금지하면 새 구성의 관리 의미를 읽지 못할 수 있어 고정 운영 규칙을 입력으로 연결했다.

역할은 기존과 같다. Maintain은 대화·결과를 이해해 필요한 내용을 기록·갱신하고, Main이 설계·분해·위임·결과 확인과 다음 행동을 조율한다. Main만 Spec·Ticket을 쓸 수 있다는 규칙이나 Maintain의 dispatch를 만들지 않았다. 다른 실행자 결과를 Main이 받는 것과 Maintain 입력·실제 파일에 반영되는 것은 구별한다. 해당 근거와 정확한 로컬 결과 위치를 연결하고 사용할 문서의 실제 준비를 확인한다는 운용 의미를 기록했다. 자동 수집·새 승인·조율 runtime을 구현한 것은 아니다.

[생성·전환 canonical](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md)은 새 목표·요구·제약을 Spec에, 필요한 실행을 Ticket에, 전체 상황을 state에 구성하도록 맞췄다. Reference의 `create-context-workspace`와 root의 `apply-context-harness` skill은 이미 live Workspace·Harness canonical을 읽도록 되어 있어 고정된 옛 파일명을 교체할 부분이 없었다. Skill이나 root 설치 설정은 수정하지 않았다. 제품 Verify의 실행·receipt·status 책임도 그대로 두었다.

## 확인한 결과

- `python3 -m unittest context.work.harness.recover.tests.test_recover context.work.harness.maintain.tests.test_operation -q`: 51개 통과. Spec 전체·Ticket 색인 포함, Ticket 본문 비포함, 누락·symlink 거부, 새 Ticket 색인 연결, 본문 진행 갱신과 stale preimage 거부, Spec 생성 후 재복구를 확인했다.
- `python3 -m unittest discover -s . -p 'test_*.py' -q`: 최종 124개 중 123개 통과, 아래 기존 Verify 테스트 1개 실패. 변경 경로 외 제품·host adapter·임시 Recover→Verify→Recover 연결을 포함한다. 해당 연결 검사는 checked-in machine status·receipt를 변경하지 않았음을 대조한다.
- 실제 샘플의 id 없는 Recover, explicit `recover 001-default-timeout --json`, `maintain bootstrap 001-default-timeout` 성공. 실제 packet에 Spec 다섯 파일·`03-project-context.md`·Ticket 색인이 들어오며 receipt freshness는 기존 `stale`로 유지된다.
- 수정 Markdown의 local link 존재와 `git diff --check` 확인. 기존 goal·constraints 경로는 대체 설명과 역사 기록에서만 남는다. Project 제품 코드·테스트·machine 계약·기존 receipt·source·root 자동 Maintain 설정은 수정하지 않았다.

### 전체 회귀에서 남은 기존 실패

`context.work.harness.verify.tests.test_verify.VerifyTests.test_timeout_covers_descendant_after_group_leader_exits`가 descendant PID 파일 존재 확인에서 실패했다. 전체 검사 두 번에서 동일했고, 단독 실행은 통과했다.

이번 변경과의 관계를 구별하려고 commit `4fe8694`의 `reference-project/`를 임시 디렉터리에 추출해 변경 전 전체 119개 검사를 실행했다. 변경 전에도 같은 테스트가 같은 PID 파일 확인에서 실패했다. 따라서 이 변경에서 새로 생겼다고 판단할 근거는 없으며 전체 실행 환경에 남아 있던 실패로 기록한다. 근본 원인은 규명하지 않았다. 검사를 건너뛰거나 timeout을 늘려 통과시키지 않았고 Verify 코드·테스트도 고치지 않았다.

## 증명하지 않은 것과 다음 작업

구조·읽기·guarded 변경·prompt 연결의 로컬 검증이다. 실제 사용자 대화에서 Maintain이 Spec·Ticket을 적절히 선택하고 갱신하는지, 다른 실행자와의 작업이 잘 이어지는지, 새 host의 lifecycle·UI report가 동작하는지까지 입증하지 않는다. 별도 비교 실험 없이 이번 구조가 장기적으로 더 낫다고 결론 내리지 않는다.

현재 결과를 검토하고 실제 Ticket 작성·실행·결과 반영 장면을 확인할 수 있다. 기존 Verify 전체 실행 실패는 후속 조사로 남는다. Reference 적용 결과와 이번 기록은 사용자 지시에 따라 커밋하지 않는다.
