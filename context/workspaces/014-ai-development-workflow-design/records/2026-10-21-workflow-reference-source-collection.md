# 구현과 검토·수정 논의를 위한 원자료 수집

2026-10-21. 사용자는 큰 논의 단위를 **구현**, **검토 및 수정**으로 두고, 운영안을 구체화하기 전에 Desktop의 Matt·pstack 로컬 자료를 더 찾아 `source`를 구성하도록 요청했다. [새 자료 진입점](../source/workflow-references/README.md)에서 단계별 핵심 본문과 조건부 상세를 찾는다. 이번 결과는 자료 수집·출처 보존·읽기 경로 정리이며, 스킬 설치나 실행 방식의 채택이 아니다.

## 요청과 범위

사용자:

> 그럼 일단 크게 구현 그리고 검토 및 수정 정도로 단계를 생각해보면 될것 같고

> 그래서 우리가 지금 하려는 범위 관련한 자료를 더 찾아보면 좋겠어 해당 폴더에서 그래서 일단 그것부터 수집해서 source 다시 구성 제대로 해보자

사용자는 Matt 자료로 `Desktop/skills`, Lauren 자료로 `plugins/pstack`을 지정했고, 이어 “plugins도 Desktop에 클론 해놨어”라고 위치를 확인했다. Vercel은 기존 원문 설계 자료로 진행해도 된다고 했다. 따라서 지정한 두 로컬 클론과 기존 Workspace 원자료를 조사했다. pstack이 직접 호출하는 같은 `plugins` 저장소의 Cursor Team Kit 세 스킬과 연결된 증거 확인 스킬까지 추가했다.

구현과 검토·수정은 현재 논의를 크게 나눌 단위다. 검사·실제 확인·필요한 세부 설계·맥락 선택을 제외한 뜻이나, 항상 두 agent만 호출하겠다는 선택으로 해석하지 않는다. 기존 B의 검토자 직접 수정 방향은 유지한다. 최종 확인의 담당·독립성·종료 조건과 실제 스킬 연결은 남아 있다.

## 수집한 원문과 구성

| 출처 | 실제 보존과 판본 | 선택 이유 |
| --- | --- | --- |
| [Matt](../source/workflow-references/matt-pocock/README.md) | 원문 81개, 403,841 bytes. `mattpocock-skills` 1.3.1, `5beb35b040e3de97e54fa9e386d7e42d15c295c2` | implement·implement-spec·TDD·code-review·codebase-design·구조 개선을 중심으로 입력·설정·진단·인계·보고와 직접 참조를 포함했다. |
| [pstack](../source/workflow-references/pstack/README.md) | 원문 148개, 3,391,164 bytes. 0.15.29, `190d28736eff128ec94f502a22c7fe0c4b56cd37` | Feature·Bug fix·Refactoring, architect·arena, interrogate·no-comments·correct·blast-radius, 검증 생성·유지와 agent·원칙·예제를 보존했다. |
| [Cursor Team Kit](../source/workflow-references/cursor-team-kit/README.md) | 원문 8개, 76,788 bytes. 1.2.0, pstack과 같은 Git 판본 | poteto-mode가 명시한 deslop·control-ui·control-cli와 연결된 verify-this 및 출처·라이선스다. Eric Zakariasson의 별도 plugin으로 구별했다. |
| [Vercel](../source/workflow-references/vercel/README.md) | 기존 article 한 편을 연결. John Phamous, 2026-06-25 게시, 2026-10-12 보존 | 구현·검토 모드, 제품 판단·기준 선택·실제 확인·기준 갱신을 찾는 절과 행을 안내했다. 내부 reference 전체는 없다. |

신규 원문은 합계 **237개, 3,871,793 bytes**다. 이 수는 새 README·manifest나 재사용한 강연 자료를 포함하지 않는다. 각 `repository/`는 원래 상대 경로와 바이트를 유지한다. 원문 안의 링크·문구를 현재 판단에 맞춰 고치지 않았다. 두 원본 저장소는 조사·수집 범위에서 작업 트리가 clean이었고 수정하지 않았다. 웹 최신판을 수집한 것으로 표시하지 않는다.

선택한 SKILL뿐 아니라 상세 reference, agent prompt, template·script, 실행 metadata와 라이선스를 함께 보존했다. pstack의 나머지 playbook·runtime 파일은 상호 참조와 실행 전제를 확인할 경계 자료로 둔다. 사용자 가이드의 연속 탐색과 그림도 보존했지만 핵심 읽기는 별도로 안내한다. 공개 폴더의 전체 자료를 매번 읽게 하는 구조가 아니다.

범위 밖의 이슈 자동화·교육·개인화·별도 도구는 제외했다. 원 README·가이드에 이들 링크가 남는 것은 원문 보존의 결과다. 각 manifest의 선정·제외 목록과 연결 점검에서 누락과 의도적 제외를 구별한다. Cursor host, 대상 앱·프로젝트의 코드·데이터·실행 환경, 외부 서비스 연결은 확보한 문서와 별개다.

## 원문 확보로 다시 볼 수 있게 된 것

