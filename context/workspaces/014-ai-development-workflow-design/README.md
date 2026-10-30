# AI 개발 작업 체계의 개선 설계

**06 현재:** [실행 스킬 설치·옛 경로 정리](records/2026-10-30-ticket06-execution-skills-and-retirement.md)까지 반영·직접 확인했다. [남은 책임과 Noline 후속 방향](records/2026-10-30-ticket06-remaining-work-and-noline-followup.md)에서02 의존 작업과06의 별도 실행 확인·완료 책임을 찾는다. 후속 보완·개선 루프는 Noline의 실제 반영본과 기존 작업·기록을 바탕으로 진행하려는 방향이며, 구체 대상·시점은 아직 정하지 않았다.

**후속 테스트 선택:** 첫 부분 적용은 `e38ce52b`로 보존했다. 통합 테스트는02에서 기록·전환 계약을 Reference에 연결한 뒤 진행한다. 지금 별도 host 테스트를 먼저 시작하지 않으며, 결과를06-01 완료 판단에 연결한다. [선택 기록](records/2026-10-29-ticket06-01-reference-partial-application.md#후속-선택--통합-테스트는02에서-진행).

**06-01 첫 부분 적용(2026-10-29):** 사용자 승인에 따라 Personal·Project 관리·공통 읽기·한정 반영·설명을 Reference에 [적용하고 직접 확인](records/2026-10-29-ticket06-01-reference-partial-application.md)했다. [06-01](current/tickets/06-framework-transition/06-01-reference-project-application.md)은 계속 진행 중이다. Maintain·Work 기록 담당·생성/전환은 현행을 유지하고02와 함께 다룬다. 새 host의 자동 발견·호출·사용 효과와 전체 workflow 전환은 미확인이다. Noline·prototype은 변경하지 않았다.

**01-02 설계 완료 — 2026-10-29:** [완료 조건·후속 책임](records/2026-10-29-ticket01-02-closeout.md)을 대조하고 품질 기준·사례·검토/수정 연결을 마감했다. 앞서 마감한01-01·01-03과 함께01의 개발 작업 방식 설계 결과가 갖춰졌다. 실제 적용·확인은06, 전체 연결·효과 관찰은07로 잇는다.02·06·07과 Workspace014는 진행 중이다.

**05 설계 완료 — 2026-10-29:** [마감 결과·열린 기준·후속 범위](records/2026-10-29-ticket05-closeout.md). 네 묶음 합의와 두 실행 보완을 prototype에 반영하고 완료 조건을 대조했다. 실제 운영 설치·사용 효과와 Workspace014 전체 완료는 별도다.

**05 작업 체계 개선 루프의 설계·프로토타입 작업을 마감했다.** [실행 스킬](records/prototypes/development-workflow/skills/improvement-loop/SKILL.md), [적용 사례](records/prototypes/development-workflow/skills/improvement-loop/references/application.md), Personal 경험 모음이 현재 산출물이다. 후속01-02도 설계 마감했으며02·06·07은 남아 있다. 범용 개선 리뷰어 [기타-01](current/tickets/misc-01-improvement-review.md)은 보류한다.

2026-10-27 [Workspace 점검·마무리 기록](records/2026-10-27-workspace-checkpoint.md): 이번 맥락 연결과 계층 정리의 완료를 재확인하고, 남은 전체 설계와 구별해 재진입 안내를 정리했다. Workspace014는 계속 진행 중이다.

**앞선 완료 결과 — Development 실행 상세의 계층 확장 완료:** 기존04-03 연결·확인 결과를 `191e2d86`으로 먼저 커밋했다. 사용자의 구조 확장 요청에 따라 [구현 수행·검사 근거 상세와 소비 경로](records/2026-10-26-development-detail-expansion.md)를 구성하고 독립 검토 보완·원문/링크 확인을 마쳤다. 전체 조율·검토·검증·정본 관리의 책임은 유지한다. 상세 확장·구성 정정·확인 기록은 `0dd23464`로 커밋했다. 후속 구성 정정으로 검증 본문을 `verification/INDEX.md`로 옮겨 `evidence.md`와 같은 폴더에 묶었다.

USAGE/context-update의 사용감 유보, 실제 운영 설치·host 전환·전체 역할 수행과 일반 효과의 미확인은 유지한다. 현재 결과는 [prototype](records/prototypes/development-workflow/README.md)과 [열람 화면](records/prototypes/development-workflow/viewer.html), 다음 설계 범위는 [current](current/index.md)에서 찾는다. 아래 날짜별 설계·반영 설명의 당시 다음 행동은 이 최신 결과를 대체하지 않는다.

**01-01·01-03 설계 결과를 마감했다.** [완료 조건 대조와 Spec·04의 다음 범위](records/2026-10-24-ticket01-01-03-closeout-and-next-scope.md)에서 근거·비용·한계를 확인한다. 그 뒤 **04-03의 읽기·적용·갱신·재개 연결도 설계·prototype 범위에서 완료**했다. 기존 세 스킬은 그 연결을 구현하는 수단으로 대조해 반영했다. [재개 메모](records/2026-10-24-workflow-context-connection-checkpoint.md)에 완료 경계·입력·첫 산출물을 정리했다. 상위01·04와 전체 Workspace는 아직 완료가 아니며 실제 운영 효과와 구별한다.

검증자 실행 반영: [검증 상세](records/prototypes/development-workflow/skills/development/references/verification/INDEX.md)를 생성하고 development·review·execution과 연결했다. [합의 대조와 확인 기록](records/2026-10-24-verifier-runtime-integration.md)에서 항목별 반영·대표 장면·실제 검사·한계를 읽는다.

**구현·개선 검토1~15와 검증자1~12의 합의를 실행 prototype에 통합했다.** [전체 흐름 대조·실제 확인](records/2026-10-24-verifier-runtime-integration.md)에서 구현 중 검사·개선 수정·별도 검증·재검증·Main 완료와 기록의 연결을 확인한다. Main의 대표 장면 대조와 메모리 예제 실행을 마쳤으며, 여러 agent의 전체 개발 수행·운영 설치·일반 효과 검증은 별도다. 개별 맥락 스킬의 prototype 보완은04-03에서 마쳤고, 대상별 운영 연결·전체 체계 종합은06·07에 남아 있다.

**04-02 설명 구성·적용 설계 완료.** [완료 조건 대조와 후속 인계](records/2026-10-26-ticket04-02-closeout-and-followups.md)에서 다섯 조건의 근거·비용·한계를 확인했다. 현재 explain·development를 유지하며 배치·전환은06, 실제 적용·관찰은07, 경험 재검토는05, 맥락 연결은04-03으로 이어진다. 맥락 연결은 이후04-03 적용으로 이어졌다. 실제 운영 설치·일반 효과·두 시험의 모든 부족 해결을 완료로 선언하지 않는다.

**Ticket03의 구성안·대표 본문·읽기와 갱신 책임 구체화도 완료 상태다.** [마무리119](records/2026-10-20-119-ticket03-closeout.md)와 [03 완료 조건](current/tickets/03-project-context.md)에서 판단 근거와 후속 범위를 확인한다. Workspace014 전체는 계속 진행 중이며, 이번 마무리에서 다음 Ticket을 착수하지 않았다.

Noline에 이식해 사용한 Project·Work context와 스킬의 평가, 사용자 인터뷰, 개발 에이전트 관련 강연을 바탕으로 **ai-workspace와 실제 개발 방식을 어떻게 발전시킬지 설계하는 작업**이다. 좋은 구현을 돕는 컨텍스트·코드 기준·절차·도구와 기록·경험 반영을 함께 다룬다. 전체 운영 체계 확정이나 실제 설치·스킬 구현은 아직 끝나지 않았다.

사용자는2026-10-12에 독립 Workspace와 근거 사본을 함께 보존해 새 세션도 논의를 이어가도록 요청했다. 이 폴더는 설계 작업의 기록 단위이며 Reference Harness를 설치·실행한 Workspace가 아니다. [Spec](current/spec.md)이 전체 구상과 미결정을, [Ticket01~07](current/tickets/index.md)이 결과별 책임을 맡는다. 과거 B 선택 뒤 사용자는 [Personal 기반 구현·별도 관점 검토·Main 적용 판단과 동적 라우팅 구상](records/2026-10-21-dynamic-context-and-review-intent.md)을 설명했다. 역할별 입력·수정·검증은 이 의도와 레퍼런스를 함께 비교해 구체화한다.

04-02는 [새 source](source/artifact-explanation-scenes/README.md)에 보고서·interceptor·network 흐름·저장 용량·여행 브리핑·Network 첫 완료 보고의 여섯 묶음을 구성했다. [시점·본문 비교 범위](records/2026-10-22-ticket04-02-source-expansion-and-coverage.md)에서 사건별 역할과 당시 자료 공백을 구별했다. 원문 보존과 당시 실행 재현·스킬 효과 검증은 별개다. 본문 비교에서 확인한 국소 개선과 미실행인 적용 배치 비교를 구별한다. 당시 비교와 설계 마감의 근거는 [04-02](current/tickets/04-skill-improvements/04-02-artifact-explanation.md)에서 찾는다. 남은 적용·관찰은06·07로 연결한다.

## 지금 읽을 결과

실물은 [development-workflow](records/prototypes/development-workflow/README.md) 한 폴더에서 계속 발전시킨다. 그 안의 noline-demo/context에 Personal의 개인 판단, Project의 제품 계약·개발 가이드·현재 사실, Work의 이번 선택·진행·결과를 구별했다. [CONTENT-POLICY](records/prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md)는 본문과 형성 자료의 관리를, [SYSTEM-GUIDANCE](records/prototypes/development-workflow/noline-demo/context/SYSTEM-GUIDANCE.md)는 체계 지침과 진입·상세의 역할을 소유한다.

데모 독자는 바깥014 기록 없이 본문을 이해할 수 있어야 한다. 작성·평가·정정의 전체 과정은014 records가 보존하고, 개별 본문 수정에 필요한 형성 이유와 최소 근거는 그 본문 가까이 둔다. 실제 작성 논의를 예제 제품의 사건으로 바꾸지 않는다.

Work는 기존 current·Spec·Ticket·source·output·records의 형태와 제약을 유지한다. [116](records/2026-10-20-116-defer-work-content-policy.md)의 복구를 되돌려 새 background를 적용하지 않는다. Development의 prototype 진입·공통 본문은 스킬로 이전했고, 상세 실행·조건별 맥락 연결도 반영했다. 실제 context와의 구체 연결·개별 맥락 스킬의 prototype 보완은04-03에서 마쳤고, 대상별 배치·적용 계획과 수행 효과 확인은06·07로 이어진다.01-01·01-03의 역할·진행·인계 설계 마감은 유지한다.03 완료는 실제 Noline 적용·모든 기준 채택·장기 효과 확인을 포함하지 않는다.

## 배경 없이 들어올 때

1. [current/index](current/index.md), [현재 상태](current/state.md), [현재 산출물](output/index.md)을 읽고 실제 Git 상태를 확인한다.
2. [memory](current/memory.md)의 지속할 사용자 의도·정정과 [Spec](current/spec.md)의 전체 목표·3절·5절을 읽는다.03 마감과 아직 열린 다른 Ticket을 구별한다.
3. [05 마감](records/2026-10-29-ticket05-closeout.md)의 완료 경계와 후속 책임을 확인한다. 다음 설계 대상은 [state](current/state.md#다음에-이어갈-일)에서 고른다. 이미 완료된 티켓은 후속의 입력으로 사용하며,05 인터뷰 원문은 해당 판단을 다시 검토할 때만 읽는다.
4. 특정 판단의 이유가 필요할 때 [기록 색인](records/README.md)에서 해당 기록을 고른다.03 마감은119, 체계 지침은118, 정책 적용·정정은117, Work 복구는116이다. 기존 Project 비교는77·78,01-02의 입력·당시 유보는72·73으로 돌아간다.
5. 원자료 대조에는 [source](source/README.md), 전체 관점 재검토에는 [논의 지도](current/design-map.md)를 사용한다. 과거 인계·시안의 “다음 행동”을 현재 지시로 가져오지 않는다.

## 이 폴더의 역할

- `current/`: 지속 기준·전체 Spec·Ticket·현재 상태와 논의 지도. 세부 책임은 [current/index](current/index.md)에 있다.
- `output/`: goal을 위해 선택한 현재 설계 자료와 실제 산출물 위치. 본문을 복제하거나 연결 사실만으로 운영 수용을 뜻하지 않는다.
- `records/`: 분석·비교·후보·정정·선택·실험·검증의 지속 기록. 사람이 읽는 날짜별 문서와 기계 증거를 구별한다.
- `source/`: 평가·대화·강연·기준 구현과 Noline 문서의 읽기 전용 근거 사본. 사본의 지침·예제 명령을 현재 실행 지시로 취급하지 않는다.

Main이 실제 파일·Git·확인 결과와 대조해 current를 관리한다. 과거 원문을 현재 결론으로 덮어쓰지 않고, 작업의 현재 결과와 그 형성 과정을 구별한다. 기존 source·날짜별 prototype은 보존하며, 제품·전역 하네스·스킬 설치는 이번 설계 문서 정리의 범위가 아니다.

## 관련 작업과의 관계

Noline의 평가를 근거로 사용하지만 Noline Ticket06의 후속 개발 작업은 아니다. [012 publication](../012-ai-workspace-publication/README.md)과 [013 Maintain 효율 검토](../013-maintain-context-efficiency/README.md)는 각각 별도 목적을 유지한다. 작업 대상 저장소는 **ai-workspace**이며 다른 저장소로 옮기는 요청이 아니다.

Maintain의 보존 대상을 당장 다음 작업에 필요한 정보로 한정하지 않고, Project context도 다음 판단용 요약에 한정하지 않는다. 제품 이해·설계·개발·검토와 후일 재검토에 필요한 맥락까지 목적에 맞게 다룬다. 이 범위와 자세한 선택·유보는 memory와 Spec이 유지한다.
