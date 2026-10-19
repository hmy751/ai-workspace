# 개인 기준과 Project 계약을 함께 읽고 선택하는 장면

**아래는 가상 적용 장면이다.** 문서는 실제로 작성했지만 개발 의뢰·제품 변경·검사는 설명용 가정이다. 실제 Noline의 함수명, Promise 해소 시점, 사용처나 검사 결과를 확인했다는 뜻이 아니다. [전체 시안](README.md)

개인 기준과 Project 계약은 독립된 본문이다. [실행 연결](workflow.md)에 따라 Main이 요청의 성격으로 개인 주제를 고르고, 대상 Project의 계약과 이번 Work의 요구를 따로 가져온다. 이 장면에서는 같은 완료 계약을 유지하면서 이름을 바꿀지, 설명을 보완할지, 동작을 바꿔야 하는지를 비교한다.

## 사람의 요청과 초기 입력

사람 → Main:

> `loginAndRefresh`와 완료 callback을 보면 화면 데이터까지 다 바뀐 것처럼 읽혀. 실제로 보장하는 책임과 완료 범위에 맞게 이름과 완료 표현을 정리해 줘. 지금의 실행 순서, 실패 처리, 화면별 이동 정책은 유지해 줘.

작업 시작 시 코드·사용처와 가정은 [시작 입력](scenario-input.md)에 고정했다. 현재 [Project 현황](noline-demo/context/project/current/authentication-flow.md)은 가상 작업 후 상태다. 최종 이름을 처음부터 구현자에게 알려 준 입력으로 취급하지 않는다.

초기 wrapper의 핵심은 다음과 같다. `loginService.signIn`은 전체 세션 조율, 계정·DB·queue 확인, 기기 저장, signed-in 적용까지 마친 뒤 해소된다고 가정한다.

