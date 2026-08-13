# Project application Workspace

`output/`에서 검증한 context+harness 책임을 실제 기존 Project 하나에 적용해 보고, 그대로 복사할 부분과 대상 Project에 맞게 바꿔야 할 부분을 확인하는 다음 작업 Workspace다.

상태는 **ready**다. 아직 대상 Project가 지정되지 않았으므로 다른 Desktop 저장소는 조사하지 않는다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 적용 목표·기준·제약·reference 접근점
2. [`current/state.md`](current/state.md): 현재 준비 상태와 다음 행동
3. [`records/`](records/): 대상 Project를 정한 뒤 생기는 분석·migration·검증 기록

이 Workspace는 `output/context/work`의 전체 구조를 정답처럼 복제하지 않는다. 대상 Project의 기존 canonical과 배치를 먼저 확인하고, 필요한 책임과 운영 흐름만 최소로 적용한다.
