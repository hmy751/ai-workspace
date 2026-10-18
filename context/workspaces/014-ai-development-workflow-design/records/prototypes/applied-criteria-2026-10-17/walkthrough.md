# 실제 적용을 가정한 한 작업의 입력과 결과

**아래 전체가 가상 적용 장면이다.** 파일은 실제로 작성했지만 개발 의뢰·코드 변경·검사 결과는 가정이다. 도중의 ‘완료’와 ‘통과’는 이 장면 안의 상태다. 실제 제품에서 실행했다고 주장하지 않는다. [프로젝트 전체 파일](README.md)

이 문서는 2026-10-17에 작성한 HTTP 인수·직접 수정 장면이다. 연결된 일반 기준과 읽기 안내는 2026-10-18에 보완됐다. 당시 메시지에 기준을 직접 지정한 조건은 그대로 남겼다. 작업자가 기준을 찾는 과정과 선택이 갈리는 조건은 [Field 추가 장면](field-walkthrough.md), 원칙·사례 분리와 후속 재구체화는 [현재 시안 입구](README.md)에서 읽는다.

## 1. 작업을 시작하기 전에 이미 존재하는 것

shop-web의 [AGENTS.md](shop-web/AGENTS.md)는 Project 안내와 지정된 작업을 읽게 한다. [Project README](shop-web/context/project/README.md)는 프로젝트의 공통 자료를 찾는 입구다. [quality.md](shop-web/context/project/quality.md)에는 일반 원칙과 질문·사례가, [http-client.md](shop-web/context/project/http-client.md)에는 이 프로젝트의 HTTP 계약이 있다. [develop skill](shop-web/.agents/skills/develop/SKILL.md)은 구현과 검토 때 하는 일을 정의한다.

작업 시작 때 HTTP 문서에 있던 계약은 다음과 같았다고 가정한다. 현재 연결된 파일은 작업 완료 후 최종본이므로, 당시 입력은 이 발췌로 구별한다.

> get/post/put/delete 호출과 정상 JSON·문자열 반환을 제공한다. 요청은 호출 시작부터 결과 또는 오류를 반환할 때까지 10초 제한을 갖는다. 오류는 APIError(status, code, message)로 전달하며, 토스트·화면 이동은 사용처가 정한다.

시작 문서에는 헤더 직후 timer 해제라는 결함이나 `finally` 수정 방법이 적혀 있지 않았다. 검토 뒤에는 ‘본문 처리가 끝날 때까지 제한 유지, 완료·실패 모두 정리’를 현재 계약에 명확히 적었다. 구체 코드 수정 방법은 검토 기록이 소유한다. 현재 파일의 완료 후 설명을 과거 검토자의 입력으로 간주하지 않는다.

기준의 내용과 적용 절차가 같은 파일에 복제되어 있지는 않다. 예를 들어 일반 기준에서 ‘공개한 결과·오류·수명이 실제 경로에서도 유지되는가’를 묻고, HTTP 문서에서는 ‘10초 timeout과 APIError 형태’라는 이 프로젝트의 약속을 읽으며, 이번 Ticket은 무엇을 정비할지 정한다.

## 2. Main이 구현자에게 보내는 메시지

이 메시지는 채팅 입력이다. 매 작업마다 같은 역할 설명이나 기준 본문을 전부 복사하는 파일을 새로 만들지 않는다.

> shop-web의 HTTP-07 구현을 맡아 줘.
>
> `AGENTS.md`에서 진입하고 `context/workspaces/http-error-contract/ticket.md`와 `.agents/skills/develop/SKILL.md`의 구현 역할을 따라줘. 이번 목표는 공통 fetcher가 본문 읽기·파싱 실패까지 일관된 오류 계약으로 전달하게 하는 거야.
>
> 기존 get/post/put/delete 호출, 정상 JSON·문자열 반환, 기본 URL·헤더·10초 timeout, 화면 정책을 사용처에 두는 계약을 유지해 줘. Project의 HTTP 계약과 quality의 공통 계약 기준을 읽고, 현재 코드와 호출부에 대입해 판단해 줘.
>
> 필요한 구현과 확인을 끝내면 이 Work의 `records/implementation.md`에 변경 이유·확인·미확인을 남겨 줘. 검토자가 같은 변경을 인수하므로 넘긴 뒤에는 동시에 수정하지 말고, 제품 계약을 바꿔야 하면 근거와 영향을 알려 줘.

