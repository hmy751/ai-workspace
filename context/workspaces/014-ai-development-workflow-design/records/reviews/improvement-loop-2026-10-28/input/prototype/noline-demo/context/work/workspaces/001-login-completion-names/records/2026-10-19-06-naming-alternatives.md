# 같은 인증 코드에서 이름 유지와 개명 비교

2026-10-19. **가능한 한 코드 자체에서 책임과 완료 범위를 이해할 수 있게 하는 것이 지향점이다.** A는 기존 이름의 모호함을 설명으로 보완하고, B는 그 의미를 이름에서도 드러낸다. 처리 순서·반환값·오류 전달·소비자 행동은 같다. 이 조건에서는 설명 의존을 줄이는 B를 권하며 현재 demo도 B를 사용한다. A는 호환성이나 변경 위험 때문에 기존 이름을 유지해야 할 때 비교할 절충안이다. 이 비교와 현재 평가는 최초 구현 당시의 수행 이력으로 소급하지 않는다.

비교의 공통 기반은 [현재 wrapper](../../../../../examples/authentication/src/authentication.mjs)와 [Login 소비자](../../../../../examples/authentication/src/consumers.mjs)다. 주입용 factory를 생략하고 같은 의존성이 바깥에 있다고 놓았다. A에는 [초기 입력](../source/scenario-input.md)의 함수명·callback 이름만 되돌렸다. 초기 입력에 없었던 조회 요청의 동기 오류 분리는 **현재 코드의 동작으로 두 안에 똑같이 유지**했다. 실제 Noline의 변경 전후 코드를 복원한 것은 아니다.

두 안 모두 인증 서비스를 기다리고, 조회를 요청하되 결과는 기다리지 않으며, 조회 오류를 `onRefreshError`로 따로 보낸다. 완료 callback과 오류 callback은 정상 반환한다는 현재 demo의 계약을 쓴다. 성공하면 같은 session을 반환한다. Login은 “로그인 완료”를 알리고 이동을 시작하며 최신 조회 값을 바로 읽지 않는다. Reauth도 같은 callback 이름 변경 외에는 기존 닫기 동작을 유지한다.

## A — 이름 유지와 설명 보완

```js
// 인증 적용 뒤 조회를 요청하되 조회 결과는 기다리지 않는다.
// 완료 callback과 반환은 인증 적용을 뜻하며 조회·화면 준비 완료가 아니다.
// 조회 요청·결과의 오류는 onRefreshError로 따로 전달한다.
async function loginAndRefresh(credentials, { onCompleted }) {
  const session = await authenticationService.signIn(credentials);

  try {
    Promise.resolve(requestSessionRefresh()).catch(onRefreshError);
  } catch (error) {
    onRefreshError(error);
  }

  onCompleted(session);
  return session;
}

function submitLogin(credentials) {
  return loginAndRefresh(credentials, {
    // 인증 적용 완료 알림이다. 조회 결과를 읽는 시점으로 쓰지 않는다.
    onCompleted() {
      showMessage("로그인 완료");
      navigateToTrips();
    },
  });
}
```

함수 정의의 설명과 callback 가까운 주석을 읽으면 현재 사용에 필요한 경계를 알 수 있다. 완료 뒤에는 이동만 시작하므로 동작 요구도 충족한다. 다만 주요 완료 의미를 설명이 대신하므로, 코드 자체의 명료함이라는 면에서는 개선 여지가 남는다.

`loginAndRefresh`·`onCompleted`만으로는 조회 요청과 인증 완료의 경계를 특정하기 어렵다. 기존 API를 바꿀 비용이나 호환 제약이 크면 이 이름을 유지할 수 있지만, 설명을 쉽게 찾을 수 있다는 사실만으로 지향할 품질에 도달했다고 판단하지 않는다. 현재 예제는 내부 두 소비자이고 공개 호환 요구는 없다.

## B — 개명과 설명 보완

