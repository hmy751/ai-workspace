# Noline demo에 적용한 context 구조

앞으로 이 폴더 하나를 계속 발전시킨다. **현재 내용은 중간 커밋으로 보존한 시안이며 전체 구조의 최종안이 아니다.** 특히 Work의 DEVELOPMENT.md 위치·이름·운영 책임과 전반적인 구체화가 남아 있다. [중간 정리90](../../2026-10-19-90-prototype-checkpoint-and-open-design.md)에서 현재 선택과 미결정을 구별한다. 적용 대상은 **[noline-demo/context/](noline-demo/context/README.md)**다. 개인 기준, 제품 맥락, 작업 맥락을 그 안에 나란히 두고, 로그인 완료 범위를 다루는 한 Work에서 함께 사용한다.

[폴더와 본문을 화면에서 보기](viewer.html) · [Noline demo 시작](noline-demo/README.md) · [한 작업을 따라 읽기](walkthrough.md)

이번에는 기존 합의와 다시 대조해 **일반 기준과 상세 사례를 별도 파일로 나눴다.** [일반 기준](noline-demo/context/personal/development/naming-and-completion.md)은 책임·표현·완료 판단의 뜻과 핵심 조건을, [상세 사례](noline-demo/context/personal/development/cases/naming-and-completion.md)는 초대·isError·silent·완료 범위의 구체 상황과 판단 차이를 설명한다. 기존 코드·당시 판단·원문 근거를 보존했으며 원칙 이해에 필요한 짧은 대비는 일반 본문에 남겼다. 사례 전체를 매번 읽는 절차는 아니다.

[Project 가이드](noline-demo/context/project/guidance/code-readability.md)와 [인증 계약](noline-demo/context/project/guidance/authentication-and-session.md)은 제품의 판단 조건을, [current](noline-demo/context/project/current/authentication-flow.md)는 선택 후 이름·코드·지원 범위를 맡는다. [적용 해설](walkthrough.md)은 초기 입력의 재구성과 현재 결과를 구별한다. 사용자 발췌·외부 참고·새 문장과 코드의 지위는 [작성 근거](authoring-basis.md), 이번 수정과 합의 대조는 [기록92](../../2026-10-19-92-principles-cases-and-agreement-reconciliation.md)에서 읽는다. 검토 겸임·생략 조건과 입력 판본 보존을 포함한 운영 세부는 미정이다.

## 실제 파일 배치

```text
development-workflow/
├── noline-demo/
│   ├── AGENTS.md
│   ├── README.md
│   ├── context/
│   │   ├── README.md
│   │   ├── personal/
│   │   │   ├── README.md
│   │   │   └── development/
│   │   │       ├── README.md
│   │   │       ├── naming-and-completion.md    일반 기준·핵심 대비
│   │   │       └── cases/naming-and-completion.md  상세 사례·판단 근거
│   │   ├── project/
│   │   │   ├── README.md
│   │   │   ├── MAINTENANCE.md
│   │   │   ├── REFERENCE/          읽기·본문 구성 기준
│   │   │   ├── common/             제품 의미
│   │   │   ├── current/            현재 구현·지원 범위
│   │   │   ├── guidance/           제품 개발 계약
│   │   │   └── decisions/          제품 선택의 근거
│   │   └── work/
│   │       ├── README.md
│   │       ├── AGENTS.md
│   │       ├── DEVELOPMENT.md      Personal·Project를 선택하는 절차
│   │       └── workspaces/
│   │           ├── README.md
│   │           ├── spec-and-tickets/README.md
│   │           └── 001-login-completion-names/
│   │               ├── README.md
│   │               ├── current/
│   │               │   ├── memory/
│   │               │   │   ├── index.md
│   │               │   │   ├── spec/        한 Work의 다섯 관점
│   │               │   │   ├── tickets/     실행 정의·상태
│   │               │   │   ├── project-context.md
│   │               │   │   └── personal-context.md
│   │               │   └── state/index.md
│   │               ├── source/              부여한 초기 입력
│   │               ├── output/              실제 결과의 위치
│   │               └── records/             선택·작성·검사 이력
│   └── examples/authentication/
│       ├── src/                  메모리 기반 인증 예제
│       └── tests/                완료·실패 경계 검사
├── authoring-basis.md             사용자 판단·외부 참고·새 구체화의 근거
├── walkthrough.md                사람이 읽는 적용 해설
├── viewer/                       화면 생성·검사 도구
└── viewer.html                   위 파일들의 표시 사본
```

