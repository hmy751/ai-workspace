# Improvement Loop의 배치·본문 형식 개선 리뷰

2026-10-28. 독립 개선 의견이며 prototype 수정·제안 채택·운영 시험 결과가 아니다. 검토 대상은 `records/prototypes/development-workflow/`의 실제 현재 파일이다. Main이 구조 가설이나 기대 결론을 제공하지 않은 상태에서 시작했다. 이전 리뷰 보고·종합은 이번 판단의 입력으로 읽지 않았다. 현재 Ticket에서 이전 제안이 미반영이라는 상태는 확인했으며, 그 제안의 채택 여부를 이 보고서가 판단하지 않는다.

## 추천

**`improvement-loop.md`는 prototype 루트에 남기되, ‘전체 구성과 사용 흐름을 설명하는 안내’로 역할을 정리하는 것이 가장 낫다.** 스킬 실행과 Personal의 경험 관리가 연결되는 모습을 보여 주므로 어느 한쪽 아래로 통째로 옮기는 것보다 현재 위치가 적합하다. 다만 현재의 제목·서술에는 실행 규칙, 설명 사례, 이번 작성 결과와 다음 작업이 섞여 있다. 위치를 유지하는 판단과 현행 내용을 그대로 유지하는 판단은 다르다.

우선 개선할 것은 다음 세 가지다.

1. 루트 안내를 **전체 관계·한 번의 사용 흐름·대표 선택·고칠 위치**로 구성하고, 이번 작성·점검·다음 작업 상태는 기존 Workspace 기록과 current가 맡게 한다. 루트와 `skills/README.md`의 임시 추가 문구도 정상적인 질문별 안내에 통합한다.
2. `references/conversation.md`와 `effects.md`는 현재 실행 상세로 유지한다. conversation의 환경별 사용 방법과 날짜가 붙은 확인 이력을 구별하고, 효과 문서는 판단이 달라지는 부분을 소제목으로 찾게 한다. 파일을 더 나누거나 `INDEX`로 일괄 개명할 이유는 없다.
3. **Personal의 독립성을 형성 근거에도 이어 준다.** Personal의 경계를 택한 사용자 발췌와 Work 정정은 Personal 가까이에서 보존하고, 루프 형성 자료가 그곳을 참조하게 한다. 지금은 계약은 독립했지만 그 계약을 재검토할 최소 근거가 스킬에 매달려 있다.

아래 제안은 루프의 호출·검토 범위·선택 권한·종료 조건을 바꾸지 않는다. 이를 바꾸는 안은 별도 실행 규칙 변경으로 다뤄야 한다.

## 현재 배치가 실제로 답하는 질문

이 보고서에서 P는 [development-workflow](../../prototypes/development-workflow/README.md), W는 Workspace014다.

| 독자와 질문 | 실제 진입·본문 | 지금 잘하는 일 / 남은 불편 |
| --- | --- | --- |
| prototype을 검토하는 사용자: ‘루프를 만들면 무엇이 연결되나?’ | P의 [improvement-loop.md](../../prototypes/development-workflow/improvement-loop.md) | 스킬·상세·Personal·반영 경로를 한곳에서 설명한다. 반면 ‘네 묶음’, ‘이번에는’, ‘다음에는’은 작성 대화의 시점에 기대고 있다. |
| 지금 루프를 수행하는 Main: ‘무엇을 보고 어떻게 판단·반영하나?’ | [SKILL.md](../../prototypes/development-workflow/skills/improvement-loop/SKILL.md) | 실질 실행 본문을 유지하며 조건부 상세로 연결한다. 전체 안내를 실행의 필수 선행 문서로 강제하지 않는다. |
| 압축된 대화를 확인하는 Main: ‘같은 세션 원문을 어떻게 찾고 공백을 처리하나?’ | [conversation.md](../../prototypes/development-workflow/skills/improvement-loop/references/conversation.md) | 공통 절차, 로컬 Codex 예, 복구 실패 처리를 담는다. 사용 방법과 이번 작성 환경에서 확인한 사실을 같은 절 안에서 읽게 된다. |
| 이전 반영을 살피는 Main: ‘안 쓴 것과 효과가 없는 것을 어떻게 구별하나?’ | [effects.md](../../prototypes/development-workflow/skills/improvement-loop/references/effects.md) | 상태별 판단 표가 실제 선택 차이를 보여 준다. 짧고 한 책임이라 추가 분할 이득은 작다. |
| 다음 루프에서 경험을 찾는 사람/AI: ‘관련 경험과 열린 질문은 어디 있나?’ | [경험 길잡이](../../prototypes/development-workflow/noline-demo/context/personal/experience/README.md), 주제별 본문 | 현재 이해·후보·근거의 연결을 유지한다. 날짜별 사건함과 후보함을 나눠 재조립하게 하지 않는다. |
| 경험을 갱신하는 담당자: ‘무엇을 보존하고 채택 후 어떻게 잇나?’ | [MAINTENANCE.md](../../prototypes/development-workflow/noline-demo/context/personal/experience/MAINTENANCE.md) | 관리 계약이 스킬 밖에 있어 경험의 지위를 유지할 수 있다. |
| 루프를 고치는 담당자: ‘왜 지금의 범위와 수단을 택했나?’ | [루프 _background](../../prototypes/development-workflow/skills/improvement-loop/_background/README.md) | 맥락·기록·근거의 역할과 읽을 질문이 구별된다. 외부 자료의 묶음 설명은 개별 원문 재접근과 적용 차이를 더 좁혀 줄 수 있다. |
| Personal 경계를 고치는 담당자: ‘왜 기준 외 경험도 Personal에 두었나?’ | [Personal 형성 자료](../../prototypes/development-workflow/noline-demo/context/personal/_background/experience-collection/README.md) | 이유는 가까이 설명하지만 직접 사용자 발화는 루프 스킬의 evidence로 나간다. |

