# Context continuity maintenance memory

마지막 갱신: `2026-08-18`

## 목표

Main과 사용자의 작업 흐름은 빠르게 유지하면서, 다음 세션이 낡은 `current`나 무관한 records 때문에 잘못 출발하지 않도록 지속 context의 freshness와 handoff 품질을 관리한다. 세션형 Maintainer가 작업을 함께 이해하고 같은 task·Workspace·worktree 동안 그 이해를 유지하며, 매 사용자 대상 Main 응답 종료에는 직전 처리 이후의 delta만 점검해 durable 변화가 있을 때만 좁게 갱신한다.

속도는 hook 실행 시간만 짧다는 뜻이 아니다. 첫 grounding 뒤에는 Main이 Maintain 완료를 기다리지 않고, Maintainer도 매번 전체 history·records·repository를 다시 읽지 않도록 이미 얻은 이해를 재사용해야 한다.

## 사용자 우선순위

- 가장 큰 우려는 **C와 E**다. C는 `current/records`가 깨지면 Recover와 handoff도 함께 무너지는 기반 신뢰 문제이고, E는 다른 세션이 들어와 작업을 이어 갈 수 있어야 한다는 continuity 문제다.
- Recover는 E를 일부 돕지만 C를 대신하지 않는다. Recover는 선택된 current를 충실히 읽으므로, `Maintain → trustworthy current → Recover → 다음 세션`에서 freshness가 먼저다.
- 재조사는 허용할 수 있지만 짧고 bounded해야 한다. 같은 세션에서 이미 이해한 내용을 매 응답마다 다시 학습하는 것은 빠른 운영이 아니다.
- Verify에 test가 계속 쌓이거나 Main이 이미 수행한 검증을 다시 맡아 관심사가 커지면 안 된다. Verify는 나중에 다시 볼 가치가 있는 이미 수행된 확인만 보존한다.

## 역할과 소유권 경계

- **Main/work**는 실제 변경, 제품 판단과 direct test·eval·수동 확인을 수행한다.
- **Recover**는 명시 Workspace의 선택된 current·output·Project context와 legacy 검증 연결을 read-only로 복구한다. Context 의미나 freshness를 고치지 않는다.
- **Maintain**은 Main 작업 세션 동안 선택한 Workspace를 이해하고 response-end마다 durable 의미 변화만 기존 Context Owner에 반영한다. Workspace 선택, 제품 canonical, acceptance와 commit을 대신 결정하지 않는다.
- **Verify**는 다른 주체가 이미 수행한 확인의 결과·재접근 위치·미검증 범위를 append-only evidence로 기록한다. 제품 명령 실행, 충분성 판단, machine status 전이와 acceptance를 소유하지 않는다.
- **Harness validation**은 위 runtime의 schema·path·호환·crash 방어를 검사한다. 일상 제품 작업의 별도 검증 단계가 아니다.
- 재사용 가능한 계약·runtime·semantic runner·writer·test는 `reference-project/`가 소유한다. Root는 Workspace 005 선택과 hook·agent 발견에 필요한 얇은 연결 설정만 소유한다.

Global `ai-system_*` reference는 이 소유권 응집, 사람용 진입, 독립 판단과 제거 가능성을 감사하는 렌즈다. 이번 Workspace의 목표나 별도 산출물이 아니며 global 파일을 수정하지 않는다.

## 세션 시작과 지속 이해

- Main 작업 세션마다 세션 전용 Maintainer 하나가 생긴다.
- 기존 Workspace의 새 세션은 첫 작업 전에 Workspace README와 current index가 선택한 필요한 current만 bounded grounding한다. 과거 이유가 실제로 필요할 때만 관련 record나 Project canonical을 추가로 읽는다.
- 초기 grounding 뒤에는 목표·현재 상태·다음 행동을 한 번 짧게 보여 Main과 사용자가 시작점을 맞춘다.
- 새 Workspace는 미리 읽을 내용이 없다. Maintainer는 세션 대화를 따라가지만, identity·goal·Owner와 사람용 entrypoint가 형성되기 전에는 지속 write를 하지 않는다.
- 같은 conversation task·Workspace·worktree에서는 같은 warm Maintainer thread가 이해를 유지한다. Main compaction만으로 초기화하거나 전체 문서를 다시 읽지 않는다.
- 새 Main 작업 세션에서는 새 Maintainer가 외부 canonical과 실제 상태에서 다시 grounding한다. 이전 agent의 내부 기억을 세션 사이 durable truth로 사용하지 않는다.

## Response-end 판단·쓰기·보고

- 매 사용자 대상 Main 응답 종료를 활동 시점으로 삼는다. Maintainer나 다른 subagent의 내부 응답은 새 trigger가 아니다.
- Hook이 user·assistant delta와 관련 변경 경로·test/Git 결과의 좁은 evidence를 durable capture한 뒤 detached worker가 semantic 판단과 write를 수행한다. 초기 grounding 뒤 Main은 그 완료를 기다리지 않는다.
- Durable 변화가 없으면 아무것도 쓰지 않고 보고도 하지 않는다.
- 명확한 durable 변화는 `current`, 필요한 날짜별 `records`, source provenance/index, `output/index` 중 올바른 기존 Owner 한 곳에 반영한다. 같은 사실을 여러 층에 반복하지 않는다.
- 사소하고 명확한 반영은 조용히 처리한다. 사용자가 알아야 할 중요한 명확 반영은 먼저 수정하고 짧게 결과를 보고한다.
- 의미·Owner·장기성·사용자 의도가 애매하면 추측해 쓰지 않고 질문한다. 해당 반영만 보류하며 관련 없는 Main 작업은 계속한다.
- Background worker가 새 UI turn을 직접 만들 수 없으므로 중요한 결과와 질문은 다음 `UserPromptSubmit` safe point에서 bounded notice로 Main에 전달한다. `needs_decision`은 화면에 전달됐다는 이유로 해결되지 않고, 뒤 응답의 의미가 그 질문을 실제로 답하거나 대체할 때만 해소한다.

