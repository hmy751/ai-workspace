# Work context 운영 규칙

Work의 의미와 관계는 [Work 입구](README.md), 지속 문서의 역할은 [Workspace collection](workspaces/README.md), 실행 장치는 [Harness](harness/README.md)가 소유한다. Project root에서 명령을 실행한다.

## 재진입·기록·검증의 책임을 구별한다

- **Recover:** `python3 -m context.work.harness recover [workspace_id]`로 필요한 현재 맥락을 읽기 전용으로 복구한다. 목적·입출력은 [Recover](harness/recover/README.md)를 따른다.
- **작업 기록:** [record-work](../../.agents/skills/record-work/SKILL.md)의 담당자가 원문·관련 결과로 사람용 Work 문서를 직접 갱신한다. 호출·같은 서브 재사용·입력 범위·반환은 스킬이, 내용·보존은 Work가 소유한다. 매 응답 자동 실행·session binding·guarded Maintain CLI는 사용하지 않는다.
- **Verify:** `python3 -m context.work.harness verify [workspace_id]`는 상태 전환·인계에 필요한 제품 증거를 receipt와 machine status로 남긴다. [Verify 계약](harness/verify/README.md)은 의미 갱신·사람 수락을 대신하지 않는다.
- **Harness validation:** [임시 fixture 검사](harness/validation/README.md)는 Recover·Verify 구현의 회귀를 확인한다. 실제 active Workspace의 receipt·status를 자기 검사로 바꾸지 않는다.

사람용 문서를 쓰거나 고칠 때 [문서 작성](workspaces/DOCUMENT-WRITING.md)과 [Spec·Ticket 갱신 기준](workspaces/spec-and-tickets/MAINTENANCE.md)을 적용한다. Main은 작업 판단·위임·전체 결과를 조율하고 기록 담당자와 같은 문서를 중복 수정하지 않는다. 다른 담당자의 결과·실제 근거가 원문에 없으면 정확한 접근점을 연결한다. 필요한 문서를 다음 수행에 넘기기 전에는 실제 반영을 확인한다.

기록 담당자는 지정 Work의 허용된 사람용 문서를 수정한다. Raw source·과거 record·제품 코드·검사·machine 계약·status·receipt와 다른 Workspace를 기록 과업으로 변경하지 않는다. Project·Personal 반영은 development·context-update·improvement-loop의 해당 책임으로 연결한다. 스킬이 불가능하면 Main이나 지정 담당자가 같은 기록 기준을 적용하고 실제 수행 주체·원문 접근의 한계를 밝힌다.

## 생성·전환을 기록과 구별한다

새 독립 Workspace는 [create-context-workspace](../../.agents/skills/create-context-workspace/SKILL.md)와 [생성·전환 계약](workspaces/CREATE-AND-TRANSITION.md)을 따른다. 기존 작업의 기록이나 재개를 위해 새 Work를 만들지 않는다. 전환 시 원래 Work의 진행 중 기록과 미반영 사항을 확인하고 새 대상과 섞지 않는다. 기본 index 선택과 이번 대화의 배정은 별개다.

## 변경은 해당 책임 가까이에서 수행한다

- Recover·Verify의 전용 규칙·구현·검증은 각 책임 디렉터리에서 관리한다. 공통 식별·안전한 경로·status 인계는 [workspace](harness/workspace/README.md), 최소 test fixture는 `harness/testing.py`가 맡는다.
- 기록의 실행 계약·상세·형성 자료는 record-work에, 지속 문서의 의미·작성·보존 기준은 workspaces에 둔다. 전역 hook·agent 설정으로 이 Reference의 기록 방식을 구현하지 않는다.
- Project의 실제 공통 내용은 [Project](../project/README.md), 기준과 권한은 [Project 관리](../project/MAINTENANCE.md)가 소유한다. 제품 코드·검사는 Project root에 둔다. 구현 결과만으로 새 제품 약속이나 개인 기준을 채택하지 않는다.
- Project의 경로·책임을 크게 바꾸면 [live consumer 확인](workspaces/README.md#project-context-변경과-live-consumer)을 따른다. 실제 작업 중인 Workspace와 active/default 소비자의 읽기 경로를 맞추며 역사 Workspace는 자동 동기화하지 않는다.
- 제품·Project evidence와 검증 cwd는 Project root 기준, Workspace index·current·source·output·records는 Work root 기준이다. `recover.json`·`verify.json`·machine status의 계약은 각 실행 책임이 소유한다.

## 실제 확인과 완료 범위를 구별한다

`python3 -m unittest discover -s . -p 'test_*.py' -v`로 제품·Harness 검사를 실행한다. 연결 검사는 `context.work.harness.validation.tests.test_ephemeral_workspace_state_preservation`의 임시 순환을 사용한다. 반복 개발 확인은 direct test로, 필요한 상태 전환의 증거만 Verify로 남긴다.

파일·링크·설정 검사와 unit test는 기록 담당자의 원문 판단·실제 재사용·다음 재개의 성공을 증명하지 않는다. 실제 host 수행과 사용 효과는 따로 확인한다. 검증 통과·문서 반영·사람 수락·Work 완료를 구별한다.
