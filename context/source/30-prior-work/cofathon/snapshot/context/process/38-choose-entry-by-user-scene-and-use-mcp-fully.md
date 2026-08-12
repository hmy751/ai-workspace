# 사용자 장면으로 진입을 고르고 MCP를 충분히 사용

날짜: 2026-07-17

## 사용자 교정과 즉시 보정

사용자는 MyRealTrip MCP를 사용할 수 있는데도 “MCP 자체가 가치가 아니다”라는 방어적 설명으로 그 역할을 일부러 낮추지 말라고 교정했다. 이어서 URL 입력도 실제 사용자 장면에 더 맞으면 좋은 진입이며, MCP를 높이기 위해 URL을 억지로 낮추라는 뜻은 아니라고 명확히 했다.

따라서 기준은 `MCP 우선 대 URL fallback`의 서열이 아니다.

> 사용자가 상품을 아직 고르지 않았는지, 이미 URL을 들고 왔는지에 따라 가장 자연스러운 진입을 고르고, MyRealTrip MCP는 현재 상품·상세·날짜별 option이 판단을 더 정확하게 만드는 구간에서 적극 사용한다.

URL은 사용자 입력 방식이고 MCP는 주로 live 데이터 회수 방식이므로 둘은 함께 작동할 수 있다.

## 두 실제 사용자 장면

### 상품을 아직 고르지 않은 사용자

- 목적지·날짜·일행·필수 조건·원하는 경험을 자연어로 말한다.
- MCP의 category·검색으로 후보를 찾고, 상세·날짜별 option으로 실제 결제 후보를 좁힌다.
- 이 장면에서 MCP 검색을 빼고 일반 추천이나 임의 URL 나열로 대체하지 않는다.

### 이미 상품을 고른 사용자

- 사용자가 MyRealTrip URL과 자기 날짜·일행·조건을 준다.
- URL이 가장 짧고 자연스러운 사용자 진입이다. product ID나 JSON으로 바꾸게 하지 않는다.
- plugin은 URL이 가리키는 상품을 MCP 상세·날짜별 option으로 다시 확인하고, MCP에 없거나 말줄임인 구역은 공개 페이지·사용자 본문으로 보완한다.
- 이미 상품이 특정됐으므로 category·검색을 의례적으로 다시 호출할 필요는 없다.

## MCP 사용 원칙

- MCP를 단순한 시연 장치나 가치 없는 plumbing처럼 표현하지 않는다. live 상품·option을 현재 사용자 조건과 연결하는 핵심 제품 capability다.
- 반대로 MCP tool 수나 호출 자체를 사용자 가치의 전부로 세지 않는다. 그 데이터가 후보·충돌·미확정과 다음 행동을 어떻게 바꿨는지 보여 준다.
- 사용자 장면에 필요한 도구만 호출한다. search-first에는 검색 계열, URL-first에는 상세·option 계열이 중심이다.
- MCP request·response·시각·누락을 보존하고, URL·본문에서 보완한 근거와 섞지 않는다.
- MCP가 실패해도 URL 기반 검토를 무가치한 경로로 낮추지 않는다. 다만 어떤 근거를 live로 확인하지 못했는지 사용자에게 밝힌다.

## Goal과 acceptance 영향

- Loop 03은 검색형 자연어 진입과 URL 진입을 둘 다 end-to-end로 검증한다.
- MCP 연동 완료를 주장하려면 적어도 한 성공한 live MCP 실행과 raw bundle이 필요하다.
- URL 진입의 acceptance는 URL을 받은 뒤 MCP 상세·option을 사용할 수 있으면 연결하고, 사용자에게 URL 본문이나 구조화 JSON을 다시 옮기게 하지 않는 것이다.
- 모든 요청에 모든 MCP tool을 호출하거나, URL-only 실행을 자동 실패로 만드는 것은 목표가 아니다.
- 실제 사용자 acceptance는 어느 진입이 그 사용자의 구매 단계에 맞았는지와 결과가 다음 행동을 바꿨는지를 함께 본다.

## 현재 영향 범위

- [선택한 솔루션](../solution/00-selected-solution.md)의 두 진입점을 동등한 사용자 장면으로 구체화한다.
- [최상위 구현 Goal](../engineering/00-top-level-goal.md)과 [Loop 03 Goal](../engineering/03-live-purchase-entry/goal.md)은 MCP 연동 증거와 사용자 장면별 진입을 함께 요구한다.
- source code는 아직 구현 전이므로 이번 결정만으로 MCP·URL workflow가 작동한다고 쓰지 않는다.
