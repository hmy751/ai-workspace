# Building Trust in Agents — 챕터별 상세 정리

> Lauren의 두 번째 강연 스크립트에 근거한 정리입니다. 아래 '실무 적용' 코드는 개념 설명을 위해 추가했으며 강연에 등장한 실제 구현이 아닙니다.

## 0. 핵심 메시지

발표자는 한 달에 약 2,000개의 PR을 Production으로 보낼 수 있었던 이유를 **Trust**라고 설명한다. 여기서 Trust는 Agent가 좋은 일을 할 것이라는 막연한 믿음이 아니다. Agent가 자신의 작업을 검증할 수 있고, Architecture와 Static Analysis가 실수를 방지하며, Codebase 자체가 좋은 Pattern을 보여주기 때문에 **개발자가 모든 Session을 감시하지 않아도 되는 상태**를 뜻한다.

발표자는 Software Factory라는 대량 생산의 이미지보다 **Michelin Kitchen**을 선호한다. 사람은 요리의 모든 단계를 직접 수행하지 않지만 주방의 작업 배치, 장비, 훈련, 최종 품질을 책임지는 Chef와 비슷하다는 비유다.

```text
External Events (Slack / Sentry / Datadog / PlanetScale)
           ↓
Outer Loop: Grokbot Routines / Automations
           ↓
Agent가 작업 시작 및 구현
           ↓
Verification Skills (CLI + Feature Map + 실제 실행 Evidence)
           ↓
Codebase / Architecture / Static Analysis / Rules / Skills
           ↓
신뢰할 수 있는 PR과 배포
           ↓
Gardener가 재발 방지와 품질 개선
```

## 1. Vision for Agent Trust (00:01~02:07)

- 발표자는 자신이 한 달 동안 약 2,000개 PR을 Production에 Shipping했다고 소개한다.
- 핵심은 PR 수가 아니라, 자리에 없을 때에도 Agent가 높은 품질의 작업을 할 수 있도록 환경을 준비했다는 점이다.
- Michelin Kitchen 비유: Line Cook, Sous Chef, 장비, 교육, 식기 세척 인력의 조합처럼 Agent의 Tool, Skill, Workflow, 제약이 품질을 좌우한다.
- 개발자는 제품을 구성하는 모든 코드를 직접 작성하지 않아도 최종 결과에 대한 책임을 진다.

## 2. Overcoming Manual Bottlenecks (02:07~05:35)

### Cursor의 Performance 문제

Cursor Agent Window의 Performance를 개선하는 과정에서 Chrome DevTools, Performance Trace, Heap Snapshot 등을 매번 사람이 수동으로 확인해야 했다. 수많은 PR이 빠르게 들어오므로 Regression이 발생했는지 확인하기 어려웠다.

### 전환점

'Agent가 있는데 왜 내가 직접 이것을 반복하고 있지?'라는 질문에서 출발해 Verification Skill을 만들기 시작했다. Agent가 Application을 실행하고 Trace를 수집하고 분석하여 Hotspot을 찾아 Performance를 개선하도록 만든 것이다.

### 병목은 자기 자신

엔지니어가 가지고 있는 검증 절차와 제품 지식을 Agent Team에 전달해야 사람이 모든 작업의 Blocker가 되지 않는다. 개별 작업을 위임하는 것을 넘어 **작업 방법을 재사용 가능한 Tool로 만든다**는 발상이 중요하다.

## 3. Levels of Agent Verification (05:35~08:38)

### 1~5 Agent 단계의 문제

- 매 Conversation마다 Babysitting과 Course Correction이 필요하다.
- 사람이 없으면 Agent가 방향을 잃거나 잘못된 일을 수행한다.
- 이런 상태에서 100개 Agent를 Spawn하면 Slop PR, Regression, Production Bug가 대량으로 발생할 수 있다.
- 따라서 **Trust Before Scale**: 병렬화 이전에 검증 능력이 필요하다.

### Verification의 범위

| 방법 | 주요 목적 | 난이도/특성 |
|---|---|---|
| Practical Verification | 실제 Application 실행, Trace, Heap Snapshot 수집 | 기존 Browser/Debug Tool 활용 |
| Formal Verification | Business Logic Invariant가 명세 아래서 유지되는지 검증 | Lean, TLA+ 등; 모델링 난도가 높음 |

발표자는 Formal Verification이 여전히 어려운 분야이고, 대부분의 팀은 실용적인 Verification Skill만으로도 많은 것을 얻을 수 있다고 말한다.

