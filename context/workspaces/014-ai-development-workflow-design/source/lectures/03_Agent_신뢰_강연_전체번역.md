# Building Trust in Agents — 전체 한국어 번역

> 발표자의 순서와 표현을 최대한 유지했습니다. Agent, Skill, CLI, Verification, Codebase 등 기술 용어는 원문에 가깝게 표기했습니다. 자동 생성 자막의 고유명사는 문맥에 맞게 정리했습니다.

## 챕터 1. The vision for agent trust (00:01~02:07)

안녕하세요. 저는 Lauren입니다. PotatoOnX로 알고 계실 수도 있습니다. SpaceX AI에서 Grokbot을 개발하고 있습니다. 지난달 저는 꽤 미친 짓을 했습니다. Production에 2,000개의 Pull Request를 배포했습니다.

제가 그렇게 할 수 있었던 이유의 상당 부분은 Trust입니다. 제가 자리에 없을 때에도 Agent들이 높은 품질의 작업을 만들어낼 거라고 어떻게 신뢰할 수 있는지 늘 생각합니다. 오늘의 주장은 Agent를 위한 Environment를 정말 잘 설정하면 개인 또는 팀 전체를 위한 Software Factory 같은 것을 만들어 전보다 훨씬 빠른 속도로 높은 품질의 코드를 생산할 수 있다는 것입니다.

그런데 저는 Software Factory라는 말이 마음에 들지 않습니다. Michelin Kitchen이라는 비유가 더 좋습니다. 기술자로서 우리가 하는 일은 조립 라인에서 제품을 대량 생산하는 일이 아닙니다. 창의적인 일이고 제품을 만드는 행위이며, 어떤 의미에서는 예술입니다. Agent를 사용하면서 제품을 이루는 개별 재료를 직접 요리하지 않게 되더라도 최종 결과에 대한 책임은 여전히 우리에게 있습니다. Kitchen을 어떻게 꾸릴지도 생각해야 합니다.

Line Cook과 Sous Chef를 어떻게 배치하는지, 어떤 장비와 훈련을 제공하는지, 식기 세척 담당자를 어떻게 두고 그 비율을 어떻게 할지 등 모든 요소가 최종 제품에 영향을 줍니다. 저는 이 비유가 정말 적절하다고 생각합니다. 시작하기 전에 이야기를 하나 해보겠습니다.

## 챕터 2. Overcoming manual bottlenecks (02:07~05:35)

6개월 전 Cursor에 처음 합류했을 때, SpaceX AI의 일부가 되기 전이었고, 막 입사했으니 사용할 Agent Skill이 없었습니다. 새로운 Codebase와 처음 작업하는 Product였습니다.

그때 Cursor는 Cursor IDE를 대체할 새로운 Agents Window를 만들고 있었습니다. 제가 합류하기 전부터 Agent Window에는 Performance 문제가 많았습니다. 당시 Manager가 도와줄 수 있냐고 물었고, 저는 전에 React Team에서 일했기 때문에 잘 맞는 작업으로 보였습니다.

하지만 일을 시작하자마자 이 Process가 얼마나 Manual한지 깨달았습니다. Performance 작업은 전에도 했습니다. 그런데 PR이 Merge되는 속도를 보니 끝없이 밀려드는 PR의 벽이 거의 넘을 수 없게 느껴졌습니다. Application Performance에 Regression이 발생하고 있는지도 알 수 없었습니다.

초기에는 Chrome DevTools를 보고 Performance Trace를 수집하고 Heap Snapshot을 찍는 데 시간을 많이 썼습니다. 모든 과정이 극도로 수동적이었습니다. 너무 답답해져서 생각했습니다. '잠깐, 우리에게 Agent가 있는데 나는 뭘 하는 거지?'

그래서 Verification Skill을 생각했습니다. Agent가 직접 Application을 실행하고, Trace를 수집하고 이해하고, Hotspot을 찾아내어 Application Performance가 개선되는 방향으로 자동으로 Hill Climbing할 수 있다면 어떨까요?

지난 6개월 동안 Cursor와 SpaceX AI에서 일하며 제 개인적인 생산성이 크게 높아졌습니다. 사실 한 달에 2,000개의 PR을 Shipping하겠다는 목표를 세운 적은 없었습니다. 그런데 제가 만들던 모든 Skill과 Tool, Codebase 변경이 결국 Trust라는 생각으로 모인다는 걸 깨달았습니다.

