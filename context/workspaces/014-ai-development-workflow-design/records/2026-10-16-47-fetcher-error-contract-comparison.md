# fetcher의 오류 계약과 inter-persona 비교

2026-10-16. 01-02에서 template의 실제 요청 사용처를 읽은 뒤, 사용자가 지정한 inter-persona의 오류 처리와 비교했다. 두 저장소는 읽기만 했으며 설치·제품 수정·실행 검증은 하지 않았다. 아래 동작은 코드 경로에 따른 분석이며 브라우저 재현 결과가 아니다.

## 사용자와 확인한 기준

사용자 발화:

> 그런거 좋은 기준 또는 생각으로 보여 누가 무엇을 알고 몰라야 하는 그런 기준과 책임을 잘 고려하는것이라고 해야하나?

> 맞아 오류를 공통으로 처리한다면 사용처에서 그 형태와 의미를 믿고 쓸 수 있어야겠네. 그럼 이번 fetcher에서 나온 기준도 기록하고 다음에 뭘 보면 좋을지 정리해보자.

이 기준은 모듈마다 자기 역할을 수행하는 데 필요한 지식과 공개 계약을 정하고, 다른 모듈의 내부 순서·예외를 알아야만 올바르게 사용할 수 있는지를 보는 것이다. 공개 오류 코드나 API 응답 구조를 아는 것 자체가 나쁜 의존은 아니다. 모든 내부 정보를 숨기거나 오류 종류를 최대한 늘리라는 원칙도 아니다.

추가로 사용자가 inter-persona 경로를 직접 지정하고 두 구현 중 무엇이 나은지 비교를 요청했다. 이 조사 권한은 지정 프로젝트의 오류 처리 및 관련 사용처에 한정하며 다른 아카이브 조사로 확대하지 않았다.

## 실제 코드와 범위

- template: `/Users/hammyeong-yeon/Desktop/20_lab/template/src/api/fetcher.ts`, `src/component/InfiniteScrollContainer/index.stories.tsx`.
- inter-persona: `/Users/hammyeong-yeon/Desktop/90_archive/project-archives/inter persona 자료/inter-persona`, 확인한 HEAD `16d7136`. 아래 경로는 이 루트 기준이다.
- `_apis/fetcher.ts`, `_libs/error/service.ts`, `_libs/error/errors/*.ts`, `_libs/types/error.ts`는 `apps/frontend/src/` 아래에서 확인했다.
- 실제 연결: `_components/pages/user/LoginForm.tsx`, `_apis/user.ts`, `_data/interviewer.ts`, `_apis/interviewer.ts`, `_components/layout/error/ErrorBoundary.tsx`, `app/error.tsx`, `app/global-error.tsx`.
- 서버의 로그인 401 응답은 `apps/backend/src/routes/user.ts:41,48`, 인증 미들웨어는 `apps/backend/src/middleware/auth.ts`에서 확인했다.
- `inter_error.md`, `inter_error2.md`, `inter_error_bou.md`는 미추적 과거 Cursor 대화·제안 자료다. 일부 도입부를 확인했지만 구현 사실의 원천으로 사용하지 않는다. 실제 파일과 같은 것으로 취급하지 않는다.

## template에서 확인한 책임

실제 Storybook 호출:

```ts
const response = await fetcher.get<{ products: Product[] }>(
  `products?skip=${(pageParam - 1) * 20}&limit=20`
);
return response.products.map(p => ({ ...p, name: p.title, price: `${p.id * 100}` }));
```

fetcher는 기본 주소·헤더·HTTP 메서드·타임아웃·본문 파싱·공통 오류 변환을 맡는다. 사용처는 상품 API·파라미터·상품 가공·페이지 규칙을 맡고 Query는 요청 상태를 관리한다. 제네릭 타입은 기대하는 본문 형태이며 런타임 검증이 아니다. 현재 story는 `isError`만 사용하므로 오류 종류별 우회 처리가 실제로 존재한다고 단정하지 않는다.

두 fetcher 모두 `try` 안에서 `return handleResponse(response)`를 사용한다. 비동기 본문 읽기·JSON 파싱의 rejection은 이 지역 catch를 통과하지 않을 수 있다. 따라서 모든 실패가 공통 오류로 변환된다는 보장은 없다. `return await`만 추가하면 비 Abort 일반 Error를 네트워크 실패로 변환하는 현재 catch 때문에 파싱 오류의 의미가 잘못 분류될 수 있다. 응답 해석 실패와 연결 실패의 의미까지 함께 판단해야 한다.

## inter-persona에서 추가된 책임과 편의

| 영역 | 실제 구현과 의미 |
| --- | --- |
| 오류 모델 | AppError 아래 APIError·AuthError·NetworkError·응답 스키마 불일치·녹음 오류 등으로 의미를 구별한다. |
| fetcher | 401을 AuthError로, fetch 단계 연결 실패를 NetworkError로 변환한다. UI를 직접 실행하지는 않는다. |
| 데이터 계약 | 면접관 Query와 로그인 사용처에서 `safeParse`를 실행해 스키마 불일치를 별도 오류로 전달한다. 모든 API의 검증을 보장하는 것은 아니다. |
| errorService | 로그를 남기고 오류별 등록 처리기를 실행한다. 해당 처리기가 없거나 우회하면 toast·dialog·silent·throw를 선택한다. |
| 공통 사용자 대응 | 인증 안내·`/user` 이동, 네트워크 토스트, 녹음 권한·장치 안내를 재사용한다. |
| ErrorBoundary | 대체 화면과 resetConfig에 따른 Query·Redux·사용자 reset을 연결한다. service에는 silent를 전달한다. |