## 4. Practical Verification Skills (08:38~13:13)

발표자의 첫 Skill인 **Control Glass**는 Chrome DevTools Protocol을 활용하여 Agent에게 Application 실행과 Trace 수집 방법을 가르친다.

### 구성 1: CLI

매 Agent Session마다 임시 Script를 생성하면 측정 조건과 실행 방식이 달라질 수 있다. Skill Directory에 안정적인 CLI를 만들고 Agent가 반복 사용하게 하면 Reproducibility를 확보하기 쉽다.

```text
verification-skill/
├── SKILL.md
└── cli/
    ├── start-app
    ├── capture-trace
    └── capture-heap
```

*실제 Skill 구조가 아닌 설명용 예시.*

CLI는 Application을 실행하고 Performance Trace, Heap Snapshot 등의 **Empirical Evidence**를 모은다. '코드를 수정했으니 빨라질 것'이라는 주장과 실제 측정 결과를 구분할 수 있다.

### 구성 2: Feature Map

사용자가 Slack에 UI의 일부 Screenshot과 `???`만 남기면 Agent는 실행 Tool이 있어도 무슨 기능을 말하는지 모를 수 있다. 그래서 발표자는 Sitemap과 유사한 **Feature Map**을 제안한다.

Feature Map에 포함되는 정보:
- Application에 어떤 Feature가 있는가?
- 그 Feature의 목적과 동작은 무엇인가?
- 어떤 Keyboard Shortcut 또는 DOM Element를 통해 접근하는가?
- User가 기능을 사용하려면 어떤 단계를 거치는가?

Feature Map은 Skill Directory에 저장되어 일종의 Materialized Memory가 되고, Automation으로 유지보수된다.

### CLI + Feature Map의 결합

CLI는 **어떻게 조작하고 측정하는가**를 제공한다. Feature Map은 **어느 기능을 어떻게 찾아가야 하는가**를 제공한다. 둘을 합치면 모호한 Bug Report도 실제 Application 흐름에 연결하고 재현할 수 있다.

### Correctness, Performance, Quality 구분

| 항목 | 질문 |
|---|---|
| Correctness | Feature가 원하는 기능을 실제로 수행하는가? |
| Performance | 얼마나 효율적으로 동작하는가? |
| Code Quality | 설계와 코드가 유지보수하기 좋은가? |

Checkout Button이 실제 결제를 수행하는지 Verification한다고 해서 Performance와 Code Quality까지 자동으로 검증되는 것은 아니다. 따라서 엔지니어링 Skill과 실제 Metric을 함께 사용해야 한다.

## 5. Architecting for Agent Success (13:13~17:22)

### PAC Plugin

발표자는 Debugging, Feature Development, Prototyping 등에 자신이 사용해온 Workflow를 Playbook/Skill로 만든 PAC Plugin을 소개한다. 숙련된 엔지니어의 암묵적인 작업 방법을 팀 공통 Skill Repository에 축적할 수 있다.

### Codebase as Memory

Agent가 읽은 File은 Context Window의 일부다. Agent는 매 PR에서 모든 것을 Refactor하기보다 **기존 Pattern을 복사하고 확장**한다. 그래서 좋은 Codebase는 Agent의 좋은 구현을 유도하는 Memory가 된다.

### Trust를 구축하는 다섯 영역

발표자는 높은 강제력의 기법부터 상대적으로 부드러운 Guidance까지 하나의 연속선으로 제시한다.

1. **Codebase / Architecture:** 나쁜 Pattern이 아예 불가능하도록 설계.
2. **Static Analysis:** Linter, Compiler Diagnostics, CI로 제약을 강제.
3. **Rules:** Agent에게 따라야 할 지침 제시.
4. **Bugbot / Skills:** 자동 Review와 Workflow 안내.
5. **Style Guide / Human Review:** 규칙을 사람이 기억하고 코드를 읽어 검증.

강연에서 Rules, Bugbot, Skills는 함께 Guidance 계층으로 설명된다. 원칙은 **사람이 지적하기 전에 구조나 도구로 문제를 막는 것**이다.

## 6. Establishing Agent Standards (17:22~22:39)

### Style Guide만으로는 충분하지 않다

모든 PR의 모든 변경 줄을 사람이 읽고 Style Guide 위반을 찾는 것은 규모가 커질수록 현실성이 떨어진다. Review에서 반복되는 문제를 발견하면 Architecture, Static Analysis, Rules/Skills로 옮긴다.