`records/prototypes/` 아래라는 점 자체는 현재 산출물의 위치 오류가 아니다. W의 README는 실물을 이 한 폴더에서 계속 발전시키고 바깥 설계 기록과 구별한다고 명시한다. 이번 파일 하나를 W의 `output/`이나 루트 `reference-project/`로 옮기면 전체 prototype의 관리·선택 경계를 바꾸게 된다. 그런 변경을 요구하는 근거는 이번 범위에서 찾지 못했다.

## 위치 대안 비교

| 대안 | 이득 | 비용·잃는 것 | 판단 |
| --- | --- | --- | --- |
| 현 위치·현 내용 그대로 | 이동과 연결 수정이 없다. | 전체 안내와 작성 상태가 계속 섞이고 실행 본문과 설명 본문의 역할을 독자가 추론한다. | 그대로 유지는 비추천. |
| **현 위치에서 지속 안내로 재구성** | 스킬·Personal·대상 반영 관계를 한 번에 읽고 각 정본으로 내려간다. 기존 `walkthrough.md`와 같은 prototype 해설 역할을 유지한다. | 안내와 실행 본문이 달라지지 않도록 같은 의미인지 확인해야 한다. | **추천.** 파일 이동보다 본문 역할·갱신 경계를 먼저 고친다. |
| 전부 `skills/improvement-loop/references/overview.md`로 이동 | 스킬 폴더만 보아도 설명을 찾는다. | Personal의 독립 저장·관리까지 스킬 부속 자료처럼 보인다. 운영 설치 때 prototype 해설까지 필요한 실행 의존으로 포장할 위험도 있다. | 스킬 실행만 설명하는 문서라면 가능하나 현재 내용에는 부적합. |
| 전부 W의 날짜별 설계 기록으로 이동 | 작성 당시 결과·미확인 보존에 맞다. | prototype 독자가 바깥 설계 기록 없이 전체 관계를 이해하기 어렵다. viewer의 바깥 로컬 문서 비의존 조건에도 맞지 않는다. | 작성·점검 경과에만 적합. |
| P에 `improvement-loop/README.md`, `INDEX.md`, 사례·배경 폴더 신설 | 여러 독립 안내가 늘면 묶음 관리가 가능하다. | 지금은 한 해설과 이미 있는 스킬·Personal을 위한 세 번째 관리 단위를 만들게 된다. | 지금은 비용이 더 크다. |

파일명은 `improvement-loop.md`를 유지해도 된다. 제목을 **‘개선 루프의 구성과 사용 흐름’**으로 바꾸고 첫 문장에서 설명 역할을 밝히면 스킬 본문과 구별된다. `IMPROVEMENT-LOOP.md`나 `INDEX.md`로 바꾼다고 책임이 명료해지지는 않는다. `SYSTEM-GUIDANCE`의 대문자 표기는 체계 지침의 대표 진입에 관한 기본 표기이며, 모든 해설·상세의 일괄 개명 규칙이 아니다.

