# Maintain acceptance와 첫 구현 slice

날짜: `2026-08-19`

상태: **acceptance 확정 / 첫 구현 책임 선택**

후속 재기준화: broad evidence 입력과 mid-session 자동 re-grounding, root 연결 blocker의 현재 범위는 [`record 06`](2026-08-19-06-purpose-rebaseline-and-remaining-scope.md)이 대체한다. 아래 내용은 최초 구현 slice를 선택한 당시 acceptance로 보존한다.

## 이 기록의 역할

[Behavior contract](2026-08-18-01-clean-room-source-and-behavior-contract.md)의 여섯 장면을 현재 `reference-project/`, 글로벌 AI-system reference와 2026-08-19의 Codex host 계약에 붙여 직접 검증 가능한 acceptance로 바꾼다. 과거 005·006 구현 topology를 비교하거나 복원하는 기록이 아니다.

## 확인된 현재 기반과 host 제약

- 현재 Recover는 명시적 Workspace id를 주면 active index를 읽지 않고, 선택된 current·output index·Project context만 path·schema·symlink 검사를 거쳐 읽는다. 새 Maintain grounding은 이 책임을 복제하지 않고 재사용한다.
- 현재 Maintain은 자연스러운 의미 변화 경계에서 main이 부르는 agent/main 문서 계약뿐이다. 같은 agent session의 이해 재사용, 모든 Main response-end, 비차단 실행은 구현돼 있지 않다.
- Codex hook은 `SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd`를 제공하지만 현재 실행되는 handler는 command뿐이다. 등록된 agent를 hook이 직접 시작하는 `agent` handler는 실행되지 않는다.
- Background hook은 완료돼도 새 turn을 시작하지 않으며, session 종료 시 미완료 작업과 전달되지 않은 출력이 취소될 수 있다. 같은 event의 여러 command도 동시에 시작하므로 순서를 서로에게 의존할 수 없다.
- Project-scoped agent role 등록은 발견 경로이지 자동 실행·warm identity·response-end callback 보장이 아니다.

