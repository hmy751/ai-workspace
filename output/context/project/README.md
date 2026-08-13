# Project context

이 디렉터리는 여러 Workspace에 걸쳐 공유되는 Project common context의 canonical을 소유한다.

- [`prd.md`](prd.md): 제품의 목적, 완료 기준, 범위
- [`architecture.md`](architecture.md): 제품 구현 구조와 검증 경로
- [`decisions/`](decisions/): 여러 작업에 계속 적용되는 채택 결정

개별 Workspace는 이 문서 전체를 기본 입력으로 읽지 않는다. [`../work/workspaces/`](../work/workspaces/)의 각 `recover.json`이 현재 작업에 필요한 문서와 선택 이유를 Project-root 상대 경로로 명시한다.

제품 코드와 테스트는 이 경계의 내용이 아니며 각각 [`../../src/`](../../src/)와 [`../../tests/`](../../tests/)가 소유한다. Harness는 이 기준을 선택해 읽을 뿐 정의하거나 갱신하지 않는다.
