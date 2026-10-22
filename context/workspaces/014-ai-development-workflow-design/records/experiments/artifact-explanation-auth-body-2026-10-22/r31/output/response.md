이 코드는 **API 요청에 로그인 토큰을 붙이고, 인증이 만료되면 토큰을 갱신해서 요청을 다시 보내는 공통 처리**예요. 여기에 **로그아웃·재로그인 전에 시작한 요청이 새 로그인 상태에 섞이지 않도록 검사하는 처리**도 들어 있습니다.

`work-artifact-briefing` 기준으로 연결된 인증 Store와 사용처까지 확인했어요. 아래는 2026-09-22에 보존된 코드에서 재구성한 동작이며, 앱을 실행해 관찰한 결과는 아닙니다.

먼저 등장하는 값 세 가지를 구분하면 읽기 쉬워져요.

| 값 | 하는 일 |
| --- | --- |
| `accessToken` | 일반 API를 호출할 때 서버에 보내는 인증 토큰 |
| `refreshToken` | 새 토큰을 발급받을 때 서버에 보내는 토큰 |
| `sessionId` | 이 요청이 어느 로그인 상태에서 시작됐는지 구분하는 앱 내부 값 |

여기서 `sessionId`는 서버에 보내는 토큰이 아니에요. `Symbol('session')`로 만드는 고유한 값이고, 같은 계정으로 다시 로그인해도 새로운 값이 됩니다. 토큰을 갱신할 때는 이 값을 유지합니다. ([로그인 시 생성](/private/tmp/0402-auth-body-20261022/r31/code/auth.ts:152), [갱신 시 유지](/private/tmp/0402-auth-body-20261022/r31/code/auth.ts:206))

**1. `setupAuthInterceptors(client)`는 요청 전과 응답 후에 실행할 함수를 등록해요.**

인터셉터는 Axios가 요청을 보내거나 응답을 처리할 때 공통으로 거치는 함수예요. 이 함수를 호출하는 순간 API를 보내는 것은 아닙니다.

```ts
client.interceptors.request.use(/* 보내기 전에 실행 */);
client.interceptors.response.use(/* 성공 응답 처리 */, /* 실패 처리 */);
```

사용처를 보면 일반 API에는 `fetcher.ts`에서 등록하고, 동기화 API에는 `sync/api.ts`에서 등록합니다. 마지막 줄은 동기화용 이름도 같은 함수를 가리키게 한 거예요.

```ts
export const setupSyncAuthInterceptors = setupAuthInterceptors;
```

따라서 두 종류의 API가 같은 인증 규칙을 사용합니다. 사용 위치는 [보존된 사용처 발췌](/private/tmp/0402-auth-body-20261022/r31/code/consumers.txt)에 있어요.

**2. 요청을 보내기 전에는 세션을 확인하고 토큰을 붙여요.**

[요청 인터셉터](/private/tmp/0402-auth-body-20261022/r31/code/auth-interceptor.ts:68)를 순서대로 풀면 이렇습니다.

```ts
config.sessionId ??= useAuthStore.getState().sessionId ?? undefined;
```

앞에서 본 `??=`예요. 처음 보내는 요청에 `sessionId`가 없으면 현재 Store의 값을 기록합니다. 이미 값이 있으면 유지하므로, 나중에 같은 요청을 재전송해도 처음 시작한 세션에 속하게 됩니다.

```ts
assertCurrentSession(config.sessionId);
```

“이 요청이 현재 사용 가능한 로그인 세션에 속하나?”를 검사합니다. 아니면 `AuthRequiredError`를 던져 여기서 중단해요. Store에서는 ID 일치뿐 아니라 `status === 'signed-in'`과 사용자 일치도 확인합니다. ([실제 검사](/private/tmp/0402-auth-body-20261022/r31/code/auth.ts:244))

```ts
if (!useAuthStore.getAccessToken(config.sessionId)) {
  await renewSession(config.sessionId);
}
```

access token이 **없으면** 먼저 갱신합니다. 이 코드는 토큰의 만료 시각을 직접 검사하지 않아요. 토큰이 존재하면 일단 보내고, 서버가 `401`로 거부하면 뒤의 응답 처리에서 갱신합니다.

이후 세션을 다시 확인하고, Store에서 토큰을 다시 읽어서 붙입니다.

```ts
config.headers.Authorization = `Bearer ${accessToken}`;
return config;
```

