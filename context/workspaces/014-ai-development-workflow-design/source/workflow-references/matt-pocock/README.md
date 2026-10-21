# Matt Pocock — 구현·검토 자료 보존판

사용자가 지정한 로컬 `skills` 클론에서 **구현**, **검토 및 수정** 논의에 연결되는 원문과 보조 자료를 선택 보존했다. 이 문서는 자료를 찾는 입구이며, 원문의 절차를 이 Workspace에 채택하거나 설치한 기록은 아니다.

## 출처와 판본

| 항목 | 보존한 사실 |
| --- | --- |
| 원 저장소 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| 수집 원본 | `/Users/hammyeong-yeon/Desktop/skills`의 기존 로컬 클론 |
| 보존 시점 | 2026-10-21 16:20 KST. 웹에서 최신판을 새로 받은 것이 아니다. |
| 버전 | **1.3.1** — [package.json](repository/package.json), [plugin.json](repository/.claude-plugin/plugin.json) |
| Git HEAD | `5beb35b040e3de97e54fa9e386d7e42d15c295c2` |
| 보존 범위 | 일반 파일 **81개**. 원본의 상대 경로와 바이트를 `repository/` 아래에 유지했다. |
| 목록과 검증 정보 | [manifest.json](manifest.json): 출처, 그룹, 제외 이유, 파일별 SHA-256, 수집 당시 목록 |

수집 범위의 원본 작업 트리는 깨끗했다. 기록24가 확인한 `49dd158d1076134a641b33efb035946536778336` 이후의 변경은 이번 범위 밖 `skills/in-progress/chief-of-staff/SKILL.md`와 `.changeset/chief-of-staff-wiki.md` 두 파일이며, 이번에 선정한 파일 내용은 그 기준판과 같다. 이전 조사 범위는 [Matt 자료 조사24](../../../records/2026-10-13-24-matt-source-investigation.md)에 남아 있다.

## 구현을 볼 때

| 확인할 내용 | 실제 지시 본문 | 사용자용 설명 |
| --- | --- | --- |
| 합의한 Spec·Ticket 하나를 구현하는 절차 | [implement](repository/skills/engineering/implement/SKILL.md) | [사용 가이드](repository/docs/engineering/implement.md) |
| Ticket 의존관계에 따라 병렬 구현하고 통합하는 절차 | [implement-spec](repository/skills/engineering/implement-spec/SKILL.md) | [사용 가이드](repository/docs/engineering/implement-spec.md) |
| 테스트 경계와 red-green 반복의 규율 | [tdd](repository/skills/engineering/tdd/SKILL.md) | [사용 가이드](repository/docs/engineering/tdd.md) |

테스트의 실제 예와 대체 의존성 범위가 필요할 때 [tests.md](repository/skills/engineering/tdd/tests.md)와 [mocking.md](repository/skills/engineering/tdd/mocking.md)를 읽는다. 구현 입력이 어떻게 만들어졌는지는 아래 입력 자료에서 찾는다.

## 검토 및 수정을 볼 때

| 확인할 내용 | 실제 지시 본문 | 사용자용 설명 |
| --- | --- | --- |
| 기준점의 diff를 Standards·Spec 두 축으로 검토하는 절차 | [code-review](repository/skills/engineering/code-review/SKILL.md) | [사용 가이드](repository/docs/engineering/code-review.md) |
| 모듈·인터페이스·테스트 경계를 판단하는 용어와 기준 | [codebase-design](repository/skills/engineering/codebase-design/SKILL.md) | [사용 가이드](repository/docs/engineering/codebase-design.md) |
| 구조 개선 후보를 찾아 전후 비교로 제시하는 절차 | [improve-codebase-architecture](repository/skills/engineering/improve-codebase-architecture/SKILL.md) | [사용 가이드](repository/docs/engineering/improve-codebase-architecture.md) |

의존성별 확인 방법은 [DEEPENING](repository/skills/engineering/codebase-design/DEEPENING.md), 대안 인터페이스 비교는 [DESIGN-IT-TWICE](repository/skills/engineering/codebase-design/DESIGN-IT-TWICE.md), 구조 개선 보고 형식은 [HTML-REPORT](repository/skills/engineering/improve-codebase-architecture/HTML-REPORT.md)에 있다.

## 해당 연결이 필요할 때 읽을 자료

