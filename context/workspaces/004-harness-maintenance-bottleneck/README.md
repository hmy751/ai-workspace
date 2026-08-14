# Harness maintenance bottleneck Workspace

Context+harness의 작은 계약 변경이 기준 Project, 이식 skill, 여러 Workspace current·records, 검증과 review까지 넓게 전파된 사례에서 시작한 유지보수 병목 분석 공간이다.

상태는 **active**다. 이전 Recover·Verify 구현은 Maintain이 설명에만 있고 Harness 안에 구조적으로 드러나지 않아 사용자가 완료를 거절했다. 교정된 `reference-project`는 Recover·Maintain·Verify·validation 책임 경계와 replaceable Maintain adapter를 구현·검증했고, 사람 acceptance와 commit을 기다린다. Skill·다른 Project 이식·Context 구조 변경은 이번 범위 밖이다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 유지할 안전 기준, 범위
2. [`current/state.md`](current/state.md): 현재 확인된 병목과 다음 분석 행동
3. [`output/index.md`](output/index.md): 이 Workspace goal의 선택된 개선 산출물
4. [`records/`](records/): 관찰, 후보, 결정, 실험과 검증 기록

이 Workspace는 이전 구현·적용 Workspace를 합치거나 historical record를 현재 계약에 맞춰 다시 쓰지 않는다. 교정된 구조와 최종 검증은 [`records/2026-08-14-06`](records/2026-08-14-06-reference-maintain-structural-correction-and-verification.md), 그전 완료 판단은 당시 상태 그대로 보존한 [`records/2026-08-14-05`](records/2026-08-14-05-reference-recover-verify-implementation-and-verification.md)에서 확인한다.
