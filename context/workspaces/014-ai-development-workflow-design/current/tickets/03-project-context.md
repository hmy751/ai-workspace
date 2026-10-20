# 03 — 개발과 판단에 쓰이는 Project context를 구체화한다

상태: **완료 — 구성·대표 본문·읽기와 갱신 책임을 검토 가능한 프로토타입으로 구체화했다.** 2026-10-20 사용자 요청으로 현재 결과를 아래 완료 조건과 대조하고 마무리했다. [종료 판단119](../../records/2026-10-20-119-ticket03-closeout.md)에 근거와 후속 책임을 남겼다. 실제 운영 설치·장기 효과와 후속 워크플로·스킬 설계는 각 담당 Ticket에서 이어간다.

현재 산출물은 [development-workflow](../../records/prototypes/development-workflow/README.md)이며, [Noline demo context](../../records/prototypes/development-workflow/noline-demo/context/README.md)에 Personal·Project·Work의 실제 본문·사례·작업 장면을 구성했다. 전체 목표와 기준은 [Spec](../spec.md)이 소유한다.03 완료가 Workspace 전체나01-02·04-03·06의 완료를 뜻하지 않는다.

## 맡은 결과와 범위

Project context에 어떤 내용을 어느 정도 구체적으로 두고, 누가 어떤 작업에서 읽고 관리할지 **실제 본문 예시·구성·읽기 경로가 연결된 안**으로 만든다. 제품 의미·현재 구조·개발 가이드·선택 이유를 함께 보며, 코드 워커·검토자·작업 워크플로가 사용할 맥락도 다룬다.

문서에 따라 핵심 설명·사례·절차가 필요한 정도가 다르다는 사용자 경험을 반영한다. 목차나 길이만 바꾸는 것으로 끝내지 않고, 무엇을 이해하거나 수행하는 데 충분한지 보여 준다. 코드가 실제 패턴을 제공하는 역할과 문서·검사·도구가 맡을 내용을 비교한다. 공통 내용을 Work마다 복제하지 않으면서 실제 작업에 필요한 의미를 전달한다.

현재 맡은 결과는 구성안과 예시의 제시다. 원본 Project 전면 수정이나 장기 사용 효과 확인은 별도 상태로 남긴다. 기존 `common/current/guidance/decisions`의 이름이나 현재 폴더 수를 모든 Project의 최종 구조로 고정하지 않는다.

## 현재 결과와 선택 이유

| 결과 | 현재 구성과 이유 |
| --- | --- |
| Personal·Project·Work의 독립 책임 | 개인의 일반 판단, 제품의 계약·규약·현재 사실, 이번 적용·선택·진행을 나눴다. [102](../../records/2026-10-19-102-personal-project-update-ownership.md)에 따라 개인 기준 변경만으로 Project를 자동 갱신하지 않으며, 필요한 설명 중복은 허용한다. |
| 역할별 Project 본문 | [기기·세션](../../records/prototypes/development-workflow/noline-demo/context/project/common/device-session/INDEX.md)은 제품 의미, [인증 개발](../../records/prototypes/development-workflow/noline-demo/context/project/guidance/authentication-and-session/INDEX.md)은 개발 계약·조건별 판단, [코드 표현](../../records/prototypes/development-workflow/noline-demo/context/project/guidance/code-readability/INDEX.md)은 제품 의미를 코드로 표현할 기준, [현재 인증 흐름](../../records/prototypes/development-workflow/noline-demo/context/project/current/authentication-flow/INDEX.md)은 예제 코드·검사의 실제 지원 범위를 맡는다. 함께 읽는다는 이유로 모호하게 합치지 않았다. |
| 일반 본문·분할 본문·사례 | 일반 본문은 현재 판단에 필요한 의미·조건을 설명하고 상세 사례는 코드·사용 조건·대안의 결과를 보여 준다. 같은 동작의 이름 유지·개명 비교와 설명 의존을 줄이는 개인 지향을 구별했다. [100](../../records/2026-10-19-100-role-based-prototype-revision.md)·[101](../../records/2026-10-19-101-self-explanatory-code-priority.md) |
| 본문 가까운 형성 자료 | 의도·배경·목적, 필요한 논의·선택·정정과 최소 원문을 선별해 보존한다. 현재 읽고 사용하는 본문과 수정·재검토용 자료를 구별하고 양쪽 입구에서 읽을 조건을 알린다. [CONTENT-POLICY](../../records/prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md)가 공통 관리 기준을 소유한다. |
| 체계 지침의 역할 | [SYSTEM-GUIDANCE](../../records/prototypes/development-workflow/noline-demo/context/SYSTEM-GUIDANCE.md)는 특정 영역의 구성·작성·사용·연결·변경을 정하는 본문을 설명한다. 진입 본체를 유지하면서 상세를 나눌 수 있고, 개발에 한정하거나 대문자만으로 권한을 구별하지 않는다. [118](../../records/2026-10-20-118-system-guidance-definition-and-entry.md) |
| 기존 Work 유지 | 새 background·본문 재배치는 기존 current·Spec·Ticket·source·output·records의 형태와 제약에 섞일 수 있어 복구했다. 관련 Project 본문 링크만 현재 위치에 맞췄다. [116](../../records/2026-10-20-116-defer-work-content-policy.md) |

