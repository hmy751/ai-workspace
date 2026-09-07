# Spec·Ticket과 Workspace 설계

Spec·Ticket을 실제 개념과 용어로 사용하면서 기존 Workspace/current와 어떤 관계를 맺을지 사용자와 설계하는 연구 Workspace다. Spec-driven 운영에 비해 Project·Work를 별도로 관리하는 선택의 이유와 비용도 함께 검토한다.

2026-09-07 사용자가 이번 대화 처음부터의 작업을 009와 분리해 010에 기록하도록 요청했다. 이 Workspace의 범위는 최초 Spec·Ticket 외부 조사 요청부터 current와의 중복, 개발 영향 조사, 스냅샷 조건, memory/state 역사 검토, 배치 후보, 제3 리뷰와 개념 트레이드오프 재검토까지다. 009의 선행 Project context 구현을 이번 세션의 성과로 포함하지 않는다.

## 재진입

1. [current/index.md](current/index.md)에서 현재 읽기 순서를 확인한다.
2. [current/memory.md](current/memory.md)의 목적·사용자 조건·후보의 지위를 읽는다.
3. [current/state.md](current/state.md)에서 확인한 결과와 다음 판단을 읽는다.
4. [output/index.md](output/index.md)에서 종합 기록과 실제 조사 근거를 찾는다.
5. 논의의 이유와 정정을 확인할 때 [세션 종합 기록](records/2026-09-07-01-session-synthesis.md)을 읽는다.

## 범위와 현재 지위

- 개념 사용의 방향과 구체적인 파일 배치·범위·갱신 방식의 결정을 구분한다.
- Spec·Ticket 정의, 전체 목표, Workspace별 독립 스냅샷, 현재와 과거, 읽기와 갱신 책임을 함께 설계한다.
- 초기 코드 영향 분석은 설계 자료다. 개념의 채택 이유를 기존 Recover·Maintain 수정 비용만으로 판단하지 않는다.
- 현재는 설계·조사 단계다. Reference의 Spec 구조·runtime·schema·hook을 변경하는 합의는 없다.
- 이번 요청은 연구 Workspace 생성과 기록·진입점 정리를 허용했다. 이전의 구현 보류를 해제한 것으로 해석하지 않는다.

## 내부 책임과 009와의 관계

이 연구 작업대의 [context 계약](../../README.md)에 따라 current는 memory.md와 state.md로 나눈다. 논의 중인 Reference의 memory/spec·tickets 폴더를 이 Workspace에 먼저 구현하지 않는다. 출력물은 output/index.md가, 과정과 판단 이유는 records가 맡는다. Reference의 machine 계약이나 자동 Maintain을 복제하지 않는다.

009에서 작성한 초기 Spec 비교·개발 영향 기록은 원래 경로에 보존하고 정확한 파일만 참고한다. 현재 적용하는 의미는 010의 current에 직접 서술하며 009의 current를 기본 입력으로 삼지 않는다. 두 Workspace는 자동 동기화하지 않는다. 009는 기존 Project context 통합 결과와 그 작업의 미완료 검증을 계속 소유한다.
