# context-harness local instructions

## Context contract

context 층의 canonical 역할은 `context/README.md`가 소유한다.

- `context/current/`: 다음 세션이 바로 행동하기 위해 읽는 현재 상태. `project.md`와 `work.md`로 나눈다.
- `context/records/`: 작업 중 만든 지속 가능한 문서·분석·중간 산출물·검증 기록의 누적층. 여기에 있다는 이유만으로 현재 상태가 되지는 않는다.
- `context/source/`: 원자료와 provenance. 현재 판단이나 새 해석을 쓰지 않는다.
- `output/`: 목표에 따른 실제 산출물. 분석 문서와 context 기록을 대신 보관하지 않는다.

## Re-entry

지속 작업을 시작할 때는 `context/current/index.md`에서 시작해 연결된 `project.md`와 `work.md`를 읽는다. records 전체나 source 전체를 기본으로 읽지 않고, 현재 질문에 필요한 자료만 current의 접근점에서 선택한다.

## Context maintenance routing

다음 중 하나가 생긴 작업은 자연스러운 종료 경계에서 `context_maintainer` subagent에게 context 정합성 점검을 한 번 맡긴다.

- 계속 보존할 작업 문서·분석·중간 산출물·검증 기록이 생김
- 프로젝트 목표·기준·제약, source 경계 또는 output 경계가 바뀜
- 현재 문제·상태·불확실성·작업 커서·다음 행동이 바뀜
- 결정, 실패, blocker, 검증, 완료, 폐기로 현재 영향이 달라짐
- `context/current/`가 실제 파일·Git 상태·test 결과·사용자 정정과 어긋날 가능성이 생김

일회성 탐색이나 임시 명령 출력을 매번 records로 만들지는 않는다. 다만 후속 작업에서 다시 사용할 분석이나 결과라면 상태 변화가 없어도 records에 보존한다.

`context_maintainer`가 수정한 diff와 근거는 main이 검토한다. 사용자 목표·승인 결정·새로운 설계 기준을 subagent가 대신 확정하게 하지 않는다. agent를 호출할 수 없는 환경이면 main이 같은 점검을 수행하고 그 사실을 보고한다.

## Source boundary

`context/source/`의 raw snapshot과 prior-work snapshot은 읽기 전용 원본으로 취급한다. 새 해석이나 현재 판단을 source에 쓰지 않는다. 사용자가 지정하지 않은 다른 Desktop 저장소로 조사 범위를 넓히지 않는다.
