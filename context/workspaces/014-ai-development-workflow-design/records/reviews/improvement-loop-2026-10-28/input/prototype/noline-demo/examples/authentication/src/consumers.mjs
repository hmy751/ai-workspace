export function createLoginConsumer({
  signInAndRequestRefresh,
  showMessage,
  navigateToTrips,
}) {
  return function submitLogin(credentials) {
    return signInAndRequestRefresh(credentials, {
      onSignedIn() {
        showMessage("로그인 완료");
        navigateToTrips();
      },
    });
  };
}

export function createReauthConsumer({
  signInAndRequestRefresh,
  showMessage,
  closeDialog,
}) {
  return function submitReauthentication(credentials) {
    return signInAndRequestRefresh(credentials, {
      onSignedIn() {
        showMessage("인증을 복구했어요");
        closeDialog();
      },
    });
  };
}