## 추천 트리와 현재 내용의 도착점

새 전체 체계를 만들지 않고 아래처럼 역할을 정리한다. `evidence.md` 한 파일의 추가는 파일 수를 맞추기 위한 것이 아니라 Personal의 근거 소유를 스킬과 분리하기 위한 선택이다.

```text
development-workflow/
├── README.md                         전체 prototype의 질문별 진입
├── improvement-loop.md               전체 연결·대표 흐름·수정 위치 해설
├── walkthrough.md                    기존 로그인 작업 해설 유지
├── skills/
│   ├── README.md                     루프를 다른 스킬과 같은 목록에서 안내
│   └── improvement-loop/
│       ├── SKILL.md                  호출·핵심 판단·행동·종료
│       ├── references/
│       │   ├── conversation.md       대화 입력과 환경별 접근 상세
│       │   └── effects.md            이전 변경의 사용·도움·부담 판단
│       └── _background/
│           ├── README.md             질문별 형성 자료 진입
│           ├── context.md            루프의 현재 선택 이유
│           ├── evidence.md           루프 관련 합의·외부 관점의 최소 근거
│           └── records/              기존 작성·개명 기록 유지
└── noline-demo/context/personal/
    ├── README.md                     Personal의 상위 경계 유지
    ├── experience/
    │   ├── README.md                 주제·미분류 질문의 길잡이
    │   ├── MAINTENANCE.md            모음의 저장·갱신 계약
    │   └── topics/*.md               경험·해석·후보·후속 판단 유지
    └── _background/experience-collection/
        ├── README.md
        ├── context.md
        └── evidence.md               Personal 경계·Work 정정의 최소 원문
```

| 현재 파일·절 | 추천 도착점과 편집 |
| --- | --- |
| 루트 `improvement-loop.md` 서두·파일 책임 표 | 같은 파일에 유지. ‘네 묶음’ 대신 실제 구성 관계로 설명하고, 표를 읽을 질문과 담당 본문을 연결하는 안내로 다듬는다. |
| `실제 한 번의 흐름` | 같은 파일에 유지하되 ‘한 번의 사용을 따라가면’으로 제목을 바꾼다. 현재 표는 운영 실행 이력이 아니라 수행 설명이므로 그 지위를 첫 문장에 밝힌다. |
| 세 대표 사례 | 같은 파일에 유지. 역사적 경험의 상세를 반복하기보다 **이 조건에서 어떤 선택이 갈리고 어디가 바뀌는지**를 보여 준다. 원문·실제 과거 결과는 Personal 주제 본문을 참조한다. |
| `입력·권한·정본의 경계` | Main·Personal·실제 반영 대상의 관계를 설명하는 부분은 파일 책임 표 가까이에 통합한다. 원문 확보 실패의 실행 상세는 conversation으로, 검사·종료의 자세한 조건은 SKILL로 연결한다. 핵심 권한 차이는 해설에서도 바로 이해할 만큼 남긴다. |
| `무엇이 만들어졌고 무엇이 남았나`의 이번 작성·점검·다음 행동 | 이미 이를 소유한 W의 `2026-10-28-ticket05-execution-prototype.md`와 current Ticket/state에서 관리한다. 기존 기록과 대조해 없는 중요한 사실만 보완하며 본문 전체를 다시 복사하지 않는다. |
| 위 절의 prototype 한계·운영 미확인 | 해설 끝의 짧은 `확인 범위`에 유지한다. 루프 사용법의 필수 이해가 바깥 W 기록에 의존하지 않게 한다. |
| 루프 evidence의 `Personal과 Work` | 최소 직접 발화와 실제 Work 정정 발췌를 Personal의 새 evidence에 모으고 루프 evidence는 해당 절을 참조한다. 긴 인터뷰 전체와 과거 snapshot은 원래 위치에 유지한다. |
| conversation의 로컬 Codex 절 | 실행에 필요한 식별·메시지 선택·압축 구별은 현재 상세에 유지. ‘작성 당시 무엇까지만 확인했는가’는 기존 루프 `_background/evidence.md`의 `로컬 원문 접근 확인` 절로 모으고 짧은 확인판 안내로 연결한다. 과거 작성 기록은 그대로 유지한다. |

