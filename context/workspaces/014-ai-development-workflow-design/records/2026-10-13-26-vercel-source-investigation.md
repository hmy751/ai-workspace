# Vercel 원문·공개 skill 조사

2026-10-13. 설계 채택 전 근거 조사다. Vercel의 내부 운영 설명, 글에 실린 축약 예제, 별도 공개 skill, 외부 고객용 Code Review 제품 문서를 구별했다. 자료를 설치·실행하거나 우리 운영안으로 채택하지 않았다.

**기록 23의 역할 배치와 Project·Spec·Ticket 구성을 Vercel의 실제 방식이라고 설명할 근거는 없다.** 아래 자료는 기준의 내용·적용 시점·검색 경로·검증 종류를 비교할 근거이며, Main·구현자·검토자 인수 체계를 입증한 자료가 아니다.

## 1. 내부 product-design을 설명한 공식 글

[Teaching agents product design at Vercel](https://vercel.com/blog/teaching-agents-product-design-at-vercel), John Phamous, 2026-06-25. 강연 전사가 아니라 공식 블로그다. 구조와 SKILL은 축약 예제라고 명시한다. 본문에 연결된 내부 전체 저장소는 확인하지 못했다.

### 입력·행동·출력 계약

| 모드 | 입력 | 행동·출력 | 사본 위치 |
| --- | --- | --- | --- |
| Shape | 미정 UI의 brief·흐름 요청 | 문제·근거·대안 비교, 흐름·상태·수락기준·위험·미결정. 편집은 별도 요청 | L118 |
| Implement | 구축·수정 요청 | 중요한 제품 선택을 해결하고 범위 내 변경 구현 | L119 |
| Review | 코드·URL·스크린샷 검토 요청 | 소스·렌더링 증거 확인, 영향순 지적과 위치·검증상태·정본·영향·수정안. 편집은 별도 요청 | L120, L199–208 |

순차 에이전트가 아니라 요청 모드다. 구현 전 AGENTS·brief·design·제품 로직을 읽고, 사용자·목적·현재 동작·결과·성공신호·비목표·객체·범위·행동·결과영향·가역성·권한·미결정을 internal brief로 정리한다. 도달 가능한 상태를 매핑한다.

사용자 목표·제약, 검증된 제품 사실, 저장소 정본, 승인된 결정, 인접 사례, 일반 휴리스틱 순으로 판단한다. 구현에도 product-judgment/interface-quality를 적용한다. 기준은 컴포넌트·디자인시스템 등 원래 소유자에게 두고 필요별로 읽는다.

확인은 lint, 화면 크기, 변경 상태, 키보드·포커스·입력, 긴 내용·국제화 등을 포함한다. 소스만으로 시각 검증을 주장하지 않는다.

기준 갱신은 collector의 자료 수집, judge의 검증·미결정, pending packet, 사람 승인, 좁은 목적지의 변경·관련 검사로 나뉜다. eval은 before 수정·rubric 판정·holdout·skill 없는 대조를 설명한다. copywriting-eval은 문구·인터페이스 언어만 평가한다.

짧은 원문: “Do not edit unless asked.” / “Automation ends with the review packet.”

### 다시 확인할 원문 위치

기존 [사본](<../source/lectures/vercel-product-design (1).md>)을 그대로 사용한다. 아래 위치는 그 파일의 줄이다.

| 질문 | 원문 위치 |
| --- | --- |
| root AGENTS·skill-local AGENTS·SKILL 역할 | L21–68 |
| 모드·authority·internal brief | L112–151 |
| 도달 가능 상태·분야별 routing·실제 확인 | L153–180 |
| 기준 변경 권한·rule 추적 | L210–237 |
| lint 본문 예시 | L271–319 |
| eval 평가 범위 | L62, L325–333 |
| 주간 증거 수집·후보 검토·사람 승인 | L335–351, L461–477 |
| repository trigger·reference 형식 | L382–433 |

### 사본과 현재 웹의 차이 확인

공식 웹 HTML의 article 본문과 사본을 비교했다. 공백·문장부호·Markdown 장식을 제거한 유의미한 231개 행 중 제목·작성자 행을 제외한 229개가 웹 본문에 포함됐다. SKILL 94개 행과 lint 18개 행도 같은 방식으로 일치했다. 제목·저자·날짜는 웹 표제에서 별도 확인했다. 바이트 동일성 검사는 아니다. 사본의 큰따옴표와 웹 lint 예제의 작은따옴표 등 표기 차이는 있지만 **조사 질문과 관련된 의미 변경은 발견하지 않았다.**

특히 `copywriting-eval` 범위 문장은 현재 웹에도 있다. 검색 결과 요약에서 생략된 것을 원문 삭제로 해석하면 안 된다. 사본 SHA-256: `e5beaac1e8d0b6c2c0bbefba68c0ca96d088a906a9665848b7a18abab8bf34b4`.

## 2. 기준 원래 소유자의 실제 내용

공식 글이 직접 연결한 [Geist Checkbox](https://vercel.com/geist/checkbox#best-practices)의 현재 본문을 읽었다. 게시·개정일과 commit은 페이지에서 확인하지 못했다. 확인일은 2026-10-13이다.

선택한 컴포넌트의 사용 조건, 동작, 문구, 접근성이 한곳에 있다. 예를 들어 다중 선택·동의 확인에 checkbox를 사용하며 단일 boolean 설정에는 Toggle을 안내한다. 필수 동의 오류는 submit에서 검사하고, 비활성 이유를 Tooltip으로 알리며, 관련 checkbox를 fieldset/legend로 묶는다. 이는 구현자가 컴포넌트를 고르는 시점에 필요한 구체 기준이다.

짧은 원문: “Indeterminate is a visual state, not a third value.”

이 내용은 우리 알림 설정에서 어떤 컴포넌트가 정답이라는 채택 근거가 아니다. 해당 제품의 저장 시점·의미·사용자 기대를 별도로 확인해야 한다. 내부 `product-judgment.md`, `interface-quality.md`, skill-local `AGENTS.md`의 전체 본문을 대신하지도 않는다.

## 3. 별도 공개 agent-skills의 실제 파일

`vercel-labs/agent-skills` 확인 commit: `063bee94c3f4df8453406c830b0a7df0f2860278`, commit 시각 `2026-08-28T13:36:07Z`. 전체 tree 응답은 잘리지 않았으며 `product-design`, `product-judgment`, `copywriting-eval` 경로가 없었다. 공개 저장소 전체에 영원히 없다는 주장이 아니라 이 commit의 조사 결과다.

### web-design-guidelines

[실제 SKILL L14–39](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/web-design-guidelines/SKILL.md#L14)은 매 검토 때 원격 `command.md` 최신판을 가져오고, 지정된 파일을 읽고, 모든 규칙을 대조해 `file:line` 지적을 출력한다. 파일 미지정 시 범위를 묻는다. 39행 skill이며 제품 brief·collector·judge·렌더링 실행 절차는 들어 있지 않다.

짧은 원문: “Fetch fresh guidelines before each review”.

실제 기준인 [command.md](https://github.com/vercel-labs/web-interface-guidelines/blob/434b7f91364665f2f733b310ec54809bf8f37937/command.md)은 `434b7f91364665f2f733b310ec54809bf8f37937`, `2026-10-05T20:49:16Z`로 고정해 읽었다. 접근성·포커스·폼·애니메이션·데이터 크기·탐색·국제화 등 규칙과 파일별 지적 형식이 있다. 예를 들어 L39–49는 입력 타입·붙여넣기·오류 위치·저장되지 않은 변경, L169–191은 출력 형식이다. 독립된 실행기나 브라우저 검증 코드는 이 저장소 tree에서 확인하지 못했다. 짧은 원문: “State issue + location.”

`main`에서 받은 두 파일은 위 commit tree의 Git blob hash와 일치함을 확인했다. 원격 최신 기준을 읽는 이 public skill과 내부 제품별 승인 기준을 같은 버전·같은 authority라고 합칠 수 없다.

### 같은 AGENTS.md 이름도 역할이 다르다

공개 저장소의 [root AGENTS L5–22, L71–79](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/AGENTS.md#L5)은 skill 제작자를 위한 형식·디렉터리·필요시 참조 읽기 안내다. 내부 `apps/vercel-site`의 제품 개발 routing 파일이 아니다. 짧은 원문: “Use progressive disclosure”.

[React SKILL L14–21, L132–149](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/react-best-practices/SKILL.md#L14)은 새 코드 작성·데이터 조회 구현·리팩터링·검토 모두에 성능 기준을 적용한다. 상세 이유·나쁜/좋은 예시는 개별 rule을 읽으며 전체 조합본은 skill 안의 AGENTS.md다. 짧은 원문: “Writing new React components or Next.js pages”. 이는 상세 기준을 검토자에게만 집중시키는 구조를 보여주지 않는다.

### 공개된 검증 코드의 범위

아래 코드는 읽었으며 설치·실행하지 않았다.

| 파일 | 코드가 실제 확인·생성하는 것 | 구별할 한계 |
| --- | --- | --- |
| [validate.ts L21–65](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/packages/react-best-practices-build/src/validate.ts#L21) | 제목·설명·예제 존재, impact enum 등 rule 구조 검사 | 에이전트가 올바른 코드를 만드는지 평가하지 않음 |
| [extract-tests.ts L15–37, L65–70](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/packages/react-best-practices-build/src/extract-tests.ts#L15) | rule의 good/bad 예제·언어·설명을 JSON으로 추출 | 모델 실행·judge·holdout 결과가 아님 |
| [build.ts L135–179, L280](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/packages/react-best-practices-build/src/build.ts#L135) | 개별 rule을 읽고 정렬·조합해 AGENTS 출력 | 제품 동작 테스트가 아님 |
| [React CI L15–33](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/.github/workflows/react-best-practices-ci.yml#L15) | 의존성 준비 후 validate·build | 내부 product-design의 eval 파이프라인이라고 볼 수 없음 |

## 4. 실제 PR 패치 검증 제품은 별도 계약

[Vercel Agent Code Review 공식 문서](https://vercel.com/docs/agent/pr-review), 현재 본문의 마지막 갱신일 `2026-09-18`을 확인했다. 검색 요약에는 예전 `2026-02-03`이 보여 현재 날짜·계약 판단에는 사용하지 않았다.

PR 생성·commit push를 입력으로 전체 코드베이스 맥락을 읽고, 패치를 Sandbox의 실제 build·test·lint로 확인한 뒤 제안한다고 문서화한다. `@vercel` 요청에 따라 review·fix·조사를 구별한다. 지침은 디렉터리 상속·하위 범위·Markdown 참조/`@import`를 지원하며 총 50KB 제한이 있다. 같은 디렉터리에서는 우선순위가 가장 높은 지침 파일을 사용한다.

짧은 원문: “Guidelines are treated as context, not instructions.” 버그·보안·성능 검토라는 제품의 핵심 행동이 충돌하는 repository 지침보다 우선한다. 이 authority는 product-design 예제의 사용자 목표 우선순위와 동일한 층이 아니다.

문서가 말하는 patch validation은 제품 모든 상태의 렌더링 검사나 사람의 사용성 수락까지 입증하지 않는다. 실제 내부 운영 run·성적을 이번 조사에서 실행하거나 확보한 것은 아니다.

## 5. 56%·100% 수치가 가리키는 평가

공식 글이 연결한 [AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals), Jude Gao, `2026-01-27` 본문을 읽었다.

이는 **Next.js 16 API 지식 접근 방식**의 비교다. 기본 skill에서 56%의 경우 skill을 호출하지 않았고, build/lint/test로 평가한 통과율은 baseline 53%, 기본 skill 53%, 명시적 호출 지침 79%, 8KB AGENTS 문서 색인 100%라고 보고한다. 프로젝트를 먼저 탐색하라는 호출 문구의 영향, 테스트 누출·모순 제거, 구현 세부 대신 관찰 행동 검증도 설명한다.

짧은 원문: “Same skill. Same docs. Different outcomes”.

product-design의 품질 향상률, collector/judge 정확도, 모든 프로젝트에서 AGENTS가 skill보다 우수하다는 일반 결론으로 옮길 수 없다. 이 문서만으로 샘플 수·모델별 전이·우리 작업 효과를 재현 검증하지 않았다.

## 6. 이번 설계에 대해 확인되지 않은 것

- 기록 23의 **상세 품질 기준은 검토자가 기본 소비자**, **구현 후 검토자가 직접 수정·최종 실제 확인**, **Main이 완료 판단**이라는 묶음은 우리의 설계 가정이다. Vercel 자료에서 이 역할 분배·인수 패킷을 발견하지 못했다.
- `shape/implement/review`를 Main/구현자/검토자의 고정 순서에 대응시키면 모드와 주체를 혼동한다. B 방향을 반박하거나 취소한 결과도 아니다. B를 채택할 판단은 별도 근거가 필요하다.
- `Load product context`·brief·work plan·review notes는 확인되지만, 우리의 지속 Project common context와 Work별 Spec·Ticket 소유·수명·인수 파일 계약은 이 자료에서 확인되지 않는다. `internal brief`를 곧바로 Work Spec이라고 바꿔 부르면 안 된다.
- 내부 reference 전체, collector/judge의 전체 실행 prompt·수집 코드·권한·누락 검출, 실제 review packet과 사람 승인 이력, copywriting rubric·fixture·holdout·결과 수치는 공개 본문과 조사한 저장소에서 확보하지 못했다.
- guideline 변경 후의 관련 검사와 별도 skill 행동 eval을 구별해야 한다. 글의 설명만으로 모든 승인 변경마다 전체 product-design end-to-end eval이 자동 실행된다고 단정할 수 없다.
- 공개 JS lint 예시는 직접 `Select` 아래의 option 개수와 일부 동적 표현을 검사한다. 배포된 전체 lint 패키지·테스트·오탐률은 확보하지 못했으므로 그 예시의 존재를 production 신뢰도 측정으로 취급하지 않는다.

공개 파일·공식 문서는 재접근 가능한 URL과 고정 commit으로 남겼다. 내부 자료의 공개 여부는 이번 검색·연결 범위에서만 말한다. 조회용 임시 다운로드는 `/tmp`에서 대조했으며, source 사본·current·제품 코드·설치 상태는 변경하지 않았다.
