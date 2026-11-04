# Context Harness 이식 판단 기준

이 문서는 live `reference-project/`를 기존 개발 Project에 적용할 때 target마다 다시 판단할 내용을 소유한다. Reference 실행 계약, target 사실과 과거 적용 이력을 여기에서 다시 설명하지 않는다.

## Owner 분리

- `reference-project/`: 현재 Project·Work·Workspace 책임, 재개·기록·개발 계약과 스킬 연결을 소유한다.
- `apply-context-harness`: live Reference를 찾고 target Owner와 충돌을 조사해 책임을 적응·검증·보고하는 절차를 소유한다.
- Target Project: 자신의 canonical, Workspace 내용, 제품 코드, 검증 명령과 acceptance를 소유한다.
- Application Workspace: target에 실제로 적용한 source commit, 선택·예외·증거와 proof ceiling을 소유한다.

Reference의 현재 구성과 상세 운영 기준은 live canonical에서 읽는다. 아카이브한 실행기와 machine 계약은 현재 설치 요구가 아니다. 기존 target의 독립된 계약은 실제 소비자와 승인 범위를 확인해 전환한다.

## Target에서 다시 판단할 것

### Project와 Work Owner

- 여러 Workspace가 공유할 Project 목적·구조·제약·채택 결정의 상세 Owner는 어디인가.
- Live Reference가 요구하는 root routing과 `common/current/guidance` 물리 layer를 구성할 때 어떤 주제는 기존 Owner에 남기고, 어떤 주제는 승인된 범위 안에서 Project context로 옮길 것인가.
- 기존 context·package·instruction·도구 설정과 어떤 물리·의미 충돌이 있는가.

### 첫 Workspace

- 실제 작업 장면, 목표, 지속 제약, 빠른 상태와 다음 행동은 무엇인가.
- 일반 재개와 한정 요청에서 무엇을 왜 읽어야 하며, 방향·단계·읽기 대상이 달라질 때 누가 안내를 갱신하는가.
- 어떤 원문·snapshot·provenance를 source로 선택하고 무엇을 제외할 것인가.
- Goal을 위해 선택한 산출물과 실제 canonical은 어디인가.
- 제품 검증 claim과 기준, 실행 입력, runtime·cwd·timeout·cache 의미는 무엇인가.

### Reference 책임 적응

- 각 책임의 live Owner와 파일을 target에 그대로 둘지, target 구조에 맞춰 적응할지, 제외할지 판단한다.
- [Live Reference skill 색인](../../../../reference-project/.agents/skills/README.md)에서 각 repo-local skill과 필요한 공통 기준·도구별 연결을 확인하고 아래 기준으로 설치·적응·제외를 정한다. 첫 Workspace는 이식 책임이 직접 만들며 아직 설치되지 않은 운영 skill을 중첩 호출하지 않는다.
- 재개는 [Work 지침](../../../../reference-project/context/work/AGENTS.md)과 Workspace README·`recover.md`를 연결한다. 기본 Workspace는 collection README에서 찾는다. 재개 안내의 선택·이유·조건과 current의 실제 내용·상태를 구별하며, 생성 담당이 초기 안내를 만들고 record-work가 필요한 변경을 유지하도록 연결한다.
- 기록 실행은 [record-work](../../../../reference-project/.agents/skills/record-work/SKILL.md)와 target Work의 작성·갱신 기준에 연결한다. 원문 접근·서브 생성·재사용·직접 수정은 실제 host의 지원을 확인한다. 기존 자동 Maintain이 있으면 진행 중 작업과 미반영 책임을 확인하고 승인된 전환에서 중복 hook·role·wrapper·전용 코드를 정리한다. 기존 대화 원문·runtime 이력·Work 기록을 일괄 삭제하거나 이식으로 새 Workspace에 귀속하지 않는다. Reference에 없는 자동 binding·activation을 다시 설치하지 않는다. 직접 수정하는 스킬의 지침과 host 권한을 기존 guarded apply의 결정적 보장과 구별한다.
- Reference sample의 제품·Workspace 내용·과거 receipt와 아카이브한 runtime·machine 파일은 payload에서 제외한다. 새 설치에 옛 실행기를 쓰기 위해 전용 schema나 상태 파일을 다시 만들지 않는다.

