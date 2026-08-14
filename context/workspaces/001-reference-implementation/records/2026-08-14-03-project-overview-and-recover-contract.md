# 실제 Project overview와 recover 계약

날짜: `2026-08-14`

## 사용자 결정

루트 `output/`은 이식 절차 자체가 아니라 이식이 끝난 뒤의 책임 구조와 실행 계약을 소유한다. Repo-local `apply-context-harness` skill은 대상 Project의 원자료와 기존 canonical을 조사해 그 도착점으로 옮기는 방법을 소유한다.

완료된 reference와 이식 target의 `context/project/`에는 다음 최소 진입점이 있어야 한다.

- `README.md`: Project common context의 책임, 상세 Owner, 충돌 우선순위와 갱신 조건
- `overview.md`: 여러 Workspace가 공통으로 알아야 할 실제 제품 목적·범위·구조·제약·채택 결정·검증 경계와 근거 경로

`overview.md`는 기존 docs의 복제본이나 링크 목록이 아니다. 상세 사실의 기존 Owner는 유지하고, 여러 Workspace의 판단에 필요한 내용을 원자료가 지지하는 범위에서 다시 구성한다. 상세 Owner와 충돌하면 상세 Owner를 우선하고 overview를 stale로 보며, 기존 Owner 자체를 `context/project/`로 옮기는 일은 별도 승인된 migration이다.

## reference와 skill에 반영된 계약

- [`output/context/project/README.md`](../../../../output/context/project/README.md)가 최소 진입점과 Owner 우선순위를 설명하고, [`overview.md`](../../../../output/context/project/overview.md)가 sample Request policy 제품의 실제 공통 맥락을 담는다.
- Recover contract는 schema `4`다. 선택 경계를 Project root의 `context/project/` 아래 regular Markdown으로 고정하고 `context/project/overview.md`를 첫 항목으로 요구한다.
- 이전 reference schema `2`와 첫 실제 적용에서 다른 의미로 사용한 target-local schema `3`은 재사용하지 않는다. Recovery packet 구조는 바뀌지 않아 schema `5`를 유지한다.
- Sample Workspace는 overview를 먼저, 이번 작업에 필요한 default-timeout 결정을 다음으로 선택한다. PRD와 architecture 전체, Workspace source·records, output index가 연결한 artifact 본문은 기본 recovery packet에 싣지 않는다.
- [Repo-local 이식 skill](../../../../.agents/skills/apply-context-harness/SKILL.md)은 기존 canonical을 보존하면서 target 사실로 README와 overview를 구성하고, 동일한 overview-first·Markdown-only recover 경계를 검증하는 절차를 소유한다.

## 검증 결과

- `output/`에서 `python3 -m unittest discover -s . -p 'test_*.py' -v`: 제품 7개, recover 21개, verify 9개로 총 37개 통과
- `.agents/skills/apply-context-harness`에서 helper unittest: 7개 통과
- Skill validator: 통과
- Live verify: 제품 테스트 7개 통과, exit `0`. 최신 receipt는 [`verify-20260814T063043445861Z-0b38bf91d06f4edcb3d86d9ee1cb1bcd.json`](../../../../output/context/work/workspaces/001-default-timeout/records/verify-20260814T063043445861Z-0b38bf91d06f4edcb3d86d9ee1cb1bcd.json)이며 machine status도 이 receipt를 가리키는 `verified_waiting_acceptance`다.
- 후속 live recover는 packet schema `5`로 성공했다. `loaded_context_paths`에는 current 6개, Workspace output index 1개, Project overview와 default-timeout 결정 2개가 순서대로 들어갔다.

## 검증 상한과 후속 경계

- 테스트와 sample recover는 overview-first·Markdown-only 구조 경계와 선택적 로딩을 검증한다. 임의 target에서 작성한 overview의 의미 정확성·근거 충실성·이후 freshness를 자동으로 증명하지 않는다.
- Live verify는 sample 제품 코드와 고정 테스트의 일치를 증명할 뿐, 실제 네트워크 동작·외부 시스템·운영 효과·사람 acceptance를 증명하지 않는다.
- 기존 적용 target은 이 reference 변경으로 자동 migration되지 않는다. 대상별 Workspace에서 원자료와 기존 canonical을 다시 확인해 별도로 적용·검증해야 한다.
