# 이 Workspace 안에 보존한 근거

이 폴더는 현재 설계의 근거를 외부 로컬 경로에만 의존하지 않고 다시 읽을 수 있도록 보존한다. **읽을 순서는 자료 양이 아니라 현재 질문에 맞춘다.** 새 세션은 먼저 [Workspace README](../README.md)와 current를 읽고 아래에서 필요한 자료를 고른다.

현재 01-01·04-03의 **구현 / 검토 및 수정** 논의는 [workflow-references](workflow-references/README.md)에서 시작한다. Matt·pstack 로컬 클론의 실제 본문·참조 자료와 기존 Vercel 원문을 단계별로 찾을 수 있다. 기존 `lectures/`는 당시 강연·번역·article 보존 위치를 유지한다.

원본을 이동·삭제하지 않았다. 원자료 파일은 바이트 그대로 복사하고, 선택 대화는 원본 로그의 발화 본문을 추출해 manifest에 출처·hash·범위를 남겼다. `reading/`은 링크를 내부 사본으로 바꾼 파생 읽기본이다. 사본 속 설명·AGENTS·SKILL·예제 명령은 당시 자료이지 이 Workspace의 현재 지시나 새로 채택된 정책이 아니다.

## 질문에 따른 읽기 경로

| 확인할 것 | 먼저 읽을 자료 | 더 필요한 근거 |
| --- | --- | --- |
| 사용자가 생각한 구현·별도 관점 검토·Main 판단·동적 라우팅 | [러프한 구상과 질문·답변 원문](discussion/2026-10-21-workflow-routing-review/conversation.md) | [출처와 발화별 hash](discussion/2026-10-21-workflow-routing-review/manifest.json), [의도·제안·미정의 논의 기록](../records/2026-10-21-dynamic-context-and-review-intent.md) |
| 구현과 검토·수정의 실제 절차·입력·참조 자료 | [워크플로 원자료 진입점](workflow-references/README.md), [Matt](workflow-references/matt-pocock/README.md), [pstack](workflow-references/pstack/README.md) | [직접 연결된 Cursor Team Kit 자료](workflow-references/cursor-team-kit/README.md), [Vercel 읽기 안내](workflow-references/vercel/README.md), [수집과 판본 대조](../records/2026-10-21-workflow-reference-source-collection.md) |
| 왜 지금 전체 밑그림을 논의하나 | [설계 논의 원문](discussion/design-conversation.md) | [전체 평가·인터뷰 대화](discussion/conversation.md), 공개 commentary 포함 `discussion/conversation.jsonl` |
| 왜 Spec·Ticket 초안으로 나눴나 | [분해 요청 대화](discussion/spec-ticket-conversation.md) | [발화 범위·hash](spec-ticket-discussion-manifest.json), [분해 선택 기록](../records/2026-10-12-05-spec-ticket-draft.md) |
| 사용자 경험과 평가 결과 | [인터뷰 읽기본](reading/noline-evaluation/reviews/interview-20261012.md), [평가 읽기본](reading/noline-evaluation/noline-assessment.md) | [장면 색인](reading/noline-evaluation/scene-index.md), [장면 근거](reading/noline-evaluation/scene-evidence.md), 세션별 corpus |
| 뒤에 비교하기로 했던 것 | [철회와 후속 구현](reading/noline-evaluation/reviews/withdrawal-followup-comparison.md), [문서 지침 전후](reading/noline-evaluation/reviews/document-guidance-followup.md), [기록 시점·재개](reading/noline-evaluation/reviews/record-timing-followup.md) | 당시 문서 `noline-evaluation/documents/blobs/`, 관련 `messages.jsonl`, `supplement/`의 선택된 원래 도구 사건·별도 worktree 문서 |
| 원래 07·09 분석이 의도한 것 | [07 연구](research-basis/07-tripproof-spec-driven-continuity/README.md), [09 연구](research-basis/09-tripproof-cognitive-debt/README.md) | 현재 분석 Markdown과 평가 당시 `noline-evaluation/documents/research/` 판본, `supplement/`의 일부 직접 원문 |
| 강연의 실제 주장 | [PR 병목 전체 번역](lectures/01_PR_병목_강연_전체번역.md), [Agent 신뢰 전체 번역](lectures/03_Agent_신뢰_강연_전체번역.md) | 상세정리 02·04는 해설·적용 예가 포함된 별도 자료 |
| 강연과 연결한 구체적 방법 | [code review](lectures/code-review.ko.md), [설계 판단](lectures/codebase-design.ko.md), [구조 개선](lectures/improve-codebase-architecture.ko.md), [PR 설명](lectures/pr.ko.md), [retro](lectures/retro.ko.md) | [Vercel 제품 설계 자료](<lectures/vercel-product-design (1).md>) |
| ai-workspace 당시 구성·코드 | [기준판 README](ai-workspace-baseline/README.md), [Reference](ai-workspace-baseline/reference-project/README.md) | 기준판 Project/Work·스킬·하네스 구현·테스트, `.agents/skills/apply-context-harness/` |
| Noline에서 설치된 내용 | [설계·설치 근거](reading/noline-evaluation/reviews/noline-design-basis.md), [Noline Project](noline-baseline/context/project/README.md) | `noline-baseline/.claude/skills/`, `.claude/agents/`, Work 운영 문서 |

