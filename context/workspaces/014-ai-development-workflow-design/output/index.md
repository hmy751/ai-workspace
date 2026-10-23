# 현재 선택한 설계 자료와 산출물

7번 확정·8~12번 추천안: [첫 입력부터 수정·검증 인계까지](../records/2026-10-23-review-workflow-7-12-proposal.md). [두 개선 리뷰](../records/2026-10-23-review-workflow-7-12-improvement-reviews.md)를 거친 뒤 사용자가 관련 본문 읽기·대안 제공·레퍼런스 반영을 확인하고7번을 확정했다. 다음은8번 논의이며8~12번의 운영 선택 전체를 확정한 것은 아니다. 실행 본문 반영은 후속이다.

6번 현재 설계안: [맥락 이해·적용부터 구현 완성·인계까지](../records/2026-10-23-implementation-completion-and-handoff-proposal.md). 사용자 요청에 따라 맥락 적용과 개선 리뷰 두 보완을 통합했다. 실제 사용·변경 장면으로 자기 설계를 판단하고, 요구·계약에서 가져온 기대 결과로 자기 확인하며, Main에게 결과와 판단 근거를 연결한다. 아래 development 실행 prototype은1~5번 반영 상태이고6번 연결·수행 효과 확인은 후속이다.

04-02 현재 적용 기록: [explain 생성과 기존 두 실행 경로의 통합](../records/2026-10-23-ticket04-02-explain-prototype-adoption.md). 사용자 요청으로 리뷰 반영 구성을 prototype에 적용했다. 기존 두 스킬 제거를 감안하되 조항 전수 이식을 요구한 것은 아니라는 정정, 보존·검사·미확인 범위를 함께 읽는다. 운영 설치·새 응답 비교는 하지 않았으며 현재 재개 지점은 [04-02](../current/tickets/04-skill-improvements/04-02-artifact-explanation.md)다.

04-02 현재 산출물: [explain 본체](../records/prototypes/development-workflow/skills/explain/SKILL.md) · [설명 작성 상세](../records/prototypes/development-workflow/skills/explain/references/constructing-explanations.md) · [앞선 발화 상세](../records/prototypes/development-workflow/skills/explain/references/prior-explanation.md) · [형성 자료](../records/prototypes/development-workflow/skills/explain/_background/README.md). 기존 두 스킬 폴더는 삭제하고 당시 본문·형성 자료는 explain/_background/legacy에 보존했다. 아래 브리핑 비교·후보는 과거 판본의 이력이며 현재 explain 효과를 확인한 결과가 아니다.

구현·검토의 현재 산출물: [development SKILL.md](../records/prototypes/development-workflow/skills/development/SKILL.md)와 [review.md](../records/prototypes/development-workflow/skills/development/references/review.md). 확정1~5번과 구성 개선 리뷰를 반영하고 DEVELOPMENT 진입을 이전했다. [적용·확인 범위](../records/2026-10-23-development-skill-prototype-adoption.md)를 읽는다. 전체 실행 운영·효과 검증이나 Ticket 완료를 뜻하지 않는다.6번 통합안과7~12번 추천안은 위 별도 설계 기록에서 이어가며 실행 본문에 아직 반영하지 않았다.

04-02 새 후보 시험: [6.0 sol 인증 비교](../records/experiments/artifact-explanation-auth-depth-sol6-2026-10-22/comparison.md) — 원래 기존판 대비 새 후보가 요청 코드·값·대기 전후 설명을 보강했다. 각1회이며 일부 개선 관찰, 사용자 이해·일반화·시점 효과 미확인이다. 두 응답 전체와 입력·출력 해시를 보존했다.

04-02 최신 검토 후보: [코드 읽기 목적과 설명 깊이를 본문에 통합](../records/2026-10-22-ticket04-02-briefing-code-depth-candidate.md) — 목적 판별·코드와 값 연결·종료를 교체하고 형식 절의 중복 문장을 제거했다. 후보 작성 당시에는 운영 미적용·응답 효과 미검증이었다. 이후 시험·채택은 위 최신 기록을 따른다.

04-02 최신 실행: [6.0 sol 인증 비교](../records/experiments/artifact-explanation-auth-sol6-body-2026-10-22/comparison.md) · [6.0 luna 인증 비교](../records/experiments/artifact-explanation-auth-luna-body-2026-10-22/comparison.md) — 같은 입력·같은 적용 시점에서 모델별 기존/수정 각1회. 두 모델 모두 요약 중심이고 후보 개선은 미확인이다. [6.1-sol 인증](../records/experiments/artifact-explanation-auth-body-2026-10-22/comparison.md)·[network](../records/experiments/artifact-explanation-network-body-2026-10-22/comparison.md)의 양쪽 상세 설명과 구별한다. 원응답·해시·사실 대조를 보존했고 운영 반영·시점 비교는 미실행이다.

04-02 자료 보강: [당시 코드·최초 변경과 비교 설계](../records/2026-10-22-ticket04-02-historical-materials-and-comparison-design.md) — 네 장면의 압축 원문·코드·diff·검사 근거 확보. 시점 배치와 본문 비교를 구별한 실행안이다. 실행 현황은 위 최신 비교에서 확인한다.

