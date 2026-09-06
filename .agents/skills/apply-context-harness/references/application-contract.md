# Context Harness 이식 판단 기준

이 문서는 live `reference-project/`를 기존 개발 Project에 적용할 때 target마다 다시 판단할 내용을 소유한다. Reference 실행 계약, target 사실과 과거 적용 이력을 여기에서 다시 설명하지 않는다.

## Owner 분리

- `reference-project/`: 현재 Project·Work·Workspace·Harness 책임, 실행 계약, tool adapter와 validation을 소유한다.
- `apply-context-harness`: live Reference를 찾고 target Owner와 충돌을 조사해 책임을 적응·검증·보고하는 절차를 소유한다.
- Target Project: 자신의 canonical, Workspace 내용, 제품 코드, 검증 명령과 acceptance를 소유한다.
- Application Workspace: target에 실제로 적용한 source commit, 선택·예외·증거와 proof ceiling을 소유한다.

Reference의 schema, status, 내부 경로와 호환 이력은 live canonical에서 읽는다. 이식 방법이 달라지지 않았다면 그 값의 변경만으로 이 skill을 수정하지 않는다.

## Target에서 다시 판단할 것

### Project와 Work Owner

- 여러 Workspace가 공유할 Project 목적·구조·제약·채택 결정의 상세 Owner는 어디인가.
- Live Reference가 요구하는 root routing과 `common/current/guidance` 물리 layer를 기존 Owner를 옮기지 않고 어떻게 구성할 것인가.
- 기존 context·package·instruction·도구 설정과 어떤 물리·의미 충돌이 있는가.

### 첫 Workspace

- 실제 작업 장면, 목표, 지속 제약, 빠른 상태와 다음 행동은 무엇인가.
- 어떤 원문·snapshot·provenance를 source로 선택하고 무엇을 제외할 것인가.
- Goal을 위해 선택한 산출물과 실제 canonical은 어디인가.
- 제품 검증 claim과 기준, 실행 입력, runtime·cwd·timeout·cache 의미는 무엇인가.

### Reference 책임 적응

- 각 책임의 live Owner와 파일을 target에 그대로 둘지, target 구조에 맞춰 적응할지, 제외할지 판단한다.
- Reference의 repo-local `create-context-workspace`, `update-project-context`와 각각의 root routing을 target 도구가 발견할 수 있는지, 기존 skill·instruction Owner와 충돌하는지 확인하고 설치·적응·제외를 정한다. 이름이 달라도 같은 책임을 맡는 기존 Project 관리 skill을 확인한다. 첫 Workspace는 이식 책임이 직접 만들며 아직 설치되지 않은 운영 skill을 중첩 호출하지 않는다. Project 맥락 갱신 skill은 target Project README의 관리 기준을 적용하고 Workspace Maintain과 독립된 호출 경로를 가진다.
- Tool-specific Maintain 연결과 Project 설정은 target의 기존 role·설정 Owner를 먼저 확인한다. 수동 role, [session binding·lifecycle canonical](../../../../reference-project/context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md), lifecycle hook, schema v2 explicit admission config, session별 activation wrapper와 runtime ignore를 하나의 Maintain 내부 관계로 설치·적응·제외하고, role 등록만으로 automatic lifecycle을 주장하지 않는다. Project 공통 Workspace id, active index나 대화 의미로 새 session을 자동 binding하지 않는다. Schema v1 설치를 올릴 때는 legacy session state를 보존하는 v2 adapter를 먼저 배치한 뒤 config를 v2로 바꾸며 runtime을 일괄 삭제·retarget하지 않는다. Project-local Codex hook은 target root의 Codex task에서 hook review/trust, 사용자가 선택한 session의 explicit activation과 같은 binding generation의 runtime event receipt가 확인되기 전까지 `activation_pending`으로 둔다. Unbound 새 session은 정상 no-op이다. 일부 또는 전체 adapter를 등록하지 않으면 canonical 계약을 main이 수행하는 fallback과 proof ceiling을 남긴다.
- Reference sample의 제품·Workspace 내용과 과거 receipt는 payload에서 제외한다.

## Layered Project context 내용 충족

기존 README·STATUS·`docs/`와 코드·테스트는 상세 사실의 canonical로 유지한다. `context/project/`는 이를 이동하거나 문단째 복제하지 않고, 여러 Workspace가 반복해서 판단할 실제 Project 목적·현재 범위·구조·제약·채택 결정을 선별해 다시 서술한다. 상세 Owner 링크는 provenance와 재대조 경로이지 내용의 대체물이 아니다.

`context/project/`에는 다음 물리 경계를 만든다.

