# Noline 설치본 독립 검토

## 판정과 경계

2026-09-09 실제 설치본의 원자료·diff·입력 계약·전체 test receipt와 Product Verify→Recover를 검토한 결과, 현재 미해결 P1/P2 finding은 없다. 아래 최종 증거 대조까지 실제 파일에서 확인했다. 설치 준비물의 검토를 설치 성공으로 대신하지 않았다.

사용자는 Noline의 기존 Context Harness를 최신 Reference로 보완하도록 요청하면서 “문서 전체까지는 말고”, “너무 많은 제약은 주지말고”라고 했다. 검토는 그 이식과 기존 사용자 작업·Noline 고유 연결 보존에 한정했다. 제품 리팩토링, 상세 문서 전체 정비, 실제 host activation과 효과 평가를 완료 조건으로 추가하지 않았다.

## 입력과 독립성

- Source: `87d21023f6acd8ae709322d48da9851594f9acb0`의 `reference-project/`, `apply-context-harness` skill과 application-contract.
- Target: `/Users/hammyeong-yeon/Desktop/10_work/noline`, baseline `b4ed41f6e4bbae26fd45827b3b9063097a2c1ea4`.
- 변경 전 관찰: [preflight.json](../application/resume-20260909/preflight.json).
- 실제 변경 목록과 파일 hash: [application paths](../application/resume-20260909/paths.json). 준비물과 실제 설치본의 runtime·skill bytes도 별도로 대조했다.

Main은 사용자 요청, source·target 접근점과 수정 금지 경계만 전달했다. Reviewer가 선택한 Project 본문에서 의미를 먼저 구성한 뒤 Noline root guide·제품 README·관련 상세 rule/context와 sync source를 열어 대조했다. 구현자의 결론을 근거로 삼지 않았다. Private session 원문과 무관한 다른 Desktop 프로젝트는 읽지 않았다. Target 파일을 수정하거나 Target durable Verify·session activation을 실행하지 않았다.

## 실제로 확인한 내용

선택된 Project 본문만으로 Noline이 불안정한 네트워크에서도 여행 일정과 경비 입력을 이어가려는 제품임을 설명할 수 있다. 활성 여행의 Local SQLite와 비활성 여행의 Server API, Data Router와 지도·검색 같은 서비스의 정책 판단, transaction과 sync queue, schema·ID·시간·인증 관계가 구별된다. 현재 client/server/schema/UI 책임과 구조 검사·제품 동작·실환경 acceptance의 증명 범위도 구분된다. 이 의미는 Noline의 기존 상세 Owner와 관련 코드에 지지됐다. Guidance는 세 설명 skill의 조건부 consumer로 유지되고 모든 Recover의 기본 입력으로 확대되지 않았다.

실제 설치본은 기존 active `001-noline-context-harness-application`의 목표를 최신 이식 보완으로 이어가며 후속 제품 리팩토링 목표를 만들지 않았다. Spec 다섯 파일과 Ticket 색인이 현재 작업의 의미를 소유하고, machine identity·Project 선택·Verify 실행 계약·결과 cursor·실행 시 freshness와 사람용 state의 역할이 구별된다.

Reviewer가 직접 `python3 -B -m context.work.harness recover 001-noline-context-harness-application --json`과 id 없는 Recover를 실행했다. 둘 다 exit 0이며 같은 context 입력 15개를 읽었다. 기본 경로에만 active index가 control 입력으로 추가됐다. Project README와 common/current/Decision, Spec 전체와 Ticket 색인·state·output이 선택되고 Ticket 본문·source·records 전체는 기본 입력에 포함되지 않았다. 이 시점의 기존 Verify receipt는 `stale`이었으며 새 Verify 전의 정상 상태로 구분했다.

Preflight의 기존 untracked 파일 18개는 실제 SHA-256이 모두 같았다. 기존 Claude adapter와 test·settings, Codex wrapper·hook·config, `noline-work`, active index는 baseline과 바이트가 같았다. `.agents/skills/`의 일곱 연결은 각각 같은 이름의 `.claude/skills/` 원본으로 해석됐다. 여섯 Reference skill의 본문·호출 설정과 변경한 Python runtime·tests는 Source와 일치했다. 옛 memory 세 파일의 `source/prior-memory/*.txt` 보존본은 baseline 원문과 바이트가 같다. HEAD는 baseline에 머물렀고 staged 변경은 없었다. 두 host runtime 디렉터리는 없었다.

실제 변경 Markdown 48개에서 local link 315개를 검사해 missing target과 Project root 밖 target은 없었다. 별도로 선택된 Project/current/output의 주요 link가 설명한 실제 Owner를 가리키는지 대조했다. 준비물의 `output/index.md`에 있던 `../../../SPEC-AND-TICKETS.md`는 설치본에서 `../../SPEC-AND-TICKETS.md`로 수정돼 Workspace collection canonical을 가리킨다. 준비 중 발견해 전달한 이 국소 결함은 해소됐다.