그때는 몰랐지만 마음속에는 '내가 병목이다. 엔지니어로서 가진 지식을 Agent Team에 전달해서 내가 매번 Blocker가 되지 않도록 해야 한다'는 생각이 있었습니다. 그리고 실제로 성과가 나타났습니다. 핵심은 Trust입니다. 그렇다면 Agent 사용의 어느 단계에 있든 이 Trust를 어떻게 쌓아야 할까요?

## 챕터 3. Levels of agent verification (05:35~08:38)

처음에는 저도 Agent 1~5개를 사용하는 단계에 있었습니다. 매 Chat과 Conversation을 Babysitting해야 한다고 느끼는 단계죠. 계속 Course-correcting하며 Agent가 올바른 일을 하게 개입하고 수정합니다. 자리를 비우면 아무 일도 제대로 일어나지 않고 Agent가 잘못된 일을 합니다.

사실 이 단계에서 벗어나는 것이 가장 어렵다고 생각합니다. 어떻게 벗어날지 항상 분명하지 않으니까요. 결국 Trust의 문제입니다. 한두 개나 1~5개에서 100개 정도의 Agent로 넘어가지 못하는 것은 아직 그 결과물을 신뢰하지 못하기 때문입니다. Trust 없이 Sub-agent나 Cloud Agent 100개를 Spawn하면 Slop PR, Regression, Bug가 잔뜩 Shipping되고 아무도 좋아하지 않을 겁니다.

그럼 Agent를 어떻게 더 신뢰할까요? 제 경우 Cursor Agent Window Performance를 작업하면서 Verification의 필요성을 깨달은 것이 시작이었습니다. Verification에도 여러 수준이 있습니다.

한쪽 끝에는 Verification Skill처럼 Agent에게 Application 실행 방법과 Chrome DevTools Protocol 또는 Debugging Protocol 사용법을 가르쳐서 Debug, Performance Trace, Heap Snapshot 등을 수집하게 하는 실용적인 방법이 있습니다.

반대쪽 끝에는 더 어렵고 아직도 Open Question인 Formal Verification이 있습니다. Formal Methods나 Lean, TLA+ 같은 언어를 이용해서 Business Logic의 Invariant가 항상 참인지, Application이 올바른 상태인지 형식적으로 검증하는 것입니다. 실제로 Formal Methods를 실행할 능력이 있는 사람은 매우 적습니다. 하지만 Verification Skill만으로도 굉장히 멀리 갈 수 있습니다.

## 챕터 4. Practical verification skills (08:38~13:13)

Cursor에 합류해 Agent Window를 작업할 때 처음 만든 Skill은 Control Glass라는 Verification Skill이었습니다. Chrome DevTools Protocol을 이용해 Agent에게 Application을 실행하고 Trace를 수집하게 가르칩니다.

이 Skill은 Iteration을 거쳐 현재의 형태가 됐습니다. 처음부터 이렇지는 않았습니다. Control 또는 Verification Skill에는 실제로 두 가지 구성요소가 있습니다.

첫째는 CLI입니다. Agent가 재현 가능한 방식으로 Application을 실행하고 Trace를 수집해 코드가 동작하며 Performance 기준을 만족한다는 Empirical Evidence를 확보해야 합니다. 매 Session마다 Agent가 새 Script를 만들면 서로 다를 수 있습니다. 대신 Skill Directory 안에 CLI를 만들어두면 매번 그걸 사용할 수 있습니다. 당연히 다양한 Use Case를 처리하고 Application을 정확하게 실행하도록 CLI 자체에도 투자해야 합니다.

둘째는 Feature Map입니다. 제가 이름을 붙인 개념인데, Sitemap에서 영감을 받았습니다. Cursor에서 Control Skill을 사용하자 문제가 드러났습니다. Slack Report로 사용자가 UI의 아주 작은 부분을 캡처한 모호한 Screenshot과 물음표 세 개만 보내는 경우가 있었습니다. Agent는 Application을 실행할 수 있었지만 사용자가 정확히 무엇을 뜻하는지 몰라 추측해야 했습니다.

