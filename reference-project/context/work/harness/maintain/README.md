# Maintain

Maintain은 한 작업 session을 이해한 agent가 모든 사용자 대상 Main response-end에서 지속할 의미가 생겼는지 점검하고, 명확한 변화만 선택한 Workspace의 기존 Context Owner에 반영하는 Harness 책임이다.

Context의 의미와 Owner는 [`Work context`](../../README.md), [`Workspace collection`](../../workspaces/README.md)과 선택한 Workspace README가 소유한다. Maintain agent, decision contract와 host adapter는 이 기준을 적용하는 교체 가능한 장치이며 새 canonical이 아니다.

Codex에서 main이 수동 fallback으로 부를 의미 판단 role은 [`workspace-context-maintainer.toml`](workspace-context-maintainer.toml)이다. Project root의 [`.codex/config.toml`](../../../../.codex/config.toml)은 이 하위 파일을 `workspace_context_maintainer` role로 발견하게 할 뿐 자동 session 시작, warm identity나 response-end dispatch를 보장하지 않는다. 자동 lifecycle은 별도의 persisted session bridge와 hook adapter가 맡는다.

## 사용자에게 보여야 하는 동작

1. 기존 Workspace에서 새 작업 session을 시작하면 명시적으로 선택된 Workspace의 bounded current를 한 번 읽고, 시작 상태를 한 번 맞춘다.
2. 같은 session의 후속 response에서는 이미 얻은 이해를 이어 쓰고 넓은 recovery를 반복하지 않는다.
3. 모든 사용자 대상 Main response-end에서 durable 변화 여부를 점검한다.
4. 변화가 없으면 지속 Workspace Context write와 Maintain report를 모두 만들지 않는다.
5. 명확한 변화는 기존 Owner에 반영한다. 사소하면 조용히 끝내고, 중요하면 실제 반영 뒤 보고한다. 목표·source 권위·acceptance처럼 사람 판단이 필요한 ambiguity는 관련 write 전에 묻는다.
6. 최초 grounding 뒤 장시간 의미 판단 때문에 Main response를 기다리게 하지 않는다. 접수, 판단, write와 report 완료를 구별하며 실패·지연·stale을 `fresh`, `current` 또는 `completed`로 가장하지 않는다.

점검 cadence와 write·report cadence는 다르다. 매 response-end 점검한다는 이유로 Workspace에 heartbeat, no-change record 또는 machine status를 남기지 않는다. Host adapter가 순서·중복·실패를 구별하기 위해 쓰는 ignored runtime은 Context나 기록이 아니며 제거 가능해야 한다.

## 책임 배치

### Recover가 소유하는 최초 grounding 입력

새 Maintainer session은 explicit `workspace_id`로 기존 [`Recover`](../recover/) packet을 한 번 만든다. 이 호출은 active index를 읽지 않고 선택된 current, `output/index.md`와 Workspace가 선택한 Project context만 안전하게 읽는다. Workspace source·records 전체, output artifact 본문과 `verify.json`은 자동 grounding 입력이 아니다.

제품 Verify receipt의 snapshot이 `fresh`라는 사실은 선언된 제품 파일이 receipt와 같다는 뜻일 뿐, 사람용 current 의미가 실제 작업과 맞다는 뜻이 아니다.

### Workspace 생성·전환 비소유

Maintain은 explicit binding으로 선택된 한 Workspace 안의 의미 변화를 관리한다. 후속 Workspace를 만들거나 이전 Workspace의 의미를 옮기고, active index·host binding을 바꾸거나 Workspace 사이를 동기화하지 않는다. Project context에도 Project-wide 적용 후보를 자동 반영하지 않는다.

새 Workspace 생성과 전환은 [`생성·전환 canonical`](../../workspaces/CREATE-AND-TRANSITION.md)을 main과 별도 skill이 적용하는 책임이다. 같은 Main session을 이어 갈지 새 session으로 격리할지는 canonical이 요구하는 현재 binding·미처리 상태·successor 영향과 실제 host 능력을 main이 대조해 정한다. Maintain은 그 선택을 대신하지 않으며, 이전 session의 warm 이해, 설정 파일 변경이나 아직 반영 여부가 확정되지 않은 background event를 successor의 current·새 grounding 또는 전달 완료처럼 간주하지 않는다.

### Agent가 소유하는 의미 판단

