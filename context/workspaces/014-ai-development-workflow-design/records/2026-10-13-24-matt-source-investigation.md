# Matt Pocock 자료 조사 — 강연의 권고와 공개 skill의 실제 계약

2026-10-13 조사. 이 문서는 설계 근거를 보존하는 기록이며 새로운 개발 체계를 채택하지 않는다. 제공된 강연 번역·skill 번역, 공식 skills Git 저장소, Matt 명의 AIHero 설명을 대조했다. Git 저장소는 임시 디렉터리에서 읽었으며 skill을 설치하거나 실행하지 않았다.

## 핵심 확인

**Matt의 자료는 구현과 상세 표준 검토를 분리할 근거는 제공하지만, 앞선 알림 설정 예시 전체를 완성된 운영 계약으로 정당화하지는 않는다.** 특히 사전 테스트 경계 합의가 구현 입력에서 빠졌고, 검토자의 직접 수정·최종 앱 확인·Main 완료 판정은 강연의 권고와 공개 구현의 빈칸을 구별하지 않은 채 연결됐다.

- 강연은 상세 coding standards를 별도 reviewer에게 주고 reviewer가 직접 수정·commit하라고 권한다. 그러나 공개 `code-review`는 Standards·Spec 두 보고서를 반환한다. 자동 수정과 commit 단계가 없다.
- 구현자가 품질 관련 정보를 전혀 읽지 않는 구조가 아니다. `implement`는 `tdd`를 호출하며, `tdd`에는 테스트 품질·mock 사용·독립적인 기대값·사전 seam 합의가 들어 있다. 인터페이스 형태가 문제이면 `codebase-design`도 읽는다.
- Spec은 기존 대화에서 결정한 것을 합성한다. 모듈·인터페이스·스키마·API·테스트 결정을 담을 수 있으며, 단순한 목표·결과만 담는 문서로 한정되지 않는다. 반대로 모든 함수 이름이나 내부 분할을 고정하라는 계약도 없다.
- `implement`의 review-before-commit과 `code-review`의 committed-diff-only는 연결 공백이 있다. 공식 설명도 이를 인정한다. 사용 가능한 구현·검토 계약을 살펴봤다는 것과 실제로 정상 작동하는 흐름을 검증했다는 것은 다르다.
- 별도 `implement-spec`은 통합 branch에서 review한 뒤 **한 implementer subagent**에게 수정을 맡긴다. 강연의 “같은 reviewer가 직접 고친다”를 그대로 구현한 흐름이 아니다.
- Spec 자동 갱신, 모든 작업의 실제 앱 최종 확인, 공통 최종보고 서식, 자동 retro 반영까지 이어지는 단일 계약은 확인되지 않았다.

아래의 항목별 근거가 이 요약의 해석 범위를 제한한다.

## 자료의 지위와 판본

