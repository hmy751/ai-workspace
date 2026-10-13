# Lauren 원자료 조사: 강연, pstack, 실제 검증 계약

2026-10-13 KST 조사. 목적은 Lauren이 실제 공개한 작업 방법을 확인하는 것이다. Workspace의 새 체계나 채택안을 제안하는 문서가 아니다. 설치·스킬 실행·제품 코드 변경·커밋은 하지 않았다.

## 먼저 확인된 답

- 발표자는 **Lauren Tan**, 공개 handle은 **poteto**다. 공식 플러그인의 이름은 **pstack**이다. 로컬 번역의 `PotatoOnX`, `PAC`는 검증된 공식 표기로 사용하지 않는다. 다만 원음에서 `PAC`가 무엇을 가리켰는지까지 이번 조사로 확정하지 않았다.
- **구현 전 설계가 있다.** `Feature`의 책임자는 설계·검토·검증을 소유하고 구현을 위임한다. `architect`는 호출자가 쓸 방식부터 타입·시그니처·모듈 경계를 만들고 복수 설계안을 비교한다. 제품 조건만 주고 설계를 구현자나 사후 reviewer에 전부 맡기는 계약이 아니다.
- **Feature Map 생성물과 유지 절차가 공개되어 있다.** 프로젝트별 검증 스킬, 기능별 Markdown, 사용자 경로·명령·관측 결과의 예제까지 확인했다. 강연의 내부 Control Glass 원본 CLI를 공개 배포물로 확인한 것은 아니다.
- **리뷰와 실행 검증이 구별된다.** `interrogate`는 읽기 전용 복수 모델 리뷰와 lead의 판단을 반환한다. `Shipping`은 코드 작성자가 아닌 별도 agent가 PR별 실제 화면/명령을 실행해 판정하게 한다. 일반 Feature의 모든 변경이 같은 Shipping 절차를 자동 수행한다는 뜻은 아니다.
- **구조·검사·스킬은 다른 책임이다.** 공개 `correct`는 반복 실수를 architecture, types, lint/CI, tests 순으로 처리하고 판단이 필요한 문서·규칙을 마지막에 둔다. 실제 계획 검사기 `check-plan.mjs`도 공개되어 있다. Dune의 제품 코드와 import 검사 구현은 이번 범위에서 확인하지 못했다.
- README의 “계획은 기본이 아니다”와 구체적인 선행 설계·큰 작업용 계획 양식은 함께 읽어야 한다. 현재 공개본에는 PR별 계획 산출물과 명시적인 실행 개시 조건이 있다.

## 출처와 버전 기준

이하 GitHub 링크는 별도 표시가 없으면 공식 `cursor/plugins` 저장소의 **commit `997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102`**, **pstack `0.15.21`**을 가리킨다. commit 시각은 **2026-10-12 17:53:26 UTC**, 조회일은 **2026-10-13 KST**다. GitHub API와 고정 commit의 raw 본문으로 확인했다. 검색엔진의 `main` 화면은 이전 README를 보여주기도 했으므로 최종 설명은 고정본을 기준으로 했다.