```js
// 인증 적용 뒤 조회를 요청하되 조회 결과는 기다리지 않는다.
// 완료 callback과 반환은 인증 적용을 뜻하며 조회·화면 준비 완료가 아니다.
// 조회 요청·결과의 오류는 onRefreshError로 따로 전달한다.
async function signInAndRequestRefresh(credentials, { onSignedIn }) {
  const session = await authenticationService.signIn(credentials);

  try {
    Promise.resolve(requestSessionRefresh()).catch(onRefreshError);
  } catch (error) {
    onRefreshError(error);
  }

  onSignedIn(session);
  return session;
}

function submitLogin(credentials) {
  return signInAndRequestRefresh(credentials, {
    // 인증 적용 완료 알림이다. 조회 결과를 읽는 시점으로 쓰지 않는다.
    onSignedIn() {
      showMessage("로그인 완료");
      navigateToTrips();
    },
  });
}
```

함수명의 `RequestRefresh`는 조회 요청을, `onSignedIn`은 인증 완료를 직접 가리킨다. 주석을 잠시 보지 않더라도 새 호출부를 훑거나 callback을 찾을 때 두 경계를 구별할 단서가 생긴다. 이것이 이번 개명의 구체 이득이다.

이름이 길어지고 함수·callback을 사용하는 곳을 함께 고쳐야 한다. 이 이름만으로 모든 실패 정책까지 드러나지는 않는다. 나머지 코드의 타입·책임·흐름으로 표현할 의미와 별도 설명이 필요한 의도·제약도 구별해 본다. 여기서는 이름의 효과만 비교하려 A와 같은 주석을 두었으며, 그 주석 전부가 최종 코드에 반드시 필요하다는 뜻은 아니다. 실제 이해 속도를 측정한 결과도 아니다.

## 두 안의 차이와 현재 선택

| 같은 질문 | A — 이름 유지 + 설명 | B — 개명 + 설명 |
| --- | --- | --- |
| 함수·callback 이름만 훑으면 무엇을 알 수 있나 | 로그인과 refresh의 관련성은 보이나 완료 범위는 주석에서 확인한다. | refresh는 요청이며 callback은 인증 완료라는 단서를 이름에서도 얻는다. |
| 가까운 설명까지 읽으면 필요한 행동을 정할 수 있나 | 가능하다. 현재 이동 소비자는 조회 완료를 필요로 하지 않는다. | 가능하다. 동작 정보는 A와 동일하며 이름에서도 경계를 재확인한다. |
| 어떤 비용이 생기나 | API 이름 변경은 없다. 설명의 접근성과 새 호출부의 완료 의미를 유지해야 한다. | 함수·callback 참조와 관련 문서를 함께 바꾼다. 현재 가정은 내부 두 소비자여서 변경 범위가 제한된다. |
| 이름만으로 해결되지 않는 것은 무엇인가 | 조회 실패의 별도 전달, 인증 유지, 화면 준비와의 차이 | A와 같다. 긴 이름에 실패 정책까지 나열하지 않는다. |

**현재는 B를 유지한다.** 조회 요청과 인증 완료를 이름에서 읽을 수 있게 하여 A에 남은 설명 의존을 줄이는 방향이다. 내부 두 곳이라는 사실은 그 개선 비용을 낮추는 조건이며 품질의 이유 자체는 아니다. A를 올바르게 사용할 수 있다는 판단과 B를 더 나은 방향으로 권하는 판단은 함께 성립한다. 공개 API 호환성이나 실제 변경 위험이 크다면 A를 유지하는 절충을 다시 검토한다. B 역시 가능한 최선의 이름·구성으로 확정한 것은 아니다.

**안내 문구 수정은 이 두 선택과 별개다.** 초기의 “로그인과 화면 갱신 완료”는 확인하지 않은 결과를 약속하므로 두 안 모두 “로그인 완료”로 맞췄다. B만 문구를 고치거나 A만 잘못된 표현을 남겨 개명의 효과를 부풀리지 않았다. 조회 완료를 기다리는 변경도 넣지 않았다. 그 결과가 실제로 필요한 소비자가 생기면 이름 비교와 별도로 동작·완료 계약을 판단한다.

두 코드 블록은 식별자 두 쌍을 대응시키면 주석을 포함해 동일하다. 이는 같은 코드의 표현 대안이라는 정적 비교이며 두 제품 버전의 회귀 검증이 아니다. 실행 예제의 이름과 동작은 이번 비교에서 바꾸지 않았다. 일반 판단은 [이름·완료 기준](../../../../personal/development/naming-and-completion/INDEX.md), 현재 선택 요약은 [Spec](../current/memory/spec/05-constraints-design-assumptions.md)에서 이어 읽는다.
