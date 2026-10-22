# 작업물 이해 브리핑 — 인증 인터셉터

이 코드는 **API 요청에 현재 로그인 세션의 access token을 붙이고, 토큰이 없거나 서버가 401을 돌려주면 refresh token으로 갱신해 요청을 이어 가는 장치**입니다. 동시에 요청을 시작한 세션과 응답을 받을 때의 세션이 같은지 확인합니다. 일반 API 클라이언트와 동기화 클라이언트 모두 이 함수를 등록해 사용합니다 (`auth-interceptor.ts:67-115`, `consumers.txt`의 `fetcher.ts`·`sync/api.ts`).

여기서 `sessionId`는 서버에 보내는 로그인 ID가 아닙니다. 앱 안에서 로그인 세대를 구분하는 `symbol`입니다. 로그아웃하거나 다시 로그인해 세대가 바뀌면, 이전 요청이 뒤늦게 끝나도 그 결과를 현재 세션의 결과로 받아들이지 않으려는 용도입니다. `assertCurrentSession`은 이 값이 store의 현재 세션과 맞고 상태가 `signed-in`인지 검사하며, 맞지 않으면 `AuthRequiredError`를 던집니다 (`auth-interceptor.ts:8-12`, `auth.ts`의 `isCurrentSession`).

대표적인 흐름은 이렇습니다.

1. **보내기 전:** 요청에 `sessionId`가 없으면 현재 store 값을 채웁니다. 앞서 본 `??=`가 바로 이 부분입니다. 이미 붙어 있는 값은 유지하므로, 재시도 중인 옛 요청을 새 로그인 세션의 요청으로 바꾸지 않습니다. 세션을 검사한 뒤 access token이 있으면 `Authorization: Bearer ...`를 붙여 보냅니다 (`auth-interceptor.ts:68-85`).
2. **access token이 없을 때:** `renewSession`이 현재 세션의 refresh token을 가져와 `/api/auth/refresh`로 새 토큰을 요청합니다. 받은 토큰을 store와 기기 저장소에 반영한 뒤, 요청 인터셉터가 새 access token을 헤더에 붙입니다. refresh 요청은 인증 인터셉터가 없는 `authAxios`를 사용하므로 자기 자신을 다시 호출하지 않습니다 (`auth-interceptor.ts:25-64`, `auth-transport.ts`, `auth.ts`의 `refreshTokens`).
3. **서버가 401을 반환할 때:** 실패한 요청의 세션을 다시 확인하고, 아직 재시도하지 않았다면 토큰을 갱신한 뒤 `client(request)`로 **같은 요청을 한 번 더 보냅니다**. 이때 요청 인터셉터가 다시 실행되어 새 토큰을 헤더에 넣습니다. `authRetried` 표시가 있으므로 재전송도 401이면 더 반복하지 않고 재로그인이 필요한 상태로 전환합니다 (`auth-interceptor.ts:92-110`).
4. **응답을 받을 때:** 성공 응답도 세션을 검사합니다. 요청 도중 로그아웃·다른 로그인이 일어났다면 그 응답을 그대로 호출자에게 전달하지 않고 인증 오류로 막습니다 (`auth-interceptor.ts:87-90`).

예를 들어 같은 세션에서 요청 A와 B가 거의 동시에 토큰 갱신을 필요로 하면, `refreshes` Map이 `sessionId`별로 진행 중인 갱신 Promise를 보관합니다. 둘은 같은 갱신을 기다리고, 완료되면 Map 항목을 지웁니다 (`auth-interceptor.ts:25-29, 61-63`).

실패도 종류별로 다룹니다. refresh token이 없거나 **refresh 요청 자체가** 401·403으로 거부되면 `requireReauthentication`이 메모리의 토큰을 먼저 비우고 `reauth-required` 상태로 만든 다음 저장을 시도합니다. 반면 refresh 요청의 네트워크 장애나 서버 오류는 자격 증명 거부로 단정하지 않고 원래 오류를 올립니다. 일반 API 요청의 401 이외 오류도 여기서는 그대로 올립니다 (`auth-interceptor.ts:34-58, 92-96`, `auth.ts`의 `requireReauthentication`).

이 설명은 제공된 **2026-09-22 보존 코드와 사용처 발췌로 재구성한 흐름**입니다. 실제 앱 실행을 관찰한 결과나 이후 코드의 현재 동작을 확인한 것은 아닙니다.
