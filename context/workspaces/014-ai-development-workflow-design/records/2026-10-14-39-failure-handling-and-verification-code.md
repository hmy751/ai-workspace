# 같은 템플릿의 실패 처리·입력 검증·동작 확인

2026-10-14. 01-02에서 실제 코드의 현재 책임을 확인했다. 구현 변경이나 검증 정책 채택은 없다.

사용자:

> 좋아 그럼 같은 템플릿에서 실패 처리랑 검증을 실제 코드부터 보면서 이어가자. 지금 어떻게 하고 있고 각자 어디까지 맡는지 보여줘.

## 실제 연결과 경계

조사 범위는 `/Users/hammyeong-yeon/Desktop/20_lab/template`의 아래 파일과 검사 설정이다. 제품 화면이 아니라 Storybook 사용 예시다.

- [무한 스크롤 story](/Users/hammyeong-yeon/Desktop/20_lab/template/src/component/InfiniteScrollContainer/index.stories.tsx): queryFn에서 fetcher.get으로 상품을 조회·변환한다. 오류를 catch하여 성공값으로 바꾸지 않는다. React Query의 isError만 Container에 전달하며 error 객체·실패 단계·재시도 버튼은 연결하지 않는다.
- [fetcher](/Users/hammyeong-yeon/Desktop/20_lab/template/src/api/fetcher.ts): 응답 파싱 뒤 response.ok가 false면 status·code·data를 가진 APIError를 던진다. fetch 단계 예외는 timeout/network 등의 APIError로 변환한다. 화면 표시는 없다. 제네릭 T는 응답 구조를 실제로 검사하지 않는다. request에서 async handleResponse를 await 없이 반환하므로 그 함수의 비동기 거부는 request의 catch에서 재분류되지 않는다. 모든 예외가 동일한 경로로 정규화된다고 설명하지 않는다.
- [Container](/Users/hammyeong-yeon/Desktop/20_lab/template/src/component/InfiniteScrollContainer/index.tsx): isLoading 다음 isError를 검사해 errorComponent만 반환한다. 데이터가 있어도 isError면 children 목록을 그리지 않는다. errorComponent로 내용을 바꿀 수 있지만 현재 기본 분기는 목록을 대체한다.
- [관찰 Hook](/Users/hammyeong-yeon/Desktop/20_lab/template/src/hooks/useInfiniteScrollObserver.ts): enabled·화면 진입·다음 페이지 여부·추가 조회 중 여부를 보고 fetchNextPage를 호출한다. 실패 분류·재시도·에러 UI는 맡지 않는다. Container가 isError일 때 enabled를 false로 전달한다.
- [폼 story](/Users/hammyeong-yeon/Desktop/20_lab/template/src/component/FormSection/index.stories.tsx): WithRegisterValidate의 required·validate 및 WithController의 rules에 규칙을 선언한다. React Hook Form이 검사와 errors를 관리하며 handleSubmit으로 성공 콜백을 연결한다. Input의 isError는 표시 스타일에, Field.Message는 오류 문구 표시에 쓰인다. 이메일 두 오류 중 먼저 보여 줄 문구도 사용처가 선택한다. 제출 콜백은 console.log이며 서버 저장·서버 필드 오류 연결은 구현하지 않았다.

## 검증이 뜻하는 서로 다른 것

입력값 검증은 위 규칙과 React Hook Form으로 구현돼 있다. 응답은 JSON/text 파싱과 HTTP 상태를 확인하지만 products가 실제 배열인지 검사하는 코드는 없다. 비밀번호 안내에는 숫자 조합이 적혀 있지만 WithRegisterValidate의 해당 규칙은 비어 있는지만 검사한다. 이 차이가 의도적 예시 생략인지 제품 요구 누락인지는 아직 확인하지 않았다.

개발자가 동작을 확인하는 자동 테스트는 별도로 살펴봤다. package.json에는 dev/build/storybook/build-storybook만 있고 test/typecheck 스크립트는 없다. src·.storybook의 TS/JS에서 테스트 assertion·play 함수와 저장소의 통상적 test/spec 파일·테스트 도구 설정을 찾지 못했다. Storybook으로 직접 조작할 예시는 있지만 과거 수동 확인 여부는 알 수 없다. strict TypeScript 설정은 있으나 build는 babel-loader를 사용하므로 설정 존재를 타입 검사 실행 증거로 취급하지 않는다.

후속 논의 후보는 기존 목록이 있는 추가 조회 실패 시 목록 유지 여부, 실제 규칙과 안내문이 일치하는지, 실패 상태에서 추가 요청과 재시도 UI가 어떻게 동작해야 하는지다. 이는 관찰에서 나온 Main의 후보이며 사용자 선호나 테스트 의무로 확정하지 않는다.

## 근거와 확인 범위

