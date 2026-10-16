# 직접 소스 읽기로 준비한 컨텍스트 — 실행 전

REA 탐색 초안 고정 뒤, 같은 story와 import 대상 8개 원문을 읽고 src 사용처를 rg로 검색했다. REA 결과를 이미 본 같은 Main이므로 독립 탐색 속도 비교가 아니다.

## 기능 책임과 변경 위치

- story가 React Query의 useInfiniteQuery를 사용한다. 페이지 시작은 1, skip=(pageParam-1)*20, limit=20. 받은 products를 name=title, price=id*100 문자열로 가공한다. 마지막 응답이 정확히 20개일 때만 다음 페이지가 있다고 본다. 페이지 크기 변경은 skip·limit·종료 판단의 20을 함께 확인해야 한다.
- fetcher가 baseURL=https://dummyjson.com, 기본 10000ms AbortController, JSON/text 응답, HTTP/APIError를 담당한다. 요청의 signal은 자체 controller로 덮어쓴다. story queryFn은 React Query의 signal을 받아 전달하지 않는다. 따라서 Query 취소와 실제 HTTP 취소의 연결을 자동으로 가정하면 안 된다.
- InfiniteScrollContainer는 pages를 평탄화하고 표시 분기를 담당한다. isLoading이면 loading, isError이면 error, items가 없으면 empty를 즉시 반환한다. 데이터가 있어도 isError가 먼저이므로 다음 페이지 실패가 isError로 전달되면 기존 목록 대신 오류만 나올 것으로 예상한다. 실제 React Query 상태 전이는 실행에서 확인할 사항이다.
- useInfiniteScrollObserver는 enabled && intersecting && hasNextPage && !isFetchingNextPage일 때 fetchNextPage를 호출한다. 기본 threshold=.1, root=null, rootMargin=0px. effect 정리에서 unobserve한다. 완료·오류·초기 로딩은 컨테이너가 enabled=false로 만든다. 렌더가 갱신되기 전 연속 콜백은 같은 false 상태를 볼 수 있어 이 조건만으로 모든 중복 요청 억제를 보장할 수 없다.
- Card·Grid는 표시 구조, ImageBox는 이미지 loading/error/success, Skeleton은 그 이미지 로딩의 표시다. Skeleton을 API 목록의 로딩 표시로 해석하면 틀린다. 목록 로딩은 story가 넘긴 p 요소다.

## 세 가지 변경 질문에 대한 답

1. 페이지 크기: story queryFn/getNextPageParam. 공통 컨테이너나 훅은 숫자 20을 모른다. 전체 개수가 정확한 배수이면 마지막 빈 페이지를 추가로 요청하는지 확인한다.
2. 중복 요청: 훅의 조건, 컨테이너의 isFetchingNextPage 전달, React Query fetchNextPage 동작, fetcher 취소 연결을 함께 본다. 단순 조건 존재와 실제 네트워크 요청 수는 구별한다.
3. 실패 표시: fetcher가 만드는 오류, story의 Query 결과, 컨테이너의 isError 선행 반환을 함께 본다. 다음 페이지 실패 때 기존 목록을 유지하려면 상태 구분과 UI 정책이 필요하다. 현재 오류 화면에 재시도 버튼은 없다.

## 입력 경계 밖에서 추가로 발견한 환경

src의 실행 코드에서 fetcher와 훅의 사용처는 이 기능 하나로 확인했다. useInfiniteQuery는 Provider가 필요하므로 template/.storybook도 따로 검색했다. preview.tsx가 new QueryClient()와 QueryClientProvider를 설치한다. 이 파일은 처음 합의한 src 입력에 없었으므로 REA 누락으로 채점하지 않는다. supplemental에 원본 사본을 보존하고 양쪽의 공통 입력 경계 누락으로 기록한다. src/store/react-query/index.md의 설정 예시는 실행 설정으로 취급하지 않는다.

## 다음 실행 확인

실제 원본 사본의 story/컨테이너/훅/fetcher와 React Query를 사용한다. 서버 응답과 IntersectionObserver 입력은 통제한다. 첫 페이지·다음 페이지·종료, 다음 페이지 실패 뒤 기존 데이터/표시, 렌더 전 연속 감지의 네트워크 요청 수를 확인한다. 실제 브라우저 스크롤 위치·CSS·실제 서버는 검증하지 않는다.
