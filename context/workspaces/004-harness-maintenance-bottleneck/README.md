# Harness maintenance bottleneck Workspace

Context+harness의 작은 계약 변경이 기준 Project, 이식 skill, 여러 Workspace current·records, 검증과 review까지 넓게 전파되는 유지보수 병목을 분석하고 줄이는 작업 공간이다.

상태는 **active**다. Recover·verify의 증거 경계를 약화시키지 않으면서, 같은 규칙의 중복 소유와 불필요한 순차 작업·반복 검증을 줄이는 것이 목표다.

## 읽는 순서

1. [`current/memory.md`](current/memory.md): 목표, 유지할 안전 기준, 범위
2. [`current/state.md`](current/state.md): 현재 확인된 병목과 다음 분석 행동
3. [`output/index.md`](output/index.md): 이 Workspace goal의 선택된 개선 산출물
4. [`records/`](records/): 관찰, 후보, 결정, 실험과 검증 기록

이 Workspace는 이전 구현·적용 Workspace를 합치거나 다시 쓰지 않는다. 필요한 과거 결론은 링크로 선택하며, 개선안이 확정되기 전에는 기존 Harness 계약을 성급하게 제거하지 않는다.
