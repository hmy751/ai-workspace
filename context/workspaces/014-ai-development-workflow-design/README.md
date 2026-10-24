# AI 개발 작업 체계의 개선 설계

**01-01·01-03 설계 결과를 마감했다.** [완료 조건 대조와 Spec·04의 다음 범위](records/2026-10-24-ticket01-01-03-closeout-and-next-scope.md)에서 근거·비용·한계를 확인한다. 다음 추천은04-03의 개별 맥락 스킬 보완이다. 상위01·04와 전체 Workspace는 아직 완료가 아니며 실제 운영 효과와 구별한다.

검증자 실행 반영: [검증 상세](records/prototypes/development-workflow/skills/development/references/verification.md)를 생성하고 development·review·execution과 연결했다. [합의 대조와 확인 기록](records/2026-10-24-verifier-runtime-integration.md)에서 항목별 반영·대표 장면·실제 검사·한계를 읽는다.

**구현·개선 검토1~15와 검증자1~12의 합의를 실행 prototype에 통합했다.** [전체 흐름 대조·실제 확인](records/2026-10-24-verifier-runtime-integration.md)에서 구현 중 검사·개선 수정·별도 검증·재검증·Main 완료와 기록의 연결을 확인한다. Main의 대표 장면 대조와 메모리 예제 실행을 마쳤으며, 여러 agent의 전체 개발 수행·운영 설치·일반 효과 검증은 별도다. 개별 맥락 스킬 보완과 대상별 연결·전체 체계 종합은 해당 후속 Ticket에 남아 있다.

04-02는 [explain 본체·상세·형성 자료](records/prototypes/development-workflow/skills/explain/SKILL.md)로 기존 두 실행 경로를 통합했다. 이후 반복 비교를 재검토해 원래 목적·실제 사용 경험·외부 자료를 선별하고 독립 개선 리뷰를 거쳤다. 사용자 요청으로 [질문 범위·실제 설명 연결·첫 전달 호출을 구체화](records/2026-10-24-ticket04-02-selective-improvement-adoption.md)했다. prototype 반영과 정적·문단 대조를 마쳤으며 운영 설치·실제 수행 효과 확인은 별도다. 현재 상태와 재개는 [04-02](current/tickets/04-skill-improvements/04-02-artifact-explanation.md)가 소유한다.

**현재 상태: Ticket03의 구성안·대표 본문·읽기와 갱신 책임 구체화를 완료했다.** [마무리119](records/2026-10-20-119-ticket03-closeout.md)와 [03 완료 조건](current/tickets/03-project-context.md)에서 판단 근거와 후속 범위를 확인한다. Workspace014 전체는 계속 진행 중이며, 이번 마무리에서 다음 Ticket을 착수하지 않았다.

Noline에 이식해 사용한 Project·Work context와 스킬의 평가, 사용자 인터뷰, 개발 에이전트 관련 강연을 바탕으로 **ai-workspace와 실제 개발 방식을 어떻게 발전시킬지 설계하는 작업**이다. 좋은 구현을 돕는 컨텍스트·코드 기준·절차·도구와 기록·경험 반영을 함께 다룬다. 전체 운영 체계 확정이나 실제 설치·스킬 구현은 아직 끝나지 않았다.

사용자는2026-10-12에 독립 Workspace와 근거 사본을 함께 보존해 새 세션도 논의를 이어가도록 요청했다. 이 폴더는 설계 작업의 기록 단위이며 Reference Harness를 설치·실행한 Workspace가 아니다. [Spec](current/spec.md)이 전체 구상과 미결정을, [Ticket01~07](current/tickets/index.md)이 결과별 책임을 맡는다. 과거 B 선택 뒤 사용자는 [Personal 기반 구현·별도 관점 검토·Main 적용 판단과 동적 라우팅 구상](records/2026-10-21-dynamic-context-and-review-intent.md)을 설명했다. 역할별 입력·수정·검증은 이 의도와 레퍼런스를 함께 비교해 구체화한다.

04-02는 [새 source](source/artifact-explanation-scenes/README.md)에 보고서·interceptor·network 흐름·저장 용량·여행 브리핑·Network 첫 완료 보고의 여섯 묶음을 구성했다. [시점·본문 비교 범위](records/2026-10-22-ticket04-02-source-expansion-and-coverage.md)에서 사건별 역할과 당시 자료 공백을 구별했다. 원문 보존과 당시 실행 재현·스킬 효과 검증은 별개다. 본문 비교에서 확인한 국소 개선과 미실행인 적용 배치 비교를 구별한다. 현재 판단과 다음 행동은 [04-02](current/tickets/04-skill-improvements/04-02-artifact-explanation.md)에서 이어간다.

## 지금 읽을 결과

실물은 [development-workflow](records/prototypes/development-workflow/README.md) 한 폴더에서 계속 발전시킨다. 그 안의 noline-demo/context에 Personal의 개인 판단, Project의 제품 계약·개발 가이드·현재 사실, Work의 이번 선택·진행·결과를 구별했다. [CONTENT-POLICY](records/prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md)는 본문과 형성 자료의 관리를, [SYSTEM-GUIDANCE](records/prototypes/development-workflow/noline-demo/context/SYSTEM-GUIDANCE.md)는 체계 지침과 진입·상세의 역할을 소유한다.

데모 독자는 바깥014 기록 없이 본문을 이해할 수 있어야 한다. 작성·평가·정정의 전체 과정은014 records가 보존하고, 개별 본문 수정에 필요한 형성 이유와 최소 근거는 그 본문 가까이 둔다. 실제 작성 논의를 예제 제품의 사건으로 바꾸지 않는다.

Work는 기존 current·Spec·Ticket·source·output·records의 형태와 제약을 유지한다. [116](records/2026-10-20-116-defer-work-content-policy.md)의 복구를 되돌려 새 background를 적용하지 않는다. Development의 prototype 진입·공통 본문은 스킬로 이전했고, 상세 실행·조건별 맥락 연결도 반영했다. 실제 대상의 개별 맥락 스킬 보완·설치와 수행 효과는01-01·04-03 및06·07에 남는다.03 완료는 실제 Noline 적용·모든 기준 채택·장기 효과 확인을 포함하지 않는다.

## 배경 없이 들어올 때

1. [current/index](current/index.md), [현재 상태](current/state.md), [현재 산출물](output/index.md)을 읽고 실제 Git 상태를 확인한다.
2. [memory](current/memory.md)의 지속할 사용자 의도·정정과 [Spec](current/spec.md)의 전체 목표·3절·5절을 읽는다.03 마감과 아직 열린 다른 Ticket을 구별한다.
3. 다음 워크플로 논의를 재개하면 [01-01](current/tickets/01-development-workflow/01-01-development-flow.md)과 [04-03](current/tickets/04-skill-improvements/04-03-context-skills.md), 현재 DEVELOPMENT를 함께 본다.02 완료를 선행 조건으로 두지 않는다.
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