예를 들어 토큰이 `abc`라면 요청 헤더에 `Authorization: Bearer abc`가 들어가요. `return config`로 준비된 설정을 넘기면 Axios가 요청을 계속 진행합니다.

중간에 `await`가 있으므로 기다리는 동안 로그아웃할 수 있어요. 그래서 갱신 전 확인만 믿지 않고 **기다린 뒤에도 세션을 다시 검사**하는 겁니다.

**3. `renewSession`은 새 토큰을 받아 저장하고, 겹친 갱신은 함께 기다리게 해요.**

[이 함수](/private/tmp/0402-auth-body-20261022/r31/code/auth-interceptor.ts:25)는 먼저 진행 중인 갱신을 찾아요.

```ts
const existing = refreshes.get(sessionId);
if (existing) {
  return existing;
}
```

`refreshes`는 “세션별로 지금 진행 중인 갱신 작업”을 담는 `Map`이에요. 값인 `Promise<void>`는 작업이 끝나거나 실패할 때까지 기다릴 수 있는 객체입니다.

예를 들어 같은 세션의 요청 A가 갱신을 시작했고, **아직 끝나기 전에** 요청 B도 갱신이 필요해졌다고 해볼게요. B는 새 갱신 요청을 만들지 않고 A의 Promise를 받아 함께 기다립니다. A의 갱신이 끝나면 둘 다 이어서 진행할 수 있어요. 모든 요청에 대해 영구히 한 번만 갱신한다는 뜻은 아닙니다.

진행 중인 작업이 없으면 다음 일을 시작합니다.

1. 현재 세션인지 확인합니다.
2. refresh token을 읽습니다. 없으면 재로그인이 필요한 상태로 바꿉니다.
3. refresh token으로 서버에 새 토큰을 요청합니다.
4. 새 토큰을 Store를 통해 기기에 저장하고 메모리에 적용합니다. 해당 세션에 적용하지 못해 `false`가 반환되면 인증 오류를 던집니다.

여기에는 이름이 같은 함수가 두 개 나와요.

```ts
tokens = await refreshTokens(refreshToken);
```

이것은 **서버에 요청하는 함수**예요. `auth-transport.ts`에서 `/api/auth/refresh`를 호출하고 응답 형식을 검증합니다. 이때는 인증 인터셉터가 없는 `authAxios`를 사용하므로, 갱신 요청이 다시 이 갱신 처리로 들어가는 순환을 피합니다. ([서버 요청 함수](/private/tmp/0402-auth-body-20261022/r31/code/auth-transport.ts:8), [Axios 구성 발췌](/private/tmp/0402-auth-body-20261022/r31/code/consumers.txt))

```ts
const saved = await useAuthStore.getState().refreshTokens(tokens, sessionId);
```

이것은 **받아온 토큰을 저장·적용하는 Store 함수**예요. 저장 전후에 세션이 여전히 일치하는지 확인합니다. ([저장 함수](/private/tmp/0402-auth-body-20261022/r31/code/auth.ts:206))

작업이 끝나면 다음 코드가 Map에서 그 작업을 지웁니다.

```ts
renewal.finally(() => refreshes.delete(sessionId)).catch(() => undefined);
```

성공·실패 어느 쪽이든 정리해 다음 갱신을 시작할 수 있게 해요. 끝의 `catch`는 이 정리 과정에서 파생된 Promise의 실패를 처리합니다. 호출자에게 반환하는 것은 원래 `renewal`이므로 **갱신 실패 자체가 성공으로 바뀌지는 않습니다.**

**4. 응답이 오면 성공 여부와 `401`에 따라 처리해요.**

[응답 인터셉터](/private/tmp/0402-auth-body-20261022/r31/code/auth-interceptor.ts:87)의 성공 함수는 세션을 검사한 뒤 응답을 그대로 넘깁니다.

```ts
assertCurrentSession((response.config as AuthRequest).sessionId);
return response;
```

서버가 성공을 반환해도 기다리는 동안 세션이 바뀌었다면 인증 오류로 처리해요. 이것은 **도착한 응답을 호출자에게 넘기지 않는 처리**입니다. 서버에서 이미 수행한 작업을 취소하는 코드는 아니에요.

실패 함수에서는 `401`만 토큰 갱신 대상으로 다룹니다.

```ts
if (!request || error.response?.status !== 401) {
  throw error;
}
```

