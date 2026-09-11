# 현재 상태와 다음 행동

사용자가 Ticket 검토를 마치고 [Ticket 01 — 경비 합계 표시](../memory/tickets/01-expense-summary.md)를 첫 실행 대상으로 선택했다. 현재는 해당 Ticket의 보존 조건과 개선 목표를 바탕으로 변경 전 검사를 준비하는 단계다. 다음 작업은 현재 코드와 검사 대상을 대조하고 구체적인 runner와 최소 검사 방법을 정해 변경 전 결과를 확인하는 것이다.

도시 검색, 저장 용량, 경비 API, 서버 일정 응답 변환의 다른 초안은 [Ticket 색인](../memory/tickets/index.md)에 유지한다. 후속 실행 순서는 아직 정하지 않았다. 코드 범위별 진행 방식은 [Spec](../memory/spec/05-constraints-design-assumptions.md), 분석 주제별 확인·잔여 범위와 전체 완료 판단은 [품질 기준](../memory/spec/04-quality-and-completion.md)이 소유한다.

Main 보고상 제품 코드·테스트·설정 수정과 제품 동작 테스트·새 Verify 실행은 없다. [output](../../output/index.md)에도 제품 산출물이 없는 상태로 기록되어 있다. 폼 초기화·재진입, picker, 날짜 그룹, 저장 후 처리, 공통 데이터·경로·정리, 완료 상태와 설정 등은 [전체 후보](../memory/analysis-items.md)에 후속 범위로 남아 있다. 직접 걸리는 버그의 기대 동작·수정·선행 관계를 해당 실행 범위와 연결한다.

## 실행 전 확인할 근거와 한계

후보와 Ticket의 조사 근거는 Main의 대표 구현·사용처 확인 보고다. 전체 파일 정독이나 앱 동작 검증 결과는 아니다. 해당 검색 범위에서 제품 test 명령을 찾지 못했다는 보고가 있으며, 과거 타입·린트 실패는 재실행하지 않았다. 실행 시 현재 코드와 필요한 검사 기준선을 확인한다. 조사 기준과 선택 이유는 [추가 조사 기록](../../records/2026-09-11-01-additional-research.md), 과거 검사·설치 한계는 [구성 기록](../../records/2026-09-10-01-workspace-setup.md)에 있다. 과거 HEAD와 작업 트리 보고는 현재 저장소 상태를 보장하지 않는다.

사용자는 source 배경을 보강한 목표, 변경 전후 동작 보존 검증, 코드 범위별 진행 방식과 전체 분석 주제의 검토 범위 관리를 채택했다. 질문 해석의 교정은 [Ticket 경계 정정 기록](../../records/2026-09-11-02-ticket-boundary-correction.md), 진행 방식의 채택 범위와 원문 근거는 [합의 기록](../../records/2026-09-11-03-agreed-ticket-workflow.md)에 있다. 문서 준비와 제품 개선 완료는 구별한다.

## 대화 반영과 자동 동작의 확인 범위

기존 Main 보고에는 이 Workspace의 generation 1 active 상태, 일부 요청의 자동 Maintain 접수와 Evidence 수집 완료, 앞선 대화의 수동 전달·사후 보존이 있다. 수동 전달, 문서 반영, 사후 보존과 자동 hook 동작은 각각 다른 확인 범위다. 사후 보존의 출처와 한계는 [추가 조사 기록](../../records/2026-09-11-01-additional-research.md)에 연결되어 있다.

자동 응답 종료 처리의 완료와 과거 미동작 원인 해소, 사후 보존 본문·해시·대화 재현 범위는 이 판단에서 독립 확인되지 않았다. 남은 운영 확인은 Main이 별도로 맡으며 제품 리팩토링의 목표·완료 기준에 포함하지 않는다. 연결과 동작 확인은 [session binding 계약](../../../../harness/maintain/SESSION-BINDING-AND-LIFECYCLE.md)을 따른다. 제공된 `status.json`의 receipt·result·finished_at은 null이며 제품 Verify 결과가 없다.

## 분석 원자료

후보 판단에는 [Workspace 안의 분석 보존본](../../source/codebase-analysis/README.md)과 [source 색인](../../source/index.md)을 사용한다. 최초 방향의 원문은 [사용자 발췌](../../source/user-direction.md)에 있다. 원래 분석 경로의 향후 삭제에 대비해 보존했으며 당시 원래 파일은 삭제하지 않았다. 원문 일치와 재진입 확인의 기존 증명 범위는 [분석 보존 검증](../../records/2026-09-10-04-analysis-preservation-validation.md)에 있고 제품 동작 검증과는 구별한다.