P 내부에서 W 바깥 기록으로 향하는 새 로컬 링크를 만들자는 제안은 아니다. [viewer 안내](../../prototypes/development-workflow/viewer/README.md)는 prototype 밖 로컬 문서 의존을 허용하지 않는다. 날짜별 전체 기록은 W에서 재접근하고, prototype에는 현재 설명·필요한 최소 발췌·확인 한계가 남아야 한다.

## 본문과 references의 형식 개선

### 전체 안내는 무엇을 고칠지까지 보여 준다

현행 책임 표는 이미 유용하다. 표를 없애거나 별도 INDEX를 만드는 대신 마지막 열을 수정 질문에 쓰면 다음 지시가 구체화된다.

대표 수정안:

> # 개선 루프의 구성과 사용 흐름
>
> 이 안내는 사용자 요청으로 시작한 개선 검토가 실행 스킬, Personal 경험 모음, 실제 반영 대상으로 어떻게 이어지는지 설명한다. 지금 루프를 수행할 때는 `skills/improvement-loop/SKILL.md`를 읽고, 아래에서는 전체 관계와 대표 선택을 살핀다.
>
> Main은 대화와 관련 내용을 살펴 선택지를 만들고, 사용자가 고른 개선을 대상의 기존 계약에 따라 반영한다. Personal은 다시 볼 경험과 판단을 보존하며, 채택된 규칙·제품 내용은 실제 반영 대상이 소유한다.

| 고치려는 것 | 담당 본문 |
| --- | --- |
| 언제 루프를 시작하고 어떤 근거로 선택·종료할지 | `skills/improvement-loop/SKILL.md` |
| 요약·압축·원문 공백을 어떻게 다룰지 | `references/conversation.md` |
| 실제 사용과 효과를 어떻게 구별할지 | `references/effects.md` |
| 경험·후보를 어디에 어떻게 보존하고 찾을지 | Personal의 `experience/MAINTENANCE.md` |
| 이번 prototype에서 무엇을 확인했는지 | 해설의 확인 범위와 W의 작성·검토 기록 |

실제 편집에서는 위 경로를 해당 파일 링크로 연결한다. 설명 문서에 실행 규칙의 제2 정본을 만들지 않고, 수정하려는 질문에서 담당 본문으로 바로 갈 수 있게 한다.

P의 README 첫머리와 `skills/README.md` 첫머리에는 루프가 최근 추가된 공지처럼 따로 얹혀 있다. 특히 `skills/README.md`는 그 다음 문장에서 ‘현재 실행 본문은 development, work-discussion, explain, context-update, create-context-workspace’라고 열거해 루프를 빠뜨린다. **루프를 정상적인 질문별 표의 한 행으로 통합하고 수동 전체 열거 문장을 제거하거나 일치시키는 편이 좋다.** 이는 링크 검사를 통과해도 남는 발견성·유지 비용 문제다.

### 사례는 원자료 요약보다 선택의 차이를 보여 준다

현재 세 사례는 실경험과 가정을 구별한다는 장점이 있다. 다만 첫 사례는 경험 설명→다음 루프→추천→선택 분기를 긴 연속 문단으로 읽게 된다. 경험 설명을 짧게 두고 분기가 갈리는 지점을 표나 짧은 문단으로 드러내면 실제 선택을 비교하기 쉽다.

예를 들어 첫 사례를 다음 관계로 고친다. 아래는 추가 실행 단계가 아니라 현행 선택지를 재배열한 설명이다.

| 지금 확인한 조건 | 가능한 선택 | 실제로 달라지는 곳 |
| --- | --- | --- |
| 기존 work-discussion이 필요한 비교·질문을 이미 설명하며 이번에도 충분함 | 현재 방식 유지, 필요하면 경험만 보존 | Personal의 해당 경험·해석 |
| 특정 열린 설계에서는 유망하지만 일반 적용 근거가 부족함 | 사용자 선택에 따른 한정 시도 | 선택된 실제 작업의 행동과 Personal의 시도 범위·기대 변화 |
| 기존 스킬의 적용 조건에 구체적인 부족이 확인됨 | 사용자 선택에 따른 본문 보완 | 해당 스킬과 필요한 연결·직접 확인, Personal의 반영 결과 |

