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
- Live Reference가 요구하는 Project common 진입 책임을 기존 Owner를 옮기지 않고 어떻게 구성할 것인가.
- 기존 context·package·instruction·도구 설정과 어떤 물리·의미 충돌이 있는가.

### 첫 Workspace

- 실제 작업 장면, 목표, 지속 제약, 빠른 상태와 다음 행동은 무엇인가.
- 어떤 원문·snapshot·provenance를 source로 선택하고 무엇을 제외할 것인가.
- Goal을 위해 선택한 산출물과 실제 canonical은 어디인가.
- 제품 검증 claim과 기준, 실행 입력, runtime·cwd·timeout·cache 의미는 무엇인가.

### Reference 책임 적응

- 각 책임의 live Owner와 파일을 target에 그대로 둘지, target 구조에 맞춰 적응할지, 제외할지 판단한다.
- Tool-specific Maintain 연결과 Project 설정은 target의 기존 role·설정 Owner를 먼저 확인한다. 수동 role, lifecycle hook, explicit binding, wrapper와 runtime ignore를 각각 설치·적응·제외하고, role 등록만으로 automatic lifecycle을 주장하지 않는다. 일부 또는 전체 adapter를 등록하지 않으면 canonical 계약을 main이 수행하는 fallback과 proof ceiling을 남긴다.
- Reference sample의 제품·Workspace 내용과 과거 receipt는 payload에서 제외한다.

## Project common context 내용 충족

기존 README·STATUS·`docs/`와 코드·테스트는 상세 사실의 canonical로 유지한다. `context/project/`는 이를 이동하거나 문단째 복제하지 않고, 여러 Workspace가 반복해서 판단할 실제 Project 목적·현재 범위·구조·제약·채택 결정을 선별해 다시 서술한다. 상세 Owner 링크는 provenance와 재대조 경로이지 내용의 대체물이 아니다.

먼저 상세 Owner의 공통 내용을 제품 목적·완료 기준·범위, 구현 구조·권한·검증 경로, 여러 작업에 계속 적용되는 채택 결정처럼 구분되는 책임으로 펼친다. Overview는 이 책임들의 진입 요약이지 별도 Owner를 없애기 위한 합본이 아니다.

Live Reference와 target 성격에 따라 필요한 Project context 파일을 선택한다. 최소 진입점 외의 PRD·architecture·decision이 선택 사항이어도, 파일 수를 줄이는 것 자체를 선택 근거로 삼지 않는다.

- 상세 Owner에 여러 Workspace가 반복해서 사용할 구분되는 제품 기준, 구현 구조 또는 채택 결정이 있으면 대응하는 Project context Owner를 만들고 실제 내용으로 채운다.
- 별도 책임으로 둘 독립된 공통 내용이 없을 때만 해당 Owner를 생략하고, 조사한 상세 Owner와 생략 이유를 dry-run manifest와 적용 기록에 남긴다.
- 내용이 있는데 overview에 흡수하거나, 출처 안내·첫 Workspace 요약만 남기기 위해 별도 Owner를 생략하지 않는다.

구현 뒤 다음 순서로 내용 충족을 검토한다.

1. 상세 Owner 링크를 열지 않고 `context/project/`만 읽는다.
2. Project의 사용자 장면과 목적, 현재 구현 범위와 목표 범위의 차이, 성공 기준과 범위 밖, 주요 구성요소의 권한·실행 흐름·불변성, 여러 Workspace에 계속 적용되는 결정, 자동 검증과 사람 acceptance 경계를 설명한다.
3. 선택 문서가 맡은 질문에 답하지 못하고 상세 Owner 경로만 가리키면 미완성으로 판정한다.
4. 그 뒤 상세 Owner를 열어 재서술한 사실이 원자료에 지지되고 현재·목표·미구현 상태를 섞지 않았는지 대조한다.
5. 첫 Workspace의 목표·검증 범위·빠른 상태가 Project 전체 사실로 승격되지 않았는지 확인한다.
6. 상세 Owner에서 확인한 구분되는 공통 책임마다 대응하는 Project context Owner가 있거나, 독립된 공통 내용이 없어 생략했다는 근거가 있는지 확인한다.

이 검토는 문서 길이나 링크 수로 자동 판정하지 않는다. 짧아도 공통 판단을 닫으면 충분하고, 길어도 출처 안내와 Workspace 전용 내용뿐이면 불충분하다.

