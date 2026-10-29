# 06-01 — Reference의 유지·교체·제거 전환 검토안

후속 상태: 사용자가 독립적인 첫 묶음의 실제 반영을 승인했고 [첫 적용 기록](2026-10-29-ticket06-01-reference-partial-application.md)에 변경·검사·유보를 남겼다. 아래는 적용 전에 작성한 전체 검토안이다. 과거의 “미반영·논의 전”은 당시 상태이며 모든 권고가 채택됐다는 뜻이 아니다.

2026-10-29. **논의용 권고안이다. Reference에 실제 반영하지 않았고 아래 선택을 새 합의로 확정하지 않았다.** [06-01](../current/tickets/06-framework-transition/06-01-reference-project-application.md)의 첫 결과로, 기존 합의와 현행 파일·호출 관계를 대조했다.

사용자 요청:

> 그럼 이제 06-01 시작하자. 관련 기록이랑 합의들을 꼼꼼히 확인해서 reference-project에서 유지·교체·제거할 부분을 구체적으로 정리해봐. 실제 반영은 그걸 보고 논의하자.

## 현재 진행 범위 — Maintain은02와 함께 다룬다

후속 사용자 요청:

> maintain 관련은 02티켓하고 하게 일단 냅두자 냅두고 가능하나?

**Maintain 관련은 현행대로 두고02와 함께 다룬다.06-01은 그 책임과 충돌하지 않는 context·설명 묶음부터 논의·구체화할 수 있다.** 이 요청은 Maintain의 영구 존치 선택도, 나머지 실제 반영의 착수 지시도 아니다. 앞선 실제 반영 전 논의 경계는 유지한다.

| 지금 나눌 범위 | 진행 방법 |
| --- | --- |
| 먼저 구체화·적용을 논의할 수 있음 | Reference 제품·Project 사실 보존, 로컬 Personal 기준·경험, 공통 정책·USAGE, Project 읽기·관리의 비충돌 부분, explain·shared와 두 설명 스킬 전환. context-update도 Personal·Project 한정 반영과 Work 영향의 현행 담당 연결로 적응할 수 있다. Main의 Personal·Project 편집 자체는 Work Maintain과 충돌하지 않는다. |
| 대상 계약에 맞춘 연결 범위를 먼저 대조 | create·improvement-loop. 생성·인수나 Personal 경험 검토는 가능하지만 실제 전환·Work 재개 지점 기록·한정 시도 종료는 현행 생성/갱신 담당에 연결해야 한다. demo 계약이나 미설치 스킬 링크를 그대로 복사하지 않는다. |
| 본문·경로 준비 가능, 운영 활성화는02 연동 유보 권고 | development·work-discussion의 현행 prototype판은 Main의 Work 직접 갱신과 자동 Maintain 미연결을 명시한다. 구현·검토·검증·설명의 비충돌 내용은 준비하되, 임시 변형판을 운영하고 다시 바꾸는 비용을 피하려면 기록 조항·실제 활성화는02 결과와 함께 잇는다. |
|02와 함께 다룰 때까지 현행 유지 | Maintain 코드·agent·hook·설정·binding·guarded apply·전용 검사, Work의 Main/Maintain 기록 책임, 생성·전환의 activation, 이식 스킬의 해당 운영 계약. Recover·Verify·Workspace JSON도 지금 유지·축소·제거를 결정하거나 변경하지 않는다. |

Work 구조 변경이나 새 기록 담당을 우회해서 먼저 넣지 않는다. 이미 유효한 내용은 먼저 정리할 수 있으며,02 완료를 모든06-01 작업의 선행 조건으로 만들 필요는 없다. 다만 전체 새 workflow의 적용 완료는 보류한 연결까지 해결한 뒤에 판단한다.

## 전체 전환 대상과 단계

이 구분에서 ‘유지’는 문구까지 무수정한다는 뜻이 아니다. 기존 내용·보장을 이어가되 자동 Maintainer에 넘기던 책임과 새 진입의 연결은 고친다. ‘교체’는 같은 역할의 새 정본으로 소비자를 옮긴 뒤 옛 실행 경로를 없애는 것이다. 근거·역사까지 삭제하는 의미가 아니다.

| 구분 | 대상 | 제안하는 결과 |
| --- | --- | --- |
| 유지 | RequestPolicy 제품과 검사, timeout 결정, Project의 제품 의미·현재 사실 | 기존 제품을 새 작업 체계가 읽고 다루는 실행 가능한 기준으로 사용한다. Noline 인증 예제로 바꾸지 않는다. |
| 유지·운영 연결 수정 유보 | Work의 Spec·Ticket·current·source·output·records, `reconsider-work` | 기존 의미·기록·현행 담당을 유지한다. Main 직접 기록으로의 전환은02와 함께 판단한다. |
| 교체·추가 | 맥락 읽기/갱신, 작업 논의, 설명, 개발 수행, 개선 루프 | USAGE·context-update와 현행 prototype의 스킬·상세·형성 자료를 대상 경로로 적응한다. |
| 추가 | 로컬 Personal과 공통 내용 관리 정책 | 개인 기준·경험과 Project/Work의 책임을 구별하고 실제 읽는 입구를 만든다. |
| 현행 유지·처리 유보 | 자동 Maintain agent·hook·session binding·guarded apply·fallback | 기존 제거 방향의 조사 결과는 아래에 보존하되 이번 적용 단위에서 제외한다. 기록 책임과 함께02에서 다룬다. |
| 현행 유지·판단 유보 | Recover·Verify와 그 공통 기반 | 아래 존치·대안 비교는 후속 판단 자료다. 이번 단계에서 존치 선택이나 계약 개편을 요구하지 않는다. |