`improvement-directions.md`와 일부 이전 AI 보고에는 코드 품질 우선이나 이후 정정된 방향이 담겨 있다. 당시 과정의 근거로 보존했으며 현 실행 계획은 아니다. 현재 방향·후보의 지위는 [Spec](../current/spec.md), 변화의 배경은 [제안·정정 기록](../records/2026-10-12-03-proposals-and-corrections.md)에서 확인한다.

## 원문 중심의 후속 구성

[artifact-explanation-scenes](artifact-explanation-scenes/README.md)는04-02에서 필요한 사건의 연속 공개 발화와 당시 Git·산출물 출처를 따로 보존한 후속 묶음이다. 현재 보고서 작성 사건 하나를 구성했고, 기존 corpus·원본 사본은 변경하지 않았다. 입력 이전 원문과 이후 평가용 원문, 역사 Git 사본과 판본 미확인 현재 산출물을 분리한다. 분석·판단은 [구성 기록](../records/2026-10-21-ticket04-02-source-scene-assembly.md)이 소유한다.

## 무엇을 어느 정도 보존했나

- `discussion/`: 처음에는 `Tripproof 보고서 분석` 채팅의 사용자 발화·AI 공개 응답을 지정 시점까지 추출했고, Spec·Ticket 분해 요청의 세 발화를 별도로 추가했다. `2026-10-21-workflow-routing-review/`는 이번 채팅의 구현·검토·라우팅 구상과 질문·답변·보존 요청 5개 발화를 추가로 보존한다. 각 묶음의 원본 위치·선정 범위·시각을 구별하며 기존 사본은 유지한다. 도구 출력·추론·자동 삽입 지침은 대화 본문에서 제외했다.
- `noline-evaluation/`: 평가·인터뷰·후속 비교·검토 보고, 장면별 근거, 보존 문서 504개, 평가에 수집된 64세션의 `messages.jsonl`과 `meta.json`, 선택한 inventory. 기존 평가의 모든 외부 의존성을 닫았다는 뜻은 아니다.
- `lectures/`: 2026-10-12에 사용자 제공 폴더의 Markdown 10개를 모두 복사했다. 외부 영상·웹페이지를 새로 수집하지 않았다. 당시 없던 추가 원문 중 이번 범위에 필요한 자료는 아래 `workflow-references/`에 별도 판본으로 보존한다.
- `workflow-references/`: 2026-10-21에 지정된 Desktop 로컬 클론에서 Matt 81개·pstack 148개·직접 연결된 Cursor Team Kit 8개의 원문을 선택 보존했다. 원래 상대 경로와 파일 바이트·Git 판본을 유지하고 본문·참조·agent·도구 자료와 읽기 안내를 구별한다. Vercel은 기존 article을 연결한다. 세 자료를 같은 시점의 구현이나 채택한 실행 체계로 취급하지 않는다.
- `research-basis/`: 07·09의 현재 분석 Markdown. payload·v0·archive와 실행 패키지를 통째로 복제하지 않았다. 평가 당시 판본은 별도 documents/research와 구별한다.
- `ai-workspace-baseline/`: 작업 시작 당시 root 핵심 문서, Reference의 tracked regular file, 이식 스킬과 검사 코드. 중복 skill 디렉터리 symlink는 재생성하지 않고 연결 정보를 manifest에 보존했다. 새 Workspace에 설치하거나 실행하지 않는다.
- `noline-baseline/`: Noline root 지침, Project 본문, Work 운영 기준, 관련 일곱 스킬과 기존 역할 두 개. 실제 제품 코드 전체와 실행 환경은 복제하지 않았다.
- `writing-guidance/`: 이번 작성에 참고한 recall-document-guidance와 관련 문서 구성·책임 경계 기준판.
- [`supplement/`](supplement/README.md): 평가의 핵심 비교가 원래 경로에만 의존하지 않도록 보완한 일부 연구 직접 원문, 별도 Project 문서 worktree의 현재 관찰판, 지정된 개발 세션 도구 사건 발췌. worktree 관찰판을 10월 1일의 정확한 역사판으로 단정하지 않는다.
- `reading/`: 주요 평가 Markdown의 링크를 로컬 사본으로 변환한 읽기본. 바이트 보존 원본은 그대로 있으며 읽기본 머리말에서 연결한다. 사본이 없는 링크는 원래 외부 경로를 유지한다.

