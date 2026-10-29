# 갱신 시점과 수행자: 맷·로렌 원문 재대조

04-03의 2번 논의에서 사용자는 작업을 마친 뒤 루프 단계에서 Project를 갱신할 수도 있는지, 갱신 담당자를 정한다는 것이 별도 제3자를 뜻하는지 물었다. 두 레퍼런스 모두 모든 갱신을 별도 편집자에게 넘기는 규칙은 아니다. 다만 우리와 같은 Personal·Project·Work 전체의 갱신 담당자를 정한 공통 규칙도 확인하지 못했다. 발견·판단·채택·편집을 상황에 따라 배치하는 실제 절차를 참고할 수 있다.

## 질문과 판단 지위

사용자 직접 발화:

> 근데 만약 작업 다하고 루프단계에서 project를 갱신하려고 한다면?

> 갱신 범위와 담당자를 정하면 된다는 꼭 제3자가 해야하는건 아니고열린 얘기인거지? 그럼 종합하면 뭐가 나을까?

> 레퍼런스에서는 어떻게 되는데? 이런 상황에 대해?

Main은 앞서 “갱신할 내용과 필요한 시점을 보고, 그 근거를 이미 이해한 주체가 가능한 한 이어서 반영한다”를 제안했다. 이는 레퍼런스에 적힌 공통 규칙이나 사용자 확정 합의가 아니다. 이번 대조에서도 같은 수행자 연속을 일률적 기본값으로 입증하지 않는다. 사용자 대상 설명은 Main이 맡는 기존 책임과 지속 문서의 실제 작성자를 구별한다.

이번에는 Main이 맷의 원문을 읽고, 별도 읽기 전용 조사자가 로렌의 원문을 조사했다. Main은 reflect와 maintain-verification-skill의 핵심 본문을 직접 대조했다. 새로운 설계 개선 리뷰나 수행 효과 시험은 아니다.

## 조사 판본과 범위

- [맷 보존 manifest](../source/workflow-references/matt-pocock/manifest.json): skills 1.3.1, commit `5beb35b040e3de97e54fa9e386d7e42d15c295c2`.
- [로렌 보존 manifest](../source/workflow-references/pstack/manifest.json): pstack 0.15.29, commit `190d28736eff128ec94f502a22c7fe0c4b56cd37`.
- 2026-10-21 보존 원문과 같은 commit의 2026-10-25 보충 자료를 사용했다. 최신 배포판 확인이나 실제 작동 관찰은 아니다. source는 수정하지 않았다.

## 맷: 논의 중 확정 내용은 즉시 기록하고, 회고는 후보 제시까지 정한다

[domain-modeling](../source/workflow-references/matt-pocock/repository/skills/engineering/domain-modeling/SKILL.md)의 8행은 용어·결정이 구체화되는 순간 기록하는 적극적 설계 작업을 설명한다. 60–64행은 용어가 확정되면 그 자리에서 GLOSSARY를 갱신하고 모아서 나중에 쓰지 않도록 한다. 이 절차를 수행하는 주체가 기록하며, 별도 작성자를 호출하는 단계는 없다. 다만 GLOSSARY는 용어집이고 구현 상세나 spec을 쌓는 곳은 아니다. ADR은 되돌리기 비용, 배경 없이는 의아함, 실제 절충이라는 세 조건을 모두 만족할 때 제안한다(66–74행).

[Domain Docs](../source/workflow-references/matt-pocock/repository/skills/engineering/setup-matt-pocock-skills/domain.md)의 5–11행과 41–51행은 관련 용어·결정문을 읽고 사용하되, 언어의 공백은 domain-modeling에 연결하고 기존 결정과 충돌하면 드러내도록 한다. 따라서 읽었다는 이유만으로 누구나 용어·결정을 새로 정하는 것은 아니다.

[retro](../source/workflow-references/matt-pocock/repository/skills/engineering/retro/SKILL.md)는 사용자가 호출하는 회고다. 지정 세션의 원자료를 읽고 탐색 경로·자동 검사·코딩 기준·도구 등 환경 개선 후보를 찾아 심각도 순으로 사용자에게 제시한다(7–25행). **실제 수정 담당자나 승인 뒤 적용 단계는 이 본문에 정해져 있지 않다.** “회고 담당자가 판단하고 그대로 고친다”는 절차로 확대해 설명하면 안 된다.

[implement](../source/workflow-references/matt-pocock/repository/skills/engineering/implement/SKILL.md)와 [implement-spec](../source/workflow-references/matt-pocock/repository/skills/engineering/implement-spec/SKILL.md)에도 구현 종료 뒤 Project 문서 전체를 누가 갱신하는지의 공통 규칙은 없다. 후자는 원문 위치를 통한 소통·담당자 구현·통합·리뷰를 구체화한다. 읽기·위임 구조를 Project 갱신의 고정 담당자 규칙으로 해석하지 않는다.

