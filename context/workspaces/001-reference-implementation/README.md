# Reference implementation Workspace

source intake부터 context 운영 경계 정리, 실행 가능한 `output/` reference 구현, Workspace current 폴더화, Harness 책임 분리, Project root와 Work root 분리까지 지금까지 수행한 작업을 보존하는 Workspace다.

상태는 **완료**다. 구현과 문서는 commits `2b110a3`, `e3c237b`에 반영됐으며, 새 실제 Project 적용 작업은 형제 Workspace [`002-project-application`](../002-project-application/)에서 진행한다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 이 작업에서 계속 유효한 목표·기준·결정·검증 상한
2. [`current/state.md`](current/state.md): 완료 상태와 최종 근거
3. [`records/`](records/): 설계·migration·구현·검증의 상세 과정
4. 저장소 루트 [`output/`](../../../output/): 실행 가능한 reference 산출물

이 Workspace를 다시 active로 전환하지 않는 한, 후속 적용 작업의 상태나 기록을 이곳에 추가하지 않는다.