먼저 논의할 핵심은 **Maintain을 건드리지 않는 첫 적용 묶음과 실제 읽기·설명 경로**다. Recover·Verify 선택을 먼저 답해야 나머지를 시작할 수 있는 구조로 두지 않는다. development의 이미 합의한 역할·위치는 유지하되 대상 Work 기록과의 연결 시점을 구별한다.

## 대조 판본과 합의의 지위

조사 시작 HEAD는 `56643f48f355aca017554149687982d02af7d434`다. Reference의 마지막 변경 커밋은 `8d5f4267`, 현재 prototype의 마지막 변경은 `f006a0e7`이다. 현재 파일도 직접 읽었다. 조사 시작에 병렬01-02의 분석·재진입 문서 변경이 있었으며 이를 채택된 품질 본문으로 사용하거나 되돌리지 않았다.02는 사용자 안내에 따라 별도 진행 중이며, 이 기록에서 새 합의를 대신 만들지 않는다.

| 확인한 근거 | 이번 전환에서 이어갈 판단 |
| --- | --- |
| [최초 직접 발화 L2320](../source/discussion/design-conversation.md#L2320)와 [13~15 후속 확정](2026-10-23-runtime-integration-and-records-13-15-proposal.md) | 사용자는 Maintainer agent 등의 장치는 없애고 기록 원칙은 남기려 했다. 이후 Main이 지침·구성을 이해해 직접 갱신하는 책임을 합의했다. 미래 기록 스킬은 아이디어이며 현재 설치 과제가 아니다. |
| [로컬 배치 정정89](2026-10-19-89-local-context-structure-correction.md), [Personal·Project 관리102](2026-10-19-102-personal-project-update-ownership.md) | Personal은 대상의 로컬 context 안에 둔다. 개인 기준 변화만으로 Project를 자동 갱신하지 않고 제품의 지속 의미와 이번 Work의 선택을 구별한다. |
| [본문·형성 자료111](2026-10-20-111-content-policy-entry.md), [진입 복구115](2026-10-20-115-complete-body-moves-and-restore-entries.md), [Work 보류116](2026-10-20-116-defer-work-content-policy.md), [체계 지침118](2026-10-20-118-system-guidance-definition-and-entry.md), [03 마감119](2026-10-20-119-ticket03-closeout.md) | 본문·실행 상세와 형성 자료의 역할을 구별한다. 체계 지침을 링크 전용 껍데기로 만들지 않는다. Work의 새 background·본문 재배치는 보류다. 모든 파일에 같은 폴더·형식이 필요한 것은 아니다. |
| [개발1~15 반영](2026-10-23-development-workflow-1-15-integration.md), [검증 통합](2026-10-24-verifier-runtime-integration.md), [01-01·01-03 마감](2026-10-24-ticket01-01-03-closeout-and-next-scope.md), [상세 확장](2026-10-26-development-detail-expansion.md) | 실행 정본은 development와 구현·개선 검토·검증·실행 배치 상세다. Main 조율, 원 구현자 수정, 독립 검증, 첫 설명과 기록을 잇는다. 모든 요청에 고정 인원·단계를 실행하는 체계가 아니다. |
| [04-01 최소 보완](2026-10-21-ticket04-01-minimal-update-and-two-checks.md), [04-02 마감](2026-10-26-ticket04-02-closeout-and-followups.md) | work-discussion은 명시 호출을 유지하고 reconsider-work는 유지한다. 설명은 explain 하나의 진입으로 통합한다. 기존 두 설명 스킬의 역할은 보존하지만 두 실행 폴더를 병행 설치하지 않는다. 일반 효과 개선이 입증된 것은 아니다. |
| [04-03 전체 책임 대조](2026-10-26-context-whole-scope-reconciliation.md), [prototype 적용](2026-10-26-context-prototype-adoption.md) | 공통 읽기는 USAGE, 허용된 Personal·Project 반영은 context-update, 수행 시점·종합은 development, Work 생성·전환은 대상 계약이 맡는다. 이름·형태의 사용감 유보는 유지하지만 이미 적용한 결과를 미채택 초안으로 되돌리지 않는다. |
| [05 마감](2026-10-29-ticket05-closeout.md) | improvement-loop와 Personal 경험 모음을 연결한다. 루프는 사용자 요청으로 실행하며 Main이 시점을 제안할 수 있다. 원문 접근·실제 사용 효과는 대상에서 확인해야 한다. |
| [개선 왕복의 범위](2026-10-12-10-workspace-and-feedback-scope.md), [06 분할](2026-10-29-ticket06-split.md) | Reference를 먼저 만들고 Noline은 기존 적용 기준·새 기준·대상 현행을 대조한다. 자동 동기화·새 배포 도구는 전제하지 않는다. |

위 기록의 이전 ‘다음·미정·미반영’은 후속 선택에 따라 읽었다. 특히 초기 검토자의 직접 수정 방향, DEVELOPMENT 위치 미정,04-03 미생성,05 미착수는 현재 입력이 아니다.

## 제품과 context를 어떻게 남기고 바꿀 것인가

아래 실제 경로는 `reference-project/` 기준이다. 제안 경로는 아직 만들지 않았다.

| 기존 대상 | 처리와 구체적인 적용안 | 같이 연결할 부분 |
| --- | --- | --- |
| [제품 코드](../../../../reference-project/src/config_loader.py), [제품 검사](../../../../reference-project/tests/test_config_loader.py) | **유지.** RequestPolicy의 기본값5000, boolean이 아닌 양의 정수 입력, 잘못된 필드 거부와 불변 결과를 보존한다. 전환을 설명하려고 제품 요구·코드를 새로 만들지 않는다. | 제품 직접 검사와 아래 Project의 실제 계약. 인증 메모리 예제·Node 검사 결과를 이 제품의 근거로 쓰지 않는다. |
| [Project common/prd](../../../../reference-project/context/project/common/prd.md), [current/architecture](../../../../reference-project/context/project/current/architecture.md), [default timeout 결정](../../../../reference-project/context/project/decisions/0001-default-timeout.md) | **내용·Owner 유지.** common/current/guidance/decisions 물리 경계도 유지한다.5000의 normative Owner는 기존 결정문이다. 정책 적용을 이유로 예외적 권위 관계를 없애지 않는다. | Project README·각 층 안내·필요한 형성 근거. 현재 파일로 충분하면 이름·주제 폴더를 억지로 늘리지 않는다. 경로를 옮길 실익이 생긴 부분만 live consumer와 함께 옮긴다. |
| [Project README](../../../../reference-project/context/project/README.md), [MAINTENANCE](../../../../reference-project/context/project/MAINTENANCE.md), [REFERENCE](../../../../reference-project/context/project/REFERENCE/README.md) | **관리·읽기 본문 보완.** prototype의 Owner 구별·질문별 선택·한정 반영·본문/형성 자료 기준을 반영한다. 제품 전용 질문·현재 사실·실제 관리 권위는 Reference 것으로 유지한다. | 옛 read/update 호출을 USAGE/context-update로 변경. Project가 Personal 채택을 관리하거나 작업 완료마다 제품 본문을 자동 갱신하지 않게 한다. 일반 작업에 관리 문서 전부를 강제하지 않는다. |
| 현재 없는 `context/personal/` | **추가.** prototype Personal의 진입·development 기준/상세/사례/형성 자료와 experience 모음을 이식한다. 현재 본문의 채택·열린 후보·예시 지위를 보존한다.01-02의 별도 미채택 개선안을 섞지 않는다. | root → context → Personal, development/USAGE/context-update/improvement-loop의 읽기 경로. 품질 기준의 최종 전체 마감과 이번 적용 가능한 판본을 구별한다. |
| 현재 없는 `context/USAGE.md`, `CONTENT-POLICY.md`, `SYSTEM-GUIDANCE.md` 및 관련 형성 자료 | **추가·대상 적응.** 공통 읽기, 본문·형성 자료 관리, 체계 지침의 역할을 구별한다. prototype의 Noline/demo 전용 경로와 서술은 실제 Reference의 것으로 바꾼다. | 정책은 Personal·Project에 적용하고 Work 보류를 명시한다. 새 정책을 모든 일반 작업의 필독 목록으로 만들지 않는다. |
| [Work collection](../../../../reference-project/context/work/workspaces/README.md), [Spec·Ticket 운영](../../../../reference-project/context/work/workspaces/spec-and-tickets/README.md), [문서 기준](../../../../reference-project/context/work/workspaces/DOCUMENT-WRITING.md) | **현재 구조·기록 원칙·담당 유지.** Main 직접 기록으로의 전환과 Maintain 인계 문장 교체는02와 함께 다룬다. | 운영 MAINTENANCE·WORKFLOW, create/reconsider/work-discussion·development가 이 보류의 consumer다.02가 바꿀 구성·분량·보존 정책은 확정하지 않는다. |
| [001-default-timeout](../../../../reference-project/context/work/workspaces/001-default-timeout/README.md)의 current/source/output/records·기계 계약 | **기존 작업·근거·현행 운영 설명 보존.** 자동 장치 설명의 전환은02와 함께 다룬다. 기존 실패/성공 receipt를 새 체계의 검증 결과로 재표시하지 않는다. | 먼저 적용하는 범위에서는 기존 선택 Project 경로·기계 계약을 유지한다. 이후 경로를 옮기면 recover.json·사람용 선택·output도 함께 확인한다. 역사 원문·receipt·당시 판정은 재작성하지 않는다. |
| [생성·전환 계약](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md) | **현행 유지, 새 의미 구성·인수안의 대조는 가능.** 실제 계약 교체는02의 기록 책임과 함께 잇는다. identity·필수 파일·안전한 경로·Recover/Verify·activation을 이번에 바꾸지 않는다. | prototype의 수동 Markdown 목록을 index.json 위에 중복 설치하지 않는다. 기본 Workspace는 기존 index.json 한곳에서 관리한다. binding·generation·pending 제거는 유보한다. |

### Personal의 예시와 Reference의 실제 사건을 구별한다

Personal의 세 경험 주제는 허구의 Reference 운영 결과가 아니라 실제 사용자 경험을 선별한 prototype 예시다. **근거·지위를 유지해 함께 가져오는 안을 권한다.** 빈 관리 폴더만 만드는 것으로 내용의 사용 가능성을 대신하지 않는다.

- [설계 논의](prototypes/development-workflow/noline-demo/context/personal/experience/topics/design-conversation.md)는014의2026-10-27~28 논의와 열린 방법 후보다.
- [문서 품질](prototypes/development-workflow/noline-demo/context/personal/experience/topics/document-quality.md)은 과거 Noline의 별도 문서 작업에 대한 경험이며 스킬 단독 효과를 입증하지 않는다.
- [설명 효과](prototypes/development-workflow/noline-demo/context/personal/experience/topics/explanation-effects.md)는014의 explain 비교에서 관찰한 국소 이득·전체 효과 미확인이다.

이 파일들과 experience README/MAINTENANCE, `personal/_background/experience-collection/`의 근거를 같이 옮기되 ‘014에서 작성한 적용 예시’와 당시 출처를 유지한다. 새 Reference 사용 이력·새 기준 채택·즉시 실행할 개선 대기열로 바꾸지 않는다. 반대로 Noline demo의 제품 인증 계약·로그인 Work·코드·테스트·실행 로그는 Reference의 제품/current로 가져오지 않는다. 스킬 상세 안의 설명 사례는 사례라는 경계와 필요한 자체 근거를 유지할 수 있다.

## 기존 스킬과 새 실행 묶음의 대응

아래는 전체 전환의 대응표다. 첫 단계에서 전부 설치·교체한다는 뜻이 아니다. Work 기록·Maintain·activation을 바꾸는 문장은 위 보류 범위에 따르며, 그 문장을 포함한 prototype을 현재 실행 경로에 그대로 설치하지 않는다. 읽기·본문 편집의 스킬도 미설치 development/improvement-loop를 실행 가능한 의존으로 연결하지 않도록 실제 묶음을 확인한다.

실행 원본 위치는 기존 `.agents/skills/`를 유지한다. 스킬 안의 상세·shared·형성 자료는 함께 옮겨야 하며 SKILL.md만 복사하지 않는다.

| 현재 Reference | 제안 | 남길 책임·제거할 연결 |
| --- | --- | --- |
| `read-project-context/` | **실행 스킬 제거 → `context/USAGE.md`로 이관** | 질문에 필요한 원문 선택·대조·적용은 유지한다. 읽기만 요청했을 때 Work 생성·전체 인수·문서 수정·별도 읽기 보고를 시작하지 않는다. root와 Project reading의 호출을 함께 바꾼다. |
| `update-project-context/` | **`context-update/`로 교체** | 허용된 Personal·Project의 한정 반영 방법을 맡는다. 내용 선별·권위·관리 계약은 해당 영역에 남긴다. 제품 정책 결정권이나 Work 전체 기록을 흡수하지 않는다. |
| `create-context-workspace/` | **현재 prototype의 의미 구성·인수 흐름으로 보완** | Reference가 실제로 요구하는 Workspace JSON·Recover 확인은 유지한다. 생성만 요청하면 기본 선택을 바꾸지 않고, 전환 요청 때에만 변경한다. 삭제할 Maintainer activation 호출을 실행하지 않게 한다. |
| `work-discussion/` | **prototype 최소 보완판으로 교체** | 직접 호출 조건·기존 정의의 충분성·필요한 구체화를 유지한다. 기록은 Main의 실제 반영으로 연결한다. 일반 목표 구체화를 자동 호출 조건으로 확대하지 않는다. |
| `reconsider-work/` | **판단 본체 유지, 환경 의존 부분 수정** | 실제 결과·전제·부담에 비춰 기존 선택을 재판단하는 역할은 development에 흡수해 없애지 않는다. 말미의 ‘Maintain에 넘김/문서 갱신 위임’을 Main 책임과 현재 Owner 계약으로 고친다. |
| `work-artifact-briefing/`, `explanation-recovery/` | **`explain/`으로 통합 후 기존 실행 폴더 제거** | 첫 결과·역할/흐름·선택 이유 설명과 앞선 말의 뜻/타당성 대조를 본체·조건부 상세로 잇는다. 옛 실행본과 형성 자료는 새 explain의 `_background/legacy/`와 Git 이력에서 당시 판본으로 보존한다. |
| 현재 없음 | **`development/` 추가** | 본체와 `references/implementation.md`, `review.md`, `verification/INDEX.md`, `verification/evidence.md`, `execution.md`를 하나의 수행 묶음으로 설치한다. 독립 검토·검증의 역할과 권한을 새 전역 agent 등록으로 바꾸지 않는다. |
| 현재 없음 | **`improvement-loop/` 추가** | 본체·conversation/application/effects 상세·형성 자료와 Personal 경험 모음을 연결한다. 사용자 요청 실행, 시점 제안, 가능한 개선의 선택·반영·관찰을 유지한다. 자동 response-end 루프로 설치하지 않는다. |
| `context/project/guidance/explanation-and-evidence-criteria.md` | **`.agents/skills/shared/explanation-and-evidence-criteria.md`로 소유 이동** | 현재 prototype의 공통 기준과 실제 consumer인 work-discussion/explain을 함께 적용한다. 옛 guidance 본문과 새 shared를 경쟁하는 정본으로 남기지 않는다. guidance README와 root/skill 안내·참조를 함께 정리한다. |
| 현재 없음 | **`.agents/skills/SKILLS-CONTENT-POLICY.md`와 필요한 형성 자료 추가** | 스킬 작성·의미 변경 때 본체/상세/형성 자료를 함께 관리한다. 새 담당자·고정 파일 수·모든 응답의 필수 단계는 추가하지 않는다. |

권고 구성은 **prototype의 실행 스킬6개 + 유지하는 reconsider-work 1개**다. 개수 맞추기가 목적은 아니며 위 대응을 적용한 결과다. 옛 이름의 wrapper 스킬을 상시 병행하면 선택·문구·갱신이 둘로 갈리므로 기본안에는 두지 않는다. 보존된 옛 본문은 실행 진입으로 노출하지 않는다.

explain의 legacy에 보존된 두 `2026-10-23-before-explain.txt`는 현행 Reference의 두 SKILL.md와 내용이 다르다. 따라서 그 legacy를 제거 직전 Reference의 정확한 복구본이라고 부르지 않는다. 실제 반영 직전 commit/blob 또는 필요한 snapshot으로 Reference 원본도 식별한다. 형성 자료의 당시 발췌 안에 있는 외부 경로는 원문으로 보존하고, 현재 실행·읽기 링크만 새 경로에 맞춘다.

### 실제 발견 경로와 대상 경로를 같이 바꾼다

현재 Reference의 Claude/Codex bridge는 read·work-discussion·reconsider·두 설명 스킬의5개 symlink이며 create/update에는 bridge가 없다. 기존7개 원본에는 `agents/openai.yaml`이 있지만 prototype 실행 묶음에는 그 metadata가 없다. 따라서 ‘prototype 복사 완료’를 설치·발견 완료로 세면 안 된다.

권고는 `.agents/skills/`를 원본으로 유지하고 `.claude/skills/`, `.codex/skills/`의 선택한 실행 스킬 연결을 같은 원본에 맞추는 것이다. 기존5개 중 제거한 read·두 설명 연결을 정리하고 새 이름·추가 스킬의 발견 경로와 기존 metadata를 맞춘다. 실제 host에서 이미 `.agents`를 읽어 중복 노출되는지 확인한 뒤 불필요한 bridge는 두지 않는다. 이 검토만으로 host별 발견을 확인했다고 주장하지 않는다.

root의 `CLAUDE.md → AGENTS.md` 연결은 유지한다. work-discussion의 `allow_implicit_invocation: false`와 improvement-loop의 사용자 요청 조건을 metadata·본문·호출자에서 일치시킨다. execution 상세의 현재 내부 담당 시작값과 실제 host의 모델·추론·상속 제약도 함께 확인하며 지원하지 않는 설정을 적용했다고 기록하지 않는다.

prototype의 `skills/`와 `noline-demo/context/`는 형제 관계지만 설치 후에는 `.agents/skills/`와 `context/`가 된다. SKILL·references·형성 자료의 상대 링크, root/Work 안내, Project·Personal의 역참조를 모두 대상 기준으로 바꾼다. viewer.html·생성 스크립트·014 전체 기록은 설치하지 않으며, 대상 본문 이해에 필요한 최소 형성 근거는 가까이 둔다.

## 02와 함께 다룰 조사 — Maintain 제거와 남는 책임

이 절은 후속 범위를 잃지 않기 위해 보존한 의존 조사다. 아래 제거·대체 조치는 현재06-01의 첫 적용 단위에서 제외한다. 필요한 기록 원칙과 실제 변경 담당·시점은02 논의와 함께 잇는다.

현재 [공통 CLI](../../../../reference-project/context/work/harness/cli.py)는 Maintain을 최상위에서 import한다. `maintain/`만 삭제하면 Recover·Verify 진입도 깨진다. 아래를 하나의 제거 단위로 잡아야 한다.

| 제거할 대상 | 함께 바꿀 consumer·확인 |
| --- | --- |
| `context/work/harness/maintain/`의 semantic agent, prompt, guarded apply, host adapters, session/runtime 처리와 전용 tests/eval | CLI의 Maintain import·하위 명령·전용 출력/dispatch, Harness 진입 설명, Maintain 전용 검사를 제거한다. Recover/Verify/workspace/validation의 독립 보장은 남겨 확인한다. |
| `.codex/config.toml`의 `workspace_context_maintainer`, `.codex/maintain.json`, `.codex/hooks.json`의 Maintain 이벤트, `.codex/hooks/maintain.py` | Reference 현행 config가 전용 내용뿐인지 확인해 삭제하거나 해당 부분만 제거한다. 사용자 설정이 섞인 대상에서는 파일 전체를 덮어쓰지 않는다. 등록·설정만 없애고 실행 안내가 남지 않게 한다. |
| `.claude/maintain.json`, `.claude/hooks/maintain.py` | Reference에는 현재 `.claude/settings.json`이 없다. 있는 것으로 가정해 변경 목록을 만들지 않는다. Noline의 실제 설정·별도 collector는06-02에서 새로 확인한다. |
| `.gitignore`의 Maintain runtime 항목 | 실제 남은 runtime·로그의 보존 필요를 먼저 확인한다. ignore를 지운 결과 session 원문이 실수로 Git에 잡히지 않게 하고, 기존 runtime의 일괄 삭제를 전환 기본값으로 두지 않는다. |
| root/Work AGENTS·README, Harness README, Spec·Ticket 운영·생성 계약, 위 기존 스킬의 자동/수동 Maintain 안내 | Main의 기록 시점·Owner·실제 반영 확인으로 바꾼다. bootstrap/activation/binding/pending/fallback을 다른 말로 남겨 자동 장치 재가동을 요구하지 않는다. |
| ai-workspace의 [이식 스킬](../../../../.agents/skills/apply-context-harness/SKILL.md)과 [적용 계약](../../../../.agents/skills/apply-context-harness/references/application-contract.md)의 설치·검증 경로 | 새 Reference에 없는 Maintain을 다시 설치하지 않도록 같이 보완한다. target 변경 보호·dry-run·판본 대조·실제 검증은 유지하고 새 Personal/스킬/기록 책임을 반영한다. 지금 이 스킬을 실행하거나 수정한 것은 아니다. |

자동 장치가 없어져도 다음 책임은 남는다.

기록 원칙은 기존 Work 문서에만 있는 것이 아니다. [Maintain README의 의미 판단 부분](../../../../reference-project/context/work/harness/maintain/README.md)에도 현재/과정 구별, 출처 강도, 정정 영향, 임시 근거의 필요한 최소 보존 기준이 들어 있다. 제거 전에 기존 Work 관리 기준과 조항별로 대조해 필요한 의미를 보존하고,02에서 바뀔 구체 운영은 그 책임으로 잇는다. README 전체와 장치의 JSON protocol을 새 문서에 그대로 복사하지 않는다.

| 계속 필요한 일 | 제거 후 맡는 주체와 위치 |
| --- | --- |
| 이번 목표·선택·이유·결과·다음 행동을 현재로 맞춤 | Main이 Work의 기존 관리·문서 기준과 development를 따라 실제 파일을 갱신한다. 필요한 원문/과정은 기존 source·records 관계에 맞춰 보존한다. |
| 다른 담당자의 결과를 채택하고 영향 범위를 잇기 | 담당자는 실제 결과·근거·미확인을 반환하고 Main이 판단·반영한다. 반환·접수와 파일 반영을 구별한다. |
| 지속되는 제품/개인 의미의 반영 | Main 또는 배정받은 담당자가 해당 Owner 계약과 context-update를 적용한다. 새 기준·제품 약속의 채택권은 편집 권한과 구별한다. |
| 새 Work 선택과 늦게 오는 결과의 귀속 | Main이 명시 요청과 Work 계약으로 선택을 바꾸고 담당자에게 최신 대상·권한을 전달한다. 늦은 결과는 원래 Work/판본에 귀속한다. 옛 generation 상태를 수동 흉내 내지 않는다. |
| source·제품·다른 Workspace·기계 증거를 임의로 덮지 않음 | 대상 지침·Owner 경계와 실제 도구 권한을 따른다. Verify/Recover가 맡는 경로·schema 검사는 유지한다. |

**달라지는 보장도 명시해야 한다.** 기존 Maintain의 read-only semantic agent와 guarded apply가 하던 경로 제한·stale preimage 거부가 Main의 일반 파일 편집을 자동 보호해 주지는 않는다. 지침을 옮겼다는 사실로 같은 실행 강제를 보존했다고 말할 수 없다. 이 전환에서는 Main이 최신 파일·병렬 변경을 확인하고 작은 diff·직접 검토·Git 복구로 관리하는 안을 제안한다. 그 차이가 요구에 부족하다면 해당 편집에 필요한 최소 검사만 별도 논의하며, 기존 Maintainer 전체를 몰래 존치하지 않는다.

## 후속 판단 자료 — Recover·Verify의 기존 비교

Maintain 보류 이전에 만든 존치 권고와 대안이다. 이번 단계에서는 현행을 그대로 두며, 이 선택을 나머지 적용의 선행 질문으로 요구하지 않는다.

[Recover](../../../../reference-project/context/work/harness/recover/README.md)는 Workspace와 선택한 Project 자료를 읽기 전용 packet으로 만들고, 연결된 검증 증거의 선언 파일이 바뀌었는지 보여 준다. [Verify](../../../../reference-project/context/work/harness/verify/README.md)는 고정 명령·실행 한도·선확보 snapshot·receipt·machine status를 맡는다. 둘의 실제 구현은 Maintain에 의존하지 않아 공통 CLI를 정리하면 독립해서 남길 수 있다.

| 선택 | 얻는 것과 비용 | 이번 권고 |
| --- | --- | --- |
| 둘을 유지하고 자동 Maintain 의존만 분리 | 기존 Workspace 읽기·경로 거부·증거 snapshot/freshness·실행 한도와 과거 receipt 접근을 유지한다. JSON 계약과 해당 검사의 유지비는 남는다. | **우선 권고.** 새 prototype이 이 결정적 기능을 대체하는 구현을 제공한 것은 아니며, 제거 합의도 없다. |
| Recover를 직접 읽기로 바꾸고 Verify만 유지 | packet 구성·고정 읽기 계약은 줄지만 Work/Project 선택·status/receipt의 재접속을 Main이 직접 수행해야 한다. Verify가 남으면 기계 상태 계약도 남는다. |02가 더 가벼운 재개 구조를 선택하거나 packet의 부담이 확인되면 비교한다. |
| 둘 다 제거하고 직접 읽기·직접 검사·수동 기록으로 전환 | 장치는 줄지만 기존 증거 연결·보호·현재성 판별의 대체와 모든 consumer 정리가 필요하다. 과거 증거를 읽는 경로도 별도로 남겨야 한다. |현재 근거로 즉시 선택하지 않는다. ‘Main 기록’ 합의만으로 이 보장을 버리지는 않는다. |

존치안에서도 Recover를 Personal·Project·Work 전체 자동 수집기로 확대하지 않는다. 기존 `recover.json`의 Project 선택과 packet은 남기고, Personal·공통 USAGE·형성 자료는 root/context의 읽기 경로에서 질문에 맞게 고른다. 한정 위임은 맡은 계약부터 읽으며 일반 Workspace 인수를 자동 수행하지 않는다. Personal 전체를 싣기 위한 새 JSON 필드는 이번 권고에 없다.

구체적인 호출 조건은 **Main이 해당 Workspace의 현재 맥락을 복구할 필요가 있을 때 Recover를 사용하고, 이미 확보한 유효한 packet/읽기는 재사용하는 것**으로 제안한다. USAGE는 추가 원문을 선택·대조하는 방법이므로 packet과 같은 자료를 다시 전수 읽는 별도 단계로 만들지 않는다. Recover가 없는 환경도 이 공통 읽기를 사용할 수 있지만, 이번 Reference 존치안의 기존 Workspace에는 현재 필수 Spec·status·recover/verify 계약이 남는다. ‘선택적으로 실행’과 ‘모든 JSON을 없애도 실행 가능’을 혼동하지 않는다. 후자의 설치 optional화는 현재 구현의 status 선행 요구와 생성·검사를 바꾸는 별도 선택이다.

Verify는 반복 개발 검사의 필수 wrapper가 아니다. 직접 테스트·실행 관찰·검증자의 요구별 판정이 우선이고, 지속 증거가 필요한 상태 전환·인계에서 선택한다. `verification_passed`는 전체 완료·사람 수락이 아니다. Recover의 freshness도 선언한 파일의 현재 일치이며 미선언 입력·현재 claim/argv 전체의 동일성까지 보장하지 않는다.

Recover의 현행 Spec 다섯 파일·memory/state/status 구조와 JSON 계약은02의 구성 선택에 영향을 받는다. **지금은 현행을 보존하는 기준으로 계획하되,02 결과가 나오면 영향을 받는 생성·읽기·검사만 재대조한다.**02 전체 완료를 모든 스킬·Project 적용의 선행 조건으로 만들지 않는다.

공통 `harness/workspace/`의 identity·안전한 경로·status 계약은 두 기능이 계속 사용하므로 유지한다. `workspace_contract.py`와 recover/verify의 `operation.py` 같은 호환 진입은 삭제할 Maintain과 같은 수명으로 보지 않는다. 현행 내부 소비가 줄었더라도06-02 대상의 사용처가 확인되기 전 일괄 제거하지 않는다. 이식 스킬의 `capture_target_state.py`와 `record_harness_tests.py`도 Maintain을 import하지 않는 판본 보존·검사 근거 helper이므로 유지 후보이며, 장치 제거에 묶어 삭제할 이유는 없다.

## 실제 반영을 선택하면 묶어서 처리할 단위

아래는 구현 승인이 아니라 논의 뒤 사용할 작업 분해안이다. 각 단위는 정본·consumer·직접 확인을 함께 완성하며 중간에 끊긴 경로를 ‘적용 완료’로 남기지 않는다.

1. **먼저 논의할 context·설명 묶음:** Personal·공통 정책·USAGE·Reference Project 관리의 비충돌 부분과 explain/shared를 연결한다. context-update의 한정 반영도 현행 Work 담당·의존에 맞춰 함께 구체화한다. root의 해당 routing만 맞추고 Maintain·Work 작성/전환 계약은 유지한다. 기존 제품·작업 기록도 보존한다.
2. **후속 실행 묶음 준비:** development·context-update·work-discussion·create·improvement-loop의 본문·경로·metadata·consumer 대응을 구체화한다. 현행 기록 담당과 충돌하는 채로 자동 발견·호출 경로를 열거나 옛 경로를 제거하지 않는다. 독립 부분을 연결할 실익이 있으면 필요한 적응 범위를 먼저 논의한다.
3. **02와 함께 해결할 기록·장치 연결:** Main/Maintain 책임·생성/전환·자동 장치 처리와 필요한 Recover/Verify 계약을 함께 판단한다. 앞선 조사 결과는 이때 재사용한다.
4. **범위가 확인된 전달판:** 실제 선택한 변경만 이식 경로·06-02 전달판에 반영한다. Maintain을 그대로 둔 중간판이면 그 범위와 남은 연결을 명시하고 전체 전환 완료라고 표시하지 않는다.

분리 단위가 별개 배포·장기 병행 운영을 뜻하지 않는다. 특히 새 Main 기록 지침과 자동 Maintainer가 동시에 같은 문서를 쓰는 상태로 실제 작업을 시작하지 않는다. 반영 전에는 실제 켜진 프로세스·binding 여부를 확인하고, 존재만으로 활성화됐다고 가정하지 않는다.

현행 `deactivate`는 이후 prompt 연결을 해제할 뿐 이미 접수된 event/worker를 취소하지 않는다. 실제 활성 상태가 있다면 진행 중·실패·미반영 결과를 필요한 metadata와 Context diff로 대조한 뒤 전환해야 한다. 설정 삭제나 deactivate 성공만으로 이전 writer가 멈췄다고 간주하지 않으며, runtime 대화 원문을 작업 기록으로 복사하지 않는다.

Reference 반영 후 운영 이식의 기준은 Reference로 모으고,014 prototype은 그 판본의 설계·비교 근거로 보존하는 안을 권한다. 두 곳을 같은 현재 실행 정본으로 계속 동시 편집하지 않는다.014 output은 실제 Reference의 선택 결과를 가리키며, Noline 개선을 돌려받을 때는 필요한 장면·당시 기준·대상 차이를 선별한다. 새 자동 동기화 시스템은 만들지 않는다.

## 반영 뒤 확인할 장면과 되돌릴 범위

| 확인할 장면 | 확인해야 할 결과 |
| --- | --- |
| Reference root에서 일반 재개 / 범위를 정한 조사·검토 | 제품·현재 Work·관련 Personal에 도달하고 판단·다음 행동을 복원한다. 한정 담당자는 역할 밖 전체 인수·기록을 떠맡지 않는다. |
| 단순 맥락 읽기 / 근거가 확인된 지속 문장 정정 | 읽기만이면 무편집으로 끝난다. 정정은 해당 Owner 본문·필요한 형성 자료/consumer만 바꾸며 기준 채택권을 넘지 않는다. |
| 의미 있는 제품 변경의 개발·개선 검토·검증·첫 설명 | 현재 제품 계약과 실제 사용처를 읽고 구현·수정·검증을 잇는다. explain으로 조사 공백을 감추거나 Verify pass로 전체 완료를 대신하지 않는다. |
| 새 Workspace 생성만 / 명시 전환 | 생성만이면 기존 기본 선택·상태를 보존한다. 전환은 Main의 대상·읽기·진행을 실제로 바꾸며 삭제한 activation을 요구하지 않는다. 이전 성공 상태를 새 Work에 복제하지 않는다. |
| 중요한 판단 뒤 종료·다음 재개 | Main이 필요한 Work/Project/Personal을 실제 갱신하고 새 독자가 현재·남은 판단을 복원한다. 자동 hook이 기록했다고 가정하지 않는다. |
| 요청된 improvement-loop, 압축·재개된 대화 | [원문 접근 상세](prototypes/development-workflow/skills/improvement-loop/references/conversation.md)에 따라 같은 세션의 범위를 확인한다. Codex 로컬 접근 예를 Claude 또는 모든 host 지원으로 확대하지 않는다. 전체 원문을 못 읽으면 그 요구는 미완료로 남긴다. |
| Maintain 없는 CLI·설정·검사 | recover/verify가 import 오류 없이 작동하고 제거한 hook/role을 요구하지 않는다. 남길 경로·schema·실행 제한과 과거 receipt 읽기 검사를 확인한다. |

구현 시에는 변경 전 해당 회귀를 기준선으로 실행한 뒤, 제품 검사·Recover/Verify·공통 Workspace·CLI·임시 Workspace validation 중 영향을 받는 검사를 수행한다. 문서/링크 검사, 실제 host의 스킬 발견, 실제 읽기·반영·재개, 장기 사용 효과는 별도 증거로 구별한다. 이 분석에서는 그 테스트나 host 실행을 수행하지 않았다.

구체적으로 `validation/tests/test_cli.py`의 명령 노출과 `test_cli_contracts.py`의 Maintain 입력 검사는 새 CLI에 맞춘다. Recover·Verify를 남기면 `test_ephemeral_workspace_state_preservation.py`의 임시 `recover → verify → recover`와 실제 Workspace 불변 검사는 보존한다. Work 경로를 바꾸기로 하면 reader뿐 아니라 `harness/testing.py`의 공통 fixture도 같은 계약으로 바꾼다. prototype의 Spec·Ticket README는 요약 한 파일이므로 Reference의 SPEC/TICKET/EXECUTION-CRITERIA/MAINTENANCE 상세 전체를 그 파일로 덮지 않는다.

복구는 반영 직전 commit과 관련 사용자 변경을 고정한 뒤 위 책임 단위의 코드·설정·문서·consumer를 함께 되돌리는 범위로 잡는다. 이후 생성된 source·records·receipt·제품/사용자 변경까지 일괄 덮어쓰지 않는다. 자동 장치를 되돌릴 때도 파일 복구와 실제 재활성화를 같은 일로 처리하지 않는다. 이번 분석 시작판56643f48을 나중에도 무조건 적용 가능한 복구판으로 고정하지 않는다.

## 이번에 확인한 범위와 남은 논의

Main은 현재06·Spec·memory·관련 합의/정정·마감 기록과 현행 실행 본문을 대조했다. 별도 읽기 전용 조사는 Reference의 실행 장치 결합, context·제품·스킬·bridge 대응을 나누어 확인했다. 현재 파일의 관계를 조사한 결과이며 실행 성공·사용자 수락을 증명하지 않는다.

작성 뒤 별도 검토자가 원문 합의·마감 기록과 현행 제품/Project·CLI·Recover·스킬/bridge·이식 경로를 대조했다. 새 권고의 합의 승격,02 책임 침범, 수정이 필요한 중요한 누락은 보고하지 않았다. 이 역시 읽기 전용 검토이며 실제 이관·host 실행의 확인은 아니다. Main의 문서 검사에서 이 검토안의 로컬 링크44개에 경로·명시 앵커 누락이 없었고 `git diff --check`가 통과했다. Git 대조에서 Reference·prototype·원자료·이식 스킬·실행 설정의 tracked 변경은 없었다.

이 기록과06-01·재진입 안내만 갱신한다. 후속 보류 요청도 같은 계획에 반영했다. Reference·prototype·제품·이식 스킬·전역 설정·Noline에는 변경하지 않는다.02와01-02의 병렬 문서·미채택 제안은 보존한다. 위 독립 검토는 최초 전체 전환안에 대한 결과이며 이번 보류 뒤 실제 연결 검증을 대신하지 않는다.

다음 논의에서는 **Maintain을 현행대로 둔 첫 context·설명 적용 묶음**을 구체화한다. 기록·장치 선택은02와 함께 다루고, 그 결과가 필요한 실행 연결만 후속으로 잇는다. 분석·부분 적용 준비를06-01 전체 완료로 표시하지 않는다.
