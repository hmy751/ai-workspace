# 저장 용량 통계 테스트 전략

## 기록 목적과 근거

Ticket 03의 리팩터링은 표시 기능을 바꾸지 않으면서 부분 실패 순서와 결과값을 보존해야 한다. 이 기록은 그 동작을 어떤 범위에서 검사할지, Expo 기반 client에 어떤 테스트 스택과 디렉터리 구성을 둘지 논의한 선택 과정과 재검토 조건을 보존한다. 현재 실행 기준은 [Ticket 03](../current/memory/tickets/03-storage-stats.md)에 압축해 두었다.

근거는 Codex session `01a08ff3-0e91-7921-afe4-69f0968638ef`의 사용자·Main 가시 발화 원문 중 raw line 9–254다. 사용자 발화와 commentary·final response가 포함됐으며 도구 호출·결과는 포함되지 않았다. 따라서 코드 구조, 현재 테스트 기반, Expo·Mapbox 구성에 관한 사실은 Main이 확인했다고 보고한 범위이고 이 기록이 독립적으로 재검증한 사실은 아니다.

사용자는 선택지 설명 뒤 “전반적으로 다 좋아”라고 답했고, package별 소유 방식을 설명받은 뒤 “그래 좋아”라고 답했다. 이어 기록 위치 제안을 “좋아”라고 받아들인 다음, Maintainer가 대화 근거를 연결해 Ticket 본문·논의 기록·색인을 작성하도록 명시적으로 요청했다. 이 수락은 아래 Ticket 03 실행 전략에 적용되며 모든 package의 영구 공통 정책이나 제품 완료 acceptance로 확대하지 않는다.

## 보호하려는 동작

Main이 현재 구현과 대조해 보고한 핵심은 다음과 같다.

- DB 파일 조회 중 실패하면 그때까지의 DB 용량을 보존하고 Mapbox 조회는 시작하지 않는다.
- `getPacks()` 실패 시 DB 결과는 남고 지도 용량은 0이 된다.
- 개별 `pack.status()` 실패는 해당 팩만 건너뛰며 뒤의 팩은 계속 집계한다.
- 바이트 표시는 1,024 단위를 사용하고 소수는 최대 한 자리이며 0은 `0 B`다.
- 프로필 화면은 `dbSize`와 `mapPackSize`를 표시한다. `totalSize`는 계산되지만 현재 화면에서는 소비되지 않는다.

리팩터링의 목표는 성공 경로와 바깥 `catch`의 stats 조립 중복을 제거하는 것이다. 함수 분리 자체가 목표는 아니다. DB 실패 시 어디에서 조회가 중단되고 어떤 부분 결과가 남는지 이해하려고 여러 파일의 `catch`와 반환 타입을 따라가야 한다면, 중복이 줄어도 가독성 개선으로 보기 어렵다는 판단을 채택했다. 조회 흐름은 가까이 유지하고 표시값 조립처럼 독립적인 책임만 자연스럽게 추출한다.

## 검토한 테스트 선택지

### Jest로 현재 hook 직접 검사 — 채택

`Jest + jest-expo + React Native Testing Library`로 실제 hook을 실행하고 FileSystem과 Mapbox 반환을 module mock으로 제어한다. mount 시 조회, `refresh()`, 비동기 실패 순서, 부분 결과 보존과 최종 문자열을 함께 확인할 수 있어 이번 리팩터링의 외부 계약과 가장 가깝다.

비용은 Expo·React Native package 변환과 네이티브 모듈 mock 설정이다. pnpm 구조에서 별도 `transformIgnorePatterns`가 필요할 수 있고 Mapbox export 형태를 직접 맞춰야 할 수 있다. 이 설정은 추측으로 미리 늘리지 않고 최초 실행 오류를 근거로 추가한다.

### 순수 함수 검사 — 보조적으로 허용

