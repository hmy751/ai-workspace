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
- Live Reference가 요구하는 root routing과 `common/current/guidance` 물리 layer를 구성할 때 어떤 주제는 기존 Owner에 남기고, 어떤 주제는 승인된 범위 안에서 Project context로 옮길 것인가.
- 기존 context·package·instruction·도구 설정과 어떤 물리·의미 충돌이 있는가.

### 첫 Workspace

- 실제 작업 장면, 목표, 지속 제약, 빠른 상태와 다음 행동은 무엇인가.
- 어떤 원문·snapshot·provenance를 source로 선택하고 무엇을 제외할 것인가.
- Goal을 위해 선택한 산출물과 실제 canonical은 어디인가.
- 제품 검증 claim과 기준, 실행 입력, runtime·cwd·timeout·cache 의미는 무엇인가.

### Reference 책임 적응

- 각 책임의 live Owner와 파일을 target에 그대로 둘지, target 구조에 맞춰 적응할지, 제외할지 판단한다.
- [Live Reference skill 색인](../../../../reference-project/.agents/skills/README.md)에서 각 repo-local skill과 필요한 공통 기준·도구별 연결을 확인하고 아래 기준으로 설치·적응·제외를 정한다. 첫 Workspace는 이식 책임이 직접 만들며 아직 설치되지 않은 운영 skill을 중첩 호출하지 않는다.
- Tool-specific Maintain 연결과 Project 설정은 target의 기존 role·설정 Owner를 먼저 확인한다. 수동 role, [session binding·lifecycle canonical](../../../../reference-project/context/work/harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md), lifecycle hook, schema v2 explicit admission config, session별 activation wrapper와 runtime ignore를 하나의 Maintain 내부 관계로 설치·적응·제외하고, role 등록만으로 automatic lifecycle을 주장하지 않는다. Project 공통 Workspace id, active index나 대화 의미로 새 session을 자동 binding하지 않는다. Schema v1 설치를 올릴 때는 legacy session state를 보존하는 v2 adapter를 먼저 배치한 뒤 config를 v2로 바꾸며 runtime을 일괄 삭제·retarget하지 않는다. Project-local Codex hook은 target root의 Codex task에서 hook review/trust, 사용자가 선택한 session의 explicit activation과 같은 binding generation의 runtime event receipt가 확인되기 전까지 `activation_pending`으로 둔다. Unbound 새 session은 정상 no-op이다. 일부 또는 전체 adapter를 등록하지 않으면 canonical 계약을 main이 수행하는 fallback과 proof ceiling을 남긴다.
- Reference sample의 제품·Workspace 내용과 과거 receipt는 payload에서 제외한다.

## Repo-local skills와 공통 기준

현재 Reference skill 색인은 `create-context-workspace`, `update-project-context`, `work-discussion`, `reconsider-work`, `work-artifact-briefing`, `explanation-recovery`를 안내한다. 이 목록을 고정 payload로 삼지 않고 호출 시점의 색인과 각 `SKILL.md`·호출 설정에서 실제 책임·입력·연결을 확인한다. Spec·Ticket의 내용과 유지 방식은 live Workspace canonical이, 생성·Project 맥락 갱신은 각각의 canonical이 소유한다. 이식 절차에서 네 Ticket 구성이나 skill별 호출 규칙을 다시 정의하지 않는다.

