# 개인 기준·Project 문서·이를 함께 쓰는 작업 흐름

**Personal과 Project는 각각 자기 내용을 소유하고, 이번 작업에서 둘을 선택·대조하는 책임은 별도 workflow가 맡는다.** 실제 문서를 나란히 읽고, 한 작업에서 어떻게 사용하는지 검토하는 시안이다. 제품 코드·작업 진행은 가상이며 실제 Noline 실행 결과가 아니다.

[열람 화면](viewer.html)에서 세 책임을 나란히 볼 수 있다. 본문 정본은 아래 Markdown이고 화면은 그 표시 사본이다. [작업 장면](walkthrough.md)은 입력 선택부터 대안 비교·변경·검토·기록까지 보여 준다.

**현재 보완87:** [개발 공통](personal-context/development/README.md)에 채택 뒤에도 목적·사용처·비용으로 적용하는 설명을 복원하고, [이름 상세](personal-context/development/naming-and-completion.md#원래-대화와-사례를-다시-읽을-때)에 원래 대화·사례를 선택해 읽는 경로를 붙였다. 사용자 동의·조건부 선호·사례 판단과 Main의 새 문장·질문·예시는 [Personal 입구](personal-context/README.md#이-시안에서-선택한-것과-검토할-것) 및 해당 본문에서 구별한다. [보완 기록87](../../2026-10-19-87-conditional-application-and-provenance.md)은 이번 요청·변경·확인 범위를 남긴다. 기존 [일곱 쌍 비교](../criteria-format-comparison-2026-10-19/README.md)는 이 보완 전 문장을 보존한 자료다.

## 실제 구조와 시안의 배치를 구별한다

실제 ai-workspace는 개발 workflow와 기준 Project를 만드는 작업대다. 현행 [context 계약](../../../../../README.md)은 Workspace와 source를 소유하고, 별도 산출물인 [reference-project의 context](../../../../../../reference-project/context/README.md)는 Project와 Work를 소유한다. 사용자는 이후 개인 기준을 작업대의 `context/personal/`에 두기로 선택했다. 이는 현행 context 책임을 확장할 방향이며 실제 폴더 생성·이동·root 계약 변경은 아직 하지 않았다.

[기록81](../../2026-10-19-81-personal-context-direction-and-next-step.md)의 위치 전제와 Project 참조 책임은 [84](../../2026-10-19-84-personal-project-ownership-and-format-correction.md)에서 재검토했다. 이후 [85](../../2026-10-19-85-personal-location-proposal-and-format-provenance.md)의 글로벌 위치 추천을 사용자가 대체하고, [86](../../2026-10-19-86-context-personal-choice-and-text-comparison.md)에서 **ai-workspace의 `context/personal/`**을 선택했다. 같은 물리 경로를 선택했다고 해서 Project의 개인 기준 직접 참조·관리 책임까지 복원하는 것은 아니다.

아래는 비교용 산출물 내부의 배치다. `personal-context/` 파일들은 이 시안에 그대로 두고, 향후 운영 위치는 `ai-workspace/context/personal/`, 개발 주제는 그 아래 `development/`에 두는 방향으로 정했다. 위치 선택은 현재 본문·파일 구성 전체의 채택이나 실제 설치와 구별한다.

```text
이 시안/
├── personal-context/                개인 판단과 이유·조건
│   ├── README.md
│   └── development/
│       ├── README.md                짧은 공통 기준과 상세 진입
│       └── naming-and-completion.md
├── noline-demo/                     대상 Project의 예시
│   ├── AGENTS.md
│   └── context/
│       ├── README.md
│       ├── project/
│       │   ├── README.md
│       │   ├── common/device-session.md
│       │   ├── guidance/authentication-and-session.md
│       │   ├── guidance/code-readability.md
│       │   └── current/authentication-flow.md
│       └── work/workspaces/login-completion-names/
│           ├── README.md
│           ├── current/{ticket,state}.md
│           └── records/{implementation,review}.md
├── workflow.md                      Main의 선택·대조·전달·갱신 절차
├── scenario-input.md                작업 전 코드와 사용처 가정
└── walkthrough.md                   그 절차를 적용한 한 장면
```

## 각각 무엇을 책임지는가

| 책임 | 실제 본문 | 이 문서가 결정하는 것 |
| --- | --- | --- |
| 개인의 공통 판단 | [짧은 공통](personal-context/development/README.md), [이름·책임·완료 범위](personal-context/development/naming-and-completion.md) | 왜 이름과 실제 보장을 맞추는지, 언제 이름·설명·동작 중 무엇을 고칠지. 특정 Project를 찾거나 채택 목록을 관리하지 않는다. |
| Project의 지속 계약 | [인증 코드의 가독성 기준](noline-demo/context/project/guidance/code-readability.md), [인증·세션 계약](noline-demo/context/project/guidance/authentication-and-session.md) | 이 제품의 저장·상태 적용·조회 갱신이 뜻하는 결과와 표현 기준. 개인 본문을 찾아가지 않아도 자기 계약을 이해할 수 있게 설명한다. |
| 작업에서의 연결 | [workflow](workflow.md) | Main이 언제 어떤 개인 주제와 Project 내용을 고르고, 충돌을 판단하며, 구현·검토 입력과 갱신 위치를 정하는지. |
| 이번 작업의 요구와 결과 | [Work](noline-demo/context/work/workspaces/login-completion-names/README.md) | 이번에 바꿀 범위, 선택한 대안과 근거, 수정·검토·미확인. 일반 기준이나 제품 계약으로 자동 승격하지 않는다. |

Personal과 Project 사이에 직접 의존 링크를 두지 않았다. Project 입구는 자기 담당 본문을 찾게 하고, Personal 입구도 개인 기준 안에서만 주제를 안내한다. 이번 Work의 입력 선택 기록에는 실제로 사용한 두 출처가 남는다. 이것은 Project의 상시 문서가 개인 기준을 관리하는 것과 다른 책임이다.

workflow는 현재 Main이 수행할 절차를 문장으로 구체화한 시안이다. 이를 어느 skill이나 실행 장치에 맡길지, 선택한 `context/personal/`에 대한 접근·버전·갱신 전달을 어떻게 관리할지는 남아 있다. 설치나 자동 실행은 수행하지 않았다.

## 01의 문서 형식 논의를 어떻게 이어받았는가

01에서는 고정 목차를 정하기보다 일반 기준의 뜻을 이해하고, 조건을 대조해 선택하며, 필요한 내용만 찾을 수 있는 형식을 고민했다. [72](../../2026-10-18-72-short-common-and-detail-prototype.md)에서 **짧은 공통＋이름·가독성의 별도 상세**를 시안에 반영하기로 했고, [73](../../2026-10-18-73-prototype-reservations-and-ticket03.md)에서 전체 수용은 유보했다.

이번에는 짧은 공통을 개발 판단 입구에, 이름·완료의 의미와 적용 조건을 상세 본문에 두었다. 상세 본문에서 질문은 실제 코드·호출자가 제공할 근거와 연결한다. 내부 호출부는 개명하는 경우, 공개 API는 이름과 계약 설명을 유지·보완하는 경우, 약속을 못 지킨 구현을 고치는 경우를 대비한다. 모든 기준을 같은 표나 질문 양식으로 만들지는 않는다.

Project 가이드에는 이번에 선택할 함수명을 미리 주지 않는다. 작업 장면에서 이름 유지＋설명 보완, 개명＋설명 보완, 대기 동작 변경을 비교한다. Project 계약이 완료의 의미를 정하는 역할과 개인 기준이 표현 수단·변경 비용을 판단하게 하는 역할을 구별한다. 이 구성만으로 개인 기준의 실제 효과가 입증되지는 않는다.

| 다시 검토하려는 질문 | 과정 근거와 읽는 이유 |
| --- | --- |
| 사용자가 어떤 형식을 원했는가 | [57 사용자 생각](../../2026-10-16-57-criteria-organization-and-guiding-questions.md). 일반 원칙·고민 기준·질문이라는 러프한 제안과 고정 양식의 채택을 구별할 때 읽는다. |
| 레퍼런스에서 무엇을 가져왔고 무엇을 보류했는가 | [61 비교](../../2026-10-17-61-reference-comparison-for-format-design.md). Matt의 개념·질문·대비, Vercel의 범위·이유·예외·근거, pstack의 관찰·유지 조건, Anthropic의 구체성·선택적 읽기를 참고한 이유와 비용을 확인한다. 외부 저자의 설계 철학·파일 구성 전체를 채택한 기록은 아니다. |
| 이름과 가독성을 왜 별도 상세로 두었는가 | [45 이름·가독성 보완](../../2026-10-16-45-naming-readability-supplement.md), [72 시안 반영](../../2026-10-18-72-short-common-and-detail-prototype.md). 실제 책임을 읽을 수 있게 하려는 의도와 본문 구성 선택을 다시 판단할 때 읽는다. |
| 왜 정답 하나와 결과만 보여 주면 부족한가 | [64 적용 시안 검토](../../2026-10-17-64-applied-format-improvement-review.md), [65 과정 재사용](../../2026-10-18-65-criteria-status-and-cross-ticket-refinement.md), [68 선택 근거](../../2026-10-18-68-principle-application-and-choice-basis.md). Project 계약이 답을 미리 주는 장면의 한계, 조건에 따라 다른 대안이 타당해지는 이유를 확인한다. |

이 표는 본문 형식의 근거를 재검토할 때 쓰는 경로다. 일반 작업마다 이 기록 전체를 읽게 하는 절차는 아니다.

## 원자료와 추가 가정의 범위

| 구분 | 이 시안에서 쓰는 내용 |
| --- | --- |
| Noline 보존 문서가 지지하는 계약 | 계정·DB·queue 확인, 기기 저장 뒤 상태 공개. 저장·상태 적용 이후 Query 갱신 실패를 인증 저장 실패로 재분류하지 않음. Store의 부분 책임과 전체 세션 변경 조율의 구별. |
| 장면에 추가한 가정 | 내부 사용처는 LoginScreen과 ReauthDialog 두 곳. 전체 서비스는 조율·검사·저장·적용 뒤 끝남. wrapper는 Query 갱신을 요청하고 재조회를 기다리지 않고 callback을 부름. 후속 실패는 별도 callback이 받음. |
| 설명용 변경 | 작업자가 대안을 비교해 함수·callback 이름을 선택하고, 검토자가 남은 ‘화면 갱신 완료’ 메시지를 바로잡는 장면. |
| 실제로 하지 않은 일 | 제품 코드·테스트 실행, 실제 로그인·화면 조작, 기준 설치·기존 가이드 이동/통합·새 운영 규칙 채택. |

계약 근거는 [기존 인증 가이드](../../../source/supplement/worktree-project-context/context/project/guidance/authentication-and-session.md), [가독성 가이드](../../../source/supplement/worktree-project-context/context/project/guidance/code-readability.md), [세션 현황](../../../source/supplement/worktree-project-context/context/project/current/session-and-local-data.md)다. 실제 Noline 로그인 경로의 Query 대기 여부는 확인하지 않았다. 작업 시작 전 함수·사용처는 [시작 입력](scenario-input.md), 작업 후 연결은 [Project 현황](noline-demo/context/project/current/authentication-flow.md)으로 구별한다.

앞선 [세 본문 시안82](../personal-project-naming-2026-10-19/README.md)와 [처음 적용 시안의 기록83](../../2026-10-19-83-personal-project-applied-example.md)은 당시 판단을 남기는 자료다. 책임·형식 수정은 [84](../../2026-10-19-84-personal-project-ownership-and-format-correction.md), 최신 위치 선택은 [86](../../2026-10-19-86-context-personal-choice-and-text-comparison.md)에서 찾는다. [01과 이번 본문의 실제 비교](../criteria-format-comparison-2026-10-19/README.md)는 유지한 의미·새 구체화·빠진 부분과 작성 이유를 나란히 보여 준다. 기존 가이드·source·01 적용 시안은 옮기거나 합치지 않았다.
