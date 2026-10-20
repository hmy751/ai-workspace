# 본문·사례와 맥락·근거의 구성 개선 — 두 리뷰어의 공통 입력

2026-10-20. 이 문서는 두 리뷰어에게 동일하게 제공하는 과제와 자료다. 기존 Main의 구성안·평가 결론이나 상대 리뷰어의 의견은 1차 입력에 포함하지 않는다.

## 이번에 필요한 일

현재 자료를 어떻게 구성하고 관리하면 사용자 의도를 더 잘 실현할 수 있을지 독립적인 개선안을 제시한다. 기존 안의 합격·불합격을 판정하는 검증이 아니다. 실제 문서와 필요한 외부 원자료를 읽고, 구체적인 구성·내용·관리 방식을 제안한다.

두 리뷰어는 먼저 서로의 안을 보지 않고 전체안을 만든다. 두 안이 완성된 뒤 Main이 상대 안을 전달해 한 차례 교차 검토·수정을 요청한다. 일부러 반대하거나 합의를 만들 필요가 없다. 같은 의견도 근거를 설명하고, 차이가 남으면 조건·이유와 함께 남긴다.

## 사용자 원문

앞선 범위 설명:

> 데모에 여러 본문에 적용할거고 이름 기준 묶음도 해당하는거 아닌가? 우리가 이거 ㄹ다루는 거잖아? 그러니까 하나에 묶어서 관리하는데 이제 데모에서는 여러 본문에서도 근데이것도 범위를 좀 생각해봐야긴 한데 데모에서는 일단 적용할 관리원칙으로 둬야되지 않나해

구성에 대한 정정:

> 여기서 하나 차이가 있는게 case를 점 해서 한건 좋은데 중요한건 context, evidence등은 뭐랄까 이걸 형성하는 의도? 이런거 잖아? 항상 읽고 사용하는 본문 역할이 아니란거지 수정하거나 이럴때 필요한 맥락 더 정확한 맥락이 필요해서 구성하는거지 근데 가까이두는건 이런게 자꾸 유실되니까 시간이 지나면 그래서 같이 두는거고 너무 중앙에 record같은데만 두고 관리하는건 유실될 단점이 있어서 그걸 보완하는거지
> 근데 여기서 case는 어찌보면 수정 근거라기보다 읽고 쓰는 어찌보면 본문과 같은 위치잖아? 근데 context랑 나란히 두는게 안 조아보여 그래서 그것도 폴더로 나누든 해서 구분하는 그런 정책이 필요해보여 여기선 completion 문서랑 case가 본문 역할이고 context, evidence가 뭐 보조? 적합한 단어는 안 떠오르는데 아무튼 그런 층위 인거고
>
> 근데 기준을 그냥 니가 적절한걸 했잖아? 그것보다 아까 외부 레퍼런스랑 내 의도 랑 고려해서 제3리뷰어한테 전달해서 물어보자 검증이 아니라 개선할 이룰 그런 리뷰어 뭐 아니면 아까 필요한 레퍼런스랑 내 의도랑 잘 아무튼 한번 물어봐봐

토론 방식에 대한 우려:

> 잠깐 그냥 리뷰어한테 종합하란것보다 토론 ? 시키는게 나을라나? 그러니까 리뷰어가 각 관점을 서로토론? 이거에 대해서 먼저 설명해줘 뭐가 나을까? 어떻게 한느게 하나의 의견만 손들라는건 아닌데 그냥 단순히 다 종합해버릴까? 싶어서

현재 요청과 추가 의견:

> 그래 그 방식으로 해보자. 본문·사례와 맥락·근거의 층위를 구분하려는 내 의도랑 실제 문서, 외부 레퍼런스를 주고 두 명이 독립적으로 안을 낸 뒤 서로 검토하게 해줘. 억지로 합치지 말고 쟁점별로 뭐가 같고 어디서 갈리는지 이유랑 같이 가져와.
> 하나 더 그 맥락 근거 층위에 일단 내 개인적인 견해는 의도 배경 목적 정도는 웬만하면 있었으면 좋겠다는 뉘앙스도 추가로 전달해줘 정담 진리라기보다 내의견

추가 의견은 사용자 선호다. 매번 의도·배경·목적이라는 세 제목이나 별도 파일을 반드시 채워야 한다는 규칙으로 올리지 않는다. 어떻게 반영하면 좋은지와 반영의 한계를 설명한다.

## 실제 검토 대상

대상물 루트:

`/Users/hammyeong-yeon/Desktop/ai-workspace/context/workspaces/014-ai-development-workflow-design/records/prototypes/development-workflow`

루트 아래 다음 실제 파일에서 시작한다.

