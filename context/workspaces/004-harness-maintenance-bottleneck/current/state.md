# Harness maintenance bottleneck state

마지막 갱신: `2026-08-14`

## 현재 문제

Maintain이 설명에만 있던 이전 구현의 완료 판단은 사용자가 거절했다. Harness 안의 Maintain 책임과 replaceable adapter까지 구조적으로 교정했고, 사용자가 agent 정의를 Maintain 관심사 아래에 두는 추가 구조를 선택했다. 최종 결과의 사람 acceptance는 아직 열려 있다.

## 현재 상태

- Harness는 책임 기준의 `recover/`, `maintain/`, `verify/`, `validation/`과 공용 fixture `testing.py`로 구성했다. Validation은 별도 task workflow 단계가 아니다.
- Maintain의 지속 의미·규칙은 Work·Workspace canonical에 남기고, 실제 `workspace-context-maintainer` 정의는 `context/work/harness/maintain/`에 계약과 함께 두었다. Root `.codex/config.toml`은 이 하위 정의를 등록하고, 상세 운영 규칙은 `context/work/AGENTS.md`가 소유한다. Maintain Python CLI·schema와 outer agent 채택은 없다.
- 최초 독립 review의 P2 두 건을 수정했다. Status receipt cursor는 nested Verify receipt와 legacy direct receipt만 허용하고, POSIX Verify timeout은 보통의 동일 process-group descendant까지 종료·정리한다. Package 설명 P3도 바로잡았다.
- 책임 구조 교정 당시 worker 전체 suite는 53/53 통과했고 독립 re-review가 두 P2 수정을 재현해 P1·P2·P3 없이 accept했다. Agent 정의 재배치 뒤에도 최종 전체 suite 53/53, 두 대상 범위의 로컬 링크 245개 누락 0, TOML parse와 `config_file` 경로 해석, staged·unstaged whitespace 검사가 통과했다. 이 정적 등록 확인은 새 Codex session의 실제 role 발견·호출까지 증명하지 않는다.
- 상세 교정·검증·proof ceiling은 [`records/2026-08-14-06`](../records/2026-08-14-06-reference-maintain-structural-correction-and-verification.md)에 둔다. [`records/2026-08-14-05`](../records/2026-08-14-05-reference-recover-verify-implementation-and-verification.md)는 완료 거절 전 상태로 보존한다.
- 이후 agent 정의 배치와 root 등록·하위 운영 지침 분리는 [`records/2026-08-14-07`](../records/2026-08-14-07-reference-maintain-agent-colocation-and-registration.md)에 둔다.

## 남은 판단

- 사용자의 결과 acceptance
- 실제 Maintain agent의 의미 선택·문서 작성·runtime 호출과 새 `config_file` 등록의 발견, detached/new-session과 non-POSIX descendant-wide 종료, concurrent Verify, 악의적 verification sandboxing의 미검증 범위를 후속 작업으로 다룰지

## 다음 행동

Main은 승인된 agent 배치 변경을 별도 commit으로 보존하고 결과와 proof ceiling을 보고한다. 사용자는 최종 결과를 검토한다. Skill과 다른 Project 이식은 이번 acceptance와 분리한다.
