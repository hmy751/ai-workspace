# Harness maintenance bottleneck memory

마지막 갱신: `2026-08-16`

## 목표

Context+harness의 안전성과 재진입 가능성은 유지하면서, 작은 변경이 과도한 문서 갱신·Workspace 정합화·검증·review로 번지는 유지보수 비용을 줄인다.

## 유지할 기준

- Harness의 보호 대상은 현재 명령·schema·경로 자체가 아니라, 필요한 맥락의 선택적 복구와 실제 검증 결과가 지속 상태·다음 행동으로 이어져 다음 작업자가 낡은 상태나 근거 없는 완료에서 시작하지 않게 하는 것이다.
- Harness의 목적과 구현 방법을 구분한다. 책임, 활성 시점, 실행 주체와 CLI·schema·경로 같은 수단을 자동으로 동일시하지 않는다.
- 재진입의 read-only Recover, 의미 변화의 Maintain, durable product Verify, ephemeral Harness validation과 사람 acceptance를 서로 다른 책임으로 유지한다. Validation은 네 번째 작업 workflow 단계가 아니다.
- Live `reference-project`가 exact schema·status vocabulary·내부 topology와 tool adapter를 소유한다. Reference-only 계약 변경이 이식 방법을 바꾸지 않으면 `apply-context-harness`를 함께 수정하지 않는다.
- `apply-context-harness`는 target 원자료 조사, preflight와 ignored path 보완, Owner mapping, 승인 전 dry-run manifest, additive adaptation, Maintain adapter 등록 또는 main fallback, 위험 기반 검증과 보고를 소유한다. Target 사실과 실제 적용 이력은 각각 Target Project와 Application Workspace가 소유한다.
- Project common context는 상세 Owner 경로를 모은 링크층이나 첫 Workspace 요약이 아니다. 여러 Workspace가 공통으로 판단할 실제 목적·현재와 미구현 범위·성공 및 검증 경계·구조·권한·흐름·불변성을 target 원자료에서 선별해 다시 서술해야 한다.
- 상세 Owner에서 제품 기준·구조·채택 결정처럼 구분되는 공통 책임을 확인하면 각각 대응하는 Project context Owner가 맡아야 한다. Overview는 진입 요약이며 독립된 책임을 흡수해 Owner를 없애는 합본이 아니다.
- Project context Owner 생략은 원자료에 독립된 공통 내용이 없을 때만 허용한다. 조사한 상세 Owner와 생략 근거를 dry-run manifest와 application record에 남기고, 작성 뒤 내용 충족·책임별 Owner closure·원자료 fidelity를 검토한다.
- 확인하지 않은 의미 정확성, 외부 동작, 사람 acceptance를 구조 테스트만으로 증명했다고 말하지 않는다.
- 사용자 변경, 기존 canonical, append-only evidence를 속도 개선을 이유로 덮어쓰거나 삭제하지 않는다.
- Current는 다음 행동에 필요한 현재 정보만 유지하고, 상세 과정은 records에 남긴다.
- Historical record는 당시 사실로 보존하며 현재 계약을 다시 설명하는 정본으로 사용하지 않는다.
- 검증 강도는 변경 위험에 비례시킨다. 반복 개발 확인과 상태 전환용 durable verify를 구분한다.
- Context 이동·링크·설명 정리처럼 실행 의미를 바꾸지 않는 작업은 경로·링크·설정 parse·diff부터 확인하고, schema·실행 코드·evidence 범위·path 방어·사용자 파일 보호처럼 실패 영향이 큰 변경에서만 검증을 단계적으로 넓힌다.
- 독립 review는 일괄 절차가 아니라 Workspace scene과 Verify output이 어긋날 위험처럼 의미상 실패 영향이 큰 경계를 검사한다. 같은 target의 blind 재적용에서는 이 기준이 API-only Verify의 누락을 실제로 찾아냈다.

## 채택된 Reference 경계

- Harness 구현은 책임 기준의 `recover/`, `maintain/`, `verify/`, `validation/`과 공용 test fixture `testing.py`로 나뉜다.
- Maintain의 지속 의미·규칙은 Work·Workspace canonical이 소유한다. 계약과 교체 가능한 agent 정의는 `context/work/harness/maintain/`, 발견 등록은 Project root `.codex/config.toml`, 상세 운영 routing은 `context/work/AGENTS.md`가 소유한다.
- Maintain용 Python CLI·schema는 두지 않는다. Reference의 `workspace-context-maintainer` adapter와 outer repo-local `context_maintainer`는 서로 다른 대상과 권위를 가진다.

## 현재 범위

- 구현·검증·commit한 `reference-project` Recover·Maintain·Verify·validation 책임 재배치와 proof ceiling
- `apply-context-harness`, application contract와 skill index의 소유 경계 간소화
- 간소화한 절차의 forward preflight, v2 링크형 content 결함, v3 Owner omission loophole과 최신 skill 교정
- 사람 acceptance와 아직 재시험하지 않은 최신 skill 교정의 최종 확인

## 범위 밖

- Recover·verify 제거
- Receipt 증거 또는 path 안전성 약화
- 사람 acceptance 자동화
- Reference exact 계약을 skill에 복제하거나 과거 target 호환 이력을 현재 절차로 고정
- 독립 target 재이식의 상세 내용·과정·검증 결과를 이 Workspace에 복제
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
- `apply-context-harness` 간소화와 검증: [`records/2026-08-14-08`](../records/2026-08-14-08-apply-context-harness-simplification-and-verification.md)
- 간소화 skill 재적용의 병목 개선 평가: [`records/2026-08-16-01`](../records/2026-08-16-01-simplified-skill-reapplication-result.md)
- Semantic content closure 교정과 v3 forward test: [`records/2026-08-16-02`](../records/2026-08-16-02-semantic-content-closure-correction-and-v3-forward-test.md)
- Project context Owner omission loophole 교정: [`records/2026-08-16-03`](../records/2026-08-16-03-project-context-owner-omission-loophole-correction.md)
- v2 상세 target 적용·검증 Owner: [`Workspace 002 v2 record`](../../002-project-application/records/2026-08-16-01-simplified-skill-blind-reapplication.md)
- v3 상세 target 적용·검증 Owner: [`Workspace 002 v3 record`](../../002-project-application/records/2026-08-16-02-project-common-context-correction-and-v3-forward-test.md)
- 최신 omission 교정의 상세 Owner: [`Workspace 002 correction record`](../../002-project-application/records/2026-08-16-03-project-context-owner-closure-correction.md)
- 실행 가능한 기준 Project: [`reference-project/README.md`](../../../../reference-project/README.md)
- 이식 skill: [`apply-context-harness/SKILL.md`](../../../../.agents/skills/apply-context-harness/SKILL.md)
