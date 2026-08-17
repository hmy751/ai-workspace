# Project application state

마지막 갱신: `2026-08-16`

## 현재 문제

사용자 후속 검토에서 v3가 link-only 문제는 개선했지만 Project common context의 Owner closure를 끝내지 못했음이 확인됐다. Target 원자료의 `docs/product-brief.md`와 공통 복구 결정에는 여러 Workspace가 함께 쓸 독립 내용이 있는데도 v3는 `README.md`, `overview.md`, `architecture.md`만 만들고 `prd.md`와 `decisions/`를 생략했다.

## 현재 상태

- V3 target은 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v3`에 그대로 있으며 이번 정정에서 보정하지 않았다.
- V3의 Harness·Product Verify·Recover 결과는 당시 실행 사건으로 유지한다. 그러나 그 green 결과와 당시 content check는 누락된 Project context Owner를 찾지 못했으므로 Project common context 이식 완료나 content closure 통과를 증명하지 않는다.
- Main은 repo-local `apply-context-harness` skill에 다음 규칙을 추가했다.
  - 원자료에 구분되는 공통 제품 기준·구조·채택 결정이 있으면 overview에 합치거나 생략하지 않고 대응 Project context Owner를 실제 내용으로 구성한다.
  - Owner 생략은 독립된 공통 내용이 없음을 원자료로 확인하고 manifest와 application record에 근거를 남길 때만 허용한다.
  - Overview는 모든 공통 내용을 합친 문서가 아니라 Project context의 진입 요약이다.
- Skill 재보강 뒤 blind reapplication, Terra 재시험, target 검증은 수행하지 않았다.
- V3 target 설치 파일은 여전히 untracked이고 stage·commit·사람 acceptance가 없다.
- V2·v3 records는 과거 사건으로 보존하며 최신 정정은 [Owner closure 정정 기록](../records/2026-08-16-03-project-context-owner-closure-correction.md)이 소유한다.

## 남은 불확실성

- 새 규칙이 실제 target에서 `prd.md`와 `decisions/` Owner를 빠짐없이 구성하는지는 미검증이다.
- V3 target은 미보정 상태이므로 현재 skill 결과를 대표하지 않는다.
- 반복 descendant timeout timing flake, 다른 Project portability, 실제 PG·DB·WebView·browser·사람 acceptance도 여전히 미해결이다.

## 다음 행동

다음 재시험이 승인되면 새 격리 target에서 원자료의 독립된 공통 내용 inventory, manifest의 Owner 대응·생략 근거, 생성된 Project context 내용을 함께 대조한다. 그 전에는 skill 재보강 완료와 적용 검증 완료를 구분한다.