### 기존 실행 장치 전환

기존 target에 자동 Maintain, Recover·Verify 또는 같은 역할의 다른 도구가 있으면 현재 연결을 먼저 조사한다. 이식 요청만으로 target의 모든 실행 장치를 제거할 권한이 생기지는 않는다. 이미 승인된 전환 범위는 재승인 없이 수행하고, 범위를 벗어나거나 사용자 변경과 충돌하는 선택만 구체적으로 확인한다.

- 명령·import·hook·설정·생성 절차·문서가 어떤 계약과 상태를 소비하는지 확인한다. 현재 작업 중인 Workspace와 실제 제품·외부 소비자를 포함하고 역사 기록의 언급은 구별한다.
- 새 재개·기록 경로가 필요한 의미와 근거에 접근하도록 먼저 구성한다. 이전 선택·identity·상태가 맡던 유효한 의미를 current와 안내에 연결하며, 두 경로가 같은 문서를 중복 관리하지 않게 한다.
- 사용 중인 소비자의 전환을 완료한 범위에서 전용 코드·계약·호출 설정을 내린다. 승인 범위 밖이거나 아직 소비자가 사용하는 기존 경로는 유지하고, 그 부분과 미전환 책임을 적용 기록에 남긴다. 일부 전환을 전체 전환으로 보고하지 않는다.
- 기존 receipt·원문·역사 record는 원래 소유 Workspace의 근거로 보존한다. 실행기·machine 계약을 아카이브할 때는 판본·원래 위치·복원 경로를 남기고, 과거 성공이나 freshness를 현재 검사 결과로 승격하지 않는다.

신규 설치에는 이 전환 대상이 없다. 아카이브를 설치하거나 기존 도구를 재구현한 뒤 다시 내리는 절차를 만들지 않는다.

## Repo-local skills와 공통 기준

설치할 스킬은 live Reference 색인과 각 `SKILL.md`·호출 설정에서 실제 책임·입력·연결을 확인해 선택한다. 이름 목록을 이 문서에 고정 payload로 유지하지 않는다. 공통 읽기는 `context/USAGE.md`, Personal·Project의 내용·관리 권한은 해당 영역의 canonical, Spec·Ticket의 내용과 유지 방식은 live Workspace canonical이 소유한다. 이식 절차에서 skill별 호출 규칙이나 Work 기록 담당을 다시 정의하지 않는다.

- **대상별 선택:** 각 skill의 원본·지원 파일·호출 설정, `context/USAGE.md`, Personal·Project의 관리 지침과 필요한 본문·형성 자료, `context/project/REFERENCE/`, `.agents/skills/shared/`의 실제 공통 기준과 consumer 색인, tool별 discovery 연결과 root routing을 dry-run manifest에 `install/adapt/exclude`로 구분한다. 이름이 달라도 같은 책임을 맡는 target Owner와 비교하고, 제외할 때는 그 이유와 필요한 기존 canonical·fallback을 남긴다. Reference의 Personal 경험은 원래 출처와 관찰 한계를 유지하며 target에서 생긴 경험으로 복사하지 않는다.
- **충돌 보호와 연결:** `.agents/skills/<name>/`의 전체 파일, target이 사용하는 `.claude/skills/<name>`·`.codex/skills/<name>` 같은 연결 경로, 공통 기준과 색인을 exact path로 확인한다. Clean·ignored 파일과 ancestor의 kind, 기존 symlink 목적지도 직접 확인하며 동명 경로를 통째로 덮어쓰지 않는다. Live source의 원본 관계와 호출 설정을 보존하되 도구별 상대 연결은 target 배치에서 해석해 같은 원본으로 이어지는지 확인한다. 도구가 지원하지 않는 연결을 기계적으로 설치하지 않는다.
- **공통 기준의 병합:** 대상의 기존 Project guidance와 skill 공통 기준의 소유 경계를 확인하고 필요한 본문·consumer 링크를 해당 Owner에 좁게 병합한다. Reference의 색인으로 target 색인 전체를 교체하지 않는다. 적용 범위·중요 예외·실제 consumer는 각 live 본문에 맞추며 모든 가이드에 같은 고정 목차를 강제하거나 모든 응답·일반 재개의 기본 자료로 확대하지 않는다. 기준 경로를 적응하거나 skill을 제외하면 남는 consumer와 색인을 함께 맞춘다.
- **실제 유지 경로:** 설치한 skill에서 target의 Spec·Ticket·Main·기록 담당자 관계를 찾게 한다. Workspace 생성과 Project·Personal 관리는 각 Owner에 남는다. record-work의 담당자가 같은 Work 문서를 직접 수정하고 Main은 필요한 실제 반영을 확인한다. 사용할 수 없는 host에서는 동일 문서 기준을 수행한 실제 주체와 한계를 남긴다. 설치·호출·반영·재개 효과를 구별한다.

