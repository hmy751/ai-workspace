# 최신 Reference 보완 적용

2026-09-09 사용자가 승인한 범위에서 기존 Context Harness를 보완한다. Source `87d21023f6acd8ae709322d48da9851594f9acb0`의 Reference는 clean이며 target은 `feat/noline-context-harness`, `b4ed41f6e4bbae26fd45827b3b9063097a2c1ea4`에서 시작한다. 이전 설치는 `f0bada9`를 사용했다. 사라진 이전 준비물을 재사용하지 않고 새 preflight를 확보했다.

## 적용과 보존

Project common/current/guidance와 Decision 계약을 구성하고, 기존 active 이식 Work를 Spec 다섯 파일·Ticket으로 이어간다. 최신 Recover·Maintain 원본의 변경분과 tests를 적용하되 Noline Claude adapter·settings·wrappers와 기존 agents·dispatcher는 유지한다. 여섯 Reference skill은 `.claude/skills/` 원본과 `.agents/skills/` 상대 bridge에 적응한다.

기존 상세 문서 전체 정비와 제품 리팩토링은 하지 않는다. Flat Project 본문은 전환 안내 뒤에 원문을 보존하고 현재 authority에서는 내려왔다. 이전 memory 세 파일의 바이트는 [prior-memory](../source/prior-memory/)에 보존한다. [Fresh preflight](receipts/preflight/preflight-20260909T140507056185Z-f1caf35fc6894327a7d811ffd7622f3c.json)는 개인 세션 파일 9개와 기존 Python cache를 보호 목록으로 고정한다. Private 원문은 해석·복제하지 않았다.

Active/default 및 변경 대상 consumer는 `001-noline-context-harness-application` 하나다. Preflight에서 두 host runtime 디렉터리가 없어 current-generation bound consumer는 관찰되지 않았다. 이 Workspace의 Project 선택·memory·state·output을 reconcile하며 active id는 바꾸지 않는다.

## 검증 입력과 상한

직접 `node scripts/check-harness.mjs`는 기존 Git whitespace 확인까지 유지한다. Durable Verify는 `node scripts/check-harness.mjs --no-git-diff`로 regular-file 검사를 실행한다. 그 명령이 읽는 모든 현재 Markdown 본문, 설정·agent 본문과 검사 스크립트를 evidence로 선언한다. Package manager·lockfile·compiler·제품 소스는 이 argv가 실행하지 않으므로 그 내용을 검증했다고 하지 않는다.

Symlink의 연결과 directory membership·링크 target 존재는 실행 당시 관찰이며 regular-file snapshot freshness가 이후 topology의 동일성을 보장하지 않는다. Git HEAD·index·whitespace는 별도 직접 검사 결과다. 새 Markdown이나 entry가 추가되면 Verify 입력 closure를 다시 구성하고 실행해야 한다. Node/OS와 외부 상태는 snapshot할 제품 입력이 아니다. Receipt는 선언 snapshot과 해당 실행 사건에만 한정한다.

Harness 테스트는 별도 [Harness test receipt](receipts/harness-tests/)에서 보존하고 Product Verify의 구조 검사와 구별한다. Ephemeral validation은 임시 fixture만 사용한다. 기존 descendant timeout timing failure는 원본 test를 바꾸지 않고 실제 결과로 남긴다.

## 현재 결과

적용 파일과 검증을 진행 중이며 실제 결과를 회수한 뒤 이 절을 갱신한다. 독립 reviewer가 원자료·target diff·증거를 직접 대조한다. 실제 target-root skill discovery·invocation·Main 결과 전달·문서 유지와 Codex/Claude host trust·explicit activation·event receipt는 미확인이다. Maintain 상태는 `activation_pending`이며 새 session default-unbound를 유지한다. Stage·commit·branch 변경·제품 acceptance·Workspace 완료는 수행하지 않는다.
