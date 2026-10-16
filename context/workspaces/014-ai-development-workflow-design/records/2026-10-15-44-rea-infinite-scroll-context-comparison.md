# 더 연결된 무한 스크롤 기능에서 REA와 직접 분석 비교

**보존 지위 — 참고 조사.** 2026-10-16 사용자 요청에 따라 이번 결과는 보조 도구를 이해하기 위한 조사 자료로만 남긴다. 아래 추천은 실험 당시의 해석이며 정식 도입·운영 기준·Ticket 진행으로 채택하지 않았다. [마무리 기록 46](2026-10-16-46-rea-reference-research-close.md).

2026-10-15. **Toast보다 연결이 많은 기능에서는 REA의 ‘읽을 파일을 찾아주는 도움’이 보였다. 그러나 이번 template의 개발 컨텍스트를 준비하는 데 직접 분석보다 유리하다는 근거는 얻지 못했다.** 관련 파일 목록은 자동으로 얻었지만, 변경에 중요한 실패·중복 요청·페이지 종료 조건은 원문을 읽고 실행해서 확인했다. 이 결론은 이번 입력과 REA 6.5.0의 실제 조회 범위에 한정한다.

사용자는 앞선 Toast 사례가 너무 작아 차이를 보기 어려웠는지 물었다.

> 그럼 이번엔 너무 작은 코드라 차이가 안 난 거 아닌가? template에서 좀 더 복잡하게 연결된 기능으로 비교하면 REA가 도움이 되는지 볼 수 있을까?

그 지적을 반영해 미리 관련 파일을 골라 주지 않고 src 전체에서 진입점 하나로 탐색했다. 앞선 [Toast 비교 43](2026-10-15-43-rea-toast-context-comparison.md)은 작은 사례의 관찰로 유지한다. REA 일반의 무용함이나 모든 큰 코드에서의 우열을 결론 내리지 않는다.

## 이번에는 무엇을 비교했나

진입점은 template의 `InfiniteScrollContainer/index.stories.tsx`다. 서버 요청, 페이지 상태, 스크롤 감지, 컨테이너의 표시 분기, 상품·이미지 표시가 연결된다. 핵심 4개 소스는 349줄이며, 표시 의존성까지 소스 8개가 이어진다. Toast의 핵심 3개·123줄보다 넓지만 여전히 작은 패턴 모음의 사례다.

공통 입력은 src 전체와 package.json·tsconfig.json의 75개 파일, 182,118바이트다. REA는 47개 TS/TSX 파일을 parse failure 없이 읽었다. 시작 질문은 ‘페이지 크기, 중복 요청 억제, 실패 표시를 바꾸려면 무엇을 함께 알아야 하는가’였다.

이번에는 REA 탐색을 먼저 수행해 [탐색 초안](experiments/rea-infinite-scroll-20261015/rea-discovery.md)을 고정했다. 그 뒤 소스와 사용처를 읽고 [직접 분석 초안](experiments/rea-infinite-scroll-20261015/direct-context.md)을 고정한 다음 실행 확인을 했다. 같은 Main이 앞선 맥락과 REA 결과를 알고 있으므로 **독립 A/B도, 직접 분석의 탐색 속도 측정도 아니다.** 도구가 반환한 정보와 AI의 원문 해석·실행 확인의 기여를 구별하는 비교다. [실험 조건](experiments/rea-infinite-scroll-20261015/protocol.md)

## REA가 실제로 더해 준 것

처음 원본 TS/TSX 입력에서는 진입점의 확장자 없는 상대 import 5개가 모두 `not-found`였다. 해당 파일들은 존재하고 파싱도 됐다. 같은 import를 유지한 ESM JavaScript 사본도 해소하지 못했다. 원본 tsconfig는 `moduleResolution: Bundler`인데 이번 도구 경로에서는 그 해석이 연결되지 않았다. TypeScript 구문을 읽는 능력과 파일 간 연결을 해석하는 능력은 구별해야 한다.

여기서 실패로 끝내지 않고 같은 코드를 CommonJS JavaScript로 변환한 분석용 사본으로 재실행했다. 이때는 진입점에서 다음 8개 소스를 자동으로 연결했다.

| 연결 | 실제 역할: 역할 설명은 원문을 읽은 뒤 확인 |
| --- | --- |
| story → fetcher | 페이지 요청과 공통 HTTP 처리 |
| story → InfiniteScrollContainer → useInfiniteScrollObserver | 페이지 상태 전달, 표시 분기, 다음 요청의 감지 조건 |
| story → Grid·Card·ImageBox → Skeleton | 상품 배치와 이미지 표시·이미지 로딩 상태 |