- **대상별 선택:** 각 skill의 원본·지원 파일·호출 설정, 공통 `context/project/guidance/explanation-and-evidence-criteria.md`, guidance 색인, tool별 discovery 연결과 root routing을 dry-run manifest에 `install/adapt/exclude`로 구분한다. 이름이 달라도 같은 책임을 맡는 target Owner와 비교하고, 제외할 때는 그 이유와 필요한 기존 canonical·fallback을 남긴다.
- **충돌 보호와 연결:** `.agents/skills/<name>/`의 전체 파일, target이 사용하는 `.claude/skills/<name>`·`.codex/skills/<name>` 같은 연결 경로, 공통 기준과 색인을 exact path로 확인한다. Clean·ignored 파일과 ancestor의 kind, 기존 symlink 목적지도 직접 확인하며 동명 경로를 통째로 덮어쓰지 않는다. Live source의 원본 관계와 호출 설정을 보존하되 도구별 상대 연결은 target 배치에서 해석해 같은 원본으로 이어지는지 확인한다. 도구가 지원하지 않는 연결을 기계적으로 설치하지 않는다.
- **공통 기준의 병합:** 기존 guidance README의 경계와 다른 항목을 유지하며 필요한 본문·consumer 링크를 좁게 병합한다. Reference의 색인으로 target 색인 전체를 교체하지 않는다. 적용·비적용·재검토·제거 조건과 실제 consumer는 live 기준을 따르며 모든 응답·Recover의 기본 입력으로 확대하지 않는다. 기준 경로를 적응하거나 skill을 제외하면 남는 consumer와 색인을 함께 맞춘다.
- **실제 유지 경로:** 설치한 skill에서 target의 Spec·Ticket·Main·Maintain 계약을 찾을 수 있게 연결한다. Workspace 생성과 Project-wide 문서 관리는 각각의 Owner에 남긴다. Bound·unbound·수동 fallback에서 누가 문서를 실제로 갱신하는지는 target Maintain 계약을 따르며, skill 설치를 session activation이나 문서 전달 완료로 취급하지 않는다.

정적 설치 확인은 frontmatter·호출 설정·일반 파일·상대 연결·canonical과 공통 기준 접근점까지다. 실제 host가 skill을 발견하고 정해진 방식으로 호출했는지, 결과가 Main을 거쳐 유지 경로에 전달되고 문서 의존 실행 전에 반영됐는지는 별도 관찰이다. 하나의 성공을 다른 skill·도구·Maintain binding의 증명으로 확대하지 않는다.

## 기존 문서의 전환

이식 범위에 들어온 기존 문서는 현재 역할과 내용을 보고 처리한다. 계속 쓰는 제품 상세 정본과 이번 이식으로 대체되는 이전 요약·운영 문서를 같은 보존 대상으로 취급하지 않는다. 생성 주체나 파일 나이만으로 유지·제거를 결정하지 않으며, 사용자 변경과 남아 있는 고유한 의미를 먼저 대조한다.

대체되는 문서의 유효한 내용은 현재 책임에 맞는 위치에 반영하고, 기존 파일의 이동·통합·제거와 영향받는 링크·소비 경로를 함께 처리한다. 승인된 이식 안에서 필요한 문서 전환은 이식의 일부다. 독립된 제품 정본의 이동, 사용자 변경과의 충돌 또는 승인 범위가 불명확한 선택만 따로 확인한다. 이 판단을 관련 없는 상세 문서 전체 정비로 확대하지 않는다.

기존 경로를 유지하려면 계속 맡는 현재 책임이나 실제 호환 필요가 있어야 한다. 새 문서를 만든 뒤 원문에 과거 문서라는 안내만 붙여 같은 위치에 남기는 것은 전환 완료 근거가 아니다. 과거 원문은 다시 판단할 필요가 있을 때 적절한 source·record 또는 기존 Git 이력에 보존하며, 모든 대체 문서의 별도 복사본을 의무적으로 만들지 않는다.

완료 검토는 새 문서뿐 아니라 전환 대상의 유효한 내용이 빠지지 않았는지, 기존 파일의 실제 배치와 남은 참조가 처리 이유에 맞는지도 대조한다. 내용 반영 없이 파일만 제거하거나, 새 구조와 대체된 구조를 이유 없이 함께 남기면 미완성이다.

### 승인된 주제별 Owner 이동

