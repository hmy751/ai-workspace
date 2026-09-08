# Spec·Ticket 설계 state

마지막 갱신: 2026-09-08

## 현재 단계

**설계 합의와 기록 정리를 마쳤으며 Reference의 실제 적용 전이다.** Spec 구성·memory 배치·기존 goal/constraints 대체, Ticket 정의·진행 통합은 정했다. 기존처럼 Maintain은 대화와 결과를 이해해 기록·갱신하고 Main이 작업을 조율한다. 별도 역할 체계를 새로 만드는 것이 아니다.

유지할 합의는 [memory](memory.md), 채택한 구성 설명과 예시는 [output](../output/index.md)에 있다. 전체 논의가 현재 선택으로 이어진 과정과 열린 부분은 [설계 정리 기록](../records/2026-09-08-11-design-status-and-remaining-work.md)에 모았다. 과거 리뷰의 제거 선호나 분리 제안을 현재 결정으로 다시 읽지 않는다.

## 다음 작업

다음 논의에서는 합의한 내용을 반영한 전체 폴더 구조와 기본 읽기 순서를 정리한다. 이번 사용자 요청은 기록 정리이며 실제 구현을 시작하라는 지시가 아니다.

1. **최종 파일 구조:** memory/spec의 다섯 Markdown 파일과 tickets, 유지할 project-context·state를 연결하고 기존 goal·constraints의 대체를 구체화한다. 폴더 위치와 구성은 이미 정했으며 파일명과 전체 진입 구조가 남아 있다.
2. **Recover:** Spec 전체를 기본 진입에서 읽도록 반영한다. Workspace 진입 시 Ticket 목록과 필요한 본문을 읽을지, 본문 전체를 함께 읽을지는 아직 정하지 않았다. 개별 Ticket 실행자의 고정 입력을 정하는 문제와 구별한다.
3. **Maintain:** 기존 역할을 유지하면서 Spec·Ticket 하위 파일을 읽고 생성·갱신할 수 있게 한다. 결과 전달과 사용할 본문의 준비 시점은 실제 흐름에서 대조한다. 작업 조율을 Maintain에 추가하지 않는다.
4. **생성·이식·기존 참조·검증:** 새 Workspace 생성과 이식 안내, 기존 goal·constraints 경로를 참조하는 부분을 맞추고 관련 동작을 확인한다. Verify 등도 실제 영향 범위를 확인해 필요한 부분을 반영한다.

Ticket 구성과 개별 실행자의 정확한 읽기·쓰기 범위는 열어 둔다. 모든 결과를 특정 Main으로 회수하거나 완료 때 Ticket을 이동하는 절차를 먼저 고정하지 않는다. 기록·읽기 경로를 구현하기 위해 필요한 선택과, 상황에 맞게 열어 둔 실행 방식을 구별한다.

## 확인한 동작과 한계

현재 Recover는 memory 바로 아래 Markdown을 읽으며 Spec 하위 폴더를 자동으로 읽지 않는다. Maintain의 현재 쓰기 허용 경로도 새 spec·tickets 폴더를 아직 포함하지 않는다. [진입 조사](../records/2026-09-08-08-workspace-ticket-execution-direction.md)와 [작성 책임 리뷰](../records/2026-09-08-10-spec-ticket-authorship-independent-review.md)에 근거가 있다.

Maintain은 사용자 발화와 Main의 마지막 사용자 대상 응답을 받고, 필요한 경우 해당 입력이 명시한 관련 로컬 자료를 제한적으로 읽는다. Main이 subagent 결과를 받은 것만으로 그 의미가 Maintain에도 전달되는 것은 아니다. 응답 뒤 비동기 반영의 접수와 실제 문서 준비도 구별한다. 이를 해결하는 별도 조율 runtime을 채택한 것은 아니다.

## 적용과 검증 범위

이번 작업은 010의 기록·진입 문서·current·output 안내를 정리한 것이다. Reference·Recover·Maintain·Verify·schema·hook·이식 절차는 변경하지 않았다. 채택한 Spec 구성과 예시 본문도 유지했다.

문서 링크와 Git diff 형식을 확인했다. 제품·runtime 테스트는 실행하지 않았다. 초기 Reference revision 5e45310의 임시 fixture·회귀 검사는 당시 영향 조사 근거이며 새 설계의 운영 효과를 입증하지 않는다. 예시의 API·30초·평가 20개도 실제 환경에서 검증한 값이 아니다. 당시 Spec 구성 저장 후 확인은 [구성요소 합의 기록](../records/2026-09-08-01-spec-components-decision.md)에 남아 있다.

현재 기록 정리는 아직 커밋하지 않았다.