## 로렌: 학습 채택과 사실 유지에 서로 다른 수행 절차를 둔다

[reflect](../source/workflow-references/pstack/repository/skills/reflect/SKILL.md)의 11행·23–58행은 사용자 호출을 받아 다음 순서로 진행한다.

1. 세 검토자가 서로 다른 관점으로 대화의 학습 후보를 찾는다.
2. 별도 종합자가 후보를 채택·탈락·보류로 정리한다. 검토자와 종합자는 편집하지 않는다.
3. 사용자에게 결과를 보여주고 실제 편집할 항목의 명시적 승인을 기다린다.
4. 승인된 기존 스킬의 사소한 수정은 parent가 직접 한다. 상당한 수정·새 스킬·발동 조건 조정은 create-skill 작성 절차로 연결한다.

원문 “the parent does it directly”는 독립 분석자를 썼다고 편집까지 제3자에게 넘겨야 하는 것이 아님을 보여준다. 반대로 “hand to ... create-skill”만으로 반드시 새 편집 agent를 생성한다고 단정할 수 없다. 이 절차의 대상은 이후 agent에게 영향을 주는 스킬 학습·개선이며, 모든 Project 사실 정정에 같은 승인·리뷰 수를 적용하라는 규칙이 아니다. 매 작업 종료마다 자동 호출하는 규칙도 아니다.

[maintain-verification-skill](../source/workflow-references/pstack/repository/skills/maintain-verification-skill/SKILL.md)의 19–37행은 검증 스킬의 문서·기능 지도·자체 도구를 유지하는 별도 절차다. 기능별 읽기 전용 조사자가 코드와 문서의 어긋남 후보를 돌려주고, coordinator가 종합·실제 앱 확인·필요한 수정을 수행한다. 별도 편집자를 추가하지 않는다. 실제 제품 결함은 문서를 고쳐 정상인 것으로 덮지 않고 보고한다. 대상 스킬 자신의 디렉터리만 수정한다.

[orchestrate](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/orchestrate.md)의 23–32행은 orchestration 상태 저장소에서 파일별 단일 작성자와 사실 게시를 정한다. 이 문장은 모든 Project 문서의 영구 작성자를 정하는 전역 규칙이 아니다. [shipping](../source/workflow-references/pstack/repository/skills/poteto-mode/playbooks/shipping.md)의 비작성자 검증 요구 역시 PR 상륙 판단의 독립성이며, 일반 문서 편집자에게 그대로 확대하지 않는다.

## 우리 설계에 대한 권고와 미정

레퍼런스에서 참고할 점은 **현재 단계의 책임자가 필요한 갱신을 끝까지 연결하고, 갱신 종류에 맞춰 판단·편집·확인의 수행자를 배치한다**는 것이다. 이미 근거를 가진 주체가 직접 쓸 수 있고, 독립 분석을 거쳤더라도 종합자가 편집할 수 있다. 같은 사람이 계속한다는 것 자체가 항상 좋은 배치의 증거는 아니다.

우리에게 적용할 후보는 다음과 같다.

- 구현 중 이미 확정·확인한 사실은 맡은 범위 안에서 구현자나 Main이 바로 정리할 수 있다. 범위 밖 변화는 Main에게 연결한다.
- 작업 완료 뒤 여러 결과를 종합해야 하면 그 정리를 맡은 주체가 실제 근거를 확인하고 직접 쓰거나 갱신을 배정한다. 원래 구현자나 별도 제3자로 고정하지 않는다.
- 루프에서 새 제품 약속·개발 기준을 채택하려면 기존 의미별 결정 권한을 따른다. 채택 후 같은 주체가 반영할 수 있으며, 독립 판단이 필요한 부분은 실제 편집과 별도로 배치한다.
- 공통 반영 방법은 갱신할 의미·Owner·영향을 다루고, 누가 언제 호출할지는 개발 수행·완료·루프 각 흐름에서 정한다. 단순 사실 정정에 reflect의 전체 학습 절차를 자동 부과하지 않는다.

이는 [2번 상세안](2026-10-26-context-02-role-execution-proposal.md)의 구현자 동시 배정 조건을 더 넓은 수행 시점과 연결할 제안이다. [3번](2026-10-26-context-03-change-records-proposal.md)의 한정 반영과 [05 루프](../current/tickets/05-improvement-loop.md)의 학습 판단을 하나로 합치거나, 05의 담당자·시점을 확정한 것이 아니다. 사용자 논의 뒤 상세안·실행 지침의 실제 수정 범위를 정한다. 이번에는 이 근거 기록과 재진입 위치만 갱신했다.