같은 Maintainer agent session은 최초 packet으로 이해를 갖춘 뒤 각 response-end의 사용자 발화와 Main response를 이전 이해에 붙인다. 이미 그 입력에 제한된 실제 근거나 기존 Verify 결과가 포함돼 있으면 출처와 입증 범위를 함께 보존할 수 있지만, 누락된 repository diff·Git 상태·raw test log를 기본 수집하거나 제품 test·eval을 새로 실행하지 않는다. 다음은 자연어 맥락을 종합해야 하므로 agent 판단에 남는다.

- 새 사실이 이후 재진입에 남길 durable 변화인지
- `current/memory`, `current/state/index.md`, `records`, source provenance 또는 `output/index.md` 중 기존 의미 Owner가 어디인지
- 사용자 결정 전에는 쓸 수 없는 ambiguity인지
- 반영 뒤 사용자에게 알려야 할 정도로 중요한지

Agent는 제품 test를 대신 실행하거나 사람의 목표·acceptance·완료를 결정하지 않는다. 사용자 결정은 결정으로, Main의 완료·test 주장은 `Main이 보고한 상태`로 출처 강도를 보존한다. 실제 확인을 입력으로 받을 때만 무엇을 확인했고 무엇은 확인하지 못했는지도 함께 유지한다.

### 규칙 장치가 소유하는 side-effect 경계

Agent 결과는 `no_change`, `update`, `needs_user_decision` 중 하나인 structured decision으로 넘긴다. Maintain의 guarded apply는 의미가 맞는지 재판단하지 않고 다음을 결정적으로 검사한다.

따라서 read-only인 것은 의미 판단 agent의 도구 권한이지 Maintain 전체의 기능이 아니다. `update`가 명확하고 아래 검사를 통과하면 Maintainer 흐름이 별도 사용자 승인 없이 해당 Context Owner를 실제로 수정한다.

- decision과 실제 binding의 exact Workspace id
- exact schema와 outcome별 허용 side effect
- 기존 파일의 expected SHA-256 preimage
- Project root·Workspace root 경계, direct child, regular file와 symlink
- Markdown EOF newline, 줄 끝 공백과 로컬 링크
- 아래 allowlist 밖의 모든 write 거부

허용되는 Workspace 상대 경로는 다음뿐이다.

- `current/memory/` 바로 아래의 Markdown
- `current/state/index.md`
- `source/index.md`
- `output/index.md`
- 새로 만드는 `records/YYYY-MM-DD-NN-*.md`
- 기존 `records/README.md`

기존 record를 다시 쓰지 않는다. Raw source snapshot, 제품 코드·문서·test, `workspace.json`, `recover.json`, `verify.json`, `current/state/status.json`, `records/receipts/`, `workspaces/index.json`은 수정하지 않는다.

새 `current/memory/*.md` 주제를 만들 때는 같은 decision에서 `current/memory/index.md`도 갱신하고 새 문서로 가는 링크를 넣는다. Guard는 이 pair가 없는 proposal을 거부한다.

새 날짜별 record를 만들 때도 같은 decision에서 기존 `records/README.md`를 preimage와 함께 갱신하고 새 record 링크를 넣는다. Guard는 이 pair가 없는 proposal과 새 `records/README.md` 생성을 거부한다. 여러 파일의 실제 write는 하나의 atomic transaction이 아니므로 중간 실패·crash 때 pair가 항상 함께 남는다는 보장은 하지 않는다.

`no_change`와 `needs_user_decision`에는 write 권한이 없다. `update`도 모든 precondition과 실제 write가 성공한 뒤에만 `updated`가 된다. Stale target이나 일부 write 실패는 성공으로 바꾸지 않으며 실제로 바뀐 범위를 드러낸다.

## Decision contract

Decision은 다음 의미를 갖는다.

- `schema_version`: 현재 contract version
- `workspace_id`: 최초 binding과 같은 explicit id
- `outcome`: `no_change`, `update`, `needs_user_decision`
- `importance`: `none`, `quiet`, `important`
- `summary`: 판단 또는 실제 반영을 사람이 이해할 수 있는 짧은 설명
- `changes`: Workspace 상대 path, expected SHA-256, 전체 새 Markdown content와 이유
- `evidence`: 판단에 사용한 사용자 발화, Main의 보고, 이미 제공된 실제 확인과 각각의 출처·입증 범위
- `unresolved`: 아직 확인하지 못했거나 다음 판단에 남길 사항
- `question`: `needs_user_decision`에서 사용자에게 물을 한 가지 구체적 질문

