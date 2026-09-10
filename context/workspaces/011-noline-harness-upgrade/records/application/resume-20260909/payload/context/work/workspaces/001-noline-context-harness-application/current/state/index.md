# 현재 이식 상태

2026-09-09 기존 이식 HEAD `b4ed41f6`에서 최신 Reference `87d2102` 보완을 진행 중이다. Project layer·Spec·Ticket·운영 skill과 Recover·Maintain을 함께 전환하며 제품 리팩토링은 아직 선택하지 않았다. 상세 실행 결과와 보호 근거는 [적용 기록](../../records/2026-09-09-01-reference-upgrade.md)에서 확인한다.

다음 행동은 적용된 파일의 검증과 독립 검토다. Codex·Claude hook은 설치돼 있지만 actual-host trust·explicit activation·같은 generation의 runtime event receipt가 확인되지 않아 `activation_pending`이다. Preflight에서 두 host runtime 디렉터리는 없었다.

[status.json](status.json)은 마지막 Verify result·receipt cursor·시각만 소유한다. [verify.json](../../verify.json)은 claim·basis·argv·evidence를, [recover.json](../../recover.json)은 Project 선택을, [workspace.json](../../workspace.json)은 identity를 맡는다. Recover가 계산하는 freshness는 선언 snapshot의 현재 일치이며 사람용 상태의 최신성이나 undeclared input을 증명하지 않는다.

후속 리팩토링 목표·효과 평가, 실제 host skill discovery·invocation·문서 유지 흐름, 제품 기능과 사람 acceptance, commit·Workspace 완료는 아직 수행한 결과가 아니다.
