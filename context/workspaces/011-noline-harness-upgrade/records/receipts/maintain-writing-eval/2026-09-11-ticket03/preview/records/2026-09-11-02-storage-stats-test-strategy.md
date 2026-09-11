# 저장 용량 테스트 전략

Ticket 03은 저장 용량 조회의 부분 결과와 기존 표시를 보존하면서 `StorageStats` 조립 중복을 줄이는 리팩터링이다. 이 기록은 자동 검증을 어느 범위까지 도입할지와 설정의 소유 위치를 정리한다.

## 선택한 검증 범위

주 검증 대상은 Expo FileSystem과 Mapbox가 반환한 값을 hook이 어떻게 집계하고 표시값으로 바꾸는지다. 빈 DB, 대상·비대상 파일 혼합, 1,024 단위와 소수 표시, DB 파일 조회 중간 실패, `getPacks()` 실패, 개별 팩 상태 조회 실패, `refresh()` 재계산을 다룬다.

DB 조회 실패는 그때까지의 DB 합계를 남기고 지도 조회를 시작하지 않아야 한다. 지도 팩 하나의 상태 조회가 실패하면 앞선 성공 결과는 남기고 다음 팩 처리를 계속해야 한다. 이 중단·계속 조건과 결과값은 검사하되, helper 이름이나 `setStats` 호출 횟수처럼 리팩터링 자체를 막는 내부 구현은 고정하지 않는다.

자동 테스트는 실제 iOS·Android 파일 경로, Expo FileSystem의 네이티브 구현, Mapbox가 보고하는 실제 팩 크기를 증명하지 않는다. 필요하면 development build에서 SQLite 생성 전후, 오프라인 지도 다운로드 전후, 재진입 또는 `refresh()` 뒤의 값 변화를 한 플랫폼에서 smoke test할 수 있다. 이는 자동 회귀 검사를 보완할 뿐 대체하지 않는다.

## 기술 선택과 경계

사용자와 Main은 Jest, `jest-expo`, React Native Testing Library로 실제 `useStorageStats` hook을 실행하고 Jest module mock으로 `expo-file-system`과 `@rnmapbox/maps`를 제어하는 방향을 채택했다. 이 조합은 mount 시 조회, 상태 갱신, `refresh()`와 실패 분기를 함께 확인할 수 있다.

순수 함수 분리는 표시값 조립처럼 책임이 분명할 때만 보조적으로 사용한다. 실패 결과를 이해하려고 여러 adapter와 helper의 `catch`를 따라가야 한다면 중복이 줄어도 가독성 개선이 아닐 수 있다. 테스트 편의를 위한 dependency injection 계층은 이번 작은 hook에 추가하지 않는다.

Vitest와 Node 내장 test runner는 React Native·Expo hook 및 native module mock 환경을 별도로 구성해야 하므로 이번 Ticket에는 선택하지 않는다. ProfileScreen 전체 렌더 테스트는 화면을 바꾸지 않는 이번 리팩터링에 비해 인증, Router, 공용 UI mock 부담이 크다. Maestro·Detox E2E는 실제 앱 흐름 확인에는 유용하지만 세밀한 부분 실패를 주입하기 어려우며, 현재 이 Ticket의 주 검증 수단이 아니다.

## 설정과 monorepo 소유

테스트 도구와 설정은 `apps/client`에만 둔다. `jest-expo`는 Expo 앱의 실행 환경에 속하므로 root나 `packages/schema` 같은 Node·순수 TypeScript package의 공통 의존성으로 올리지 않는다. lockfile의 root 변경은 package별 의존성 선언과 별개로 설치 결과를 기록하는 정상적인 변화다.

초기 구성은 `apps/client/jest.config.cjs`, `apps/client/tsconfig.test.json`, 그리고 `apps/client/tests/features/profile/hooks/useStorageStats.test.ts`를 둔다. Jest 설정은 `jest-expo` preset, client `@/` alias, 테스트 파일 범위와 mock 초기화를 맡는다. `transformIgnorePatterns`, setup 파일, 전역 `__mocks__`, fixtures, coverage threshold, 공용 test-config package는 실제 필요가 확인될 때만 추가한다.

다른 package의 테스트는 각 package가 자신의 runtime과 manifest 안에서 소유한다. 여러 workspace를 묶는 root 실행 명령은 두 번째 이상의 실제 테스트 소비자가 생기고 각 package의 테스트 계약을 정리한 뒤 판단한다.

## 근거와 남은 확인

이 기록의 코드 상태 설명은 2026-09-11 대화에서 Main이 보고한 관찰에 근거하며, 별도 코드 원출력이나 테스트 실행 결과는 제공되지 않았다. 사용자는 이 대화에서 위 전략과 문서 배치를 수용한 뒤 기록을 요청했다.

최초 구현 시에는 Expo SDK 51에 맞는 실제 의존성 버전, pnpm 환경에서 추가 변환 규칙이 필요한지, Mapbox mock의 정확한 형태, 실기기 smoke test를 할 플랫폼을 확인해야 한다.
