# 무한 스크롤 컨텍스트 작성 참고 예시

**참고 조사용 예시.** 2026-10-16 사용자 요청에 따라 공식 Project 컨텍스트·개발 가이드·변경 지시로 사용하지 않는다. 아래는 당시 입력 사본에서 얻은 설명과 검토 질문이다. [보존 지위와 마무리](../../2026-10-16-46-rea-reference-research-close.md).

2026-10-15, template HEAD `8a200e050debc355150b9a67f68b140214197f7f`의 소스 사본 기준. 사용자 정책이 아니라 확인한 현재 구현이다.

**페이지 규칙은 story, 요청 처리는 fetcher, 화면 분기는 컨테이너, 스크롤 감지는 훅이 맡는다.** 페이지 크기를 바꾸는 작업과 실패 때 화면을 유지하는 작업은 수정 책임이 다르다.

| 수정 관심사 | 먼저 읽을 소스 사본 | 함께 확인할 조건 |
| --- | --- | --- |
| 페이지 크기·종료 | [story](input/src/component/InfiniteScrollContainer/index.stories.tsx) | skip·limit·마지막 응답 길이 비교의 20을 함께 확인. 정확히 20개면 빈 다음 페이지를 한 번 더 요청할 수 있음 |
| 실패 시 기존 목록 유지 | [컨테이너](input/src/component/InfiniteScrollContainer/index.tsx)와 story | isError가 데이터 표시보다 먼저 반환됨. 다음 페이지 재시도 종료 후 기존 목록도 오류 화면으로 대체됨 |
| 중복 요청 억제 | [훅](input/src/hooks/useInfiniteScrollObserver.ts), 컨테이너, [fetcher](input/src/api/fetcher.ts) | isFetchingNextPage가 전달된 뒤에는 감지 억제. 재렌더 전 연속 콜백은 같은 상태를 볼 수 있음 |
| 요청 취소·실패 | fetcher와 story queryFn | story가 Query signal을 전달하지 않음. fetcher는 자체 10초 타임아웃 signal 사용. Query 취소가 HTTP 취소로 이어진다고 가정하지 않음 |
| 이미지의 로딩·실패 | [ImageBox](input/src/component/ImageBox/index.tsx) | Skeleton은 이미지 로딩용. 목록의 API 로딩 표시는 story의 loadingComponent |

실행으로 확인한 조건:

- 첫 20개와 다음 5개를 합쳐 25개 표시하고 감지를 중단한다.
- 다음 페이지 요청이 기본 재시도까지 실패하면 캐시에 20개가 남아도 화면에는 상품 0개와 오류가 표시된다.
- 감지 콜백을 React 재렌더 전에 연속 두 번 주면 같은 페이지 요청이 두 번 발생한다. 실제 브라우저 발생 빈도는 확인하지 않았다.
- 20개 뒤 빈 응답을 받으면 20개를 유지하며 종료 안내를 표시한다.

실행은 실제 React·React Query와 원본 소스를 사용했지만 HTTP·IntersectionObserver는 통제한 JSDOM 검사다. 브라우저 geometry·CSS·실제 서버 수락 검사가 아니다. [검사 결과](../../receipts/rea-infinite-scroll-20261015/runtime-results.json)

실행 환경은 [Storybook preview](supplemental/.storybook/preview.tsx)의 기본 QueryClientProvider다. `src/store/react-query/index.md`는 설정 메모이며 실제 Provider 설정을 대신하지 않는다.

실험에서 남긴 검토 질문은 실패 시 기존 목록 유지 여부, 재시도 UI, 중복 HTTP 요청을 어느 수준까지 막을지다. 현재 관찰을 원하는 정책으로 자동 승격하지 않는다. [비교 보고서](../../2026-10-15-44-rea-infinite-scroll-context-comparison.md)
