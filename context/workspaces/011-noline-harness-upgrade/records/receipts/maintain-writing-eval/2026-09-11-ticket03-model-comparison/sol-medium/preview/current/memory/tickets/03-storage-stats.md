# 03 — 저장 용량 통계

## 맡은 결과와 범위

`useStorageStats`의 성공 경로와 바깥 `catch`에서 반복되는 `StorageStats` 조립을 한곳으로 모아, 부분 실패 때 남는 값과 조회 중단·계속 규칙을 더 쉽게 읽을 수 있게 한다.

이번 Ticket은 표시 기능을 바꾸는 작업이 아니다. 프로필 화면이 사용하는 `dbSize`와 `mapPackSize`, 현재 hook 계약에 포함된 `totalSize`, 1,024 기준 단위 변환과 소수 최대 한 자리 표기를 유지한다. `totalSize`의 새 화면 표시나 필드 제거는 범위에 포함하지 않는다.

## 실행 맥락과 접근

Main이 현재 구현을 확인해 보고한 동작은 다음과 같다.

- DB 파일 조회가 중간에 실패하면 그때까지 합산한 DB 용량을 보존하고 Mapbox 조회를 시작하지 않는다.
- `getPacks()`가 실패하면 DB 결과를 보존하고 지도 용량은 0으로 둔다.
- 개별 `pack.status()`가 실패하면 해당 팩만 건너뛰고 다음 팩을 계속 집계한다.
- `.db`, `.db-wal`, `.db-shm`만 DB 용량에 포함한다.
- 0은 `0 B`로, 1,024 bytes는 `1 KB`로, 1,536 bytes는 `1.5 KB`로 표시한다.

중복 제거 뒤에도 DB 실패와 지도 팩 실패의 차이, 부분 결과가 남는 위치, 조회가 중단되거나 계속되는 조건을 가까운 코드에서 파악할 수 있어야 한다. 표시값 조립처럼 경계가 분명한 책임은 추출할 수 있지만, 작은 중복을 없애기 위해 dependency adapter나 여러 파일의 추상 계층을 새로 만들지는 않는다.

자동 검사는 `apps/client`가 소유한다.

- `Jest`, `jest-expo`, `@testing-library/react-native`의 `renderHook`·`waitFor`·`act`, `@types/jest`를 사용한다.
- `expo-file-system`과 `@rnmapbox/maps`는 각 테스트에서 Jest module mock으로 제어한다. 두 번째 실제 소비자가 생기기 전에는 공용 `__mocks__`나 별도 adapter를 만들지 않는다.
- 설정은 `apps/client/jest.config.cjs`, 테스트 전용 타입 검사는 `apps/client/tsconfig.test.json`에 분리한다.
- 테스트는 `apps/client/tests/features/profile/hooks/useStorageStats.test.tsx`에 둔다. 루트 `tests/`나 Expo Router의 `app/`에는 두지 않는다.
- 테스트 의존성과 preset은 루트나 다른 package가 아니라 `apps/client/package.json`이 소유한다. 루트 `pnpm-lock.yaml` 변경은 설치 결과로 허용한다.
- `packages/schema`, `packages/ui`, `apps/server`에는 client의 Expo preset을 전파하지 않는다. 실제 중복이 생기기 전에는 `packages/test-config`도 만들지 않는다.

선택 근거와 대안 비교는 [저장 용량 통계 테스트 전략](../../../records/2026-09-11-02-storage-stats-test-strategy.md)에 있다.

## 완료 조건과 확인 방법

리팩터링 전후에 같은 hook 계약 검사를 실행해 다음을 확인한다.

1. 빈 DB 디렉터리와 빈 지도 팩에서 모든 크기가 `0 B`다.
2. `.db`, `.db-wal`, `.db-shm`만 합산하고 무관 파일은 조회하지 않는다.
3. DB·지도·합계와 1,024 단위 및 소수 표기가 기존 결과와 같다.
4. DB 파일 조회 중간 실패 시 앞선 합계가 남고 이후 DB 파일과 Mapbox는 조회하지 않는다.
5. `getPacks()` 실패 시 DB 결과가 남고 지도 용량은 0이다.
6. 개별 `pack.status()` 실패 뒤에도 다음 팩을 조회하며 성공한 팩만 합산한다.
7. `refresh()`는 이전 값에 누적하지 않고 처음부터 다시 계산한다.

결과값과 중요한 중단·계속 조건을 검사하되 helper 이름, `setStats` 호출 횟수, 중요하지 않은 전체 호출 순서까지 고정하지 않는다. 화면 코드를 바꾸지 않는 한 `ProfileScreen` 전체 렌더 테스트와 E2E 도입은 완료 조건으로 삼지 않는다. 가능하면 development build 한 플랫폼에서 SQLite 생성과 지도 다운로드 전후 값, 재진입 또는 `refresh()` 갱신을 smoke test하고 확인하지 않은 플랫폼과 실제 native 동작은 미확인으로 남긴다.

완료 판단에는 테스트 통과뿐 아니라 기존 동작 보존과 stats 조립 중복 감소, 실패 흐름의 가독성 개선을 함께 대조한다.

## 현재 상태와 실제 결과

논의 시점에는 미착수다. Main은 관련 제품 코드와 테스트에 변경이 없고 현재 구현이 위 동작 관찰과 일치한다고 보고했다. 이 문서 작성 입력에는 코드 원출력이나 테스트 실행 결과가 포함되지 않았으므로 구현 및 검증 완료로 간주하지 않는다.

최초 실행에서 Expo SDK 51에 맞는 실제 설치 버전, pnpm 환경의 `transformIgnorePatterns` 필요 여부, Mapbox mock의 정확한 형태를 확인해야 한다. smoke test를 수행한다면 대상 플랫폼도 실행 시 정한다.
