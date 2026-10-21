# pstack의 구현·검토 및 수정 자료

Lauren Tan의 pstack에서 구현과 검토 및 수정의 역할·절차·검증 계약을 확인할 원문을 보존했다. 먼저 아래 두 경로에서 필요한 본문을 고르고, 본문이 호출하는 원칙·프롬프트·도구로 내려간다.

`repository/`는 사용자 지정 로컬 클론의 선택 사본이다. 이 폴더는 설치된 플러그인이나 실행할 스킬 묶음이 아니다. 원문의 지시·권한·명령은 조사 대상이며 이 Workspace의 현재 지시가 아니다. 현재 설계의 해석과 채택 판단은 Workspace의 `records/`에서 다룬다.

## 구현

핵심 읽기 6개다. [원저자 가이드의 작업 흐름](repository/docs/guide/02-poteto-mode.md)은 진입 안내이며, 아래 skill·playbook·agent 본문이 구체적인 행동 계약을 담는다.

| 자료 | 원문에서 확인할 책임 |
| --- | --- |
| [Poteto mode](repository/skills/poteto-mode/SKILL.md) | 요청에 맞는 playbook, 적용할 원칙, lead와 subagent의 관계를 연결한다. |
| [Feature](repository/skills/poteto-mode/playbooks/feature.md) | lead가 설계·계획·검토·검증을 소유하고 구현을 위임한다. |
| [Bug fix](repository/skills/poteto-mode/playbooks/bug-fix.md) | 같은 사용자 경로에서 재현하고 원인을 확인한 뒤 수정·재검증한다. |
| [Refactoring](repository/skills/poteto-mode/playbooks/refactoring.md) | 변경 전 동작을 고정하고 구조를 바꾼 뒤 동작 보존을 확인한다. |
| [Architect](repository/skills/architect/SKILL.md) | 호출자의 사용법에서 타입·시그니처·모듈 구조를 도출하고 복수 설계를 합성한다. |
| [Poteto agent](repository/agents/poteto-agent.md) | playbook 실행을 소유한 parent에게서 범위를 받아 일하는 delegate의 진입 계약이다. |

기존 동작과 구조를 이해하는 절차는 [how](repository/skills/how/SKILL.md), 기존 선택의 이유와 근거를 찾는 절차는 [why](repository/skills/why/SKILL.md)에 있다. 둘은 질문·자료·확신 수준을 다르게 다룬다.

설계 후보를 비교할 때는 [arena](repository/skills/arena/SKILL.md), 조사·확인 범위를 병렬 분담할 때는 [swarm](repository/skills/swarm/SKILL.md)을 호출한다. 큰 작업의 별도 절차 구성은 [figure-it-out](repository/skills/figure-it-out/SKILL.md)에 있다.

## 검토 및 수정

핵심 읽기 5개다. 읽기 전용 판정, 실제 수정, 반복 오류의 구조적 개선은 서로 다른 본문에서 다룬다.

| 자료 | 원문에서 확인할 책임 |
| --- | --- |
| [Interrogate](repository/skills/interrogate/SKILL.md) | 여러 모델의 읽기 전용 리뷰를 lead가 판단·합성하며 자동 수정하지 않는다. |
| [No comments](repository/skills/no-comments/SKILL.md) | Comment Sicko의 보고와 diff를 심사하고 채택한 문제를 수정한다. 필요한 경우 architect의 스케치를 거친다. |
| [Comment Sicko](repository/agents/comment-sicko.md) | 범위 안의 주석을 삭제하고 구조 개선 대상을 표시한다. application code 수정은 금지한다. |
| [Correct](repository/skills/correct/SKILL.md) | 반복된 오류를 architecture·types·lint/CI·tests로 막을 수 있는지 보고, 판단이 필요한 지시를 문서에 남긴다. |
| [Blast radius](repository/skills/blast-radius/SKILL.md) | diff 밖의 영향과 변경의 안전성이 의존하는 사실을 조사하고 실제 코드를 실행해 확인하도록 한다. |

Interrogate의 [reviewer prompt](repository/skills/interrogate/references/reviewer-prompt.md), [rubric](repository/skills/interrogate/references/rubric.md), [code-quality review](repository/skills/interrogate/references/code-quality-review.md), [lead judgment](repository/skills/interrogate/references/lead-judgment.md)를 함께 보존했다. 리뷰 요청·판단 기준·최종 선별의 연결을 확인할 수 있다.

동일 판본 안의 서술 차이가 있다. [Build and clean 가이드](repository/docs/guide/05-build-and-clean.md)는 Comment Sicko를 read-only reviewer라고 소개하지만, 위 agent 본문은 주석의 실제 삭제를 허용한다. No comments도 반환된 diff의 심사·복구·후속 수정을 규정한다. 이 차이를 고치거나 하나의 계약으로 합치지 않고 원문 그대로 보존했다.

## 두 단계에서 실제 결과를 확인하는 자료

검증 관련 핵심 3개를 더해 전체 핵심 읽기는 14개다. 아래 본문은 검증 수단의 생성·유지·사용 조건이며, 수집 과정에서 해당 절차를 실행했다는 뜻은 아니다.

