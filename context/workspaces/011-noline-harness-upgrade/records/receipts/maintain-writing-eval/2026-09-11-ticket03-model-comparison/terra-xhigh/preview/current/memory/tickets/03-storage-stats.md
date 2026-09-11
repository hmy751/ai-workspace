# 03 — 저장 용량 통계

## 맡은 결과와 범위

`useStorageStats`의 저장 용량 조회 흐름과 기존 프로필 표시를 보존하면서, 성공 경로와 바깥 오류 처리에서 반복되는 `StorageStats` 조립을 한곳으로 모은다. 이 리팩터링의 회귀를 막을 수 있는 좁은 hook 테스트 기반도 함께 마련한다.

다음 동작은 보존한다.

- DB 파일 조회 중 실패하면 그때까지 합산한 DB 용량을 남기고 Mapbox 조회를 시작하지 않는다.
- `getPacks()` 실패 시 DB 결과를 보존하고 지도 용량은 `0 B`로 처리한다.
- 개별 `pack.status()` 실패는 건너뛰고 다음 팩 집계를 계속한다.
- 용량 표시는 1,024 단위, 소수 최대 한 자리이며 0은 `0 B`로 표시한다.
- 프로필 화면이 사용하는 `dbSize`와 `mapPackSize`의 의미를 바꾸지 않는다. `totalSize`의 화면 표시 추가나 반환 필드 제거는 이 Ticket 범위가 아니다.

실제 FileSystem·Mapbox 네이티브 구현의 정확성, 프로필 화면 전체 렌더링, 새 E2E 기반 구축은 이번 범위에서 제외한다.

## 실행 맥락과 접근

테스트는 `apps/client`가 소유한다. Expo React Native hook과 네이티브 모듈의 결과·실패 순서를 제어해야 하므로 Jest, `jest-expo`, React Native Testing Library를 사용하고, FileSystem과 Mapbox는 테스트별 `jest.mock()`으로 대체한다.

테스트와 설정은 제품 source 및 다른 workspace와 분리한다.

```text
apps/client/
├── jest.config.cjs
├── tsconfig.test.json
└── tests/features/profile/hooks/useStorageStats.test.ts
```

- Jest 설정에는 `jest-expo` preset, 테스트 경로, client 내부 `@/` 별칭만 둔다.
- 테스트용 TypeScript 설정은 제품 `tsconfig.json`과 Jest 타입을 분리한다.
- 공용 `__mocks__`, setup 파일, fixture 폴더, coverage 기준, root 공용 Jest 설정 및 새 test-config package는 지금 만들지 않는다.
- Mapbox·FileSystem mock은 우선 이 테스트 파일 안에 두고, 실제 두 번째 소비자가 생길 때만 feature helper 또는 공용 mock으로 승격한다.
- 의존성은 root가 아니라 `apps/client/package.json`에 선언한다. 다른 package의 test runner·preset·테스트 디렉터리를 이번 Ticket에서 통일하거나 추가하지 않는다.
- SDK 호환 의존성 버전과 필요한 `transformIgnorePatterns`는 최초 설치·실행 결과를 보고 정한다. 확인 전에는 추측으로 고정하지 않는다.

상세 선택 이유와 채택하지 않은 대안은 [저장 용량 통계 테스트 전략](../../../../records/2026-09-11-02-storage-stats-test-strategy.md)에 남긴다.

## 완료 조건과 확인 방법

리팩터링 전후 같은 hook 계약 테스트로 다음을 확인한다.

- 빈 DB·지도 팩에서 각 용량과 합계가 `0 B`로 계산된다.
- 대상 DB 파일만 합산하며 무관한 파일은 조회하지 않는다.
- 1,024 및 1,536 bytes 등 단위·소수 표시 경계에서 DB·지도·합계 문자열이 유지된다.
- DB 파일 조회 중간 실패는 부분 DB 결과를 보존하고 Mapbox 호출을 막는다.
- `getPacks()` 실패는 DB 결과를 보존한다.
- 개별 팩 상태 조회 실패 뒤에도 다음 팩을 조회하고 성공한 팩만 합산한다.
- `refresh()`는 이전 결과에 누적하지 않고 새 조회 결과로 다시 계산한다.

결과값뿐 아니라 DB 실패 후 Mapbox를 호출하지 않는지, 팩 하나의 실패 뒤 다음 팩을 계속 조회하는지처럼 이 Ticket이 보존하는 중단·계속 조건을 확인한다. helper 이름, `setStats` 횟수, 모든 내부 호출 순서를 고정하지 않는다.

가능하면 development build에서 한 플랫폼의 DB 생성 전후, 오프라인 지도 다운로드 전후, 재진입 또는 `refresh()` 후 표시 변화를 smoke test 한다. 확인하지 않은 플랫폼과 실제 네이티브 팩 동작은 미확인으로 남긴다.

## 현재 상태와 실제 결과

전략은 2026-09-11 논의에서 채택되었으나, 이 기록 시점에는 의존성 설치·설정 작성·제품 코드 변경·테스트 실행이 보고되지 않았다. 이전 Main의 코드 관찰은 관련 구현이 Ticket의 실패 순서와 일치하고 client에 제품 테스트 파일·실행 스크립트가 없었다고 보고했지만, 이 Ticket 문서는 그 관찰이나 제품 검증을 독립적으로 재실행한 근거는 아니다.