`scripts/check-harness.mjs`가 `--no-git-diff`에서 내용으로 읽는 현재 regular 입력을 다시 펼쳤다. 확인한 111개 입력은 `canonical_basis`와 `evidence_paths`의 123개 경로 안에 모두 포함되며 해당 선언 경로는 regular file이다. Directory entry·symlink target·link target 존재성은 실행 시 관찰되는 topology이고 이후 byte freshness가 이를 증명하지 않는다는 상한이 claim에 명시돼 있다. Git diff whitespace는 기본 구조 검사에서 별도로 실행된다.

## 시간 제한 테스트의 관찰

Worker의 첫 전체 Harness log인 `/private/tmp/noline-upgrade-all-tests.log`를 직접 읽었다. 전체 122건 중 1건이 실패했다. 실패는 `test_timeout_covers_descendant_after_group_leader_exits`에서 timeout exit 124를 기록한 뒤 `descendant.pid` 존재를 확인하는 assertion이었다. 자식 프로세스 잔존 여부를 확인하는 다음 단계까지 진행하지 못했으므로 이 실행으로 descendant 종료 장면이 입증됐다고 할 수 없다. 해당 테스트 본문과 Verify runtime은 baseline 대비 바뀌지 않았다.

Reviewer는 baseline Harness만 `/private/tmp/noline-review-baseline-nrfz43wv`에 복원하고 같은 테스트를 단독 실행했다. 이어 실제 Target의 같은 테스트도 단독 실행했다. 두 실행 모두 테스트 내부의 임시 Workspace만 사용했으며 Target durable Verify나 activation을 만들지 않았다.

```text
명령: python3 -B -m unittest context.work.harness.verify.tests.test_verify.VerifyTests.test_timeout_covers_descendant_after_group_leader_exits -v

baseline b4ed41f6: Ran 1 test in 0.413s — OK
installed target: Ran 1 test in 0.418s — OK
```

단독 실행에서는 이식 회귀가 재현되지 않았다. 최초 전체 실행 실패는 보존하며 timing에 민감한 fixture 관찰로 한정한다. 단독 pass로 최초 전체 suite가 모두 통과했다고 바꾸지 않는다.

## 최종 증거 대조

Worker가 문서 반영 뒤 실행한 실제 Target 증거를 다시 읽었다.

- [첫 전체 실행 log](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/001-noline-context-harness-application/records/receipts/harness-tests/2026-09-09-first-full-run.log)는 앞서 읽은 임시 원본과 바이트가 같다. 122건 중 앞서 설명한 1건 실패를 그대로 보존한다.
- [두 번째 전체 test receipt](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/001-noline-context-harness-application/records/receipts/harness-tests/harness-test-20260909T143128349049Z-ca581a4a12244cabba828fe6315ad037.json)는 전체 122건 pass, exit 0과 잘리지 않은 실제 unittest 출력을 담는다. 실행 전 snapshot한 Harness source 27개 모두 현재 파일 hash와 같다. Ephemeral validation과 기존 Noline Claude adapter tests도 그 실행의 통과 목록에서 확인했다.
- [Product Verify receipt](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/001-noline-context-harness-application/records/receipts/verify/verify-20260909T143334748605Z-8e8696ffe7494c0982d28b66308c7cad.json)는 `node scripts/check-harness.mjs --no-git-diff`, exit 0, `result: pass`를 기록한다. 실제 claim·argv·basis와 evidence 경로가 현재 `verify.json`과 같고, 실행 전 수집한 basis 3개와 evidence 120개가 현재 파일 hash와 모두 같다.
- Reviewer가 explicit/default Recover를 다시 읽기 전용 실행해 둘 다 exit 0, 위 receipt cursor, `fresh`, snapshot 123개, changed·missing·unavailable 각각 0을 확인했다. 이는 선언 파일의 동일성이며 topology·제품 동작·사람용 의미의 자동 증명으로 확대하지 않는다.

최종 적용 기록의 보호 파일 분류에 비차단 수치 오기 하나가 있었다. “개인 세션 파일 9개”는 preflight상 세션 파일 7개와 cache 11개, 총 18 entries이므로 Main에 정정을 전달했다. 보호 hash 확인 자체에는 불일치가 없다.

## 남은 확인

정적 설치·관련 실행 근거는 actual-host의 skill discovery·invocation, Main 결과 전달·Maintain 문서 반영, hook trust·explicit activation·같은 generation의 runtime event를 증명하지 않는다. `activation_pending` 표기가 현재 근거와 맞는다. 제품 기능·실기기·외부 시스템 acceptance, 후속 리팩토링 효과와 commit·Workspace 완료는 이번 독립 검토의 결론이 아니다.

이 리뷰 결과를 Target의 state·Ticket·적용 기록에 반영하면 그 Markdown도 Verify 입력이므로 직전 receipt는 stale해진다. Main/Worker가 짧은 Verify→Recover를 다시 실행해 최종 cursor를 연결할 예정이다. 이 문서에 이름을 적은 receipt의 확인 시점과 이후 새 receipt를 혼동하지 않는다. 제품·runtime을 추가로 바꾸지 않는 결과 기록 반영 때문에 독립 검토나 전체 test suite를 다시 반복할 필요는 없다.
