이 코드는 **API 요청에 로그인 토큰을 붙이고, 토큰이 거부되면 갱신해서 요청을 한 번 다시 보내는 공통 처리**예요. 여기에 **요청 도중 로그아웃하거나 다시 로그인했을 때, 이전 요청의 결과를 받아들이지 않도록 하는 검사**도 들어 있습니다.

붙여준 코드와 당시 보존된 관련 코드를 기준으로 설명할게요. 실제 앱을 실행해서 관찰한 결과는 아닙니다. `work-artifact-briefing` 스킬의 기준을 적용해, 전체 흐름부터 살펴봤어요.

### 1. 먼저 세 가지 값을 구분하면 쉬워요

| 값 | 의미 | 쓰는 곳 |
| --- | --- | --- |
| `accessToken` | API를 호출할 때 서버에 보내는 인증 토큰 | `Authorization` 헤더 |
| `refreshToken` | 새 토큰을 발급받을 때 서버에 보내는 토큰 | 토큰 갱신 API |
| `sessionId` | 이 요청이 앱의 어느 로그인 세션에서 시작됐는지 구분하는 값 | 앱 내부의 세션 검사 |

**`sessionId`는 서버에 보내는 인증 토큰이 아니에요.** 이 코드에서는 요청 설정인 `config`에 보관합니다.

관련 [auth.ts](/private/tmp/0402-auth-body-20261022/r74/code/auth.ts)의 `saveAndApplySession`을 보면 로그인 세션을 적용할 때 `Symbol('session')`을 새로 만들어요. `Symbol`은 설명 문자열이 같아도 생성할 때마다 다른 값입니다.

```ts
Symbol('session') === Symbol('session') // false
```

그래서 같은 계정으로 다시 로그인해도 이전 요청과 새 요청을 구분할 수 있어요.

### 2. `setupAuthInterceptors`는 요청 전후에 실행할 함수를 등록해요

```ts
setupAuthInterceptors(client);
```

이 함수 자체가 API를 호출하는 건 아니에요. 전달받은 Axios 클라이언트에 다음 처리를 등록합니다.

```text
API 호출
  → request interceptor: 세션 확인, 토큰 준비, 헤더 추가
  → 서버로 전송
  → response interceptor: 성공 응답 검사 또는 401 처리
  → 호출한 쪽에 결과나 오류 전달
```

실제 사용처에서는 일반 API 클라이언트와 동기화 클라이언트 양쪽에 등록하고 있어요. 마지막 줄의 `setupSyncAuthInterceptors = setupAuthInterceptors`는 **동기화에서도 같은 함수를 다른 이름으로 쓰겠다**는 뜻입니다. ([사용처 발췌](/private/tmp/0402-auth-body-20261022/r74/code/consumers.txt))

### 3. 요청을 보내기 전에는 이렇게 움직여요

```ts
config.sessionId ??= useAuthStore.getState().sessionId ?? undefined;
assertCurrentSession(config.sessionId);
```

처음 보내는 요청이면 현재 로그인 세션의 ID를 요청에 넣습니다. 이미 ID가 있으면 유지해요. **재전송할 때도 처음 요청을 시작한 세션을 유지하는 것**이 중요합니다.

`assertCurrentSession`은 그 ID가 현재 로그인된 세션인지 검사해요. 관련 Store의 `isCurrentSession`은 ID 일치뿐 아니라 로그인 상태가 `signed-in`인지도 확인합니다. 유효하지 않으면 `AuthRequiredError`를 던져서 처리를 중단해요.

다음은 토큰 준비입니다.

```ts
if (!useAuthStore.getAccessToken(config.sessionId)) {
  await renewSession(config.sessionId);
}
```

- access token이 있으면 그대로 진행합니다.
- access token이 없으면 토큰 갱신이 끝날 때까지 기다립니다.

여기서는 토큰의 **존재 여부**를 확인해요. 만료 시각을 미리 검사하는 코드는 아닙니다. 토큰이 있어도 서버가 거부하면 뒤의 401 처리로 넘어갑니다.

그다음 세션을 다시 확인하고, 토큰을 읽어 헤더에 넣습니다.

```ts
assertCurrentSession(config.sessionId);

const accessToken = useAuthStore.getAccessToken(config.sessionId);
if (!accessToken) {
  throw new AuthRequiredError();
}

config.headers.Authorization = `Bearer ${accessToken}`;
return config;
```

`await`로 기다리는 동안 로그아웃할 수도 있어서 세션을 다시 확인하는 거예요. 마지막 `return config`까지 도달하면, Axios가 이 설정으로 서버에 요청을 보냅니다.

### 4. `renewSession`은 토큰을 갱신하고, 중복 갱신을 합쳐요

```ts
const refreshes = new Map<symbol, Promise<void>>();
```

이 Map에는 **세션별로 현재 진행 중인 갱신 작업**을 보관합니다. `Promise<void>`는 “완료를 기다릴 수 있지만, 성공 결과로 별도 값을 돌려주지는 않는 비동기 작업”이라는 뜻이에요. 새 토큰은 반환받는 대신 Store에 저장합니다.

설명용으로 요청 세 개가 거의 동시에 갱신을 시도한다고 해볼게요.

