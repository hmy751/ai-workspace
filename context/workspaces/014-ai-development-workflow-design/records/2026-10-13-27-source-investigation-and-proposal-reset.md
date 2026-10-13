# 원자료 조사와 앞선 합성안의 재검토

2026-10-13. 이 기록은 Matt·Lauren·Vercel의 실제 방법을 조사한 결과를 현재 설계에 연결하는 진입점이다. 새 운영안의 채택 기록이 아니다.

## 사용자 요청

> 이러지말고 matt, 라우렌 자료 찾아서 관련 부분을 어덯게 하는지 더 구체적으로 먼저 조사하자 난 사실 확신이 안서 니가 그냥 이렇게 제시하는게 뭘 바탕으로 한건지도 모르겠고 vercel 도 어떻게 할지 기존 자료와 추가 자료 등 좀 조사하고 정확히 이해하고

Main이 만든 기록 22·23은 강연의 일부 권고, 기존 ai-workspace의 Spec·Ticket 책임, Main의 판단을 합친 가설이었다. 그 근거를 나열했어도 각 원자료의 실제 작업 방법과 우리 제안을 충분히 구별해 설명하지 못했다. 현재는 그 가설을 더 상세화하기보다 출처별 실제 입력·행동·산출물·적용 조건을 먼저 이해한다.

## 조사 결과를 읽는 경로

| 자료 | 확인 범위와 상세 기록 |
| --- | --- |
| Matt Pocock | 제공된 강연·스킬 사본, AIHero 공식 설명, 과거 기준 `068b6e0`과 현재 공개 저장소 `49dd158`의 작업 정의·구현·TDD·검토·회고. [조사 24](2026-10-13-24-matt-source-investigation.md) |
| Lauren Tan | 제공 강연, 저자와 공개 저장소의 관계, 현재 `cursor/plugins`의 pstack `997ffc7`에서 기능 개발·구조 설계·검증 스킬 생성/유지·shipping. 강연 당시의 구현과 현재 공개판은 구별한다. [조사 25](2026-10-13-25-lauren-source-investigation.md) |
| Vercel | 제공 글과 공식 live 본문 대조, 공개 product-design 예시, 별도 공개 agent-skills·가이드·검사와 Vercel Agent 문서의 범위. [조사 26](2026-10-13-26-vercel-source-investigation.md) |

각 기록에 URL·접근 시점·고정 commit 또는 판본 정보·필요한 짧은 원문과 한계를 남긴다. 기존 source 사본은 수정하지 않는다. 공개된 skill 파일에 계약이 있다는 사실과 실제 실행 효과가 확인됐다는 사실은 구별한다. 이번에는 설치·제품 실행·외부 서비스 변경을 하지 않았다.

## 먼저 바로잡을 이해