결과별 조합은 고정한다.

- `no_change`: `importance=none`, changes 없음, question 없음
- `update`: `importance=quiet|important`, 하나 이상의 changes, question 없음
- `needs_user_decision`: `importance=important`, changes 없음, 비어 있지 않은 question

이 schema는 agent 판단을 코드로 대체하지 않는다. Outcome마다 어떤 부작용 권한이 있는지와 false success를 제한한다.

## Host-neutral 실행 순서

1. Host 또는 main이 Workspace id를 명시하고 Recover packet으로 새 Maintainer agent를 한 번 grounding한다.
2. Grounding이 성공하기 전에는 warm 또는 current를 주장하지 않는다. 실패하면 Main에 Workspace와 실패 범위를 드러낸다.
3. 같은 agent identity에 각 사용자 대상 Main response-end의 delta를 전달한다.
4. Agent가 decision을 만들면 guarded apply가 검증·적용한다.
5. No-change는 `context_status=no_change`로 이번 경계의 무변화만 나타내고 조용히 끝난다. 전체 Context freshness나 이전 실패 경계까지 current라고 주장하지 않는다. Quiet update도 report를 만들지 않는다. Important update는 실제 apply 성공 뒤에만 보고한다. Ambiguity는 zero-write 상태로 질문한다.
6. 새 Main session은 bounded grounding부터 다시 한다. 같은 Main session의 Workspace 전환은 생성·전환 canonical이 소유하며, 설정 변경만으로 자동 re-grounding됐다고 간주하지 않는다. 살아 있는 Main session에서 agent thread가 사라지면 disk cache로 warm 이해를 흉내 내지 않고 실패로 남긴다. 현재 Reference host adapter는 같은 outer session의 자동 re-grounding을 지원하거나 보장하지 않는다.

자동 lifecycle adapter가 없는 host에서는 main이 이 순서를 직접 수행할 수 있다. 이 수동 fallback은 Workspace 의미를 유지하지만 모든 response-end 자동 점검이나 Main 비차단을 증명하지 않는다.

## Reference Codex host adapter

Reference Project는 다음 교체 가능한 연결을 함께 제공한다.

- [`.codex/maintain.json`](../../../../.codex/maintain.json): host session을 묶을 explicit Workspace id. Active index를 암묵적 binding으로 사용하지 않는다.
- [`.codex/hooks.json`](../../../../.codex/hooks.json): `SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd` command routing. Hook trust와 실제 event 의미는 Codex host가 소유한다.
- [`codex_session.py`](codex_session.py): 최초에는 `codex exec`로 read-only semantic thread를 시작하고, 후속 response-end에는 검증한 같은 thread id를 `codex exec resume`으로 재사용한다. Nested thread에서는 project hook을 꺼 재귀 실행을 막는다.
- [`host_adapter.py`](host_adapter.py): stable hook payload만 받아 session별 ignored runtime에 binding·event·실제 effect를 격리한다. Transcript 파일 형식은 읽지 않는다.

`SessionStart`만 bounded grounding 완료를 기다린다. Grounding이 실패하거나 사람 결정이 필요하면 session state를 grounded로 commit하지 않고 그 사실을 Main과 사용자 표면에 돌려보낸다.

`UserPromptSubmit`은 stable `turn_id`와 prompt를 짧게 보존하고, 이전 important update·ambiguity·failure 또는 아직 끝나지 않은 accepted boundary가 있으면 다음 Main model request와 사용자 UI에 전달한다. 일반 pending은 worker를 다시 시작하되 완료·fresh·current로 표시하지 않는다. 이전 semantic resume 또는 guarded apply가 실패해 thread와 Context의 관계가 불확실하면 뒤 event를 같은 session에서 재시작하지 않고 pending으로 남기며 새 Main session의 bounded grounding을 요구한다. Immediate 별도 chat message를 생성하는 장치가 아니므로, background 결과는 다음 prompt가 들어올 때 보인다.

