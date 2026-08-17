# Apply Context Harness 간소화와 검증

기록일: `2026-08-14`
상태: 구현·독립 review·정적 확인 완료, portability 검증·사람 acceptance·commit 대기

## 병목과 사용자 승인

Reference 책임 재배치는 commits `638bfbc`, `7793bab`에 보존됐고 현재 HEAD는 `7793bab`이다. `reference-project/` scoped tree도 clean이다. 그러나 `apply-context-harness`와 application contract가 Reference의 exact schema, status vocabulary, 내부 경로와 과거 호환 이력을 다시 설명하고 있어, 이식 방법이 바뀌지 않은 Reference-only 변경도 skill 갱신·검증으로 전파되는 병목이 남았다.

사용자는 Workspace 004 범위에서 이 중복을 줄이는 skill 간소화를 승인했다. 채택한 소유 경계는 다음과 같다.

- Live [`reference-project`](../../../../reference-project/)가 현재 Project·Work·Workspace·Harness 책임, exact 실행 계약, schema·status와 내부 topology를 소유한다.
- [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/SKILL.md)는 target 원자료 조사, preflight와 ignored path 보완, Owner mapping, 승인 전 dry-run manifest, additive adaptation, Maintain adapter 등록 또는 main fallback, 위험 기반 validation과 evidence/reporting을 소유한다.
- Target Project는 자기 canonical·제품 코드·검증 명령·acceptance를, Application Workspace는 실제 적용 source commit·선택·예외·증거와 proof ceiling을 소유한다.
- Reference-only 계약 변경이 target 이식 방법을 바꾸지 않으면 skill은 바뀌지 않아야 한다.

## 변경 파일과 크기

- [`.agents/skills/apply-context-harness/SKILL.md`](../../../../.agents/skills/apply-context-harness/SKILL.md): live Reference 탐색부터 승인 전 manifest, 책임별 적응, 위험 기반 검증과 보고까지 이식 절차만 남겼다.
- [`.agents/skills/apply-context-harness/references/application-contract.md`](../../../../.agents/skills/apply-context-harness/references/application-contract.md): exact Reference 계약 대신 target마다 다시 판단할 Owner·충돌·evidence closure·검증 선택 기준을 남겼다.
- [`.agents/skills/README.md`](../../../../.agents/skills/README.md): skill 설명을 현재 소유 경계에 맞췄다.

독립 review P3 문구를 반영한 뒤 `wc -l -w`로 계측한 작업 트리와 HEAD baseline의 비교는 다음과 같다. 이 숫자는 `2026-08-14` 검증 시점의 byte 상태이며 이후 수정의 자동 불변 조건은 아니다.

- `SKILL.md`: 157줄·1,860단어 → 120줄·1,122단어
- `application-contract.md`: 137줄·1,701단어 → 94줄·792단어
- 합계: 294줄·3,561단어 → 214줄·1,914단어. 80줄, 1,647단어를 줄여 각각 27.2%, 46.3% 감소했다.

## Synthetic forward preflight

간소화한 절차를 synthetic target `/private/tmp/context-harness-skill-forward.PQGFll`에서 approval 이전까지만 forward 실행했다. Target HEAD는 `4f90f5eb47e276889e2e413d4e8e82cfb3105e2b`였다.

- Preflight는 기존 untracked `notes/in-progress.md`를 54 bytes, SHA-256 `89b8c642a90663974d550d15aa8e8ee2d48866a9f221bc3ed0a24cd0c95c02fa`로 포착했다. 실행 뒤에도 이 파일은 untracked 상태로 보존됐다.
- Target의 `.gitignore`가 `context/`를 무시한다는 사실과 기존 `.codex/config.toml`이 같은 `workspace_context_maintainer` role을 `../ops/existing-maintainer.toml`에 등록한다는 Owner 충돌을 별도로 찾았다.
- Dry-run manifest는 ignore 예외를 승인받아 추가할지와 기존 role을 보존하고 Reference adapter를 제외해 main fallback을 쓸지 등의 선택을 사용자 승인 경계에 남겼다. 자동 overwrite·role 교체는 하지 않았다.
- Target에는 `context/`를 만들지 않았고 tracked 파일도 고치지 않았다. Target setup 뒤 pre-approval 실행의 유일한 새 출력은 `/private/tmp/preflight-20260814T114943536220Z-d7d8c8362a6d48ddbb9ff2e09de4b130.json`이었다.

이 결과는 helper가 ignored inventory를 직접 수집한다는 뜻이 아니다. Skill이 receipt 밖에서 payload path·ancestor, ignore와 기존 설정을 별도로 대조해야 한다는 절차가 실제 충돌을 찾았음을 보여 준다.

## 독립 review와 반영

독립 reviewer의 verdict는 `accept`였고 P1·P2는 없었다. P3 두 문구는 바로 반영했다.

- 설정 parse와 adapter path 해석만 확인했을 때 새 Codex task의 실제 role discovery까지 검증했다고 쓰지 않고, discovery가 확인되지 않거나 충돌하면 live Maintain 계약을 main이 수행하는 fallback과 미설치 범위를 남긴다.
- Ephemeral Harness validation, target-specific durable Harness test receipt와 Product Verify receipt는 목적과 보존 경계가 다르므로 서로를 대신하지 않는다.

## 검증과 proof ceiling

- Reference 전체 suite 첫 실행은 53개 중 POSIX descendant-timeout test 1건이 실패했다. 해당 범위 5/5와 전체 suite 재실행 53/53은 통과했다. 이번 skill 변경은 Reference 실행 코드를 고치지 않았으며, 첫 실패가 timing flake인지 확정하지 않았다.
- 이 suite 결과는 기존 Reference 회귀 상태의 관찰이지 skill 문구의 의미 정확성, target portability나 새 Codex task의 role discovery를 증명하지 않는다.
- Official skill `quick_validate`는 환경에 PyYAML이 없어 실행하지 못했다. 대체 확인으로 exact frontmatter 규칙, helper test 7개, 로컬 링크, stale literal 부재, staged·unstaged `git diff --check`가 통과했다.
- Synthetic 실행은 승인 전 preflight와 manifest 판단까지만 확인했다. 실제 이식, Harness validation, Product Verify, 사람 acceptance와 target commit은 수행하지 않았다.

## 다음 독립 적용

사용자는 다음 portability 검증으로 Workspace 002 이력의 Payment Recovery/Kurly portfolio target을 선택했다. 별도 worktree에서 `gpt-5.6-terra` 독립 task에 최소 prompt만 주고 재이식해, 현재 skill과 live Reference만으로 Owner 조사·충돌 보호·적응·검증 절차를 복원하는지 본다.

이 실행의 target-specific source, 선택, manifest, 변경, receipt와 검증 결과는 해당 Application Workspace가 소유한다. Workspace 004에는 재이식 결과가 skill의 일반 소유 경계나 절차를 바꿀 때 그 결론과 근거 접근점만 되돌린다.
