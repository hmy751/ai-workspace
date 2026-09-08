# Project context 파일명 정리와 적용 커밋

## 후속 요청

> 그래 커밋하기전에 03-project... 여기 번호는 바꿔야 하지 않을까? 수정하고 커밋

앞선 적용 결과 미커밋 지시는 이 후속 요청으로 해제됐다. 사용자는 이어 memory-harness-research가 이번 상황을 인지하도록 맥락·근거를 종합한 문서 전달 방식도 물었다.

## 변경

`03-project-context.md`의 번호는 기존 goal·constraints와 같은 층에 있던 순서였다. 두 파일이 Spec으로 대체된 뒤에는 순서의 의미가 없어 `current/memory/project-context.md`로 바꿨다. 내용과 Project context 선택 책임은 유지한다.

Recover의 필수 경로, 공통 테스트 fixture, Recover 기대 경로, 현재 안내·canonical·010의 현재 설명을 함께 맞췄다. 009 기록에서 실제 파일로 가는 링크 한 곳은 목적지만 새 경로로 연결했다. 과거 상태를 설명하는 기록의 파일명·발화·당시 실행 결과는 소급 변경하지 않았다.

커밋 범위는 직전 Reference Spec·Ticket 적용과 관련 010 문서, 이번 파일명 정리·검증 기록 및 깨진 링크 복구다. 무관한 `.DS_Store`, 외부 연구 저장소, root 자동 Maintain 설정은 포함하지 않는다. 구체적인 커밋 식별자는 성공 후 현재 state와 후속 전달 문서에서 연결한다.

## 검증

파일명 정리 후 Reference root에서 `python3 -m unittest discover -s . -p 'test_*.py' -q`를 실행했다. 전체 124개 중 123개 통과, 기존 Verify의 `test_timeout_covers_descendant_after_group_leader_exits`가 같은 descendant PID 파일 확인에서 실패했다. 변경 전 커밋에서도 재현한 근거는 [직전 적용 기록](2026-09-08-12-reference-spec-ticket-implementation.md)에 있다. 해당 코드·테스트는 수정하지 않았다.

실제 샘플의 active/default Recover·explicit Recover와 Maintain bootstrap을 읽기 전용으로 확인해 모두 새 Project context 경로·Spec 다섯 파일·Ticket 색인을 포함함을 확인했다. `project-context.md` 본문은 변경 전 파일과 바이트 단위로 같았다. 변경·추가 Markdown의 로컬 링크 존재와 `git diff --check`도 확인했다.

이 기록은 이름·참조·구조 적용의 확인이며 자동 Maintain의 실제 의미 판단이나 독립 Ticket 실행 운영을 입증하지 않는다.