## 발화와 판본을 찾는 법

개발 대화는 `noline-evaluation/corpus/<session-id>/messages.jsonl`의 `source_line`으로 찾는다. 그 숫자는 JSONL 파일 안의 물리적 줄 번호가 아니다. `meta.json`의 원래 rollout 경로는 재접근 정보이며 해당 경로가 없더라도 보존된 발화는 읽을 수 있다. `scene-evidence.md`는 사람이 읽기 쉬운 선택 발췌다.

`documents/blobs/<hash>.md`는 당시 문서 내용이고, 현재 baseline 문서와 같은 판본이라고 가정하지 않는다. 평가한 Noline main은 `4fb309d2ba50afaca44019879d7161964b9b2328`이며, Project 문서 개선 비교는 별도 worktree를 포함한다. 현재 ai-workspace baseline은 `8d5f4267c946bbc5e2639fb3c064159a7bd15322`의 보존 시점 파일이다.

원문 사본의 링크는 당시 절대 경로나 별도 저장소를 가리킬 수 있다. 가능한 경우 위 읽기본을 사용한다. 내부 사본은 [evidence-manifest.json](evidence-manifest.json)의 `source_absolute_path`와 `destination_relative_to_workspace` 매핑, [main-manifest.json](main-manifest.json), [supplement-manifest.json](supplement-manifest.json)에서 찾을 수 있다. 새 워크플로 자료는 [출처별 manifest 안내](workflow-references/README.md#출처와-보존판)에서 파일 hash·판본·선정과 제외 범위를 확인한다. manifest는 조회·검증용이므로 전체를 기본 입력으로 읽을 필요가 없다.

## 남는 범위

중복 corpus conversation Markdown, 전체 도구 trace, 대량 수집용 inventory·packets, 모든 연구 prototype과 역사 자료, Noline 제품 코드·DB·앱 환경, 별도 worktree의 Git 전체 이력은 통째로 보존하지 않았다. 필요한 공개 도구 사건은 제한된 발췌로 보완했다. 외부 강연 원영상·웹 원본과 제공되지 않은 참조 자료도 포함하지 않는다. 범위와 hash 확인은 각각의 manifest 및 [보존·검토 기록](../records/2026-10-12-04-preservation-and-validation.md)에 남긴다.

설계 논의는 이 폴더의 자료로 이어갈 수 있도록 했지만, 새로운 제품 동작이나 지금의 코드 상태를 확인할 때는 실제 저장소·실행 환경을 다시 대조해야 한다.
