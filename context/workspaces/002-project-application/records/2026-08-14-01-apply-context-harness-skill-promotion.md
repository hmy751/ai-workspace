# Apply Context Harness 반복 절차 승격

날짜: `2026-08-14`
상태: repo-local skill과 migration helper 구현·로컬 검증 완료, 두 번째 실제 Project 이식 전

## 승격 결정

첫 Payment Recovery 적용에서 반복된 이식 순서와 증거 요구를 repo-local [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/) skill로 승격했다. 첫 적용의 구체 배치·실패·receipt·proof ceiling은 [기존 적용 기록](2026-08-13-01-payment-recovery-project-application.md)이 계속 소유하며, skill에 복제하지 않았다.

이 절차는 대상 Project의 경로가 있는 context+harness 이식 요청에서 기존 canonical과 사용자 변경을 먼저 고정하고, 대상별 Owner 배치와 recover·verify 계약을 만든 뒤 `recover → verify → recover`와 durable receipt로 확인한다. 대상 경로가 없거나 단순 `reference-project/` 수정·구조 설명·이미 설치된 Project의 브라우저 acceptance만 요청하는 경우에는 발동하지 않는다.

## 세 산출물의 역할

- 현재 [`reference-project/`](../../../../reference-project/): Project–Workspace–Harness 책임이 실제로 실행되는 기준 Project다. 범용 복사 템플릿이나 설치 패키지가 아니다.
- [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/): 기준 Project의 책임을 대상 Project의 기존 Owner 구조에 맞춰 이식하는 절차와 migration-only helper다. Project 사실이나 적용 결과를 소유하지 않고, `reference-project/`나 target 내용을 assets로 복제하지 않는다.
- 이 Workspace의 `records/`: 실제 적용에서 확인한 배치, 사용자 선택, 시도, 실패·성공 receipt, target별 예외와 증거 상한을 보존한다.

실행 책임 변경은 `reference-project/`, 반복할 판단과 절차는 skill, 실제 이식 결과는 application Workspace records에 둔다.

## Repo-local 배치와 routing

skill은 이 저장소의 live `reference-project/`, Project application Workspace, context maintainer routing을 함께 사용하므로 [`.agents/skills/`](../../../../.agents/skills/)에 두었다. 루트 [`AGENTS.md`](../../../../AGENTS.md)는 사용자가 대상 Project 경로와 함께 이식·적용을 요청할 때 skill을 사용하도록 routing하고, 루트 [`README.md`](../../../../README.md)는 사람이 찾는 진입점을 제공한다.

점검 시 `~/.claude/skills/apply-context-harness`, `~/.codex/skills/apply-context-harness`는 없었고 global skills·projects·runtime index에도 이름이 없었다. repo-local skill을 전역 capability나 다른 Project의 기본 규칙으로 등록하지 않았다.

## Migration-only helper와 보존 범위

### `capture_target_state.py`

첫 target 쓰기 전에 다음을 임시 append-only receipt로 관찰한다.

- target Git root, branch, HEAD와 사람이 읽는 porcelain status
- tracked worktree 변경, staged 변경, untracked 파일
- dirty·untracked path의 kind, byte size, SHA-256 또는 symlink target
- 발견한 `AGENTS.md`, `CLAUDE.md`의 위치와 hash

기본 출력은 target 밖 `/private/tmp`에 두고, Workspace records가 생기면 byte-identical copy로 보존한다. 이 receipt는 한 번의 순차 local capture이며 Git lock을 잡은 atomic snapshot이 아니다. 동시 writer가 있으면 status와 hash 시점이 다를 수 있고, 저자·변경 이유·삭제 주체·Git 밖 과거 상태를 증명하지 않는다.

### `record_harness_tests.py`

target-specific Harness의 Python source를 실행 전에 SHA-256·size로 캡처하고, 현재 Python으로 shell 없이 `unittest discover`를 실행해 argv, test count, exit, timeout, stdout·stderr와 truncation을 append-only receipt로 남긴다. timeout은 POSIX에서 같은 process group을 종료하고, 0개 discovery나 unittest 요약 부재는 pass로 기록하지 않는다.

이 helper는 임의 command runner가 아니며 제품 verify를 대신하지 않는다. 지정한 source root 아래 Python 파일과 unittest 결과만 연결하고, 새 session으로 process group을 벗어난 descendant까지 격리하는 sandbox는 아니다. 브라우저·외부 시스템·사람 acceptance와 target commit도 증명하거나 수행하지 않는다.

두 helper는 이식 과정에서 관찰과 증거 기록을 결정적으로 만드는 도구다. target 제품 runtime이나 Harness payload에 복사하는 산출물이 아니다.

## 검증 결과

### Helper unit

같은 7개 unit test를 두 runtime에서 실행했다.

- `python3` `3.14.3`: 7개 통과, exit `0`
- `/usr/bin/python3` `3.9.6`: 7개 통과, exit `0`

테스트는 target 비변경 preflight, Git root 아닌 하위 경로 거부, Harness source 선캡처와 성공·실패 receipt, 0개 discovery 실패 처리, bounded output, timeout process-group 종료를 확인한다.

### Skill 구조와 routing

- skill-creator의 `quick_validate.py`를 `uv run --with pyyaml` 임시 의존성 환경에서 실행해 `Skill is valid!`를 확인했다. 기본 `python3` 실행은 환경에 PyYAML이 없어 validator가 시작되지 않았으며 skill 실패로 계산하지 않았다.
- `agents/openai.yaml`은 별도 YAML parser로 mapping과 `interface`, `policy` key를 확인했다.
- 새 skill과 routing 파일을 exact path로 stage한 뒤 `git diff --cached --check`가 통과했다.
- 실제 skill discovery에서 `apply-context-harness`의 이름·경로·description이 노출됐다.
- trigger-forward 검증은 대상 절대 경로가 있는 이식 요청은 trigger, 대상이 없는 일반 적용 요청과 이미 설치된 Project의 브라우저 acceptance 요청은 non-trigger로 판정했다.

### 독립 검토

구현과 분리된 reviewer가 최신 live skill, helper와 tests를 검토하고 unit 7개 통과를 재확인했다. 최종 판정은 `P1 없음`, `P2 없음`, `P3 없음`이며 reviewer는 파일을 수정하지 않았다.

## 검증 상한과 다음 확인

이번 검증은 skill 문서·routing·helper 계약의 구조 정합성, 두 Python runtime 호환성, synthetic 임시 Git repository에서의 helper 행동과 독립 코드 검토를 확인한다.

두 번째 실제 Project에는 아직 이식하지 않았다. 따라서 다음은 증명하지 않았다.

- 다른 Project canonical과 기존 `context/`·instruction file 충돌에서의 실제 adaptation
- 다른 runtime, package manager, test graph에서 verify evidence가 닫히는지
- preflight부터 `recover → verify → recover`, 사람 acceptance 경계까지 전체 절차가 다시 재현되는지
- 두 Project 이상에서의 portability와 generalization

다음 검증은 사용자가 두 번째 대상 Project와 변경 범위를 명시한 뒤 이 repo-local skill을 처음부터 끝까지 적용하고, 그 Project의 Workspace records에 target별 결과와 proof ceiling을 남기는 것이다. 그전에는 이 skill을 범용으로 입증됐다고 표현하지 않는다.
