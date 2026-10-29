# 06-01 — Maintain을 유지한 Reference 첫 적용

2026-10-29. **Personal·Project 관리·공통 읽기·한정 반영·설명 묶음을 Reference에 적용하고 직접 확인했다.** Maintain·Work 기록 담당·생성/전환은 현행을 유지했다. 전체06-01 완료, 새 host의 자동 발견·호출, Noline 재적용은 아직 아니다.

사용자 승인 범위:

> 그래 그럼 maintain 관련은 02에서 하는 걸로 두고, 먼저 가능한 부분부터 reference-project에 반영해봐. 기존 내용이랑 합의도 잘 지키고.

[전환 검토안](2026-10-29-ticket06-01-reference-transition-proposal.md)의 독립적인 첫 묶음에 대한 후속 실행이다. 앞선 검토안 전체나 Maintain 제거안을 일괄 채택한 것이 아니다. [06-01](../current/tickets/06-framework-transition/06-01-reference-project-application.md)이 남은 범위를 소유한다.

## 적용 결과와 소유 위치

| 선택 | 실제 결과와 이유 |
| --- | --- |
| 추가 | [로컬 Personal](../../../../reference-project/context/personal/README.md)에 판단·조건별 사례·경험 모음과 형성 자료를 배치했다. 개인 기준의 채택, 경험 관찰, 열린 후보를 구별하고 기존 제품 계약을 대체하지 않는다. |
| 추가·적응 | [USAGE](../../../../reference-project/context/USAGE.md), CONTENT-POLICY, SYSTEM-GUIDANCE와 근거 자료를 연결했다. Work의 새 정책 적용은 유보하며 Reference 안에 없는 development·improvement-loop를 필수 호출하지 않는다. |
| 유지·보완 | [Project](../../../../reference-project/context/project/README.md)의 실제 제품 의미와 common/current/guidance/decisions를 유지하고 읽기·관리·구성 진입을 새 방법에 연결했다. demo의 인증 제품·Workspace를 가져오지 않았다. |
| 교체 | read-project-context는 USAGE·Project 읽기 기준으로, update-project-context는 [context-update](../../../../reference-project/.agents/skills/context-update/SKILL.md)로 교체했다. 한정 반영은 Personal·Project에만 쓰고 Work 영향은 기존 Main·Maintain 경로로 연결한다. |
| 교체·이동 | work-artifact-briefing·explanation-recovery의 실행 폴더를 [explain](../../../../reference-project/.agents/skills/explain/SKILL.md)으로 통합하고 공통 설명 기준을 skills/shared로 옮겼다. 형성 자료와 이전 프로토타입 판본은 보존한다. |
| 유지 | create-context-workspace·reconsider-work는 원본과 설정을 유지했다. work-discussion은 공통 기준 링크만 바꾸고 명시 호출 조건과 Work 기록 계약을 보존했다. |
| 연결 | [스킬 색인](../../../../reference-project/.agents/skills/README.md), root·context·Project 진입, 새 두 스킬의 Codex metadata, Claude/Codex 상대 연결을 맞췄다. 설치 스킬은5개, 각 host 연결은4개다. create는 기존 root 진입으로 찾는다. |
| 소비자 보정 | [이식 판단 문서](../../../../.agents/skills/apply-context-harness/references/application-contract.md)의 폐기된 스킬 이름·공통 기준 경로만 현행 소유 관계에 맞췄다. Personal 자료 선택도 출처·한계를 보존하도록 연결했다. Maintain 설치·binding·activation·fallback 계약은 그대로다. |

Personal 경험은014 설계와 당시 확인한 Noline 사건의 기록이며 Reference에서 관찰한 효과가 아니다. 과거 사례·후보를 채택 기준으로 올리지 않았다. 현재 실행 자료는 Reference 안에서 찾고, 바깥 장문 원자료·과거 prototype 연결은 재검토용 출처로 남겼다. 설명용 인증 예시는 실행 방법을 보여 주는 사례로 유지하며 Reference의 Request policy 제품에 새 요구를 부여하지 않는다.

