# 범위와 수집 계획

작성일: `2026-11-04`

자료 수집을 시작하기 전에 합의한 이름, 주제, 방법을 남긴다. 판단의 현재 요약은 [`memory.md`](../current/memory.md)가 소유한다. 대상의 위치·계정·규모와 대상별 확정 사실은 공개하지 않으므로 [로컬 수집 기록](collection/README.md)에 둔다.

## 범위가 정해진 경위

| 단계 | 사용자 발화 | 반영 |
|---|---|---|
| 출발 | "UI의 뭐라해야하지 위치나 구성 레이아웃 단순 absoulte로 떼우더라고" | 처음에는 레이아웃 구성 문제로 조사했다. |
| 이름 정정 | "뭔가 컴포넌트 시스템처럼 쌓는 그런 관점도 중요하고 그렇다고 생각해서 그런걸 쌓는 층이니까" | 범위가 넓다는 판단을 철회하고 `design-system`을 주제 이름으로, 레이아웃 구성을 그 안의 한 층으로 정했다. |
| 대상 지정 | "dev-hub에서 뭐 이력서나 인터뷰 등의 자료에서 좀 관련 관점들 뽑고 interpersona, noline등의 디자인시스템 관점으로 클라이언트 코드 면밀히 조사" | 자료 수집을 Personal 작성의 앞 단계로 분리했다. |
| 주제 확장 | "아까 내가 한 얘기에 한정하지말고 좀 다양한주제로 안빠지게 해줘 headless UI 방식이나 스토리북이나 등등 도 있잖아?" | 조사 주제를 디자인 시스템 전반으로 넓히고 누락 방지 방법을 추가했다. |

저장소가 공개로 확인된 뒤 사용자가 수집 기록을 Git에서 제외하기로 했다. 수집 뒤 사용자는 문제를 "구조를 보지 않고 덧대는 방식"으로 정리했고 absolute는 그 한 증상으로 보기로 했다. 아래 사전 조사는 그 전에 쓴 기록이며 현재 목표는 [`memory.md`](../current/memory.md)를 따른다.

## 조사 주제

| 영역 | 포함 내용 |
|---|---|
| 기반값 | 색, 타이포, 간격, radius, shadow, z-index, breakpoint 토큰, 테마, 이름 짓는 법 |
| 레이아웃 | 프리미티브, flex·grid·absolute 선택, 간격 소유, 반응형, overflow, 긴 텍스트 대응 |
| 컴포넌트 구조 | 공통·도메인·페이지 구분, 공통으로 올리는 기준, 파일과 폴더 구성 |
| 컴포넌트 API | props, variant, Composition, Compound, Headless, slot, 제어·비제어, ref, 스타일 확장 방식 |
| 상태와 접근성 | 로딩·에러·빈 상태, 폼 필드, 키보드와 포커스, ARIA, 모달·토스트 같은 오버레이 |
| 스타일 기술 | CSS-in-JS, 유틸리티 CSS, sass 등의 선택 이유, 외부 UI 라이브러리를 감쌀지 말지, 웹과 RN 호환 |
| 개발과 검증 | Storybook, 시각 회귀, 컴포넌트 테스트, E2E, Figma와 코드 연결, 사용 문서 |
| 운영과 변화 | 재작성, 이전과 폐기, 모노레포 패키지 분리, lint 같은 강제 수단, 번들과 성능, 다국어 |
| AI 협업 | AI가 시스템을 벗어나는 패턴, 사용자가 고친 부분, AI에게 줘야 할 지침 |

이 목록은 출발점이며 제한이 아니다.

## 수집 방법

1. **주제 목록으로 찾기:** 자료마다 모든 주제를 확인하고 "근거 있음, 찾았지만 없음, 확인 못 함"으로 적는다.
2. **자료에서 거꾸로 찾기:** 폴더 구조, `package.json`, 자주 고친 파일, 리팩터링 커밋을 먼저 훑어 목록에 없던 주제를 추가한다.
3. **자료 간 대조:** 한 자료에서 나온 주제를 나머지 자료에서도 찾아 일관된 판단과 한때의 선택을 구별한다.