**Matt의 설계는 ‘구현은 동작, 검토는 좋은 설계’ 한 문장으로 충분하지 않다.** 현재 `to-spec`에는 이미 논의한 모듈·인터페이스와 테스트 관련 결정이 들어가며 테스트 경계를 확인한다. `implement`는 그 경계를 바탕으로 TDD를 수행한다. 강연의 standards 집중 권고와 실제 구현 스킬의 설계·테스트 입력을 함께 봐야 한다. 공식 설명은 검토가 커밋 전 변경을 못 볼 수 있다는 연결 문제와 findings 수정·Ticket 종료의 공백도 밝힌다. [to-spec](https://www.aihero.dev/skills-to-spec), [implement](https://www.aihero.dev/skills-implement)

**Lauren의 현재 공개 구성은 구현 전에 구조를 구체화한다.** pstack의 기능 개발 절차는 관련 시스템을 이해하고 설계 대안을 탐색한 뒤 데이터 형태·범위·성공 기준을 주어 구현을 위임한다. `architect`는 호출자 사용 예, 타입·함수 모양, 모듈 구성을 먼저 다룬다. 별도 계획 문서를 기본으로 두지 않는다는 README 문장을 ‘선행 설계를 하지 않는다’로 읽으면 안 된다. [feature](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/poteto-mode/playbooks/feature.md), [architect](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/architect/SKILL.md)

**Vercel의 모드는 에이전트 분업 순서가 아니다.** 제공 글의 shape·implement·review는 요청에 따라 선택하는 동작이다. 구현에서도 제품 판단·인터페이스 품질 기준을 읽고 도달 가능한 상태를 확인한다. review는 별도 요청 없이 수정하지 않는다. 코드 작성 시점에 기준을 적용하는 방식과 검토 모드의 권한을 따로 봐야 한다. [공식 글](https://vercel.com/blog/teaching-agents-product-design-at-vercel)

## 역할 배치 외에 구체적으로 확인한 방법

**Feature Map과 자료 routing은 확인된 기능부터 구별한다.** Lauren의 공개 생성 스킬은 프로젝트 검증 스킬·기능 색인·기능별 실행 방법을 만들고 한 기능을 실제로 실행하게 한다. Notes 예제는 저장 표시만 보지 않고 목록에서 다시 열어 영속성을 확인하며, 명령과 관측 결과·증거를 짝짓는다. 유지 스킬은 소스 조사와 실제 앱 확인을 구별하고 제품 결함을 문서 수정으로 덮지 않는다. Vercel product-design의 routing은 요청에 맞는 판단 기준과 canonical을 찾아 읽게 한다. 이 두 기능만으로 서로 대체한다고 판단할 수 없으며, 기존 Project context와의 배치·중복은 이후 설계 대상이다. [생성 스킬](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/create-verification-skill/SKILL.md), [Notes 예제](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/create-verification-skill/references/feature-map-example/create-note.md), [Vercel 글](https://vercel.com/blog/teaching-agents-product-design-at-vercel)

**경험을 반영하는 대상과 승인도 서로 다르다.** Matt의 `retro`는 반복 가능한 위반을 기존 검사와 대조해 자동 검사 후보로, 판단이 필요한 기준은 검토용 문서 후보로 제안한다. Lauren의 `correct`는 반복 실수를 코드 구조·타입·검사·테스트로 막는 방법을 먼저 검토하고 판단이 필요한 경우에 문서를 쓴다. Vercel 글은 원자료 수집·기준 후보 판단·사람의 선택을 구별한다. 이를 모두 ‘작업 후 메모를 갱신한다’로 줄이면 자료의 중요한 차이를 잃는다. 세 자료의 공개 절차를 우리 자동 Maintainer 재개 근거로 사용하지 않는다. [Matt retro](https://www.aihero.dev/skills-retro), [Lauren correct](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/correct/SKILL.md), [Vercel 글](https://vercel.com/blog/teaching-agents-product-design-at-vercel)

## 앞선 우리 제안은 무엇에 근거했나

| 앞선 설명 | 실제 근거와 현재 처리 |
| --- | --- |
| Project는 공통 맥락, Spec은 이번 결과, Ticket은 수행과 근거를 맡는다 | 주로 기존 ai-workspace의 [Spec](../source/ai-workspace-baseline/reference-project/context/work/workspaces/spec-and-tickets/SPEC.md)·[Ticket](../source/ai-workspace-baseline/reference-project/context/work/workspaces/spec-and-tickets/TICKET.md), [Noline Project](../source/noline-baseline/context/project/README.md)의 역할을 간추린 Main의 구성이다. 세 외부 자료가 공통으로 제시한 문서 체계가 아니다. |
| 이번 Spec은 목표·동작·범위를 적고 내부 설계는 구현·검토에서 발전시킨다 | 유효할 수 있는 우리 가설이나, 앞선 짧은 예시는 선행 구조·테스트 설계의 정도를 충분히 드러내지 못했다. Matt의 Implementation/Testing Decisions, Lauren의 구조 스케치와 구체적인 차이를 다시 논의해야 한다. |
| 상세 품질 기준을 검토자에게 집중하는 쪽이 우선이다 | Matt 강연의 권고를 전체 기준 배치의 출발점으로 확장한 Main의 추천이었다. 현재 공개 TDD·구조 설계와 Vercel의 구현 모드는 구현 단계에도 기준을 적용한다. 기준의 종류·시점·적용 주체를 확인하기 전 일반 기본안으로 두지 않는다. |
| 직접 수정한 검토자가 최종 실제 확인도 맡는다 | 앞선 사용자 질문에 답하며 만든 우리 진행안이다. 세 자료의 공통 계약이 아니다. 특히 pstack의 shipping은 코드 작성에 참여하지 않은 주체의 실제 표면 검증을 별도로 요구한다. 기능 작업의 초기 확인과 shipping 판정을 같은 단계로 합치지 않는다. |
| 기능 설명·실행 방법·품질 기준을 Project에 배치한다 | 기존 Project 역할과 강연을 연결한 후보였다. 실제 공개 생성 스킬의 산출물과 기존 canonical을 확인한 뒤 무엇을 어디에 둘지 판단해야 한다. Feature Map과 자료 routing의 대체 여부도 이름만으로 정하지 않는다. |

수정 주체에 관한 B 선택은 사용자 선택으로 유지한다. 그러나 B를 선택했다는 이유만으로 선행 설계의 깊이, 입력의 구성, 최종 검증의 독립성까지 모두 결정됐다고 보지 않는다. [pstack shipping의 실제 계약](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/poteto-mode/playbooks/shipping.md)

## 이후 논의의 출발점

다음에는 우리 인수 예시를 다시 다듬기 전에 **각 자료가 구현 전에 무엇을 정하고 남기는지**부터 실제 본문으로 논의한다. Matt의 결정 기록·테스트 경계, Lauren의 구조 스케치·작업별 절차, Vercel의 제품 brief·상태와 기준 선택은 각각 다른 방법이다. 먼저 이 차이를 이해한 뒤 기존 Spec·Ticket과 어떻게 연결할지 판단한다.

관련 Ticket은 이 조사로 구체화할 근거가 늘어난 상태다. 외부의 체계를 채택하거나 01·02·03·04의 설계를 완료한 것은 아니다. 전체 잠정안은 논의를 모으는 역할을 유지하고, 기록 22·23은 재검토할 분석 이력으로 보존한다. 자동 Maintainer는 재개하지 않으며 글로벌 코드 퀄리티 문서를 설계 비교의 기준으로 다시 가져오지 않는다.