## 보존과 직접 확인

- 적용 전 `56643f48f355aca017554149687982d02af7d434`와 작업 트리를 기준으로 파일·symlink를 대조했다. 제품 코드·검사, 제품 common/current/decisions, Work 전체·Workspace JSON·current·원자료·receipt·status, Maintain 등록·hook·wrapper·ignore가 동일하다. 이전 source prototype도 diff가 없다.
- Reference root에서 `python3 -m unittest tests.test_config_loader context.work.harness.validation.tests.test_ephemeral_workspace_state_preservation -v`: 제품7개와 임시 fixture의 순환·기존 machine state 보존1개, 총8개 통과.
- `python3 -m context.work.harness recover 001-default-timeout`와 id 없는 `recover`: 둘 다 성공. 기본 선택에서 `workspaces/index.json`을 읽는 한 줄만 다르며 본문은 같다. 과거 평면 Project 경로에 대한 receipt의 `stale`을 그대로 보존했다. durable Verify·새 receipt·activation은 실행하지 않았다.
- 새/변경 Reference Markdown의 상대 파일 링크696개와 앵커201개를 확인했다. 누락0. 복사 과정에서 확인한 기존 설명 배경의 앵커4개를 실제 제목에 맞췄다. 날짜별 원문·코드 발췌는 고치지 않았다.
- Python quick_validate는 PyYAML 부재로 실행되지 않았다. Ruby YAML.safe_load로5개 frontmatter·호출 metadata를 읽고 필드·이름·description·새 short_description·default_prompt·정책과8개 상대 연결을 대체 확인했다. work-discussion의 implicit=false가 유지된다. 새 host discovery를 검증한 것은 아니다.
- `git diff --check` 통과. 원본·대상 파일별 hash와 보존 범위, 검사 구별은 [기계 대조 결과](receipts/reference-application/2026-10-29-phase1.json)에 남겼다.

## 본문을 실제 질문에 대입한 확인

Main이 새 root→USAGE→Project 경로를 따라 “timeout을 생략하거나 boolean을 주면 무엇을 보장하나”를 읽었다. PRD·5000ms normative 결정·실제 config loader를 대조해, 생략은5000이며 bool은 Python에서 int의 하위 타입이어도 거부한다는 계약을 복원했다. 네트워크 요청 성공·화면 동작으로 증거를 확대하지 않았다. 위 제품 테스트가 그 동작을 직접 확인한다.

Personal의 이름·완료 사례는 제품 계약을 새로 채택하는 권한이 아니라 판단 관점이다. RequestPolicy를 인증 demo로 바꾸거나 사례의 코드 모양을 강제하지 않는 경계를 확인했다. context-update의 실제 이식에서는 기존 Project 본문을 보존하면서 진입·관리 링크만 맞췄으며, Work current와 machine 상태를 이 스킬의 쓰기 대상으로 추가하지 않았다.

explain 본체→작성 상세·앞선 발화 상세→공통 근거 기준의 읽기 조건을 대조했다. 설명 요청은 근거 확인과 추천까지 가능하지만 제품 수정·수락·Work 기록 담당 변경 권한을 자동 부여하지 않는다. 이 확인은 Main의 본문 대조이며 독립 실행자 실험이나 새 host의 호출 관찰이 아니다.

## 후속과 복구

Maintain과 연결되는 development·새 work-discussion·create 적응·improvement-loop 활성화는02의 채택 결과와 함께 판단한다. 01-02의 병렬 분석·미채택 제안은 수정하거나 현재 기준으로 올리지 않았다.06-02는 이후 확인한 판본을 Noline의 기존 설치와 대조하며, 지금 부분 적용을 전체 기준의 배포 완료로 취급하지 않는다.

