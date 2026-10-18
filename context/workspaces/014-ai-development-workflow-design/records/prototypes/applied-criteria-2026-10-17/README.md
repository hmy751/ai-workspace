# 기준·사례·작업·후속 설계가 이어지는 시안

**문서는 실제 파일이고 제품·작업 장면은 가상이다.** shop-web의 AGENTS·develop도 형식을 보여 주는 예시이며 설치된 지침이 아니다. HTTP 장면의 구현·검사 결과는 가정이고, 새 주문 장면은 구현 전 판단까지 채웠다. 실제 제품 코드·테스트는 없다.

현재 시안은 사용자 요청에 따라 **공통을 짧게 두고 이름·가독성을 별도 절로 찾는 방향**을 반영했다. [요청·변경 이유·03에 남긴 판단72](../../2026-10-18-72-short-common-and-detail-prototype.md). 일반 원칙 전체의 의무 채택, 영구 파일 배치, 실제 사용 효과는 별도로 판단한다.

## 이번 보완을 읽는 입구

1. **작업자가 어떻게 찾아 읽는가:** [주문 작업 장면](order-walkthrough.md). 같은 작업 경로와 역할을 전달받고, 현재 동작·짧은 공통에서 필요한 상세와 사례로 내려가는 문서 링크와 판단을 볼 수 있다.
2. **기준이 실제로 어떻게 존재하는가:** [Project의 읽기 안내](shop-web/context/project/README.md#reading-route)와 [기준 본문](shop-web/context/project/quality.md). 같은 quality 문서 안에서 공통과 상세를 절로 구별한다. [이름·가독성](shop-web/context/project/quality.md#naming-readability)도 독립적으로 찾아갈 수 있다.
3. **무엇이 원칙이고 무엇이 제품의 값인가:** [주문 대비 사례](shop-web/context/project/cases/order-flow.md), [현재 주문 동작](shop-web/context/project/order-workflow.md), [이번 작업 요구](shop-web/context/workspaces/order-coupon-refresh/ticket.md). 사례의 조건, 현재 제품 계약, 이번 목표가 서로 다른 문서 역할로 존재한다.
4. **03에서 무엇을 다시 판단하는가:** [후속 설계 장면](refinement-walkthrough.md). 이번 선택의 이유와 다시 볼 실제 조건, 유지·변경할 본문과 읽기 안내의 반환 위치를 연결했다.

앞선 [Field 작업 장면](field-walkthrough.md)은 같은 공유 원칙이 다른 조건에서 기존 연결 유지로 이어지는 대비다. [HTTP-07 장면](walkthrough.md)은 구현·검토자 직접 수정·결과 기록을 끝까지 채운 가상 예시다. 해당 작업의 가상 검사 통과를 주문 작업의 상태로 옮기지 않는다.

## 실제 파일의 배치

```text
shop-web/
├── AGENTS.md
├── .agents/skills/develop/SKILL.md
└── context/
    ├── project/
    │   ├── README.md                 # 제품 이해와 필요한 자료의 읽기 안내
    │   ├── quality.md                # 짧은 공통 + 주제별 상세 절
    │   ├── http-client.md            # 현재 HTTP 계약
    │   ├── order-workflow.md         # 수정 전 주문 계약
    │   └── cases/
    │       ├── shared-choice.md      # Field·Container 조건 대비
    │       └── order-flow.md         # 같은 API·다른/같은 주문 흐름 대비
    └── workspaces/
        ├── order-coupon-refresh/
        │   ├── README.md             # 구현 전 상태와 이어받는 경로
        │   └── ticket.md             # 목표·범위·확인할 동작
        └── http-error-contract/
            ├── README.md
            ├── ticket.md
            └── records/
                ├── implementation.md
                └── review.md
```

일반 기준의 내용은 quality, 작업 단서에서 기준·현재 계약을 찾는 안내는 Project README, 구현·검토의 절차는 develop이 맡는다. AGENTS와 작업 README에는 필요한 입구만 연결하고 같은 안내 표를 복제하지 않는다.

실제 채팅에서 보내는 의뢰와 반환은 각 walkthrough에 채웠다. 지속 문서마다 채팅 메시지 사본을 두지는 않는다. 주문 작업에는 아직 구현·검토 결과를 만들지 않았으며, Field와 후속03은 별도 가상 Workspace 세트를 만들지 않고 장면 문서에서 보여 준다.

## 고치려는 대상에 맞춰 들어간다

| 고치려는 내용 | 실제 위치 |
| --- | --- |
| 일반 판단 방향·조건·이름과 표현 관점 | [quality.md](shop-web/context/project/quality.md) |
| 필요한 상세·계약을 찾는 조건 | [Project README](shop-web/context/project/README.md#reading-route) |
| 구현·검토·확인·반환 절차 | [develop](shop-web/.agents/skills/develop/SKILL.md) |
| 현재 제품의 약속 | [주문 동작](shop-web/context/project/order-workflow.md) 또는 [HTTP 계약](shop-web/context/project/http-client.md) |
| 이번 주문의 목표·진행 | [작업 README](shop-web/context/workspaces/order-coupon-refresh/README.md)와 [Ticket](shop-web/context/workspaces/order-coupon-refresh/ticket.md) |
| 사례 조건과 해석 | [주문 사례](shop-web/context/project/cases/order-flow.md) 또는 [Field·Container 사례](shop-web/context/project/cases/shared-choice.md)에서 원기록으로 이동 |
| 현재 배치와 본문을 다시 설계할 이유 | [후속 설계 장면](refinement-walkthrough.md)과 [반영 근거72](../../2026-10-18-72-short-common-and-detail-prototype.md) |

사람이 시안을 검토·수정하는 입구는 이 README이고,014의 현재 기록은 Main이 갱신한다. 실제 대상 Project에서 기준을 채택·갱신할 권한과 책임은03·04-03 등 관련 Ticket에서 구체화한다.

이전 보완의 이유는 [원칙·사례 구별66](../../2026-10-18-66-principles-cases-and-refinement-prototype.md), [리뷰 세 의견 반영68](../../2026-10-18-68-principle-application-and-choice-basis.md)에 보존했다. 원칙 채택 이후에도 현재 목적·조건으로 적용하며, Field의 공유 이득 부족과 목표 미충족 반환, HTTP의 현재 계약과 작업 제외 범위 구별을 유지한다. 최신 형식의 도출은 [구성안70](../../2026-10-18-70-criteria-organization-proposal.md)과 [주문 대입71](../../2026-10-18-71-order-reading-and-criteria-boundaries.md)에서 읽는다.
