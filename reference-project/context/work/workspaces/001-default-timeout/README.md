# Default timeout Workspace

설정에서 `request_timeout_ms`가 빠졌을 때 Project가 정한 기본값 `5000`밀리초를 사용하도록 구현·확인하는 작업 공간이다. 명시값 유지·잘못된 입력 거부·불변 policy가 범위이며 실제 네트워크 실행은 포함하지 않는다.

## 재개

[재개 안내](recover.md)에서 현재 초점과 기본·조건부 읽기 범위를 찾는다. 내용별 탐색은 [memory 색인](current/memory/index.md)이 맡고, 현재 상황·다음 판단은 [state](current/state/index.md)가 소유한다. 전체 문서를 같은 순서로 매번 읽지 않는다.

## Workspace가 소유하는 내용 층

- [current](current/): memory의 Spec·Ticket·Project 선택과 state의 전체 상황·판단·다음 행동. [구성·관리 기준](../spec-and-tickets/README.md)을 따른다.
- [source](source/index.md): 이 Workspace가 선택한 원문·snapshot·provenance. 원래 출처의 권위를 유지하고 현재 해석은 쓰지 않는다.
- [output](output/index.md): 선택한 현재 산출물의 canonical 위치. Project의 코드·검사는 복제하지 않는다.
- [records](records/README.md): 선택·실행·검증 근거. 과거 Verify receipt는 당시 증거로 보존한다.

기존 기계 계약과 실행기를 내려놓은 이유·보존 위치는 [전환 기록](records/2026-11-04-recovery-guide-transition.md)에 있다. 현재 재개·기록은 [Work 지침](../../AGENTS.md), 생성·전환은 [해당 계약](../CREATE-AND-TRANSITION.md)을 따른다.
