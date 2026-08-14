# Harness maintenance bottleneck state

마지막 갱신: `2026-08-14`

## 현재 문제

Maintain이 설명에만 있던 이전 구현의 완료 판단은 사용자가 거절했다. Harness 안의 Maintain 책임과 replaceable adapter까지 구조적으로 교정한 구현은 검증됐고, 사람 acceptance와 commit은 아직 결정되지 않았다.

## 현재 상태

- Harness는 책임 기준의 `recover/`, `maintain/`, `verify/`, `validation/`과 공용 fixture `testing.py`로 구성했다. Validation은 별도 task workflow 단계가 아니다.
- Maintain의 지속 의미·규칙은 Work·Workspace canonical에 남기고, Reference에는 별도 `workspace-context-maintainer` adapter를 두었다. Maintain Python CLI·schema와 outer agent 채택은 없다.
- 최초 독립 review의 P2 두 건을 수정했다. Status receipt cursor는 nested Verify receipt와 legacy direct receipt만 허용하고, POSIX Verify timeout은 보통의 동일 process-group descendant까지 종료·정리한다. Package 설명 P3도 바로잡았다.
- Worker 전체 suite는 53/53 통과했다. 독립 re-review가 두 P2 수정을 재현했고 P1·P2·P3 없이 accept했다.
- 상세 교정·검증·proof ceiling은 [`records/2026-08-14-06`](../records/2026-08-14-06-reference-maintain-structural-correction-and-verification.md)에 둔다. [`records/2026-08-14-05`](../records/2026-08-14-05-reference-recover-verify-implementation-and-verification.md)는 완료 거절 전 상태로 보존한다.

## 남은 판단

- 사용자의 결과 acceptance
- 이 변경을 commit할지와 commit 경계
- 실제 Maintain agent의 의미 선택·문서 작성·runtime 호출, detached/new-session과 non-POSIX descendant-wide 종료, concurrent Verify, 악의적 verification sandboxing의 미검증 범위를 후속 작업으로 다룰지

## 다음 행동

사용자가 교정된 구현과 proof ceiling을 검토해 acceptance와 commit 여부를 결정한다. Skill과 다른 Project 이식은 이번 acceptance와 분리한다.