### 'Agent는 Shortcut을 좋아한다'

발표자 팀은 Agent-friendly Framework인 **Dune**을 구축했다. 핵심은 Agent에게 **가장 쉬운 길이 가장 올바른 길**이 되게 만드는 것이다. 이것이 Paved Path 접근이다.

예시:
- API 요청은 공통 API Client 경유.
- Feature Code는 하나의 Directory에 Co-location.
- Layer 사이의 Import는 명확한 Dependency Rule을 따름.
- UI Renderer에서는 무거운 Process Code를 사용하지 못하도록 제한.

### 팀에 엔지니어가 아닌 Builder도 늘어난다

Designer, Product Manager, CEO 등 코드에 익숙하지 않은 사람이 Agent를 조작해 Feature를 Shipping할 수 있다. Context가 부족한 Agent라도 규칙을 추측하지 않아도 되도록 구조를 명확하게 만드는 것이 중요하다.

### Anti-pattern의 바이러스성 확산

기존 Workaround나 주석을 Agent가 그대로 따라 하면 며칠/몇 주 만에 나쁜 Pattern이 사실상의 Convention이 될 수 있다. Codebase 품질을 유지하는 것은 현재 유지보수뿐 아니라 미래 Agent의 출력 품질을 보호하는 일이다.

## 7. The Role of the Gardener (22:39~26:42)

### Gardener란

정원의 잡초를 관리하듯 Codebase에 생기는 Technical Debt, Workaround, Anti-pattern을 조기에 찾아 확산을 막는 책임이다.

### Code Comment 금지 사례

발표자 팀에서는 Agent가 Workaround Comment를 근본 문제를 해결하지 않을 이유로 삼고, 임시방편을 복사하는 문제가 있었다. 그래서 Dune에서는 Comment를 금지했다. 이는 **그 팀의 특정 정책**이지 모든 프로젝트에 일반적으로 적용해야 할 규칙이라는 뜻은 아니다.

### Dune의 세 가지 운영 원칙

1. **기존 Technical Debt 삭제.** Agent가 나쁜 패턴을 복사하지 않게 한다.
2. **Single Paved Path 강제.** 권장 Pattern을 위한 표준 구현 경로를 만든다.
3. **Lint Rule로 출혈 차단.** 전체 Debt를 즉시 청산하지 못해도 새 Anti-pattern이 추가되지 않게 한다.

발표자의 판단 기준: **'다음 Agent가 이 코드를 그대로 복사해도 만족할 수 있는가?'**

## 8. The Dune Framework (26:42~30:38)

### 구조

Dune은 Grokbot을 구동하는 Agent-friendly Client Framework. Feature, React Entry Point, Transcript Card, Host, Client 같은 단위와 Import Boundary를 가진다. Feature는 하나의 Folder에 Co-location하는 등 배치와 의존성 Convention을 엄격히 정한다.

### Electron Performance 사례

Cursor Agent Window에서는 무거운 코드가 Renderer에 잘못 Import되어 UI Performance를 악화시키는 문제가 있었다. Dune은 Main 쪽 코드와 Renderer 쪽 코드의 경계를 Import/Dependency Graph로 강제한다.

- 60 FPS의 Frame 간격은 약 16.7ms.
- 120 FPS의 Frame 간격은 약 8.3ms.
- Renderer가 Long Task로 막히지 않도록 작은 Chunk로 작업을 나누어야 한다.

**중요:** 발표자의 메시지는 특정 Dune 구현을 복제하라는 것이 아니라, 팀에 쌓인 Performance·설계 교훈을 Codebase 자체에 Encoding하라는 것이다.

## 9. System-wide Integration (30:38~36:06)

### Outer Loop

Grokbot은 Slack, Datadog, Sentry, PlanetScale 등의 Connector에서 Event와 정보를 받고 Cloud Agent 같은 작업을 자동 시작하는 Outer Loop를 맡는다. 발표자는 이것을 반드시 거대한 'Company Brain'으로 만들 필요는 없다고 말한다. Agent가 기존 Tool을 잘 활용할 수 있기 때문이다.

### Michelin Kitchen 구축

```text
Sentry Alert / Slack Thread
  → Grokbot Routine
  → Cloud Agent 작업 시작
  → 기존 Skills와 Verification 재사용
  → Bug Reproduction / Code Fix
  → PR 자동 생성
```