```ts
// 변경 전: 설명용 발췌다.
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

그 뒤 wrapper가 조회 갱신을 요청하고 재조회 완료를 기다리지 않은 채 callback을 호출한다. Query 실패는 Promise rejection으로 전달되고 `onRefreshError`가 처리하며, 두 callback은 정상 반환하고 다시 던지지 않는다고 가정한다. `void` 자체가 오류를 처리하는 것은 아니다. 실제 라이브러리 설정이나 생략한 동기 실패 경로를 검증한 발췌도 아니다.

초기 사용처는 내부의 LoginScreen·ReauthDialog 두 곳뿐이라고 가정한다. LoginScreen은 `onCompleted`에서 `로그인과 화면 갱신 완료`를 표시하고 기존 이동을 요청하며, ReauthDialog는 모달을 닫는다. 변경 전 전체 발췌는 시작 입력에 있다. 두 곳이라는 조건과 과도한 표시 문구는 이번 판단 재료이며 Project 가이드가 정해 준 개명 정책이 아니다.

## Main이 독립된 입력을 가져온다

Main은 [Work 입구](noline-demo/context/work/workspaces/login-completion-names/README.md)와 [Ticket](noline-demo/context/work/workspaces/login-completion-names/current/ticket.md)에 이번 목표·보존 범위를 둔다. 개인 기준은 [Personal 입구](personal-context/README.md)에서 개발 작업임을 보고 [짧은 공통](personal-context/development/README.md)과 [이름·완료 범위 상세](personal-context/development/naming-and-completion.md)를 고른다.

별도로 [Project 입구](noline-demo/context/project/README.md)에서 [인증·세션 계약](noline-demo/context/project/guidance/authentication-and-session.md)과 [코드 가독성 가이드](noline-demo/context/project/guidance/code-readability.md)를 읽고 초기 코드·소비자와 대조한다. Project 문서에는 개인 기준의 경로나 이번 답으로 쓸 후보 이름이 들어 있지 않다. 개인 기준 없이도 로그인 완료와 실패·화면 책임을 이해할 수 있다.

| 입력 | 이번에 제공하는 판단 |
| --- | --- |
| 개인 개발 공통·이름 상세 | 목적·조건·비용으로 유지와 수정을 판단한다. 같은 의미를 이름·타입·가까운 설명 중 무엇으로 전달할지, 개명이 실제 오독을 줄이는지 비교한다. |
| Project 인증·표현 계약 | 로그인 완료가 무엇인지, 조회 요청·재조회·렌더가 무엇과 다른지, 후속 실패와 화면 책임에서 지킬 약속을 정한다. 특정 개명 답을 정하지 않는다. |
| 이번 Work와 시작 입력 | 현재 요청은 표현 정리이며 동작 보존이 필요하다. 내부 두 소비자, 설명이 없는 초기 인터페이스, 과도한 완료 문구가 이번 선택의 근거다. |

계정·로컬 데이터의 제품 의미를 바꾸지 않으므로 [기기 세션](noline-demo/context/project/common/device-session.md) 전체를 이 장면에서 다시 읽지는 않는다. 필요한 판단이 생기면 추가한다. 개인 상세를 이미 충분히 알고 있다면 재독할 필요도 없다. 이 표는 한 작업의 선택이며 모든 자료를 매번 읽는 순서가 아니다.

Main → 구현자:

> 이 Work의 이름·완료 표현 정리를 맡아 줘. 원요구와 보존 범위는 [Ticket](noline-demo/context/work/workspaces/login-completion-names/current/ticket.md), 시작 코드와 두 소비자는 [시작 입력](scenario-input.md)이야. 실제 작업이었다면 이 가정 대신 코드·호출부를 확인해야 해.
>
> 별도 입력으로 [개인 개발 공통](personal-context/development/README.md)과 [이름·완료 기준](personal-context/development/naming-and-completion.md)을 가져왔어. 표현 수단과 변경 비용을 판단할 때 사용해 줘. [Project 입구](noline-demo/context/project/README.md)에서 [인증 계약](noline-demo/context/project/guidance/authentication-and-session.md)·[표현 가이드](noline-demo/context/project/guidance/code-readability.md)를 읽어 어떤 완료·실패 의미를 유지할지 확인해 줘.
>
> 이름을 유지하며 설명을 보완할지, 개명할지, 실제 동작 문제가 있는지를 비교해 줘. 특정 이름을 답으로 정해 두지는 않았어. 선택을 가른 근거·변경·확인과 미확인은 Work 구현 기록에 남겨 줘. 새 대기·실패·화면 계약이 필요하면 Main에게 돌려줘.

## 구현자가 같은 계약에서 가능한 선택을 비교한다

구현자는 개인 상세의 질문을 현재 코드에 대입한다. 호출자는 callback을 받으면 무엇을 믿을 수 있는가? 이름·타입·가까운 설명으로 이미 충분한가? 표현을 바꾸어 줄일 오독이 변경·호환 비용에 맞는가?

Project 계약과 초기 코드가 모두 인증 적용 뒤 조회를 요청하는 흐름을 가리키므로, 이 장면에서 확인된 문제는 그 범위를 넘겨 읽히는 표현이다. 이름에 맞추기 위해 조회 완료까지 기다리는 동작을 추가할 이유는 아직 없다.

| 대안 | 이번 입력에서의 이득·비용과 판단 |
| --- | --- |
| 이름 유지＋가까운 계약 설명 보완 | callback 직전에 인증 적용은 끝났고 조회는 진행 중이라고 설명하면 동작 의미를 전달할 수 있다. 호환 변경이 없다는 이점이 있다. 다만 초기 인터페이스에는 이 설명이 없고 소비자의 표시도 이미 화면 갱신 완료로 이어져 있어, 이번에는 설명만 추가하는 것보다 이름에서도 차이를 드러낼 이득이 있다고 판단한다. |
| 함수·callback 개명＋짧은 계약 설명 | 인증과 갱신 요청의 차이를 호출부에서 더 빨리 읽을 수 있다. 내부 두 소비자만 바꾸고 외부 호환 계약은 없다는 이번 가정에서는 비용이 제한적이므로 이 안을 선택한다. 모든 하위 작업을 이름에 나열하지 않고 세부 완료·실패는 설명으로 보완한다. |
| 재조회 완료까지 기다리는 동작 변경 | 기존 이름의 넓은 의미에 맞출 수 있지만 callback·화면 이동·로딩의 시점과 후속 실패 처리가 달라진다. 이번 보존 요구와 맞지 않으므로 선택하지 않는다. 실제 요구가 화면 준비 대기로 바뀌면 Project 계약을 다시 판단해야 한다. |

개인 기준은 두 표현 대안의 전달력·비용을 비교하는 데 기여하고, Project 계약은 어떤 의미까지 표현할 수 있는지를 제한한다. 어느 한쪽도 다른 쪽의 결론을 자동으로 대신하지 않는다. 초기 표현을 그대로 두는 것만으로는 이번 오독 문제를 해결했다고 보기 어렵지만, **이름 유지와 설명 보완**은 가능한 대안으로 비교했다.

[개인 상세의 조건별 대비](personal-context/development/naming-and-completion.md)처럼 공개 API이고 이미 널리 쓰이는 이름이라면 호환 비용이 달라진다. 기존 이름과 명확한 계약 설명을 유지하거나 단계적으로 바꾸는 선택이 타당할 수 있다. 반대로 약속한 완료를 구현이 못 지키는 경우에는 개명만으로 해결하지 않는다. 이는 이번 입력에서 발견한 외부 소비자나 실제 결함이 아니라, 같은 기준에서 판단이 달라지는 조건이다.

## 구현자가 선택한 이름과 남긴 문제

이 비교 뒤 wrapper는 `signInAndRequestRefresh`, callback은 `onSignedIn`으로 정한다. 이름만으로 모든 보장을 전달하지 않으므로 가까운 설명도 붙인다. 아래는 구현자 변경판이며 LoginScreen의 오래된 문구는 놓쳤다고 가정한다.

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

구현자 → Main:

> 내부 두 사용처에서 바꿀 비용이 제한적이고, 초기 이름·callback에 완료 범위 설명이 없어 개명과 짧은 설명을 함께 선택했어. 이름 유지와 설명 보완도 비교했지만 이번에는 호출부에서 갱신 요청이라는 차이를 드러낼 이득이 더 크다고 봤어.
>
> 서비스 대기, Query 요청 뒤 callback 호출, 후속 오류 담당과 화면별 이동·닫기는 유지했어. 변경과 확인 계획은 `records/implementation.md`에 남겼어. 화면 표시 문구까지의 전체 대조는 검토에 남아 있어.

이 인계와 변경은 가상이다. [구현 기록](noline-demo/context/work/workspaces/login-completion-names/records/implementation.md)은 선택·미확인을 남기며 실제 검사 통과를 주장하지 않는다. 구현자가 놓친 표현을 검토 전에 이미 고친 결과로 덮어쓰지 않는다.

## 검토자가 원자료와 변경을 받아 직접 판단한다

Main → 검토자:

> [원요구·Ticket](noline-demo/context/work/workspaces/login-completion-names/current/ticket.md), [시작 입력](scenario-input.md), [개인 개발 공통](personal-context/development/README.md)·[이름 상세](personal-context/development/naming-and-completion.md), Project의 [인증 계약](noline-demo/context/project/guidance/authentication-and-session.md)·[표현 가이드](noline-demo/context/project/guidance/code-readability.md), [구현 인계](noline-demo/context/work/workspaces/login-completion-names/records/implementation.md)를 함께 봐줘. 구현자의 결론이나 특정 이름을 정답으로 두지 말고, 현재 변경과 두 소비자가 실제 책임·완료 범위를 정확하게 전달하는지 대조해 줘.
>
> 기존 목표와 보존 계약 안의 품질 문제는 직접 고치고 관련 확인을 해줘. 새 대기·실패·화면 정책이나 외부 호환성 판단이 필요하면 Main에게 돌려줘. `records/review.md`에 직접 판단·수정·확인과 한계를 남겨 줘. 실제 확인하지 못한 동작은 계획·예상과 구별해 줘.

검토자는 같은 독립 입력을 받으며, 특정 문구를 찾아 고치라는 결론을 요청문에서 받지 않는다. 이 예시에는 검토자 수정 이후 별도의 최종 독립 검증을 실제로 수행한 단계가 없다.

가상 검토자는 callback의 표시 문구를 대조해 재조회·렌더까지 완료됐다고 알리는 문제를 찾는다. Project의 완료 계약과 개인 기준의 ‘완료 알림도 보장 범위에 맞춘다’는 판단을 함께 적용해 문구를 직접 수정한다. 사용자가 알아야 할 성공은 로그인 완료이므로 내부 조회 단계를 화면에 나열하지 않는다.

```diff
 onSignedIn: () => {
-  showStatus("로그인과 화면 갱신 완료");
+  showStatus("로그인 완료");
   navigateAfterSignIn();
 },
