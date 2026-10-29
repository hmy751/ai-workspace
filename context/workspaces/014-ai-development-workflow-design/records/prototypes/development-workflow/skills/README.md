# 개발·작업 판단·설명 스킬 prototype

이 폴더는 실행 지침을 구성한 prototype이며 전역이나 실제 제품에 설치한 상태는 아니다. 각 SKILL.md가 호출 조건과 실행 방법을 소유한다.

| 필요한 일 | 현재 본문과 상세 |
| --- | --- |
| 사용자 요청으로 대화와 현재 체계의 개선을 찾고 함께 선택·반영한다 | [improvement-loop](improvement-loop/SKILL.md) · [적용 사례](improvement-loop/references/application.md). 경험 보존·재조회는 [Personal 관리 본문](../noline-demo/context/personal/experience/MAINTENANCE.md)이 맡고 실행·판단은 스킬 본체가 맡는다. |
| 개발 작업의 맥락·구현·검토·확인·결과를 조율한다 | [development](development/SKILL.md) · [개선 검토](development/references/review.md) · [검증 상세](development/references/verification/INDEX.md) · [실행 배치](development/references/execution.md) |
| 구현·수정의 설계·완성·자기 확인·인계를 수행한다 | [구현 상세](development/references/implementation.md). Main이 구현을 겸해도 같은 책임을 적용한다. |
| 검사·기존 결과가 현재 주장을 뒷받침하는지 판단한다 | [검사 근거 판단](development/references/verification/evidence.md). 검증자뿐 아니라 Main·구현·조사 담당이 필요한 때 사용한다. |
| 질문에 필요한 원문을 골라 실제 판단에 사용한다 | 대상 context의 공통 참조. 이 demo에서는 [USAGE](../noline-demo/context/USAGE.md)를 사용한다. |
| 지정한 Personal·Project 본문에 확인된 의미를 반영한다 | [context-update](context-update/SKILL.md). 내용의 권위·관리 기준은 대상 영역에 남는다. |
| 요청된 새 독립 Work를 구성하고 인수 가능한지 확인한다 | [create-context-workspace](create-context-workspace/SKILL.md) · demo의 [생성·전환 계약](../noline-demo/context/work/workspaces/CREATE-AND-TRANSITION.md) |
| 기존 작업 정의가 충분한지, 무엇을 더 구체화할지 판단한다 | [work-discussion](work-discussion/SKILL.md) |
| 개념·코드·작업 결과·앞선 말의 뜻과 관계·선택 이유를 설명한다 | [explain](explain/SKILL.md) |
| 원자료를 골라 관계·조건·이유를 실제 설명으로 만든다 | [설명 작성 상세](explain/references/constructing-explanations.md) |
| 앞선 말의 원뜻과 현재 타당성을 대조해 보완·정정한다 | [앞선 발화 상세](explain/references/prior-explanation.md) |
| 설명·논의에서 현재성·근거·판정 경계를 구별한다 | [공통 기준](shared/explanation-and-evidence-criteria.md) |

explain은 기존 작업물 브리핑과 설명 복구를 대신하는 현재 진입점이다. 본체가 질문 범위와 실제 대상·결론의 연결을 수행하고, 필요한 조건에서 두 상세를 함께 사용한다. 작성 상세는 전체 코드와 한 대목의 후속, 실제 요약의 빠진 처리, 역할 설명과 선택 판단에 맞는 근거를 구별해 보여 준다. 앞선 발화 상세는 원뜻과 현재 타당성의 대조를 맡는다. [형성 자료](explain/_background/README.md)에는 원래 목적·사용자 정정·레퍼런스의 선별·리뷰·실제 관찰과 한계를 보존했다. 실행 본문 반영과 실제 설명 효과 확인은 별개다.

development는 Main의 맥락 선택·재탐색·종합·전달·갱신을 소유한다. Personal은 개인 판단 기준을, Project와 Work는 제품 맥락과 이번 작업을 계속 소유한다. 첫 결과를 구성할 때 explain으로 목표·실제 변경·확인에서 결론까지 연결하며, 답을 바꿀 사실 공백의 추가 확인은 작업 담당자가 맡는다. 상세 인계·호출·수정·종료의 설계 상태는 development 본문과 [형성 자료](development/_background/README.md)에서 확인한다.

work-discussion은04-01에서 기존 정의의 충분성과 필요한 구체화를 직접 답하는 최소 보완을 채택했다. reconsider-work는 보존 원형을 유지하고 여기에 설치한 스킬로 취급하지 않는다. development가 현재 본문에서 전제 재판단을 수행하며 실제 대상의 호환 스킬이 있으면 그 발동 조건에 따라 연결한다. [형성 자료](work-discussion/_background/README.md)에서 근거를 확인한다.

기존 read의 일반적인 선택·대조 방법은 USAGE로 옮겼다. 개발 중 담당자와 직접 읽기 요청이 같은 방법을 사용하며, 새 읽기 스킬의 호출이나 보고서를 전제하지 않는다. 기존 update는 대상의 관리 기준을 따르는 한정 반영 과업으로 재구성했고, create는 수동 demo의 생성·인수·전환 계약에 연결했다. Work의 일상 유지와 전체 완료는 Main·Work·development가 맡는다. 실제 설치판의 옛 호출·bridge 교체는 별도 배치 과제다.

USAGE와 context-update라는 형태는 잠정 합의를 이 prototype에서 실행할 수 있게 펼친 것이다. 같은 수행자가 유효한 근거로 읽기·검토·반영을 이어가며, 파일이 나뉘었다는 이유로 재입력·전면 재독·새 담당자를 요구하지 않는다. 실제 사용 부담이 드러나면 이 묶음을 다시 판단할 수 있다.

## 공통 기준과 관리

공통 설명·근거 기준의 현재 consumer는 work-discussion과 explain이다. consumer가 필요한 조건에서 읽으며 모든 AI 응답의 상위 workflow로 자동 적용하지 않는다. 이 안내가 현재 본문과 의존 자료의 읽기 경로를 소유하고, 실행 방법과 읽을 조건은 각 본문이 소유한다.

스킬을 새로 만들거나 의미·구성을 바꾸는 주체는 [SKILLS-CONTENT-POLICY](SKILLS-CONTENT-POLICY.md)를 적용한다. 해당 본문·실행 상세·형성 자료와 실제 호출자를 함께 갱신한다. 실제 설치할 때에는 필요한 상세와 shared 기준도 동반하고 대상의 운영 계약을 확인한다.

## 이전 두 스킬의 기록

기존 두 스킬 폴더는 사용자 요청으로 삭제했다. 당시 본문과 형성 자료는 explain의 [이전 브리핑 기록](explain/_background/legacy/work-artifact-briefing/README.md)과 [이전 복구 기록](explain/_background/legacy/explanation-recovery/README.md)에 보존한다. 이 자료는 실행·설치 대상이 아니다.

[이전 스킬 안내 원문](explain/_background/records/2026-10-23-skills-index-before-explain.txt)에는 당시 채택·보류 상태와 후보 비교가 남아 있다. 현재 구성의 이유는 [통합 기록](explain/_background/records/2026-10-23-unification.md)이 설명한다.