코드는 두 단계로 본다. 먼저 absolute, z-index, 임의의 px 값, 컴포넌트 바깥 여백, 프리미티브와 토큰 사용량을 프로젝트별로 센다. 그다음 토큰, 프리미티브, 공통 컴포넌트, 화면 순서로 읽는다. absolute는 "적절함, 대체 가능, 땜질"로 나눈다.

**관찰 항목:** 주제, 층, 관찰, 출처(파일·커밋), 근거 종류, 시기, 확신도

**결과물:** 자료별 수집 기록, 주제별 현황표, 종합 정리, Personal 후보

## 사전 조사

### pstack

pstack 플러그인에는 레이아웃이나 디자인 시스템 전용 자료가 없다. 참고할 수 있는 것은 두 곳이다.

- `skills/principle-experience-first/SKILL.md:14`: 정렬과 간격 같은 디테일을 챙기라는 한 줄
- `skills/poteto-mode/playbooks/prototype.md:7`: 레이아웃 결정은 시안을 띄워 고르라는 검증 방법

### 외부 자료

Personal 작성 때 대조할 후보이며 채택한 기준은 아니다. 2026-11-04에 읽은 내용이다.

| 자료 | 가져올 점 |
|---|---|
| [CUBE CSS Composition](https://cube.fyi/composition.html) | 레이아웃 층의 책임 정의. 픽셀 단위로 맞추지 않고 유연한 규칙을 주어 브라우저에 맡긴다. |
| [Every Layout](https://every-layout.dev/rudiments/composition/) | 한 가지 일만 하는 작은 레이아웃의 조합 |
| [Braid Layout](https://seek-oss.github.io/braid-design-system/foundations/layout/) | 컴포넌트는 바깥 여백을 갖지 않고 간격은 레이아웃 컴포넌트가 맡는다. |
| [Margin considered harmful](https://mxstbr.com/thoughts/margin) | 간격은 부모가 정해야 하는 이유 |
| [Space in Design Systems](https://eightshapes.com/articles/space-in-design-systems/) | inset, stack, inline 어휘 |
| [Aksel 프리미티브](https://aksel.nav.no/grunnleggende/kode/layout-primitives) | 프리미티브와 토큰, 브레이크포인트의 연결 |
| [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines) | 긴 내용과 여러 화면 폭 확인 항목, AI 에이전트 연결 방법 |
| [Thoughtbot](https://thoughtbot.com/blog/absolute-positioning-with-css-grid), [PQINA](https://www.pqina.nl/blog/css-grid-position-absolute-alternative/) | absolute 없이 grid 같은 칸으로 겹치기 |
| [MDN Anchor Positioning](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning/Using) | 다른 요소에 붙는 UI를 CSS로 처리. 지원 범위는 사용 전에 다시 확인한다. |

### 레이아웃 판단 초안

자료를 종합한 웹 기준 초안이며 수집 전에 썼다. React Native에는 fixed와 CSS grid가 없어 그대로 적용할 수 없다. 현재 판단은 수집 후 종합을 따른다. 핵심 질문은 "이 요소의 내용이 길어지거나 화면이 좁아지면 주변이 밀려나야 하는가"이다.

| 요소의 관계 | 쓸 것 |
|---|---|
| 순서대로 놓이고 서로 밀어냄 | 일반 흐름, flex + gap |
| 행과 열을 맞춤 | grid |
| 겹치지만 부모 크기에 반영돼야 함 | 같은 grid 칸 |
| 겹치고 부모 크기에 영향이 없어야 함 | absolute |
| 다른 요소에 붙어서 뜸 | popover, anchor positioning, 쓰는 UI 라이브러리 |
| 화면 기준으로 뜸 | fixed, dialog |