정적 설치 확인은 frontmatter·호출 설정·일반 파일·상대 연결·canonical과 공통 기준 접근점까지다. 실제 host가 skill을 발견하고 정해진 방식으로 호출했는지, 결과가 Main을 거쳐 유지 경로에 전달되고 문서 의존 실행 전에 반영됐는지는 별도 관찰이다. 하나의 성공을 다른 skill·도구·기록 재사용의 증명으로 확대하지 않는다.

## 기존 문서의 전환

이식 범위에 들어온 기존 문서는 현재 역할과 내용을 보고 처리한다. 계속 쓰는 제품 상세 정본과 이번 이식으로 대체되는 이전 요약·운영 문서를 같은 보존 대상으로 취급하지 않는다. 생성 주체나 파일 나이만으로 유지·제거를 결정하지 않으며, 사용자 변경과 남아 있는 고유한 의미를 먼저 대조한다.

대체되는 문서의 유효한 내용은 현재 책임에 맞는 위치에 반영하고, 기존 파일의 이동·통합·제거와 영향받는 링크·소비 경로를 함께 처리한다. 승인된 이식 안에서 필요한 문서 전환은 이식의 일부다. 독립된 제품 정본의 이동, 사용자 변경과의 충돌 또는 승인 범위가 불명확한 선택만 따로 확인한다. 이 판단을 관련 없는 상세 문서 전체 정비로 확대하지 않는다.

기존 경로를 유지하려면 계속 맡는 현재 책임이나 실제 호환 필요가 있어야 한다. 새 문서를 만든 뒤 원문에 과거 문서라는 안내만 붙여 같은 위치에 남기는 것은 전환 완료 근거가 아니다. 과거 원문은 다시 판단할 필요가 있을 때 적절한 source·record 또는 기존 Git 이력에 보존하며, 모든 대체 문서의 별도 복사본을 의무적으로 만들지 않는다.

완료 검토는 새 문서뿐 아니라 전환 대상의 유효한 내용이 빠지지 않았는지, 기존 파일의 실제 배치와 남은 참조가 처리 이유에 맞는지도 대조한다. 내용 반영 없이 파일만 제거하거나, 새 구조와 대체된 구조를 이유 없이 함께 남기면 미완성이다.

### 승인된 주제별 Owner 이동

사용자가 특정 주제의 Owner를 Project context로 옮기도록 승인했다면 그 범위는 이식 또는 후속 갱신의 실제 전환 대상이다. 이미 받은 승인을 다시 묻지 않으며, 다른 상세 문서 전체의 이동으로 확대하지 않는다.

- Ticket, Workspace, 회의나 source 묶음은 근거 경계이지 문서 책임이 아니다. 다음 작업이 찾을 지속 주제와 판단 질문을 먼저 구성하고, 수명과 갱신 Owner는 분리 필요성을 판단하는 근거로 사용한다.
- 지속 의미는 `common/`, 교체되는 구현·지원·proof 경계는 `current/`, 관련 작업의 계약·적용·검증은 `guidance/`, 현재 답과 별도로 남길 중요한 선택 이유는 `decisions/`에 둔다. 한 질문을 이해하는 데 필요한 의미를 층 구분 때문에 흩뜨리거나 모든 주제에 세 문서를 만들지 않는다.
- 이동한 범위의 Project 문서는 현재 의미의 canonical임을 밝히고, 링크 없이도 그 의미와 경계를 설명한다. 링크는 구현 상세·원문·검증의 재대조 경로로 사용한다.
- 이전 canonical의 유효한 의미를 통합한 뒤 남은 역할을 구현 상세, 근거·역사 또는 호환 routing으로 좁히거나 target 규칙에 따라 이동·제거한다. 같은 현재 답의 active canonical을 둘 이상 남기지 않는다.
- 미정인 제품 선택은 열어 두고 확인된 나머지를 이동한다. Owner 이동을 새로운 제품 결정을 확정하는 것으로 바꾸지 않는다.
- Root의 주제별 진입과 layer index, 영향받는 실제 작업 진입점과 live consumer를 새 authority에 맞춘다. producer 본문이 존재하기 전에 consumer만 새 경로를 참조하는 중간 상태를 완성으로 남기지 않는다. 과거 Workspace 전체를 역동기화하지 않는다.

