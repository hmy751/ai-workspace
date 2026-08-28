# 생성·전환 canonical 응집과 Workspace skill 검증

날짜: `2026-08-28`

## 변경 배경

초기 문서 계약은 사용자 요청에 따라 commit `1a4a9ff`로 먼저 보존했다. 그 뒤 같은 원칙이 Workspace collection, Work instruction, Recover와 Maintain 문서에 나뉘어 있어 생성 주체가 전체 workflow를 한 번에 찾기 어렵고, 이미 이식된 Project에서 새 Workspace 생성 요청을 실제로 붙잡는 실행 진입점이 없다는 문제를 별도 단계로 다뤘다.

## 선택한 구조

- [`reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md`](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md)가 생성 유형, 의미 선별, current·source·상세 근거 배치, 비상속·비동기화, bounded 재진입 검토와 session 활성화 경계를 함께 소유한다.
- Workspace collection README는 collection 정체성, 내부 Owner와 Workspace 독립 관계만 남기고 상세 workflow를 새 canonical로 routing한다.
- [`create-context-workspace`](../../../../reference-project/.agents/skills/create-context-workspace/SKILL.md)는 이미 Context Harness가 설치된 Project에서 새 독립 또는 후속 Workspace를 구성하는 repo-local 실행 adapter다. 지속 원칙과 live schema를 복제하지 않고 canonical을 읽는다.
- Reference root와 Work AGENTS는 새 Workspace 생성 요청만 skill로 routing한다. 최초 이식, 기존 Workspace 재진입·current 수정과 Project context 반영은 trigger에서 제외한다.
- [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/SKILL.md)는 최초 이식과 첫 Workspace를 계속 소유한다. 이후 Workspace용 운영 skill과 target root routing은 기존 파일을 덮어쓰지 않고 `install/adapt/exclude`와 fallback을 명시하며, 파일 설치와 새 target-root session의 실제 discovery를 구분한다.

## Global AI-system 기준 적용

- Context ownership: 지속 정의와 관리 규칙은 `CREATE-AND-TRANSITION.md`, 실행 시점의 적용은 제거 가능한 skill에 두었다.
- Responsibility cohesion: canonical, collection 진입점, instruction routing, Recover·Maintain 비소유와 이식 책임이 모두 같은 생성·전환 책임으로 이어지게 했다.
- Behavior responsibility allocation: 사람은 goal·source 권위·acceptance와 Project-wide 반영을, 모델과 skill은 의미 선별·구성을, schema와 validation은 명시 가능한 shape·경로 안전만 맡는다.
- Human-readable structure: 다음 세션의 판단을 바꾸는 의미는 current에 직접 쓰고, 추가 원문은 exact 경로·역할·이유·읽을 시점으로 찾게 했다.
- Harness rippability: skill을 제거해도 사람이나 다른 AI가 canonical을 따라 같은 생성 책임을 수행할 수 있으며, hook·동기화·parent schema와 deterministic generator를 추가하지 않았다.

## 정적·회귀 검증

- 새 skill의 frontmatter 허용 key, name·description 형식과 TODO 부재를 `quick_validate.py`의 검사 조건과 같은 Ruby fallback으로 확인했다.
- `agents/openai.yaml`은 YAML parse와 `allow_implicit_invocation: true`, `$create-context-workspace` default prompt를 확인했다. Routing 검토에서 default prompt가 독립 Workspace만 말하고 설치 전제를 생략한 잔여 위험을 찾아, 이미 설치된 Project의 독립 또는 후속 Workspace로 문구를 보정했다.
- 수정·추가 Markdown의 relative local link와 `git diff --check`가 통과했다.
- `apply-context-harness` helper test `7`개가 모두 통과했다.
- Reference 전체 unit test `97`개가 최종 실행에서 모두 통과했다. 첫 실행에서 기존 timing 민감 Verify test 하나가 실패했지만 같은 test 단독 실행과 이어진 전체 suite는 통과해 이번 문서·skill 변경의 회귀로 판정하지 않았다.

제공된 Python `quick_validate.py` 자체는 기본 Python과 Codex bundled Python 모두 `PyYAML`이 없어 import 단계에서 실행되지 않았다. 따라서 validator 실행 성공으로 보고하지 않고, script 원문과 같은 내용 검사 및 별도 YAML parse 통과만 증거로 남긴다.

## 격리한 001→002 forward test

Reference를 `/private/tmp` 아래 격리 복사하고 predecessor `001-default-timeout`에 retry budget 분석 record를 추가한 뒤, 새 작업 주체가 repo-local skill과 live canonical만 따라 `002-retry-budget-design`을 만들게 했다.

새 002 current는 다음 의미를 링크로 대신하지 않고 직접 소유했다.

- 기존 `5000`밀리초는 한 request attempt의 timeout이며 전체 operation budget이 아니다.
- retry 횟수나 backoff보다 별도 operation budget 채택 여부를 먼저 결정한다.
- 그 결정 전에는 기본값 변경, silent retry와 retry 횟수 확정을 하지 않는다.

Current state에는 predecessor 분석의 exact path, 상세 분석 record라는 역할, 첫 판단 왜곡을 막기 위해 필요한 이유와 첫 budget·API 판단 직전이라는 읽을 시점을 함께 남겼다. Predecessor의 나머지 current, 구현 선택, Verify receipt·status, acceptance와 records는 이어받지 않았다고 bounded하게 밝혔다.

검증 결과는 다음과 같다.

- Explicit `recover 002-retry-budget-design --json` 성공, packet schema `6`
- Initial machine status `ready_for_verification`, `result`·`receipt`·`finished_at`은 `null`
- Predecessor 전체, `workspaces/index.json`과 `.codex/maintain.json`은 생성 전후 SHA-256 목록이 같음
- 새 Workspace JSON parse와 local Markdown link 검사 통과
- 제품 code·Project canonical·제품 Verify·active index·host binding·commit 변경 없음
- Recover packet만 받은 별도 read-only 주체가 goal·제약·첫 판단·다음 행동, 필수 원문의 경로·역할·이유·시점, 계승·비상속과 증명 한계를 predecessor 없이 복원함

격리 fixture 자체는 지속 산출물이 아니며 Git 저장소도 아니므로, 이 기록은 관찰한 결과와 경계를 보존하고 임시 경로를 재접근 가능한 canonical 증거로 취급하지 않는다.

## 독립 검토와 증명 상한

최종 독립 검토는 canonical 중복, Owner·routing 충돌, 자동화 과잉, overwrite 위험과 proof ceiling을 확인했고 새 P1·P2·P3를 찾지 않았다. 별도 trigger 검토도 후속/무관 신규 Workspace는 생성 skill, 최초 이식은 apply skill, Recover·current 수정·Project context 반영은 기존 Owner로 분리됨을 확인했다.

이 결과는 Reference 안의 canonical·skill·routing과 한 격리 시나리오의 semantic 재진입을 확인한다. 현재 session에 새로 생긴 skill의 실제 registry 갱신, 새 target-root session의 implicit discovery, 실제 다른 Project 설치 효과, 모든 goal에서의 의미 충분성, host 활성화·binding 전환과 사람 acceptance는 증명하지 않는다.