그래서 Feature Map을 만들었습니다. 일종의 Materialized Memory로, Application이 어떻게 동작하는지, 어떤 Feature가 있는지, 사용자가 Keyboard Shortcut이나 DOM Element 클릭 등으로 어떻게 그 Feature에 접근하는지, 각 Feature가 무엇을 하는지 기록합니다. Feature Map은 Codebase의 Skill Directory에 저장하고 Automation으로 유지보수합니다.

CLI와 Feature Map을 결합하니 아주 강력했습니다. Agent는 Application을 재현 가능하게 제어하고 Trace를 수집할 뿐 아니라 내부와 외부 User의 요청도 이해할 수 있었습니다. Control Verification Skill은 팀의 핵심 Infrastructure가 되었고 우리는 꾸준히 관리합니다. Agent가 자신의 작업을 직접 검증할 수 있다는 것은 매우 강력합니다. 그 Trust를 만들기 위해 Skill에 많은 시간을 투자했습니다.

물론 Verification 외의 것도 필요합니다. Verification은 주로 Correctness에 관한 것입니다. Correctness란 Feature나 Code가 원하는 일을 실제로 하는가입니다. Checkout Button을 눌렀을 때 실제로 결제가 되는가 하는 것이죠. Verification은 기능이 실제로 작동한다는 Empirical Evidence를 줍니다. 하지만 그 Feature의 Performance나 Code Quality에 대해 많은 것을 말해주지는 않습니다. 그래서 Agent가 진짜 Software Engineer처럼 일하도록 가르치는 Skill을 생각해야 합니다.

## 챕터 5. Architecting for agent success (13:13~17:22)

저는 PAC이라는 Plugin을 만들었습니다. 오늘 많이 설명하지는 않겠지만 제가 만든 여러 Skill을 모은 것입니다. Debugging, Feature Development, Prototyping 등 제가 Software Engineering을 하며 직접 사용해온 Workflow에서 영감을 받은 Playbook과 Skill입니다. Agent에게 원하는 방식으로 코드를 작성하는 법을 가르칩니다.

경험 많은 엔지니어가 기여하여 팀 공통 Skill Repository를 만들면 Agent가 훨씬 더 똑똑해질 수 있습니다. 그런 Skill과 Verification Skill을 결합하면 Agent가 작업의 Correctness뿐 아니라 높은 품질도 확인할 수 있습니다. 실제 Performance Metric, 숫자, 통계, Telemetry를 수집할 수도 있습니다. 투자할 가치가 큰 부분입니다.

또 정말 중요한 것은 Architecture를 Refactoring 또는 Rewriting해서 Agent-friendly하게 만드는 것입니다. 소프트웨어 팀이 할 수 있는 가장 중요한 일 중 하나라고까지 말하고 싶습니다. 미래에 Agent들이 모든 코드를 작성할 것이라고 믿는다면, 기본적으로 올바른 일을 하게 Codebase를 설계해야 합니다.

Agent Trust를 구축하는 데는 일종의 Scale 또는 Continuum이 있습니다. Codebase는 최고의 Memory 형태입니다. Agent는 눈앞에 있는 기존 Pattern을 확장하는 것을 좋아합니다. LLM은 Context Window에 들어 있는 것을 사용해 변경할 가능성이 높고, Agent가 열어본 File이 Context Window를 구성하기 때문입니다. Agent는 모든 PR에서 Codebase를 통째로 Refactor하는 게 아니라 있는 Pattern을 연장합니다.

다음 수준은 Static Analysis입니다. Linter, Compiler Diagnostics, Continuous Integration 같은 것을 통해 Guideline과 Constraint를 강제할 수 있습니다. Agent가 같은 실수를 반복하면 Lint Rule을 추가할 수 있습니다. 더 좋은 방법은 그 실수가 구조적으로 불가능해지도록 Codebase를 Refactor하는 것입니다.

그 위에는 Hard Constraint보다 Guidance에 가까운 Rules, Bugbot, Skills가 있습니다. Agent가 대체로 사용하겠지만 어떤 이유로 Rule을 읽지 않거나 User가 무시할 수도 있습니다. 그래서 완벽하게 강제되지는 않지만 Trust를 구축하는 중요한 부분입니다.

