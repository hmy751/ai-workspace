# Workspace memory map

이 폴더에는 작업 단계나 최근 검증 결과가 바뀌어도 계속 유효하고, 다음 작업자가 모르면 판단이 달라지는 현재 맥락만 둔다. 과거 상태와 상세 실행 결과는 `records/`에 남기며 이곳에 누적하지 않는다.

## 현재 문서

- [`01-goal.md`](01-goal.md): 이 Workspace가 해결할 문제와 완료 기준
- [`02-constraints.md`](02-constraints.md): 작업 중 계속 지켜야 하는 결정과 제약
- [`03-project-context.md`](03-project-context.md): 이번 작업에 필요한 상위 Project 맥락과 선택 경계

`recover`는 이 index를 먼저 읽고 같은 폴더의 나머지 Markdown 문서를 파일명 순서로 읽는다. 새 memory 문서는 지금도 유효하고 기본 재진입에 항상 필요한 경우에만 추가한다.
