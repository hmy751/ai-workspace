# 증거 중심 사이클 폐기와 기능 core 보존

날짜: 2026-07-17

## 사용자 교정

사용자는 정적 심사자 페이지가 합의한 제품 사용 장면을 보여 주지 못하고, 상품 ID·option ID·revision·scope 같은 내부 값을 전면에 노출해 실제 여행자가 쓸 수 없는 결과가 됐다고 지적했다. 이어 최근 작업을 뒤엎되 기능 개발분만 남기라고 결정했다.

선택한 솔루션의 실제 시작은 `상품 URL 또는 본문 + 자연어 여행 조건`이다. 통제 입력과 내부 상태를 나열한 페이지는 이 계약을 구현하거나 시연하지 않았다. 통제 비교와 기술 재현성도 실제 사용자 제품과 가치의 대체물이 아니다.

## 적용한 변경

- `src/tour-purchase-review/`의 plugin 기능 코드, fixture와 product test는 보존한다.
- 정적 `reviewer-artifact/` 전체를 제거한다.
- 현행 상품·통제 여행자 비교를 담은 `context/engineering/02-live-product-controlled-evidence/`를 현재 산출물에서 제거한다.
- product test가 삭제한 증거 JSON을 직접 참조하던 결합을 없애고 `src/` 내부 fixture만으로 실행되게 한다.
- Loop 02의 개방과 수행 이력은 Git과 [process/35](./35-open-live-product-controlled-evidence-loop.md)에 남지만, 완료된 제품·가치 증거로 사용하지 않는다.

## 현재 판정

보존한 것은 구조화 입력 이후의 조건 계약, 승인, 질문, 답변 적용, 상태 전이, decision card와 저장 기능이다. 사용자가 상품 URL과 자연어 조건을 주면 상품 조회부터 이 core까지 이어지는 실제 사용자 end-to-end는 아직 제품으로 완성·검증하지 않았다.

이 결정은 Campaign Goal을 약화하거나 바꾸는 amendment가 아니다. 잘못 완료 처리한 증거 사이클을 현재 결과에서 제외하고 실제 구현 상태로 지도를 되돌리는 경로 교정이다. 다음 loop나 제출 단계는 자동으로 열지 않는다.