## Layered Project context 내용 충족

Owner 이동이 승인되지 않은 README·STATUS·`docs/`와 코드·테스트는 기존 상세 사실의 canonical로 유지한다. `context/project/`는 여러 Workspace가 반복해서 판단할 실제 Project 목적·현재 범위·구조·제약·채택 결정을 선별해 다시 서술한다. 승인된 주제별 이동과 이번 이식으로 역할이 바뀌는 문서는 위 전환 기준을 따른다. 상세 Owner 링크는 provenance와 재대조 경로이지 내용의 대체물이 아니다.

`context/project/`에는 다음 물리 경계를 만든다.

```text
context/project/
├── README.md
├── MAINTENANCE.md
├── REFERENCE/
│   ├── README.md
│   ├── composition.md
│   └── reading.md
├── common/
│   └── README.md
├── current/
│   └── README.md
├── guidance/
│   └── README.md
└── decisions/
    └── README.md
```

Root `README.md`는 작업·주제에서 실제 본문, 세 책임 layer와 Owner 우선순위를 찾는 안정된 routing anchor다. 독자가 layer를 먼저 분류해야만 내용에 들어갈 수 있게 하지 않고 Project 본문을 root의 평면 overview로 합치지 않는다. 첫 Workspace의 `recover.md`는 현재 goal과 요청에 필요한 Project 진입점·실제 본문을 이유·조건에 따라 연결한다. 모든 layer나 관리·작성·읽기 기준을 기본 자료로 선택하지 않는다.

- `common/`에는 여러 Work에 지속되는 제품·사용자·domain 의미와 Project-wide 제약을 둔다.
- `current/`에는 상세 Owner 변화에 맞춰 교체되는 현재 구현·지원·미지원 범위, 연결 구조와 proof boundary 중 다음 관련 판단을 바꾸는 맥락을 둔다.
- `guidance/`에는 관련 작업의 구체적인 계약·이유·적용·변경 판단·검증을 둔다. 조언이나 순서에 한정하지 않고, 적용할 작업과 중요한 예외를 본문에서 이해할 수 있게 한다.
- `decisions/`에는 중요한 선택의 이유·대안·재검토 신호를 둔다. 현재 세 layer의 답을 기본적으로 대신하지 않지만 문서가 현재 normative Owner임을 명시한 예외는 허용한다.

`common/current/guidance` layer와 각 README는 생략하지 않는다. 특정 layer에 README 외 실제 본문이 없을 수는 있으며, 이때 README에 현재 없음, 확인한 상세 Owner와 새 항목을 만들 조건을 적는다. 반대로 layer가 존재한다는 이유로 모든 주제에 본문을 하나씩 만들지 않는다. 파일 수를 줄이거나 늘리는 것을 목표로 독립된 내용을 합치거나 한 질문의 의미를 흩뜨리지 않는다. 기존 target의 flat Project context 문서도 현재 역할과 내용에 따라 전환하며, 평면 파일이라는 이유만으로 모두 이동하거나 보존하지 않는다.

각 실제 내용 문서에서 맡은 질문과 읽을 조건을 이해할 수 있어야 한다. 현재 authority, 구현·검증 상세 Owner, 갱신 책임과 재확인 신호는 그 문서의 판단에 실제로 필요한 범위에서 밝힌다. 모든 문서에 같은 메타데이터나 목차를 강제하지 않는다. 한 문서에 다른 층의 짧은 전제 설명이 있을 수 있지만 독립 정책을 두 곳에서 관리하게 만들지는 않는다.