| 자료 | 이번에 확인한 범위 | 사용 한계 |
| --- | --- | --- |
| 제공 강연 번역 | [PR 병목 전체 번역](../source/lectures/01_PR_병목_강연_전체번역.md), 특히 11:20–16:17 / 16:17–22:24 | 사용자 제공 스크립트의 번역. 첫머리에서 01:15–01:48 누락을 밝힌다. [원영상 재접근 URL](https://www.youtube.com/watch?v=LlgiOCmFG_w)은 이번 web 도구로 본문·자막을 재취득하지 못했으므로 영문 발화와 번역 정확도는 독립 검증하지 못했다. |
| 제공 skill 번역 | [설계](../source/lectures/codebase-design.ko.md), [review](../source/lectures/code-review.ko.md), [구조 개선](../source/lectures/improve-codebase-architecture.ko.md), [PR](../source/lectures/pr.ko.md), [retro](../source/lectures/retro.ko.md) | 출발 자료로 모두 읽었다. 번역 파일 자체에는 원본 Git commit이 없다. 제공 사본 전체를 아래 과거 commit과 동일한 판본으로 취급할 수 없다. |
| 과거 기준 | [`068b6e0c62393147daf03530149cdce209c93da8`](https://github.com/mattpocock/skills/commit/068b6e0c62393147daf03530149cdce209c93da8), 2026-08-15 22:24:19 +01:00 | 이전 Ticket 논의의 기준과 비교하는 역사 자료. 이 tree에는 `pr`, `retro`, `implement-spec` skill이 없다. |
| 현재 공개 구현 | [`49dd158d1076134a641b33efb035946536778336`](https://github.com/mattpocock/skills/commit/49dd158d1076134a641b33efb035946536778336), 2026-10-09 11:56:49 +01:00. 10월 13일 clone 당시 HEAD | 아래 GitHub 링크는 이 commit으로 고정했다. 실제 에이전트 실행 결과가 아니라 Markdown skill 계약을 확인했다. |
| 공식 설명 | [AIHero skills](https://www.aihero.dev/skills)와 각 skill 설명 본문 | 현재 동작 의도·사용상 한계 설명. 여러 페이지는 Updated Aug 24, 2026을 표시하지만 내용과 구현의 최신성이 항상 맞지는 않는다. 구현 판정은 고정한 Git 파일을 우선한다. |

현재 공개 구현은 강연의 발표 시점과 같은 버전이라는 증거가 없다. 제공 번역에 있는 `GLOSSARY.md` 명명은 과거 기준의 `CONTEXT.md`와도 다르다. PR·retro의 engineering 승격은 [2026-09-24 commit](https://github.com/mattpocock/skills/commit/a7d038f6bf7f01b516408e95e2fb56e0b338fa6f), implement-spec의 승격은 [같은 날 별도 commit](https://github.com/mattpocock/skills/commit/24f41cc26d34ffd688e9105b43798a4b446e267d)에서 확인했다.

## 요구·설계·Spec·Ticket은 누가 만드는가

### 인터뷰와 결정 보존

`grill-with-docs`는 `grilling`과 `domain-modeling`을 함께 호출한다. 전자는 AI가 결정 의존관계를 질문으로 구성하고 추천을 제시하되, 환경에서 찾을 수 있는 사실은 조사하고 결정은 사용자에게 확인하게 한다. 미해결 결정이 없고 사용자가 공동 이해에 도달했다고 확인해야 마친다. 후자는 합의한 용어를 즉시 glossary에 반영하고, 되돌리기 어렵고 맥락 없이는 의아하며 실제 대안 사이의 선택인 결정에만 ADR을 제안한다. 모든 합의가 문서에 남는 것은 아니다.

근거: [grill-with-docs L1–7](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/grill-with-docs/SKILL.md#L1-L7), [grilling L6–30](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/grilling/SKILL.md#L6-L30), [domain-modeling L40–74](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/domain-modeling/SKILL.md#L40-L74). 공식 [grill-with-docs 설명](https://www.aihero.dev/skills-grill-with-docs)은 glossary·ADR에 해당하지 않는 결정은 대화에만 남는다고 명시한다. 정밀한 합의가 Spec·Ticket·test까지 빠짐없이 연결되는 추적 장치는 제공되지 않는다.

### 단계별 실제 입력·행동·산출물

| 단계 | 입력과 실제 행동 | 산출물·확정 범위 | 고정 근거 |
| --- | --- | --- | --- |
| 설정 | 기존 repo·tracker·domain 문서를 조사하고 사용자의 tracker와 문서 배치를 확인 | issue-tracker/domain 등의 안내와 steering file의 포인터. 프로젝트별 실행 수단은 이 설정에 의존 | [setup L9–15, L63–118](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/setup-matt-pocock-skills/SKILL.md#L9-L118) |
| `to-spec` | 현재 대화와 코드 이해를 합성. 새 인터뷰는 하지 않지만 **테스트 seam은 먼저 스케치하여 사용자에게 확인** | 문제·해결·상세 user stories·Implementation Decisions·Testing Decisions·범위 밖·기타를 담은 issue. `ready-for-agent` 표기 | [to-spec L7–75](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-spec/SKILL.md#L7-L75) |
| `to-tickets` | 대화·plan·spec, 또는 전달한 issue 본문과 comments. 필요하면 코드 조사·prefactoring 탐색. 작은 수직 결과와 blocking 관계를 제안해 사용자 승인까지 조정 | local이면 Ticket별 파일, tracker이면 issue별 Ticket. 결과·AC·blocking을 갖고 부모 issue는 수정·종료하지 않음 | [to-tickets L15–105](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-tickets/SKILL.md#L15-L105) |
| `implement` | 사용자가 준 spec/ticket. Ticket 참조를 tracker에서 가져와 제목 확인. 합의한 seam에서 가능하면 `tdd` 호출 | 코드·테스트 변경, 반복 typecheck와 개별 test, 마지막 전체 test suite, `code-review` 호출, 현재 branch commit | [implement L7–17](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/implement/SKILL.md#L7-L17) |
| `implement-spec` | Spec·Ticket task graph·blocking 관계. 선택적으로 공통 탐색 notes. 각 ready Ticket은 별도 worktree의 implementer가 `tdd`로 수행 | 하나의 integration branch. 모든 Ticket 합류 뒤 review, **별도 implementer 하나가 지적 수정**. tracker 방식에 따라 PR ready 또는 Ticket 해소 | [implement-spec L7–40](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/implement-spec/SKILL.md#L7-L40) |

**Spec의 구체성:** `Implementation Decisions`에는 만들거나 바꿀 모듈, 바뀔 인터페이스, 개발자의 기술 설명, 아키텍처 결정, 스키마, API 계약, 구체적 상호작용이 들어갈 수 있다. `Testing Decisions`에는 외부 행동을 검사한다는 원칙, 테스트할 모듈, 기존 유사 테스트를 담는다. 파일 경로·코드 스니펫은 일반적으로 제외하되, prototype에서 나온 state machine·schema·type shape처럼 결정 자체를 더 정확히 표현하는 부분은 예외다. 이 계약은 “모든 함수·구현순서를 사전에 고정”도 “내부 설계는 모두 구현자에게 맡김”도 아니다. 이미 한 결정을 전달한다는 뜻이다. 위 `to-spec` L43–65가 근거다.

**Ticket의 구체성:** 한 Ticket은 독립적으로 시연·검증 가능하고 새 context window 하나에 들어가는 수직 결과다. 광범위한 기계적 리팩터링은 예외로 expand–migrate–contract를 쓰며, 개별 batch가 green일 수 없으면 마지막 integrate-and-verify Ticket에서 green을 약속한다. 함수목록·파일목록을 고정하는 템플릿은 없다. 위 `to-tickets` L29–40, L69–105가 근거다.

**언제 생략·갱신하는가:** 공식 [to-spec 설명](https://www.aihero.dev/skills-to-spec)은 여러 세션에 걸친 작업을 주 사용처로 보고, 작은 작업은 대화에서 곧바로 implement할 수 있다고 한다. `to-prd`는 v1.1에서 `to-spec`으로 바뀐 이름이다. Spec을 구현 중 동기화하는 장치는 없으며, 지속할 학습은 glossary·ADR에 남기라고 설명한다. 따라서 우리의 지속 Spec·current 관리 규칙을 Matt의 동기화 계약이라고 주장할 수 없다. 이는 같은 내용을 가진 [고정 docs L24–63](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/docs/engineering/to-spec.md#L24-L63)에서도 확인된다.

## 구현자에게 실제로 들어가는 설계·테스트 기준

현재 `tdd`는 **red→green** 반복이다. 테스트부터 실패하게 만들고 최소 구현으로 통과시키며 한 번에 한 seam·한 test·한 구현을 진행한다. 기존 `CONTEXT.md`를 쓰던 과거 기준에서도 이 본질은 동일하다. refactor는 구현 loop에서 빼고 review 단계로 보낸다. 원문 최소 발췌: “Refactoring is not part of the loop.” [tdd L34–38](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd/SKILL.md#L34-L38)

구현자는 다음 기준을 받는다. 테스트는 공개 인터페이스의 관찰 가능한 행동을 검사하고, 내부 함수·호출 순서·구조에 결합하지 않는다. 기대값은 구현의 계산을 반복하지 않고 알려진 literal·계산 예제·Spec 같은 독립 근거에서 얻는다. 테스트할 seam을 사용자와 먼저 확인하고 각 seam이 잡는 것과 놓치는 것을 짧게 설명한다. **인터페이스 형태·depth·seam 위치·노출 범위 자체가 문제일 때** `codebase-design`을 호출한다. 따라서 모든 구현 때 설계 자료 전체를 주입하는 것도, 설계 기준 참조를 금하는 것도 아니다. [tdd L10–32](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd/SKILL.md#L10-L32)

구체적 보조 자료의 관계는 다음과 같다.

| 보조 자료 | 실제 기준·예외 | 근거 |
| --- | --- | --- |
| `tests.md` | 실제 interface로 얻은 결과를 확인. `createUser` 뒤 DB를 직접 조회하기보다 `getUser`로 재조회하는 예. 내부 mock 호출 횟수·순서 검사는 부정 예 | [tests L3–77](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd/tests.md#L3-L77) |
| `mocking.md` | 외부 API·시간·난수·일부 filesystem/DB에서 대체 허용. DB는 test DB 선호. 자기 module·내부 collaborator mock은 금지 | [mocking L1–18](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd/mocking.md#L1-L18) |
| `codebase-design` | Interface는 type signature뿐 아니라 불변조건·순서·오류·설정·성능까지 포함. Depth는 호출자가 배워야 할 정보 대비 얻는 행동의 양. 외부 interface를 단순하게 해도 내부 구성·내부 seam은 존재할 수 있음 | [design L14–28, L60–65](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/codebase-design/SKILL.md#L14-L65) |
| `DEEPENING.md` | 프로세스 내부는 직접 합쳐 interface로 테스트. local 대체 가능 의존은 stand-in 사용. 소유한 원격 서비스는 production/test adapter, 외부 서비스는 mock adapter. 깊어진 interface test가 생기면 대체된 얕은 unit test를 쌓아두지 않음 | [DEEPENING L5–37](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/codebase-design/DEEPENING.md#L5-L37) |
| `DESIGN-IT-TWICE.md` | 선택한 후보의 대안 interface를 원할 때만 3개 이상 병렬 설계. 제약·의존·seam을 기술 brief로 전달하고 interface·사용예·숨기는 구현·adapter·trade-off를 비교 | [DESIGN-IT-TWICE L3–44](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/codebase-design/DESIGN-IT-TWICE.md#L3-L44) |

보조 파일의 미묘한 차이도 남아 있다. `mocking.md`의 “자기 module을 mock하지 않음”은 `DEEPENING.md`가 허용하는 소유 원격 서비스의 in-memory adapter와 구별해야 한다. `tdd`의 internals 테스트 금지와 `codebase-design`의 내부 seam 허용도 모든 내부 테스트 금지라는 단일 규칙으로 평탄화할 수 없다. 두 자료가 모든 사례의 경계를 합의해 준 것은 아니다.

공식 [tdd 설명](https://www.aihero.dev/skills-tdd)은 config·wiring·glue·type annotation·단순 CRUD 전달처럼 독립 기대값을 만들기 어려운 작업에 TDD를 적용할지 판정하는 단계가 없다고 인정한다. browser test는 느려 구현 전 red-green에 불리하다는 설명도 있으나, skill 본문이 이를 금지하지는 않는다. 별도 [Day 4 강좌 소개](https://www.aihero.dev/workshops/day-4-feedback-loops-fcqu2)는 backend에는 red-green-refactor, frontend에는 직접 구현을 다룬다고 적는다. **이 소개만으로 비공개 강의의 정확한 prompt·도구·예외를 복원할 수 없다.** 현재 `tdd` 계약과 옛 강좌 소개를 같은 판본으로 합치지 않는다.

## 검토·직접 수정·실제 확인·보고

### 강연의 권고와 공개 구현의 차이

제공 [강연 번역 L69–83](../source/lectures/01_PR_병목_강연_전체번역.md#L69)은 구현자의 탐색·수정·debug context 부담 때문에 상세 standards를 reviewer에게 배치하고, review가 문제를 찾으면 기본적으로 직접 수정·commit하라고 권한다. 불확실한 사항은 comment로 남길 수 있다. 이 권고는 직접 수정 방향의 근거지만, reviewer에게 넘기는 정확한 artifact 계약·수정 후 테스트 순서·수정 권한 충돌·중단 조건·완료 판단자를 제공하지 않는다.

공개 `code-review`의 입력은 기준점에서 HEAD까지의 diff 명령·commit 목록, standards 문서, originating spec이다. 두 하위 agent가 따로 검토하여 Standards는 규칙·hunk, Spec은 Spec 문장을 근거로 지적한다. 최종 산출물은 축별 보고·지적 수·각 축의 가장 큰 문제다. 두 축을 합쳐 순위를 매기지 않는다. **직접 edit·commit·자동 검사 실행·실제 앱 확인 단계는 없다.** 기준점 미지정이면 질문하고, invalid/empty diff면 멈추며, Spec이 없으면 해당 축을 생략한다. [code-review L17–80](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review/SKILL.md#L17-L80)

Standards에는 저장소 문서 외에 Fowler smell baseline이 있다. 문서화된 repo 규칙이 우선하며 smell은 판단 후보이고 도구가 이미 강제하는 항목은 생략한다. 이 baseline은 “품질 문제를 모두 검증하는 실행기”가 아니다. [같은 파일 L34–56](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review/SKILL.md#L34-L56)

공식 [implement 설명](https://www.aihero.dev/skills-implement)은 Ticket 종료·AC 체크·review finding 적용이 내장되어 있지 않다고 적는다. 또한 review가 commit 이전에 실행되지만 review의 `<fixed-point>...HEAD`에는 staged/working-tree 변경이 없어서 해당 변경을 놓칠 수 있음을 명시한다. 이는 고정 skill 두 파일의 순서와 diff 범위를 대조해 확인한 계약 공백이다. 이번 조사에서 실제 재현 실행은 하지 않았다.

공식 [code-review 설명](https://www.aihero.dev/skills-code-review)은 하위 agent 보고를 다시 파일에 대조하는 검증 단계가 없고 지적은 확인할 가설이라고 설명한다. 매번 다시 돌려 무결점으로 수렴한다는 보장도 없다. 문서의 사용자 실패 사례는 Matt가 공개 설명에 수록한 보고이지 이번 조사에서 재현한 실험이 아니다.

### 실행 증거와 사람의 최종 판단

`pr`는 PR 본문의 형식 reference다. 핵심을 보여주는 최소 시각자료, before/after 증거, 되돌릴 수 있는지와 영향 범위를 쓰게 한다. 환경이 있고 시각 변경이면 screenshot, 실행 증거이면 test/console 출력이 좋은 증거다. 그러나 `pr` 본문에는 browser/server 실행 권한·검증 소유자·테스트 환경 준비·모든 변경의 실제 앱 검사 강제·merge 승인 절차가 없다. [pr L12–37, L158–170](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/pr/SKILL.md#L12-L170)

강연은 자동 검사→자동 review→사람 review라는 층과 가역성·영향에 따라 사람 review 강도를 달리하는 판단을 제시한다. [강연 번역 L25–37, L91–117](../source/lectures/01_PR_병목_강연_전체번역.md#L25) 이것만으로 “검토자가 실제 앱의 성공·거절·재시도·재진입을 모두 실행하고 Main이 최종 완료를 판정”하는 구체적 역할 계약은 나오지 않는다.

## Retro와 구조 개선의 실제 종료점

`retro`는 사용자가 지정한 세션 원자료를 읽고, 없으면 현재 세션을 대상으로 환경 개선 후보를 심각도 순서로 제시한다. 새 자동 검사 전에 repo의 기존 check/CI를 읽고, 기계적으로 판정 가능한 위반은 결정론적 검사로, 판단이 필요한 규칙만 `CODING_STANDARDS.md`로 분류한다. 탐색·도구 효율·no-op 지시·정보 접근도 대상이다. 이 파일을 review에서 읽으라는 문장은 명시적이다. 최소 발췌: “this file is read during review, not implementation.” [retro L7–44](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/retro/SKILL.md#L7-L44)

공식 [retro 설명](https://www.aihero.dev/skills-retro)은 후보 제안에서 멈추고 사용자가 고르기 전에는 수정하지 않는다고 분명히 한다. 자동 hook을 설치하지 않으며, 모든 성공 세션에 의무 실행하는 규칙도 없다. 기존 검사들의 장기 효과·오탐을 지속 감시하는 장치는 없다고 인정한다. 따라서 “매 작업 후 자동 학습·기준 갱신”은 별도 설계다. [고정 docs L31–55](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/docs/engineering/retro.md#L31-L55)

`improve-codebase-architecture`는 코드·변경 이력·glossary·ADR을 바탕으로 후보를 탐색해 임시 HTML에 before/after·효과·추천 강도를 보여준다. 사용자가 후보를 고르면 제약·의존·모듈 형태·테스트를 인터뷰하며 필요한 glossary·ADR을 갱신한다. 코드 수정 완료가 이 skill의 종료 산출물은 아니다. [architecture L18–71](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/improve-codebase-architecture/SKILL.md#L18-L71)

## 판본 차이와 남은 미확인

| 항목 | 과거 068b6e0 → 현재 49dd158 | 해석 |
| --- | --- | --- |
| `to-spec` | 주요 절차와 템플릿 유지 | 이전 기준에도 seam 사용자 확인·설계/테스트 결정이 있었다. 이번에 새로 생긴 상세화가 아니다. |
| `to-tickets` | 수직 slice·사용자 승인·wide refactor 예외는 유지. 현재는 source issue의 sub-issue 생성과 native blocking의 본문 생략을 더 명시 | 과거판을 참고했다는 사실만으로 우리 Ticket의 담당·증거·상태 필드가 Matt 원형과 같다고 할 수 없다. |
| `implement` | 현재는 Ticket 참조 fetch·제목 확인과 실제 Skill 도구 호출을 명시 | review 후 commit 순서와 finding 수정 누락은 그대로 남는다. |
| `tdd` | context 파일명 변경, seam별 잡는 것/놓치는 것 설명 추가 | 과거판부터 red-green이며 refactor를 review로 넘겼다. README의 red-green-refactor 표현만 읽으면 틀린다. |
| `code-review` | 현재는 standards 전수 탐색과 foreground 병렬 호출을 더 분명히 함 | 보고서 취합형 계약은 유지. 직접 edit로 바뀌지 않았다. |
| `pr`·`retro`·`implement-spec` | 과거 tree에는 없고 후에 추가·승격 | 제공 5개 skill 번역을 모두 068b6e0 판본으로 묶으면 안 된다. |

확인 방법은 `git show`·`git diff 068b6e0...49dd158` 및 commit별 파일 본문이다. 현재 기본 branch와 관계없는 다른 branch의 commit은 현재 계약의 근거로 사용하지 않았다. 공식 TDD 설명은 seam trade-off 안내가 아직 없다고 말하지만, 현재 SKILL L24에는 이미 추가돼 있다. 웹의 Update 표시나 FAQ 전체를 곧바로 현재 구현 사실로 취급하면 안 되는 사례다.

이번 조사에서는 다음을 확인하지 못했다.

- 강연 시연 환경의 정확한 source commit, reviewer 직접 수정에 쓰인 별도 prompt·harness·재검사·종료 조건.
- 비공개 강좌 `do-work`의 전체 본문과 실제 실행 trace. 공개 소개에는 알림 기능 PRD 사용이 나오지만 그것이 우리의 ‘댓글 알림 설정’ 사례와 같은 기능이라는 근거는 없다.
- 이 skills 조합을 실제 제품에 실행했을 때 규칙을 얼마나 준수하는지, 생산성·품질이 얼마나 개선되는지.
- 어떤 단일 문서가 모든 사람·agent의 작업 상태와 실제 검증 결과를 지속적으로 갱신하는지. 해당 canonical 전체 계약은 조사한 자료에 없다.

## 앞선 알림 설정 인수 예시에서 근거를 분리해야 할 부분

[기록 23](2026-10-13-23-notification-settings-handoff-example.md)은 가상 예시라고 밝혔지만, 아래 연결은 Matt 자료의 실제 계약과 별도 판단이어야 한다.

| 기존 예시 위치 | 조사로 드러난 차이 |
| --- | --- |
| Spec L30–42, 구현자 요청 L60–70 | 테스트할 공개 경계를 무엇으로 정하고 사용자와 언제 합의하는지가 빠졌다. “자동 검사를 추가”만으로 Matt의 implement 입력을 재현하지 못한다. |
| Project 품질 기준 L24–26 | 상세 coding standards를 reviewer에게 집중하는 것은 근거가 있다. 그러나 구현자가 받는 TDD의 품질·설계 discipline까지 제거하면 공개 구성과 달라진다. |
| Ticket L48–54 | 한 Ticket 안에서 구현자→직접 수정 reviewer→Main 완료 판정으로 연결하는 것은 우리의 역할 설계다. Matt Ticket 템플릿은 이 담당·진행·증거 전달을 정의하지 않는다. |
| 검토자 요청 L76–86 | 직접 수정은 강연의 권고에 기대지만, 현재 code-review가 실행하는 일은 아니다. 수정 후 실제 앱 최종 확인까지 같은 reviewer가 소유한다는 근거도 없다. |
| Spec/Project 갱신 L92–95 | 지속 Spec 보존·Project 현재 구조 갱신·Main 책임을 연결한 규칙은 이 Workspace의 설계 후보다. Matt의 Spec 자동 동기화 계약을 옮긴 것이 아니다. |
| 반환물 L68·86 | 변경 상태·명령·환경·미확인 항목을 함께 반환하는 것은 타당성 검토가 필요한 자체 계약이다. Matt에게 공통 최종보고 schema가 있다고 확인하지 못했다. |

여기서의 결론은 해당 자체 판단이 나쁘다는 것이 아니다. **강연의 방향, 공개 skill이 실제 지시하는 행동, 공식 설명이 인정한 공백, 우리가 추가로 정할 책임을 구별해야 이후 설계를 검토할 수 있다.**
