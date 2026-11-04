# 보존된 기계 증거

이 폴더는 Default timeout Workspace에서 기계가 생성한 과거 증거를 보존한다. 실행기가 아카이빙되어도 당시 증거의 의미와 수명은 이 Work에 남는다.

- [verify](verify/): 이전 고정 검증의 claim·선언한 입력 hash·argv·결과·출력·실행 제한. 서로 다른 당시 schema를 그대로 보존한다.

과거 receipt는 현재 성공·freshness·수락을 자동 증명하지 않는다. 재사용하려면 실제 현재 입력·기준·실행 조건과 대조한다. 현재 확인과 다음 판단은 [state](../../current/state/index.md), 변경 이유와 옛 status의 복원 위치는 [전환 기록](../2026-11-04-recovery-guide-transition.md)에서 찾는다. 새 Work에 Verify 폴더·receipt·status를 미리 만들도록 요구하지 않는다.
