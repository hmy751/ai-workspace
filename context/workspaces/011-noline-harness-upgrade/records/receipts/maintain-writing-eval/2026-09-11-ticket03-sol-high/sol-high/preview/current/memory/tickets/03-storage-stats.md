# 03 — 저장 용량 통계

## 맡은 결과와 범위

`useStorageStats`에서 성공 경로와 바깥 `catch`에 반복되는 `StorageStats` 조립을 한곳으로 모은다. 중복을 줄이되 DB와 지도 팩 조회의 실패 경계, 부분 결과 보존, 현재 표시값을 그대로 유지해야 한다.

이번 Ticket은 저장 용량 표시 기능을 바꾸는 작업이 아니다. `ProfileScreen`이 사용하는 `dbSize`와 `mapPackSize`를 유지하고, 현재 화면에서 소비하지 않는 `totalSize`도 hook 반환 계약에서 유지한다. 새 표시 추가, 필드 제거, Expo FileSystem이나 Mapbox 네이티브 구현 자체의 정확성 검증은 범위에 포함하지 않는다.

## 실행 맥락과 접근

Main이 현재 구현을 확인해 보고한 범위에서는 Ticket이 지적한 중복과 실패 순서가 코드와 일치하며, 제품 코드와 관련 테스트는 아직 변경되지 않았다. 구현은 조회 흐름과 실패 경계를 같은 함수에서 따라갈 수 있게 유지하면서, 최종 표시값 조립처럼 분명한 책임만 추출한다. 작은 중복을 없애기 위해 dependency adapter나 여러 파일의 추상 계층을 새로 만들지는 않는다.

리팩터링 전후 동작을 비교할 수 있도록 다음 테스트 기반을 `apps/client`가 소유한다.

- 실행기는 Jest, Expo preset은 `jest-expo`, hook 실행은 React Native Testing Library의 `renderHook`을 사용한다.
- `expo-file-system`과 `@rnmapbox/maps`는 테스트 파일 안의 `jest.mock()`으로 제어한다. 반복이 실제로 생기기 전에는 전역 `__mocks__`, 공용 fixture, 별도 dependency injection 계층을 만들지 않는다.
- 테스트는 `apps/client/tests/features/profile/hooks/useStorageStats.test.ts` 또는 JSX가 필요하면 `.tsx`에 둔다.
- Jest 설정은 `apps/client/jest.config.cjs`, 테스트 전용 타입 검사는 `apps/client/tsconfig.test.json`이 맡는다.
- 테스트 의존성과 스크립트는 `apps/client/package.json`에 선언한다. 루트와 다른 workspace가 Expo 전용 설정이나 의존성에 암묵적으로 기대지 않게 한다.
- 루트 공용 Jest 설정, `packages/test-config`, 전체 workspace 테스트 집계 명령은 이번 Ticket에서 만들지 않는다. 두 번째 실제 소비자가 생기면 공유 범위를 다시 판단한다.

기술 선택과 제외 이유의 상세는 [저장 용량 통계 테스트 전략](../../../records/2026-09-11-02-storage-stats-test-strategy.md)에 남긴다. Expo SDK 51에 맞는 정확한 설치 버전, pnpm 환경에서 `transformIgnorePatterns`가 필요한지, Mapbox mock의 실제 export 형태는 최초 설치와 실행 결과로 확정한다.

## 완료 조건과 확인 방법

자동화 테스트는 hook이 의존성 결과를 해석하고 상태에 반영하는 다음 동작을 확인한다.

1. 빈 DB 디렉터리와 지도 팩 없음은 DB·지도·합계 모두 `0 B`를 반환한다.
2. `.db`, `.db-wal`, `.db-shm`만 합산하고 무관한 파일에는 크기 조회를 시작하지 않는다.
3. 1,024 bytes는 `1 KB`, 1,536 bytes는 `1.5 KB`로 표시하며 불필요한 `.0`을 붙이지 않는다.
4. DB 파일 조회 중 실패하면 실패 전까지의 DB 합계를 보존하고 이후 DB 파일과 Mapbox 조회를 시작하지 않는다.
5. `getPacks()`가 실패하면 DB 결과를 보존하고 지도는 `0 B`, 합계는 DB 용량과 같게 둔다.
6. 개별 `pack.status()`가 실패하면 그 팩만 건너뛰고 뒤의 팩을 계속 조회하며 성공한 팩만 합산한다.
7. `refresh()`는 이전 결과에 누적하지 않고 처음부터 다시 계산한다.

결과 문자열과 중요한 중단·계속 조건을 검증하되 helper 이름, `setStats` 호출 횟수, 관심사와 무관한 전체 호출 순서는 고정하지 않는다. 가능하면 현재 코드에서 기준 테스트를 먼저 실행한 뒤 리팩터링 후 같은 테스트를 다시 실행한다.

구조 개선은 중복된 stats 조립이 제거됐는지와 함께, DB 실패와 개별 지도 팩 실패의 서로 다른 처리 흐름을 한곳에서 계속 이해할 수 있는지도 비교한다. 이번 변경에서 `ProfileScreen`을 수정하지 않는다면 인증·라우터·공용 UI mock이 필요한 전체 화면 테스트는 추가하지 않는다.

실제 파일 경로와 Mapbox 네이티브 연동은 자동 hook 테스트의 입증 범위 밖이다. 여유가 있으면 development build 한 플랫폼에서 SQLite 생성과 지도 다운로드 전후 값, 재진입 또는 `refresh()` 갱신을 smoke test하고, 확인하지 않은 플랫폼과 실제 기기 범위를 결과에 명시한다.

## 현재 상태와 실제 결과

논의와 테스트 전략 선택까지 마쳤으며 구현과 테스트 작성은 미착수다. 제공된 근거에는 제품 코드 수정, 의존성 설치, 테스트 실행, Verify receipt 또는 실기기 확인 결과가 없다. Main의 코드 관찰 보고 외에 원본 도구 출력도 제공되지 않았으므로 실제 실행 결과는 후속 작업에서 확인해야 한다.