fetcher를 거꾸로 조회하면 이 story가 사용처로 나왔다. **진입점에서 관련 파일 범위를 얻고, 공통 코드의 사용처를 다시 찾는 데는 실제 도움이 됐다.** 읽을 파일을 하나씩 열기 전에 연결을 확인하고 같은 증거를 재조회할 수 있다. 단, CommonJS 사본은 분석 편의를 위한 변환이며 실제 Webpack 빌드나 실행 동등성 검증이 아니다.

그 이후의 의미 추적에는 한계가 있었다. `useInfiniteScrollObserver`의 호출자 조회는 함수 자신만 반환했고 연결은 없었다. 관련 unknown 4개가 있어 ‘호출자가 없음’으로 해석할 수 없다. `fetchNextPage` 속성의 영향 조회도 매치 없이 partial이었다. fetch 요청·타이머 노드는 나왔지만 주소·지연 값은 null이었다. 이 조회들만으로 React Query, props, 콜백을 관통하는 동작을 복원했다고 볼 수 없다.

또한 Skeleton 연결 자체는 맞지만 **상품 목록의 API 로딩이 아니라 이미지 로딩**이다. 관계 목록에 나온다고 모두 현재 질문의 수정 대상은 아니다. 이런 구분에는 원문 해석이 필요했다.

## 개발 컨텍스트에서 중요했던 답

| 변경 질문 | 준비한 답 | 답을 얻은 근거 |
| --- | --- | --- |
| 20개씩 가져오던 것을 바꾸려면? | story의 skip 계산, limit, 마지막 페이지 길이 비교를 함께 바꿔야 한다. 컨테이너·훅은 20을 모른다. | 직접 소스 읽기 |
| 다음 페이지 실패 때 기존 목록은 남는가? | 재시도 중에는 남는다. 재시도가 끝나 오류 상태가 되면 기존 20개는 캐시에 있지만 화면은 오류만 표시한다. | 소스에서 가설 도출, 실제 React Query·컴포넌트 실행으로 확인 |
| 로딩 중 감지 조건이 있으면 중복 요청이 완전히 막히는가? | 로딩 상태가 화면에 반영된 뒤의 감지는 막힌다. 반영 전에 콜백을 두 번 주면 같은 다음 페이지 요청이 두 번 발생했다. | 훅·상태 전달·fetcher 읽기, 통제한 콜백 실행으로 확인 |
| 마지막 페이지가 정확히 20개면? | 다음 페이지가 있다고 판단하므로 빈 응답을 한 번 더 받은 뒤 종료 표시가 나온다. | 종료 조건 읽기와 실행 확인 |

REA가 찾아 준 관련 파일 안에 이 답의 근거가 있었다. 그러나 위 답을 도구가 새로 도출해 준 것은 아니다. **REA를 사용하는 AI도 이 단계에서는 소스 해석과 실행 검사를 추가해야 했다.** 최종 산출물은 [짧은 개발 컨텍스트](experiments/rea-infinite-scroll-20261015/prepared-context.md)에 분리했다.

## 실행 확인의 범위

보존한 실제 story·컨테이너·훅·fetcher를 React 19.1.0과 React Query 5.80.6으로 실행했다. QueryClient는 실제 preview와 같은 기본 설정이다. HTTP 응답과 IntersectionObserver 콜백을 통제하고 JSDOM·가상 시간을 사용했다. CSS·실제 스크롤 위치·실제 서버·Storybook 전체 실행은 확인하지 않았다.

1. 첫 20개 → 다음 5개: 총 25개 표시, 종료 안내, 감지 중단. 요청 중 상태가 반영된 뒤의 재감지는 추가 요청 없음.
2. 다음 페이지 HTTP 500: 최초 시도와 기본 재시도 3회 이후 오류. 캐시 20개, 화면 상품 0개, 감지 중단.
3. React 재렌더 전 감지 콜백 2회: 같은 skip=20 요청 2개, 앞 요청의 fetch signal은 취소되지 않음. 응답 후 표시 데이터는 25개로 중복되지 않음. 실제 브라우저에서 이 간격의 콜백이 얼마나 발생하는지는 별도 문제다.
4. 첫 응답 20개 → 다음 응답 0개: 두 번째 요청 뒤 종료 안내.