**Ticket 03의 구성안·본문 예시는 완료됐다.** 현재 결과와 한계는 [03](../current/tickets/03-project-context.md), 완료 판단·후속 책임은 [119](../records/2026-10-20-119-ticket03-closeout.md)에서 확인한다. Workspace014 전체의 목표는 컨텍스트·코드 기준·절차·검증·기록·경험 반영이 연결된 개발 체계를 설계하는 것이다.

## 현재 결과를 읽는 곳

| 산출물 | 맡는 내용과 현재 지위 |
| --- | --- |
| [단일 적용 프로토타입](../records/prototypes/development-workflow/README.md) · [열람 화면](../records/prototypes/development-workflow/viewer.html) | 같은 폴더에서 발전시킨 본문·실행 예제·적용 장면. Markdown과 코드가 정본이며 화면은 표시 사본이다. 실제 운영 Noline에 설치한 결과는 아니다. |
| [Personal 개발 기준](../records/prototypes/development-workflow/noline-demo/context/personal/development/README.md) | 일반 판단과 조건·분할 본문·사례, 수정에 필요한 형성 자료. 개인 기준 전체 항목과 모든 문장의 최종 채택은01-02와 후속 적용에서 이어 본다. |
| [Project context](../records/prototypes/development-workflow/noline-demo/context/project/README.md) | 기기·세션 계약, 인증 개발 가이드, 코드 표현, 현재 인증 구현과 구성·읽기·관리 지침. 개인 기준의 채택·갱신 관리를 Project에 맡기지 않는다. |
| [CONTENT-POLICY](../records/prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md) | 지속 본문과 형성 자료의 역할·배치·읽기·갱신. 사례를 필수 서식으로 만들지 않으며 Work는 적용을 보류한다. |
| [SYSTEM-GUIDANCE](../records/prototypes/development-workflow/noline-demo/context/SYSTEM-GUIDANCE.md) | 체계 지침의 성격, 진입 본문·상세 지침의 책임과 이름·위치. [118](../records/2026-10-20-118-system-guidance-definition-and-entry.md)에 선택 이유와 확인 범위가 있다. |
| [Development](../records/prototypes/development-workflow/skills/development/SKILL.md) · [독립 검토](../records/prototypes/development-workflow/skills/development/references/review.md) · [작업 장면](../records/prototypes/development-workflow/walkthrough.md) | 공통 수행 계약과 검토 판단을 반영한 현재 prototype. Main의 맥락 재선택·종합·전달·갱신과 역할별 판단을 연결한다. 로그인 예제의 선택·계약은 Work·Project에 유지하며 상세 실행·운영 배치는 후속이다. |
| [Work 예시](../records/prototypes/development-workflow/noline-demo/context/work/README.md) | 기존 Spec·Ticket·current·source·output·records를 유지한 인증 이름 변경 작업. [116](../records/2026-10-20-116-defer-work-content-policy.md)의 복구 상태이며 새 background 정책을 적용한 표준이 아니다. |

본문의 목적·의미·조건은 대상물 안에서 이해할 수 있게 구성했다. 바깥014 records는 작성·평가·정정의 과정을 보존하며, 대상물 본문을 대신하는 정본이 아니다. 형성 이유를 다시 볼 필요가 있을 때는 본문 가까운 자료에서 시작한다.

## 전체 설계와 다른 Ticket의 입력

- [04-02 원래 스킬 형성 자료](../records/2026-10-21-ticket04-02-original-skill-background.md): 두 설명 스킬의 원래 목적·분리·조건부 보강·운영 연결을 각 _background에 복원했다. 기존 수정안은 보류 상태이고 형성 자료 구성은 채택·실제 효과 검증을 뜻하지 않는다.

- [04-02 첫 보고 책임 재판단](../records/2026-10-21-ticket04-02-first-report-responsibility-review.md): 새 source에서 확인한 목적·역할 합의와 실제 교정 근거를 대조한 현재 분석. 빠진 책임과 아직 확인하지 못한 실행 원인을 구별하며 수정안·시험 설계는 후속이다.

- [04-02 원문 중심 source](../source/artifact-explanation-scenes/README.md): 보고서·interceptor·network 흐름·저장 용량·여행 브리핑·Network 첫 완료 보고의 여섯 원문 묶음. 아래 최초 구성·추가 구성 기록은 당시 네 사건까지의 이력이며 최신 사례 상태는04-02에서 확인한다. [최초 구성](../records/2026-10-21-ticket04-02-source-scene-assembly.md)과 [추가 구성·시점/본문 비교 범위](../records/2026-10-22-ticket04-02-source-expansion-and-coverage.md)에 검증과 공백을 연결했다. 사건 요약이나 기대 답을 대신 공급하지 않으며, 당시 실행 전체의 재현 준비·스킬 효과 검증은 완료하지 않았다.

