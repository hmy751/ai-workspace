# 통화와 금액의 제품 의미

경비의 통화 분리, 합계·대표 표시, 금액 정밀도와 반올림을 판단할 때 읽는다. 이 본문은 이 주제의 현재 Project 기준을 소유한다. 기존 [Currency context](../../../.claude/context/currency.md)는 이전 경로를 새 Owner로 연결하고 구현 위치를 찾는 호환 진입점으로 남는다.

## 서로 다른 통화는 서로 다른 금액이다

**경비는 통화별로 관리하고 합산한다.** 환율과 환산 시점이 정해지지 않은 금액을 통화 구분 없이 더하지 않는다. 표시에는 currency code 또는 symbol을 함께 둔다.

| 값 | 맡는 의미 |
| --- | --- |
| Trip의 `baseCurrency` | 새 경비의 기본 통화를 제안하고, 해당 통화의 합계가 있으면 우선 배치한다. |
| Expense의 `currency`·`amount` | 그 경비 자체의 통화와 금액. 사용자는 여행 기본값과 다른 통화도 선택할 수 있다. |

오프라인 수동 입력에서도 이 관계를 유지한다. 환산 합계를 도입하려면 환율 출처·기준 시각·오프라인 동작·실패 시 표시를 먼저 결정한다.

## 현재 합계와 대표 표시를 해석하는 법

경비 화면은 같은 통화의 amount를 숫자로 바꿔 더한 뒤 아래 순서로 표시한다.

| 조건 | 현재 표시 |
| --- | --- |
| 합계에 `baseCurrency`가 있음 | 해당 그룹을 먼저 두고 나머지는 금액 숫자의 내림차순으로 둔다. |
| 합계에 `baseCurrency`가 없음 | 금액 숫자가 큰 그룹부터 둔다. 환산한 가치의 비교는 아니다. |
| 화면의 첫 그룹 | 강조하고 `주 통화` 라벨을 붙인다. |

따라서 **첫 그룹과 여행의 기본 통화는 항상 같지 않다.** 강조·라벨을 바꿀 때는 첫 그룹, baseCurrency, 가장 큰 숫자 합계 중 무엇을 표현할지 구별한다. 기본 통화가 없는 경우 `주 통화`가 무엇을 뜻해야 하는지는 아직 제품 선택으로 남아 있다.

대표 금액 하나만 보여야 하는 위치에서는 통화별 결과 중 하나와 나머지 통화 개수를 함께 표시한다. 다만 현재 `getPrimaryCurrency`는 baseCurrency를 받지 않고 가장 큰 숫자 합계를 고르며, 실제 consumer는 확인되지 않았다. 새 카드가 helper 이름만으로 대표 기준을 채택하지 않는다.

구현은 [경비 합계 화면](../../../apps/client/src/screens/ExpensesScreen.tsx)과 [통화 helper](../../../apps/client/src/shared/lib/currency.ts)에서 확인한다.

## 표시 자릿수는 금액 정밀도 계약이 아니다

현재 표시 관례는 **KRW·JPY 0자리, 그 밖의 통화 2자리**다. 저장 가능한 정밀도·합산 방식·반올림 시점·회계 처리까지 결정한 규칙은 아니다.

| 경계 | 현재 구현 | 판단할 차이 |
| --- | --- | --- |
| [공유 entity](../../../packages/schema/src/entities/expense.ts)·[client SQLite](../../../apps/client/src/shared/db/schema.ts) | amount를 문자열로 처리 | 소수 자릿수 제한을 선언하지 않는다. |
| [server PostgreSQL](../../../apps/server/src/db/schema.ts) | `decimal(10,2)` | client의 문자열 계약과 저장 정밀도가 다르다. |
| Client 합계 | `Number`로 변환해 더함 | 표시 자릿수 규칙만으로 합산 정밀도를 보장하지 않는다. |
| 합계 화면 / 공용 formatter | `toFixed` / `toLocaleString` | 같은 값도 반올림 결과가 다를 수 있다. |

Ticket 01의 Node 기반 비교에서는 `1.005 USD`가 화면 표시식에서 `1.00`, 공용 formatter에서 `USD 1.01`이었다. 이는 **리팩터링 전후 같은 동작이었다는 근거**이며 올바른 금액 처리의 기대값이나 실제 기기 검증이 아니다.

입력 정밀도·저장 경계·합산·표시 반올림은 함께 정해야 한다. 당시 작업은 이 정책을 결정하지 않았으며 두 자리 표시를 Project-wide 금액 계약으로 확대하지 않는다.

## 변경할 때 확인할 관계

- **합계·카드·폼:** 같은 통화를 불필요하게 나누거나 다른 통화를 환율 없이 합치지 않는지 확인한다. 기본 통화와 대표 표시의 의미도 구별한다.
- **자릿수·반올림:** formatter만 바꾸지 않고 입력 schema·client/server 저장·합산·표시 consumer를 함께 대조한다.

작성 근거는 Workspace 002의 [Ticket 01](../../work/workspaces/002-code-readability-refactoring/current/memory/tickets/01-expense-totals.md)과 2026-09-14의 코드·schema 대조다. 2026-10-01 편집에서는 그 Ticket의 보존 범위와 열린 선택을 다시 읽고 이 브랜치의 helper·schema·화면 사용처를 대조했다. 제품 테스트나 실제 React Native 렌더를 새로 실행하지 않았다.