```text
context/project/
├── README.md
├── common/
│   └── README.md
├── current/
│   └── README.md
├── guidance/
│   └── README.md
└── decisions/
    └── README.md
```

Root `README.md`는 세 책임 layer, 실제 내용 위치, 읽기 조건과 Owner 우선순위를 찾는 안정된 routing anchor다. Project 본문을 root의 평면 overview로 합치지 않는다. 첫 Workspace의 `recover.json`은 root README와 현재 goal의 판단을 바꾸는 실제 layer 문서를 이유와 함께 별도로 선택하며, 모든 layer를 자동으로 읽지 않는다.

- `common/`에는 여러 Work에 지속되는 제품·사용자·domain 의미와 Project-wide 제약을 둔다.
- `current/`에는 상세 Owner 변화에 맞춰 교체되는 현재 구현·지원·미지원 범위, 연결 구조와 proof boundary를 둔다.
- `guidance/`에는 특정 종류의 Work에서만 실제 반복 행동을 바꾸는 조건부 판단 기준을 둔다. 각 항목은 적용·비적용·재검토·제거 조건을 밝힌다.
- `decisions/`에는 중요한 선택의 이유·대안·재검토 신호를 둔다. 현재 세 layer의 답을 기본적으로 대신하지 않지만 문서가 현재 normative Owner임을 명시한 예외는 허용한다.

`common/current/guidance` layer와 각 README는 생략하지 않는다. 특정 layer에 README 외 실제 본문이 없을 수는 있으며, 이때 README에 현재 없음, 확인한 상세 Owner와 새 항목을 만들 조건을 적는다. 파일 수를 줄이기 위해 독립된 내용을 overview나 다른 layer에 흡수하지 않는다. 기존 target의 flat Project context 문서는 상세 canonical로 보존할지, 승인받아 Owner를 이동할지 먼저 판정하고 자동 이동하지 않는다.

각 실제 내용 문서에서 읽기 조건, 현재 authority와 상세 Owner, 갱신 책임, stale·재검토 신호를 찾을 수 있어야 한다. 한 문서에 보조 설명이 함께 있을 수 있지만 주 책임과 경로를 흐리거나 수명과 갱신 Owner가 다른 내용을 합치지 않는다.

내용의 보존·불확실성 표현·변경과 갱신 시점은 live [`Project context 계약`](../../../../reference-project/context/project/README.md)을 target README에 적응한다. 이식 검토에서는 미정 부분의 존재를 이유로 원자료가 뒷받침하는 제품 목적·domain 의미까지 빠지지 않았는지, 남은 판단이 현재 확정된 규칙으로 바뀌지 않았는지를 함께 대조한다. 이 기준을 관리 skill에만 설치하고 target Project 계약에서 빠뜨리지 않는다.

구현 뒤 다음 순서로 내용 충족을 검토한다.

1. Root README에서 `common/current/guidance`와 `decisions`의 책임, layer README와 실제 내용 위치를 찾는다.
2. 상세 Owner 링크를 열지 않고 `common/`의 사용자 장면·목적·domain 의미·성공 기준과 범위 밖, `current/`의 현재 구현·지원·미지원 범위·실행 흐름·proof boundary, `guidance/`의 적용 여부와 관련 Decision을 설명한다.
3. 선택 문서가 맡은 질문에 답하지 못하고 상세 Owner 경로만 가리키면 미완성으로 판정한다.
4. 그 뒤 상세 Owner를 열어 재서술한 사실이 원자료에 지지되고 현재·목표·미구현 상태를 섞지 않았는지 대조한다.
5. 첫 Workspace의 목표·검증 범위·빠른 상태가 Project 전체 사실로 승격되지 않았는지 확인한다.
6. 각 layer에 원자료가 지지하는 실제 내용이 있거나, README 외 본문이 없는 이유와 새 항목을 만들 조건이 명시됐는지 확인한다.
7. 첫 Workspace의 explicit Recover packet에 root README와 goal에 필요한 실제 layer 문서가 함께 선택됐는지 확인한다. Fresh reader가 선택 문서만으로 사용자 장면·목적, 현재·목표·미구현 차이, domain 관계, 지원·미지원 경계, proof ceiling과 적용할 판단 기준을 설명하지 못하면 미완성이다.

이 검토는 문서 길이나 링크 수로 자동 판정하지 않는다. 짧아도 공통 판단을 닫으면 충분하고, 길어도 출처 안내와 Workspace 전용 내용뿐이면 불충분하다.

## 영향받는 live consumer reconciliation

Project 문서의 path·책임·authority를 새로 만들거나 크게 바꿀 때에는 producer만 검사하지 않고 영향을 받는 live consumer를 고정한다.

