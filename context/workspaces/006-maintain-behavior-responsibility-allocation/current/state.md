# Maintain behavior responsibility allocation state

마지막 갱신: `2026-08-18`

## 현재 상태

Workspace 006을 새로 만들고 active Workspace와 root Maintain binding을 이 Workspace로 전환했다. 글로벌 responsibility-allocation reference와 Workspace 005의 완료된 Reference Maintain 구현을 출발점으로 선택했지만, 아직 어떤 내부 동작이나 파일을 먼저 개선할지 결정하지 않았다.

## 확인된 시작점

- Workspace 005의 Reference-first Maintain 구현과 로컬 검증은 commit `9553d0a`에 보존돼 있다.
- 개선 대상의 canonical은 `reference-project/context/work/harness/maintain/`이며 root에 semantic code나 prompt를 복제하지 않는다.
- 새 작업은 기능 추가가 아니라 현재 동작 안의 모델 판단, 지침·schema·code guard, 사람 권한과 test 증거의 배치·표현 개선을 우선한다.
- 글로벌 reference는 판단 렌즈이며 수정 대상이 아니다.
- 아직 문제 목록, 설계안, 수정 파일, acceptance나 완료 기준을 확정하지 않았다.

## 생성·연결 검증

- Root `.codex/context-maintain.json`은 `006-maintain-behavior-responsibility-allocation`을 선택한다.
- Reference Maintain config loader에서 새 Workspace가 `workspace_bound: true`로 판정됐다.
- Maintain status 진입은 Workspace 006 identity와 session `0`인 새 runtime 상태를 반환했다.
- Root Maintain JSON·TOML 설정 parse와 `git diff --check`가 통과했다.
- Reference Maintain 코드나 글로벌 reference는 이 Workspace 생성 과정에서 수정하지 않았다.

## 다음 행동

다음 대화에서 개선할 실제 Maintain 동작 하나를 선택하고, 그 동작의 시작 조건·입력·결과·부작용과 반드시 지킬 약속을 먼저 적는다. 그다음 현재 구현에서 해석·선택, 보장·거부, 권한·승인, 실행·기록이 각각 어디에 배치됐는지 대조해 첫 개선 범위와 검증 방법을 정한다.

세부 논의 전에는 Reference 코드·지침을 바꾸거나 새로운 runtime 장치를 추가하지 않는다.
