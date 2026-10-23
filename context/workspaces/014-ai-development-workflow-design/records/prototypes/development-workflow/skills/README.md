# 개발·작업 판단·설명 스킬 prototype

현재 실행 본문은 `development`, `work-discussion`, `explain`이다. 이 폴더는 설계 prototype이며 전역이나 실제 제품에 설치한 상태는 아니다. 각 SKILL.md가 호출 조건과 실행 방법을 소유한다.

| 필요한 일 | 현재 본문과 상세 |
| --- | --- |
| 개발 작업의 맥락·구현·검토·확인·결과를 조율한다 | [development](development/SKILL.md) · [검토 상세](development/references/review.md) |
| 기존 작업 정의가 충분한지, 무엇을 더 구체화할지 판단한다 | [work-discussion](work-discussion/SKILL.md) |
| 개념·코드·작업 결과·앞선 말의 뜻과 관계·선택 이유를 설명한다 | [explain](explain/SKILL.md) |
| 원자료를 골라 관계·조건·이유를 실제 설명으로 만든다 | [설명 작성 상세](explain/references/constructing-explanations.md) |
| 앞선 말의 원뜻과 현재 타당성을 대조해 보완·정정한다 | [앞선 발화 상세](explain/references/prior-explanation.md) |
| 설명·논의에서 현재성·근거·판정 경계를 구별한다 | [공통 기준](shared/explanation-and-evidence-criteria.md) |

explain은 기존 작업물 브리핑과 설명 복구를 대신하는 현재 진입점이다. 본체가 기본 설명을 직접 수행하고, 필요한 조건에서 두 상세를 함께 사용한다. 관계·이유·근거를 한 작성 상세로 묶고 자료 선정 이유와 실제 짧은 설명을 연결하는 예시를 넣었다. [형성 자료](explain/_background/README.md)에는 사용자 목적·정정, 실제 source와 리뷰, 이번 선택의 한계를 보존했다. 생성·연결 정리와 실제 설명 효과 확인은 별개다.

development는 Main의 맥락 선택·재탐색·종합·전달·갱신을 소유한다. Personal은 개인 판단 기준을, Project와 Work는 제품 맥락과 이번 작업을 계속 소유한다. 결과의 관계·선택 이유를 설명할 필요가 생기면 explain을 사용하며, 답을 바꿀 사실 공백의 추가 확인은 작업 담당자가 판단한다. 상세 인계·호출·수정·종료의 설계 상태는 development 본문과 [형성 자료](development/_background/README.md)에서 확인한다.

work-discussion은04-01에서 기존 정의의 충분성과 필요한 구체화를 직접 답하는 최소 보완을 채택했다. reconsider-work는 기존 유지로 결정해 여기에 교체 본문을 만들지 않았다. [형성 자료](work-discussion/_background/README.md)에서 근거를 확인한다.

## 공통 기준과 관리

공통 설명·근거 기준의 현재 consumer는 work-discussion과 explain이다. consumer가 필요한 조건에서 읽으며 모든 AI 응답의 상위 workflow로 자동 적용하지 않는다. 이 안내가 현재 본문과 의존 자료의 읽기 경로를 소유하고, 실행 방법과 읽을 조건은 각 본문이 소유한다.

스킬을 새로 만들거나 의미·구성을 바꾸는 주체는 [SKILLS-CONTENT-POLICY](SKILLS-CONTENT-POLICY.md)를 적용한다. 해당 본문·실행 상세·형성 자료와 실제 호출자를 함께 갱신한다. 실제 설치할 때에는 필요한 상세와 shared 기준도 동반하고 대상의 운영 계약을 확인한다.

## 이전 두 스킬의 기록

기존 두 스킬 폴더는 사용자 요청으로 삭제했다. 당시 본문과 형성 자료는 explain의 [이전 브리핑 기록](explain/_background/legacy/work-artifact-briefing/README.md)과 [이전 복구 기록](explain/_background/legacy/explanation-recovery/README.md)에 보존한다. 이 자료는 실행·설치 대상이 아니다.

[이전 스킬 안내 원문](explain/_background/records/2026-10-23-skills-index-before-explain.txt)에는 당시 채택·보류 상태와 후보 비교가 남아 있다. 현재 구성의 이유는 [통합 기록](explain/_background/records/2026-10-23-unification.md)이 설명한다.