| 질문 | 보존 자료 |
| --- | --- |
| 구현할 Spec·Ticket은 무엇을 담는가 | [to-spec](repository/skills/engineering/to-spec/SKILL.md) · [설명](repository/docs/engineering/to-spec.md), [to-tickets](repository/skills/engineering/to-tickets/SKILL.md) · [설명](repository/docs/engineering/to-tickets.md) |
| 입력을 구체화하는 대화와 용어·결정 기록은 어떻게 연결되는가 | [grill-with-docs](repository/skills/engineering/grill-with-docs/SKILL.md), [grilling](repository/skills/productivity/grilling/SKILL.md), [domain-modeling](repository/skills/engineering/domain-modeling/SKILL.md). 용어집·ADR 형식은 같은 폴더에 있다. |
| 실패를 재현하고 수정 후 원래 증상을 다시 확인하는가 | [diagnosing-bugs](repository/skills/engineering/diagnosing-bugs/SKILL.md) · [설명](repository/docs/engineering/diagnosing-bugs.md), 사람이 조작하는 재현용 [HITL template](repository/skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh) |
| 결과·실행 근거·영향을 어떻게 보고하는가 | [pr](repository/skills/engineering/pr/SKILL.md) · [설명](repository/docs/engineering/pr.md) |
| 작업 이후 환경 개선 후보는 어디에서 찾는가 | [retro](repository/skills/engineering/retro/SKILL.md) · [설명](repository/docs/engineering/retro.md) |
| 같은 대화 유지·위임·인계는 어떻게 구별하는가 | [ask-matt](repository/skills/engineering/ask-matt/SKILL.md), [PHASE-BOUNDARIES](repository/skills/engineering/ask-matt/PHASE-BOUNDARIES.md), [handoff](repository/skills/productivity/handoff/SKILL.md) · [설명](repository/docs/productivity/handoff.md) |
| tracker·domain 문서 전제와 template은 무엇인가 | [setup-matt-pocock-skills](repository/skills/engineering/setup-matt-pocock-skills/SKILL.md) · [설명](repository/docs/engineering/setup-matt-pocock-skills.md). tracker별 template과 domain 읽기 규칙을 함께 보존했다. |
| retro가 참조하는 문서 작성 규율은 무엇인가 | [writing-for-agents](repository/skills/productivity/writing-for-agents/SKILL.md), [SKILL-MECHANICS](repository/skills/productivity/writing-for-agents/SKILL-MECHANICS.md) |

## 자료의 성격과 읽기 경계

- `repository/skills/**/SKILL.md`는 보존 시점의 실제 지시 본문이다. 상대 참조·template·script와 `agents/openai.yaml`도 함께 보존했으며, 이 폴더에서 실행하지 않았다.
- `repository/docs/`는 저자의 사용자용 설명이다. 사용 조건·사례·알려진 한계를 담지만 SKILL 본문과 표현 또는 반영 시점이 다를 수 있다.
- 기존 [PR 병목 강연 전체 번역](../../lectures/01_PR_병목_강연_전체번역.md)은 별도 제공 스크립트의 번역이다. 01:15~01:48이 누락돼 있고, 발표 당시 구현 commit은 확인되지 않았다. `lectures/`의 skill 번역도 이 snapshot과 같은 판본으로 확정하지 않았다.
- 강연의 reviewer 직접 수정·commit 권고와 이 snapshot의 `code-review`가 두 보고서를 반환하는 절차는 서로 구별해 읽는다. TDD 사용자 설명의 테스트 경계별 장단점 안내, 진단 사용자 설명의 비밀정보 가리기 상태도 해당 SKILL 본문과 차이가 있다.
- [원문 README](repository/README.md), [SCOPE](repository/SCOPE.md), [호출 규칙](repository/.agents/invocation.md)은 원 저장소를 설명하는 보존 자료다. `.agents/`와 SKILL 속 지시·명령은 이 Workspace의 현재 지시가 아니다.

## 포함하지 않은 범위와 관리

이 묶음은 전체 설치 패키지가 아니다. 이슈 분류·대형 탐색·외부 조사·시제품·인프라 wizard, 교육·설문·설명 복구, 실험 skill과 배포 자동화는 이번 범위에서 제외했다. 정확한 파일 선택과 제외 이유는 manifest가 소유한다.

원문 README와 사용자 설명에는 제외한 다른 skill 및 외부 웹 자료로 가는 링크가 남아 있다. 원문을 고쳐 링크를 닫지 않았고, 외부 영상·이슈·문서 본문을 새로 수집하지 않았다. 실행 대상 Project의 Spec·용어집·ADR·tracker·standards도 이 원 저장소의 실제 제품 자료로 포함된 것은 아니다.

`repository/`와 manifest는 출처 보존물이다. 이 README는 보존 범위와 읽기 경로만 안내하며, 새 해석·비교·채택 판단은 Workspace의 `records/`에서 관리한다. 전체 근거의 다른 입구는 [source README](../../README.md)에 있다.