4개 시나리오 모두 통과했다. 실패 UI나 요청 정책이 사용자의 의도에 맞는지는 아직 선택하지 않았고 원본을 수정하지 않았다. [검사 코드](experiments/rea-infinite-scroll-20261015/verify-runtime.cjs), [실행 결과](receipts/rea-infinite-scroll-20261015/runtime-results.json)

직접 읽기 중 Provider 위치를 확인하려고 `.storybook/preview.tsx`를 추가로 읽었다. 최초 공통 입력인 src 밖이므로 REA의 탐색 누락으로 채점하지 않는다. 별도 [사본](experiments/rea-infinite-scroll-20261015/supplemental/.storybook/preview.tsx)과 [manifest](receipts/rea-infinite-scroll-20261015/supplemental-manifest.json)를 보존했다. src 아래 React Query 설정 메모를 실제 실행 설정으로 오인하지 않는다.

## 실험 당시의 해석과 제안

**당시 Main은 직접 소스 분석과 필요한 실행 검사를 기본으로 유지하자고 제안했다.** 이 제안은 정식 작업 방식으로 채택한 것이 아니며, 최종 보존 지위는 참고 조사다. 이번에 REA의 관련 파일 탐색 효용은 보였으므로 Toast만 보고 ‘관계가 복잡해져도 도움이 없다’고 일반화하지 않는다. 다만 이 template에서는 같은 관계를 import와 사용처 검색으로도 확인할 수 있었고, REA에는 변환·질의 준비가 추가됐다. 얻은 연결만으로 준비해야 할 컨텍스트가 완성되지는 않았다.

도구를 다시 평가할 조건은 단순히 파일 수가 늘어나는지가 아니다. 여러 기능이 공유하는 코드의 영향 범위를 반복해서 찾아야 하거나, 사람이 따라가기 어려운 연결을 REA가 실제로 해석·좁혀 줄 수 있는지가 중요하다. 이 실험은 그 규모의 탐색 누락률·시간 절감·장기 재사용 비용을 측정하지 않았다. REA의 바이너리·런타임 수집·소스맵 복원 등 다른 기능도 평가 범위 밖이다.

정적 분석 실행은 원본 약 3.60초, ESM 사본 약 3.81초, CommonJS 사본 약 4.09초였다. 사람이 준비·해석한 시간은 통제하지 않았으므로 속도 우열을 주장하지 않는다. 전체 graph를 대화에 모두 넣을 필요도 없다. 원본 summary 조회는 약 10KB이고, 선택 조회로 범위를 줄일 수 있다.

이 기록의 사례·실행 결과·컨텍스트 예시는 참고 조사로 보존한다. 01-02·01-03·03의 공식 결과나 진행 근거로 편입하지 않는다.

## 근거와 재현

- [입력 hash·원본 Git 상태](receipts/rea-infinite-scroll-20261015/input-manifest.json), [REA 초안 고정](receipts/rea-infinite-scroll-20261015/rea-discovery-freeze.json), [직접 초안 고정](receipts/rea-infinite-scroll-20261015/direct-context-freeze.json).
- [원본 분석](receipts/rea-infinite-scroll-20261015/analysis.json.gz), [ESM 분석](receipts/rea-infinite-scroll-20261015/emitted-analysis.json.gz), [CommonJS 분석](receipts/rea-infinite-scroll-20261015/commonjs-analysis.json.gz). 무손실 gzip이며 [압축 전 hash](receipts/rea-infinite-scroll-20261015/archive-manifest.json)를 보존했다.
- [원본 진입점 조회](receipts/rea-infinite-scroll-20261015/entry-outgoing.json), [변환 후 파일 연결](receipts/rea-infinite-scroll-20261015/commonjs-entry-outgoing.json), [fetcher 사용처](receipts/rea-infinite-scroll-20261015/fetcher-importers.json), [훅 호출자 조회](receipts/rea-infinite-scroll-20261015/observer-callers.json), [fetchNextPage 조회](receipts/rea-infinite-scroll-20261015/fetch-next-page.json), [질의 조건·실행 수치](receipts/rea-infinite-scroll-20261015/query-executions.json).
- 설치 버전·integrity는 [REA lock](receipts/rea-infinite-scroll-20261015/rea-package-lock.json), [실행 검사 lock](receipts/rea-infinite-scroll-20261015/runtime-package-lock.json)에 있다. 재실행 방법은 protocol에 있다.
- 원본 template과 기존 미커밋 문서는 보존했다. 글로벌 MCP·설정·원본 코드 수정, 커밋은 하지 않았다. [보존·문서 검사](receipts/rea-infinite-scroll-20261015/validation.json).