프로토타입 바깥에 두었던 작업대 모형과 별도 workflow 폴더는 현재 구성에서 없앴다. 초기 작업 입력도 해당 Workspace의 source에서 찾는다. 바깥에는 화면 도구, 적용 해설과 본문 작성 근거를 둔다. 개발 기준을 적용할 때 작성 이력을 먼저 읽는 절차는 두지 않는다.

## 실제 Noline에서 확인한 것과 이번 추가

실제 Noline의 `context/README.md`, `project/README.md`와 관리·읽기·구성 기준, `work/workspaces/README.md`, 실제 Workspace의 memory·state·Spec·Ticket 배치를 직접 확인했다. 관찰 기준은 Noline `4fb309d2`이며, 확인 경로와 이번 정정은 [기록89](../../2026-10-19-89-local-context-structure-correction.md)에 남긴다.

| 구분 | 이 프로토타입에 반영한 내용 |
| --- | --- |
| 실제 Noline의 구조 | Project의 common/current/guidance, 관리·읽기 기준과 decisions. Work의 current/memory·state, source·output·records. Spec 다섯 파일과 Ticket, 작업별 Project 선택. |
| 사용자 정정에 따른 추가 | `context/personal/`을 Project·Work와 같은 context 아래에 둔다. 실제 Noline에 이미 있는 층이라고 주장하지 않는다. |
| 이번 연결 구체화 | Work의 `DEVELOPMENT.md`가 Personal과 Project를 각각 선택한다. 현재 사용한 개인 주제는 Work memory의 `personal-context.md`에 남긴다. 둘 다 이번 프로토타입에서 구체화한 절차다. |
| 실행 범위 | 인증 예제 코드는 직접 실행할 수 있다. 실제 Noline의 앱 코드를 복제한 것이 아니므로 `examples/authentication/`에 둔다. 실제 Noline의 apps/client·server·packages 전체를 재현하지 않는다. |
| 아직 연결하지 않은 운영 장치 | 실제 Noline의 Recover·Maintain·Verify Harness와 host hook·skill bridge는 이 demo에 설치하지 않았다. 실행되지 않는 기계 계약이나 성공 상태를 꾸며 넣지 않고 문서 경로로 재진입한다. |

## 같은 context 안에서 담당을 나눈다

Personal은 개인의 판단 이유·적용 조건을, Project는 제품 자체의 의미·개발 계약을, Work는 이번 요구·선택·상태·결과를 소유한다. 같은 부모 폴더에 있다는 사실이 본문 통합이나 Project의 개인 기준 관리 의무를 뜻하지 않는다.

01에서 반영하도록 선택한 형식·조건별 적용과 이번에 새로 쓴 질문·예시의 지위는 [작성 근거](authoring-basis.md)에서 구별한다. 핵심 원문 발췌와 원기록 경로를 함께 보존하고, Personal·Project 본문에는 실제 판단에 필요한 설명과 조건을 직접 쓴다.

## 확인과 다음 수정

코드 실행법은 [Noline demo README](noline-demo/README.md#직접-실행한다), 현재 결과와 다음 행동은 [Work state](noline-demo/context/work/workspaces/001-login-completion-names/current/state/index.md), 산출물 위치는 [output](noline-demo/context/work/workspaces/001-login-completion-names/output/index.md)에서 읽는다. 다음 변경도 이 폴더의 해당 Owner를 고친 뒤 [화면 재생성](viewer/README.md)을 수행한다.

이 프로토타입을 만드는 설계 작업 자체는 바깥 [Workspace 014](../../../README.md)가 소유한다. 기존 날짜별 시안과 실제 Noline 원본은 유지한다. 이전 배치와 문서는 [정정89](../../2026-10-19-89-local-context-structure-correction.md)의 변경 전 보존본에서 복원할 수 있다.