사용자가 특정 주제의 Owner를 Project context로 옮기도록 승인했다면 그 범위는 이식 또는 후속 갱신의 실제 전환 대상이다. 이미 받은 승인을 다시 묻지 않으며, 다른 상세 문서 전체의 이동으로 확대하지 않는다.

- Ticket, Workspace, 회의나 source 묶음은 근거 경계이지 문서 책임이 아니다. 다음 작업이 찾을 지속 주제, 판단 질문, 수명과 갱신 Owner를 기준으로 본문을 구성한다.
- 지속 의미는 `common/`, 교체되는 구현·지원·proof 경계는 `current/`, 조건부 판단은 `guidance/`, 현재 답과 별도로 남길 중요한 선택 이유는 `decisions/`에 둔다. 서로 다른 책임·수명·갱신 Owner를 같은 근거 묶음이라는 이유로 합치지 않는다.
- 이동한 범위의 Project 문서는 현재 의미의 canonical임을 밝히고, 링크 없이도 그 의미와 경계를 설명한다. 링크는 구현 상세·원문·검증의 재대조 경로로 사용한다.
- 이전 canonical의 유효한 의미를 통합한 뒤 남은 역할을 구현 상세, 근거·역사 또는 호환 routing으로 좁히거나 target 규칙에 따라 이동·제거한다. 같은 현재 답의 active canonical을 둘 이상 남기지 않는다.
- 미정인 제품 선택은 열어 두고 확인된 나머지를 이동한다. Owner 이동을 새로운 제품 결정을 확정하는 것으로 바꾸지 않는다.
- Root와 layer index, 영향받는 live consumer를 새 authority에 맞춘다. 과거 Workspace 전체를 역동기화하지 않는다.

## Layered Project context 내용 충족

Owner 이동이 승인되지 않은 README·STATUS·`docs/`와 코드·테스트는 기존 상세 사실의 canonical로 유지한다. `context/project/`는 여러 Workspace가 반복해서 판단할 실제 Project 목적·현재 범위·구조·제약·채택 결정을 선별해 다시 서술한다. 승인된 주제별 이동과 이번 이식으로 역할이 바뀌는 문서는 위 전환 기준을 따른다. 상세 Owner 링크는 provenance와 재대조 경로이지 내용의 대체물이 아니다.

`context/project/`에는 다음 물리 경계를 만든다.