- id 없는 Recover가 선택하는 active/default Workspace
- Maintain runtime의 current generation에 explicit session-bound된 Workspace
- 이번 적용에서 명시적으로 생성·변경하는 Workspace

과거 generation, unbound session과 이미 소비 경로에서 내려온 역사 Workspace는 자동 갱신하지 않는다. Private turn·prompt·response payload는 열지 않고 binding 식별에 필요한 session metadata만 본다. 역사 Workspace 비동기화 원칙은 해당 Workspace가 live consumer에서 내려온 뒤에 적용한다.

각 live consumer는 Project 선택, 사람용 current의 경로·machine Owner 설명, output target을 현재 canonical에 맞게 reconcile하거나 successor 전환·deactivation으로 소비 경로에서 내린다. 모든 id에 `recover <workspace_id> --json`을 실행하고 active/default 경로는 id 없는 Recover도 실행한다. Recover 성공만으로 의미 정합성을 통과시키지 않고 fresh reader가 packet의 실제 내용과 target을 대조한다.

## Preflight와 충돌

`capture_target_state.py` receipt는 한 번의 관찰에서 target Git root, branch, HEAD, tracked·staged·untracked 변경, 파일 kind·size·hash와 instruction file을 고정한다.

이 receipt는 atomic snapshot, ignored file inventory, 저자·변경 이유나 Git 밖의 과거를 증명하지 않는다. 따라서 다음을 추가로 수행한다.

1. Dry-run payload의 exact path와 ancestor가 실제로 존재하는지 확인한다.
2. `.agents/skills/create-context-workspace/`, `.agents/skills/update-project-context/`와 같은 책임의 기존 skill, root instruction route의 clean 파일을 helper receipt와 별도로 직접 확인한다.
3. Target ignore 규칙과 기존 clean canonical·설정 내용을 대조한다.
4. Preflight 변경과 payload의 교집합을 계산한다.
5. 교집합이 없으면 exact addition과 좁은 patch로 진행한다.
6. 교집합이나 Owner 충돌이 있으면 additive routing 가능성을 확인하고 의미 선택을 사용자에게 돌려보낸다.

기존 `context/`, instruction과 tool config는 빈 설치 자리가 아니다. Directory replace, broad recursive copy, 자동 이동·삭제와 broad staging을 하지 않는다. 임시 preflight receipt를 Workspace에 보존할 때는 바이트와 SHA-256을 유지한다.

## 적용 표면 검사

Local link와 target 적응 잔재는 결정적 탐지와 의미 판정을 나눈다.

1. 변경한 Project Markdown과 각 live consumer의 loaded current·output index에서 local link의 source, line, label, lexical target과 resolved target을 수집한다.
2. Target이 존재하고 Project root 경계를 벗어나거나 symlink로 우회하지 않는지는 기계적으로 검사한다.
3. 존재하는 target이라도 label·주변 설명이 말하는 실제 Owner인지 fresh reviewer가 판정한다. 기계 존재성 pass를 semantic target pass로 바꾸지 않는다.
4. Source Reference의 sample Project 이름·Workspace id·sample path와 이번 변경에서 제거·rename한 Project 문서 path·basename을 dry-run manifest의 residue 목록으로 만든다.
5. 적용 표면을 fixed-string으로 검사하고, archive·source·records의 provenance hit처럼 의도한 보존은 exact allowlist와 이유를 남긴다. 나머지 hit는 generic 문구인지 target 미적응·stale 참조인지 판정해 해소한다.
6. 사람용 current가 `workspace.json`의 identity, `recover.json`의 선택, `verify.json`의 claim·basis·argv·evidence, `status.json`의 마지막 result·receipt cursor, Recover가 실행 시 계산하는 freshness와 `output/index.md`의 사람용 지도를 서로 바꿔 설명하지 않는지 확인한다.

## Evidence closure

Product Verify의 evidence는 중요해 보이는 파일 표본이 아니라 고정 실행이 실제로 읽는 입력을 설명해야 한다.

1. Root argv가 호출하는 package manager, task runner와 script를 펼친다.
2. Lockfile, workspace 선언, 공통 compiler·build 설정을 확인한다.
3. 실제 대상 package의 tracked source, manifest와 package-local 설정을 포함한다.
4. Runtime fixture, scenario, schema와 generated input을 확인한다.
5. 제외한 output, external state와 environment를 proof ceiling에 적는다.
6. Evidence를 실행 전에 snapshot한 뒤 같은 검증 사건에서 명령을 실행한다.