내용의 보존·불확실성 표현·변경과 갱신 시점은 live [`Project 관리 계약`](../../../../reference-project/context/project/MAINTENANCE.md), 선별·구성·읽기는 live [`Project REFERENCE`](../../../../reference-project/context/project/REFERENCE/README.md)를 읽고 target의 대응 위치에 적응한다. Root README는 각 기준의 역할과 읽는 시점을 연결한다. 이 기준은 제품·domain 본문과 구분하며 이식·복원·갱신·읽기 주체가 필요한 작업에서 직접 읽고, 일반 재개의 기본 자료에는 자동 추가하지 않는다. 이번 이식에서 무엇을 통합·이동·제거하고 어떻게 보존했는지는 적용 Workspace 기록이 소유한다. 이식 검토에서는 미정 부분의 존재를 이유로 원자료가 뒷받침하는 제품 목적·domain 의미까지 빠지지 않았는지, 남은 판단이 현재 확정된 규칙으로 바뀌지 않았는지를 함께 대조한다. 이 기준을 skill에만 설치하고 target Project 계약에서 빠뜨리지 않는다.

구현 뒤에는 다음 독자가 맡을 대표 관련 작업을 정하고 [읽기 기준](../../../../reference-project/context/project/REFERENCE/reading.md)으로 내용 충족을 검토한다.

1. Root README의 주제별 진입에서 대표 작업에 필요한 실제 본문과 그 책임을 찾는다.
2. 작성 중 읽은 원자료나 대화 기억 없이 선택 본문만으로 그 작업이 요구하는 제품 의미·계약·이유·현재 차이·열린 판단을 설명하고 구현 확인으로 내려간다.
3. 선택 문서가 맡은 질문에 답하지 못하고 상세 Owner 경로만 가리키거나 Ticket·기록 묶음의 목차만 재현하면 미완성으로 판정한다.
4. 그 뒤 상세 Owner와 실제 코드·테스트를 열어 재서술한 사실과 문장의 범위, 현재 authority와 proof boundary가 맞는지 대조한다. 일부 경로만 확인했다면 Project 전체 사실로 일반화하지 않는다.
5. Owner 이동이면 기존 Owner의 유효한 의미가 새 본문에 보존됐는지, Project README와 대표 기존 작업 진입점이 같은 현재 Owner에 도달하는지 각각 확인한다.
6. 첫 Workspace의 목표·검증 수치·환경 오류·미실행 항목이 다음 판단과 재확인 조건 없이 Project 현재 사실로 승격되지 않았는지 확인한다.
7. 각 layer에 원자료가 지지하는 실제 내용이 있거나 README 외 본문이 없는 이유와 새 항목을 만들 조건이 명시됐는지 확인한다.
8. 첫 Workspace를 명시한 재개에서 README·`recover.md`를 따라 goal에 필요한 Project 진입점과 실제 본문에 도달하는지 확인한다. `MAINTENANCE.md`와 `REFERENCE/`는 읽을 이유가 있는 작업에서 선택되고 일반 제품 작업의 기본 자료로 자동 추가되지 않았는지 대조한다.

이 검토는 문서 길이나 링크 수로 자동 판정하지 않는다. 짧아도 공통 판단을 닫으면 충분하고, 길어도 출처 안내와 Workspace 전용 내용뿐이면 불충분하다.

## 영향받는 live consumer reconciliation

Project 문서의 path·책임·authority를 새로 만들거나 크게 바꿀 때에는 producer만 검사하지 않고 영향을 받는 live consumer를 고정한다.

- collection README가 기본값으로 안내하는 Workspace
- 현재 Main·기록 담당자에게 명시적으로 배정되어 실제 작업 중인 Workspace. 전환 전 자동 Maintain이 남아 있다면 현재 연결된 작업도 포함한다.
- 이번 적용에서 명시적으로 생성·변경하는 Workspace

과거 배정과 이미 소비 경로에서 내려온 역사 Workspace는 자동 갱신하지 않는다. 현재 배정·문서 선택으로 소비자를 확인하며 무관한 대화 원문을 열거나 복제하지 않는다. 옛 자동 연결의 처리가 필요한 경우 해당 대상의 운영 metadata부터 확인한다. 역사 Workspace 비동기화 원칙은 해당 Workspace가 live consumer에서 내려온 뒤에 적용한다.