```

검토자 → Main:

> LoginScreen에 화면 갱신까지 끝났다고 알리는 문구가 남아 있어 `로그인 완료`로 직접 고쳤어. 구현자가 고른 이름과 짧은 설명은 이번 내부 사용처·보장 범위에 맞는 선택으로 봤어. 대기·실패·이동 동작은 바꾸지 않았어.
>
> 느린 Query, Query 실패, 인증 서비스 실패를 나눠 확인할 계획과 예상 판정을 검토 기록에 남겼어. 실제 제품 검사와 UI 실행은 하지 않았으므로 제품 완료로 승인할 수는 없어.

[검토 기록](noline-demo/context/work/workspaces/login-completion-names/records/review.md)은 직접 수정·예상 판정·실행 한계를 남긴다. 한 가상 장면에서 기준을 사용한 서술이 있다는 사실로 실제 AI의 기준 발견·판단 효과가 증명되지는 않는다.

## Main이 결과를 각 책임에 돌려준다

| 위치 | 이 장면 뒤 남는 것 |
| --- | --- |
| Personal 기준 | 일반 판단과 조건별 대비를 유지한다. 이번 이름을 모든 Project의 필수 어휘로 올리지 않는다. |
| Project common·guidance | 제품 의미·인증·표현 계약을 유지한다. 개인 기준을 연결하거나 이번 선택 이유를 제품 정책으로 추가하지 않는다. |
| Project current | 가상 작업 후 함수·callback·두 소비자의 연결을 맞춘다. 초기 상태는 시작 입력에 보존한다. |
| Work | 원래 목표, 비교한 대안과 이번 선택 이유, 구현자가 놓친 문구와 검토 수정, 확인 계획·미확인·현재 상태를 남긴다. |
| 실행 연결 | 이번 사례의 결과만으로 새 역할·skill을 만들지 않는다. 전달·인수에 드러난 문제가 있다면 그 근거로 별도 보완을 판단한다. |

Main → 사용자, 이 시안의 반환 예시:

> 이름 유지와 설명 보완도 비교했지만, 이번에는 내부 두 사용처의 변경 비용과 오독을 줄이는 이득을 보고 `signInAndRequestRefresh`, `onSignedIn`과 짧은 계약 설명을 선택했어. 검토에서는 남은 사용자 문구를 `로그인 완료`로 고쳤어.
>
> 제품의 인증·조회·화면 계약과 개인 기준은 유지하고, Project 현황의 연결과 Work의 선택·검토 기록을 맞췄어. 이것은 문서와 코드 발췌로 구성한 가상 적용 시안이며 실제 Noline 변경·검사 통과를 뜻하지 않아.
