# 공동 스킬과 Spec·Ticket 통합

이 디렉터리는 [기존 공동 스킬 준비본](../06-judgment-and-understanding-application/README.md)에 [Spec·Ticket 통합 결과](../07-context-harness-spec-ticket-integration.md)를 연결한 논의와 수정 준비본을 소유한다. [Workspace 012](../../../../workspaces/012-skills-spec-ticket-integration/README.md)에서 합의한 내용을 네 스킬에 반영했다.

**현재 결과는 미설치 준비본 [v0](v0/README.md)다.** 네 스킬의 역할과 호출 조건을 유지하면서 Spec의 구체화, Ticket과 실제 결과의 대조, Main의 판단과 Maintain의 문서 갱신 관계를 연결했다. 실제 설치 프로젝트는 미정이며, Context Harness의 Spec·Ticket·Maintain 운영을 전제로 만든 배포 사본이다.

이후 [Spec·Ticket 정의와 범위](03-spec-ticket-definition-and-scope.md)를 확정하고, 제3 리뷰를 거쳐 [Ticket 네 구성요소](04-ticket-components-and-rationale.md)를 채택했다. Work당 Spec 하나와 기존 Spec 다섯 구성을 유지하고, Ticket은 기능 구현·코드 개선 등 작업 성격에 맞는 확인 가능한 결과를 만드는 실행 단위로 둔다. 합의 문서와 최초 v0를 `7fa7bde`에 보존한 뒤, 이 후속 합의도 v0의 논의·재판단·작업물 설명에 반영했다. 상세 변경과 확인 범위는 [검토 기록](02-review-and-validation.md#후속-합의의-v0-반영)에 있다. Context Harness의 상위 운영 계약은 아직 수정하지 않았다.

## 읽을 문서

- [논의 결정](01-discussion-decisions.md): 스킬 수정 전에 합의한 방향, 중요한 사용자 정정, 기존 상위 계약과 이번 운영 선택의 구별을 보존한다.
- [Spec·Ticket 정의와 범위 확정](03-spec-ticket-definition-and-scope.md): v0 작성 뒤 채택한 두 정의, 작업별 Ticket 범위와 설계 개선의 관계, 기존 Spec을 유지하는 이유를 남긴다.
- [Ticket 구성요소와 구성 이유](04-ticket-components-and-rationale.md): 네 기본 구성, Matt의 근거와 우리 운영에 맞춘 차이, Spec·state·records와의 관계를 보존한다.
- [v0 안내](v0/README.md): 실제 수정 스킬과 배포 구성, 기존 준비본 대비 변경, 적용 전제를 안내한다.
- [검토와 확인 범위](02-review-and-validation.md): 수행한 검사와 검토 근거, 실제 설치·실행으로 아직 확인하지 않은 범위를 남긴다.

`v0/payload/`가 수정 스킬과 함께 옮길 공통 기준의 실제 파일을 소유하고, `v0/manifest.json`은 입력 출처·파일 차이·해시·상대 연결을 기록한다. 이 README는 묶음의 범위와 진입점을, Workspace의 current는 진행 중인 판단과 다음 행동을 맡는다. 후속 수정을 수행하는 Main이 논의 근거와 준비본·검토 기록의 관계를 함께 유지한다.

## 이번 작성의 범위

사용자는 논의 문서를 먼저 만든 뒤 다음과 같이 요청했다.

> 아냐 그럼 08 문서말고 08 디렉토리파고 해당 문서 넣고
> 거기에 v0 해서 합친 결과물 만들어놓자

이에 기존 08 문서를 이 디렉터리의 `01-discussion-decisions.md`로 옮기고, 합의한 변경을 `v0`에 작성했다. 기존 06 준비본은 입력 판본으로 유지한다. Spec·Ticket의 다섯 파일 구성, Recover, Main·Maintain 상위 계약과 실행 장치는 기존 Reference가 소유하며 이 묶음에 복사하지 않는다.

현재 연구 저장소나 전역 스킬 경로에 설치한 것은 아니다. 준비본 작성과 정적 검토의 완료는 실제 host의 발견·호출, 비동기 갱신, 작업 품질이나 사용자 이해가 개선됐다는 근거와 구별한다.
