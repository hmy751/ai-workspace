# 재개 안내와 직접 검사로 전환

2026-11-04. Reference의 기존 Recover·Verify 실행기를 내리고 Work 지침과 Workspace `recover.md`로 재개를 안내하도록 바꿨다. 이 작업은 기록·재개 체계의 전환이며 default-timeout 제품 요구나 코드 변경은 아니다.

## 선택 이유와 대체 관계

사용자는 Harness를 없앨 때 생기는 빈틈을 확인하고, 다른 세션에서도 선택의 이유와 뉘앙스를 이어받되 Workspace 전체를 매번 읽지 않는 기준을 원했다. “recover.json같은 파일은 두는건 좋은것 같은데”라고 했지만 JSON 형식을 고정하지 않았고, prototype에서 `recover.md`·공통 Work 지침·기존 current의 역할을 나누어 확인한 뒤 Reference 적용을 요청했다.

| 이전 역할 | 현재 위치와 범위 |
| --- | --- |
| index·workspace JSON의 기본 선택·정체성 | collection README의 기본 링크와 Workspace README |
| Recover의 고정 packet·Project 선택 | `recover.md`의 기본·조건부 자료와 이유, 기존 Project 선택 문서. 필요한 추가 확인은 읽는 주체가 판단한다. |
| Verify 실행·receipt·machine status | 직접 제품 검사, 해당 Ticket·records의 실행 근거와 state의 현재 의미 |
| 재개 안내 갱신 | 생성 담당자가 초기 구성, record-work가 방향·단계·자료 변화 때 조건부 갱신 |

제품 테스트·Git/해시·출력 보존으로 수행할 수 있는 부분과 이전 기계 보장은 다르다. 자동 입력 snapshot·제한된 출력 묶음·receipt/status 갱신·freshness 판정과 POSIX process-group timeout은 제거된 구현의 기능이다. 직접 도구가 같은 보장을 제공한다고 주장하지 않는다. 대기 시간과 강제 종료 시간을 구별하고, 현재 대상·조건·결과·한계를 판단에 필요한 만큼 남긴다.

## 보존과 직접 확인

변경 전 제품·Harness 검사 95개가 통과했다. 이후 runtime 61개·기계 계약 5개·전용 package 표식 2개를 원래 bytes와 대조해 [보존본](../../../../../../context/workspaces/014-ai-development-workflow-design/records/archives/2026-11-04-recover-verify/README.md)에 남기고 활성 경로에서 제거했다. 옛 경로를 참조하는 날짜별 기록은 수정하지 않았다. 기존 Verify receipt 12개는 원래 Work의 당시 근거로 그대로 남는다.

변경 뒤 Reference root에서 `python3 -B -m unittest tests.test_config_loader -v`를 실행해 제품 검사 7개가 통과했다. 제품 파일은 변경하지 않았다. 검사 범위는 누락 기본값·명시값 유지·잘못된 입력 거부·불변 반환이며 네트워크 실행·사용자 수락·Work 전체 완료를 뜻하지 않는다. 이번 실행은 새로운 Verify receipt나 machine status를 생성하지 않는다.

## 이후 읽기

현재 의미·다음 행동은 [state](../current/state/index.md), 읽을 대상·조건은 [recover.md](../recover.md)가 소유한다. 과거의 마지막 성공 receipt와 현재 직접 검사 결과를 구별한다. 원문·장기 사용·host 통합까지 이 기록만으로 확인했다고 주장하지 않는다. Runtime 복원은 위 archive를 별도 임시 위치에서 사용하며 현재 재개 절차에 다시 연결하지 않는다.