`formatBytes`나 stats 조립 함수가 구현 책임상 자연스럽게 분리되면 입력과 결과를 빠르고 명확하게 검사할 수 있다. 그러나 순수 함수만으로는 `useEffect`가 조회를 시작하는지, 결과가 hook 상태에 반영되는지, `refresh()`가 재계산하는지, 실패 뒤 조회를 중단하거나 계속하는지를 충분히 보호하지 못한다. 따라서 실제 hook 테스트를 대체하지 않는다.

테스트 편의를 위해 dependency adapter나 provider 계층을 추가하면 mock은 쉬워지지만 제품 코드의 파일과 타입을 늘리고 조회 흐름을 흩을 수 있다. 이번 작은 hook에는 module mock으로 충분하다고 판단했으며, 여러 저장공간 기능이 같은 계산 책임을 공유하게 될 때 다시 검토한다.

### Vitest와 Node 내장 test runner — 이번에는 제외

두 선택지는 순수 TypeScript 계산에는 가볍고 빠르다. 하지만 이번 대상은 Expo·React Native hook과 네이티브 모듈을 함께 제어해야 한다. Vitest는 Metro/Babel과 별도의 Vite 변환·mock 체계를 요구할 수 있고, `node:test`는 TypeScript·JSX·React Native 렌더링과 module mock 구성을 별도로 해결해야 한다. client hook 하나를 위해 두 번째 실행 체계를 도입하는 비용이 이점보다 크다고 판단했다.

향후 `packages/schema` 같은 순수 TypeScript package가 자체 테스트 실행기를 고를 때에는 Expo client와 별도로 Vitest, Node runner 또는 Node 환경의 Jest를 비교할 수 있다.

### ProfileScreen 테스트 — 화면 변경 시에만

현재 화면은 hook의 `dbSize`와 `mapPackSize`를 단순히 연결한다고 Main이 보고했다. 화면 전체를 렌더하면 인증 store, Expo Router, 공용 UI와 기타 모듈 mock이 필요해 이번 관심사보다 테스트 부담이 커진다. 이번 Ticket에서 화면 코드를 바꾸지 않으면 사용처와 diff를 확인하고 전체 컴포넌트 테스트는 만들지 않는다. 표시 구조를 실제로 변경할 때 다시 판단한다.

### E2E와 실기기 확인 — 자동 hook 테스트의 보완

Maestro나 Detox는 빌드된 앱의 화면과 통합을 확인할 수 있지만 특정 DB 파일 또는 지도 팩 하나에만 실패를 주입하기 어렵고, 현재 기반이 없다면 설치·빌드·CI 비용이 크다. 이번 실패 분기의 주 검증으로 사용하지 않는다.

Development build의 수동 smoke test는 실제 SQLite 파일 경로와 Mapbox native pack 연동을 확인할 수 있지만 반복 가능한 회귀 검사는 아니다. 가능하면 한 플랫폼에서 데이터 생성과 지도 다운로드 전후 표시, 앱 재진입 또는 `refresh()` 갱신만 확인하고 자동 hook 테스트를 보완한다.

## 자동화 범위

대표 시나리오는 다음 일곱 가지다.

1. 빈 DB 디렉터리와 지도 팩 없음
2. 대상 DB 파일과 무관 파일의 선별
3. 1,024·1,536 bytes 등 단위 경계와 DB·지도·합계 계산
4. DB 파일 조회 중간 실패 뒤 부분 결과 보존과 Mapbox 조회 중단
5. `getPacks()` 실패 뒤 DB 결과 보존
6. 개별 `pack.status()` 실패 뒤 다음 팩 계속 처리
7. mock 값을 바꾼 뒤 `refresh()` 재계산

테스트는 반환 문자열과 의미 있는 중단·계속 조건을 확인한다. helper 이름, `setStats` 호출 횟수, 관심사와 무관한 세부 호출 순서를 고정해 이후 리팩터링을 방해하지 않는다. 자동 테스트가 입증하는 범위는 우리 hook이 의존성 반환을 해석하는 방식이며, iOS·Android 실제 파일 경로, FileSystem 네이티브 구현, Mapbox가 보고하는 실제 팩 크기는 포함하지 않는다.

## 설정과 디렉터리 선택

이번 테스트 기반은 `apps/client`가 소유한다.

