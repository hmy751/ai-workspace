# 07 TripProof spec-driven continuity

이 폴더는 `07-tripproof-spec-driven-continuity` source에서 이어지는 후속 분석과 해결안 초안을 둔다.

원래 단일 분석 문서였던 본문은 [`01-problem-analysis.md`](01-problem-analysis.md)로 분리했다. 이 `README.md`는 폴더 진입점, 문서가 만들어진 순서와 현재 지위를 소유한다.

파일명의 번호는 중요도나 최종 정답의 우선순위가 아니라 **작업과 판단이 전개된 순서**다. 이후 문서가 앞선 문서를 자동으로 대체한다는 뜻도 아니다.

**Spec·Ticket의 현재 통합 결과부터 이어가려면 [`07-context-harness-spec-ticket-integration.md`](07-context-harness-spec-ticket-integration.md)를 먼저 읽는다.** 2026-09-08 Context Harness Reference에서 채택·구현한 구조와 기존 02·06에서 바뀐 선택, 유지한 문제의식과 검증 한계를 정리했다. 이 연구 저장소와 실제 TripProof에 이식한 상태는 아니다.

네 공동 스킬과 이 구조를 연결한 후속 결과는 [`08-skills-spec-ticket-integration/`](08-skills-spec-ticket-integration/README.md)에 있다. Spec 작성 판단과 Main·Maintain·서브 결과 전달의 논의 결정, 이를 반영한 미설치 스킬 준비본 v0와 검토 기록을 함께 둔다.

**평가 준비는 [09 개선안 평가 디렉토리](09-improvement-evaluation/README.md)에서 이어간다.** 대화에서 정리한 [전체 구조](09-improvement-evaluation/01-evaluation-structure.md)와 [상세 평가 방법](09-improvement-evaluation/02-evaluation-method.md)을 먼저 읽는다. 외부 자료 분석·실제 평가와 사용 예·문제 및 개입 근거도 현재 본문으로 나눴다. 기존 09~13의 전체 분석·초안·리뷰 판본은 그 안의 [archive](09-improvement-evaluation/archive/README.md)에, 작업·정리 이력은 [Workspace records](../../../workspaces/013-tripproof-pre-application-evaluation/records/README.md)에 보존했다. 평가 대상은 문제 분석을 바탕으로 개선한 스킬·레퍼런스·작업 구성이며, 여러 프로젝트와 작업에 적용할 방법을 준비한다. 현재는 [06 성과별 평가안](09-improvement-evaluation/06-outcomes-and-evaluation-plan.md)에 확인할 성과, 판정 기준·근거, 업무 의미·개발자의 기여를 연결해 제안했다. 작성·검토·보완을 거쳤으며 제안의 수용과 실제 적용 조건 선택이 남아 있다.

## 현재 문서