`Stop` handler는 stable `turn_id`와 `last_assistant_message`를 session별 event로 먼저 확정하고 detached worker를 시작한 뒤 끝난다. 장시간 agent 판단과 write를 기다리지 않는다. Worker는 같은 semantic thread를 resume하고 guarded apply를 거친다. Effect가 이미 확정된 ordinary duplicate는 다시 적용하지 않는다. Prompt·response pairing 이전 실패는 failure로 남기고 뒤의 정상 event 처리를 막지 않는다. Semantic resume 또는 guarded apply가 실패하면 그 event는 뒤 event를 막는 failure가 되고, 뒤 event는 적용되지 않은 pending으로 남는다. Semantic resume·apply 뒤 effect 기록 전 hard crash의 strict effect-once는 주장하지 않는다.

Failure ordering 필드가 생기기 전 schema v1 runtime의 `failed` effect는 원래 실패 단계를 구분할 수 없으므로 fail-closed로 뒤 event를 막는다. 새 Main session의 canonical grounding으로 돌아가는 안전한 과잉 정지이며, 새 runtime의 pairing 실패에는 명시적으로 nonblocking을 기록한다.

Runtime 기본 위치는 ignored `.codex/maintain-runtime/`이다. Project 내부의 absolute lexical descendant만 허용하고 기존 symlink component를 거부한다. Warm thread binding과 delivery truth만 소유하며 Workspace 의미를 복제하지 않는다. 폴더를 지우면 자동 session continuity만 사라지고, 다음 session은 canonical에서 다시 grounding한다.

현재 process lock은 POSIX `fcntl`을 사용한다. 이 Reference host adapter는 non-POSIX portability를 주장하지 않는다.

`codex` 실행 경로가 symlink이고 실제 binary 옆에 `codex-code-mode-host`가 있으면 semantic bridge는 실제 binary 경로를 사용한다. Host가 sibling tool을 실행 파일의 겉보기 경로에서 찾는 설치에서는 이 해소가 read-only Owner inspection을 가능하게 하며, sibling host가 없으면 임의 경로를 추정하지 않고 원래 실행 실패를 그대로 드러낸다.

## Codex host proof ceiling

Codex의 command hook은 `SessionStart`와 `Stop` 경계를 제공하지만 등록된 agent role을 직접 실행하지 않는다. Background hook 완료는 새 turn을 시작하지 않고 session 종료 시 취소될 수 있으므로, Reference는 async hook 안에서 장시간 agent를 실행하지 않고 빠른 sync enqueue 뒤 별도 process에서 persisted thread를 resume한다.

자동 adapter를 연결하려면 실제 Codex host에서 다음을 먼저 확인한다.

- 새 session당 bounded grounding 1회
- 후속 turn에서 같은 agent identity 재사용
- 사용자 대상 Main response와 `Stop`의 실제 관계
- response-end의 빠른 접수 뒤 Main 비차단
- 순서 역전·중복·종료 중 누락과 session 간 격리
- important report와 ambiguity 질문이 다음 prompt에서 도달하는 실제 사용자 표면 및 그 지연이 허용되는지
- semantic resume 또는 guarded apply가 실패한 뒤 후속 boundary가 최신 Context인 것처럼 적용되지 않는지

이 확인 전에는 role 등록과 unit test만으로 automatic Maintain이나 actual acceptance를 주장하지 않는다.

## 소유하지 않는 것

Maintain은 다음을 수행하거나 결정하지 않는다.

- Project 제품 코드·제품 문서·제품 test 수정
- 제품 검증 실행, Verify receipt 또는 machine status 생성·수정·삭제
- active Workspace 선택·변경
- 다른 Workspace 생성·수정, Workspace 사이의 계승·동기화
- Project context 후보의 자동 승격·반영
- 사용자 대신 목표·source 권위·설계 기준·acceptance·완료 결정
- 파일 stage, commit, push 또는 외부 쓰기
- no-change heartbeat나 지속 warm cache 생성

허용 범위 밖의 변화가 필요해 보이면 필요와 근거를 `unresolved`로 돌려보낸다.

## 교체와 제거

Maintain의 의미 기준은 agent prompt, decision schema나 hook state에 있지 않다. Adapter를 제거하거나 사람·다른 AI·다른 host로 교체해도 이 README에서 Work·Workspace canonical을 적용하면 같은 책임을 수동으로 수행할 수 있다. Runtime state를 지워도 Workspace Context가 사라지거나 의미가 바뀌지 않아야 한다.
