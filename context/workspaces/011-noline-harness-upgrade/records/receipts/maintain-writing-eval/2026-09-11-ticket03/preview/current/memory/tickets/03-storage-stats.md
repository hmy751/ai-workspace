# 03 — 저장 용량 통계

## 맡은 결과와 범위

`useStorageStats`에서 성공 경로와 바깥 오류 처리에 흩어진 `StorageStats` 조립을 한곳으로 모은다. DB와 오프라인 지도 팩의 용량을 집계해 기존 프로필 화면에 전달하는 동작은 유지한다.

이번 범위에는 부분 결과와 실패 순서의 보존을 검사하는 hook 테스트 기반도 포함한다. 프로필 화면의 새 표시를 추가하거나 `totalSize` 반환 필드를 제거하지 않으며, 화면 전체 E2E나 네이티브 저장소 구현 자체의 검증은 이 Ticket의 자동화 범위가 아니다.

## 실행 맥락과 접근

`apps/client`가 테스트 도구와 Jest 설정을 소유한다. Expo 환경의 hook을 직접 실행하는 Jest, `jest-expo`, React Native Testing Library 조합을 사용하고, FileSystem과 Mapbox는 테스트별 module mock으로 제어한다.

테스트는 `apps/client/tests/features/profile/hooks/useStorageStats.test.ts`에 두어 제품 TypeScript 범위와 Expo Router route 경로에서 분리한다. root 공용 Jest 설정이나 다른 package를 위한 공용 test-config는 만들지 않는다. 순수한 표시값 조립 함수가 자연스럽게 생기면 보조적으로 분리·검사할 수 있지만, DB 실패가 지도 조회를 중단하는지와 지도 팩 실패 뒤 다음 팩을 계속 처리하는지는 hook 수준에서 확인한다.

상세 선택지와 제외 이유는 [저장 용량 테스트 전략](../../../../records/2026-09-11-02-storage-stats-test-strategy.md)에 남긴다.

## 완료 조건과 확인 방법

- DB 대상 파일만 집계하고 단위·소수 표시 규칙을 보존한다.
- DB 파일 조회 중 실패하면 그때까지의 DB 결과를 보존하고 Mapbox 조회를 시작하지 않는다.
- `getPacks()` 실패 시 DB 결과를 보존하고 지도 용량은 0으로 처리한다.
- 개별 `pack.status()` 실패는 건너뛰고 다음 팩을 계속 집계한다.
- `refresh()`는 이전 결과에 누적하지 않고 다시 계산한다.
- 실제 최초 설치에서 Expo SDK 51 호환 의존성, 필요한 변환 설정, Mapbox mock 형태를 확인한다.

## 현재 상태와 실제 결과

미착수다. 대화에서 Main은 관련 구현이 Ticket의 관찰과 일치하며 제품 코드와 테스트에는 아직 변경이 없다고 보고했다. 이 문서의 테스트 전략은 사용자와 Main이 논의해 채택한 실행 기준이며, 테스트 설치·실행이나 실기기 smoke test가 수행되었다는 증거는 없다.
