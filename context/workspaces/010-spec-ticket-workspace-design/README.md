# Spec·Ticket과 Workspace 설계

Spec·Ticket을 실제 개념과 용어로 사용하면서 기존 Workspace/current와 어떤 관계를 맺을지 사용자와 설계하는 연구 Workspace다. Spec-driven 운영에 비해 Project·Work를 별도로 관리하는 선택의 이유와 비용도 함께 검토한다.

2026-09-07 사용자가 이번 대화 처음부터의 작업을 009와 분리해 010에 기록하도록 요청했다. 이 Workspace의 범위는 최초 Spec·Ticket 외부 조사 요청부터 current와의 중복, 개발 영향 조사, 스냅샷 조건, memory/state 역사 검토, 배치 후보, 제3 리뷰와 개념 트레이드오프 재검토까지다. 009의 선행 Project context 구현을 이번 세션의 성과로 포함하지 않는다.

현재는 Spec의 다섯 구성요소·이유·예시, memory의 Spec·Ticket 배치와 기존 goal·constraints 대체를 정한 설계 단계다. 기존처럼 Maintain은 기록·갱신을, Main은 작업 조율을 맡는다. Reference의 실제 적용은 시작하지 않았다.

## 재진입

1. [current/index.md](current/index.md)에서 현재 읽기 순서를 확인한다.
2. [current/memory.md](current/memory.md)에서 목적·조건·유지할 합의를 읽는다.
3. [current/state.md](current/state.md)에서 현재 단계와 남은 적용 작업을 읽는다.
4. [output/index.md](output/index.md)에서 채택한 구성 설명·예시를 찾는다.

기록 정리 시점의 전체 합의와 남은 일은 [설계 정리 기록](records/2026-09-08-11-design-status-and-remaining-work.md)에 있다. 판단 이유나 사용자 원문이 필요하면 [records 색인](records/README.md)에서 해당 기록만 선택한다. 당시 제거·분리 후보나 리뷰 권고는 이후 사용자 선택과 구별해 읽는다.

## 범위와 현재 지위

- 개념 사용의 방향과 구체적인 파일 배치·범위·갱신 방식의 결정을 구분한다.
- Spec·Ticket 정의, 전체 목표, Workspace별 독립 스냅샷, 현재와 과거, 읽기와 갱신 책임을 함께 설계한다.
- 초기 코드 영향 분석은 설계 자료다. 개념의 채택 이유를 기존 Recover·Maintain 수정 비용만으로 판단하지 않는다.
- 현재는 Spec의 내용·배치·기존 파일과의 관계를 정한 설계 단계다. Reference의 실제 파일·runtime·schema·hook 변경은 아직 진행하지 않는다.
- 기록과 산출물 정리는 승인됐으며, 이전의 Reference 구현 보류를 해제한 것으로 해석하지 않는다.

## 내부 책임과 009와의 관계

이 연구 작업대의 [context 계약](../../README.md)에 따라 current는 memory.md와 state.md로 나눈다. 논의 중인 Reference의 memory/spec·tickets 폴더를 이 Workspace에 먼저 구현하지 않는다. 출력물은 output/index.md가, 과정과 판단 이유는 records가 맡는다. Reference의 machine 계약이나 자동 Maintain을 복제하지 않는다.

009에서 작성한 초기 Spec 비교·개발 영향 기록은 원래 경로에 보존하고 정확한 파일만 참고한다. 현재 적용하는 의미는 010의 current에 직접 서술하며 009의 current를 기본 입력으로 삼지 않는다. 두 Workspace는 자동 동기화하지 않는다. 009는 기존 Project context 통합 결과와 그 작업의 미완료 검증을 계속 소유한다.