## 챕터 6. Establishing agent standards (17:22~22:39)

마지막에는 Style Guide가 있습니다. 사실상 Human Code Review를 통해 강제되는 경우가 많습니다. 물론 Rules, Bugbot, Skills에 넣을 수도 있지만 그러지 않으면 Human이 변경된 모든 줄을 직접 보고 지적해야 합니다. PR이 밀려드는 속도를 생각하면 불가능합니다. 따라서 Style Guide에만 의존하지 마세요. Human Review는 부족한 것을 찾기 위한 출발점으로 유용하지만, Codebase와 Data Structure, Algorithm으로 문제를 아예 불가능하게 하고 Static Analysis를 적용한 뒤 Rules, Bugbot, Skills를 쌓는 데 투자해야 합니다.

우리는 Grokbot Codebase에서 Dune이라는 Agent-friendly Framework를 구축했습니다. Cursor Agent Window의 Performance 문제에서 배운 것이 많은 영감이 됐습니다. 핵심 원칙은 **Agent는 Shortcut을 정말 좋아한다**는 것입니다. 그렇다면 Agent에게 가장 쉬운 Shortcut이 곧 올바른 경로가 되도록 Framework를 만들면 어떨까요?

인간이 코드를 작성하기에는 지나치게 엄격해서 짜증 날 수도 있습니다. 무엇을 할 수 있고 할 수 없는지 제한돼 있기 때문이죠. 하지만 Context가 거의 없는 Agent에게는 완벽한 환경이 될 수 있습니다. 이제 Codebase에 기여하는 사람이 모두 엔지니어인 것은 아닙니다. Designer, Product Manager, CEO도 직접 Feature를 Shipping할 수 있습니다. 바쁘고 Context가 부족한 사람이 Agent를 사용해도 기본적으로 좋은 결과가 나오도록 해야 합니다.

Codebase는 Agent의 Memory이고 Agent는 기존 Pattern을 확장합니다. 반대도 사실입니다. 나쁜 Pattern을 구조적으로 금지하거나 Lint Rule로 막을 수도 있지만, 기존 Anti-pattern이 남아 있으면 바이러스처럼 퍼질 수 있습니다. 작은 Workaround나 그 이유를 적은 Comment 하나를 Agent가 복사하고, 며칠 또는 몇 주 사이 온 Codebase에 퍼져 De facto Pattern이 되어버릴 수 있습니다. 그건 정말 나쁜 상태입니다.

그래서 Agent의 실수를 수정할 때마다 Codebase와 Static Analysis의 변경을 고민하고 좋은 Rules, Bugbot, Skills를 쌓아야 합니다. 저는 Codebase를 정원에 비유하기도 합니다. 처음에는 무해해 보이는 Workaround가 Agent의 복사를 통해 증식해 유지보수가 고통스럽고 Performance 문제가 많은 Vibe-coded Codebase가 될 수 있습니다. 완벽한 Agent Codebase는 매우 엄격하게 표준화된 Codebase라고 생각합니다.

## 챕터 7. The role of the gardener (22:39~26:42)

인간에게 코드를 쓰기 짜증 날 정도로 제약이 많지만 Convention과 Standard가 너무 명확해 무해해 보이는 Pattern조차 금지되는 상태입니다. 가장 좋은 예시는 Agent가 코드에 Comment를 남기는 Pattern입니다.

처음에는 Agent의 Comment가 상당수 Slop이라고 생각했지만 꼭 나쁘다고 보지는 않았습니다. 사람도 Edge Case, Workaround, 어려운 Codebase의 부분에 대해 자신이나 동료에게 Note를 남기려고 Comment를 쓰니까요.

그런데 Cursor Codebase에서 보니 Agent들은 주변 Comment를 실제 문제를 해결하지 않아도 된다는 정당화 근거로 사용했습니다. 근본 문제 대신 Band-aid나 단기적인 해결책으로 덮는 것이었죠. 그래서 Grokbot을 구동하는 Dune에서는 Comment를 금지했습니다. Agent가 그 Pattern을 복사해 퍼뜨리지 못하도록 하기 위해서입니다.

