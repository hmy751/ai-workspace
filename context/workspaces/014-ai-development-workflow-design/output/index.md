# 현재 선택한 설계 자료와 산출물

현재 goal은 전체 역할과 가능성을 이해하고 각 부분을 세밀하게 설계하는 것이다. B의 검토자 직접 수정 방향을 선택했으며, 전체 운영 아키텍처의 확정이나 새 스킬·개발 워크플로 구현은 아직 없다.

- [Spec 초안](../current/spec.md): 전체 목적·공통 기준·제약에 더해 현재 전체 잠정안·선택·주요 미결정을 유지한다. 014의 설계 문서 운영과 개선할 시스템의 Spec·Ticket 설계를 구별한다.
- [Ticket 초안 목록](../current/tickets/index.md): 상위 01~07과 하위 Ticket으로 나누어 구체화할 결과와 연결. 본문과 색인은 current가 소유하며 여기에는 복제하지 않는다. 각 설계 작업의 상세 결과와 진행은 해당 Ticket에서 확인한다.
- [코드 기준 논의 전 체크포인트](../records/2026-10-13-29-discussion-checkpoint-and-code-criteria-scope.md): 코드 기준 탐색을 시작한 배경. 마지막 정리 뒤 대화의 중요한 변화, 브레이크·컨텍스트·워크플로와 코드 기준 논의의 관계, 미결정과 선택적 원문 보존을 연결한다.
- [code-template 참고 자료 확인](../records/2026-10-13-30-code-template-reference-and-authorship-sampling.md): 코드 기준 논의에 사용할 지정 예제의 내용과 한계, 회사 코드의 사용자 작성 부분을 좁혀 보는 조사 제안.
- [책임 분리 선호와 상황별 조건](../records/2026-10-13-31-criteria-roles-and-responsibility-interview.md): 현재 논의 위치. 페이지·합성형 UI·재사용 단위·기능 Hook 내부 분리와 기존 도구에 맡긴 책임에 관한 인터뷰, code-template 탐색이 끝난 것은 아니라는 정정과 다음 후보. 현재 선호를 모은 자료이며 확정된 코드 원칙은 아니다.
- [작업 단계 우선순위와 코드 기준의 근거 후보](../records/2026-10-13-28-execution-system-priority-and-code-criteria.md): Main과 작업을 결정하는 단계와 구현 단계를 구별하고, 컨텍스트·코드 기준·절차·도구를 우선 구체화하려는 사용자 의도를 보존한다.
- [원자료 조사와 합성안 재검토](../records/2026-10-13-27-source-investigation-and-proposal-reset.md): Matt·Lauren·Vercel의 기존·추가 1차 자료에서 실제 계약과 판본·공개 한계를 확인하고 앞선 인수 예시와 구별한다. 당시 선행 설계부터 논의하자는 제안과 현재 우선순위는 구별한다.
- [구현·품질 검토·실제 검증의 워크플로 비교](../records/2026-10-12-13-implementation-review-verification-workflows.md): 강연·Vercel·기존 구성에서 만든 세 안, 가상 작업 예시와 과거 사례 대조. 미채택 설계안이며 당시 C 기본 추천은 아래 후속 비교에서 다시 판단했다. 앞선 여행 조회 비교는 기록 12에 보조 자료로 남는다.
- [B/C의 상황별 비교](../records/2026-10-12-14-reviewer-editing-scenarios.md): C를 기본으로 볼 근거의 한계를 확인하고, 같은 요구에서 검토자 직접 수정과 구현자 수정의 차이를 구체화했다. 당시 기본 미정 판단을 남긴 비교 이력이며, 이후 B 방향을 선택했다.
- [B 방향 선택과 시작점](../records/2026-10-12-15-reviewer-editing-choice-and-start.md): 현재 사용자 선택과 Main의 작업 정의·구현 인수·실행 중 재판단의 경계. 상세 운영·실제 구현은 미완료다.
- [B의 인수·수정·최종 검증 상세 초안](../records/2026-10-12-16-b-execution-review-verification-contract.md): 구현자 입력과 결과, 검토자의 기준·직접 수정 범위, 구현자의 최종 실제 확인과 Main의 완료 판단 제안. 최종 검증 담당은 아래 기록 17에서 제안을 변경했다. 실제 실행 효과는 미확인이다.
- [반영 근거와 당시 연결 설계 제안](../records/2026-10-12-17-workflow-basis-and-connected-design.md): 검토자가 최종 실제 확인까지 이어가는 진행안, 자료별 반영 정도와 남은 공백, 관련 Ticket을 같은 장면에서 구체화하자는 당시 제안. 다음 순서는 아래 기록 18에서 다시 정했다.
- [01-02 자료 논의와 기록 체크포인트](../records/2026-10-12-18-quality-materials-next-step.md): 사용자가 선택한 다음 순서, 강연 설명에서 약해진 구체 방법, 자료 논의 뒤 기준·배치를 판단할 범위.
- [01-02 설계·테스트 방법의 구체 비교](../records/2026-10-12-19-design-and-testing-methods.md): 가상 저장 기능의 설계·검사 대비와 현행 기준의 공통점·차이. 현재 논의 자료이며 기준 채택·제품 구현 결과가 아니다.
- [전체 설계와 Spec·Ticket 사용 방향 재검토](../records/2026-10-13-20-overall-design-and-ticket-direction.md): 사용자의 최신 요청, 현재 연결의 공백, 전체안 중심으로 논의를 모을 방법의 제안.
- [설계 논의 지도](../current/design-map.md): 다음 논의를 위해 선택한 현재 작업 자료. 영역·질문·후보를 보여 주며 최종 분류나 채택안이 아니다.
- [기반과 강연 읽기](../records/2026-10-12-02-framework-and-lecture-reading.md): 구체화에 사용할 자료 대조 결과와 검토할 차이.
- [평가·인터뷰 연결](../records/2026-10-12-01-background-and-evaluation.md): 기존 사용 경험과 효과·한계를 설계 논의로 연결하는 근거.

앞으로 논의한 설계안이나 실제 산출물이 goal의 현재 결과로 선택되면 이 지도에서 연결하고, 제안·채택·구현·검증 상태를 구별한다. 사본을 별도 결과로 복제하지 않으며 output에 있다는 사실만으로 최종 acceptance를 뜻하지 않는다.