**Matt의 핵심 자료는 이전 조사와 같은 내용이다.** 로컬 Git에서 조사24의 `49dd158d1076134a641b33efb035946536778336`과 이번 HEAD를 비교했다. 차이는 이번 선정에서 제외한 `skills/in-progress/chief-of-staff/SKILL.md`와 `.changeset/chief-of-staff-wiki.md` 두 파일이었다. 이번 보강은 기존 조사에서 링크로 남았던 실제 본문·상세·가이드·템플릿을 Workspace 안에서 읽을 수 있게 한 것이다. 예전 `lectures/` 번역이 이 commit의 정확한 번역이라는 뜻은 아니다.

Matt [implement](../source/workflow-references/matt-pocock/repository/skills/engineering/implement/SKILL.md)는 검토 뒤 커밋하도록 하고, [code-review](../source/workflow-references/matt-pocock/repository/skills/engineering/code-review/SKILL.md)는 고정점과 HEAD의 committed diff를 읽는다. [implement-spec](../source/workflow-references/matt-pocock/repository/skills/engineering/implement-spec/SKILL.md)은 검토 지적을 구현 담당자에게 넘긴다. 강연의 직접 수정 권고와 이 실제 연결을 같은 계약으로 묶지 않는다. 일부 `docs/`의 미구현 설명과 SKILL 본문에도 차이가 있어 원문을 함께 대조할 필요가 있다.

**pstack은 과거 조사와 판본이 다르며, 검토·수정 경로도 더 살펴볼 수 있다.** 조사25의 0.15.21·고정 `997ffc7`과 비교58의 0.15.25를 이번 0.15.29에 섞지 않는다. 특히 [no-comments](../source/workflow-references/pstack/repository/skills/no-comments/SKILL.md)는 주석을 다루는 특수 절차로, Comment Sicko의 보고와 삭제 diff를 lead가 심사한 뒤 채택한 문제를 수정하고 필요하면 architect의 스케치를 연결한다. [interrogate](../source/workflow-references/pstack/repository/skills/interrogate/SKILL.md)의 읽기 전용 검토만으로 pstack의 모든 검토 방식을 대표시키면 부족하다. 반대로 이 특수 절차를 일반 리뷰 전체가 직접 수정한다는 계약으로 확대하지 않는다.

[사용 가이드](../source/workflow-references/pstack/repository/docs/guide/05-build-and-clean.md)는 Comment Sicko를 read-only reviewer로 설명하지만, [agent 본문](../source/workflow-references/pstack/repository/agents/comment-sicko.md)은 주석 삭제를 허용하고 application code 변경을 금지한다. 이 차이도 원문을 함께 보존했다. 형식 검증 생성·유지 스킬은 실제 사용자 경로 검증과 보장 대상이 달라 경계 자료로 두었다.

**Vercel은 기존 글의 확보 범위를 유지한다.** 축약된 SKILL과 lint 예시는 있지만 내부 `product-judgment`, `interface-quality` 등의 독립 본문과 실제 전체 eval·검토 packet은 없다. 해당 파일이 없다는 것을 임의 초안으로 메우거나 새 공개 구현을 확보한 것으로 기록하지 않는다.

## 확인과 후속

Main은 신규 원문 237개의 크기·SHA-256을 원본과 사본에 대조했고, 기존 tracked source 1,121개가 이번 작업 전 hash를 유지하는지 확인했다. 기존 강연·번역·Vercel을 포함한 lectures 10개는 기존 evidence-manifest와도 일치한다. 수집한 스킬·실행 도구 자체는 설치·실행하지 않았다.

자료 안내와 현재 상태·Ticket의 로컬 링크 309개를 확인했고 누락은 없었다. 원문 내 상대 링크는 구별해 점검했다. 선택 범위 밖 탐색 링크 57개와 예시 placeholder 1개는 원문대로 남겼다. 최종 연결 점검과 확인 수치는 [수집 확인 receipt](receipts/source-collection/2026-10-21-workflow-references.json)에 있다.

별도 검토자는 지정 원본·선정 목록·읽기 안내를 대조해 핵심 참조 자료의 중요한 누락을 발견하지 않았다. Matt 판본 차이의 파일 수와 Vercel의 `copywriting-eval` 범위 표현을 지적했고, Main이 원문과 Git으로 확인해 안내를 바로잡았다. 이 점검은 자료의 충실도와 출처 구분을 확인한 것이며 스킬 실행이나 워크플로 효과 검증은 아니다.

다음 논의는 이 자료를 **구현**, **검토 및 수정** 단위로 읽으며 각 방식의 입력·실제 행동·수정 권한·확인·반환을 대조하는 것이다. 현재 DEVELOPMENT·기존 스킬을 바로 재작성하거나 역할 수·최종 확인 담당을 먼저 확정하지 않는다. 상세 책임은 [01-01](../current/tickets/01-development-workflow/01-01-development-flow.md)과 [04-03](../current/tickets/04-skill-improvements/04-03-context-skills.md)에서 잇는다. 04-01 완료와 다른 세션의 04-02 진행은 유지한다.
