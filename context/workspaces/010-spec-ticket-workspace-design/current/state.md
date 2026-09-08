# Spec·Ticket 설계 state

마지막 갱신: 2026-09-08

## 현재 단계

**설계 기록은 `4fe8694`로 커밋했고, 합의한 Spec·Ticket 구조를 Reference에 적용했다.** 후속 사용자가 Project context 파일 번호 정리와 커밋을 요청했다. `03-project-context.md`를 `project-context.md`로 바꾸고 실제 읽기 경로·테스트를 맞췄으며, 적용 결과와 검증 기록을 함께 커밋하는 단계다.

유지할 합의는 [memory](memory.md), 실제 결과와 canonical 위치는 [output](../output/index.md), 구체적인 변경·판단·검증은 [Reference 적용 기록](../records/2026-09-08-12-reference-spec-ticket-implementation.md)에 있다.

## 적용한 동작

- Spec 다섯 파일이 샘플 Workspace의 goal·작업별 constraints를 대체했다. `project-context.md`는 유지한다. Ticket은 memory의 별도 폴더에 정의·진행을 함께 남기는 구조다.
- Recover는 Spec 전체와 Ticket 색인을 기본으로 읽고, 작업 주체가 필요한 Ticket 본문을 선택한다. 아직 Ticket이 없는 샘플에 과거 실행 Ticket을 소급 생성하지 않았다.
- Maintain은 같은 역할로 Spec·Ticket을 생성·갱신한다. 새 Ticket은 Ticket 색인에, 새 Spec·기타 memory 문서는 memory 색인에 연결한다. 기존 Ticket의 상태 갱신만으로 색인·state를 함께 바꾸지는 않는다.
- Workspace의 Spec·Ticket canonical을 Maintain의 규칙 입력에도 연결했다. Main은 계속 작업을 조율하며 다른 실행자 결과의 자동 수집이나 새 조율 runtime을 만들지 않았다.
- 생성·전환 canonical을 새 구성에 맞췄다. 생성·이식 skill은 live canonical을 읽는 기존 경로를 유지한다.

## 검증 결과와 한계

- Recover·Maintain operation 관련 51개 테스트 통과. Spec 읽기, Ticket 생성·진행 갱신, 색인 연결과 stale SHA·symlink 거부를 포함한다.
- 전체 제품·Harness 회귀는 124개 중 123개 통과, Verify의 `test_timeout_covers_descendant_after_group_leader_exits` 1개 실패. 재실행에서도 같았고, 변경 전 `4fe8694`를 임시 디렉터리에 추출한 119개 검사에서도 같은 테스트가 같은 지점에서 실패했다. 해당 테스트 단독 실행은 통과했다. 기존 전체 실행 환경에서의 실패로 구별하며 전체 통과로 기록하지 않는다.
- 실제 샘플의 active/default Recover, explicit Recover, Maintain bootstrap은 성공했다. Spec 다섯 파일·Project 선택·Ticket 색인이 들어오는 것을 확인했다. 기존 receipt의 `stale`과 machine status는 그대로 보존했다.
- 수정 문서의 로컬 링크와 diff 형식을 확인했다. 실제 자동 Maintain·새 실행자 위임 장면의 semantic 평가나 host acceptance는 수행하지 않았다.

## 다음에 이어갈 일

구현과 파일 구성을 검토하고 실제 작업에서 Ticket 작성·실행·결과 반영을 사용해 본다. 특히 Main이 받은 결과가 Maintain 입력과 실제 문서까지 이어지는지, 새 실행자에게 필요한 본문이 준비되는지를 확인한다. 개별 실행자의 입력·쓰기 범위는 작업에 맞게 열어 둔다.

전체 회귀의 기존 Verify timeout 실패는 별도 후속 조사로 남아 있다. 파일명 정리 뒤 전체 124개 검사를 다시 실행해도 같은 한 건만 실패했다. 이번 Spec·Ticket 적용을 이유로 Verify 코드·시간 기준을 바꾸거나 실패 검사를 건너뛰지 않았다. 파일명 정리와 커밋 경계는 [후속 기록](../records/2026-09-08-13-project-context-filename-and-commit.md)에 남긴다. 이어 memory-harness-research가 배경·선택 이유·구현·검증 범위를 함께 인지할 전달 문서를 구성한다.
