# Records

이 Workspace에서 수행한 Spec·Ticket 도입 논의, 조사, 후보 비교, 사용자 정정, 검토 결과와 선택 근거를 보존한다. 현재 적용하는 방향은 [current](../current/index.md)가, 선택된 결과의 진입점은 [output](../output/index.md)이 소유한다.

## 현재 선택을 먼저 확인할 때

- [08 후속 합의와 네 스킬의 Reference 통합](2026-09-08-15-skills-spec-ticket-reference-integration.md): 사용자 반영 요청에 따른 미커밋 변경. 상위 계약·payload·guidance·이식 절차와 검증·제한 평가의 범위를 보존한다.
- [Reference 재확인과 08 재이식 분석](2026-09-08-14-skills-spec-ticket-reintegration-assessment.md): 외부 연구의 후속 Spec·Ticket 합의와 네 스킬을 현재 Reference에 대조했다. 상위 계약·guidance·이식 절차의 변경 지점, Main·Maintain 연결과 실제 검증 상한을 정리했다. 설치 전 분석이다.
- [Project context 파일명 정리와 적용 커밋](2026-09-08-13-project-context-filename-and-commit.md): 옛 `03` 번호 제거, 실제 경로·링크 대조와 후속 커밋 요청.
- [Reference 적용과 검증](2026-09-08-12-reference-spec-ticket-implementation.md): 설계 기록 커밋 후 구조·Recover·Maintain·생성 경로 적용. 변경 전에도 재현되는 Verify 실패와 실제 host 미검증 범위를 구별한다.

- [설계 합의와 적용 전 남은 작업](2026-09-08-11-design-status-and-remaining-work.md): 기록 정리 시점의 확정 내용·열린 부분·남은 실제 적용 작업을 모았다. 이후 상태는 current에서 이어간다.
- [Spec 구성의 채택 근거](2026-09-08-01-spec-components-decision.md)와 [Spec 배치·기존 파일 대체](2026-09-08-02-workspace-spec-scope.md).
- [Ticket 관리 선택](2026-09-08-07-memory-ticket-placement-decision.md)과 [기본 진입·실행자 구상](2026-09-08-08-workspace-ticket-execution-direction.md).
- [기존 Main·Maintain 역할 확인](2026-09-08-10-spec-ticket-authorship-independent-review.md): 리뷰 본문 뒤 후속 사용자 확인까지 읽는다.

아래 분리·제거·보존 후보와 역할 분석은 선택 과정의 근거다. 당시 후보·리뷰 선호를 현재 규칙으로 읽지 않는다.

## 대화와 판단의 진행 순서

- [2026-09-07-01-session-synthesis.md](2026-09-07-01-session-synthesis.md): 이번 대화 처음부터 010 분리 요청까지의 종합 기록. 최근 트레이드오프 리뷰만으로 축소하지 않고 개념·시스템 조사·스냅샷·memory/state·Ticket 상태·배치 후보와 판단 변화를 함께 보존한다.
- [2026-09-08-01-spec-components-decision.md](2026-09-08-01-spec-components-decision.md): 이후 연구·원문 재독, Spec 구성의 축약·확장, 독립 개선 리뷰, 기존 문서의 어휘로 설명하기 위한 정정, 예시·설명 문서 분리와 다섯 구성의 채택까지. 관련 핵심 원문과 평가 이유를 보존한다.
- [2026-09-08-02-workspace-spec-scope.md](2026-09-08-02-workspace-spec-scope.md): Spec 하나라는 가정과 정정, memory에서 Workspace와 함께 유지하는 수명, goal·constraints 대체, project-context 유지와 다섯 Markdown 파일 결정.
- [2026-09-08-03-ticket-references-and-placement.md](2026-09-08-03-ticket-references-and-placement.md): Matt·Spec Kit·Kiro·OpenSpec의 실행 단위와 상태 용례, Ticket 정의를 memory에 두고 진행을 state에 두는 제안 및 관리 비용. 사용자 채택 전 의견이다.
- [2026-09-08-04-memory-removal-and-records-boundary.md](2026-09-08-04-memory-removal-and-records-boundary.md): Ticket을 정의·진행과 함께 관리하는 후보에서 memory 폴더 제거 재검토로 이어진 대화. 기존 records/current 선택 이유와 제거 후에도 유지할 현재 의미의 선택·갱신 책임.
- [2026-09-08-05-memory-ticket-independent-review.md](2026-09-08-05-memory-ticket-independent-review.md): 사용자 요청에 따른 독립 제3 리뷰. 전달한 발화·자료·판단 범위와 결과 상태.
- [2026-09-08-06-ticket-preservation-placement-candidate.md](2026-09-08-06-ticket-preservation-placement-candidate.md): 현재 영향이 없는 Ticket도 기록으로 남길 수 있다는 사용자 생각과 유보. 현재 필요한 Ticket은 current, 기록으로만 남길 Ticket은 records에 두는 구체안과 비용. 채택 전이다.
- [2026-09-08-07-memory-ticket-placement-decision.md](2026-09-08-07-memory-ticket-placement-decision.md): memory 유지와 Ticket 정의·진행 함께 관리, 필요에 따른 records 사용, Matt를 기본으로 삼되 구성을 열어 두는 사용자 선택. 엄격한 분리·이동·이력 체계를 추가하지 않는다.
- [2026-09-08-08-workspace-ticket-execution-direction.md](2026-09-08-08-workspace-ticket-execution-direction.md): 전체 Spec·Workspace 담당과 독립 Ticket 실행자에 관한 구상. 기존 Recover를 확인해 Spec 전체를 기본 진입에서 읽는 방향으로 보완하고 실행자 범위를 열어 둔 대화. 당시 열려 있던 갱신 역할은 10의 후속 확인으로 이어졌다.
- [2026-09-08-09-main-maintain-responsibility-analysis.md](2026-09-08-09-main-maintain-responsibility-analysis.md): 판단 책임을 Main에 몰게 되는지에 대한 사용자 문제 제기. 실제 Maintain의 의미 판단과 007의 목적·입력 선택을 확인하고, 작업 판단·실행과 Context 반영을 상황별로 비교한 미채택 제안.
- [2026-09-08-10-spec-ticket-authorship-independent-review.md](2026-09-08-10-spec-ticket-authorship-independent-review.md): Spec·Ticket을 Main이 작성해야 하는지 독립 검토한 입력·리뷰 본문·Main 평가. 후속 사용자는 Maintain이 기록·갱신을 맡고 Main이 작업 조율을 맡는 방향으로 정리했다. 구현은 아직 적용하지 않았다.

초기 공개 비교와 개발 영향 분석은 009의 원래 기록을 정확히 연결해 사용한다. 종합 기록은 그 파일들을 대체하는 코드 감사 보고서나 대화 전체의 축어록이 아니다.

첫 기록 당시 미결정이던 Spec 구성요소는 2026-09-08 채택했다. 과거 기록을 새 결론으로 덮어쓰지 않으며 현재 선택은 [구성 설명](../output/spec-components-and-rationale.md)과 [예시 Spec](../output/spec-example-travel-answer.md)에서 읽는다.