Codebase, Lint, Diagnostics, Rules, Bugbot, Skills가 각각 독립된 도구가 아니라 결합된 **재사용 가능한 Infrastructure**가 된다. Cursor Automations와 SDK로 추가 Bot도 구축할 수 있다. 발표자는 실제로 Bug Report 자동 재현과 PR 생성에 사용한다고 이야기한다.

### 병렬화의 조건

이런 환경이 구축된 이후에야 Agent를 더 높은 수준으로 병렬화하고 팀 전체로 확장하는 것이 유리하다. 높은 Trust는 많은 Agent를 실행하기 위한 출발점이다.

## 10. Closing Thoughts on Trust (36:06~37:50)

Agent를 수정하거나 개입할 때마다 다음 질문을 한다.

1. Codebase, Architecture, Data Structure를 바꿔 그 실수를 원천적으로 불가능하게 만들 수 있는가?
2. Static Analysis로 자동 검출할 수 있는가?
3. Rules와 Bugbot, Skills로 적절한 Guidance를 제공할 수 있는가?
4. Code Quality를 검증하는 Skill을 더 잘 만들 수 있는가?

최종 목표는 **Agent 자체에 대한 막연한 신뢰가 아니라, Agent가 일하는 Environment에 대한 근거 있는 신뢰**다.

## 11. React / TypeScript / Next.js 실무 적용 (정리자가 추가한 예시)

### 단계 1 — Verification부터 구축

- Agent가 `next dev`로 App을 실행할 수 있게 설정.
- `tsc --noEmit`, ESLint, Vitest, Playwright를 표준 스크립트로 제공.
- 실제 Browser E2E, Performance Trace와 Screenshot을 수집할 수 있는 Tool/CLI 구성.

### 단계 2 — Feature Map 제작

```yaml
features:
  search:
    entry:
      shortcut: "Meta+K"
      selector: "[data-testid='search-button']"
    flow:
      - open_search
      - type_query
      - select_result
    expected:
      - selected_project_opens
```

*이 YAML은 원문에 등장하지 않는 실무 예시.*

### 단계 3 — Architecture Paved Path

```text
src/
├── app/
├── features/
│   ├── auth/
│   └── dashboard/
├── domain/
└── shared/
    ├── api/
    └── ui/
```

중요한 것은 폴더 모양 자체가 아니라 기능의 위치와 Layer Dependency가 일관되게 유지되는 것이다.

### 단계 4 — 반복 오류를 Lint/Type/CI로 옮기기

특정 API Client를 직접 Import하는 것이 금지라면 ESLint `no-restricted-imports`로 차단할 수 있다. Business Invariant는 Type/Runtime Validation으로, UI Behavior는 실제 Rendering/E2E Test로 검증한다.

### 단계 5 — Gardener 활동 정례화

- Review에서 반복된 Comment 수집.
- 신규 Workaround와 Anti-pattern 감지.
- 금지할 Import/Pattern을 Lint Rule로 정의.
- Tech Debt 제거 후보 선정.
- Feature Map 및 Skill의 최신성 확인.
- 'Agent가 이 코드를 복사해도 괜찮은가?'를 리뷰 기준으로 활용.

## 12. 앞선 PR Bottleneck 강연과의 관계

| 주제 | PR Bottleneck 강연 | Agent Trust 강연 |
|---|---|---|
| 문제 | PR Review 처리량 부족 | Agent 결과를 믿기 어려움 |
| 초점 | Checks → AI Review → Human Review | Verification + Agent-friendly Architecture |
| 구조 | Deep Module | Paved Path, Dune, 강한 Boundary |
| 학습 루프 | Retro로 반복 Comment를 규칙화 | Gardener가 Anti-pattern을 차단 |
| 지향점 | 빠르고 안전한 PR 통과 | 사람 개입 없이 좋은 결과를 내는 환경 |

두 강연은 상호 보완적이다. Agent Trust 강연은 **좋은 코드가 생성될 환경**에 집중하고, PR Bottleneck 강연은 **생성된 변경을 빠르고 신뢰성 있게 통과시키는 과정**에 집중한다.

## 13. 최종 메시지

**Agent 수를 늘리기 전에, Agent가 일을 이해하고 실행하고 검증할 수 있는 Tool과 좋은 Pattern을 따르게 하는 Architecture를 만들라. 반복되는 실수는 Prompt로만 교정하지 말고 Codebase, Lint, Skills에 반영하라.**
