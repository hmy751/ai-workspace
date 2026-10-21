# AI 개발 작업 체계의 개선 설계

**현재 상태: Ticket03의 구성안·대표 본문·읽기와 갱신 책임 구체화를 완료했다.** [마무리119](records/2026-10-20-119-ticket03-closeout.md)와 [03 완료 조건](current/tickets/03-project-context.md)에서 판단 근거와 후속 범위를 확인한다. Workspace014 전체는 계속 진행 중이며, 이번 마무리에서 다음 Ticket을 착수하지 않았다.

Noline에 이식해 사용한 Project·Work context와 스킬의 평가, 사용자 인터뷰, 개발 에이전트 관련 강연을 바탕으로 **ai-workspace와 실제 개발 방식을 어떻게 발전시킬지 설계하는 작업**이다. 좋은 구현을 돕는 컨텍스트·코드 기준·절차·도구와 기록·경험 반영을 함께 다룬다. 전체 운영 체계 확정이나 실제 설치·스킬 구현은 아직 끝나지 않았다.

사용자는2026-10-12에 독립 Workspace와 근거 사본을 함께 보존해 새 세션도 논의를 이어가도록 요청했다. 이 폴더는 설계 작업의 기록 단위이며 Reference Harness를 설치·실행한 Workspace가 아니다. [Spec](current/spec.md)이 전체 구상과 미결정을, [Ticket01~07](current/tickets/index.md)이 결과별 책임을 맡는다. 검토자가 필요한 품질 수정을 직접 수행하는 B 방향은 선택했고 상세 인계·검증·운영은 후속에서 구체화한다.

04-02는 기존 설명 스킬 수정안을 보류하고 보고서 사건의 연속 대화·당시 Git 자료를 [새 source](source/artifact-explanation-scenes/README.md)로 구성했다. 원문 경계·동일성의 독립 검토는 마쳤으며 당시 실행 전체 재현은 미완료다. 현재 판단과 다음 행동은 [04-02](current/tickets/04-skill-improvements/04-02-artifact-explanation.md)에서 이어간다.

## 지금 읽을 결과

실물은 [development-workflow](records/prototypes/development-workflow/README.md) 한 폴더에서 계속 발전시킨다. 그 안의 noline-demo/context에 Personal의 개인 판단, Project의 제품 계약·개발 가이드·현재 사실, Work의 이번 선택·진행·결과를 구별했다. [CONTENT-POLICY](records/prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md)는 본문과 형성 자료의 관리를, [SYSTEM-GUIDANCE](records/prototypes/development-workflow/noline-demo/context/SYSTEM-GUIDANCE.md)는 체계 지침과 진입·상세의 역할을 소유한다.

데모 독자는 바깥014 기록 없이 본문을 이해할 수 있어야 한다. 작성·평가·정정의 전체 과정은014 records가 보존하고, 개별 본문 수정에 필요한 형성 이유와 최소 근거는 그 본문 가까이 둔다. 실제 작성 논의를 예제 제품의 사건으로 바꾸지 않는다.

Work는 기존 current·Spec·Ticket·source·output·records의 형태와 제약을 유지한다. [116](records/2026-10-20-116-defer-work-content-policy.md)의 복구를 되돌려 새 background를 적용하지 않는다. Development의 최종 위치·Owner·스킬 연결은01-01·04-03의 후속 범위다.03 완료는 실제 Noline 적용·모든 기준 채택·장기 효과 확인을 포함하지 않는다.

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
