# 현재 범위와 Maintain 경계 교정

기록일: `2026-08-14`
상태: 사용자 최신 정정 반영, 구현 전 마지막 점검 대기

## 교정한 현재 범위

현재 출발점과 구현 분석 대상은 `reference-project`의 Recover·Verify 병목이다. 이를 개선하려고 현재 기능을 펼친 뒤 Recover·Maintain·Verify·Harness check 책임과 program·agent·main·human 주체를 다시 나누는 논의를 진행했다.

Maintain 책임은 버린 것이 아니다. 작업 중 의미 변화를 `current/records/output`의 Owner 경계에 맞게 반영하는 중요한 책임 후보로 유지한다. 다만 이 책임 모델 전체와 구체 구현은 아직 사용자에게 채택되지 않았다.

현재 범위에 포함하지 않는 것은 다음과 같다.

- `apply-context-harness` skill 개선
- 다른 Project 이식과 계약 전파 개선
- Project common context와 Workspace `current/source/output/records` 구조 변경
- 새 CLI·module·agent·schema의 확정 또는 구현

Skill과 다른 Project 이식 문제는 Reference 내부 책임을 먼저 검토한 뒤 다룰 이후 단계다.

## Maintain 책임과 outer agent의 경계

루트 [`.codex/agents/context-maintainer.toml`](../../../../.codex/agents/context-maintainer.toml)은 outer `context-harness` 저장소의 Workspace 004 current·records를 유지하기 위한 repo-local agent다. 이것은 `reference-project` 안에 구현된 Maintain 책임이 아니다.

현재 파일 대조에서는 `reference-project` 안에 이 agent가 없고, `apply-context-harness` skill도 이를 대상 Project에 설치하지 않는다. 이 사실은 Maintain 책임이 필요한지와 별개다.

따라서 다음 두 과교정을 피한다.

- outer agent를 Reference Maintain 구현으로 끌어오지 않는다.
- outer agent와 Reference가 분리돼 있다는 이유로 Maintain 책임 후보를 버리지 않는다.

앞선 [책임·주체 종합 기록](2026-08-14-03-harness-responsibilities-actors-and-implementation-layers.md)이 outer repo의 현재 maintenance routing을 설명한 부분은 그 운영 사실의 기록이다. Reference 구현 채택을 뜻하지 않으며, 이 교정 기록이 현재 해석 범위를 제한한다.

## 지금 유지하는 후보와 마지막 점검

Recover·Maintain·Verify·Harness check 책임과 program·agent·main·human 주체를 분리해 보는 모델은 구현 전 검토할 후보로 유지한다. 책임 이름이 곧 새 명령·Python module·agent를 뜻하지 않는다.

구현 전에 fresh verifier가 다음을 마지막으로 교차 확인한다.

1. Workspace 004 current·records가 사용자 최신 정정을 그대로 반영하는지
2. 현재 분석 대상이 Reference Recover·Verify로 제한됐는지
3. Maintain 책임과 outer repo-local agent가 섞이지 않았는지
4. 실제 `reference-project` 코드와 agent 위치·부재 설명이 맞는지
5. Skill·다른 Project 이식·Context 구조 변경이 현재 범위로 다시 들어오지 않았는지

이 점검 전에는 runtime, root agent·routing, skill을 변경하지 않는다.
