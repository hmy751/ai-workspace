# 개인 기준의 운영 위치 추천과 본문 형식의 결정·구체화 구별

> 후속 선택: [86](2026-10-19-86-context-personal-choice-and-text-comparison.md)에서 사용자는 관리·축적·수정 분리를 이유로 ai-workspace `context/personal/`를 선택했다. 아래 글로벌 위치 추천은 대체된 당시 제안으로 보존한다. 형식의 결정·새 구체화 구별은 실제 본문 비교로 이어지며 운영 파일은 아직 옮기지 않는다.

2026-10-19. 사용자는 실제 위치를 미정으로만 남기지 말고 이름·위치·찾아 읽는 연결을 제안하되 아직 옮기지 말라고 요청했다. 또한84에서 사용자 생각과 레퍼런스를 ‘반영했다’는 설명이 이미 결정한 내용을 옮긴 것인지, Main이 이번에 조합한 것인지 물었다. **이 기록은 Main의 추천과 근거 구별이며 사용자 선택·설치 완료 기록이 아니다.**

## 요청과 답변 범위

> 근데 개인 기준의 실제 위치를 미정으로만 두지 말고, 지금 구조를 기준으로 어디에 어떤 이름으로 두는 게 맞는지 제안해봐. 워크플로나 스킬이 그걸 어떻게 찾아 읽을지도 같이 보여줘. 아직 실제로 옮기지는 말고.
> 그리고 하나더 니가 사용자 생각과 레퍼런스 비교랑 이런걸 반영했다고 했는데 결저오딕널 반영한거야 니가 지금 보고 임의로 조합한거야?

둘째 문장은 앞뒤 맥락에서 ‘결정된 내용을 반영했는가, 이번에 새로 조합했는가’라는 질문으로 이해했다. 최신 요청은 위치 추천을 요구하며84의 독립 책임을 철회하거나 운영 파일 이동·설치를 승인한 말은 아니다.

## 위치와 이름의 Main 추천

실제 운영 본문의 입구는 `/Users/hammyeong-yeon/.claude/personal-context/README.md`, 현재 개발 기준은 그 아래 `development/`에 두는 안을 추천한다.

```text
/Users/hammyeong-yeon/.claude/personal-context/       ← 제안; 현재 없음
├── README.md
└── development/
    ├── README.md
    └── naming-and-completion.md
```

상위 README는 개인 기준의 범위·주제·관리 책임과 현재 적용 지위를, development README는 짧은 공통과 필요한 상세의 진입을, 이름 상세는 해당 판단의 의미·조건·질문·대비를 소유한다. 개발 입구에는 선택할 본문의 현재 적용 지위를 표시하고 관리 책임을 다시 볼 때 상위 README로 올라가는 경로를 둔다. 매 작업마다 상위 전체를 다시 읽는 절차는 만들지 않는다. 지금 다루지 않은 개인 주제를 미리 채우거나 모든 개인 정보를 이곳으로 모으는 제안은 아니다. 검토 중인 문장과 시안을 두었다는 이유로 모든 내용을 확정된 전역 규칙으로 사용하지 않는다.

**이 위치는 기존 canonical이 정한 답이 아니라 현재 전역 구조를 이용하는 새 설계 추천이다.** 근거는 다음과 같다.

- 실제 [작업대 context](../../../README.md)는 Workspace와 source를 소유하고 [Reference context](../../../../reference-project/context/README.md)는 Project·Work의 맥락을 소유한다. 개인 운영 기준을 특정 개발 작업대나 대상 제품의 담당 내용으로 둘 이유는 약하다. ai-workspace에는 설계 과정·시안·판단 근거가 남는다.
- 현행 공통 전역 지침의 원천은 `/Users/hammyeong-yeon/.claude/CLAUDE.md`이며 `/Users/hammyeong-yeon/.codex/AGENTS.md`는 그 파일로 연결된다. 실제 symlink를 확인했다. 따라서 현재 운영에서는 `.claude` 이름 아래에도 두 도구가 공유하는 원천이 있다. 새 도구 중립 루트와 별도 저장소를 먼저 만들지 않고 이 발견 경로를 이용할 수 있다.
- `personal-context`라는 독립 이름으로 기준 본문과 `skills/`의 절차를 구별한다. 특정 Project의 경로나 채택 목록을 Personal 입구에 관리하지 않으며, Project README에도 개인 원천의 위치를 넣지 않는다.

