# Maintain clean-room reimplementation state

마지막 갱신: `2026-08-18`

## 현재 상태

- Active Workspace는 007이고 선택된 구현은 없다.
- 006 중단 기록은 `0952b1d`, code reset은 `b508d80`에 있다.
- `reference-project/`와 적용 skill의 복원 대상은 preimplementation commit `2649e9b`와 일치한다.
- Root hook은 빈 설정이며 Maintain agent·Workspace binding은 없다.
- `.context-harness/runtime/`의 과거 005·006 runtime 잔재 전체는 inactive이며 새 설계·canonical·migration 입력이 아니다.
- 사용자 소유 untracked `.DS_Store`는 범위 밖이다.

정확한 commit·path·검증은 [`record 02`](../records/2026-08-18-02-code-reset-baseline-and-excluded-topologies.md)가 소유한다.

## 검증 상한

- Parent exact diff, root config parse, Markdown link와 whitespace 검사는 통과했다.
- Reference 전체 suite는 같은 parent baseline에서 `53/53` 통과 1회와 동일 timeout test 1건 실패 2회가 관찰됐다. Reset 회귀가 아니라 알려진 baseline timing instability로 분리했다.
- 새 Maintain 구현과 actual host·semantic acceptance는 아직 없다.

## 다음 시작점

새 세션은 `reference-project/`를 직접 읽고, record 01의 동작과 record 02의 금지선만 대조해 첫 접근을 스스로 정한다. 과거 구현 diff를 출발 architecture로 사용하지 않는다.
