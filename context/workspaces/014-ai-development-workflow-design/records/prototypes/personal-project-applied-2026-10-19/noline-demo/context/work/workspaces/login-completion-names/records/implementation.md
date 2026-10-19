# 구현자 인계: 이름과 두 내부 사용처

> 아래는 가상 구현자의 인계 기록이다. 변경과 관찰은 설명을 위한 가정이며 실제 제품 코드 수정이나 실행 로그가 아니다. 검토 뒤 결과로 이 초기 인계를 덮어쓰지 않는다.

`loginAndRefresh`를 `signInAndRequestRefresh`, `callbacks.onCompleted`를 `callbacks.onSignedIn`으로 바꾸고 짧은 계약 설명과 두 내부 사용처의 연결을 맞춘 장면이다. 표시 문구를 포함한 완료 표현의 전체 대조는 검토에 남겼다. 이 인계만으로 작업 완료를 권고하지 않는다.

## 왜 이 이름을 골랐는가

[Ticket](../current/ticket.md)의 목표는 실제 책임과 완료 표현을 맞추는 것이다. Main이 별도 입력으로 전달한 [개인 개발 공통](../../../../../../personal-context/development/README.md)·[이름 상세](../../../../../../personal-context/development/naming-and-completion.md)는 표현 수단과 변경 이득·비용을 판단하는 데 사용했다. [Project 인증 가이드](../../../../project/guidance/authentication-and-session.md)와 [표현 가이드](../../../../project/guidance/code-readability.md)는 인증 적용·후속 조회·화면 완료에서 지킬 약속을 제공한다. Project가 개인 기준을 채택하거나 이번 개명 답을 미리 제시한 것은 아니다.

초기 입력에는 내부 사용처가 두 곳이고, 인터페이스·호출부에 완료 범위 설명이 없으며 LoginScreen은 화면 갱신 완료까지 표시한다는 가정이 있다. 이름을 그대로 두고 가까운 계약 설명을 보완하면 호환 변경 없이 의미를 전달할 수 있다. 이번에는 두 사용처의 변경 비용이 제한적이고 호출부 이름에서도 오독을 줄일 이득이 있다고 판단해 개명과 짧은 설명을 함께 선택했다. 공개 API라면 변경 비용이 달라져 이름 유지가 타당할 수 있다는 개인 기준의 대비를 이번 사실로 혼동하지 않았다.

가정한 서비스는 전체 세션 조율부터 인증 적용까지 기다린다. 그 뒤 wrapper가 조회 갱신을 요청하므로 `RequestRefresh`는 재조회 완료까지 기다린다는 오해를 줄이고, `onSignedIn`은 인증 적용 뒤라는 의미를 드러낸다. 이름에 맞춰 조회 완료까지 기다리는 안은 callback·화면 시점·실패 의미를 바꾸므로 이번 범위에서 선택하지 않았다. 두 이름은 이 코드와 조건에서 고른 표현이며 다른 함수의 필수 어휘가 아니다.

## 구현자 변경판

```ts
type LoginCallbacks = {
  // 인증 적용 뒤 호출한다. 재조회·화면 반영 완료는 보장하지 않는다.
  onSignedIn: () => void;
  onRefreshError: (error: unknown) => void;
};

// 전체 인증 서비스를 마친 뒤 조회 갱신을 요청한다.
async function signInAndRequestRefresh(
  input: LoginInput,
  callbacks: LoginCallbacks,
): Promise<void> {
  await loginService.signIn(input);
  void queryClient
    .invalidateQueries({ queryKey: ["session-data"] })
    .catch(callbacks.onRefreshError);
  callbacks.onSignedIn();
}

// LoginScreen
signInAndRequestRefresh(input, {
  onSignedIn: () => {
    showStatus("로그인과 화면 갱신 완료");
    navigateAfterSignIn();
  },
  onRefreshError: showQueryRefreshError,
});

// ReauthDialog
signInAndRequestRefresh(input, {
  onSignedIn: () => closeDialog(),
  onRefreshError: showQueryRefreshError,
});
```

서비스를 기다리는 지점, Query를 기다리지 않는 지점, `onRefreshError`와 callback 소비자의 역할은 보존했다. `void`를 유지한 것은 기존 예시의 동작을 바꾸지 않기 위해서다. [시작 입력](../../../../../../scenario-input.md)과 같이 Query 실패는 Promise rejection으로 오고 두 callback은 정상 반환하며 다시 던지지 않는다고 가정한다. 실제 라이브러리 설정을 검증하거나 동기 throw 등 생략한 실패 경로를 새로 정의한 것은 아니다.

## 확인 계획과 인계의 한계

| 실제 적용 때 확인할 것 | 이 장면에서 가정한 변경·남은 확인 |
| --- | --- |
| 함수·callback 참조와 타입 연결을 찾아 이전 식별자가 남았는지 대조 | 두 내부 사용처의 식별자를 바꿨다고 가정한다. 실제 검색·타입 검사는 하지 않았다. |
| 서비스의 해소 시점과 Query 요청·callback 호출 순서 | 제시한 발췌에서는 호출 순서와 대기를 바꾸지 않았다. 실제 서비스 구현의 보장은 미확인이다. |
| Query가 늦거나 실패할 때 callback·오류 담당·인증 상태 | 확인 계획만 넘긴다. 실제 실행 결과는 없다. |
| 소비자가 알리는 완료 범위 | 표시 문구까지 전체 대조하지 않은 상태로 검토에 넘기는 장면이다. |

검토자는 원요구와 계약, 변경 전후와 두 사용처를 직접 대조한다. 기존 범위 안의 이름·표현 문제는 직접 고치고 [검토 기록](review.md)에 남긴다. 대기·실패 분류·화면 정책 또는 외부 API 호환성을 바꿀 필요가 생기면 Main에게 돌려준다. 실제 Noline 코드·OAuth·기기 저장·화면 동작은 이 시안에서 확인하지 않았다.