HTTP 전송, 도메인별 데이터 검증, 앱의 공통 대응, 화면별 결정으로 책임을 나눈 방향은 실제 앱의 반복을 줄이는 데 유리하다. 이는 사용자 채택 완료 판정이 아니라 이번 비교의 AI 평가다.

## 사용처가 우선순위를 알아야 하는 구체 사례

service의 핵심 순서:

```ts
if (!bypassRegisteredHandlers && error instanceof AppError) {
  const handler = this.registeredHandlers.get(error.constructor as AppErrorConstructor);
  if (handler) {
    handler(error);
    return;
  }
}
if (errorFallbackOptions.type) {
  this.displayUI(error, errorFallbackOptions);
} else {
  throw error;
}
```

옵션 이름이 fallback인 것처럼 등록 처리기가 우선이며, 세 번째 인자로 우회할 수 있다. 우선순위 자체가 무조건 잘못된 것은 아니다. 다만 다음 실제 연결에서는 호출부만 읽어 기대하기 어려운 효과가 생긴다.

1. LoginForm은 `errorService.handle(error, { type: 'toast', title: '로그인 실패', description })`를 호출한다. 서버는 잘못된 로그인 자격 정보에 401을 반환한다. fetcher는 이를 고정 메시지 '인증이 필요합니다.'의 AuthError로 바꾸고, 등록 처리기는 '인증 에러' 토스트와 `window.location.href = '/user'`를 실행한다. 로그인 실패 안내와 세션 인증 실패의 대응을 같은 것으로 취급한다. 화면 정책의 적합성은 별도 판단이지만 이 경로는 실제 코드로 연결된다.
2. ErrorBoundary는 `errorService.handle(error, { type: 'silent', context: ... })`를 호출한다. AuthError·NetworkError 등의 등록 처리기는 silent 분기 전에 실행되므로 토스트나 이동이 발생할 수 있다. 현재 호출은 우회 인자를 전달하지 않는다.
3. 일반 AppError의 표시에서는 `error.message`가 사용처의 `description`보다 우선한다. 로컬 설명이 항상 덮어쓰는 API라고 해석하면 안 된다.

오류 클래스와 UI 처리 함수는 함수로는 나뉘어 있지만 같은 모듈에 있고, 오류 export 진입점을 통해 store·브라우저 의존성이 연결된다. 재사용 범위를 넓힐 때 확인할 결합이며 이번에 파일 분리를 의무화하거나 수정하지 않는다.

## 비교 판단과 다음 논의

template는 작은 공통 요청 도구로 읽기 쉽고 화면 정책의 자유도가 크다. inter-persona는 실제 앱의 오류 의미·검증·반복 대응을 더 많이 제공한다. 따라서 해당 앱의 반복 대응에는 inter-persona의 계층 구성이 더 유용하지만, 구현의 모든 보장이 더 낫다는 뜻은 아니다. 두 fetcher의 파싱 오류 처리 공백은 공통이고, inter-persona에는 공통 정책과 로컬 선택의 우선순위를 알아야 하는 부담이 추가됐다.

사용자 동의로 보존할 기준은 '공통으로 제공한 형태와 의미를 사용처가 신뢰할 수 있어야 한다'이다. 비교에서 도출한 후속 후보는 '공통 정책과 사용처 선택이 충돌할 때 우선순위와 예외 범위를 명확히 한다', '오류 구분은 실제로 다른 대응·진단에 쓰이는 만큼 둔다'이다. 후속 후보와 inter-persona 평가를 사용자가 이미 채택한 규칙으로 승격하지 않는다.

다음 추천은 이 비교의 판단을 먼저 확인한 뒤 계획 42의 template `useToastStore` 실제 호출로 돌아가는 것이다. 이번에 나온 토스트를 연결점으로 삼되, 상태 범위·삭제 액션·타이머 수명을 누가 책임지는지라는 다른 판단을 본다. 오류 클래스·버튼 API를 더 설계하는 작업은 현재 요청 범위가 아니다. 01-02 전체 완료나 다른 영역 탐색 충분성을 선언하지 않는다.

## 후속 사용자 응답

> 맞아 나도 공감해 inter-persoan 는 더 큰 규모에서 적합한것 같고 정답은 아니고 다만 뭐 니말대로 fetcher 가 어딜 맡을지에 대한 책임 고려나 뭐 그런 부분이 중요해보여

사용자는 규모·상황에 따른 적합성과 책임 경계 고려에 공감하고 template useToastStore로 진행하도록 요청했다. 특정 클래스 체계·우선순위 API·수정안을 채택한 것으로 확대하지 않는다. 이후 실제 상태·타이머 책임은 기록 48에 보존한다.
