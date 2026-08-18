# Reference Maintain 구현과 actual host evidence

후속 재기준화: 이 기록의 구현·검증 사실은 유지하되, 아래 구조 문제의 현재 우선순위와 root 연결 기준은 [`record 06`](2026-08-19-06-purpose-rebaseline-and-remaining-scope.md)이 소유한다.

날짜: `2026-08-19`

상태: **Reference 구현·주요 실제 장면 확인 / root 연결 보류**

## 이 기록의 역할

[Acceptance와 첫 slice](2026-08-19-04-acceptance-and-first-implementation-slice.md)를 실제 `reference-project/` 코드와 현재 설치된 Codex host에서 어디까지 입증했는지 고정한다. 임시 host runtime이나 Codex transcript를 새 canonical로 삼지 않고, 재검토에 필요한 최소 식별자·관찰 결과와 아직 닫히지 않은 구조 문제만 남긴다.

## 구현한 책임

- `maintain/operation.py`는 explicit Workspace의 기존 Recover packet을 bootstrap으로 재사용하고, exact decision schema를 검증하며, Markdown Owner allowlist·symlink·preimage·로컬 링크·결과별 zero-write를 지키는 guarded apply를 제공한다.
- 새 memory topic은 같은 decision에서 `current/memory/index.md`를 갱신하고 새 문서 링크를 넣어야 한다. 일반 진입점에 보이지 않는 고아 memory는 guard가 거부한다.
- `maintain/codex_session.py`는 새 read-only Codex semantic thread를 한 번 만들고, 검증한 같은 thread id만 resume한다. Grounding은 supplied Recover packet만 사용하고 후속 판단은 explicit Workspace의 관련 Owner와 delta로 제한한다.
- `maintain/host_adapter.py`는 `.codex/maintain.json`의 explicit binding, session별 ignored runtime, stable `turn_id` pairing, 빠른 `Stop` enqueue, detached drain, thread restore, guarded apply와 다음 prompt notice 전달을 연결한다.
- `.codex/hooks.json`과 `.codex/hooks/maintain.py`가 `SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd` command hook을 연결한다. Root hook은 계속 비활성이다.
- CLI에는 `maintain bootstrap`과 `maintain apply`를 추가했다. 의미 판단을 Python 규칙으로 대체하지 않고 수동 fallback과 contract 검증에만 쓴다.
- `codex`가 앱 bundle binary의 symlink인 설치에서 sibling `codex-code-mode-host`를 찾지 못하는 실제 오류를 확인했다. Semantic bridge는 실제 binary 옆에 실행 가능한 sibling host가 있을 때만 symlink를 해소하고, 없으면 임의 경로를 추정하지 않는다.

독립 리뷰 뒤에는 `no_change` 결과를 전체 current 주장과 구별하고, 새 날짜별 record와 `records/README.md`를 같은 decision에서 연결하며, ignored runtime의 Project containment·기존 symlink 거부와 unresolved accepted event의 다음 prompt 표시를 보완했다. TOML role은 자동 실행 주체가 아니라 수동 fallback임을 분명히 했고, 적용 skill은 role·hook·binding·wrapper·runtime ignore를 각각 설치·적응·제외하도록 좁게 보완했다.

## 실제 Codex host에서 확인한 장면

환경은 `codex-cli 0.148.0-alpha.15`다. `reference-project/`는 상위 저장소 안의 하위 폴더라 자체 `.codex/`가 repo-local config layer로 발견되지 않으므로, 같은 bytes를 이미 trusted인 독립 임시 Git repo에 복제했다. Hook source는 이번 구현으로 검토한 파일만 trust bypass해 실행했으며, 이 flag를 Reference runtime에 저장하거나 production 기본값으로 만들지 않았다.

### 새 session과 warm reuse

- Outer thread `01a01592-ce34-7521-8ade-ef4320c11cf2`는 runtime key `8e650a808767f32261324a08be349ead71683118d20489cd675b9dc2a534486b` 하나와 semantic thread `01a01592-da9e-77a1-8bb1-663c7ed032f6` 하나를 만들었다.
- Semantic rollout에는 grounding task 1회와 response decision task 2회만 있다. Outer 두 번째 turn의 `SessionStart`는 `grounded_at`과 thread id를 바꾸지 않고 기존 session을 재사용했다.
- 두 `UserPromptSubmit`·`Stop` 쌍은 각각 동일한 stable `turn_id`와 실제 user prompt·Main response로 event가 됐다. 두 판단은 모두 `no_change`였고 Workspace tree diff와 notice가 없었다.

### response-end 비차단

- 첫 no-change outer task는 `00:52:33.262 KST`에 끝났고 effect는 약 `7.38초` 뒤 완료됐다.
- 두 번째 outer task는 `00:53:14.323 KST`에 끝났고 effect는 약 `10.07초` 뒤 완료됐다.
- Quiet update outer task는 `01:05:52.880 KST`에 끝났고 effect는 약 `28.96초` 뒤 완료됐다.

따라서 실제 `Stop`은 event를 먼저 durable enqueue한 뒤 Main 종료를 semantic 판단·write보다 먼저 돌려줬다. 이 관찰은 hard-crash reconciliation이나 모든 host 부하 조건을 입증하지 않는다.

### Ambiguity와 다음 prompt 전달

