# Harness maintenance bottleneck memory

마지막 갱신: `2026-08-14`

## 목표

Context+harness의 안전성과 재진입 가능성은 유지하면서, 작은 변경이 과도한 문서 갱신·Workspace 정합화·검증·review로 번지는 유지보수 비용을 줄인다.

## 유지할 기준

- Harness의 보호 대상은 현재 명령·schema·경로 자체가 아니라, 필요한 맥락의 선택적 복구와 실제 검증 결과가 지속 상태·다음 행동으로 이어져 다음 작업자가 낡은 상태나 근거 없는 완료에서 시작하지 않게 하는 것이다.
- Harness의 목적과 구현 방법을 구분한다. 책임, 활성 시점, 실행 주체와 CLI·schema·경로 같은 수단을 자동으로 동일시하지 않는다.
- 재진입의 read-only Recover, 의미 변화의 Maintain, durable product Verify, ephemeral Harness validation과 사람 acceptance를 서로 다른 책임으로 유지한다. Validation은 네 번째 작업 workflow 단계가 아니다.
- Reference의 Maintain 책임은 자연스러운 작업 경계의 agent/main workflow이며, 지속되는 의미와 규칙은 Work·Workspace canonical이 소유한다. Maintain 계약과 교체 가능한 agent 정의는 `context/work/harness/maintain/`에 함께 두고, Project root `.codex/config.toml`은 하위 정의의 발견 경로만 등록한다. 상세 Work·Harness 운영 규칙은 `context/work/AGENTS.md`가 소유하고 root `AGENTS.md`는 최소 라우터로 유지한다.
- Maintain을 위한 Python CLI·schema는 두지 않는다. Reference의 `workspace-context-maintainer` adapter와 outer repo-local `context_maintainer`는 서로 다른 대상과 권위를 가진다.
- Harness 구현은 책임을 기준으로 `recover/`, `maintain/`, `verify/`, `validation/`을 나누고 공용 test fixture만 `testing.py`에 둔다.
- 실제 실행 계약의 Owner와 이식 절차, 적용 이력의 Owner를 구분한다.
- 확인하지 않은 의미 정확성, 외부 동작, 사람 acceptance를 구조 테스트만으로 증명했다고 말하지 않는다.
- 사용자 변경, 기존 canonical, append-only evidence를 속도 개선을 이유로 덮어쓰거나 삭제하지 않는다.
- Current는 다음 행동에 필요한 현재 정보만 유지하고, 상세 과정은 records에 남긴다.
- Historical record는 당시 사실로 보존하며 현재 계약을 다시 설명하는 정본으로 사용하지 않는다.
- 검증 강도는 변경 위험에 비례시킨다. 반복 개발 확인과 상태 전환용 durable verify를 구분한다.
- Context 이동·링크·설명 정리처럼 실행 의미를 바꾸지 않는 작업은 필요한 경로·링크·diff만 확인한다. 모든 이동에 full runtime test, durable verify, 독립 review를 일괄 적용하지 않는다.
- Schema, 실행 코드, evidence 범위, path 방어, 사용자 파일 보존처럼 실패 영향이 큰 변경만 검증 범위를 단계적으로 넓힌다. Main이 변경 성격을 판단해 가장 작은 충분한 확인부터 시작한다.

## 현재 범위

- 사용자 완료 거절 뒤 구조를 교정해 구현·검증한 `reference-project` Recover·Maintain·Verify·validation 책임 재배치
- Work·Workspace canonical과 replaceable Maintain adapter의 경계
- 교정된 구현의 현재 proof ceiling
- 사람 acceptance와 commit 전 최종 결과 확인

## 범위 밖

- Recover·verify 제거
- Receipt 증거 또는 path 안전성 약화
- 사람 acceptance 자동화
- 현재 Payment target 재적용
- `apply-context-harness` skill과 다른 Project 이식·전파 개선
- Outer repo-local `context_maintainer` 자체 개선 또는 Reference 구현으로의 채택
- Project common context와 Workspace `current/source/output/records` 책임 구조 자체의 재설계
- Workspace 전체 lifecycle을 한 번에 새로 설계하는 작업

## 접근점

- Recover·verify 목적과 활성 시점 가설: [`records/2026-08-14-02`](../records/2026-08-14-02-recover-verify-purpose-and-activation-hypotheses.md)
- Harness 책임·주체·구현 층위 종합: [`records/2026-08-14-03`](../records/2026-08-14-03-harness-responsibilities-actors-and-implementation-layers.md)
- 현재 범위와 Maintain 경계 교정: [`records/2026-08-14-04`](../records/2026-08-14-04-current-scope-and-maintain-boundary-correction.md)
- 완료 판단 전의 Reference Recover·Verify 구현과 검증: [`records/2026-08-14-05`](../records/2026-08-14-05-reference-recover-verify-implementation-and-verification.md)
- Reference Maintain 구조 교정과 최종 검증: [`records/2026-08-14-06`](../records/2026-08-14-06-reference-maintain-structural-correction-and-verification.md)
- Reference Maintain agent 배치와 등록 결정: [`records/2026-08-14-07`](../records/2026-08-14-07-reference-maintain-agent-colocation-and-registration.md)
- 실행 가능한 기준 Project: [`reference-project/README.md`](../../../../reference-project/README.md)
- 직전 machine receipt 변경 기록: [`001 record`](../../001-reference-implementation/records/2026-08-14-05-machine-receipt-boundary-and-durable-verify.md)
