# Harness maintenance bottleneck output

마지막 갱신: `2026-08-14`

## Workspace goal

Context+harness의 안전성과 재진입 가능성을 유지하면서, Reference Recover·Maintain·Verify의 활성 결합과 반복 검증 병목을 책임별로 분리한다.

## 현재 선택된 산출물

- [`Harness 책임과 실행 경계`](../../../../reference-project/context/work/harness/README.md): Recover·Maintain·Verify와 Harness validation의 관계
- [`Recover 계약과 구현`](../../../../reference-project/context/work/harness/recover/): explicit Workspace 선택, read-only recovery, verification snapshot freshness
- [`Maintain 계약`](../../../../reference-project/context/work/harness/maintain/): 자연스러운 의미 변화 경계, 기존 Context Owner routing, main 검토와 비소유 범위
- [`Reference Maintain adapter`](../../../../reference-project/.codex/agents/workspace-context-maintainer.toml): Maintain 계약을 읽어 수행하는 교체 가능한 Codex 실행 장치
- [`Verify 계약과 구현`](../../../../reference-project/context/work/harness/verify/): claim·canonical basis·evidence snapshot과 durable machine receipt
- [`Harness validation`](../../../../reference-project/context/work/harness/validation/): checked-in 제품 상태를 바꾸지 않는 ephemeral `recover → verify → recover` 회귀 검사

완료 거절 뒤의 구조 교정, review 수정과 증명 상한은 [`2026-08-14-06 교정·검증 기록`](../records/2026-08-14-06-reference-maintain-structural-correction-and-verification.md)에 있다. 이 Workspace는 산출물을 복제하지 않고 실제 canonical 위치만 연결한다.
