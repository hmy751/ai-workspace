export function createAuthenticationService({
  requestAuthentication,
  waitForActiveWork,
  deviceSession,
}) {
  return {
    async signIn(credentials) {
      const session = await requestAuthentication(credentials);
      // 실제 sync·cleanup·DB 조율기의 연결 위치다. 이 예시는 대기 경계만 실행한다.
      await waitForActiveWork();
      return deviceSession.applyAuthentication(session);
    },
  };
}

export function createSignInAndRequestRefresh({
  authenticationService,
  requestSessionRefresh,
  onRefreshError,
}) {
  return async function signInAndRequestRefresh(credentials, { onSignedIn }) {
    const session = await authenticationService.signIn(credentials);

    // 요청은 인증 뒤에 시작하되 재조회 결과는 인증 완료를 막지 않는다.
    // 두 callback은 오류를 다시 던지지 않는 소비자 계약을 갖는다.
    try {
      Promise.resolve(requestSessionRefresh()).catch(onRefreshError);
    } catch (error) {
      onRefreshError(error);
    }

    onSignedIn(session);
    return session;
  };
}