- `README.md`
- `noline-demo/context/README.md`
- `noline-demo/context/personal/README.md`
- `noline-demo/context/personal/development/README.md`
- `noline-demo/context/personal/development/naming-and-completion.md`
- `noline-demo/context/personal/development/cases/naming-and-completion.md`
- `noline-demo/context/personal/development/naming-and-completion.context.md`
- `noline-demo/context/personal/development/naming-and-completion.evidence.md`
- 필요한 경우 `noline-demo/context/work/DEVELOPMENT.md`, `noline-demo/context/project/MAINTENANCE.md`

현재 문서의 진술·배치 자체도 개선 대상이다. 여기에 적혀 있다는 이유로 형식·정책이 이미 사용자에게 확정됐다고 취급하지 않는다.

prototype이 바깥 설계 Workspace의 records 아래에 저장된 것과, 그 안의 Personal·Project·Work의 내용 책임은 다르다. 대상물을 읽는 사람이 바깥014의 전체 작업 기록을 읽어야 이해되는 안은 피한다. 필요한 판단 근거를 가까이 두는 사용자 요구는 유지한다.

외부 자료·실제 문서에서 부족한 근거를 발견하면 필요한 범위를 보고하고 추가 자료를 요청할 수 있다. 다른 Desktop 저장소나 다른 리뷰어의 출력은 탐색하지 않는다. 전체 이전 대화나 Main의108 구성안은 이번 독립 제안의 입력으로 읽지 않는다.

## 외부 레퍼런스 접근점

아래는 앞선 조사에서 찾은 1차 자료 접근점이다. 특정 배치의 정답으로 주는 것이 아니다. 제안에 영향을 주는 자료를 직접 읽고, 자료가 실제로 말하는 것과 자신의 적용 판단을 구별한다. 접근하지 못한 자료는 확인한 것으로 쓰지 않는다.

- Lauren Tan의 pstack 설계 이유 문서: [rationale-template](https://github.com/cursor/plugins/blob/ddf824aff1e55ba14bd666b30bce3fc69962abe6/pstack/skills/architect/references/rationale-template.md)
- 같은 프로젝트의 과거 의도·증거 구별: [epistemics](https://github.com/cursor/plugins/blob/ddf824aff1e55ba14bd666b30bce3fc69962abe6/pstack/skills/why/references/epistemics.md)
- Gwern Branwen의 실제 사이트: [현재 설계](https://gwern.net/design), [Design Graveyard](https://gwern.net/design-graveyard)
- Ryan Lopopolo의 공개 자료집: [ARCHITECTURE](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/ARCHITECTURE.md), [docs 작성 원칙](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/docs/AGENTS.md), [sources 관리 원칙](https://github.com/lopopolo/harness-engineering/blob/226c8d35fb6ea3ed55467753dba6dea2b5fd5778/sources/AGENTS.md)
- 보조 자료: Andy Matuschak의 [원자료 노트와 개념 노트](https://notes.andymatuschak.org/Literature_notes_are_secondary_and_separate), Michael Nygard의 [결정 맥락 보존](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

GitHub 고정 링크를 읽지 못하면 동일 commit의 raw.githubusercontent.com 경로를 사용할 수 있다. 다른 판본을 읽으면 그 차이를 밝힌다. 공개 자료집·설계 이유 문서·실제 사이트를 모두 같은 종류의 운영 검증 결과로 취급하지 않는다.

## 1차 결과에 필요한 것

- 사용자 목적을 이루기 위한 권장 구성 한 안. 실제 이름 기준의 파일·문단을 어디에 두고 어떻게 읽게 할지 보여 준다. 필요한 층위의 이름도 제안할 수 있다.
- 현재 문서에서 유지·이동·축소·재구성이 필요한 내용을 구체적인 절이나 짧은 예로 설명한다.
- 의도·배경·목적을 웬만하면 남기고 싶다는 선호를 어떻게 다룰지, 필요한 만큼 충분한지 판단할 기준.
- 데모 공통 관리 원칙과 각 묶음 입구의 책임, 일반 사용과 수정·정확한 이해가 필요한 때의 읽기, 갱신 때 관계를 유지하는 방법.
- 포기하거나 감수하는 비용, 다른 선택이 더 적합한 조건, 상대와 논의할 가치가 있는 주요 쟁점.
- 실제로 읽은 외부 근거와 그 근거에서 도출할 수 없는 것. 독자의 설명을 자료의 주장으로 소급하지 않는다.

장문의 운영 체계나 전역 표준을 새로 설계할 필요는 없다. 서로 비교할 수 있을 만큼 구체적인 개선안을 작성하고, 사용자에게 다시 물어야만 결정할 수 있는 부분은 이유와 함께 남긴다.

## 작업 경계

prototype과 기존 workspace 문서는 읽기 전용이다. 각 리뷰어가 작성할 수 있는 파일은 Main이 별도로 지정한 자기 보고서 하나뿐이다. 다른 작업자가 있으므로 다른 파일을 수정하거나 되돌리지 않는다. 커밋·설치·자동화·제품 코드 변경은 수행하지 않는다. 1차 보고서는 완성 뒤 고정하며, 교차 검토는 별도 파일로 남긴다.