표만으로 끝내지 않고 왜 이 조건들이 다른 선택을 낳는지 짧게 설명한다. 기존 사례의 ‘한정 시도는 일반 채택이 아님’, ‘기존 본문 전체 대조’, ‘새 조건 없는 재권고 금지’는 가까이 유지한다. 모든 후보에 이 표를 채우는 출력 양식으로 만들지 않는다.

### conversation은 실행 조건과 확인 이력을 분리해 읽히게 한다

현재 번호 목록은 세션 식별→누락 원문 접근→순서대로 읽기라는 의존이 있으므로 적합하다. references 아래에 있다는 이유로 건조한 사실 목록으로 바꿀 필요는 없다. 이 파일은 **현재 실행 절차**다.

로컬 Codex 절의 대표 수정안:

> ## 로컬 Codex의 세션 파일을 사용하는 경우
>
> 현재 host가 `CODEX_THREAD_ID`와 로컬 세션 파일을 제공하면, 식별자가 일치하는 파일을 찾고 `session_meta`의 세션 ID와 작업 경로를 대조한다. 이름이나 수정 시각만으로 대상을 결정하지 않는다.
>
> 사용자·AI 메시지는 원본 순서와 줄 위치를 유지해 읽는다. 같은 발화가 `event_msg`에도 있으면 중복해서 세지 않는다. 압축된 replacement history는 요약일 수 있으므로 압축 전 메시지가 남아 있는지 확인한다.
>
> 확인판: 2026-10-28 로컬 환경에서 파일 식별과 메시지 필드만 확인했다. 전체 원문 완전성은 확인하지 않았다. 당시 확인 범위는 형성 근거의 ‘로컬 원문 접근 확인’에서 읽는다.

원래의 `response_item`, `payload.type`, `role`, `content` 필드 설명과 fork·재개·주입된 설정의 구별은 삭제하지 않고 이 문단 아래에 남긴다. **이 정리에는 새 파일이 필요 없다.** 기존 루프 evidence에 확인일·확인한 범위·확인하지 않은 범위와 원기록 식별자를 한 절로 추가하고, conversation은 짧은 확인판 한계와 링크를 유지한다. 코드나 추출기를 새로 만드는 제안도 아니다. 환경별 상세가 더 생기고 갱신 이유가 독립할 때만 `conversation/` 같은 분할을 다시 고려한다.

### effects는 현재 크기를 유지하고 판단 단위를 드러낸다

도입의 적용 조건과 여섯 행의 상태 구분은 유지한다. 표 뒤의 내용에는 `자료로 판단할 수 없는 부분`, `비교가 선택을 바꿀 때`, `원래 경험과 실제 대상에 결과를 잇기` 같은 소제목을 필요한 만큼 붙일 수 있다. 새로운 파일이나 번호 단계는 필요 없다.

대표 수정안:

> ## 비교가 선택을 바꿀 때
>
> 지금 자료만으로 유지·수정·철회 중 무엇을 택할지 갈리지 않고, 한정 비교가 그 선택을 바꿀 수 있다면 비교를 제안한다. 관련 대표 요청에서 대안의 조건과 결과를 대조하고 비용에 맞는지 판단한다. 비교가 결정적이지 않으면 불확실성을 남긴다.

이 문장 재구성은 현재 의무를 확대하지 않는다. 매 변경 비교·긴 대화 전체 재실행을 기본으로 삼지 않는 기존 조건도 같은 절에 유지한다.

SKILL 첫 절 역시 대화 범위, Personal·대상 본문 탐색, 후보 제시로 넘어갈 조건을 소제목으로 찾게 할 수 있다. 핵심 실행을 여러 새 reference로 흩뜨릴 정도의 독립 책임 차이는 아직 없다.

## 외부 레퍼런스와 형성 자료를 어떻게 다듬을까

이번에는 `references/`라는 폴더 형식과 외부 원형 두 의미를 함께 확인했다.

현재 [SKILLS-CONTENT-POLICY](../../prototypes/development-workflow/skills/SKILLS-CONTENT-POLICY.md)는 references에 조건별 절차·현재 사용하는 사례·자료 계약을 둘 수 있다고 명시한다. 따라서 conversation·effects의 명령문·표·설명 문단은 역할에 맞다. context의 일반 본문 `INDEX.*` 관례를 스킬 상세까지 복제하면 현재 계약을 혼동한다. `Project/REFERENCE`도 Project 관리 상세를 맡는 별도 책임이므로 폴더 이름을 맞출 필요가 없다.

