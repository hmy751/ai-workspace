# Maintain clean-room reimplementation current

마지막 갱신: `2026-08-18`

이 폴더는 새 구현이 이어받아야 할 현재 유효 기준과 빠르게 바뀌는 실행 상태만 소유한다. Workspace 005·006의 상세 과정은 이곳에 복제하지 않고 records의 선별 근거에서 연결한다.

## 재진입 순서

1. [`memory.md`](memory.md)에서 사용자 장면, 책임 배치, canonical과 금지선을 읽는다.
2. [`state.md`](state.md)에서 reset commit, 현재 파일 상태, 검증 상한과 다음 원자 행동을 확인한다.
3. [`../output/index.md`](../output/index.md)에서 선택된 구현이 아직 없는지 확인한다.
4. 근거가 필요할 때만 [`../records/`](../records/)의 source·reset record와 handoff를 연다.

구현이 시작된 뒤에도 current에는 선택된 기준과 현재 커서만 유지한다. 후보 비교, 탈락 이유, 실패와 검증 상세는 records가 소유한다.