공식 host 근거는 [Codex Hooks](https://developers.openai.com/codex/hooks), [Codex Subagents](https://developers.openai.com/codex/subagents), [Codex App Server](https://developers.openai.com/codex/app-server), [Non-interactive mode](https://developers.openai.com/codex/noninteractive)다. 문서의 transcript 경로는 편의 입력일 뿐 stable interface가 아니므로 production 의미 입력으로 파싱하지 않는다.

## Acceptance matrix

### 1. 새 세션 grounding

- 시작: 기존 Workspace와 새 host session의 명시적으로 해소된 binding이 있다.
- 의미 판단: Maintainer가 목표·제약·현재 문제·불확실성·다음 행동의 충돌 여부를 종합한다.
- 결정적 경계: 기존 Recover가 identity·schema·root·regular file·symlink·읽기 allowlist를 검사한다. 제품 receipt의 snapshot freshness를 Context freshness로 해석하지 않는다.
- 관찰 결과: 필요한 시작 상태를 한 번만 드러내고 persistent write는 없다.
- 실패 truth: 필수 current가 없거나 grounding이 실패하면 `grounded`, `current`, `ready`로 표시하지 않는다.
- 검증: 제외 파일 marker가 grounding 입력에 없고, 명시적 id에서 active index를 읽지 않으며, 전후 Workspace bytes가 같은지 확인한다. 실제 host에서는 새 task의 최초 1회 표시를 확인한다.

### 2. 같은 세션의 warm 이해

- 시작: 최초 grounding이 성공한 같은 Maintainer session의 후속 Main turn이다.
- 의미 판단: 기존 이해에 이번 사용자 정정·작업·검증 delta만 붙이고 필요한 실제 Owner만 다시 본다.
- 결정적 경계: session과 Workspace binding을 암묵적으로 바꾸지 않는다. Write 직전 Owner hash가 달라지면 stale precondition으로 거부한다.
- 관찰 결과: 넓은 grounding을 반복하지 않으면서 이전 판단을 이어 간다. Agent session이 사라지면 warm이라고 가장하지 않고 다시 grounding한다.
- 검증: 여러 후속 check에서 Recover 호출은 최초 1회이고, agent restart 뒤에는 다시 1회인지 확인한다. 실제 host에서는 같은 agent identity 재사용을 확인한다.

### 3. 모든 Main response-end 점검

- 시작: grounding 뒤 사용자 대상 Main response가 끝났다.
- 의미 판단: 이번 경계에 durable 변화 후보가 있는지 매번 판별한다.
- 결정적 경계: host event 하나를 unique boundary 하나에 결합하고, 중복 전달은 중복 write·report를 만들지 않는다. Session별 처리를 격리한다.
- 관찰 결과: 대부분 조용하지만 각 완료 response는 semantic check를 거친다.
- 실패 truth: 누락된 boundary 뒤 최신 상태까지 checked라고 주장하지 않는다.
- 검증: 연속·중복·누락·두 session fake event에서 effect-once와 격리를 확인하고, 실제 host에서 `Stop`과 사용자 대상 response의 관계를 확인한다.

### 4. Durable 변화 없음

- 시작: response-end check는 정상 시작됐지만 새 지속 의미가 없다.
- 의미 판단: 일회성 대화·반복 확인·이미 반영된 사실과 durable 변화를 구분한다.
- 결정적 경계: `no_change` 결과에는 writer와 user reporter 권한이 없다. Check 실패를 `no_change`로 바꾸지 않는다.
- 관찰 결과: persistent diff와 Maintain report가 모두 없다.
- 검증: checker 호출은 1회이되 tree bytes, writer call과 report가 모두 0인지 확인한다.

### 5. 명확한 변화·중요도·ambiguity

- 시작: 사용자 정정, 실제 diff·파일, test·eval·Verify 결과와 그 입증 범위 중 관련 근거가 있다.
- 의미 판단: 모델이 durability, 기존 Owner, ambiguity와 사용자 보고 중요도를 판단한다.
- 결정적 경계: 규칙 장치가 explicit Workspace, write allowlist, path·symlink, stale preimage와 결과별 side-effect를 집행한다. 제품 코드, machine 계약, receipt·status, active index에는 쓰지 않는다.
- 사람 권한: 목표·source 권위·정책·설계 기준·acceptance·완료와 ambiguity 해결은 사람에게 남는다.
- 관찰 결과: 사소하고 명확하면 Owner 반영 뒤 조용히 끝난다. 중요하고 명확하면 실제 반영 성공 뒤 보고한다. 애매하면 관련 write 전에 질문한다.
- 실패 truth: 부분 또는 실패 write 뒤 `updated`를 보고하지 않고, report를 실제 반영보다 먼저 내지 않는다.
- 검증: `quiet update`, `important update`, `needs_user_decision`, restricted path, symlink, stale hash와 write 실패를 각각 직접 검사한다. 의미 품질은 별도 semantic eval과 실제 장면으로 확인한다.

### 6. 비차단·실패·지연·stale truth

- 시작: 최초 grounding 뒤 background check가 느리거나 crash·conflict·host 종료·report 전달 실패를 만난다.
- 의미 판단: 실패의 영향과 사람에게 필요한 선택을 설명한다.
- 결정적 경계: Main response delivery는 장시간 모델 판단을 기다리지 않는다. 접수·판단·write·report 성공을 구별하고 관찰한 단계 이상을 주장하지 않는다. Session별 실패를 격리한다.
- 관찰 결과: Main 응답이 먼저 보이고, 실패·지연은 가장 이른 신뢰 가능한 사람 표면에 Workspace, 영향 범위, 실제 write 여부와 열린 판단을 드러낸다.
- 실패 truth: background 접수만으로 `completed`나 `fresh`를 표시하지 않는다.
- 검증: 느린 checker, crash, stale conflict, 응답 직후 종료·재진입과 두 session 동시 진행을 fake runtime과 실제 host에서 나눠 확인한다.

## 선택한 책임 배치

### 기존 Workspace Context와 Recover

Workspace README와 `current/source/output/records`가 의미와 canonical을 계속 소유한다. Recover는 explicit selection과 bounded read를 그대로 소유한다. Maintain runtime이나 agent session은 새 Context Owner가 아니다.

### Maintain semantic core

같은 session의 agent가 durability·Owner·ambiguity·importance를 판단한다. 이 판단은 자연어 맥락을 종합해야 하므로 enum 규칙으로 대체하지 않는다. 대신 결과를 작은 decision contract로 넘겨 side effect 권한과 성공 truth를 제한한다.

### Guarded apply

Maintain 안의 결정적 하위 장치가 다음만 집행한다.

- decision의 Workspace id와 실제 binding 일치
- 기존 Context Owner 중 허용된 Markdown 경로만 수정
- raw source, 제품, machine 계약·status·receipt와 active index 거부
- direct-child·regular-file·symlink·Project root 경계 검사
- 기존 파일의 expected SHA-256과 실제 preimage 일치
- `no_change`와 `needs_user_decision`의 zero-write
- 실제 적용 성공 뒤에만 `updated`

이 장치는 의미상 무엇을 남길지 결정하지 않고, 모델이 지키겠다고 쓴 prompt를 deterministic 보장으로 과장하지 않게 한다.

### 교체 가능한 session/host adapter

Host adapter는 새 session에 Recover grounding을 한 번 연결하고, 같은 Maintainer agent identity에 response-end delta를 전달하며, Main 비차단과 사람 표면으로의 결과 전달을 맡는다. Workspace 의미나 semantic success를 소유하지 않는다. 제거하면 자동 cadence와 warm reuse는 사라지지만 Workspace와 수동 Maintain 계약은 그대로 남는다.

## 첫 구현 slice

첫 slice는 `explicit bootstrap → structured decision → guarded zero-write/update`다.

1. Maintain bootstrap은 기존 Recover를 explicit Workspace id로 한 번 호출한다.
2. Agent adapter는 bootstrap packet으로 grounding하고 후속 turn에는 같은 session 이해와 해당 response-end delta를 사용한다.
3. Decision contract는 `no_change`, `update`, `needs_user_decision`을 구별하고 evidence·unresolved·importance·변경 후보를 반환한다.
4. Guarded apply는 `no_change`와 ambiguity에 쓰기 권한을 주지 않고, 명확한 update도 allowlist와 current hash가 맞을 때만 적용한다.
5. Direct tests는 bounded bootstrap, no-change bytes 보존, 허용 update, restricted/symlink/stale 거부를 먼저 고정한다.

이 slice는 Python이 의미 판단을 흉내 내는 CLI가 아니다. Python은 Recover 재사용과 부작용 경계만 담당하고, 실제 의미 판단은 agent가 맡는다.

## 다음 host slice와 proof ceiling

Direct core가 통과한 뒤 `SessionStart → 동일 agent session → response-end` adapter를 붙인다. 현재 가장 단순한 실험 후보는 Codex의 persisted thread를 시작하고 후속 turn에서 resume하는 command bridge다. Hook 자체에 장시간 모델 실행을 맡기지 않고 response-end는 빠른 접수만 한 뒤 session별 worker가 처리해야 한다.

다음은 실제 host acceptance 전까지 완료로 쓰지 않는다.

- `SessionStart`가 사용자 경험에서 정확히 한 번 보이는지
- 같은 agent thread가 resume·compact와 후속 turn에서 유지되는지
- `Stop`이 사용자 대상 Main response와 1:1인지
- response-end 접수가 Main 응답을 실질적으로 지연하지 않는지
- 응답 직후 종료, 순서 역전과 두 session에서 누락이나 상호 차단이 없는지
- 중요 보고와 ambiguity 질문이 실제 사용자 표면에 언제 전달되는지

Root automatic Maintain은 이 actual acceptance 뒤에만 다시 연결한다.
