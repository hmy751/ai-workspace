# 작업물 이해 브리핑 — 인증 인터셉터

이 코드는 **API 요청에 현재 로그인 세션의 access token을 붙이고**, 토큰이 없거나 서버가 `401`을 돌려주면 refresh token으로 갱신한 뒤 요청을 이어 가는 장치예요. 그 사이에 로그아웃하거나 다른 계정으로 로그인했다면, 예전 요청의 결과가 새 세션에 섞이지 않도록 막습니다. 제공된 2026-09-22 코드에서 일반 API 클라이언트와 sync 클라이언트가 같은 `setupAuthInterceptors`를 등록하고 있습니다.

먼저 여기서 말하는 두 토큰과 `sessionId`를 구분하면 흐름이 쉬워집니다.

- **access token**: 일반 API 요청의 `Authorization: Bearer ...` 헤더에 넣는 값입니다.
- **refresh token**: access token을 새로 받기 위해 `/api/auth/refresh`에 보내는 값입니다. 이 호출은 인증 인터셉터가 없는 `authAxios`를 사용하므로, 갱신 요청이 다시 자기 자신을 갱신하려 들지 않습니다.
- **`sessionId`**: 토큰 문자열이 아니라, 앱 메모리에서 *이번 로그인 세대*를 구별하는 `symbol`입니다. 요청에 붙은 세대가 현재 로그인 세대인지 `auth.ts`의 `isCurrentSession`으로 검사합니다.

### 요청을 보낼 때

`setupAuthInterceptors(client)`의 첫 번째 `request.use`가 요청마다 실행됩니다.

```ts
config.sessionId ??= useAuthStore.getState().sessionId ?? undefined;
assertCurrentSession(config.sessionId);

if (!useAuthStore.getAccessToken(config.sessionId)) {
  await renewSession(config.sessionId);
}

assertCurrentSession(config.sessionId);
const accessToken = useAuthStore.getAccessToken(config.sessionId);
config.headers.Authorization = `Bearer ${accessToken}`;
```

앞서 물어보신 `??=` 줄은 요청에 `sessionId`가 **없을 때만** 현재 store의 값을 붙입니다. 재시도하는 요청에는 원래 `sessionId`가 남아 있으므로, 재시도 시점에 다른 사람이 로그인했더라도 새 세션으로 몰래 바뀌지 않습니다. 이어지는 `assertCurrentSession`은 값이 실제 현재 세션인지 검사하고, 아니면 `AuthRequiredError`를 던집니다.

access token이 있으면 그대로 헤더에 넣습니다. 없으면 `await renewSession(...)`으로 갱신이 끝날 때까지 기다립니다. `await` 중 로그아웃할 수도 있으므로 **기다린 뒤 다시 세션을 검사**하고 토큰을 다시 읽습니다. 그때도 토큰이 없다면 인증 오류로 끝납니다. 위 코드는 핵심 줄만 골랐고, 실제 코드에는 토큰이 끝내 없을 때의 검사도 있습니다.

예를 들어 설명용으로 현재 세대가 `S1`, access token이 `A1`이면 요청은 `Bearer A1`로 나갑니다. `A1`이 없고 refresh token `R1`만 있으면 `R1`을 교환해 새 토큰을 저장한 뒤, 새 access token으로 보냅니다. 갱신을 기다리는 동안 `S1`이 종료되어 새 세대 `S2`가 되면 `S1` 요청은 중단됩니다.

### 서버가 401을 보냈을 때

요청 당시 access token이 있었어도 서버가 이를 거절할 수 있습니다. 응답 오류 인터셉터는 **요청 정보가 있고 상태가 `401`일 때만** 다음 처리를 합니다. 다른 오류는 그대로 던집니다.

1. 원래 요청의 `sessionId`가 아직 현재 세션인지 확인합니다.
2. `authRetried`가 이미 `true`라면 재시도를 멈추고 재로그인이 필요한 상태로 전환합니다.
3. 처음 받은 `401`이면 원래 요청에 `authRetried = true`를 표시하고 `renewSession`으로 토큰을 갱신합니다.
4. 갱신 후 세션을 다시 확인하고 `client(request)`로 **원래 요청을 한 번 더** 보냅니다. 이때 요청 인터셉터가 다시 실행되어 저장된 새 access token을 헤더에 붙입니다.

즉 `authRetried`는 `401 → 갱신 → 재요청 → 또 401`의 무한 반복을 막는 표식입니다. 정상 응답에도 세션 검사가 있어서, 응답이 돌아오기 전에 로그아웃했다면 이전 세션의 성공 결과를 호출자에게 넘기지 않습니다.

### 여러 요청이 동시에 갱신하려 할 때

`refreshes`는 `sessionId`별로 **진행 중인 갱신 Promise 하나**를 보관하는 `Map`입니다. 같은 세대의 요청 여러 개가 동시에 토큰이 없음을 발견하거나 `401`을 받으면, 첫 요청만 갱신을 시작하고 나머지는 그 Promise를 함께 기다립니다. 끝나면 `finally`에서 Map 항목을 지웁니다. 따라서 이후의 별도 `401`에는 새 갱신을 시도할 수 있습니다. `Map<symbol, Promise<void>>`에서 `void`인 이유는 갱신된 토큰을 Promise 결과로 나누어 주는 대신, 갱신 후 각 요청이 store에서 토큰을 다시 읽기 때문입니다.

### 갱신이 실패하면

`renewSession`은 현재 세대인지 확인하고 refresh token을 가져와 `refreshTokens`로 교환합니다. refresh token이 없거나 교환 요청이 `401`/`403`이면 `rejectCredentials`가 `requireReauthentication`을 호출합니다. `auth.ts`에서는 이때 토큰을 메모리에서 먼저 지우고 세대를 바꾸며 상태를 `reauth-required`로 만듭니다. 저장 작업이 실패해도 API 호출자에게는 `AuthRequiredError`를 던집니다.

반면 네트워크 끊김이나 서버 장애처럼 **자격 증명이 거부됐다고 볼 근거가 없는 오류**는 원래 오류를 다시 던집니다. 이 경로에서는 이 코드만으로 재로그인 필요 상태로 바꾸지 않습니다. 갱신 결과를 저장하는 동안 세대가 바뀌면 store의 `refreshTokens`가 `false`를 반환하고, 예전 요청은 인증 오류로 끝납니다.

이 설명은 제공된 당시 source와 연결 위치로 재구성한 동작입니다. 앱을 실행해 실제 요청 순서나 서버 응답을 관찰한 결과는 아닙니다.