React Query가 queryFn의 throw 또는 rejected Promise를 오류로 받는 계약은 [공식 문서](https://tanstack.com/query/latest/docs/framework/react/guides/query-functions)에서 확인했다. RHF의 검증·제출 계약은 [공식 저장소](https://github.com/react-hook-form/react-hook-form/blob/master/src/types/form.ts)를 참고했다. 확인일 2026-10-14, 템플릿 package.json 선언은 React Query ^5.80.6, RHF ^7.56.4다. 설치된 정확한 버전의 전체 동작을 검증한 것은 아니다.

코드 읽기와 검색만 수행했다. 실제 HTTP 요청·Storybook 실행·자동 테스트·코드 수정은 하지 않았다. 템플릿의 기존 미추적 doc/FORM_IMPLEMENTATION_GUIDE.md와 doc/react-query/는 변경하지 않았다. 앞선 판단 기준은 [체크포인트 38](2026-10-14-38-component-criteria-discussion-checkpoint.md)에 유지한다.

후속 위치: 아래 비교 뒤 사용자가 질문 목적과 버튼 논의의 혼란을 짚었다. 당시 제안은 이력으로 남기며, 현재 필요한 다음 작업은 [점검 40](2026-10-14-40-ticket-01-02-findings-and-remaining-work.md)에서 다시 정했다.

## 후속 비교: 기존 목록을 유지하고 아래에 오류·재시도를 표시한다면

사용자:

> 좋아 그럼 기존 상품이 있는 상태에서 다음 페이지 요청이 실패하면 어떻게 할지 보자. 목록은 유지하고 아래에 오류랑 재시도 버튼을 보여준다면 각자 어디까지 맡는 게 좋을까? 실제 코드로 비교해줘.

사용자가 지정한 비교 시나리오다. 아래는 실제 코드에 적용해 보는 미실행 제안이며, 현재 구현이나 보편 정책 채택으로 기록하지 않는다.

현재 Container는 isError이면 목록을 대체한다. 제안은 다음 페이지 실패만 그 분기에서 제외하고, 기존 children(items)를 유지한 채 하단에 오류 슬롯을 표시한다. 초기 조회·기존 페이지 재조회 실패의 정책은 이번 비교에서 확대 변경하지 않는다.

- React Query: pages·요청 상태·isFetchNextPageError를 제공하고 fetchNextPage로 다음 페이지를 다시 요청한다. 목록과 오류를 별도 useState로 복제하지 않는다.
- 사용처: query 설정·상품 UI·안내 문구·버튼 구성을 정하고 재시도 동작을 연결한다. 초기 요청이나 전체 재조회와 다음 페이지 재시도를 구별한다.
- Container: 실패 종류에 따라 전체 오류/하단 오류를 분기하고, 기존 목록 유지·하단 로딩/오류/끝 표시의 순서를 맡는다. 추가 props는 isFetchNextPageError?: boolean, nextPageErrorComponent?: ReactNode다. 예시 기본값은 각각 false, 기존 errorComponent다.
- 관찰 Hook: 기존대로 enabled와 조회 상태를 보고 자동 호출한다. Container의 기존 enabled: !isLoading && !isError && hasNextPage를 유지하면 오류 중 자동 스크롤 요청은 멈춘다. React Query 자체의 자동 재시도·포커스 재조회 설정까지 해제한다는 뜻은 아니다.
- fetcher: 기존 HTTP 요청과 실패 전달 역할을 유지한다.

사용처의 추가 연결 제안(query는 기존 useInfiniteQuery 결과, 나머지 props·Grid/Card 목록은 기존과 같다):

```tsx
isFetchNextPageError={query.isFetchNextPageError}
nextPageErrorComponent={
  <div>
    <p role="alert">다음 상품을 불러오지 못했어요.</p>
    <button
      type="button"
      disabled={query.isFetchingNextPage}
      onClick={() => {
        void query.fetchNextPage({ cancelRefetch: false });
      }}
    >
      다시 시도
    </button>
  </div>
}
```

Container 본문의 변경 제안(기존 Hook 호출·props 수신에 위 두 prop을 추가한 뒤):

```tsx
if (isLoading) return <>{loadingComponent}</>;
if (isError && !isFetchNextPageError) return <>{errorComponent}</>;

const items = data?.pages.flatMap(page => page) ?? [];
if (items.length === 0) return <>{emptyComponent}</>;

return (
  <>
    {children(items)}
    <div ref={loadMoreRef} style={{ height: '1px', padding: '2rem 0' }}>
      {isFetchingNextPage ? loadingComponent
        : isFetchNextPageError ? nextPageErrorComponent
        : !hasNextPage ? endComponent
        : null}
    </div>
  </>
);
```

요청 중에는 버튼 대신 로딩을 보여준다. cancelRefetch:false는 진행 중인 다음 페이지 호출을 반복 클릭으로 새로 시작하지 않도록 하는 선택이다. 자동 재시도가 설정돼 있다면 하단 최종 오류 표시는 그 시도가 끝난 실패 상태 기준이다. React Query와 같은 prop 이름을 쓴다고 import 의존성이 생기지는 않지만, 다음 페이지 실패를 구분해 주는 입력 계약은 추가된다.

버튼·문구까지 Container에서 기본 제공하면 사용처 코드가 줄어들고 공통 디자인을 맞추기 쉽다. 슬롯으로 받으면 문구·버튼 조합·오류별 동작을 사용처가 바꾸기 쉽고 연결 코드는 더 필요하다. 이번에는 기존 ReactNode 슬롯 방식과 사용자 합성 논의에 맞춰 슬롯 제공안을 우선 제안했다. 공통 기본 UI가 반복된다면 기본 제공+슬롯 교체도 가능한 후속 선택이다.

동작 검증 후보는 첫 페이지 성공 뒤 다음 페이지 실패를 제어해 (1) 기존 목록 유지와 하단 오류, (2) 오류 중 관찰 이벤트로 재요청하지 않음, (3) 버튼이 전체 refetch 대신 다음 페이지를 요청하며 중복 요청을 막음, (4) 성공 시 다음 항목 추가·오류 제거, (5) 다시 실패하면 목록·재시도 유지다. 아직 실행하거나 테스트를 작성하지 않았다.

라이브러리 계약은 2026-10-14 [공식 useInfiniteQuery 문서](https://tanstack.com/query/latest/docs/framework/react/reference/functions/useInfiniteQuery)의 isFetchNextPageError·fetchNextPage·cancelRefetch 항목으로 확인했다. 템플릿 설치 버전의 실행 검증은 아니다.
