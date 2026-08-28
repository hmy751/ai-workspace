# Workspace 생성·전환 계약 검증과 독립 리뷰

날짜: `2026-08-28`

## 정적 확인

- 수정·추가한 Markdown `14`개의 relative local link를 확인했고 누락은 `0`개였다.
- `git diff --check`가 통과했다.
- Harness code, machine schema와 hook은 변경하지 않았다.

## 회귀 테스트

Reference root에서 `python3 -m unittest discover -s . -p 'test_*.py' -v`를 실행했다. 최종 실행은 `97`개 전체가 통과했다.

작업 중 전체 suite의 `test_timeout_covers_descendant_after_group_leader_exits`가 descendant PID 파일을 timeout 전에 만들지 못해 간헐적으로 실패했다. 같은 test 단독 재실행과 이어진 전체 `97`개 실행은 통과했다. 이 증상은 이번 문서 변경 전 reset baseline부터 분리된 timing instability이며, 근거는 [Workspace 007의 baseline record](../../007-maintain-clean-room-reimplementation/records/2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md)에 있다. 따라서 실패를 새 문서 계약의 회귀로 바꾸거나 이번 범위에서 Verify 구현을 수정하지 않았다.

## 독립 리뷰

001에서 002를 만드는 실제 장면을 기준으로 한 시나리오 검토는 다음을 확인하고 지적 없이 통과했다.

- 생성자가 새 goal의 판단을 바꾸는 원문 의미를 successor current에 직접 남길 수 있다.
- 새 002 세션은 predecessor 전체를 Recover하지 않고도 필요한 원문의 역할과 읽을 시점을 알 수 있다.
- 전체 상속, 링크-only 인계, 자동 동기화·역전파, recursive recovery와 사용 횟수 기반 Project context 승격을 요구하지 않는다.

별도 Owner·권한 검토는 처음에 네 가지 보정을 요구했다.

- Recover가 `source/index.md`를 읽지 않으므로 필수 source의 exact canonical 경로나 직접 링크도 current에 있어야 한다.
- 의도적으로 이어받지 않은 내용은 전체 목록이 아니라, 계속 적용된다고 오해하면 현재 판단이 달라지는 bounded 범주만 current에 드러내야 한다.
- Workspace 활성화는 같은 Main session의 binding 변경이 아니라 이전 session 종료, binding 정렬, 새 Main session의 explicit grounding 순서여야 한다.
- Project context 반영은 여러 Workspace 사용 여부가 아니라 Project 전체 적용 근거와 기존 Owner 판단에 맡기고, Work AGENTS는 상세 의미를 복제하지 않는 router여야 한다.

보정 뒤 같은 reviewer가 네 지적이 모두 해소됐고 새 P1·P2·P3가 없다고 판정했다.

## 검증 상한

이 검증은 문서 링크, 기존 실행 경계의 회귀와 독립적인 계약 검토를 확인한다. 생성 실행기, 자동 의미 선별이나 의미 충분성 판정, actual host의 Workspace 활성화·binding 전환, 실제 다른 Project 적용과 사람 acceptance는 구현하거나 증명하지 않는다.