## Preflight와 충돌

`capture_target_state.py` receipt는 한 번의 관찰에서 target Git root, branch, HEAD, tracked·staged·untracked 변경, 파일 kind·size·hash와 instruction file을 고정한다.

이 receipt는 atomic snapshot, ignored file inventory, 저자·변경 이유나 Git 밖의 과거를 증명하지 않는다. 따라서 다음을 추가로 수행한다.

1. Dry-run payload의 exact path와 ancestor가 실제로 존재하는지 확인한다.
2. Target ignore 규칙과 기존 clean canonical·설정 내용을 대조한다.
3. Preflight 변경과 payload의 교집합을 계산한다.
4. 교집합이 없으면 exact addition과 좁은 patch로 진행한다.
5. 교집합이나 Owner 충돌이 있으면 additive routing 가능성을 확인하고 의미 선택을 사용자에게 돌려보낸다.

기존 `context/`, instruction과 tool config는 빈 설치 자리가 아니다. Directory replace, broad recursive copy, 자동 이동·삭제와 broad staging을 하지 않는다. 임시 preflight receipt를 Workspace에 보존할 때는 바이트와 SHA-256을 유지한다.

## Evidence closure

Product Verify의 evidence는 중요해 보이는 파일 표본이 아니라 고정 실행이 실제로 읽는 입력을 설명해야 한다.

1. Root argv가 호출하는 package manager, task runner와 script를 펼친다.
2. Lockfile, workspace 선언, 공통 compiler·build 설정을 확인한다.
3. 실제 대상 package의 tracked source, manifest와 package-local 설정을 포함한다.
4. Runtime fixture, scenario, schema와 generated input을 확인한다.
5. 제외한 output, external state와 environment를 proof ceiling에 적는다.
6. Evidence를 실행 전에 snapshot한 뒤 같은 검증 사건에서 명령을 실행한다.

Cache hit만으로 fresh pass를 선언하지 않는다. Force/no-cache option을 고정하거나 cached validation 한계를 밝힌다. 명령 통과와 evidence가 어떤 tree를 대표하는지는 별도로 설명한다.

## 검증 선택

| 변경 성격 | 최소 확인 | 확대 조건 |
| --- | --- | --- |
| 설명·링크·routing | 경로, link, 설정 parse, diff | 실행 의미나 discovery가 달라짐 |
| Harness 코드·machine 계약·path 방어 | 관련 단위 테스트 | 공통 경계나 target 배치가 달라짐 |
| Target Harness 적응 | 전체 Harness tests와 ephemeral validation | 실패, source 변경 또는 proof 공백 |
| 상태 전환·인계 | Product Verify와 후속 Recover | Evidence closure나 runtime 불확실성 |
| Context 의미 변화 | 명시 Workspace Maintain과 main diff 검토 | 새 목표·canonical·acceptance 판단 필요 |
| 신규 이식·사용자 파일 충돌 | 독립 review | P1/P2 또는 원자료 충돌 |

반복 개발 확인과 durable evidence를 구분한다. Harness validation은 임시 fixture의 회귀 검사이고, Harness test receipt는 target-specific 관리 장치 증거이며, Product Verify는 실제 Workspace 상태 전환 증거다. 서로를 대신하지 않는다.

## 자동화하지 않을 판단

- Canonical과 Owner 선택, Owner migration 승인
- Active Workspace 선택과 변경
- 사용자 파일 삭제·이동·승격
- 임의 검증 명령의 신뢰 승인
- 일부 hash나 cache 결과를 전체 tree proof로 승격
- Pass 뒤 acceptance, completion, canonical 반영과 commit
- Concurrent Verify와 receipt/status transaction 보장

Helper는 관찰과 실행 증거만 결정적으로 만든다. 의미 선택과 최종 적용은 target 원자료, 사용자 권한과 실제 결과를 본 main이 맡는다.

## 최종 proof 문장

Target 사실로 다음을 답한다.

1. 어떤 Reference commit과 책임을 target에 그대로 적용·적응·제외했는가.
2. Recover가 실제로 무엇을 읽고 무엇을 제외했는가.
3. Validation과 Product Verify가 어떤 입력·runtime에서 무엇을 확인했는가.
4. 무엇이 외부 환경과 사람 acceptance로 남아 있는가.
