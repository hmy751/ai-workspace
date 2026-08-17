# Project context Owner closure 정정

## 사용자 정정

V3는 `context/project/README.md`, `overview.md`, `architecture.md`에 링크가 아닌 실제 내용을 담아 v2의 link-only 문제는 개선했다. 그러나 target의 `docs/product-brief.md`와 공통 복구 결정에는 여러 Workspace에 공통인 독립 제품 기준과 채택 결정이 있었는데도 대응하는 `context/project/prd.md`와 `context/project/decisions/` Owner를 만들지 않았다.

따라서 [v3 forward-test 기록](2026-08-16-02-project-common-context-correction-and-v3-forward-test.md)의 실행·검증 결과는 과거 사건으로 유효하지만, v3를 Project common context 이식 완료나 content closure 통과로 해석한 부분은 최신 상태가 아니다. V3 target은 이번 정정에서 수정하지 않았다.

## Skill 재보강

Main은 repo-local `apply-context-harness` skill에 다음 기준을 추가했다.

- 원자료에 구분되는 공통 제품 기준·구조·채택 결정이 있으면 overview에 억지로 합치거나 생략하지 않고 대응 Project context Owner를 실제 내용으로 구성한다.
- Owner 생략은 독립된 공통 내용이 없음을 원자료로 확인하고 manifest와 application record에 근거를 남길 때만 허용한다.
- Overview는 모든 공통 내용을 합친 문서가 아니라 Project context Owner들을 찾는 진입 요약이다.

## 현재 검증 상태

Skill 규칙 보강 뒤 blind reapplication이나 Terra 재시험을 수행하지 않았다. `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v3`도 미보정 상태다. V3의 기존 Harness·Product Verify·Recover receipt는 당시 설치와 제품 명령 실행을 증명하지만, 누락된 `prd.md`·`decisions/` Owner나 새 omission 근거 계약을 검증하지 않는다.

다음 재시험에서는 원자료의 독립 공통 내용 inventory, manifest의 Owner 대응·생략 근거, 실제 생성된 Project context 내용을 함께 대조해야 한다. 그 전까지 현재 상태는 **skill 재보강 완료, 재시험 안 함, v3 target 미보정**이다.
