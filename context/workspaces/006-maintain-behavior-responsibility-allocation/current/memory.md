# Maintain behavior responsibility allocation memory

마지막 갱신: `2026-08-18`

## 목표

이 Workspace의 원래 목표는 Workspace 005에서 합의한 사용자 경험을 보존하면서 기존 Reference Maintain을 더 단순한 책임 구조로 개선하는 것이었다. 이 접근은 중단됐다. 보존할 결론은 기존 topology가 요구사항이 아니라는 점과, 새 구현이 bounded grounding, warm continuity, response-end 점검, no-change·quiet update·important report·write 전 ambiguity, Main 비차단과 false freshness 방지에서 다시 출발해야 한다는 점이다.

## 적용 기준

- 글로벌 `ai-system_behavior-responsibility-allocation.md`와 연결 references를 판단 기준으로 사용한다.
- 구현 방식을 먼저 고르지 않고 운영상 하나인 동작의 시작 조건, 입력과 맥락, 결과와 부작용, 비목표와 반드시 지킬 약속을 먼저 식별한다.
- Workspace 005 records 01–09를 시간순 근거로 사용한다. 특히 record 02의 고정 topology 과설계 경고, record 06의 Observe delivery 실패, record 08의 교체 가능한 기술 후보와 record 09의 실제 구현·proof ceiling을 분리한다.
- 각 책임을 해석·선택, 보장·거부, 권한·승인, 실행·기록으로 구분한다.
- 의미가 맥락에 따라 달라지는 선택은 모델 판단에 남길 이유를 검토하고, 명확한 predicate와 반복 가능한 거부가 필요한 약속은 schema·validator·permission·code 같은 집행 장치를 검토한다.
- 가치·정책·중요한 예외·되돌리기 어려운 결과·acceptance는 자동화 가능성만으로 모델이나 코드의 권한으로 올리지 않는다.
- 지침은 준수를 표현하고, schema는 허용 형태를 정의하며, validator·code는 실행 시 거부를 집행하고, test·eval은 구현이나 행동의 증거라는 차이를 유지한다.
- 장치를 추가하거나 유지할 때 얻는 보장과 함께 새 상태·실패·복구·검증 책임을 비교한다.
- 각 구성요소는 유지 근거뿐 아니라 제거·통합·다른 정본에서 파생할 수 있는지를 먼저 검토한다.
- 책임을 옮기거나 제거할 때 무엇이 달라지는지 일반적인 진입점에서 다시 찾을 수 있어야 한다.

## 현재 경계

- 006의 Reference code diff는 커밋하지 않고 제거할 대상이다. `completed pair`, `Workspace attention`과 그 migration도 새 구현의 전제가 아니다.
- Workspace 005 records는 사용자 목적, 실패와 proof ceiling의 원자료다. Commit `9553d0a`의 구현 topology는 역사적 결과이지 보존 대상이 아니다.
- 새 구현의 code baseline은 `9553d0a`의 부모 `2649e9b`로 돌리되, Workspace 005 records와 합의 문서는 보존한다.
- 전체 repository reset이나 history rewrite를 하지 않는다. 현재 사용자 소유 파일과 다른 Workspace 기록을 건드리지 않고 path-scoped 복원과 새 커밋으로 상태를 남긴다.

## 소유권

- Workspace 006은 중단된 분석과 구현 시도만 소유한다.
- 새 Workspace가 clean-room 구현의 목표·current·records·output을 소유한다.
- 사용자는 목표, 정책, 중요한 예외, 기능 변화와 acceptance를 결정한다. 새 실행 주체는 006 implementation diff가 아니라 선택된 005 근거와 실제 code baseline에서 판단한다.