제가 제안하는 것은 모든 팀에 **Gardener**라고 부르는 역할이 필요하다는 것입니다. 실제 정원에서는 원하지 않는 방향으로 자라나는 잡초와 다른 유기적인 성장, 해충을 살펴봐야 합니다. 정원 가꾸기는 사실 잘 모르지만요. Codebase에서도 그런 것들이 퍼지기 전에 싹을 잘라야 합니다.

Dune의 원칙은 세 가지에 집중합니다. 첫째, 기존 Technical Debt를 제거합니다. 둘째, 권장된 Pattern에는 하나의 Paved Path를 유지하거나 강제합니다. 한 가지 Conventional Way가 있어 Agent가 추측할 필요가 없게 합니다. Codebase, CI, Lint Rule에서 그 길을 안내해야 합니다.

셋째, Technical Debt나 Bad Pattern을 발견하면 먼저 '이것을 막는 Lint Rule을 만들어야겠다'고 생각합니다. 곧바로 전부 정리하지 못하더라도 Lint Rule로 출혈을 멈출 수 있습니다. 문제가 완전히 해결되지는 않지만 커지는 것은 막을 수 있습니다. Anti-pattern이 바이러스처럼 퍼지지 않도록 방어한 뒤 Agent를 활용해 기존 문제도 정리하세요. **Agent가 이 코드를 복사해도 만족할 상태**로 Codebase를 유지하는 Mindset을 추천합니다.

## 챕터 8. The Dune framework (26:42~30:38)

Dune의 모든 Detail을 살펴보지는 않고 흥미로운 부분만 지나가겠습니다. Dune은 Grokbot을 위해 만든 Architecture이자 Client Framework입니다. Code가 어디에 있어야 하는지, 서로 어떻게 Import해야 하는지에 대해 많은 Convention을 만들었습니다.

Dune Application에는 몇 가지 Concept이 있습니다. Feature는 하나의 Folder에 Co-location됩니다. React 쪽의 Entry Point는 일종의 Route처럼 생각할 수 있습니다. Grokbot Application에 표시되는 Transcript Card, Grokbot Virtual Machine에서 실행되는 Host, 전체 Application을 구동하는 Client도 있습니다.

이들 사이에는 엄격한 Boundary가 있습니다. 예를 들어 Electron의 Main Process나 Main Thread에서 실행해야 하는 코드가 Renderer Thread에서 실행되지 못하게 합니다. Cursor Agent Window에서 코드가 실수로 Renderer에 Import되어 UI가 느려지는 사례를 겪었기 때문입니다.

Renderer는 부드럽고 Performance가 좋아야 합니다. 60 FPS라면 16ms 정도, 120 FPS라면 8ms 정도보다 긴 작업을 피해야 합니다. Renderer는 작업을 작은 단위로 나누어 처리할 수 있어야 하고 한 번에 모두 수행해서는 안 됩니다. Dune은 Import와 Dependency Graph를 통해 이런 Boundary를 강제합니다. Performance를 크게 악화시키던 Pattern을 Architecture를 통해 구조적으로 제거한 사례입니다.

나머지 Dune의 세부 내용보다 중요한 것은 여러분 자신의 Agent-friendly Framework가 매우 강력할 수 있다는 사실입니다. 팀의 가장 좋은 엔지니어들이 가진 Tribal Knowledge와 경험을 Framework에 Encoding할 수 있습니다.

과거에 Style Guide와 Code Review, 엔지니어가 다른 엔지니어에게 남기는 Comment에 있던 지식을 추출해 Framework와 Codebase 자체에 기록하는 것이죠. Codebase가 Memory처럼 동작하게 합니다. Codebase는 미래 Agent가 확장하길 바라는 상태의 Materialized Snapshot입니다. 그 상태를 아주 깨끗하게 유지해 다음 Agent가 좋은 Pattern을 이어가도록 해야 합니다.

## 챕터 9. System-wide integration (30:38~36:06)

이 과정에 충분히 시간을 투자하면 Michelin Kitchen이나 Software Factory 같은 것을 구축할 수 있습니다. Codebase, Lint Rules, Diagnostics, Rules, Bugbot, Skills 등 Agent를 신뢰할 수 있게 하는 Layer들이 결합해 높은 Trust를 만듭니다.