되돌릴 때는 위 기준 commit과 receipt의 정확한 변경 목록을 사용한다. 삭제한 네 스킬·옛 guidance·도구 연결과 변경한 기존 진입을 복원하고 이번에 추가한 Reference 파일·연결만 선택해 되돌린다. 그 전에 이후 사용자·병렬 변경을 다시 대조한다. 전체 저장소 reset·clean으로01-02·02나 Work 기록을 되돌리지 않는다. explain의 legacy 원문은 과거 프로토타입판이며 적용 직전 Reference의 정확한 복구본은 기준 commit이다.

첫 적용 확인 시점에는 커밋·push를 하지 않았다. 후속 사용자 요청으로 이 기록과06-01 변경을 함께 커밋한다. 병렬01-02 문서와 공유 진입점의 해당 변경은 커밋에서 제외하며 작업 트리에 보존한다. Push는 요청하지 않아 수행하지 않는다. 새 host별 발견·호출, 실제 사용자 설명 경험, 전체 개발·경험 개선 흐름은 남은 관찰이며 설치·링크·제품 회귀 통과로 대신하지 않는다.

## 후속 확인 — 스킬 원본과 도구별 연결

사용자는 “근데 왜 .codex와 .agents에 둘다 스킬이 있어?”라고 물었고 설명 뒤 “아 이해됐어 일단 기록할거 하고 커밋하자 그리고 더 보완하거나 구체화 논의해야할게 있는지 말해주고”라고 요청했다.

실제 파일을 다시 확인했다. `.agents/skills/`는 원본이며 `.codex/skills/`와 `.claude/skills/`의 네 항목은 같은 원본을 가리키는 상대 symlink다. 두 본문을 별도로 유지하거나 복제한 구조는 아니다. 이번 적용에서는 기존 도구별 연결 방식을 유지했다. 현재 Codex에서 `.codex/skills` 연결이 추가로 필요한지, 같은 원본이 중복 발견되는지는 아직 검사하지 않았다. 사용자의 이해 응답을 그 구조의 필수성 확인이나 제거 승인으로 해석하지 않는다.

## 다음 보완과 논의의 구별

| 남은 일 | 먼저 구체화할 내용 | 판단 위치 |
| --- | --- | --- |
| 현재 설치의 실제 사용 확인 | Reference에서 시작한 새 Codex·Claude 세션이 어떤 경로로 스킬을 찾는지, 동일 원본의 중복 노출 여부, 명시 호출·자동 선택 조건, 설명과 한정 반영의 대표 장면을 확인한다. 정적 링크 검사를 대신하는 실제 관찰이며, 결과 전에는 연결 제거를 결정하지 않는다. |06-01의 확인 과제. 새 설계 합의가 필요한 일과 조사로 답할 일을 구별한다. |
| 보류한 실행·기록 연결 |02가 채택한 Work 기록 담당·반영 시점·생성/전환 계약을 받아 development·work-discussion·create·improvement-loop에 연결한다. 중간에 Main 직접 기록을 임의 활성화하지 않는다. |02와06-01의 연결 선택.02 진행을 이 세션에서 대신하지 않는다. |
| Noline에 넘길 범위 | Reference 공통 방법, 대상의 제품 계약, 기존 개인 기준·경험을 구별해 유지·병합·제외할 항목을 정한다. Reference의 경험 사례를 Noline에서 새로 발생한 기록으로 복사하지 않는다.01-02에서 나중에 채택한 품질 기준도 현재 적용판과 대조해 반영한다. |06-02 착수 때 대상 현행과 대조한다. 지금 새 동기화 도구나 자동 배포를 만들지 않는다. |

현재 가장 먼저 권하는 것은 새 host의 발견·호출과 대표 사용 장면 확인이다. 검사 없이 지침을 더 늘리기보다 실제 누락·중복·불충분이 드러난 부분을 보완한다. 전체06-01 마감과06-02 재적용은 남은 연결·확인과 구별한다.