- [`01-problem-analysis.md`](01-problem-analysis.md): 07이 말하는 문제, `05-tripproof-harness-retro`가 보조하는 운영 공백, 다음 해결책에서 확인해야 할 질문을 정리한 본문
- [`02-workspace-based-continuity-direction.md`](02-workspace-based-continuity-direction.md): 독립된 spec을 기본으로 유지하지 않기로 했던 Workspace의 초기 채택 방향. current·records·Project context의 책임과 수명에 관한 근거이며, Reference에서 달라진 작업 정의·기본 읽기 범위는 07에서 확인한다.
- [`03-project-context-foundation-direction.md`](03-project-context-foundation-direction.md): Project 내부의 공통 맥락·현재 상태·조건부 지침 책임, Decision의 제한된 역할과 Project 계약을 따르는 얇은 관리 skill 방향
- [`04-conversation-scene-analysis.md`](04-conversation-scene-analysis.md): Guidance 해결을 구체화하던 중 기존 진단만으로는 부족하다는 사용자 정정에 따라, 인터뷰와 세 개의 실제 TripProof 대화 장면으로 01의 남은 판단 연속성 문제를 다시 구체화한 보충 분석. 세 장면은 해결 과제나 해결 범위를 대신하지 않는다.
- [`05-judgment-continuity-solution-direction/`](05-judgment-continuity-solution-direction/README.md): 기존 분석·설계·v0를 archive에 보존하고 V1·V2와 Matt에서 이어갈 결과를 선별해 새 본문으로 구성한 판단 연속성 설계 작업. 출발 문서는 원래 문제와 이 결과를 연결한다. 현재 입력은 해당 README가 안내하며 과거 문서 전체를 필수 읽기로 상속하지 않는다.
- [`06-judgment-and-understanding-application/`](06-judgment-and-understanding-application/README.md): 판단 연속성과 이해 지원의 공동 적용 판단 기록, 제3 리뷰와 최소 일반화한 네 스킬의 배포 준비본. 적용 프로젝트는 미정이고 실제 설치는 하지 않았다.
- [`06-work-first-spec-ticket-tradeoff-analysis.md`](06-work-first-spec-ticket-tradeoff-analysis.md): Work-first와 Spec/Ticket-first의 최적화 대상, 실제 중복과 고유 책임, 장단점·적용 조건·비용·검증 상한을 정리한 후속 비교 분석
- [`07-context-harness-spec-ticket-integration.md`](07-context-harness-spec-ticket-integration.md): Context Harness Reference에 채택·구현된 Spec·Ticket과 current의 관계, 읽기·갱신 방식, 이전 연구와의 차이, 실제 검증과 미적용 범위를 정리한 후속 분석
- [`08-skills-spec-ticket-integration/`](08-skills-spec-ticket-integration/README.md): Workspace 012에서 합의한 네 스킬과 Spec·Ticket 연결의 논의 결정과 수정 준비본 v0. 적극적인 Spec 구체화, Main·Maintain의 관계를 반영했으며 실제 설치·운영 효과는 미확인
- [`09-improvement-evaluation/`](09-improvement-evaluation/README.md): 개선안 평가의 전체 구조와 상세 방법, 외부 자료 분석, 실제 평가·사용 예, 문제·개입 근거. 당시 09~13 연구 판본은 archive에, 작업·정리 이력은 Workspace records에 보존했다.

앞으로 07에서 파생되는 분석, 해결안 초안, 적용 검토 문서는 이 폴더에 둔다.

## 작업 전개와 읽는 순서

1. 이 `README.md`에서 폴더 지위와 현재 본문을 확인한다.
2. [`01-problem-analysis.md`](01-problem-analysis.md)에서 문제 진단과 설계 질문을 읽는다.
3. [`02-workspace-based-continuity-direction.md`](02-workspace-based-continuity-direction.md)에서 먼저 채택한 Workspace의 해결 범위와 후속 책임을 읽는다.
4. [`03-project-context-foundation-direction.md`](03-project-context-foundation-direction.md)에서 그 다음 채택한 Project context의 최소 책임과 관리 skill 경계를 읽는다.
5. [`04-conversation-scene-analysis.md`](04-conversation-scene-analysis.md)에서 두 기반을 마련한 뒤 해결을 논의하다가 실제 장면으로 되돌아가 구체화한 판단 연속성 문제를 읽는다.
6. [`05 판단 연속성 설계의 새 출발`](05-judgment-continuity-solution-direction/README.md)에서 현재 출발 문서와 다음 판단을 확인한다. 과거 설계의 도출 이유가 필요한 경우에만 archive로 내려간다.
7. 이전 비교의 선택 이유와 비용은 [`06-work-first-spec-ticket-tradeoff-analysis.md`](06-work-first-spec-ticket-tradeoff-analysis.md)에서 읽는다. 당시 Work-first 기본값이나 Matt의 특정 운영 규율을 새 Reference의 필수 규칙으로 적용하지 않는다.
8. [`07-context-harness-spec-ticket-integration.md`](07-context-harness-spec-ticket-integration.md)에서 Reference의 채택·구현 결과와 연구 후속 기준을 확인한다. 현재 통합 작업을 이어갈 때는 이 문서부터 시작하고 필요한 앞 문서만 선택해 읽는다.
9. 필요할 때만 source 원문이나 07이 연결한 context-harness의 정확한 근거를 다시 연다.

