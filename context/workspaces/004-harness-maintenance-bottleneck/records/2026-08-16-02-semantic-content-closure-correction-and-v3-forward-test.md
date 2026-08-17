# Semantic content closure 교정과 v3 forward test

## 기존 결론의 보정

V2 blind 재적용은 live Reference runtime, Workspace와 Verify를 실제 target에 구성했으므로 Reference exact 계약을 skill에서 제거한 방향 자체는 작동했다. 그러나 사용자가 `context/project/`의 PRD·architecture가 상세 Owner 링크와 첫 Workspace 요약에 가까워 Project common context 책임을 실제 내용으로 채우지 못한 결함을 발견했다.

따라서 [`v2 재적용 평가`](2026-08-16-01-simplified-skill-reapplication-result.md)의 “중복 제거가 live contract 추종을 방해하지 않았다”는 기술적 적용 경계 안의 과거 판단으로 보존한다. 현재 결론은 간소화만으로 충분했던 것이 아니라, 이식 방법에 semantic content closure가 빠져 있었다는 것이다.

## Skill 보강

Main은 `apply-context-harness`와 application contract에 다음 이식 방법을 추가했다.

- 상세 Owner 경로만 연결하지 않고 여러 Workspace에 공통인 target 사실을 다시 서술한다.
- 선택한 Project context 문서가 맡은 내용을 채우지 못하면 보강하거나 만들지 않는다.
- Dry-run manifest에서 `source fact → target section` 매핑을 제시한다.
- 링크를 열지 않고 Project common context만 읽어 내용 충족을 검사한 뒤 원자료를 열어 사실·범위·우선순위 fidelity를 review한다.

Helper tests `7/7`, manual frontmatter·local link·diff 검사는 통과했다. 공식 `quick_validate`는 환경의 PyYAML 부재로 실행하지 못했다.

## V3 forward test 결론

`gpt-5.6-terra` 독립 task `01a009d3-5128-70a2-8ba3-591bcf62b1fe`에는 target `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test-v3`와 첫 Workspace 장면만 제공하고 과거 Workspace, v2 결과와 결함의 정답은 주지 않았다.

V3는 기존 docs를 상세 Owner로 보존하고 tracked 제품 변경 `0`, 새 non-ignored untracked 파일 `55`개로 additive 이식했다. Project common README·overview·architecture는 링크 목록이나 Workspace 요약에 머물지 않고 실제 Project 목적, 현재·미구현 범위, 성공·검증 경계, 구성요소의 권한·흐름·불변성을 다시 서술했다. Independent review는 P1 `0`이었고 sample routing P2는 target에 맞게 적응했다.

Product Verify는 root task graph `11/11`을 통과했고 후속 Recover는 snapshot `35/35`를 `fresh`로 판정했다. 상세 target 선택·문서·receipt와 Main 재검증은 [`Workspace 002 v3 record`](../../002-project-application/records/2026-08-16-02-project-common-context-correction-and-v3-forward-test.md)가 소유한다.

## 병목 결론과 proof ceiling

Exact Reference 계약 복제 제거는 live runtime 추종의 중복을 줄였지만, target Project common context를 책임 있는 내용으로 닫는 별도 이식 규칙이 필요했다. 사용자 발견으로 semantic closure를 명시하고 과거 답을 주지 않은 blind v3에서 같은 target 결함이 해소된 것은 이 보강의 forward evidence다.

다만 Terra와 Main의 첫 full Harness run에서 같은 descendant timing test 한 건이 각각 실패하고 isolated·full rerun 뒤에 통과했다. 안정적인 all-green은 증명하지 않는다. V3도 같은 Payment target의 새 사본이므로 서로 다른 Project portability·generalization, 실제 PG·DB·WebView·브라우저, 새 target-scoped role discovery와 사람 acceptance를 증명하지 않는다. Source skill·Workspace 문서와 target 설치물은 commit하지 않았다.