## Freshness와 복구 기준

- Response event와 processing checkpoint는 Workspace Context가 아닌 ignored runtime state다. No-change도 완료 cursor를 전진하지만, 실패는 완료로 가장하지 않고 같은 event를 replay할 수 있어야 한다.
- Queue와 checkpoint는 session별로 격리하되, 새 세션의 grounding·write는 그보다 먼저 시작한 세션의 freshness와 보고를 확인한다. 더 나중에 생긴 세션 때문에 과거 세션이 역으로 막히면 안 된다.
- 한 worker는 한 response event만 처리하고, 남은 durable work에는 successor wake를 남긴다. Capture와 worker 종료가 겹쳐도 새 queue generation을 놓치지 않아야 한다.
- 일시적 실패와 Maintainer restart는 retry·replay·canonical rebootstrap으로 먼저 조용히 복구한다. ordinary background lag나 살아 있는 lease만으로 경고하지 않는다.
- Processor 반복 실패, content conflict, malformed checkpoint·session state, 확정된 sequence gap처럼 자동 복구 뒤에도 freshness를 세울 수 없을 때만 짧게 경고한다.
- 누락 Stop이 실제 higher sequence로 확정된 gap은 자동으로 건너뛰지 않는다. 사용자 승인, 정확한 session·expected sequence와 bounded provenance를 받은 명시적 repair만 cursor를 전진시킨다.
- Semantic ambiguity는 runtime 실패가 아니므로 retry로 미루지 않는다.

## Guarded write 기준

- Agent decision은 곧바로 파일 권한이 아니다. Event identity와 baseline hash를 가진 durable intent를 먼저 남기고 deterministic writer가 Workspace-relative allowlist, symlink·Markdown link, latest baseline을 검사한다.
- 모든 Main session은 Workspace 하나의 writer lock·journal·completion marker를 공유한다. 서로 다른 session이 같은 Context를 stale baseline으로 덮어쓰면 안 된다.
- Multi-file write는 stage·journal·replace와 directory sync를 거친다. Crash 뒤에는 exact transaction marker와 journal로 이미 적용된 판단을 재실행 없이 reconcile하거나 안전하게 재시도한다.
- Write 뒤 checkpoint 전 crash, checkpoint 뒤 intent·marker cleanup 전 crash 모두 같은 event를 중복 의미 판단하거나 다른 session의 write를 잃지 않게 해야 한다.
- Target이 판단 중 바뀌어 baseline이 stale하면 옛 intent를 영구 replay하지 않는다. Warm state를 invalidation하고 최신 canonical에서 다시 grounding·판단한다.

## Verify와 Recover 호환 기준

- Verify evidence는 관찰 시각, producer, subject, 실제 method, `pass|fail|partial` outcome, 구체 결과, source reference와 미검증 범위를 입력받는다.
- 세 outcome은 모두 기록 성공 시 CLI exit `0`일 수 있다. 이는 evidence가 append-only receipt로 보존됐다는 뜻이지 제품 성공이나 완료가 아니다.
- 새 recorder는 `records/receipts/verify/evidence-*.json`만 추가하며 제품 명령, `verify.json`, legacy `verify-*.json`, `current/state/status.json`, `recover.json`을 읽거나 바꾸지 않는다.
- 과거 Verify receipt와 status는 migration하지 않고 Recover의 읽기 호환을 보존한다. 새 evidence는 legacy 제품 검증 cursor로 자동 승격하지 않는다.
- `apply-context-harness`는 target canonical과 사용자 변경을 먼저 고정하고, Reference의 Maintain 실행 연결과 축소 Verify를 이식하되 실제 fresh hook·warm session을 실행하지 않았다면 증명했다고 쓰지 않는다.

## 증명 상한

Reference 코드와 root 연결 설정은 구현됐고, 이전 root Observe runtime은 active 경로에서 제거됐다. Fake semantic process와 임시 filesystem을 사용한 단위·통합 검사는 session pairing·격리, grounding·warm resume, forming no-write, guarded multi-owner write, crash replay, ambiguity·report 전달, legacy Recover/Verify 호환을 폭넓게 다룬다.

Cross-session recovery wake, response replay conflict 차단, checkpoint가 이미 포함한 raw residue cleanup과 incomplete capture residue의 비차단·선별 경고를 포함한 Maintain test `165/165`, Reference 전체 test `223/223`, 이식 skill helper test `7/7`이 통과했다. Python compile, JSON·TOML parse, 두 hook 설정의 8개 shell command 문법·동기 실행 조건과 root·Reference status 진입도 확인했다. 실제 nested `codex exec`가 Workspace를 읽고 같은 thread를 resume하는 동작, fresh Codex host의 hook trust·session 시작, 실제 background process와 UI notice 전달, semantic 문서 품질은 live acceptance 전까지 미검증이다. 전달 evidence가 없는 외부 branch·worktree 전환을 자동 감지하는 별도 fingerprint도 이번 구현에 넣지 않았다. 정적 설정과 fake-process test를 이 범위의 증거로 승격하지 않는다.