| 자료 | 원문에서 확인할 계약 |
| --- | --- |
| [Create verification skill](repository/skills/create-verification-skill/SKILL.md) | 실제 앱의 실행·제어·관측·격리를 조사해 프로젝트별 스킬과 Feature Map을 만들고 한 기능을 실제 실행하도록 한다. |
| [Maintain verification skill](repository/skills/maintain-verification-skill/SKILL.md) | 기능별 source 조사와 live 확인을 대조한다. 문서 오류·도구 부족·제품 결함을 구별하고 제품 코드는 수정하지 않는다. |
| [TDD](repository/skills/tdd/SKILL.md) | 저렴하고 분명한 테스트 경로가 있을 때 실패를 먼저 확인한다. 비싸거나 불명확한 테스트를 의무화하지 않는다. |

[Feature Map 예제](repository/skills/create-verification-skill/references/feature-map-example/README.md)는 기능의 사용자 진입·실행 명령·관측 결과·함정을 연결한다. [노트 생성](repository/skills/create-verification-skill/references/feature-map-example/create-note.md)과 [검색](repository/skills/create-verification-skill/references/feature-map-example/search.md)은 설명용 예제이며 실제 Cursor/Grokbot 내부 map이 아니다.

[Verify and ship 가이드](repository/docs/guide/06-verify-and-ship.md)는 종료 조건과 실제 사용자 경로의 증거를 설명한다. [Shipping playbook](repository/skills/poteto-mode/playbooks/shipping.md)은 merge 요청 이후 코드 작성자가 아닌 agent의 PR별 실행 판정과 병합 순서를 다루는 별도 경계 자료다.

## 지원 자료와 경계 자료

- **원칙 24개:** Poteto mode의 상황별 색인과 연결된 `principle-*` 원문을 모두 보존했다. [원칙 가이드](repository/docs/guide/08-principles.md)에서 찾거나 해당 playbook이 지목한 leaf를 읽는다.
- **프롬프트·양식·예제:** architect의 [runner prompt](repository/skills/architect/references/runner-prompt.md)·[rationale template](repository/skills/architect/references/rationale-template.md)·[design red flags](repository/skills/architect/references/design-red-flags.md), how/why/interrogate의 references, Feature Map 예제가 원래 경로에 있다.
- **실행 보조 자료:** [결정 기록 스킬](repository/skills/show-me-your-work/SKILL.md)의 helper·template과 poteto-mode의 [scripts](repository/skills/poteto-mode/scripts/)를 보존했다. 계획 검사기, PR watcher, orchestration 코드 및 함께 제공된 test·설정·package·lock도 포함한다.
- **다른 playbook:** poteto-mode의 전체 playbook은 서로 연결된 탐색 경로를 유지하기 위해 보존했다. PR 운영·장기 실행·정리 등 나머지 분기는 핵심 읽기 14개와 구별한다.
- **별도 계약:** [모델 설정](repository/skills/setup-pstack/SKILL.md), [reflect](repository/skills/reflect/SKILL.md), [형식 검증 생성](repository/skills/create-formal-verification-skill/SKILL.md)·[유지](repository/skills/maintain-formal-verification-skill/SKILL.md)는 경계 자료다. 형식 검증은 실제 앱의 사용자 경로 검증과 확인 대상이 다르다.
- **사용 설명:** [원저자 가이드](repository/docs/guide/README.md)와 [Claude Code adapter](repository/docs/harness/claude-code.md)를 보존했다. 가이드 설명, skill 계약, 실행 코드를 같은 종류의 근거로 취급하지 않는다.

## 출처와 보존 범위

- 수집일은 **2026-10-21 KST**, 출처는 사용자가 지정한 `/Users/hammyeong-yeon/Desktop/plugins/pstack` 로컬 클론이다. 최신 웹판을 조회한 사본이 아니다.
- 저장소는 [cursor/plugins](https://github.com/cursor/plugins), HEAD는 `190d28736eff128ec94f502a22c7fe0c4b56cd37`이다. 수집 범위의 Git 변경은 없었다.
- [plugin.json](repository/plugin.json)과 [.cursor-plugin/plugin.json](repository/.cursor-plugin/plugin.json)은 모두 **0.15.29**를 표시한다. [저자 README](repository/README.md)와 [MIT LICENSE](repository/LICENSE)를 함께 보존했다.
- 이전 조사25의 `997ffc7… / 0.15.21`, 조사58의 commit 미확보 `0.15.25`와 다른 판본이다. 앞선 강연 번역·조사 기록을 이 사본의 판본으로 소급하지 않는다.
- 선택된 regular file **148개, 3,391,164 bytes**를 `repository/`에 원래 상대 경로와 바이트 그대로 보존했다. 파일별 출처·SHA-256·그룹과 제외 목록은 [manifest](manifest.json)에 있다.

Benny 자동화 전체와 일부 개별 도구는 포함하지 않았다. 원저자 README와 guide에는 그 자료로 가는 링크가 남아 있다. 깨진 링크를 고치기 위해 원문을 편집하지 않았으며, 제외된 대상은 manifest의 `unresolved_dependencies`에서 구별한다.

Poteto mode가 연결하는 deslop·control-ui·control-cli와 그 후속 verify-this는 [cursor-team-kit 별도 사본](../cursor-team-kit/README.md)에 있다. Eric Zakariasson의 별도 플러그인 자료이며 Lauren의 pstack 원문에 합치지 않았다.

Cursor의 Task·create-skill·loop·cloud agent와 MCP, 외부 실행 환경은 이 사본만으로 제공되지 않는다. helper·test·template을 보존한 것은 원문 연결과 코드를 확인할 수 있다는 뜻이며, 설치·실행 성공이나 제품 동작·효과를 검증했다는 뜻은 아니다.