잠시 Grokbot Codebase에서 일한다고 상상해보세요. 아주 엄격하게 제한되어 있어 나쁜 코드를 작성하기가 거의 불가능합니다. Context가 거의 없는 Agent나 Reasoning 능력이 높지 않은 Agent도 좋은 코드를 작성할 수 있습니다.

Michelin Kitchen의 비유처럼 Agent와 Bot을 Skill과 Tool로 훈련시키고, 기본적으로 올바른 일을 할 수 있도록 Kitchen을 정리하는 것입니다. 주방에서 요리사나 식기 세척 담당자가 같은 곳에서 계속 걸려 넘어진다면 문제를 해결해 다음 사람은 넘어지지 않게 해야겠죠. Codebase에서도 지식이 많지 않은 Agent가 좋은 일을 할 수 있게 만들어야 합니다.

Grokbot과 Cursor는 함께 흥미로운 역할을 합니다. Grokbot은 제가 Outer Loop라고 부르는 일을 잘합니다. Slack, Datadog, Sentry, PlanetScale 같은 Connector에 연결해 정보를 모으고 그 정보를 이용해 판단할 수 있습니다. 어떤 사람은 이것을 Company Brain이라고 부르지만 그렇게 정교한 것이 꼭 필요하지는 않다고 생각합니다. Agent는 Tool 사용을 잘하니까요.

Grokbot에 이런 Tool을 연결하고 Cloud Agent를 자동으로 시작하게 만들면 Software Factory에 엄청난 Infrastructure가 꼭 필요한 것은 아닙니다. 그런데 저는 그 용어를 별로 안 좋아하니 지우겠습니다. 여러분만의 Personal Michelin Kitchen을 만들 수 있습니다.

Grokbot Routine으로 Slack Thread나 Sentry Alert를 구독하고 자동으로 작업을 시작할 수 있습니다. Codebase, Rules, Skills를 결합하면 서로 Compounding됩니다. Grokbot이 Outer Loop Event에 자동 반응해 Cloud Agent를 시작할 수 있습니다. Cursor Automations와 SDK로 이런 Agent Infrastructure를 재사용하는 추가 Bot도 만들고 훨씬 복잡한 작업을 수행할 수 있습니다.

우리는 Cursor에서 Bug Report를 자동 Reproduce하고 Pull Request를 자동 생성하는 Automation과 Agent들을 사용하고 있습니다. 이런 요소들이 결합해 Team 전체에 가치를 제공합니다.

다시 Trust Graph로 돌아가 보겠습니다. Trust를 높이는 요소들을 충분히 고민하고 구축하면 Agent를 더 신뢰하게 되고 작업을 Parallelize할 수 있습니다. 팀의 모든 Engineer와 Builder가 Agent Infrastructure 위에 더 많은 것을 만들고 높은 품질의 코드를 생산할 수 있도록 도울 수 있습니다.

## 챕터 10. Closing thoughts on trust (36:06~37:50)

마지막으로 보여드리고 싶은 Slide가 있습니다. 제가 강연에서 단 하나만 가져가길 바란다면 바로 이것입니다. 높은 Trust의 Environment를 만드는 활동들입니다. Agent를 교정하거나 개입할 때마다 이 다섯 가지 요소를 생각하고 어느 단계에서 문제를 해결하는 것이 가장 효과적인지 고민하세요.

이 순서를 추천합니다. 먼저 Codebase, Architecture, Data Structure를 통해 Bad Pattern을 구조적으로 불가능하게 만드세요. 아니면 Static Analysis를 살펴보세요. 그 위에 Rules, Bugbot, Skills를 쌓습니다. Skill을 통한 Code Quality에도 투자하면 Environment 자체를 충분히 신뢰할 수 있게 되어 Agent를 더 자유롭게 일하게 할 수 있습니다.

저는 Grokbot Codebase를 위해 여기에 정말 많은 시간을 투자했습니다. 이것이 비결입니다. 사실 비밀도 아닙니다. 많은 노력이 필요한 일이죠. 강연이 유용했길 바랍니다. X에서 연락해주세요. 제 Handle은 끝에 e가 들어가는 potato입니다. 여러분도 자신만의 Michelin Kitchen을 구축하면서 즐겁고 성공적인 경험을 하길 바랍니다. 시청해주셔서 감사합니다.