이 시점 Ticket은 구현할 목표와 계약이 정해진 상태다. 현재 저장한 [ticket.md](shop-web/context/workspaces/http-error-contract/ticket.md)는 작업을 마친 뒤의 상태이며 원래 요구·범위를 그대로 남겼다. 상태가 ‘완료’였던 Ticket을 구현자에게 처음 보냈다는 뜻은 아니다.

## 3. 구현자가 실제로 찾아 읽고 적용한 것

가정한 열람 순서는 AGENTS → Project README와 작업 Ticket → develop의 구현 역할 → HTTP 계약과 quality의 관련 기준이다. 파일 순서를 외우게 하려는 것이 아니라 AGENTS와 각 문서의 링크로 이 내용을 찾을 수 있도록 구성했다.

| 읽은 내용 | 구현에서 사용한 판단 |
| --- | --- |
| 일반 원칙: 사용처가 공통 계약의 형태·의미를 믿을 수 있어야 한다 | 본문 읽기·파싱 실패도 공개 APIError로 전달되게 한다. |
| 질문: 내부 실패 때문에 이미 얻은 정보가 사라지는가 | HTTP 500의 본문이 깨져도 HTTP 상태 500은 보존한다. |
| 현재 프로젝트의 계약과 Ticket의 제외 범위 | 오류 처리와 관련 있다고 자동 재시도·공통 토스트·인증 이동까지 넣지 않는다. |
| 구현 역할의 반환 요구 | 바꾼 코드뿐 아니라 확인하지 않은 느린 본문·timer 정리 경로를 검토자가 알 수 있게 남긴다. |

구현자가 남긴 실제 형식의 문서는 [implementation.md](shop-web/context/workspaces/http-error-contract/records/implementation.md)다. 이 장면에서 구현자는 본문 rejection 전달과 HTTP 상태 보존 등을 고쳤고, 정상 JSON·문자열·200 깨진 JSON·500 깨진 JSON·비객체 오류 본문을 확인했다고 가정한다. 느린 본문과 timer 정리는 미확인으로 남았다.

구현자 → Main 메시지:

> HTTP-07의 오류 전달과 상태 보존을 구현했어. 호출·정상 반환·화면 정책 경계는 유지했어. 검사한 경로와 변경 이유는 `records/implementation.md`에 남겼어. 본문이 늦게 도착하는 경우와 timer 정리 회귀는 아직 확인하지 못했으니 검토 인수에 포함해 줘.

## 4. Main이 검토자에게 보내는 메시지

> HTTP-07의 품질 검토와 필요한 직접 수정을 맡아 줘.
>
> 같은 `ticket.md`와 Project의 HTTP 계약·quality 기준을 읽고, develop skill의 검토 역할을 적용해 줘. 구현자의 전달 기록은 `records/implementation.md`야. 현재 변경 코드와 호출부, 실행 근거를 직접 대조해 줘. 구현자의 결론을 그대로 완료 근거로 쓰지는 말아줘.
>
> 목표와 보존 계약 안의 품질 문제는 직접 고치고 관련 경로를 다시 확인해 줘. 이번 계약을 바꾸거나 새 제품 동작이 필요하면 Main에 돌려줘. 수정·확인·남은 한계는 `records/review.md`에 남기고 결과를 알려 줘.

검토자에게 ‘타이머를 반드시 이렇게 고쳐라’라는 결론을 주지는 않았다. 검토자는 같은 기준, 원요구, 실제 변경과 구현자가 남긴 검증 공백을 받는다.

## 5. 검토자가 기준을 적용해 발견하고 직접 수정한 것

가정한 관찰: 헤더는 바로 오지만 본문이 계속 지연되는 응답을 확인하니 10초가 지나도 본문 읽기가 중단되지 않았다. 헤더 직후 timer를 해제하고 있었기 때문이다. 일반 기준의 ‘제공한 수명과 실제 경로가 일치하는가’라는 질문을 Project의 10초 계약에 대입해 찾은 문제다.

판단에 관련된 부분만 펼친 코드다. 전체 fetcher 소스나 실행 가능한 코드 전체가 아니다.

구현자 변경판에 남아 있던 부분:

```ts
const timer = setTimeout(() => controller.abort(), timeoutMs);

try {
  const response = await fetch(url, options);
  clearTimeout(timer);
  return await readResponse(response);
} catch (error) {
  throw normalizeError(error);
}
```