원래 요청 정보가 없거나, `401` 이외의 오류라면 이 인증 처리에서는 그대로 넘깁니다.

처음 `401`을 받았다면 다음 순서로 진행해요.

```ts
request.authRetried = true;
await renewSession(request.sessionId);
assertCurrentSession(request.sessionId);
return client(request);
```

`authRetried`에 “이 요청은 인증 갱신 후 재시도를 한 요청”이라고 표시하고, 토큰을 갱신한 뒤 같은 요청을 다시 보냅니다. `client(request)`도 요청 인터셉터를 다시 거치므로 새 토큰이 헤더에 들어갑니다.

그 재전송마저 `401`이면 `authRetried`가 이미 `true`이므로 갱신을 반복하지 않고 `rejectCredentials`를 호출합니다.

설명용 값으로 한 요청을 따라가면 이래요. 현재 세션이 S1이고 access token이 T1이라고 가정하겠습니다.

1. 요청에 S1을 기록하고 T1을 붙여 보냅니다.
2. 서버가 `401`을 반환합니다.
3. `authRetried = true`로 표시하고, refresh token으로 새 토큰 T2를 받습니다.
4. S1이 여전히 현재 세션인지 확인하고, T2를 붙여 같은 요청을 다시 보냅니다.
5. 성공하면 응답을 넘깁니다. 다시 `401`이면 재로그인이 필요한 상태로 전환합니다.

3번을 기다리는 중 로그아웃하거나 재로그인해서 S1이 더 이상 현재 세션이 아니게 되면, 이전 요청은 인증 오류로 끝납니다. 앞의 `??=`가 기존 S1을 유지하는 이유도 여기에 있어요.

**5. “갱신 실패”가 항상 “로그인 해제”를 뜻하지는 않아요.**

이 코드가 구분하는 조건은 다음과 같습니다.

| 조건 | 인증 처리 결과 |
| --- | --- |
| 갱신에 쓸 refresh token이 없음 | 재로그인 필요 상태로 전환 |
| 토큰 갱신 서버가 `401` 또는 `403` 반환 | 재로그인 필요 상태로 전환 |
| 갱신 후 재전송한 일반 요청도 `401` 반환 | 재로그인 필요 상태로 전환 |
| 토큰 갱신 중 연결 실패·서버 장애 | 세션이 그대로라면 해당 오류를 전달하고, 이 이유만으로 토큰을 지우지는 않음 |
| 요청의 세션이 현재 세션과 다름 | 이전 요청을 인증 오류로 중단하고 현재 세션은 건드리지 않음 |

일반 API에서 바로 받은 `403`은 위의 “토큰 갱신 서버가 반환한 `403`”과 다릅니다. 일반 요청의 응답 처리에서는 `401`만 갱신 대상으로 삼아요.

`rejectCredentials`가 부르는 Store의 `requireReauthentication`은 access·refresh token을 비우고, 세션 ID를 바꾸며, 상태를 `reauth-required`로 만듭니다. 사용자 ID와 사용자 정보는 유지합니다. 메모리 차단을 먼저 하고 기기에 저장하므로, 저장에 실패해도 이 실행 중 이전 인증을 다시 허용하지 않아요. `rejectCredentials`는 그 저장 실패를 기록한 뒤 호출자에게 `AuthRequiredError`를 던집니다. ([상태 전환](/private/tmp/0402-auth-body-20261022/r31/code/auth.ts:225), [오류 처리](/private/tmp/0402-auth-body-20261022/r31/code/auth-interceptor.ts:14))

마지막으로 타입 문법 몇 가지도 동작과 연결해 보면 좋아요.

- `sessionId?: symbol`: 요청에 `sessionId`가 없을 수도 있다는 뜻입니다.
- `asserts sessionId is symbol`: 함수가 오류 없이 끝났다면 TypeScript가 이후의 `sessionId`를 `undefined`가 아닌 `symbol`로 취급하게 합니다. 실제 검사는 함수 안의 `if`가 해요.
- `Promise<never>`: 비동기 함수가 정상 값을 반환해 끝나지 않는다는 뜻입니다. 여기서는 마지막에 반드시 오류를 던집니다.
- `as AuthRequest`: TypeScript에 그 타입으로 취급하라고 알려줍니다. 실행 중 값을 검사하거나 바꾸는 코드는 아닙니다.
