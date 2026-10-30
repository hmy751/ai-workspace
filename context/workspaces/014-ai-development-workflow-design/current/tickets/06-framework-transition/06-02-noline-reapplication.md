# 06-02 — Noline의 기존 설치에 다시 적용한다

**현재 — 2026-10-30 실행 묶음 반영·직접 확인:** [이번 결과](../../../records/2026-10-30-ticket06-execution-skills-and-retirement.md). development·improvement-loop 설치와 work-discussion·create의 비충돌 보완을 Reference에서 확인한 뒤 Noline에 적응했다. Noline 옛4개 실행 스킬·bridge는 소비 경로·근거 보존을 처리한 뒤 제거했다. 기존 Work 기록·생성/전환·Maintain 계약을 유지했다. 전체 Ticket은 진행 중이며 남은 운영 계약 전환과 실제 host 통합은02에 둔다. 아래 날짜별 첫 부분 반영은 이전 경과이고, 전환표의 ‘착수 시’는 이번 적용 전 상태다.

**부분 반영·직접 확인 — 2026-10-30:** [적용·보존·검증 연결](../../../records/2026-10-30-ticket06-02-noline-partial-application.md)을 마쳤다. Source `f5082bc3`의153개 경로를 Noline `main @ 4fb309d2`에 반영했다. Noline 고유 기준과 제품·artifacts·Maintain·기존 병렬 변경을 보존했고, 정적 링크·bridge·호출 설정과 기본001·명시001·002 Recover를 확인했다. 자체 검사의 실패는 기존 과거 링크8건 그대로다. Maintain·Work 계약·host 통합 확인은 계속02에 둔다.

상태: **진행 중 · context·실행 스킬 반영과 옛4개 제거·정적/읽기 전용 확인 완료 · 새 계약 연결·host 확인은02 후속**. [앞선 context 적용 결과](../../../records/2026-10-30-ticket06-02-noline-partial-application.md)가 Noline001의 결과 정본과 receipt를 연결한다. [적용안 재대조](../../../records/2026-10-30-ticket06-02-reference-refresh-review.md)와 [첫 적용안](../../../records/2026-10-29-ticket06-02-noline-preflight-and-plan.md)은 선택·이전 관찰 근거다. Maintain·Work 전환·통합 테스트는02에 유지하며 전체 workflow 적용으로 확대하지 않는다.

## Noline의 남은 전환과 지금 적용할 범위

**2026-10-30 재대조·착수:** 사용자 지적 “development 생기지도 않았고 또 기존 스킬중에 지워야 하는 게 있을 수도”에 따라, 남은 일을02 이후 통합 테스트로만 묶었던 안내를 바로잡는다. 사용자는 두 티켓 보완과 Maintain에서 분리 가능한 부분의 실제 반영을 요청했다. 아래는 착수 시 상태와 선택한 범위다. 해당 비충돌 설치·교체·제거를 마쳤으며 실제 결과·검증·보존·미확인은 위 이번 결과에서 확인한다.

| 대상 | 착수 시 실제 상태 | 이번 반영과 후속 경계 |
| --- | --- | --- |
| development·improvement-loop | Reference와 Noline 모두 미설치 |06-01에서 현행 Work 계약에 적응·확인한 판본을 받아 Noline 경로·고유 기준에 연결한다. |
| work-discussion·create-context-workspace | 기존 본체 유지 | Reference의 비충돌 보완을 반영하고 Noline의 기록·JSON·Recover·activation 계약은 보존한다. |
| read-project-context·update-project-context·work-artifact-briefing·explanation-recovery | 비활성 호환 스킬4개와 bridge가 남음 | 검사·현재 evidence 입력·역사 링크를 대조해 새 읽기/갱신/설명 경로로 전환하고 옛 실행 폴더·bridge를 제거한다. 과거 본문·결정·receipt의 사실은 보존한다. |
| reconsider-work·start-app | 현재 고유 역할 유지 | development 도입을 이유로 제거하지 않는다. |
| noline-work | deprecated, 원본·bridge 보존 결정 있음 |2026-09-10의 명시 보존 결정을 유지한다. 다른4개의 교체와 묶어 자동 삭제하지 않는다. |
| Maintain·수집기·Work 기록과 전환 | 현행 운영 중 | 장치·hook·설정·기록 Owner·activation 변경은02에 둔다. 스킬 참조 전환에 필요한 현재 evidence 경로 변경과 운영 schema 변경을 구별한다. |

Maintain 유보는 모든 실행 본문의 준비·설치·옛 스킬 정리를 유보한다는 뜻이 아니다. 이번에는 기존 Work 계약으로 적응한 실행 묶음을 반영한다.02가 소유하는 기록·구성·전환 정책을 새로 정하지 않으며, 실제 host 통합 테스트는 기존 선택대로02에서 진행한다. 설치·정적 확인과 실제 발견·호출·효과를 구별한다.

## 만들 결과

Reference에서 확인한 개발 작업 체계를 [Noline](</Users/hammyeong-yeon/Desktop/10_work/noline/CLAUDE.md>)의 기존 설치·제품 맥락·진행 작업에 맞게 반영한다. 이전 이식 뒤 Noline에서 달라진 내용과 사용자 변경을 보존하며, 공통 변경을 적용한 부분·대상에 맞게 적응한 부분·유지 또는 제외한 부분과 그 이유를 설명할 수 있게 한다.