외부 보존판을 보면 [pstack technical-writing](../../../source/workflow-references/pstack/repository/skills/technical-writing/SKILL.md)은 독자가 하려는 일을 먼저 정하고 설명·방법·조회 자료를 구별한다. 이 관점은 이번 역할 정리에 유용하다. 그러나 원형의 ‘문서 하나에 한 모드’, 영어 단어 수·문장 규칙을 이번 한국어 문서의 강제 서식으로 가져올 이유는 없다. 로컬 SYSTEM-GUIDANCE는 한 파일이 여러 역할을 함께 맡을 수도 있고 실제 읽기·수정 필요로 분리하라고 설명한다.

[pstack reflect](../../../source/workflow-references/pstack/repository/skills/reflect/SKILL.md)의 references는 세 리뷰어와 합성자의 프롬프트다. 우리 루프는 Main 중심이고 references는 원문 입력·효과 판단 상세다. 같은 이름의 디렉터리가 원형과 동일 파일 수나 역할을 요구하지 않는다. [Matt chief-of-staff](../../../source/workflow-reference-supplements/2026-10-27-learning-perspectives/repository/skills/skills/in-progress/chief-of-staff/SKILL.md)의 짧은 색인·주제별 페이지·관련 페이지 갱신 관점은 Personal 구성과 연결되지만, 원형은 날짜를 붙인 역사 wiki이고 현재 Personal은 현재 해석·후보도 관리한다. 원형의 모든 작업 위임·주기 점검·원문 비복사 지시는 이번 합의의 일부가 아니다.

현재 루프 `_background/evidence.md`의 외부 자료 표는 ‘가져온 관점/가져오지 않은 절차’를 밝힌 점이 좋다. 더 나은 수정 경로를 위해서는 여러 자료를 한 행으로 묶은 곳에서 **어느 원형의 어느 내용이 현재 어느 선택을 설명하는지**를 조금 더 직접 연결하는 편이 좋다. 새로운 서지 DB나 원형 전체 복사는 필요 없다.

대표 보완 예:

> **technical-writing — 독자의 질문에 맞춰 문서를 구성한다.** 보존판의 `Pick the mode first` 절은 작업 방법·조회 사실·선택 이유의 독자 요구를 구별한다. 여기서는 실행 본문, 조건별 상세, 형성 자료의 읽는 목적을 구별하는 데 이 관점을 사용했다. 문서 전체를 반드시 단일 모드로 분할하는 규칙과 영어 문장 길이 제한은 채택하지 않았다. 원형 확인 위치와 보존판 식별자는 함께 남긴다.

위 보완은 이번 리뷰에서 실제 확인한 원형과 기존 조사 기록의 관계를 드러내는 예다. 과거 작성자가 직접 원문을 읽었다고 소급해서 쓰지 않는다. 나머지 외부 자료도 실제 형성에 사용한 범위와 보존 조사에 의존한 범위를 구별한다. P 밖 원자료의 경로를 클릭 필수 의존으로 만들기보다, 필요한 최소 설명·발췌와 정확한 원형/절/판본 식별자를 가까이 남기고 상세 재조사는 W source에서 수행한다.

Personal의 근거 배치는 한 단계 더 고치는 편이 좋다. [경험 관리](../../prototypes/development-workflow/noline-demo/context/personal/experience/MAINTENANCE.md)는 ‘해당 스킬이 없어져도 이 모음과 읽기·갱신 관계는 유지한다’고 한다. 현재 관리 본문과 경험 자체는 이 조건을 만족한다. 다만 [Personal 형성 자료 README](../../prototypes/development-workflow/noline-demo/context/personal/_background/experience-collection/README.md)는 사용자 원문을 루프의 evidence 한 곳으로 연결한다. 스킬을 제거해도 경험 사용은 가능하지만 **Personal의 중요한 경계 선택을 재검토하는 길이 약해진다.** 실제 운영 파손을 재현했다는 뜻은 아니다.

따라서 Personal 경계·Work 정정의 최소 발췌는 Personal evidence가 소유하고, 루프의 context/evidence는 그 선택을 사용한 관계를 설명한다. 루프 실행 시점·선택·효과 판단의 근거는 계속 루프에 남긴다. 같은 인터뷰를 근거로 했다는 이유로 전부 ‘공통 근거’ 폴더로 올리거나 전체 발췌를 두 번 복사하지 않는다.