[플러그인 metadata](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/.cursor-plugin/plugin.json)는 이름 `pstack`, 작성자 `Lauren Tan`, 버전 `0.15.21`을 명시한다. 짧은 원문은 `"name": "Lauren Tan"`이다. [최초 공개 PR #73](https://github.com/cursor/plugins/pull/73)의 작성자는 `poteto`, 생성은 2026-05-23 01:58:17 UTC, merge는 같은 날 21:20:39 UTC, merge commit은 `1fcd4d626199fd8c018c9aa499e2153782a89cf7`이다. 이것은 저자와 공개 계보의 근거이며 강연 당시 버전의 근거는 아니다.

### 강연 원출처 연결의 확인 범위

| 자료 | 확인한 사실 | 남은 한계 |
|---|---|---|
| [GitHub poteto 프로필](https://github.com/poteto) | 표시 이름 lauren, X `@poteto`와 React compiler 관련 자기소개를 직접 확인. 원문 `Software Engineer @xai-org & @react compiler core team`. 조회일 2026-10-13. | 프로필은 현재 자기소개다. 특정 강연 날짜나 당시 소속을 증명하지 않는다. |
| [YouTube 재업로드](https://www.youtube.com/watch?v=NjoZoUm85x0) | YouTube 공개 player/oEmbed metadata에서 제목 `How I Shipped 2000 PRs Last Month`, uploader Raner, 2282초, 공개 시각 2026-09-21 18:54:58 -07:00 확인. 설명란이 아래 X 글을 원출처로 연결한다. | Lauren 공식 채널이 아니다. 업로드일을 실제 발표일로 쓰지 않는다. 영상 전체를 원음 대조하지 않았다. |
| [설명란이 지목한 Lauren의 X 글](https://x.com/poteto/status/2102050467505430555) | 재업로드 설명란의 원문 `Source:` 뒤 링크가 이 주소다. | 직접 조회가 403으로 실패했다. 본문·첨부 영상·게시 시각을 직접 확인하지 못했다. 연결 경로 확인과 최초 영상 검증은 구별한다. |
| [공식 Maven 강연 안내](https://maven.com/p/e23d9c/how-cursor-turned-ai-agents-into-better-engineers) | 2026-08-12, 60분, Lauren Tan 발표. 안내문이 Cursor 내부 framework의 공개명이 pstack이라고 명시한다. 원문 `now open sourced as pstack`. 챕터에 verification/feature map, pstack, Dune가 있다. | 제목·길이가 다른 별도 강연이다. Workspace의 38분 강연과 동일 원본으로 합치지 않았다. 이 페이지는 안내문이며 전체 실연을 확인한 증거는 아니다. |

출발점은 [03 전체번역](../source/lectures/03_Agent_신뢰_강연_전체번역.md)과 [04 상세정리](../source/lectures/04_Agent_신뢰_강연_상세정리.md)다. 04는 실제 구현이 아닌 추가 예시를 포함한다고 스스로 명시한다. 따라서 그 안의 YAML Feature Map, CLI 폴더 구조, React/Next.js 적용 예시는 Lauren의 원본 계약 근거에서 제외했다.

## 요구 이해와 구현 전 설계

### README의 계획 문장을 읽는 범위

[pstack README](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/README.md), `why are there no planning skills?`의 짧은 원문은 **“the best spec is code.”**다. 해당 절은 Cursor plan mode를 사용할 수 있고 `poteto-mode`가 계획을 다루지만 기본값은 아니라는 설명이다. 이것만으로 “설계하지 않는다”, “계획 문서가 없다”, “Spec을 쓰면 안 된다”는 결론을 낼 수 없다. 같은 공개본의 실제 계약을 아래에서 확인했다.

### Feature playbook: lead가 설계하고 구현을 위임

[Feature 본문](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/poteto-mode/playbooks/feature.md)의 원문은 **“You own the design. Plan, review, verify.”**다. 영향받는 subsystem을 `how`로 이해하고 `architect`로 설계안을 탐색한 뒤 위임한다. 입력에는 파일 범위, 이름 붙인 데이터 형태와 이를 조직하는 구조, 성공 기준이 들어간다. 구현 형태가 여러 개 가능하면 `arena`로 비교하게 한다. 이후 해당 사용자 표면에서 검증하며 불확실하거나 다른 표면에서 확인한 결과는 통과가 아니다. 설계가 논쟁적이면 shipping 전에 `interrogate`를 쓴다.

### architect: 계약은 호출자 사용법과 타입 스케치

[architect 본문](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/architect/SKILL.md)의 원문은 **“The synthesized sketch is the contract.”**다. 기존 시스템을 먼저 이해하고, 소유권·계층을 바꾸면 기존 이유도 조사한다. 구조가 다른 후보를 최소 두 개 만들고 합성한다. 기본은 구현으로 진행하며, 사람의 사전 확인은 호출자가 요청하면 들어간다. 구현 중 계약을 벗어나는 변경은 묵살하지 않고 드러낸다. 같은 형태의 마찰이 반복되면 스케치를 다시 만든다. 작은 작업의 출력은 타입·시그니처 파일, 큰 작업은 모듈 지도와 타입 정의이며 이유 문서가 함께 간다.

[rationale template](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/architect/references/rationale-template.md)의 원문은 **“The caller's experience is the spec.”**다. Problem, Usage, Shape, Synthesis decision, Tradeoffs, Alternatives, Open questions, Next implementation step을 요구한다. Usage에는 사용자가 읽을 quickstart와 현실적인 호출부 2~3개를 먼저 적고 타입을 그로부터 도출한다. 호출 경험과 타입이 다르면 타입을 사용법에 맞춘다. 여기의 spec은 별도 Spec/Ticket 문서 체계를 선언한 용어가 아니다.

### 큰 작업 계획: 공개 양식과 실제 검사기가 있음

[Multi-phase plan](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md)의 원문은 **“The plan is the deliverable. Do not implement.”**다. 명백한 1~2파일 변경이면 계획을 생략한다. 큰 작업에서는 prototype 근거, PR 의존 관계·파일 범위·구현·관측 결과·unit/live/perf 확인·review gate·merge 조건을 쓴다. PR별 live 검증에는 구체 시나리오·스크린샷·통과 조건을 가진 10개 lane을 요구한다. 상호작용 변경은 사람이 영상·스크린샷을 보고 merge 전 검토한다. 계획 파일과 검사 결과를 반환한 뒤 명시적인 실행 지시를 기다린다. 이는 이 playbook의 강한 계약이며 모든 작은 작업의 기본 절차로 일반화할 수 없다.

[check-plan.mjs](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/poteto-mode/scripts/check-plan.mjs)는 실제 공개 코드다. 호출 형태는 `node check-plan.mjs <plan.md>`. 제목·절 순서, PR별 필수 블록, lane 1~10, 증거 경로·통과 문구, perf 항목과 review gate 구성을 검사하고 문제 수에 따라 종료 코드를 반환한다. 본문을 읽었지만 실행하지 않았다. **이 검사는 계획의 형식과 일부 명시 항목을 검사하며, 기능의 의미적 정확성이나 실제 증거 존재를 증명하지 않는다.**

## 검증 스킬과 Feature Map의 실제 공개 계약

### 생성 입력과 산출물

[create-verification-skill](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/create-verification-skill/SKILL.md)의 원문은 **“A generated skill that was never executed is a draft, not a deliverable.”**다.

입력은 제품 저장소의 실제 사용자 표면, 실행법·seed/auth, 기존 harness, 관측 가능한 증거, 인스턴스 격리 조건이다. 저장소에서 알 수 없는 것만 사용자에게 묻는다. 출력은 다음이다.

```text
.cursor/skills/verify-<app>/
├── SKILL.md
├── features/README.md
├── features/<user-facing-feature>.md
└── 필요하면 실행 가능한 helper scripts
```

위 트리는 공개 지시의 경로를 모아 표현한 것이며 CLI 이름·스크립트 파일명은 고정되어 있지 않다. `SKILL.md`에는 Launch, Doctor, Drive, Evidence, Cleanup, Helpers를 실제 명령과 함께 적는다. 기능은 초기 3~5개를 목표로 한다. 생성 뒤 기능 하나를 실제 실행하고 증거를 남기며 정리 후에도 증거가 남았는지 확인해야 한다. 내부 setter나 test-only endpoint로 실제 사용자 경로를 대신하지 않는다. 대체 환경에서만 확인한 설정 단계는 실제 대상에서 미검증으로 남긴다.

### 공개된 Feature Map 본문 예제

[예제 README](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/create-verification-skill/references/feature-map-example/README.md)는 Notes 앱 검증 지도의 baseline·구동 관례·증거/skip 기준과 기능 색인이다. 원문 **“Keep implementation details out of the map.”** 기능 파일에는 사용자 동작, 안정적인 핸들, 전제 상태, 명령, 관측 가능한 증거를 둔다. 각 파일의 네 H2는 `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, `Gotchas`다. 사용자 경로 중 하나를 건너뛰고 다른 경로의 통과로 대신하지 않는다.

[create-note 예제](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/create-verification-skill/references/feature-map-example/create-note.md)의 원문은 **“A save status alone is insufficient proof.”**다. 버튼·키보드·CLI 진입, 입력과 저장, 취소, 목록으로 돌아가 다시 열어 영속성을 확인하는 단계가 있다. 각 행동에는 `control-notes` 명령과 관측 결과가 짝지어진다. 증거 파일은 ARIA snapshot과 screenshot이며 데이터 정리와 증거 보존을 구별한다. `control-notes`는 이 예제의 인터페이스 이름이다. 해당 이름의 완성된 CLI 구현이나 Notes 제품 배포물을 확인한 것은 아니다.

[search 예제](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/create-verification-skill/references/feature-map-example/search.md)의 원문은 **“Wait for the results list or empty status, not a fixed sleep.”**다. toolbar·키보드·CLI 진입, 제목/본문 일치, 결과 열기, 검색 결과 없음, 검색어 지우기를 구분한다. CLI에는 JSON과 종료 코드, UI에는 query·앱 식별·결과가 드러나는 증거를 요구한다. 입력창에 focus가 있으면 shortcut이 다른 행동을 하는 함정도 문서화한다.

### 갱신은 source와 실제 앱을 모두 대조

[maintain-verification-skill](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/maintain-verification-skill/SKILL.md)의 원문은 **“Never edit product code during a run”**이다. 대상으로 삼을 검증 스킬을 찾고 색인을 정리한다. 기능별 읽기 전용 agent는 소스 진입점·문서 drift·실행 recipe를 반환한다. coordinator가 실제 앱을 구동하며 모든 기능을 최소 한 번 확인한다. 소스가 깨끗해도 live pass는 필요하다.

수정 범위는 검증 스킬 자체 디렉터리다. 설명이 틀리면 doc drift, 앱은 작동하지만 구동 못 하면 harness gap, 실제 앱이 깨졌으면 product gap으로 보고한다. 마지막 경우 문서를 바꿔 정상처럼 만들지 않는다. 결과는 `clean`/`changed`/`blocked`; 변경은 입증된 보정 PR 최대 하나다. 도달 불가능 판정에는 실제 시도한 경로와 부족한 전제조건이 필요하다. 실행 메모는 scratch에 두며 commit하지 않는다.

### 개발·버그 수정에서 언제 쓰는가

[검증·shipping 공식 가이드](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/docs/guide/06-verify-and-ship.md)의 원문은 **“State the finish condition up front”**이다. 첫 요청부터 종료 조건을 주고, 변경된 실제 표면에서 증명한다. 예컨대 CLI 변경은 실제 명령, 저장 변경은 쓴 값 재조회, 성능 변경은 전후 profile이다. 프로젝트 스킬을 만들고 나면 구현/재현 요청에 `verify-<app>`를 지정한다. 같은 임시 스크립트를 반복 작성하면 작은 control CLI로 만들라고 한다. 풍부한 help, 조합 가능한 명령, JSON 등 기계용 출력이 제시되어 있지만 보편적인 CLI schema는 아니다.

가이드는 map 유지 실행을 매일 권장하고 scheduled automation을 이상적으로 제시한다. 반면 **생성 스킬 본문은 사용자가 물을 때만 cadence를 제안**하게 한다. 설명용 가이드의 권장 주기와 호출 스킬의 행동 조건을 구별해야 한다. 설치만으로 매일 자동 실행된다고 확인한 근거는 없다.

[Bug fix playbook](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/poteto-mode/playbooks/bug-fix.md)의 원문은 **“Unit tests show branch behavior, not bug absence.”**다. lead가 matching control surface에서 먼저 재현하고, 관측으로 원인 후보를 제거한다. 원인 mechanism을 확인한 뒤 설계·구현 위임으로 간다. 수정 후 같은 표면에서 원래 재현이 사라졌는지 확인한다. 저렴한 local test 경로가 있으면 failing-test-first를 쓰고, 비싸거나 integration이 무겁거나 불명확하면 생략 이유를 남긴다. 코드 리뷰·단위 테스트·실제 재현은 같은 확인으로 취급되지 않는다.

## 리뷰·독립 검증과 실행 도구의 경계

### 리뷰는 판단 산출물, shipping 검증은 별도 실행 판정

[interrogate](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/interrogate/SKILL.md)의 원문은 **“The deliverable is a synthesized verdict. Do NOT auto-apply changes.”**다. 사용자 요구·commit·PR 설명·코드로 의도를 한 문단에 정하고, 같은 입력을 모델별 읽기 전용 reviewer에게 준다. lead는 결과를 합친 뒤 Act on / Consider / Noted / Dismissed로 판단한다. 여러 모델의 동의는 신호지만 단독 발견도 읽으며, 합의·불일치를 보고한다. 결과만으로 자동 수정하는 스킬이 아니다.

[Shipping](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/poteto-mode/playbooks/shipping.md)의 원문은 **“Safe means a verdict from an agent that did not write the code.”**다. PR마다 별도 cloud agent가 parent와 head에서 matching control skill로 실제 기능을 확인한다. CI green과 bot approval 자체는 이 판정이 아니다. 판정은 PASS / PASS+NOTES / FAIL이며, 검증된 연속 stack만 아래부터 처리한다. 판정 당시 SHA·base·patch-id를 기록하고 변경 후 여전히 같은 patch인지 확인한다. 이 문서는 merge 요청 이후 절차이며 read-only 리뷰 요청의 권한까지 확대하지 않는다.

### 공개 control-ui/control-cli와 내부 Control Glass를 동일시하지 않음

[cursor-team-kit의 control-ui](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/cursor-team-kit/skills/control-ui/SKILL.md)의 원문은 **“First reuse the repo's own Playwright, browser, or Electron harness if it exists”**다. 기존 도구를 우선 쓰고 없으면 로컬 웹/Chromium debug port 기반 harness를 만든다. 앱 식별, 한 번 행동 후 다시 관측, 화면·접근성·profile 수집 방법이 있다. 이는 범용 Markdown 절차와 짧은 코드 예제이며, 모든 앱을 지원하는 완성 CLI binary를 배포한다고 쓰여 있지 않다.

[control-cli](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/cursor-team-kit/skills/control-cli/SKILL.md)의 원문은 **“Use a repeatable local harness to exercise an interactive CLI”**다. 기존 test/demo harness를 우선하고 없으면 격리한 tmux/PTY로 입력·화면·prompt·종료를 제어한다. profile과 전후 transcript를 수집하는 recipe도 있다. 앱별 명령·경로·프롬프트를 발견해야 하며, 이름만 같은 내부 도구를 그대로 제공하는 계약은 아니다.

### Benny는 공개된 별도 자동화 사례

[Benny reproduce-and-fix-issues](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/automations/benny/skills/reproduce-and-fix-issues/SKILL.md)의 원문은 **“No confirmed repro means no authored fix.”**다. 외부 configuration, trusted triage marker, control adapter와 완성 map이 있어야 실행한다. 보고된 경로를 두 번 실제 UI에서 재현하고, media reviewer가 증거에 구별되는 실패 상태가 보이는지 판단한다. 기존 fix artifact가 있으면 검증으로 전환하며 경쟁 수정하지 않는다. 수정은 근거·범위·예산 조건을 만족한 경우만 수행하고 전후 증명 후 draft PR을 연다. merge/deploy는 이 workflow에서 하지 않는다. 일반 `poteto-mode`와 PR 상태가 다른 별도 계약이다.

[Benny Feature Map 예제](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/automations/benny/skills/reproduce-and-fix-issues/references/feature-map.example.md)는 **“These features belong to a fictional task app.”**라고 명시한다. map을 pack 밖에 두고 configuration에서 경로를 지정해 refresh가 덮어쓰지 않게 한다. 사용자 진입, adapter action, stable selector, 확인할 상태·전제·증거·함정을 적는다. 이는 실제 Cursor/Grok Bot Feature Map 유출본이나 완제품 map이 아니다.

## codebase as memory를 구체화하는 공개 자료와 미공개 경계

### 강연에서 한 주장

로컬 전체번역의 08:38~13:13은 Control Glass를 CDP 기반 앱 실행·trace 수집 skill로 설명한다. 반복 사용 CLI와 Feature Map을 skill directory에 두고 후자를 automation으로 유지한다고 한다. 13:13~30:38은 agent가 열린 파일의 패턴을 복제하므로 architecture·types·static checks로 잘못된 경로를 막고, rules/skills를 보조층으로 둔다는 설명이다. Dune의 구체 예는 feature co-location과 Electron main/renderer import 경계다. 이 부분은 **제공된 번역에서 확인한 강연 주장**이며, 내부 구현을 실행하거나 독립 검증한 사실은 아니다.

### 공개 구현 방법은 correct와 검사 코드에서도 찾을 수 있음

[correct](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/correct/SKILL.md)의 원문은 **“Write docs or agent rules last, only for judgment calls.”**다. commits·reverts·review comments·지침·workaround comments에서 두 번 이상 나온 실수 유형을 찾는다. 상태 소유자 하나, 지원 경로 하나, 잘못된 import 차단, authoritative source 하나, 오래된 복제 대상 삭제를 먼저 시도한다. 이후 타입, 수정 위치를 알려주는 lint/CI, 동작 테스트를 사용한다. 실제 과거 실수에서 새 검사가 실패함을 확인하고 local/CI에서 같은 명령을 쓴다. agent 지침에는 규칙과 이를 강제하는 장치의 대응표를 남긴다. 이것은 문서 지시이며 특정 제품에 이 효과가 실제 발생했다는 측정값은 아니다.

[encode-lessons-in-structure](https://github.com/cursor/plugins/blob/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)의 원문은 **“If the fix is structural, only use the structural fix.”**다. 판단을 코드로 만들 수 없다면 지시를 더 잘 보이게 하고 실패 예를 추가한다. 따라서 모든 판단을 lint로 바꿀 수 있다는 주장도, 문서를 없애라는 주장도 아니다.

### 확인하지 못한 것

| 항목 | 현재 판정 | 다음에 필요한 자료 |
|---|---|---|
| `PAC`와 `pstack`의 정확한 동일성 | pstack의 저자·공개 원천은 확인. 번역 PAC의 원음 대응은 미확인. | X 원영상 또는 발표 slide의 해당 표기. |
| Control Glass의 정확한 명령·출력 schema·구현 | 강연 주장만 확인. 공식 공개물에서 해당 이름의 구현은 찾지 못함. | 작성자 공개 repo/docs 또는 실제 CLI help·코드. |
| Cursor/Grok Bot의 실제 Feature Map 전체 | 범용 생성 계약과 Notes/Benny 예제는 공개. 실제 내부 map은 확인 못함. | 공개된 실제 프로젝트 map, 유지 실행 diff와 증거. |
| Dune 구현·lint/CI import 검사 | 강연·Maven 안내에서 명칭을 확인. 이번에 조사한 공식 plugin tree와 저자 공개 경로에서 제품 구현은 확인 못함. | Dune 공식 source·설계 문서·검사 코드. 공개되지 않았다고 전면 단정하지 않는다. |
| 회사의 요구 정의·Spec/Ticket 운영 전체 | 초기 종료 조건, 설계 rationale, PR별 plan, 선택적 tracker 연결은 확인. 별도 전사 Spec/Ticket schema나 승격 규칙은 확인 못함. | 실제 제품 개발 사례의 요구 입력부터 PR까지 연결된 기록. |
| 공개 스킬의 효과·내부 사용 결과 | 작성자 공개 지시와 일부 실행 검사 코드의 본문을 확인. | 실제 실행 기록·eval·제품 전후 증거. 이번 조사에서는 설치/실행하지 않음. |

## 이번 기록의 검증 범위

- 검색 결과는 원천 찾기에 사용하고 핵심 사실은 공식 GitHub의 본문·고정 commit, GitHub API, YouTube 공개 metadata, Maven 주최 페이지로 확인했다.
- 외부 긴 원문·영상·repo 전체를 파일로 복제하지 않았다. 소스별 짧은 발췌와 200단어 이내의 파생 설명, 원문 재접근 링크만 남겼다. 본문 코드 블록은 생성 경로 관계를 재구성한 표시이며 원본 CLI 배포물은 아니다.
- 변경 파일은 이 기록 하나다. 기존 `source/`와 Workspace의 `current/`, 전역 지침, 제품 코드, 설치 상태는 변경하지 않았다.