기준은 **이전 적용 판본·06-01의 새 판본·Noline 현행**의 대조다. Reference를 통째로 덮어쓰거나 Noline의 제품 문서를 demo 내용으로 교체하지 않는다. 사전 준비·적용 계획·실제 반영·직접 확인을 구별해 남긴다.

## 적용 범위와 연결

| 대상 | 이 Ticket에서 맡는 결과 |
| --- | --- |
| 기존 설치와 제품별 차이 | 현재 Project 내용 Owner, 기존 rules·guards·runbooks·깊은 제품 문서, 스킬 원본과 bridge, Workspace와 진행 작업을 확인하고 새 공통 기준과 대응시킨다. |
| 새 개발 체계 | 선택된 Personal·Project·Work 연결, development·explain·맥락 관련 스킬·improvement-loop를 Noline의 실제 진입·수행·갱신 경로에 적용한다.06-01의 이름·폴더만으로 target에서도 동작한다고 가정하지 않는다. |
| 기존 장치 전환 | Maintain·Recover·Verify와 실제 target의 추가 연결을 확인한다. 자동 Maintainer 제거 후 기록 책임·재개·검증을 잇고, 별도 수집기 등 target 고유 의존의 유지·전환 필요를 판단한다. |
| 적용과 복구 | 현재 판본·사용자 변경·진행 중 작업을 고정해 적용 경계를 정하고 실제 변경을 확인한다. target의 파일 배치·명령·원문 접근 차이를 반영하고 실패 시 되돌릴 범위를 남긴다. |
| 경험 왕복 | Noline에서 발견한 문제를 공통 기준의 부족과 대상 고유 사정으로 나눈다. 공통 개선은 필요한 원문·조건·판본·최소 근거와 함께 Reference의 해당 책임으로 돌려주고, 채택된 변경의 target 반영까지 추적한다. |

02의 기록 운영과01-02의 품질 기준 후속은 채택된 판본으로 받는다. Reference 적용 뒤 추가 변경이 생기면 차이를 다시 대조한다. 이미 끝난 개발 흐름·검증 역할을 target에 들어왔다는 이유만으로 처음부터 설계하지 않는다.

실제 설치·수행 경로의 확인은 이 Ticket이 맡고, 전체 체계의 사용·부담·효과를 어떤 장면에서 볼지는 [07](../07-integrated-rehearsal.md)과 연결한다. Noline 제품 리팩터링의 다음 Ticket을 자동 착수하거나 제품의 모든 미확인을 이번 이식의 필수 조건으로 올리지 않는다.

## 시작할 때 확인할 입력

- 06-01의 반영 판본·변경 이유·직접 확인·남은 제약과 공통/대상 적응 경계.
- [이전 Noline 적용 Workspace](../../../../011-noline-harness-upgrade/README.md)와 [보존된 설치·설계 근거](../../../source/reading/noline-evaluation/reviews/noline-design-basis.md). 당시 source/target 기준과 실제 Noline 현행의 차이를 확인한다.
- 실제 target의 root·Work·Project 진입·관리 지침, 운영 스킬·설정·현재 작업·Git 상태. 최초 현황 파악 결과를 후속 적용 시점에도 유효하다고 가정하지 않는다.
- [05 배치 입력](../../../records/2026-10-29-ticket05-closeout.md): Personal 경험 정본·동반 자료·같은 세션 원문 접근과 압축/재개/누락 처리. 한 host의 경로 확인을 다른 host의 지원 보장으로 확대하지 않는다.

## 완료 조건과 확인

- source 판본·이전 적용 기준·target 현행을 대조했고, 적용·적응·유지·제외의 이유와 실제 대상이 연결돼 있다.
- 선택한 변경이 Noline의 실제 진입·스킬·문서·설정·장치에 반영돼 있다. 기존 내용 Owner와 진행 중 작업, 사용자 변경을 보존했고 옛 호출·서로 다른 정본·남은 의존 충돌을 처리했다.
- 변경한 책임의 직접 검사·필요한 회귀와 실제 host의 필수 수행 경로를 확인했다. 설정 존재·단위 검사·읽기 결과를 제품 사용·실제 자동 실행·사용자 수락과 혼동하지 않는다. 필수 미확인은 남은 작업으로 둔다.
- 실패 시 복구할 범위·판본, 현재 사용할 진입과 알려진 제약이 target의 작업 기록에서 발견된다. 실제 적용 결과의 정본은 Noline에 두고014는 선택·대조·공통 개선 근거를 연결한다.
- 필요한 개선 왕복에서 전달한 근거와 반영 결과를 찾을 수 있고, 수동 전달 대비 줄어든 재조사와 추가 판본 관리 부담을 비교할 수 있다. 일반 자동 동기화나 새 배포 도구를 필수로 만들지 않으며 관찰하지 않은 시간·토큰 절감을 주장하지 않는다.

현재 승인된 독립 묶음의 반영과 직접 확인을 마쳤다. 위 전환표의 비충돌 설치·교체·옛 실행 경로 정리를 마쳤다. 남은 것은02의 채택 계약에 따른 Work 기록 담당·생성/전환·Maintain/수집기 연결과 실제 host의 발견·호출·기록·재개 통합 확인,07의 사용 효과 관찰이다. 이번 Noline 실행 스킬 전환은 `41170efd`로 커밋했다. Reference와06 기록은 별도 커밋으로 보존한다. 앞선 context 부분 반영은 `2839d467`에 있다. 제품 acceptance·push·Workspace 완료는 수행하지 않았다.

[상위06](README.md) · [선행06-01](06-01-reference-project-application.md)
