# Simplified skill 재적용의 병목 개선 평가

## 평가 경계

Simplified `apply-context-harness`가 Reference의 exact schema·status·내부 topology를 skill에 복제하지 않고도 live Reference를 따라 실제 target 이식을 수행할 수 있는지 확인했다. `gpt-5.6-terra` 독립 task `01a00054-46b1-7a90-b4f1-1cbf1f49de2c`에는 같은 Payment target의 새 사본, 첫 Workspace 장면과 과거 application Workspace 입력 금지만 주었다. 사용한 live Reference commit은 `7793babc81f80562d677438a9190abebe182faed`다.

적용과 receipt의 상세 사실은 이 Workspace가 복제하지 않는다. Target 선택, manifest, Context·Workspace 구성, 검증 명령과 결과, Main 재현 및 target proof ceiling은 [`Workspace 002의 blind 재적용 record`](../../002-project-application/records/2026-08-16-01-simplified-skill-blind-reapplication.md)가 소유한다.

## 병목 개선 결론

- Reference exact 계약 복제를 제거했어도 독립 task는 live Reference runtime과 contract를 읽어 target Owner, Project common context, Workspace와 Harness를 구성했다. 승인 전 dry-run은 target write `0`을 유지했고, 승인 뒤 설치는 additive였다. 새 non-ignored untracked 파일은 `55`개, tracked 제품 diff는 `0`이었으며 stage·commit·사람 acceptance는 수행하지 않았다.
- 이 재적용 때문에 skill code를 추가 수정하지 않았다. 따라서 이번 범위에서는 Reference 실행 계약과 이식 절차의 중복 제거가 live contract 추종을 방해했다는 증거가 없다.
- 위험 기반 independent review는 형식 확인을 반복한 것이 아니라 첫 API-only manifest가 Workspace scene의 Checkout 결과 불명 output을 검증하지 않는 P1을 발견했다. Verify를 API+Checkout `9/9` durable 실행으로 보정했고 Main도 같은 `9/9`를 재현했다. 위험에 비례한 review가 실제 의미 누락을 잡은 사례다.
- Main은 target 사람용 record에서 source commit, preflight link, ignored `node_modules`와 toolchain snapshot 한계, target-scoped role discovery 한계가 빠진 것을 발견했다. Explicit Workspace Maintain으로 이를 보완했다. 이는 적용 완료 시 reporting completeness를 확인할 필요가 있음을 보여주지만, 현재 증거만으로 skill completion/reporting 문구를 다시 수정할 근거는 아니다.

## 검증 상한

마지막 durable Harness receipt는 `46/46`, ephemeral validation은 `1/1`을 보존하고 Recover는 packet schema `6`, status schema `3`, current freshness `fresh`, snapshot `16`개의 changed·missing·unavailable `0`을 보고했다. 그러나 독립 task와 Main의 첫 full Harness run에서 같은 descendant timing test가 각각 한 번 실패했고 isolated·full rerun 뒤에만 통과했다. 그러므로 안정적으로 반복되는 all-green은 증명하지 않는다.

이 시험은 같은 Payment target에 simplified skill을 다시 적용한 결과다. 서로 다른 Project portability·generalization, 새 target-scoped Codex role discovery, 실제 PG·영속 DB·WebView·브라우저, 사람 acceptance와 운영 효과는 증명하지 않는다. Source skill 간소화와 Workspace 문서는 `context-harness` main working tree에서 아직 commit하지 않았고, target 설치물도 stage·commit하지 않았다.

## 현재 영향

계획했던 blind 재적용은 완료됐다. 남은 판단은 사람 acceptance, source skill·Workspace 004·002 문서 commit 여부, 반복 timing flake를 별도 진단할지, 실제 role discovery나 서로 다른 Project 시험을 후속 범위로 열지다.