검토자가 직접 수정한 부분:

```ts
const timer = setTimeout(() => controller.abort(), timeoutMs);

try {
  const response = await fetch(url, options);
  return await readResponse(response);
} catch (error) {
  throw normalizeError(error);
} finally {
  clearTimeout(timer);
}
```

이 발췌에서 `options`에는 기존 controller의 signal이 연결되어 있고, `normalizeError`는 timeout과 다른 실패를 구별한다고 가정한다. 변경 의미는 timer 정리를 본문 처리 종료까지 늦추고 성공·실패 모두에서 수행하는 것이다. 본문 파싱 처리에서 timeout을 파싱 실패로 덮지 않는지도 함께 확인했다.

검토자 → Main 메시지:

> 헤더를 받은 직후 timeout을 해제해 느린 본문을 중단하지 못하는 문제를 확인했어. 본문 처리를 기다리는 동안 timer를 유지하고, 성공·실패 후에는 finally에서 정리하도록 직접 수정했어.
>
> 기존 오류 전달·HTTP 상태 보존 경로, 일반 본문 읽기·파싱 실패와 네트워크 실패의 구별, 느린 본문의 TIMEOUT, 완료·실패 후 정리를 다시 확인했어. 호출 방식과 화면 정책 책임은 그대로야. 구체 결과는 `records/review.md`에 남겼어. 실제 운영 서버 장애와 브라우저 UI 흐름은 이번 확인 범위에 포함하지 않았어.

검토자가 남기는 파일은 [review.md](shop-web/context/workspaces/http-error-contract/records/review.md)다. 구현자가 보고한 결과와 검토자가 직접 다시 확인한 결과를 나눠 썼다.

## 6. 작업이 끝난 뒤 프로젝트에 남아 있는 상태

| 위치 | 남는 내용과 이유 |
| --- | --- |
| [quality.md](shop-web/context/project/quality.md) | ‘공통 계약의 의미·수명을 실제 경로에서 확인한다’는 일반 기준을 그대로 유지한다. 이번 버그 하나 때문에 새 의무 질문을 덧붙이지 않았다. |
| [http-client.md](shop-web/context/project/http-client.md) | timeout이 응답 본문 읽기까지 포함하고 성공·실패 후 정리된다는 현재 프로젝트 계약을 명확히 했다. 이후 다른 작업도 이 문서를 읽는다. |
| [implementation.md](shop-web/context/workspaces/http-error-contract/records/implementation.md) | 초기 구현 선택과 당시 확인·미확인. 검토 결과로 과거 상태를 덮어쓰지 않는다. |
| [review.md](shop-web/context/workspaces/http-error-contract/records/review.md) | 발견한 문제·직접 수정·재확인과 범위 한계. |
| [ticket.md](shop-web/context/workspaces/http-error-contract/ticket.md)와 [작업 README](shop-web/context/workspaces/http-error-contract/README.md) | HTTP-07의 범위 안에서 완료되었다는 Main의 판단과 근거 위치. |

Main → 사용자 최종 메시지:

> fetcher 오류 계약 정비를 마쳤어. 본문 읽기·파싱 실패도 APIError로 전달하고, HTTP 오류의 본문이 깨져도 원래 상태를 보존하게 했어.
>
> 검토 과정에서는 헤더 뒤에 timeout이 풀리던 문제를 고쳤어. 이제 본문 읽기까지 timeout이 적용되고 성공·실패 후 timer가 정리돼. 정상 반환과 기존 오류 경로, 느린 본문과 정리 경로를 확인했어.
>
> 호출 방식과 화면별 토스트·이동 책임은 유지했어. Project의 HTTP 계약도 실제 동작에 맞춰 갱신했어. 운영 서버 장애와 브라우저 UI 흐름은 이번 확인 범위 밖이야.

이것이 형식이 적용된 한 결과다. 일반 기준은 판단 방향을 제공했고, Project 계약은 이 프로젝트에서 보존할 의미를 제공했으며, Ticket은 이번 범위를 정했다. skill은 읽기·수정·반환을 연결하고, Work 기록은 실제로 무엇을 했다고 주장하는지와 근거를 남기는 역할을 한다. **이 사례의 코드 변경·검사·완료는 모두 가정이다.**
