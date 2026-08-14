# Project context

이 디렉터리는 여러 Workspace에 걸쳐 공유되는 실제 Project common context를 소유한다. 기존 제품 문서의 복사본이나 링크 목록이 아니라, 작업 재진입에 필요한 공통 목적·구조·제약·채택 결정을 읽을 수 있는 내용 층이다.

- [`overview.md`](overview.md): 여러 상세 Owner에서 선택한 실제 AI용 Project 공통 맥락과 정합성 경계
- [`prd.md`](prd.md): 제품의 목적, 완료 기준, 범위
- [`architecture.md`](architecture.md): 제품 구현 구조와 검증 경로
- [`decisions/`](decisions/): 여러 작업에 계속 적용되는 채택 결정

Project context의 최소 진입점은 책임·상세 Owner·충돌 우선순위를 설명하는 `README.md`와 실제 공통 맥락을 담은 `overview.md`다. Project 성격에 따라 PRD·architecture·decision을 별도 문서로 더 둘 수 있다.

기존 README·STATUS·docs가 상세 제품 사실을 이미 소유하는 Project에서는 그 문서를 그대로 domain canonical로 유지한다. `overview.md`는 원문을 복사하지 않고 여러 Owner에서 Workspace 공통 판단에 필요한 내용을 압축하며, 근거 경로와 충돌 시 우선할 Owner를 명시한다. 상세 Owner가 바뀌면 overview는 stale 후보이므로 recover 전에 다시 대조한다. 기존 Owner를 `context/project/`로 완전히 옮기는 것은 별도의 승인된 Owner migration이다.

한 Workspace에만 해당하는 목표·현재 상태·분석·후보·검증 이력은 이 층으로 올리지 않는다. 첫 Workspace의 작업 장면도 상세 Owner가 Project 전체에 적용됨을 뒷받침할 때만 Project common context로 일반화한다.

개별 Workspace는 이 문서 전체를 기본 입력으로 읽지 않는다. [`../work/workspaces/`](../work/workspaces/)의 각 `recover.json`이 현재 작업에 필요한 문서와 선택 이유를 Project-root 상대 경로로 명시한다.

제품 코드와 테스트는 이 경계의 내용이 아니며 각각 [`../../src/`](../../src/)와 [`../../tests/`](../../tests/)가 소유한다. Harness는 이 기준을 선택해 읽을 뿐 정의하거나 갱신하지 않는다.