여기에는 Personal의 `evidence.md` **한 파일을 추가하는 안**을 추천한다. 기존 context에 발췌까지 합치면 파일은 늘지 않지만, 이미 구별한 현재 이유 설명과 원문 근거의 역할이 다시 섞인다. 새 파일은 ‘Personal 범위 확대’와 ‘Work 등록을 강제하지 않는 정정’의 두 근거와 출처·수용 범위만 담으면 된다. 네 묶음 합의 전체, 외부 자료 표, 날짜별 records 묶음은 만들 필요 없다. 현행 Personal README의 루프 evidence 링크를 자기 evidence로 바꾸고, 루프 evidence의 해당 절은 짧은 적용 관계와 Personal 근거 링크로 바꾸는 것이 최소 이동이다. 스킬을 제거해도 Personal의 두 중요한 선택 이유를 직접 재검토할 수 있다는 이득이 이 한 파일의 유지 비용을 정당화한다.

## 유지할 구조, 비용과 확인 한계

유지할 것은 명확하다. SKILL의 실질 본문, 두 조건부 reference, Personal의 README·MAINTENANCE·주제 상세, 루프의 `_background` 구분은 현재 목적에 맞는다. 아직 묶지 않은 짧은 질문을 길잡이에 두는 것도 합의된 저비용 선택이다. 세 경험 주제마다 README·INDEX·evidence·records를 기계적으로 추가하지 않는다. 지금의 좋은 경험·열린 후보를 전부 작업 티켓으로 바꾸지 않는다.

추천안의 주된 비용은 안내·실행·근거 사이의 재서술을 대조하고 들어오는 참조를 맞추는 것이다. Personal evidence 이동은 기존 인용의 출처와 당시 조건을 유지해야 한다. 현행 `_background/records`와 고정 리뷰 입력은 과거 판본이므로 새 결론에 맞춰 다시 쓰지 않는다. 기록 안의 원래 `learning-loop` 명칭도 역사적 설명이라는 이유로 존재할 수 있다.

수정 후 확인은 파일 존재 검사에 그치지 않아야 한다. 다음 질문에서 실제로 출발해 답과 수정 대상을 찾는다.

- prototype만 받은 사람이 ‘전체 관계가 무엇인가’와 ‘지금 수행할 본문은 무엇인가’를 구별한다.
- 압축 구간이 있는 Main이 원문 접근 방법과 확인 한계를 찾고, 조사 이력을 실행 보장으로 읽지 않는다.
- 이전 보완의 효과가 모호할 때 effects에서 다른 선택이 갈리는 조건을 찾는다.
- Personal의 경계 수정자가 루프 스킬 없이도 이유와 최소 근거를 복원한다. 이는 삭제 실행이 아니라 링크 의존을 제외해 읽어 보는 확인으로 충분하다.
- 작성 진행 상태를 확인하려는 사람이 W의 current·기록을 읽고, prototype 해설의 ‘다음에는’를 현재 지시로 해석하지 않는다.

채택·편집 후에는 기존 viewer 생성·검사와 영향을 받은 현재 링크·앵커·표시 사본을 확인하면 된다. 이 문서 리뷰만을 위해 제품 코드 테스트나 새 실행 도구를 만들 필요는 없다. 문장만 재배열했다는 판단과 실행 의미 보존 여부는 별도로 대조한다.

이번 확인은 원문을 읽고 역할·대안·읽기 경로를 비교한 정적 개선 리뷰다. 새 모델의 실제 루프 수행, host 설치·세션 원문 완전성, 브라우저 사용감, 장기 경험 누적의 검색 비용은 시험하지 않았다. 이동안의 실제 편집 부담도 아직 측정하지 않았다. 따라서 추천안은 읽기·관리 책임의 근거 있는 개선 선택이지 수행 성공률이나 효과 향상의 증명은 아니다.

적용 기준은 root AGENTS·CODE-QUALITY, P의 SKILLS-CONTENT-POLICY, demo CONTENT-POLICY·SYSTEM-GUIDANCE, 전역의 사람용 진입·지침 명확성·컨텍스트 소유·하네스 제거 가능성 기준이다. context 정책은 지정된 Personal·Project·공통 본문에, 스킬 정책은 skills에 적용했다. W의 Work 전체나 모든 루트 안내를 동일한 README/INDEX/_background 형태로 바꿀 의무로 확대하지 않았다.
