# 구현과 검토·수정의 참고 자료

01-01 개발 흐름과 04-03 맥락 스킬 연결을 논의하기 위한 원자료 묶음이다. **구현**, **검토 및 수정**을 큰 읽기 단위로 삼고, 각 단계의 입력·설계·검사·인수·반환을 확인할 때 필요한 자료로 내려간다. 검증 자료는 두 단계의 결과를 확인하는 데 함께 읽는다. 이 구분은 자료 탐색용이며 역할 수나 고정 실행 순서를 정한 운영안이 아니다.

2026-10-21에 사용자가 지정한 `Desktop/skills`와 `Desktop/plugins/pstack`의 로컬 클론에서 관련 파일을 보존했다. pstack이 직접 참조하는 같은 `plugins` 저장소의 Cursor Team Kit 일부도 별도 출처로 보존했다. Vercel은 기존 `lectures/` 원문을 연결한다. 현재 채택·비교 판단과 수집 과정은 [구성 기록](../../records/2026-10-21-workflow-reference-source-collection.md)이 맡는다.

## 먼저 읽을 자료

| 보고 싶은 것 | 실제 본문으로 들어갈 곳 |
| --- | --- |
| 구현 인수, 한 작업과 여러 Ticket의 실행 | Matt의 [implement](matt-pocock/repository/skills/engineering/implement/SKILL.md)·[implement-spec](matt-pocock/repository/skills/engineering/implement-spec/SKILL.md), pstack의 [Feature](pstack/repository/skills/poteto-mode/playbooks/feature.md)·[Bug fix](pstack/repository/skills/poteto-mode/playbooks/bug-fix.md)·[Refactoring](pstack/repository/skills/poteto-mode/playbooks/refactoring.md) |
| 구현 중 설계와 테스트 경계 | Matt의 [TDD와 상세](matt-pocock/repository/skills/engineering/tdd/SKILL.md)·[codebase-design과 상세](matt-pocock/repository/skills/engineering/codebase-design/SKILL.md), pstack의 [architect](pstack/repository/skills/architect/SKILL.md)·[arena](pstack/repository/skills/arena/SKILL.md) |
| 검토의 관점, 지적의 판단, 실제 수정 | Matt의 [code-review](matt-pocock/repository/skills/engineering/code-review/SKILL.md), pstack의 [interrogate](pstack/repository/skills/interrogate/SKILL.md)·[no-comments](pstack/repository/skills/no-comments/SKILL.md)와 [Comment Sicko](pstack/repository/agents/comment-sicko.md), Cursor Team Kit의 [deslop](cursor-team-kit/repository/skills/deslop/SKILL.md) |
| 구현·수정 결과의 실제 동작 확인 | pstack의 [검증 스킬 생성](pstack/repository/skills/create-verification-skill/SKILL.md)·[유지](pstack/repository/skills/maintain-verification-skill/SKILL.md)·[blast-radius](pstack/repository/skills/blast-radius/SKILL.md), [UI·CLI 제어와 주장 확인 자료](cursor-team-kit/README.md) |
| 필요한 제품 기준 선택, 구현·검토 모드와 결과 확인 | [Vercel 원문 읽기 안내](vercel/README.md). 원문은 내부 제품 설계 체계의 설명과 축약 예시이며, 내부 reference 전체를 확보한 자료는 아니다. |
| 앞뒤 단계의 맥락과 문서·도구 연결 | [Matt 자료 안내](matt-pocock/README.md), [pstack 자료 안내](pstack/README.md)에서 입력 생성·진단·인계·보고·환경 개선 및 조건부 playbook을 고른다. |

처음에는 해당 질문의 본문만 읽고, 그 본문이 참조하는 상세·예시·agent prompt를 이어 읽는다. 원 저장소의 전체 README와 사용자 가이드는 사용 맥락을 설명하며, 개별 SKILL·agent·playbook과 서술이 다를 수 있다. 차이를 판단할 때 해당 원문을 함께 대조한다.

## 출처와 보존판

| 자료 | 보존 범위와 판본 | 출처 확인 |
| --- | --- | --- |
| [Matt Pocock](matt-pocock/README.md) | 관련 원문 81개. 로컬 `mattpocock-skills` 1.3.1, Git `5beb35b040e3de97e54fa9e386d7e42d15c295c2` | [파일별 manifest](matt-pocock/manifest.json) |
| [Lauren Tan의 pstack](pstack/README.md) | 관련 원문 148개. 로컬 0.15.29, `cursor/plugins` Git `190d28736eff128ec94f502a22c7fe0c4b56cd37` | [파일별 manifest](pstack/manifest.json) |
| [Cursor Team Kit 연결 자료](cursor-team-kit/README.md) | 직접 연결된 네 스킬과 출처 파일 8개. Eric Zakariasson의 별도 plugin 1.2.0, pstack과 같은 저장소·Git 판본 | [파일별 manifest](cursor-team-kit/manifest.json) |
| [Vercel 제품 설계 글](vercel/README.md) | John Phamous, 2026-06-25 게시. 2026-10-12에 보존한 기존 원문 한 편을 재사용 | [기존 원자료 manifest](../evidence-manifest.json), [연결 정보](vercel/provenance.json) |

로컬 클론의 보존 시점과 웹의 최신 판본은 다르다. 세 로컬 묶음의 `repository/`에는 원래 상대 경로와 파일 바이트를 유지했다. Git 내부 파일과 설치된 실행 환경은 복사하지 않았다. Manifest에는 출처 경로·Git 판본·파일별 크기와 SHA-256·선정 범위·제외 항목·남은 의존이 있다.

## 기존 강연 및 조사와의 관계

- [Matt 강연 전체 번역](../lectures/01_PR_병목_강연_전체번역.md)과 [Lauren 강연 전체 번역](../lectures/03_Agent_신뢰_강연_전체번역.md)은 강연 주장의 보존본이다. 같은 폴더의 상세정리에는 정리자의 해설·적용 예가 섞여 있다.
- `lectures/`의 다섯 Matt 스킬 번역은 당시 제공판이다. 이번 원문 보존판과 같은 commit의 번역이라고 가정하지 않는다.
- [Matt 조사24](../../records/2026-10-13-24-matt-source-investigation.md), [Lauren 조사25](../../records/2026-10-13-25-lauren-source-investigation.md), [Vercel 조사26](../../records/2026-10-13-26-vercel-source-investigation.md)은 각 조사 시점의 분석이다. 특히 pstack은 이번 0.15.29와 과거 0.15.21·0.15.25를 구별한다.

## 보존과 관리

이 묶음은 Workspace014의 원자료이며 설치된 skill이나 현재 실행 지침이 아니다. `repository/` 안의 SKILL·agent·명령·설정은 분석 대상이다. 실제 호출 권한, 제품·전역 하네스의 변경 권한을 부여하지 않는다.

원문 사본과 기존 강연·manifest를 수정해 판본을 섞지 않는다. 다른 판본을 수집할 때는 새 보존 단위로 두고 출처와 관계를 기록한다. 이 README와 출처별 README는 읽기 경로·보존 범위를 안내한다. Workspace Main이 안내와 출처 연결을 관리하고, 설계 해석·선택·검증 결과는 `records/`와 `current/`에 남긴다.

선택 보존이므로 원 저장소의 README·가이드에는 이번 범위 밖 형제 자료로 가는 링크가 남아 있다. 외부 서비스, 실행 host, 대상 프로젝트의 실제 코드·Spec·검증 환경도 사본에 포함되지 않는다. 자세한 제외와 의존은 각 manifest에서 확인한다.
