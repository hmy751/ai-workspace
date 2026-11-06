# Design system Personal Workspace

프론트엔드에서 토큰·레이아웃·컴포넌트·화면을 층으로 쌓는 사용자의 판단을 `design-system` Personal로 정리하기 위한 작업이다. 먼저 사용자의 과거 코드와 문서에서 근거를 모으고, 그 결과에서 Personal 후보를 고른다.

현재는 **Personal 2차 초안과 형성 자료 작성 완료 / 재측정 전** 단계다. 저장소가 공개이므로 수집 기록은 Git에서 제외된 `records/collection/`에 둔다.

## 재진입

1. [`current/index.md`](current/index.md)
2. [`current/memory.md`](current/memory.md)
3. [`current/state.md`](current/state.md)
4. [`output/index.md`](output/index.md)
5. 현재 판단, 조사 대상, 수집 결과는 [`로컬 수집 기록`](records/collection/README.md) (Git 제외, 이 컴퓨터에만 있음)
6. 주제 전체와 방법의 상세가 필요하면 [`범위와 수집 계획`](records/2026-11-04-01-scope-and-collection-plan.md)

## 범위

- **포함:** 디자인 시스템 전반의 판단 근거 수집, 자료 간 대조, Personal 후보 정리, 사용자가 후보를 고른 뒤의 본문 작성
- **제외:** 조사 대상 저장소 수정, 실제 Project의 토큰·컴포넌트 구현이나 리팩터링, 브랜드·시각 디자인 자체의 평가
- **조사 대상:** 사용자가 지정한 dev-hub, InterPersona, Noline, oround(본인 담당분), POD-SHOP, template으로 한정한다.

## 책임 경계

- **이 Workspace:** 수집 근거, 대조 분석, 후보 선택 과정을 소유한다.
- **Personal:** 완성된 개인 판단 기준을 소유한다. 채택한 본문은 [`reference-project/context/personal/development/`](../../../reference-project/context/personal/development/INDEX.md)에 먼저 적용한다. 다른 Project 반영은 별도로 판단한다.
- **각 Project:** 실제 토큰·컴포넌트와 제품별 규약을 소유한다. Noline의 디자인 시스템은 Personal로 옮기지 않는다.
- **[Workspace 014](../014-ai-development-workflow-design/):** Personal·Project·Work 구조의 설계를 소유한다. 이 Workspace는 그 구조를 쓸 뿐 다시 설계하거나 014의 상태를 이어 쓰지 않는다.
