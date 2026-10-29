# 작업 시작 입력 — 인증 흐름의 이름과 완료 경계

> 이 문서는 이번 프로토타입에 부여한 초기 문제와 코드 가정이다. 기존 Noline의 실제 과거 코드나 커밋을 복원한 것이 아니다. 아래 발췌는 비교 입력이고, 현재 실행 가능한 구현은 [데모 소스](../../../../../examples/authentication/src/authentication.mjs)에 있다. 작업 후 이름과 검토는 [Work 현재 상태](../current/state/index.md)에 따로 남긴다. 이 시작 입력을 사후 결과로 덮어쓰지 않는다. 작업 후 Project 현황은 [현재 연결](../../../../project/current/authentication-flow/INDEX.md)에 있다.

## 현재 책임과 사용처

| 단위 | 이 예시에서 맡는 일 |
| --- | --- |
| `loginService.signIn` | 전체 세션 변경 서비스를 거쳐 진행 중 작업을 조율하고 계정·DB·queue 확인, 기기 저장, `signed-in` 적용을 마친다. 실패하면 기존 계약에 맞게 전달한다. Query 갱신은 이 함수에 들어 있지 않다. |
| `loginAndRefresh` | 위 서비스를 기다린 뒤 Query 무효화를 시작하고 재조회를 기다리지 않은 채 `onCompleted`를 부른다. |
| `LoginScreen` | `onCompleted`에서 기존 화면으로 이동한다. `onRefreshError`에서 후속 조회 실패를 처리한다. |
| `ReauthDialog` | `onCompleted`에서 재인증 모달을 닫는다. `onRefreshError`에서 후속 조회 실패를 처리한다. |

두 사용처는 모두 내부 코드라고 가정한다. 그 외 공개 소비자·외부 호환 계약은 없다고 놓았다. 이는 이번 가상 작업의 관찰 입력이며 Project 가이드의 영구적인 명명 정책이 아니다. 두 화면은 각각의 정책에 따라 이동·닫기를 수행하며 wrapper는 화면 반영 완료를 관찰하지 않는다.

## 변경 전 코드 발췌

전체 앱을 재현하는 실행 파일이 아니라 완료 경계를 보여 주는 발췌다. `LoginInput`, `queryClient`, `loginService`와 화면별 오류 처리는 이미 존재한다고 가정한다. 두 callback은 정상 반환하고 다시 던지지 않는다고 놓았다.

```ts
type LoginCallbacks = {
  onCompleted: () => void;
  onRefreshError: (error: unknown) => void;
};

async function loginAndRefresh(
  input: LoginInput,
  callbacks: LoginCallbacks,
): Promise<void> {
  await loginService.signIn(input);

  void queryClient
    .invalidateQueries({ queryKey: ["session-data"] })
    .catch(callbacks.onRefreshError);

  callbacks.onCompleted();
}
```

이 발췌에서는 Query 실패가 해당 Promise의 rejection으로 전달된다고 가정한다. Promise에 `void`를 붙인 것 자체가 실패 처리인 것은 아니며 연결된 `catch`와 callback이 처리 책임을 갖는다. Query 라이브러리 설정·버전 전체의 동작을 확인한 코드는 아니다.

## 초기 사용처와 표현

```ts
// LoginScreen
loginAndRefresh(input, {
  onCompleted: () => {
    showStatus("로그인과 화면 갱신 완료");
    navigateAfterSignIn();
  },
  onRefreshError: showQueryRefreshError,
});

// ReauthDialog
loginAndRefresh(input, {
  onCompleted: () => closeDialog(),
  onRefreshError: showQueryRefreshError,
});
```

초기 인터페이스와 두 호출부에는 callback의 완료 범위를 설명하는 가까운 주석이 없다고 가정한다. LoginScreen에는 재조회·렌더까지 끝났다고 읽히는 표시 문구가 있다. `navigateAfterSignIn`은 기존 이동 정책을 실행하는 소비자 동작이고 `closeDialog`는 기존 닫기 동작이며, 여기서 새 화면 정책을 제안한 것이 아니다.

비교할 현재 약속은 [인증 계약](../../../../project/guidance/authentication-and-session/INDEX.md), Project 자체의 표현 요구는 [가독성 가이드](../../../../project/guidance/code-readability/INDEX.md)에서 읽는다. 이 초기 입력에는 개선 이름이나 개명 결론을 미리 적지 않는다. 이름을 유지하며 설명을 보완할지, 개명할지, 동작의 문제가 있는지는 Work에서 판단한다.

초기 가정과 현재 구현을 구별한다. 위 발췌는 변경 이유를 비교하는 입력이며, 지금의 함수·대기·실패 동작은 데모 소스와 테스트에서 확인한다. 초기판과의 실제 제품 회귀를 검증한 것은 아니다. 보존된 Noline 문서만으로 이 함수명·대기 동작을 도출한 것도 아니다.