- [04-02 접근법·검증 재검토](../records/2026-10-21-ticket04-02-approach-and-evaluation-reset.md): 현재 판단 진입점. 첫 전달·조사·기준 적용과 사용자 교정 이후 재설명을 구별하고, 원인별 개입과 검증 방법을 다시 정했다. [두 스킬 재수정안](../records/2026-10-21-ticket04-02-original-intent-revision.md)과 기존 prototype은 보류한 후보이며 효과·채택이 확인된 현재 해법이 아니다.

- [스킬 본문 관리 정책](../records/prototypes/development-workflow/skills/SKILLS-CONTENT-POLICY.md): 스킬의 실행 본문·상세·형성 자료 구성과 갱신을 정하는 진입 지침. 정책과 작성 경로를 만들고 [work-discussion 형성 자료](../records/prototypes/development-workflow/skills/work-discussion/_background/README.md)에 적용했다. [형성 자료 이해·수정 판단과 소비 확인](../records/2026-10-21-ticket04-01-background-reading-check.md)에서 각1회의 읽기 결과를 확인했다. [작성·적용 마무리](../records/2026-10-21-skills-content-policy-and-work-discussion.md)에 전체 범위와 후속을 연결했다. 다른 스킬 적용은 후속이다.
- [04-02 세 장면 익명 응답 비교](../records/2026-10-21-ticket04-02-blind-response-comparison.md): 기존판·수정안 최초 응답 여섯 개와 독립 평가 두 개. 이번 범위에서 수정안의 우세는 확인하지 못했다. 통합안의 적용 효과나 실제 제품 검증으로 해석하지 않는다.
- [work-discussion prototype 본문](../records/prototypes/development-workflow/skills/work-discussion/SKILL.md): 04-01 설계 결과 완료. 기존 정의·보완 후보 대조와 요청별 반환의 최소안을 승인·반영했고 reconsider-work는 유지한다. [두 조건 수행 기록](../records/2026-10-21-ticket04-01-minimal-update-and-two-checks.md)에 확인과 한계가 있다. 사용자 위치 정정으로 Reference 수정은 원복했다. Reference·외부 Noline 설치나 운영 책임 변경은 포함하지 않는다.
- [04-02 두 설명 스킬의 본문 통합 수정안](../records/2026-10-21-ticket04-02-integrated-skill-drafts.md): 앞선 대조·정정·응답 예시를 반영한 전체 SKILL.md 후보. 기존 조건을 유지하고 중복을 본문에 합쳤다. [프로토타입의 실제 스킬 파일·변경점](../records/prototypes/development-workflow/skills/README.md)로 이어진다. 검토용이며 운영 미적용·효과 미확인이다.
- [04-02 설명 스킬 대조와 응답 제안](../records/2026-10-20-ticket04-02-skill-comparison-and-response-proposals.md): 사용자 정정에 따른 원문 재대조와 보완안. 근본 역할 우선·실제 코드와 흐름, 이전 보고와의 연속성, 설명과 적절성 판단을 구체화하고 Promise의 실패 해석을 낮췄다. 응답 예시·본문 후보는 미채택·미설치이며 상세 진행은 [04-02](../current/tickets/04-skill-improvements/04-02-artifact-explanation.md)가 맡는다.
- [Spec](../current/spec.md): 전체 목적·공통 기준·잠정안·선택·미정.
- [Ticket 목록](../current/tickets/index.md): 결과별 책임과 후속 연결.01-02·04-03 등의 완료 상태는03 완료로 함께 바꾸지 않는다.
- [01-02 기준 종합54](../records/2026-10-16-54-code-quality-criteria-and-remaining-work.md)와 [형식 반영72](../records/2026-10-18-72-short-common-and-detail-prototype.md): 코드 기준과 공통·상세·사례의 앞선 입력. [73](../records/2026-10-18-73-prototype-reservations-and-ticket03.md)의 당시 전체 만족 유보를 함께 읽고, 현재 본문은 위 단일 prototype에서 확인한다.
- [B 방향 선택15](../records/2026-10-12-15-reviewer-editing-choice-and-start.md): 검토자가 필요한 품질 수정을 직접 수행하는 당시 선택. 현재는 [사용자 후속 구상](../records/2026-10-21-dynamic-context-and-review-intent.md)의 별도 관점 검토·Main 적용 판단에 맞춰 상세 권한을 더 비교한다.
- [원자료 조사27](../records/2026-10-13-27-source-investigation-and-proposal-reset.md)와 [작업 단계 우선순위28](../records/2026-10-13-28-execution-system-priority-and-code-criteria.md): 외부 방식의 실제 계약과 사용자가 우선 구체화할 범위.
- [설계 논의 지도](../current/design-map.md): 다음 논의에서 필요한 전체 관점. 확정 분류가 아니다.

이전 날짜별 prototype·비교·선택 이유는 [기록 색인](../records/README.md)에 보존한다. 같은 결과를 output에 복제하거나 과거 기록 전체를 현재 산출물로 다시 열거하지 않는다. 이 지도에 연결된 사실은 운영 채택·설치·장기 효과의 확인을 뜻하지 않는다.