```text
apps/client/
├── jest.config.cjs
├── package.json
├── tsconfig.json
├── tsconfig.test.json
├── src/features/profile/hooks/useStorageStats.ts
└── tests/features/profile/hooks/useStorageStats.test.ts
```

별도 `jest.config.cjs`를 선택한 이유는 Expo preset 외에도 테스트 경로, client의 `@/` alias, 필요 시 transform 규칙이 추가될 수 있어 `package.json`의 역할을 흐리지 않기 위해서다. 초기 설정은 `jest-expo` preset, `tests/` 대상, `@/` mapping, mock 초기화 정도로 시작하고 실제 오류가 없는 설정은 추가하지 않는다.

`apps/client/tests/`는 제품 `src`의 소유 구조를 반영한다. 현재 제품 TypeScript 범위와 테스트 전용 타입을 분리하고 Expo Router의 route 디렉터리인 `app/`에 테스트가 들어가는 것을 피하기 위한 선택이다. 테스트가 장기 회귀 자산으로 남을 예정이므로 `tsconfig.test.json`으로 Jest mock과 fixture도 별도 타입 검사하는 방향을 채택했다.

네이티브 모듈 mock은 처음에는 테스트 파일 안에 둔다. 반복이 커지면 같은 파일의 builder, 같은 feature의 helper, 여러 feature가 실제로 공유할 때 공용 helper나 `__mocks__` 순으로 이동한다. 처음부터 `jest.setup.ts`, 전역 mock, 별도 fixture, snapshot, coverage threshold는 만들지 않는다.

## Monorepo 소유 경계

Expo 전용 테스트 의존성과 script는 `apps/client/package.json`에 선언하고, 설치 결과인 루트 `pnpm-lock.yaml` 변경은 정상적인 파생 결과로 본다. 루트에 Jest를 설치하거나 Expo preset을 공통 기반으로 두지 않는다.

`apps/server`, `packages/schema`, `packages/ui`는 실행 환경과 소비 계약이 다르므로 각 workspace가 필요할 때 자기 runner, preset, `tsconfig`, 테스트 디렉터리를 소유한다. 루트 `tests/`는 여러 workspace를 실제 배포 형태로 연결하는 통합 테스트가 생길 때만 고려한다.

두 번째 workspace에서 실제로 같은 React Native Jest 설정이 반복되기 전에는 `packages/test-config`를 만들지 않는다. 공유하게 되더라도 Expo preset과 일반 transform처럼 실제 공통 부분만 대상으로 하고 client의 `@/` alias, Mapbox mock, Expo Router 설정과 feature별 setup은 공유하지 않는다.

루트의 전체 테스트 집계 명령도 이번 Ticket에서 추가하지 않는다. 각 workspace에 실제 테스트 계약이 생긴 뒤 script 이름과 `--if-present` 사용 여부를 정한다. client 테스트가 workspace package를 소비하게 되더라도 `@repo/*`를 무조건 source로 mapping해 package export와 build 계약을 우회하지 않는다.

## 실행하며 확정할 사항

다음 항목은 방향만 정했으며 제공된 근거에서 설치하거나 실행해 확인하지 않았다.

- Expo SDK 51과 현재 client 의존성에 맞는 Jest·`jest-expo`·React Native Testing Library의 정확한 버전
- pnpm 환경에서 `transformIgnorePatterns` 조정이 실제로 필요한지
- 현재 `@rnmapbox/maps` export에 맞는 최소 mock 형태
- 테스트 파일에 JSX가 필요한지에 따른 `.ts` 또는 `.tsx` 확장자
- development build smoke test를 수행할지와 수행한다면 어느 플랫폼인지
- 테스트 전 현재 코드의 기준 결과, 리팩터링 후 결과, lint·format·typecheck 결과

Main은 Expo 공식 단위 테스트·native module mock·Router 테스트 안내를 근거로 제시했지만, 제공된 대화에는 해당 페이지의 원문이나 도구 결과가 없다. 정확한 설치와 설정은 실행 시 현재 공식 문서와 실제 오류를 확인해 확정한다.
