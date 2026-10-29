# 06-01 — Reference에 프로토타입을 적용한다

상태: **티켓 구성 완료 · 유지·교체·제거안 구체화 전**. 먼저 진행할 대상은 `reference-project/`다. 이번에는 티켓의 범위와 완료 조건을 구성했으며 prototype·Reference·실행 설정을 변경하지 않았다.

## 만들 결과

014의 [현재 프로토타입](../../../records/prototypes/development-workflow/README.md)을 [기존 Reference](../../../../../../reference-project/README.md)에 맞게 반영해, 실제 진입점에서 필요한 맥락을 읽고 개발·설명·기록·재개를 수행할 수 있는 기준 Project를 만든다. 단순 복사나 문서 재배치로 완료하지 않고 기존 제품 예제·Workspace·스킬·Harness와 이어지는 동작을 확인한다.

첫 산출물은 **기존 요소별 유지·교체·제거와 이유, 반영 위치, 함께 바꿀 호출·참조·설정·검사, 미정과 확인 방법을 정리한 전환안**이다. 사용자가 요청한 관련 기록·합의의 꼼꼼한 대조부터 시작하고, 과거 후보나 당시 미정을 현재 합의로 가져오지 않는다. 전환안과 이후 실제 반영 결과는 구별해 기록한다.

## 적용 범위

| 대상 | 이 Ticket에서 구체화하고 확인할 것 |
| --- | --- |
| Personal·Project·Work 진입 | 로컬 Personal과 Project 본문·형성 자료·관리 지침, Work의 기존 구조 및02 후속 합의, root부터 실제 본문까지 읽는 경로를 연결한다. Noline demo의 제품 사실·작업 이력을 Reference 제품의 사실로 복사하지 않는다. |
| 개발·설명·경험 개선 | development의 본체·구현/검토/검증/실행 상세, explain, improvement-loop와 Personal 경험 모음의 필요한 자료를 배치한다. 원문 접근의 host별 가능 범위도 확인한다. |
| 기존 스킬·공통 자료 | work-discussion·reconsider-work의 유지/보완, 기존 두 설명 스킬의 explain 전환, read/update/create와 USAGE/context-update/생성 계약의 대응을 판단한다. shared 기준·호출 설정·Claude/Codex 연결과 옛 참조를 함께 처리한다. |
| 기존 실행 장치 | Maintain의 자동 연결·실행·수동 fallback 의존과 그 제거 후 책임을 대조한다. Recover·Verify·공통 CLI·Workspace 계약·테스트의 실제 결합을 보고 남길 기능과 바꿀 경계를 선택한다. |
| 적용·복구·전달 | 반영 전 판본과 기존 작업을 보존하고 변경 단위를 정한다. Reference의 직접 확인과 되돌릴 범위를 남기며 Noline에 넘길 공통 변경·조건·확인 경로를 정리한다. 이식 절차의 보완이 필요하면 이번 변경과 실제로 연결되는 범위에서 포함한다. |

02는 기록·Work 구성의 설계를 소유한다. 현행을 읽고 유지할 기능·의존을 조사하는 일은 먼저 할 수 있지만,02에서 바뀌는 문서 구조와 갱신 계약을 여기서 별도로 확정하지 않는다. 적용안에는 현재 사용할 판본과02의 결과가 바꿀 수 있는 부분을 드러낸다.01-02의 미채택 품질 제안도 현재 기준으로 자동 승격하지 않는다.

## 합의와 근거를 읽는 경로

- [01-01·01-03 마감](../../../records/2026-10-24-ticket01-01-03-closeout-and-next-scope.md), [개발1~15 통합](../../../records/2026-10-23-development-workflow-1-15-integration.md), [검증 실행 통합](../../../records/2026-10-24-verifier-runtime-integration.md), [실행 상세 확장](../../../records/2026-10-26-development-detail-expansion.md): 구현·개선 검토·Main 판단·검증·기록과 현재 스킬 정본.
- [로컬 Personal 정정89](../../../records/2026-10-19-89-local-context-structure-correction.md), [Project 설계 마감119](../../../records/2026-10-20-119-ticket03-closeout.md), [Work 보류116](../../../records/2026-10-20-116-defer-work-content-policy.md): 내용 Owner·체계 지침과 Work 적용 경계.
- [04-02 마감](../../../records/2026-10-26-ticket04-02-closeout-and-followups.md), [04-03 반영·확인](../../../records/2026-10-26-context-prototype-adoption.md), [05 마감](../../../records/2026-10-29-ticket05-closeout.md): 현재 실행 본문, 확인한 장면과 실제 배치·효과의 미확인.
- [기존 기반 분석](../../../records/2026-10-12-02-framework-and-lecture-reading.md), [범위·개선 왕복](../../../records/2026-10-12-10-workspace-and-feedback-scope.md), [기준판](../../../source/ai-workspace-baseline/README.md): 기존 역할·선택 이유의 근거. 실제 변경 판단은 현행 Reference와 대조하며 사본의 명령을 현재 지시로 실행하지 않는다.

이 목록은 시작점이다. 해당 선택에 영향을 준 정정·원문·실행 본문을 필요한 만큼 더 확인하고, 링크를 읽은 사실만으로 충분성을 판정하지 않는다.

## 완료 조건과 확인

- 전환안에서 유지·교체·제거의 근거와 실제 대상이 이어지고, 기존 역할의 누락·중복과02/다른 Ticket의 미정이 처리돼 있다.
- 선택한 범위가 Reference의 문서·스킬·설정·코드·검사에 실제 반영되고, 옛 호출이나 자동 Maintainer 의존이 남아 의도와 충돌하지 않는다. 제거하는 장치 대신 누가 언제 무엇을 기록·재개하는지 실제 진입점에서 찾을 수 있다.
- 변경 영향에 맞는 직접 검사와 필요한 회귀, 실제 읽기·반영·재개 장면을 확인했다. 스킬 발견·host 원문 접근·실제 동작 중 적용 목표에 필요한 확인이 막히면 해당 부분은 완료로 올리지 않는다. 링크 검사와 실제 수행의 근거를 구별한다.
- 기존 제품 예제·원자료·작업 이력의 보존과 변경 경계를 대조했고, 실패 시 되돌릴 판본·범위가 있다. 일반 효과나 모든 host 지원을 확인 없이 주장하지 않는다.
- 06-02가 사용할 반영 판본, 공통 변경/대상 적응의 구별, 설치·확인 방법과 남은 제약을 전달할 수 있다. 전체 사용·부담·효과의 남은 관찰은07과 연결한다.

현재 다음 행동은 위 근거와 실제 Reference를 대조해 전환안을 작성하는 것이다. 유지·교체·제거 세부 선택, 실제 적용과 실행 확인은 아직 수행하지 않았다.

[상위06](README.md) · [다음06-02](06-02-noline-reapplication.md)