```text
context/project/
├── README.md
├── MAINTENANCE.md
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

`common/current/guidance` layer와 각 README는 생략하지 않는다. 특정 layer에 README 외 실제 본문이 없을 수는 있으며, 이때 README에 현재 없음, 확인한 상세 Owner와 새 항목을 만들 조건을 적는다. 파일 수를 줄이기 위해 독립된 내용을 overview나 다른 layer에 흡수하지 않는다. 기존 target의 flat Project context 문서도 현재 역할과 내용에 따라 전환하며, 평면 파일이라는 이유만으로 모두 이동하거나 보존하지 않는다.

각 실제 내용 문서에서 읽기 조건, 소유하는 주제 범위와 현재 authority, 구현·검증 상세 Owner, 갱신 책임, stale·재검토 신호를 찾을 수 있어야 한다. 한 문서에 보조 설명이 함께 있을 수 있지만 주 책임과 경로를 흐리거나 수명과 갱신 Owner가 다른 내용을 합치지 않는다.

내용의 보존·불확실성 표현·변경과 갱신 시점은 live [`Project 관리 계약`](../../../../reference-project/context/project/MAINTENANCE.md)을 읽고 target의 `context/project/MAINTENANCE.md`에 적응한다. Root README는 관리 계약의 역할과 읽는 시점을 연결한다. 관리 계약은 제품·domain 본문과 구분하며 이식·복원·갱신 주체가 직접 읽고, 일반 Recover 입력에는 추가하지 않는다. 이번 이식에서 무엇을 통합·이동·제거하고 어떻게 보존했는지는 적용 Workspace 기록이 소유한다. 이식 검토에서는 미정 부분의 존재를 이유로 원자료가 뒷받침하는 제품 목적·domain 의미까지 빠지지 않았는지, 남은 판단이 현재 확정된 규칙으로 바뀌지 않았는지를 함께 대조한다. 이 기준을 관리 skill에만 설치하고 target Project 계약에서 빠뜨리지 않는다.

구현 뒤 다음 순서로 내용 충족을 검토한다.

1. Root README에서 `common/current/guidance`와 `decisions`의 책임, layer README와 실제 내용 위치를 찾는다.
2. 상세 Owner 링크를 열지 않고 `common/`의 사용자 장면·목적·domain 의미·성공 기준과 범위 밖, `current/`의 현재 구현·지원·미지원 범위·실행 흐름·proof boundary, `guidance/`의 적용 여부와 관련 Decision을 설명한다.
3. 선택 문서가 맡은 질문에 답하지 못하고 상세 Owner 경로만 가리키거나, Ticket·기록 묶음의 목차만 재현하면 미완성으로 판정한다.
4. 그 뒤 상세 Owner를 열어 재서술한 사실이 원자료에 지지되고 현재·목표·미구현 상태를 섞지 않았는지 대조한다.
5. 첫 Workspace의 목표·검증 범위·빠른 상태가 Project 전체 사실로 승격되지 않았는지 확인한다.
6. 각 layer에 원자료가 지지하는 실제 내용이 있거나, README 외 본문이 없는 이유와 새 항목을 만들 조건이 명시됐는지 확인한다.
7. 첫 Workspace의 explicit Recover packet에 root README와 goal에 필요한 실제 layer 문서가 함께 선택됐는지 확인한다. Fresh reader가 선택 문서만으로 사용자 장면·목적, 현재·목표·미구현 차이, domain 관계, 지원·미지원 경계, proof ceiling과 적용할 판단 기준뿐 아니라 이동한 주제의 현재 canonical과 이전 문서의 남은 역할을 설명하지 못하면 미완성이다.

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
2. 선택한 각 repo-local skill·지원 파일·도구별 상대 연결, 공통 기준·guidance 색인과 같은 책임의 기존 Owner, root instruction route의 clean·ignored 파일을 helper receipt와 별도로 직접 확인한다.
3. Target ignore 규칙과 기존 clean canonical·설정 내용을 대조한다.
4. Preflight 변경과 payload의 교집합을 계산한다.
5. 교집합이 없으면 exact addition과 좁은 patch로 진행한다.
6. 교집합이나 Owner 충돌이 있으면 additive routing 가능성을 확인하고 의미 선택을 사용자에게 돌려보낸다.

기존 `context/`, instruction과 tool config는 빈 설치 자리가 아니다. Directory replace, broad recursive copy, 역할·내용·사용자 변경을 대조하지 않은 일괄 이동·삭제와 broad staging을 하지 않는다. 임시 preflight receipt를 Workspace에 보존할 때는 바이트와 SHA-256을 유지한다.

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
| Repo-local skill·공통 기준 | 각 frontmatter·호출 설정, canonical·조건부 consumer link, 도구별 상대 연결·root routing, 기존 skill·guidance 보존 | 새 target-root session의 실제 발견·정해진 호출 방식·문서 유지 흐름 확인 필요 |
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
5. 각 repo-local skill·공통 기준·guidance 색인·도구별 연결과 root routing이 설치·적응·제외 중 무엇이며, 실제 발견·호출·문서 유지 흐름은 어디까지 확인됐는가.
6. Validation과 Product Verify가 어떤 실제 input closure·runtime에서 무엇을 확인했는가.
7. Project-local Maintain hook이 installed, activation_pending, activated, excluded 중 어디에 있고 default-unbound, session별 explicit activation, trust와 runtime receipt가 무엇으로 확인됐는가.
8. 무엇이 외부 환경과 사람 acceptance로 남아 있는가.
