# 저장 용량 통계 테스트 전략

## 논의한 문제

Ticket 03은 `useStorageStats`의 stats 조립 중복을 줄이면서 부분 실패의 의미를 보존하는 리팩터링이다. 기존 client에는 제품 테스트 파일과 실행 스크립트가 없다고 Main이 보고했기 때문에, 리팩터링 전후 동작을 무엇으로 보호할지와 새 테스트 기반을 monorepo 어디에 둘지가 함께 논의됐다.

테스트의 경계는 네이티브 저장소 구현 자체의 정확성까지 증명하는 것이 아니라, hook이 FileSystem과 Mapbox의 결과를 어떤 순서로 집계하고 실패 시 무엇을 보존하며 어떤 문자열을 반환하는지 검증하는 것으로 잡았다.

## 검토한 선택지

### Jest로 현재 hook 직접 검사

`Jest + jest-expo + React Native Testing Library`로 실제 hook을 실행하고 FileSystem과 Mapbox를 module mock으로 대체하는 방안이다. mount 시 자동 조회, `refresh()`, 부분 실패, 중단·계속 조건과 최종 표시값을 한 계약 안에서 확인할 수 있다.

Expo·React Native 변환과 native module mock 설정이 필요하고 Vitest보다 초기 실행이 무거울 수 있지만, 현재 제품이 사용하는 Expo/Babel/Metro 환경에 가장 가깝고 테스트 때문에 제품 구조를 크게 바꿀 필요가 없다.

### 집계 책임을 순수 함수로 분리

`formatBytes`나 stats 조립처럼 자연스럽게 경계가 생기는 계산은 순수 함수로 분리해 빠르고 명확하게 검사할 수 있다. 그러나 순수 함수만 검사하면 `useEffect`, 상태 반영, `refresh()`와 native module import 연결을 놓친다.

DB 집계, 지도 집계, 실패 처리와 표시 조립을 각각 다른 파일이나 adapter로 나누면 중복은 줄어도 실패 결과를 이해하기 위해 여러 파일을 따라가야 할 수 있다. 따라서 자연스러운 작은 helper는 허용하되 hook의 실패 흐름은 가까운 코드와 hook 테스트에서 보존하기로 했다.

### Vitest 또는 Node 내장 test runner

순수 TypeScript 계산에는 가볍고 빠르지만, 이번 대상은 Expo·React Native hook과 native module을 함께 제어해야 한다. React Native 변환, Expo module mock, JSX renderer와 Metro/Babel 차이를 별도로 해결해야 하므로 client hook 하나를 위해 두 번째 테스트 체계를 도입하지 않기로 했다.

### ProfileScreen 테스트, E2E와 실기기 확인

`ProfileScreen` 전체 렌더 테스트는 두 표시값을 확인하려고 인증 store, Router, 공용 UI 등 많은 주변 mock을 요구한다. 화면 코드를 바꾸지 않는 이번 Ticket에는 넣지 않는다.

Maestro나 Detox 같은 E2E는 실제 앱 통합을 확인할 수 있지만 특정 DB 파일이나 지도 팩 실패를 정밀하게 주입하기 어렵고 새 기반의 비용이 크다. development build의 수동 smoke test는 실제 SQLite와 Mapbox 연결을 확인하는 보완 수단으로만 두며 자동 회귀 검사를 대신하지 않는다.

## 채택한 기본안

- `apps/client`에 `Jest`, `jest-expo`, `@testing-library/react-native`, `@types/jest`를 둔다.
- `apps/client/jest.config.cjs`가 Expo preset, 테스트 탐색과 client의 `@/` alias를 소유한다.
- 테스트 전용 타입 범위는 `apps/client/tsconfig.test.json`으로 제품 TypeScript 범위와 분리한다.
- hook 테스트는 `apps/client/tests/features/profile/hooks/useStorageStats.test.tsx`에 둔다.
- FileSystem과 Mapbox mock은 우선 해당 테스트 파일 가까이에 둔다. 반복이 생기면 같은 파일의 builder, feature helper, 여러 feature가 공유할 때의 공용 mock 순으로 확장한다.
- 설정 오류가 실제로 나타나기 전에는 큰 `transformIgnorePatterns`, `jest.setup.ts`, 공용 `__mocks__`, fixture 폴더, snapshot, coverage threshold와 E2E 구성을 추가하지 않는다.
- `packages/schema`, `packages/ui`, `apps/server`는 각 실행 환경에 맞는 테스트 설정을 각자 소유한다. client의 Expo 설정을 루트 공통 preset으로 만들거나 아직 반복되지 않은 `packages/test-config`를 선행 도입하지 않는다.
- 루트 `package.json`은 지금 테스트 도구를 소유하지 않는다. 여러 workspace에 실제 테스트 계약이 생긴 뒤 `test:run` 같은 공통 script 이름과 `pnpm -r --if-present` 기반 실행 조율만 검토한다.
- client 테스트에서 `@repo/*`를 무조건 각 package의 source로 mapping하지 않고 실제 package export 계약을 따른다.

## 자동 검사 범위

대표 검사는 빈 상태, 대상·무관 DB 파일 혼합, 단위 경계, DB 조회 중간 실패, `getPacks()` 실패, 개별 `pack.status()` 실패, `refresh()` 재계산이다. 결과 문자열과 중요한 중단·계속 조건을 확인하되 helper 이름, 내부 state 갱신 횟수와 중요하지 않은 전체 호출 순서는 고정하지 않는다.

자동 검사는 iOS·Android의 실제 파일 경로, Expo FileSystem의 native 구현, Mapbox가 실제 보고하는 pack 크기나 다운로드된 팩과 화면의 일치를 증명하지 않는다. 필요하면 development build 한 플랫폼의 smoke test로 보완하고 나머지는 미확인으로 기록한다.

## 실행하며 확정할 사항

이 논의에서는 설정이나 테스트를 실제로 설치·실행하지 않았다. 다음 항목은 최초 실행 결과를 보고 확정한다.

- Expo SDK 51과 현재 의존성에 맞는 정확한 설치 버전
- pnpm 구조에서 `transformIgnorePatterns` 보완이 필요한지
- `@rnmapbox/maps`가 요구하는 정확한 mock 형태
- development build smoke test 수행 여부와 대상 플랫폼
- 두 번째 실제 테스트 소비자가 생겼을 때 mock 또는 Jest 설정의 공유 범위

## 근거와 한계

이 기록은 2026-09-11 사용자·Main 대화에서 사용자가 기술 스택과 설정·디렉터리·monorepo 경계를 재질문하고, Main이 제시한 전반적 방향과 기록 위치에 동의한 내용을 정리한다. 코드와 package 구성에 관한 사실은 Main이 당시 파일을 확인해 보고한 범위이며, 이 기록 작성 입력에는 도구 원출력, 설치 결과 또는 테스트 실행 증거가 포함되지 않았다.
