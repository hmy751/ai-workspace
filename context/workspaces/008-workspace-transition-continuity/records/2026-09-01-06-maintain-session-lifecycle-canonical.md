# Maintain 내부 session lifecycle canonical 책임 정렬

날짜: `2026-09-01`

## 다시 검토한 질문

Session별 explicit admission과 generation 전환을 구현한 뒤, 이 책임을 Maintain과 별도의 Harness 단위로 떼고 새 이름을 줄지 논의했다. 그러나 최근 대화의 “분리”와 이름 선택만 따라가면 실제 행동 경계보다 문서 구조가 먼저 책임을 만들어 낼 수 있었다. 전체 AI system에서 다시 보면 binding runtime은 Recover·Verify나 일반 Workspace routing이 함께 쓰는 독립 lifecycle이 아니라, Maintain이 선택된 Workspace에서 시작하고 Main response-end를 처리하며 비동기 결과를 전달하기 위한 host 연결과 운영 truth다.

따라서 Session binding을 Recover·Maintain·Verify와 나란한 새 Harness peer로 만들지 않았다. 별도 peer를 만들면 Maintain의 한 response-end 행동을 여러 최상위 Owner가 나눠 갖고, adapter를 제거할 때 남아야 할 semantic 계약과 함께 제거해야 할 host 장치의 경계도 흐려진다.

## 확정한 Owner

- [`Maintain README`](../../../../reference-project/context/work/harness/maintain/README.md)는 Maintain 전체의 정체성·범위·비소유 경계와 내부 세 책임의 관계를 소유한다. 세 책임은 session binding과 lifecycle, semantic 판단, guarded apply다.
- [`SESSION-BINDING-AND-LIFECYCLE.md`](../../../../reference-project/context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md)는 Maintain 내부 authoritative subcanonical이다. 새 session의 unbound 기본값, explicit activation·rebind·deactivation, generation commit과 prompt·response-end 귀속, late worker·failure·notice, 민감 runtime·retention, config migration과 actual-host 증명 상한을 소유한다.
- [`CREATE-AND-TRANSITION.md`](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md)는 새 Workspace를 왜·언제 만들고 어떤 의미를 successor가 직접 소유해야 하는지, 현재 binding과 미처리 상태를 보고 같은 Main session을 이어 갈지 새 session으로 격리할지를 판단하는 Workspace canonical로 남는다. 그 결정 뒤 generation과 hook event를 기계적으로 처리하는 상세 계약은 Maintain 내부 canonical을 참조한다.

이 배치는 “진입점과 소유를 확실히 한다”는 목적을 문서 수 증가가 아니라 행동 책임의 실제 관계로 구현한다. Uppercase 파일명은 Maintain 디렉터리 안에서 README 다음에 읽을 권위 있는 운영 계약이라는 역할을 드러내지만, 상위 Harness taxonomy를 추가한다는 뜻은 아니다.

## 기존 구현과의 관계

이번 정렬은 2026-09-01에 이미 구현·검증한 기능을 다시 설계하거나 이동하는 변경이 아니다. Schema v2 explicit config, 새 session default-unbound, session별 generation history, A→B→A, rollback, predecessor late worker 격리, generation-local failure와 v1 compatibility를 유지한다.

`host_adapter.py`, `codex_session.py`, Project `.codex` wrapper, `.codex/maintain-runtime/`, `status|activate|deactivate`와 `maintain` 이름도 그대로 둔다. 새 canonical은 이 구현들이 Maintain 안에서 어떤 보장과 한계를 집행하는지 찾게 할 뿐, runtime을 다른 디렉터리로 옮기거나 session state를 공통 Workspace selection 장치로 승격하지 않는다.

## 문서 응집과 증명 상한

Maintain README에는 내부 책임 지도와 전체 semantic 계약을 남기고, session generation·hook·worker·runtime 세부는 새 canonical 한 곳에서 소유하게 했다. CREATE canonical은 전환의 의미 판단을 유지하고 runtime 실행 세부를 복제하지 않는다. Root·Work routing, Reference 사람용 진입점, create-context-workspace와 apply-context-harness는 각자 필요한 경계에서 새 canonical로 이어진다.

새 canonical은 runtime이 사용자 prompt 전체와 Main response 전체를 포함한다는 민감도, `deactivate`가 cleanup이 아니라는 점, retention과 삭제 승인이 사람·Project 운영자 책임이라는 점도 명시한다. Main-only control은 현재 인증된 caller 권한이 아니라 운영 정책이며, 실제 Codex host의 hook trust·event 순서·worker 생존·notice UI 전달, resume sandbox 보존과 failed-grounding thread 정리는 별도 acceptance 전에는 보장하지 않는다.

Target 문서 적응과 최종 link·test·Git 검증 결과는 이 판단 기록이 대신 주장하지 않는다. 실제 적용 결과는 Main 실행에서 target의 기존 runtime·사용자 문서·Workspace 004를 보존한 채 별도로 대조한다.