대상물은 바깥014 작성 기록 없이 본문을 이해할 수 있게 구성했다.014는 전체 설계의 과정·평가·정정을 보존하고, 개별 본문을 이해하거나 고칠 때 필요한 형성 이유는 대상물 안에서 찾는다. 가상 제품의 작업 사건과 실제 문서 작성 대화를 섞지 않는다.

## 완료 조건과 확인 결과

아래 네 조건은 착수 때의 조건을 유지해 대조했다. 운영 설치를 완료 조건에서 새로 빼거나 조건을 축소한 것이 아니다.

| 완료 조건 | 현재 근거와 판정 |
| --- | --- |
| 역할이 다른 대표 문서에 충분한 본문 예시가 있고, 필요한 개념·사례·절차의 수준을 선택한 이유가 보인다. | **충족.** 위 제품 계약·개발 가이드·현재 구현과 Personal 일반 기준·사례에 실제 내용이 있고,100·102 및 인접 형성 자료에서 구성·수정 이유를 확인한다. |
| 대표 작업에서 필요한 맥락을 찾아 실제 판단이나 수행에 사용할 수 있다. 위치만 알려 주거나 다음 작업 요약만 제공하는 구성으로 끝나지 않는다. | **충족.** [walkthrough](../../records/prototypes/development-workflow/walkthrough.md)는 소비자 요구·완료 계약·같은 코드 비교·선택·구현과 확인·갱신을 잇는다.107의 변경 실험,113·118의 새 독자 관찰은 제한된 장면에서 읽기와 적용을 추가 확인했다. |
| Project·Work·코드·검사·스킬·도구가 맡는 내용과 읽기·갱신 책임이 연결되고, 중복 정본이나 빠진 책임을 검토한다. | **구성안 수준에서 충족.** Project의 [MAINTENANCE](../../records/prototypes/development-workflow/noline-demo/context/project/MAINTENANCE.md)·[REFERENCE](../../records/prototypes/development-workflow/noline-demo/context/project/REFERENCE/README.md)와 [DEVELOPMENT](../../records/prototypes/development-workflow/noline-demo/context/work/DEVELOPMENT.md)가 선택·충돌·결과별 갱신을 설명한다. 코드·검사는 current에서 연결한다. 스킬 실제 보완·호출과 최종 운영 책임은04-03·01-01로 잇는다. |
| 기존 구성의 유지·보완·변경안과 영향, 사용자에게 남은 선택, 이후 효과를 확인할 장면을 제시한다. | **충족.** 115·116의 일반 본문 이동 정리와 진입·Work 복구,117의 열린 판단,118의 체계 지침 구별이 대안·영향을 남긴다.107·114의 변경 실험과118의 읽기 관찰을 실제 운영·장기 효과와 구별했다. |

73·96의 과거 전체 품질 유보는 그대로 보존한다. 이후100~118의 개선과 현재 실물을 완료 조건에 대조한 이번 판정이03의 현재 상태다. 사용자 “좋아”를 모든 문장·관리 단위·운영안의 일괄 승인으로 확대하지 않는다.

## 후속에서 이어받을 범위

- **01-01·04-03:** DEVELOPMENT의 구체 진행·인계·수정·최종 확인, 기존 스킬과의 연결 및 최종 위치·Owner. 입력 선택과 갱신 기본값은 현재 본문을 사용하되 실제 스킬 행동을 대조한다.
- **02:** Work의 기존 구성과 형성 맥락·기록 관계. 현재 Work는 그대로 두며 이번 마감을 새 정책 재적용의 계기로 삼지 않는다.
- **01-02:** 개인 코드 기준 전체와 검토·수정 방법의 완결.03의 본문 결과와 새 실행 조건을 받아 재종합한다.
- **06·07:** 실제 운영 배치·전환·전체 연결과 사용 효과 확인. 실제 Noline 수정·설치·배포는 수행하지 않았다.
- **후속 소비·변경에서 재검토:** 관련 계약·가이드를 각각 관리할지 묶을지, 형성 자료의 충분성과 유지 비용. 현재는 개별 본문과 연결을 갖춘 안이며 전역 분류를 확정하지 않았다. 구체 문제가 확인되면 관련 담당 Ticket에서03 결과까지 함께 고친다.

## 필요한 과정 근거

기존 Project의 내용과 판본 차이는 [지도77](../../records/2026-10-18-77-existing-project-content-map.md)·[비교78](../../records/2026-10-18-78-code-guides-comparison-and-applicability.md), 독립 책임과 로컬 context 배치는84·89, 역할별 본문과 갱신은100~103, 형성 자료의 조사·실험·정책은104~118에서 질문에 맞게 고른다. [기록 색인](../../records/README.md)에서 각 원문에 접근한다.

01-02의 [과정 연결65](../../records/2026-10-18-65-criteria-status-and-cross-ticket-refinement.md)와 [시안72](../../records/2026-10-18-72-short-common-and-detail-prototype.md)는 이전 판단과 조건을 복원하는 입력이다. 이전 날짜별 시안과75의 착수 인계는 원형으로 남기고 현재 첫 행동으로 읽지 않는다. 과거 current 판본은 체계 지침 커밋 `450d3a8`과 앞선 Git 이력에서 확인할 수 있다.