Spec·Ticket과 연결한 네 스킬을 이어가려면 [08의 통합 준비본](08-skills-spec-ticket-integration/README.md)에서 시작한다. 그 입력인 [06의 공동 적용 준비본](06-judgment-and-understanding-application/README.md)은 최소 일반화한 당시 판본을 보존한다. 각 사본의 적용 전제와 미설치 상태를 함께 확인한다.

`04`는 `03`에서 곧바로 파생된 별도 기반 설계가 아니다. 제품·코드 판단 연속성의 해결을 논의하던 중 문제 이해가 여전히 추상적이라는 점이 드러나, 해결안을 확정하기 전에 실제 작업 장면으로 돌아가 만든 보충 분석이다. 이후 05에서 방향 재설정·V1·V2와 Matt 비교·구체 설계·v0 보완이 이어졌다. 2026-09-06에는 그 결과의 이해와 누적 복잡성을 다시 판단하기 위해 05의 기존 묶음 전체를 [archive](05-judgment-continuity-solution-direction/archive/README.md)에 보존하고 새 설계를 시작했다. 과거 선택의 상세 전개는 archive와 원래 records가 소유한다.

## 근거 위치

- [`../../source/07-tripproof-spec-driven-continuity/source.md`](../../source/07-tripproof-spec-driven-continuity/source.md): 07 source의 지위와 원문 목록
- [`../../source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-conceptual.md`](../../source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-conceptual.md): 제품, 코드, spec, 평가, context 관점의 주 원문
- [`../../source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-chronological.md`](../../source/07-tripproof-spec-driven-continuity/original/spec-driven-retro-chronological.md): 논의 전개 순서 보존본
- [`../../source/05-tripproof-harness-retro/source.md`](../../source/05-tripproof-harness-retro/source.md): 07이 후속 설명 가설로 삼은 prior-work 근거층

## 현재 지위

`07-context-harness-spec-ticket-integration.md`는 Reference 구현 `dcd3c6f`와 전달문 `9505bf3`를 기준으로 채택 결과·기존 분석과의 차이·후속 적용 지점을 소유한다. 아래 이전 문서들의 문제·근거·당시 선택을 통째로 대체하지 않는다. 특히 02의 Spec 배제 기본값과 06의 조건부 도입 관계는 이번 Reference에서 변경됐고, 판단 연속성의 실제 효과와 대상 프로젝트 이식은 여전히 별도 확인 사항이다.

`01-problem-analysis.md`는 문제 진단과 다음 해결 논의의 범위를 소유하며 해결책 채택안은 아니다. `02-workspace-based-continuity-direction.md`는 그 질문 가운데 Workspace가 맡을 구조적 해결 범위에 대해 채택한 방향이다. `03-project-context-foundation-direction.md`는 그 위에서 Project context의 최소 책임과 관리 skill의 비소유 경계를 채택한 후속 방향이다. `04-conversation-scene-analysis.md`는 두 기반 이후에도 남은 01의 문제를 사용자 인터뷰와 실제 대화 장면으로 구체화한 보충 분석이다. `05-judgment-continuity-solution-direction/`은 새 설계의 출발점과 과거 분석·설계를 구분해 소유한다. Archive 이동과 출발 문서 작성은 새 설계의 채택·적용·효과 또는 사람 acceptance를 뜻하지 않는다. `06-work-first-spec-ticket-tradeoff-analysis.md`는 Work와 Spec/Ticket의 비교 기준과 설계 가설을 소유하지만, 어느 방식의 일반적 우월성이나 실제 TripProof 적용 효과를 주장하지 않는다.