- 사용자가 canonical timeout을 `6000` 또는 `7000`밀리초 중 아직 고르지 않았다고 한 장면은 `needs_user_decision`·`important`, changes 없음으로 끝났다.
- Workspace tree diff는 없었고 runtime에는 “새 canonical 기본 timeout을 어느 값으로 정할까요?”라는 ambiguity notice가 생겼다.
- 다음 실제 outer turn의 model 입력에는 `Previous Workspace Maintain results requiring attention`과 그 질문이 들어갔고 Main이 사용자에게 미결정을 보고했다.

### 명확한 quiet update와 guard

- 별도 session에서 “향후 acceptance 결과 보고에 exact verify receipt path를 포함한다”는 final Workspace process 결정을 줬다.
- 실제 binary 경로 해소 뒤 semantic agent는 `current/memory/02-constraints.md`를 read-only로 읽고 SHA-256 `9b730ede6dcea1c9a5ba2982f9ca83ace1955468f095bff1dd76802d643a6ad6`을 제안했다.
- Guard는 임시 복제본의 그 파일 한 곳만 갱신했고 effect는 `updated`·`quiet`였다. Notice는 없었다. 이 변경은 host 검증용 임시 복제본에만 있었고 canonical Reference Workspace에는 반영하지 않았다.
- 그 전 시도에서 tool host를 못 찾아 기존 파일의 preimage가 `null`인 proposal이 나왔을 때 guard는 write 없이 실패 effect와 notice를 남겼다. 다음 실제 prompt는 “failed, not completed”를 Main 입력과 사용자 응답에 전달했다.

## Direct 검증

- Maintain suite: `40/40` 통과
- Recover suite: `31/31` 통과
- Reference 전체 suite: `93`개 중 기존 Verify descendant-timeout timing test 1건만 실패했고, 같은 test의 isolated retry는 통과했다. 이 test는 reset baseline에서도 동일하게 간헐 실패한 것으로 [record 02](2026-08-18-02-code-reset-baseline-and-prior-topology-evidence.md)에 분리돼 있다.
- Python compile, JSON·TOML parse, Markdown local link와 `git diff --check`는 통과했다. 적용 skill의 bundled `quick_validate.py`는 현재 Python에 PyYAML이 없어 시작하지 못했고, 같은 frontmatter key·name·description·unfinished placeholder 조건을 Ruby YAML parser로 확인해 통과했다.

## 아직 닫히지 않은 구조 문제

다음은 fake test나 위 실제 장면으로 완료됐다고 할 수 없으며 root 자동 연결을 막는다.

1. Prepared changes는 모두 preflight하지만 실제 file write는 순차 실행된다. 뒤 file의 stale·write failure·hard crash는 앞 file을 남길 수 있어 memory/record와 그 index pair도 원자적이지 않다. Semantic resume 또는 guarded apply 성공 뒤 effect marker를 쓰기 전 hard crash가 나면, 재실행이 이미 반영된 write와 이전 semantic turn을 어떻게 reconcile할지도 보장하지 않는다. 현재는 false success 대신 stale 또는 failure가 될 수 있지만 cross-file transaction과 strict effect-once는 아니다.
2. 앞 event가 실패한 뒤 같은 semantic thread로 뒤 event를 계속 처리할지, session을 quarantine하고 다시 grounding할지 정책이 확정되지 않았다.
3. 최초 grounding 자체가 `needs_user_decision`이면 grounded session을 commit하지 않는 것은 맞지만, 같은 outer session에서 사용자의 답을 받아 grounding을 이어 갈 경로가 없다.
4. `SessionEnd`의 hook output은 새 turn을 만들지 않는다. 종료 시점 notice와 background 결과가 이후 resume에서 사용자에게 확실히 전달되는지는 아직 actual acceptance가 없다.
5. Process lock은 POSIX `fcntl` 전제다. Non-POSIX portability는 구현하거나 주장하지 않았다.
6. Response-end event에는 user prompt와 Main response만 들어간다. 계약이 요구한 관련 diff·파일·Git 상태·test/eval 근거의 bounded snapshot을 자동 공급하지 않으므로 Main 응답에 드러나지 않은 실제 변화는 놓치고 설명만 근거로 오인할 수 있다.
7. Persisted semantic thread가 사라지면 같은 thread id의 resume 실패를 terminal failed effect로 남길 뿐, bounded bootstrap으로 다시 grounding해 semantic continuity를 복구하는 경로가 없다.
8. Existing Owner의 preimage를 write 직전에 다시 읽지만 hash 확인과 `replace`가 하나의 compare-and-swap은 아니다. 그 사이 Main이나 사용자가 쓴 내용을 background Maintain이 덮을 수 있다.

1·2·6·7·8은 독립 리뷰에서 transaction/reconciliation, evidence acquisition, re-grounding과 concurrent writer 정책을 함께 요구하는 큰 범위 문제로 분류됐다. 사용자가 정한 범위 gate에 따라 즉시 재설계하지 않았다. 3·4·5도 root 연결 전에 닫거나 명시적으로 수용해야 할 proof gap으로 유지한다.

## 현재 판단

Reference 구현은 `새 session → warm reuse → 모든 실제 Stop 접수 → no-change/ambiguity/quiet update/failure truth`의 핵심 세로 흐름을 실제 Codex에서 보였다. 독립 리뷰의 국소 지적은 반영했지만 위 구조 문제를 닫지 않은 상태에서 “automatic Maintain 완료”나 root 연결을 주장하지 않는다. Root의 빈 hook과 미등록 상태를 유지한다.