Directory-scoped command나 package script가 `evidence_paths` 밖 파일을 읽는데 일부 표본만 snapshot하는 상태를 허용하지 않는다. 완전한 closure를 구성할 수 없으면 argv를 좁히거나 claim과 proof ceiling을 선언 evidence 범위에 맞춰 낮춘다. Verify runtime과 receipt freshness는 undeclared input을 자동 발견하거나 현재 claim·argv 동일성을 증명하지 않는다.

Cache hit만으로 fresh pass를 선언하지 않는다. Force/no-cache option을 고정하거나 cached validation 한계를 밝힌다. 명령 통과와 evidence가 어떤 tree를 대표하는지는 별도로 설명한다.

## 검증 선택

| 변경 성격 | 최소 확인 | 확대 조건 |
| --- | --- | --- |
| 설명·링크·routing | 경로, link, 설정 parse, diff | 실행 의미나 discovery가 달라짐 |
| Repo-local Workspace 생성·Project 맥락 갱신 skill | 각 frontmatter, canonical link, root routing, 기존 skill 보존 | 새 target-root session의 discovery·implicit invocation 확인 필요 |
| Harness 코드·machine 계약·path 방어 | 관련 단위 테스트 | 공통 경계나 target 배치가 달라짐 |
| Target Harness 적응 | 전체 Harness tests와 ephemeral validation | 실패, source 변경 또는 proof 공백 |
| 상태 전환·인계 | Product Verify와 후속 Recover | Evidence closure나 runtime 불확실성 |
| Context 의미 변화 | 명시 Workspace Maintain과 main diff 검토 | 새 목표·canonical·acceptance 판단 필요 |
| Project path·책임·authority 변화 | 모든 live consumer의 explicit Recover, active fallback Recover, local link·residue 탐지와 fresh semantic review | consumer를 유지할 수 없거나 successor·deactivation 선택 필요 |
| Codex lifecycle hook | v2 default-unbound, installed/activation_pending/activated 상태 분리 | target task의 hook trust, explicit session activation 또는 같은 generation의 runtime event receipt 부재 |
| 신규 이식·사용자 파일 충돌 | 독립 review | P1/P2 또는 원자료 충돌 |

반복 개발 확인과 durable evidence를 구분한다. Harness validation은 임시 fixture의 회귀 검사이고, Harness test receipt는 target-specific 관리 장치 증거이며, Product Verify는 실제 Workspace 상태 전환 증거다. 서로를 대신하지 않는다.

신규 이식이나 큰 Project 내용 복원·책임 재구성에서는 구현자의 결론과 파일명 힌트를 답안으로 주지 않은 cold/blind review를 사용한다. Application Workspace record에는 reviewer brief, 허용 source와 revision, worker result 또는 patch/hash, finding, 수정 이유와 최종 disposition을 남긴다. Private 원문 전체를 불필요하게 복제하지 않고 이 narrative review를 machine Verify receipt로 취급하지 않는다. 낮은 위험의 설명·routing 변경에는 이 절차를 자동으로 붙이지 않는다.

## 자동화하지 않을 판단

- Canonical과 Owner 선택, Owner migration 승인
- Active Workspace 선택과 변경
- 사용자 파일 삭제·이동·승격
- 임의 검증 명령의 신뢰 승인. 단, 사용자가 명시적으로 요청한 target-local Codex hook trust는 target root task에서 hook definition을 확인하고 activation receipt를 남기는 별도 activation 단계로 처리할 수 있다.
- 일부 hash나 cache 결과를 전체 tree proof로 승격
- Pass 뒤 acceptance, completion, canonical 반영과 commit
- Concurrent Verify와 receipt/status transaction 보장

Helper는 관찰과 실행 증거만 결정적으로 만든다. 의미 선택과 최종 적용은 target 원자료, 사용자 권한과 실제 결과를 본 main이 맡는다.

## 최종 proof 문장

Target 사실로 다음을 답한다.

1. 어떤 Reference commit과 책임을 target에 그대로 적용·적응·제외했는가.
2. Recover가 실제로 무엇을 읽고 무엇을 제외했는가.
3. 어떤 live consumer를 확인했고 Project 선택·current·output을 reconcile, 전환 또는 deactivation했는가.
4. Local link·semantic target·residue와 machine Owner 설명을 어디까지 확인했는가.
5. Repo-local Workspace 생성·Project 맥락 갱신 skill 각각과 root routing이 설치·적응·제외 중 무엇이며, 실제 discovery는 어디까지 확인됐는가.
6. Validation과 Product Verify가 어떤 실제 input closure·runtime에서 무엇을 확인했는가.
7. Project-local Maintain hook이 installed, activation_pending, activated, excluded 중 어디에 있고 default-unbound, session별 explicit activation, trust와 runtime receipt가 무엇으로 확인됐는가.
8. 무엇이 외부 환경과 사람 acceptance로 남아 있는가.
