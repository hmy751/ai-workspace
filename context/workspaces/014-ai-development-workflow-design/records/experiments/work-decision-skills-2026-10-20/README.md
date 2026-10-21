# work-discussion·reconsider-work의 기존판·보완판 비교

2026-10-20 실행 자료. 같은 조건의 기존판과 보완판을 각2회, 네 조건에서 총16회 실행했다. 실제 Reference 스킬이나 Noline 제품에는 적용하지 않았다.

결과와 판단은 [비교 기록](../../2026-10-20-ticket04-01-blind-skill-comparison.md)이 소유한다. 이 폴더에는 입력·판본·원응답·독립 검토 근거를 보존한다. 반대 조건 D2·R2는 실제 Noline 사건이 아닌 가상 변형이다.

## 읽을 자료

- [실행 전 계획](protocol.md): 범위·원자료 관계·평가 관점.
- [실행 목록과 입력 해시](run-manifest.json): 각 실행의 조건·판본·반복 번호·실제 지시문·입력 해시.
- [work-discussion 변경분](work-discussion.patch), [reconsider-work 변경분](reconsider-work.patch): 실험에 사용한 실제 문구 차이.
- [기존 work-discussion](versions/current/work-discussion/SKILL.md), [보완 work-discussion](versions/proposed/work-discussion/SKILL.md), [기존 reconsider-work](versions/current/reconsider-work/SKILL.md), [보완 reconsider-work](versions/proposed/reconsider-work/SKILL.md): 전체 판본.
- [공통 실행 지침](common/AGENTS.md), [공통 설명·근거 기준](common/explanation-and-evidence-criteria.md): 모든 실행에 같은 내용으로 제공.
- [독립 검토 지침](reviews/REVIEW.md), [작업 구체화 검토](reviews/definition.md), [재판단 검토](reviews/reconsideration.md): 버전 매핑을 제공하지 않은 두 검토자의 원보고서.
- [구체화 검토 응답 매핑](review-D-mapping.json), [재판단 검토 응답 매핑](review-R-mapping.json): 검토 당시에는 숨긴 응답 번호와 실제 실행의 연결.
- [보존·무변경 확인](integrity.json): 입력 해시·응답 보존·Reference와 기준판 일치 여부.

## 조건과 원응답

각 링크의 두 응답은 반복1·반복2 순서다.

| 조건 | 입력 | 기존 스킬 | 보완 스킬 |
| --- | --- | --- | --- |
| D1: 기존 표시를 보존하는 경비 합계 Ticket | [요청](case-inputs/D1/REQUEST.md), [Ticket](case-inputs/D1/ticket.md), [관찰](case-inputs/D1/observations.md) | [run-11](results/run-11.md), [run-15](results/run-15.md) | [run-14](results/run-14.md), [run-05](results/run-05.md) |
| D2: 표시 통일로 범위가 바뀌었으나 기준 미선택 | [최신 범위](case-inputs/D2/latest-scope.md), [Ticket](case-inputs/D2/ticket.md) | [run-10](results/run-10.md), [run-07](results/run-07.md) | [run-02](results/run-02.md), [run-01](results/run-01.md) |
| R1: 기존 화면의 복귀 인지가 충분한지는 미관찰 | [요청](case-inputs/R1/REQUEST.md), [이전 정책](case-inputs/R1/original-policy.md), [후속 정책](case-inputs/R1/revised-policy.md), [관찰](case-inputs/R1/observations.md) | [run-16](results/run-16.md), [run-06](results/run-06.md) | [run-03](results/run-03.md), [run-09](results/run-09.md) |
| R2: 화면을 잠시 보지 않은 사용자가 복귀를 놓침 | [UX 관찰](case-inputs/R2/ux-observation.md), [현재 조사](case-inputs/R2/observations.md) | [run-08](results/run-08.md), [run-12](results/run-12.md) | [run-13](results/run-13.md), [run-04](results/run-04.md) |

각 case 폴더의 나머지 파일도 해당 입력에 포함된다. 원응답의 `/tmp/work-decision-trial-20261020/runs/run-XX/context/work/` 링크는 실행 당시 경로를 그대로 보존했다. 재접근할 때는 실행 목록에서 case를 찾아 이 폴더의 `case-inputs/<case>/`에 있는 같은 파일을 읽는다. 임시 디렉터리의 존속에 판단 근거를 의존하지 않는다.

독립 검토자는 각 계열의 두 조건을 case-1·case-2로, 응답을 섞은 answer-1~4로 받았다. 원응답의 자료 링크만 해당 검토 사본으로 바꿨고 응답 내용은 유지했다. 보고서의 case·answer 번호는 매핑 파일로 되짚을 수 있다. 검토자는 스킬 판본·버전·사후 정정·Main의 결과 해석을 받지 않았다.

## 재검토할 때 지킬 경계

제품 전체와 긴 대화를 복원한 시험이 아니다. 조사에서 보고된 사실을 선별해 제공한 뒤 판단한 비교다. 입력 선정의 영향을 버전 효과와 혼동하지 않는다. 같은 모델·추론 설정을 상속했지만 생성 결과의 결정론이나 일반 성능을 보장하지 않는다.

범위 밖 열람은 실행 지시로 제한했다. 별도 OS 격리를 만들지 않았고 Main이 모든 도구 접근 이력을 감사한 것도 아니다. 해시 검사는 입력이 바뀌지 않았다는 확인이며 접근 격리를 증명하지 않는다.
