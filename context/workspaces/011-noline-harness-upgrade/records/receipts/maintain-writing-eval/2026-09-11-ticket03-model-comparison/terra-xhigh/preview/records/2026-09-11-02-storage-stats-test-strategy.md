# 저장 용량 통계 테스트 전략

## 결정의 범위

Ticket 03은 저장 용량 조회 로직의 동작을 바꾸는 작업이 아니라, 부분 결과와 기존 표시를 보존하며 `StorageStats` 조립 중복을 줄이는 리팩터링이다. 따라서 테스트도 네이티브 저장소 자체의 정확성이나 화면 전체 흐름까지 넓히지 않고, hook이 의존성의 결과와 실패를 어떤 순서로 해석해 표시값으로 내보내는지에 맞춘다.

사용자는 제안된 기록 배치와 테스트 전략에 동의했다. 이 기록은 그 논의에서 채택한 실행 기준과 선택 이유를 보존하며, 실제 설치·구현·실행 결과를 주장하지 않는다.

## 채택한 테스트 방식

`apps/client` 안에서 Jest, `jest-expo`, React Native Testing Library를 사용해 `useStorageStats`를 직접 실행한다. FileSystem과 Mapbox는 각 테스트가 필요한 성공·실패 결과를 명시하는 module mock으로 제어한다.

이 방식은 mount 시 조회, `refresh()` 재조회, DB와 지도 팩의 부분 실패, 최종 표시 문자열처럼 hook의 외부 계약을 함께 확인한다. 반면 iOS·Android 실제 파일 경로, Expo FileSystem의 네이티브 구현, 실제 Mapbox 팩 크기는 이 테스트로 입증하지 않는다.

주요 회귀 확인은 다음과 같다.

- 빈 상태와 파일 선별
- 1,024 단위와 소수 표시 경계
- DB 조회 중간 실패 뒤 부분 DB 결과 보존 및 Mapbox 조회 중단
- `getPacks()` 실패 뒤 DB 결과 보존
- 개별 팩 상태 실패 뒤 다음 팩 계속 조회
- `refresh()`가 이전 값을 누적하지 않고 다시 계산함

실기기 확인은 자동 테스트의 대체물이 아니라 보완이다. 가능하면 development build 한 플랫폼에서 DB와 오프라인 지도 변화, 재진입 또는 새로고침 뒤 표시를 확인한다.

## 검토한 대안과 선택 이유

순수 함수 분리는 `formatBytes`나 stats 조립처럼 자연스러운 단일 책임에 한해 허용한다. 그러나 실패 결과를 이해하려고 DB 수집, 지도 수집, 오류 처리, 표시 조립 파일을 연달아 따라가야 하는 구조는 피한다. 이 Ticket의 핵심인 “어느 실패에서 중단하고 어떤 부분 결과를 남기는가”는 hook 가까이에서 읽혀야 한다.

Vitest나 Node 내장 test runner는 순수 TypeScript 계산에는 가볍고 빠를 수 있지만, 이번 대상인 Expo React Native hook과 네이티브 모듈 mock을 위해 별도 변환·renderer·mock 체계를 추가해야 한다. client에 이미 필요한 Expo 실행 환경과 다른 테스트 체계를 도입할 이점이 작아 채택하지 않았다.

`ProfileScreen` 전체 렌더 테스트는 화면 구조를 바꾸지 않는 이번 작업에 비해 인증 store, router, 공용 UI 등의 mock 부담이 크다. DB와 지도 표시 연결은 현재 hook 반환 계약과 변경 검토로 다루며, 화면 구조를 실제로 바꿀 때만 별도 컴포넌트 테스트를 재검토한다.

Maestro·Detox 같은 E2E는 실제 앱 흐름이나 화면 표시를 확인할 수 있지만, 특정 DB 파일 또는 특정 지도 팩에서만 발생하는 실패를 정밀하게 주입하기 어렵고 기반 구축 비용도 크다. 이 Ticket의 주 검증 수단으로는 채택하지 않는다.

## 설정과 디렉터리 소유

테스트 runner와 preset은 실행 환경이 다른 monorepo 전체의 공통 기반이 아니라 `apps/client`의 의존성이다. client는 Expo React Native, server는 Node, schema는 순수 TypeScript, UI는 별도 React Native 컴포넌트 책임을 가질 수 있으므로 하나의 root Jest 설정이나 Expo preset을 전체에 퍼뜨리지 않는다.

초기 구조는 다음과 같이 둔다.

```text
apps/client/
├── package.json
├── jest.config.cjs
├── tsconfig.test.json
└── tests/
    └── features/profile/hooks/
        └── useStorageStats.test.ts
```

테스트 source를 `tests/`로 분리해 현재 제품 TypeScript 범위와 Jest 타입을 섞지 않는다. `tests/` 아래에서는 source의 feature 소유 구조를 반영해 평면적인 테스트 더미가 되지 않게 한다. Expo Router route 디렉터리에는 테스트를 두지 않는다.

테스트별 실패 조건이 서로 다르므로 초기에는 테스트 파일 내부 mock을 사용한다. 동일 모듈을 여러 feature가 실제로 소비할 때에만 feature helper, `tests/helpers`, 공용 `__mocks__` 순서로 승격을 검토한다. client와 UI 양쪽에서 실제 반복이 확인되기 전에는 공용 test-config package도 만들지 않는다.

root는 나중에 테스트가 준비된 workspace의 실행을 조율할 수 있지만, 이번 Ticket에서는 root 집계 명령을 추가하지 않는다. 다른 package의 placeholder test script나 실행 환경을 이번 작업이 바꾸지 않기 때문이다.

## 최초 실행에서 확인할 사항

다음은 전략으로 채택되었지만 아직 실제 환경에서 확인되지 않았다.

- Expo SDK 51과 호환되는 실제 의존성 버전 및 설치 방식
- `@rnmapbox/maps`와 Expo FileSystem의 실제 import 형태에 맞는 mock 형상
- pnpm 환경에서 `transformIgnorePatterns` 조정이 필요한지 여부
- 테스트용 TypeScript 설정과 기존 client typecheck의 실제 상호작용
- development build smoke test를 수행할 플랫폼과 다른 플랫폼의 미확인 범위

이 항목들은 최초 설정·실행 결과로 구체화한다. 오류가 발생하기 전부터 넓은 transform 규칙, 전역 setup, 공용 mock을 추가하지 않는다.

## 근거와 확인 한계

이 기록의 테스트 대상·현재 코드 상태·monorepo 구성에 관한 관찰은 2026-09-11 Ticket 03 논의에서 Main이 보고한 내용이다. 제공된 대화 원문에는 도구 원출력, package manifest 본문, 코드 diff, 설치 결과, 테스트 로그가 포함되지 않았으므로 이 기록은 이를 독립적으로 확인하거나 제품 검증이 완료되었다고 주장하지 않는다.