각 live consumer는 재개 안내의 선택·이유, current의 경로·내용 Owner 설명, output target을 현재 canonical에 맞게 reconcile하거나 successor 전환·deactivation으로 소비 경로에서 내린다. Workspace를 명시한 진입과 collection의 기본 선택을 각각 따라 실제 README·안내·본문으로 이어지는지 확인한다. Fresh reader가 일반 재개나 한정 요청에 필요한 의미와 첫 행동을 복원하고 설명·실제 Owner를 대조하게 한다. 링크가 존재한다는 사실을 의미 정합성 확인으로 바꾸지 않는다. 남겨 둔 target 실행 소비자는 그 실제 계약에 맞춰 별도로 확인한다.

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
6. README의 정체성·구성, `recover.md`의 읽기 안내, current의 목표·판단·상태, output의 산출물 지도, records의 실행 근거가 실제 Owner와 맞는지 확인한다. 남겨 둔 역사 machine 결과를 현재 상태나 현재 유효성 판정으로 설명하지 않는다.

## 검증 근거와 재사용

검사 결과를 지속 근거로 남기거나 재사용할 때는 실제 명령이 무엇을 읽고 어떤 조건에서 실행됐는지 설명한다. 제품 검증의 충분성은 해당 제품 계약과 development가 판단하며 이식 절차가 별도 범용 Verify를 만들지 않는다.

- 실행 명령·cwd·판본과 관련 변경분, 실제로 영향을 주는 package script·설정·fixture·generated input·환경·cache 조건을 확인한다. Git commit만으로 미커밋·미추적 입력과 외부 환경을 식별했다고 하지 않는다.
- 필요한 판본 식별·출력·종료 결과와 실패·미실행 항목을 같은 검증 사건의 Work 기록에 연결한다. 보존하지 못한 입력·환경이 있으면 주장 범위를 그 한계에 맞춘다. 고정 machine schema나 전체 파일 해시 수집을 모든 검사에 의무화하지 않는다.
- 이전 결과는 관련 코드·계약·입력·실행 조건의 변화를 대조해 재사용하거나 다시 실행한다. 원래 기록에 없는 정보를 뒤늦게 당시 snapshot처럼 보충하지 않는다.

실행이 길거나 자식을 만들거나 출력량이 큰 검사는 실제 실행 도구의 시간·프로세스·출력 제한을 확인한다. 반환 대기 시간은 강제 종료 제한이 아니며 직접 프로세스 종료와 자식까지 종료하는 것은 다르다. 필요한 제한이 없으면 적합한 실행 방법을 선택하거나 미확인 범위를 남긴다. 새 안내·스킬이 기존 Verify의 자동 snapshot, 출력 보존 한도, append-only receipt나 atomic status 보장을 그대로 제공한다고 설명하지 않는다.

Cache hit만으로 fresh pass를 선언하지 않는다. Force/no-cache option을 고정하거나 cached validation 한계를 밝힌다. 명령 통과와 evidence가 어떤 tree를 대표하는지는 별도로 설명한다.

## 검증 선택

| 변경 성격 | 최소 확인 | 확대 조건 |
| --- | --- | --- |
| 설명·링크·routing | 경로, link, 설정 parse, diff | 실행 의미나 discovery가 달라짐 |
| Repo-local skill·Project REFERENCE·공통 기준 | 각 frontmatter·호출 설정, canonical·consumer link, 도구별 상대 연결·root routing, 기존 skill·guidance 보존 | 새 target-root session의 실제 발견·호출·본문 적용·문서 유지 흐름 확인 필요 |
| 기존 target 실행 장치의 유지·전환 | 해당 계약의 직접 검사, 실제 호출·소비자 확인, 기존 증거 보존 | 공통 경계·사용자 파일 보호·실행 제한이 달라짐 |
| Workspace 재개 안내 | 명시 Workspace·기본 선택의 읽기 경로와 일반/한정 요청의 의미 복원 | 선택 이유·필수 근거·첫 행동의 누락 |
| 상태 전환·인계 | 필요한 직접 검사·eval·수동 확인, Work 근거 보존과 다음 재개에서의 접근 | 검사 입력·환경이나 이전 결과 재사용의 불확실성 |
| Context 의미 변화 | 명시 Workspace의 record-work 반영과 Main 결과 확인 | 새 목표·canonical·acceptance 판단 필요 |
| Project path·책임·authority 변화 | 모든 live consumer의 재개·읽기 경로, local link·residue 탐지와 fresh semantic review | consumer를 유지할 수 없거나 successor·deactivation 선택 필요 |
| 기록 실행 전환 | 원문 접근·동일 담당자 재사용·직접 반영과 옛 자동 경로 제거 확인 | 실제 host 입력·호출·반영의 미확인 또는 미반영 책임 |
| 신규 이식·사용자 파일 충돌 | 독립 review | P1/P2 또는 원자료 충돌 |