```text
첫 요청: 갱신 작업을 시작하고 Map에 저장
둘째 요청: 같은 세션의 진행 중인 작업을 발견 → 그 작업을 기다림
셋째 요청: 같은 세션의 진행 중인 작업을 발견 → 그 작업을 기다림
```

따라서 **같은 세션에서 갱신이 진행 중이면 그 작업을 공유**합니다. 끝난 뒤 새로 갱신을 요청하면 다시 실행될 수 있어요.

새 갱신 작업 안에서는 다음 순서로 처리합니다.

1. 현재 세션인지 확인합니다.
2. refresh token을 읽습니다. 없으면 재로그인이 필요한 상태로 바꿉니다.
3. `refreshTokens(refreshToken)`으로 서버에 새 토큰을 요청합니다.
4. 받은 토큰을 Store의 `refreshTokens(tokens, sessionId)`로 저장·적용합니다.

이름이 비슷하지만 3번은 **서버 통신 함수**, 4번은 **Store 갱신 함수**예요. Store 함수는 기기에 저장하기 전후로 세션이 여전히 같은지 확인하고, 적용할 수 없으면 `false`를 반환합니다. 그러면 인터셉터는 인증 오류를 던집니다. ([auth-transport.ts](/private/tmp/0402-auth-body-20261022/r74/code/auth-transport.ts), [auth.ts](/private/tmp/0402-auth-body-20261022/r74/code/auth.ts)의 `refreshTokens`)

갱신 API는 이 인증 인터셉터가 없는 별도 `authAxios`를 사용해요. 갱신 요청이 다시 이 갱신 로직에 들어가는 일을 피하는 구조입니다.

```ts
renewal.finally(() => refreshes.delete(sessionId)).catch(() => undefined);
```

이 줄은 성공하든 실패하든 Map에서 작업을 제거해요. 뒤의 `catch`는 `finally`가 만든 별도 Promise의 오류를 처리합니다. **호출자에게 반환하는 `renewal`의 실패까지 없애지는 않아요.**

### 5. 서버 응답이 오면 성공과 401을 나눠 처리해요

**성공 응답이어도 세션을 확인합니다.**

```ts
(response) => {
  assertCurrentSession((response.config as AuthRequest).sessionId);
  return response;
}
```

예를 들어, 세션 A에서 요청을 보낸 뒤 로그아웃하고 세션 B로 다시 로그인했다고 해볼게요. 늦게 도착한 A의 성공 응답은 현재 세션과 ID가 다르므로 오류로 바뀝니다. 서버에서 이미 수행한 작업을 취소하는 것은 아니고, **그 응답을 성공 결과로 호출자에게 넘기는 것을 막습니다.**

**실패 응답이 401이면 토큰을 갱신하고 재전송합니다.**

```ts
if (!request || error.response?.status !== 401) {
  throw error;
}
```

요청 정보가 없거나 401이 아니면, 이 인증 처리에서는 원래 오류를 그대로 넘깁니다.

401이면 현재 세션인지 확인한 다음 `authRetried`를 봐요.

```ts
if (request.authRetried) {
  return rejectCredentials(request.sessionId);
}

request.authRetried = true;
await renewSession(request.sessionId);
assertCurrentSession(request.sessionId);
return client(request);
```

`authRetried`는 **이 요청이 401 때문에 이미 재전송됐는지** 표시합니다. 다음 흐름이 됩니다.

```text
첫 요청 → 401
  → authRetried를 true로 설정
  → 토큰 갱신
  → 같은 요청을 다시 전송
      → 성공: 결과 반환
      → 또 401: 재로그인 필요 처리
```

`client(request)`는 같은 Axios 클라이언트로 다시 호출하므로 요청 인터셉터도 다시 통과합니다. 이때 기존 `sessionId`는 유지하고, Store에서 새 access token을 읽어 헤더를 다시 붙여요. `authRetried` 때문에 401 재전송이 무한 반복되지는 않습니다.

### 6. 갱신 실패가 전부 재로그인으로 이어지는 건 아니에요

| 상황 | 이 코드의 처리 |
| --- | --- |
| 갱신에 필요한 refresh token이 없음 | 재로그인 필요 처리 |
| 갱신 API가 401 또는 403 반환 | 재로그인 필요 처리 |
| 갱신 후 재전송한 원래 요청이 다시 401 반환 | 재로그인 필요 처리 |
| 갱신 API에서 네트워크 오류나 서버 장애 발생 | 세션이 여전히 같다면 원래 오류 전달 |

여기서 `rejectCredentials`는 Store의 `requireReauthentication`을 호출합니다. 해당 Store 구현은 **메모리의 두 토큰을 비우고 상태를 `reauth-required`로 바꾼 뒤 기기에 저장**해요. 사용자 정보와 로컬 계정은 남습니다.

기기 저장이 실패해도 메모리에서는 이미 인증 요청이 차단된 상태이고, 호출자에게는 `AuthRequiredError`를 전달합니다. 다만 실제 로그인 화면을 띄우는 동작은 이 함수 안에 없어요. 이 코드는 재로그인이 필요한 상태와 오류를 만드는 역할까지 담당합니다.
