# context-harness local instructions

## Re-entry

지속 작업을 시작할 때는 `context/active/index.md`에서 시작해 연결된 `project.md`와 `work.md`를 읽는다. history 전체나 source 전체를 기본으로 읽지 않고, active가 가리키는 자료만 필요할 때 연다.

## Context maintenance routing

다음 중 하나가 생긴 작업은 자연스러운 종료 경계에서 `context_maintainer` subagent에게 context 정합성 점검을 한 번 맡긴다.

- 프로젝트 목표·기준·제약 또는 source 경계가 바뀜
- 현재 문제·작업 커서·다음 행동이 바뀜
- 의미 있는 결정, 실패, blocker, 검증 결과, 완료 또는 폐기가 생김
- `context/active/`가 실제 파일·Git 상태·test 결과·사용자 정정과 어긋날 가능성이 생김

단순 질의, 표현 수정, 일회성 탐색처럼 지속 상태가 바뀌지 않은 작업에는 호출하지 않는다. 명령·도구 출력마다 history를 만들지 않는다.

`context_maintainer`가 수정한 diff와 근거는 main이 검토한다. 사용자 목표·승인 결정·새로운 설계 기준을 subagent가 대신 확정하게 하지 않는다. agent를 호출할 수 없는 환경이면 main이 같은 점검을 수행하고 그 사실을 보고한다.

## Source boundary

`context/source/`의 raw snapshot과 prior-work snapshot은 읽기 전용 원본으로 취급한다. 새 해석이나 현재 판단을 source에 쓰지 않는다. 사용자가 지정하지 않은 다른 Desktop 저장소로 조사 범위를 넓히지 않는다.
