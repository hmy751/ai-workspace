# 선택한 산출물

마지막 갱신: `2026-09-16`

현재 선택된 결과는 비용 개선 설계와, 그에 앞선 Reference Maintain 구조 리팩터링이다.

- [`record 01`](../records/2026-09-15-01-scope-correction-and-runtime-evidence.md): 사용자 정정으로 다시 잡은 문제 범위와 실제 token·compact 근거
- [`record 02`](../records/2026-09-15-02-improvement-design-and-validation-plan.md): semantic checkpoint와 bounded rollover 중심의 개선 구조, 두 대상 적용 순서와 acceptance
- [`리팩터링 기록`](../records/2026-09-16-01-maintain-refactoring.md): 책임·테스트·도구 연결 분리와 실제 검증 결과
- [`구현 안내`](../../../../reference-project/context/work/harness/maintain/STRUCTURE.md): 코드·테스트 진입점, 호환 경로와 Codex·Claude 지원 범위

실제 산출물은 복제하지 않고 다음 canonical에서 유지한다.

- 공통 Source: [`reference-project/context/work/harness/maintain/`](../../../../reference-project/context/work/harness/maintain/)
- Noline Target: Noline 저장소의 `context/work/harness/maintain/`
- Reference 검증: Source의 `tests/`와 이 Workspace의 필요한 replay receipt
- Target 검증: Noline이 소유하는 적용 Workspace·tests·host evidence

Reference 구조 변경과 자동 테스트 결과는 있다. 비용 replay receipt, 실제 host acceptance, Noline 적용과 commit은 아직 없다.