반복 개발 확인과 지속 근거 보존을 구분한다. 제품 검사, 문서·연결 확인, 실제 host의 읽기·기록 수행과 사람 수락은 서로를 대신하지 않는다. 기존 Python Harness를 유지·수정할 때 선택할 수 있는 `record_harness_tests.py`는 그 전용 source·unittest 결과를 `harness_test` receipt에 남기는 독립 helper다. 새 설치의 선행 조건이나 범용 제품 검사기가 아니다.

신규 이식이나 큰 Project 내용 복원·책임 재구성에서는 구현자의 결론과 파일명 힌트를 답안으로 주지 않은 cold/blind review를 사용한다. Application Workspace record에는 reviewer brief, 허용 source와 revision, worker result 또는 patch/hash, finding, 수정 이유와 최종 disposition을 남긴다. Private 원문 전체를 불필요하게 복제하지 않고 이 narrative review를 제품 검사 결과로 취급하지 않는다. 낮은 위험의 설명·routing 변경에는 이 절차를 자동으로 붙이지 않는다.

## 자동화하지 않을 판단

- Canonical과 Owner 선택, Owner migration 승인
- Active Workspace 선택과 변경
- 사용자 파일 삭제·이동·승격
- 임의 검증 명령의 신뢰 승인. 단, 사용자가 명시적으로 요청한 target-local Codex hook trust는 target root task에서 hook definition을 확인하고 activation receipt를 남기는 별도 activation 단계로 처리할 수 있다.
- 일부 hash나 cache 결과를 전체 tree proof로 승격
- Pass 뒤 acceptance, completion, canonical 반영과 commit
- 새 문서·스킬에서 자동 동시성 제어·파일 비교·증거 transaction을 보장한다는 주장

Helper는 관찰과 실행 증거만 결정적으로 만든다. 의미 선택과 최종 적용은 target 원자료, 사용자 권한과 실제 결과를 본 main이 맡는다.

## 최종 proof 문장

Target 사실로 다음을 답한다.

1. 어떤 Reference commit과 책임을 target에 그대로 적용·적응·제외했는가.
2. Workspace를 명시하거나 기본값으로 진입했을 때 재개 안내에서 실제로 무엇을 읽고 무엇을 제외했는가.
3. 어떤 live consumer를 확인했고 Project 선택·current·output을 reconcile, 전환 또는 deactivation했는가.
4. Local link·semantic target·residue와 내용 Owner 설명을 어디까지 확인했는가.
5. 각 repo-local skill·Project REFERENCE·공통 기준·guidance 색인·도구별 연결과 root routing이 설치·적응·제외 중 무엇이며, 실제 발견·호출·본문 적용·문서 유지 흐름은 어디까지 확인됐는가.
6. 직접 검사·eval·수동 확인은 어떤 판본·입력·실행 조건에서 무엇을 확인했고, 근거는 어디에 보존했는가.
7. Record-work의 설치·원문 접근·담당자 재사용·직접 반영, 기존 자동 경로 전환과 미반영 책임은 어디까지 확인됐는가.
8. 무엇이 외부 환경과 사람 acceptance로 남아 있는가.
9. 기존 실행 장치가 있었다면 어떤 소비자·호출·계약을 전환하거나 유지했고, 기존 증거와 미전환 책임은 어디에서 찾는가.