| 비교한 위치 | 판단 |
| --- | --- |
| `/Users/hammyeong-yeon/.claude/personal-context/development/` | 추천. 기존 전역 원천 곁에 개인 기준의 독립 입구와 관리 책임을 둔다. 새 경계와 발견 안내는 정의해야 하며 도구 이름이 물리 경로에 남는 비용은 있다. |
| `/Users/hammyeong-yeon/.claude/references/development/` | 가능한 대안. 현행 references는 여러 workflow에 걸친 판단축이므로 개발 기준을 원천적으로 금지하는 곳이 아니다. 다만 개인의 표현 선호·상세 가이드 묶음 전체를 shared reference로 올리는 판단과 개인 묶음의 독립 관리가 섞이지 않도록 별도 검토가 필요하다. 이번에는 독립 Personal 입구를 권고한다. |
| `/Users/hammyeong-yeon/Desktop/10_work/personal-context/` | 도구와 분리된 별도 저장소를 운영할 때의 후보. 전역 색인의 주요 작업 위치 관례에 따른 새 경로 제안일 뿐 존재를 확인한 저장소가 아니다. 지금은 추가 저장소와 전역 발견 연결을 관리할 필요가 충분하지 않다. |

전역 [shared references의 현재 계약](/Users/hammyeong-yeon/.claude/references/README.md)은 기준 의미와 적용 시점을 구별한다. 이 구별은 개인 기준에도 참고할 수 있지만, 그 문서가 새 Personal 위치나 본문 전체 채택을 정해 준 것은 아니다. `/Users/hammyeong-yeon/.claude/personal-context/`가 현재 없음을 확인했으며 이번에 생성하지 않았다.

## Main·workflow·skill이 찾아 읽는 구체 연결

이번 추천의 최소 연결은 **공통 전역 지침의 발견 안내와 Main/workflow의 선택 행동**이다. 별도의 새 read skill부터 설치하는 안으로 정하지 않는다. 다음 내용은 채택한다면 반영할 연결이며 현재 동작을 묘사한 것이 아니다.

1. 공통 전역 지침에 개발 작업의 발견 조건과 Personal 개발 입구 경로를 짧게 둔다. Claude와 Codex는 이미 같은 공통 원천을 읽으므로 개인 본문을 두 도구에 복제할 필요가 없다. 전체 기준을 상시 지침에 넣지 않는다.
2. Main/workflow가 작업 주제에 필요한 개인 기준이 아직 없거나 질문이 달라졌을 때 개발 입구를 읽고 해당 상세를 선택한다. 이번 이름 작업에서는 공통과 `naming-and-completion.md`를 고른다. 이미 읽은 유효한 본문은 재사용한다.
3. 대상 Project는 별도로 로컬 진입 지침과 Project README에서 찾아 읽는다. 기존 [read-project-context](../../../../reference-project/.agents/skills/read-project-context/SKILL.md)는 대상의 제품·개발 계약을 고르는 책임을 유지한다. 이 skill에 개인 기준의 위치나 내용을 추가하지 않는다.
4. Main이 구현자·검토자에게 이번 Work의 목표, 선택한 개인 본문의 절대 경로와 선택 이유, 관련 Project 계약·코드·사용처를 전달한다. 새 실행 주체가 Main의 대화 내용을 이미 안다고 가정하지 않는다. 본문 접근에 실패하면 읽고 적용했다고 보고하거나 임의 사본으로 메우지 않는다.
5. 이번 판단·검사와 사용한 근거는 Work에, Project 의미·계약·현황 변화는 그 Project의 담당 문서에, 여러 Project에서도 유지할 개인 판단 변화는 Personal의 관리 책임에 돌린다. 개인 선호가 제품 계약·팀 합의·호환 요구를 자동으로 덮어쓰지 않는다.

공통 전역 지침에 들어갈 짧은 안내의 예시는 다음과 같다. 이 문구도 Main의 초안이다.

> 코드 구현·수정·리뷰에서 필요한 개인 개발 기준이 아직 선택되지 않았거나 작업의 판단 주제가 바뀌면 `/Users/hammyeong-yeon/.claude/personal-context/development/README.md`에서 관련 본문을 골라 읽는다. 대상 Project의 의미·계약은 별도로 확인하며 이미 확보한 유효한 내용은 재사용한다. 위임 시 선택한 본문 경로와 적용 이유를 함께 전달한다.

예를 들어 Noline 로그인 이름 작업에서는 이 경로에서 개인의 이름·완료 판단을 고르고, 대상 Project의 입구에서 인증 완료·Query 실패 계약을 고른다. Project는 Personal의 경로를 알 필요가 없다. 두 입력을 함께 받은 구현자·검토자가 이번 사용처와 대조하며, 선택 이유는 Work에 남긴다.

