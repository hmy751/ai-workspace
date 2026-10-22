## 작업물 이해 브리핑 — 인증 인터셉터

이 코드는 **API 요청에 현재 로그인 세션의 access token을 붙이고, 토큰이 없거나 서버가 401을 돌려주면 refresh token으로 갱신한 뒤 요청을 다시 보내는 장치**예요. 갱신할 수 없을 때는 다시 로그인이 필요하다는 `AuthRequiredError`를 냅니다. 아래 설명은 질문 당시 제공된 코드에서 재구성한 흐름이며, 앱에서 실제 실행한 결과는 아닙니다.

핵심은 `sessionId`를 토큰과 함께 확인한다는 점입니다. 이것은 서버에 보내는 ID가 아니라, 앱 안에서 로그인 세대를 구별하는 `symbol`입니다. 로그인하거나 로그아웃하는 등 세션이 바뀌면 이전 요청이 나중에 돌아와도 현재 세션의 결과처럼 취급하지 않으려는 검사입니다. `auth.ts`의 `isCurrentSession`은 ID가 현재 세대와 일치하고 상태가 `signed-in`인지 확인하며, `getAccessToken`과 `getRefreshToken`도 그 조건에서만 토큰을 돌려줍니다.

일반 요청 하나를 따라가면 이렇습니다.

1. `setupAuthInterceptors(client)`가 Axios의 **요청 전**과 **응답 후**에 검사 함수를 등록합니다. 일반 API 클라이언트와 sync 클라이언트가 이 함수를 사용합니다.
2. 요청 전에 `config.sessionId ??= ...`로 현재 세션 ID를 요청에 기록합니다. 이미 ID가 있으면 유지하므로 재전송할 때도 원래 요청의 세션을 추적할 수 있습니다. 이어 `assertCurrentSession`이 현재 로그인과 맞는지 확인합니다.
3. access token이 있으면 `Authorization: Bearer <토큰>` 헤더를 붙여 보냅니다. 없으면 `renewSession`으로 refresh token을 교환하고, 다시 세션과 access token을 확인한 뒤 보냅니다.
4. 응답이 성공해도 요청에 기록한 세션이 여전히 현재 세션인지 확인합니다. 기다리는 사이 로그아웃하거나 다른 세션으로 바뀌었다면 성공 응답을 그대로 전달하지 않고 인증 오류를 냅니다.

서버가 **401**을 돌려준 경우에는 요청을 한 번만 더 시도합니다. `authRetried`가 아직 없으면 이를 `true`로 표시하고, `renewSession`으로 토큰을 갱신한 뒤 `client(request)`로 같은 요청을 재전송합니다. 재전송도 401이면 `rejectCredentials`가 재인증 필요 상태로 바꾸고 `AuthRequiredError`를 던집니다. 예를 들어 access token이 만료됐지만 refresh token이 유효하면 첫 요청의 401 → 토큰 갱신 → 새 토큰을 붙인 재요청으로 이어집니다. 401이 아닌 응답 오류는 이 인증 재시도 경로에서 그대로 다시 던집니다.

`renewSession` 안의 `refreshes` Map은 **같은 세션에서 동시에 여러 요청이 갱신을 요구할 때** 하나의 갱신 Promise를 공유하게 합니다. 실제 토큰 교환은 인증 인터셉터가 없는 `authAxios`로 `/api/auth/refresh`에 요청하고, 돌아온 토큰은 auth store의 `refreshTokens`가 기기에 저장한 다음 현재 세션에 적용합니다. 저장 전후에 세션이 바뀌면 새 토큰을 이전 세션의 것으로 적용하지 않습니다.

실패도 구별합니다. refresh token이 없거나 갱신 API가 401/403으로 토큰을 거부하면 `requireReauthentication`이 메모리의 토큰을 먼저 비우고 상태를 `reauth-required`로 바꿉니다. 네트워크 오류나 서버 장애처럼 자격 증명 거부로 볼 수 없는 오류는 그 원래 오류를 전달합니다. 일반 API 쪽 `fetcher.ts`는 `AuthRequiredError`를 그대로 전달하고, sync 클라이언트에는 별도의 5xx 재시도 처리도 붙어 있습니다.

따라서 이 코드의 큰 흐름은 **현재 세션 확인 → 토큰 준비 → 요청 → 성공 시 세션 재확인, 401이면 갱신 후 한 번 재요청**입니다. `setupSyncAuthInterceptors`는 별도 구현이 아니라 같은 함수를 가리키는 이름입니다. 여기서 설명한 것은 제공된 소스와 연결 코드의 동작이며, 서버가 어떤 경우에 401/403을 반환하는지나 실제 네트워크 실행 결과까지 확인한 뜻은 아닙니다.