추후 개인 기준 선택 절차를 skill로 묶더라도 skill은 위 입구를 소비하고 본문은 Personal에 남기는 관계를 권고한다. skill 신설 여부·이름·세부 호출 계약은 이번에 결정하지 않았다. 현재 [workflow 시안](prototypes/personal-project-applied-2026-10-19/workflow.md)의 Main 책임을 실제 전역 발견 경로로 연결하는 추천이다. 실제 배치 때는 새 디렉터리의 관리·보존 및 기존 전역 snapshot 범위도 확인해야 하며 이번에는 전역 지침·색인·스킬·브릿지를 변경하지 않았다.

## ‘반영했다’는 말에서 구별해야 하는 것

**이미 선택한 방향과 앞서 보완한 판단 방식을 이어받았지만, 현재 Personal의 구체 문장·질문·사례·파일 배치와 workflow는 Main이 새로 작성한 시안이다.** 앞선 답변은 둘을 구별하지 않고 ‘반영했다’고만 설명해 완성된 결정안을 그대로 옮긴 것처럼 읽힐 여지를 만들었다.

| 내용 | 원자료의 지위 | 이번84에서 한 일 |
| --- | --- | --- |
| 일반 원칙과 판단 질문 | [57](2026-10-16-57-criteria-organization-and-guiding-questions.md)의 사용자 생각. 러프한 제안이며 고정 목차·질문 문장은 미정. | 그 의도를 바탕으로 지금 주제에 필요한 질문을 새로 썼다. |
| 의미·조건·질문·대비·선택적 읽기 | [61](2026-10-17-61-reference-comparison-for-format-design.md)의 외부 자료 비교와 Main 권고. 레퍼런스 전체 형식 채택 아님. | 본문을 작성·검토할 근거로 이용했다. 외부 자료의 완성 양식을 복사한 것이 아니다. |
| 원칙·사례의 구별과 과정·근거 재사용 | [66](2026-10-18-66-principles-cases-and-refinement-prototype.md)에서 사용자가 실제 시안 보완을 요청. | 이번에도 유지했다. 이 구별을84에서 처음 발명했다고 설명하지 않는다. |
| 목적·조건·비용에 따른 원칙 적용 | [68](2026-10-18-68-principle-application-and-choice-basis.md)에서 사용자가 세 보완의 반영을 요청. | 개명·유지·동작 수정이 각각 타당한 조건을 새 주제에서 비교했다. |
| 짧은 공통＋이름·가독성의 별도 절 | [72](2026-10-18-72-short-common-and-detail-prototype.md)의 명시적인 시안 반영 선택. 당시에는 같은 quality 파일 안의 독립 절이었다. | 관계는 계승했고 Personal에서 README와 상세 파일로 나눈 배치·파일명은 이번 Main 구체화다. |
| 전체 문서 형식의 수용 | [73](2026-10-18-73-prototype-reservations-and-ticket03.md)의 전체 만족·최종 수용 유보. | 유보를 유지한다.72의 반영 요청 자체를 철회한 것으로 읽지도 않는다. |

72의 직접 원문:

> 그럼 공통은 짧게 두고 이름·가독성은 별도 절로 두는 방향으로 기존 시안에도 반영해줘.

현재 상세의 ‘내부 함수 개명 / 공개 API 유지·설명 보완 / 파일 저장의 실제 동작 수정’이라는 세 사례와 표, 구체 질문 문장, 독립 Personal·Project를 묶는 workflow 문장, 가상 로그인 두 사용처·후보 이름은 이번에 Main이 구체화한 것이다. 관련 의미와 조건별 대비 방식은 [기존 quality](prototypes/applied-criteria-2026-10-17/shop-web/context/project/quality.md)에도 있었으므로 전부 이번에 처음 조합한 발상이라고 하지는 않는다. **근거가 있는 새 구체화와 이미 결정된 구성은 같은 지위가 아니다.**

## 이번 변경 범위

이 제안·근거 구별을 Workspace 기록과 현재 진입 안내에만 남긴다.84의 시안 본문·viewer, 과거 기록, 원자료, 실제 개인 기준 디렉터리, Project·전역 지침·스킬·브릿지는 변경하지 않는다. 위치 추천을 사용자 채택으로 올리지 않으며 관련 Ticket은 미완료다. 커밋하지 않는다.
