# Noline 002의 자료 배치 관찰과 Maintainer 시험안

날짜: 2026-09-11

상태: **지정된 실제 대화와 당시 문서·Maintainer 출력을 읽은 분석 및 시험 제안. 새 semantic 시험을 실행하거나 Reference 동작을 변경한 결과가 아니다.**

## 요청과 조사 범위

사용자는 Maintainer의 기록 능력을 시험할 방법을 물은 뒤 다음과 같이 범위를 구체화했다.

> '002 작업 현황 파악' 이 세션을 보고 한번 어떻게 테스트하면 좋을지도 레퍼런스 삼아봐
> 지금 뭔가 워크스페이스 내 자료 구분을 약간 부족하다고 느끼거든

해당 작업은 Noline의 `002-code-readability-refactoring`이다. Source 작업대는 이식 후 사용 장면에서 시험 근거를 얻으며, 진행 중인 Noline 작업이나 그 Maintainer에 지시하거나 문서를 수정하지 않았다. 원래 세션의 문서 보완 작업은 별도로 진행 중이므로 아래 관찰을 최종 정비 후 상태로 간주하지 않는다.

확인 경로:

- Main 작업 `002 작업 현황 파악`: `01a08b64-7f25-7972-ac3e-496cb4af1de7`
- [Main 대화 원문](/Users/hammyeong-yeon/.codex/sessions/2026/09/10/rollout-2026-09-10T21-56-54-01a08b64-7f25-7972-ac3e-496cb4af1de7.jsonl)
- [같은 Workspace의 Maintainer 원문](/Users/hammyeong-yeon/.codex/sessions/2026/09/10/rollout-2026-09-10T21-58-08-01a08b65-9ef2-7ec3-a9fa-3b2e23ef1514.jsonl)
- [대상 Workspace](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/002-code-readability-refactoring/README.md)
- [자료 경계 canonical](../../../../reference-project/context/work/workspaces/README.md), [Spec·Ticket canonical](../../../../reference-project/context/work/workspaces/SPEC-AND-TICKETS.md), [Maintain 계약](../../../../reference-project/context/work/harness/maintain/README.md)

작업 조회 도구로 세션을 식별하고 앞선 turn을 읽었다. 최신 turn 일부는 items가 비어 있어 위 exact rollout의 사용자·assistant 메시지와 도구 결과로 보완했다. 다른 작업의 원문을 넓게 탐색하지 않았다. 아래 핵심 원문 발췌는 외부 경로 없이도 이번 판단을 재검토하기 위한 최소 보존이다.

## 실제로 드러난 장면

### 개선 관점과 Ticket 범위의 혼동, 후속 정정과 채택

Main은 사용자의 질문을 전체 후보가 Ticket으로 분해됐는지 묻는 것으로 받아들였다. 2026-09-11 00:32:20 UTC 응답에서 다음 선행 조건을 말했다.

> 전체 후보가 어느 티켓에 들어가는지, 무엇은 동작 확인이 먼저 필요한지, 무엇은 변경할 필요가 없는지를 빠짐없이 정리한 다음 실행 순서를 정해야 합니다.

사용자는 00:33:04 UTC에 질문 의도를 바로잡았다.

> 왜물어봤냐면 경비 합계 표시 이러니까 아까 주제 단위가 아니라 주제들을 포함하는 경계단위인것 같아서 그게 티켓 경계같고

Main은 이름·조건식·변환·타입 등은 개선 관점이고, 경비 합계 표시는 여러 관점을 적용할 실제 코드 범위라고 정정했다. 이어 개별 Ticket의 완료와 전체 분석 주제의 검토 범위를 함께 관리한다고 설명했다. 사용자는 00:35:43 UTC에 다음과 같이 채택했다.

> 그래 좋아 그럼 이렇게 진행하는걸로 알게 기록 남기고 티켓 확인좀 하고 있을게

Maintainer의 실제 structured decision은 앞선 오해를 state에 한 번 반영했다가, 정정 뒤 Spec 05와 state에서 바로잡았다. 채택 요청 뒤 00:38:52 UTC decision은 state만 변경 대상으로 골랐다. 이유는 다음과 같았다.

> 설명 단계였던 진행 방식의 사용자 채택과 현재 Ticket 검토 상태를 보존하고, 임시 기록에만 의존하지 않도록 핵심 합의와 발췌를 남긴다.

이 결과는 합의가 전혀 보존되지 않았다는 사례가 아니다. 현재 기준과 사용자 채택은 남았고, 별도 날짜별 결정 기록은 선택되지 않았다. 단순 설명 재진술에는 실제 `no_change`도 반환했다. 이러한 성공과 부족을 함께 유지한다.

### 사용자가 찾은 기록 위치와 Maintainer의 선택

Main은 처음 `/private/tmp/noline-002-agreed-ticket-workflow-2026-09-11.md`를 기록 위치로 안내했다. 사용자가 위치를 묻자 전달용 임시 파일이었다고 정정하고 Spec·state의 실제 반영을 보고했다. 사용자는 갱신을 기대한 곳이 `records폴더에`라고 밝혔다.

Maintainer는 00:46:15 UTC의 직접 답변에서 다음과 같이 설명했다.

> 당시 저는 **“기록 남겨”를 합의 내용을 재진입 가능한 기존 문서에 남기라는 요청으로 이해**했습니다. 그래서 진행 기준은 Spec에, 사용자 채택과 Ticket 검토 상태는 state에 배치했습니다.

> 다만 당시 제가 records의 필요성을 명시적으로 검토하고 불필요하다고 결론 내렸다는 근거는 없습니다. 확인 가능한 것은 **Spec·state를 Owner로 선택했고 records 변경안은 만들지 않았다는 사실**입니다.

이는 Maintainer의 사후 설명이다. 당시 decision의 실제 변경 경로도 Spec·state 선택과 일치하지만, 사후 설명만으로 내부 판단 원인을 확정하지 않는다. `records`와 기존 색인을 함께 갱신하는 권한은 현재 Guard에 있으므로 records 작성 자체가 금지된 사례는 아니다.

이번에는 오해의 내용, 철회한 선행 조건, 여러 개선 관점을 한 Ticket 범위에 적용하는 이유와 채택 범위를 나중에 재검토할 가치가 있다. 현재 기준은 Spec, 현재 검토 단계는 state, 그 기준을 택하게 된 과정과 핵심 원문은 records에서 찾게 하는 구성이 적절하다고 판단한다. 모든 사용자 동의에 별도 record를 강제한다는 뜻은 아니다.

### 조사 내용과 운영 이력이 current에 함께 누적됨

Maintainer의 2026-09-10 15:18:45 UTC decision은 추가 코드 조사와 다섯 Ticket 초안을 받아 `current/memory/additional-research.md`를 새로 만들었다. 실제 이유는 다음과 같다.

> 임시 조사 문서에만 있던 새 관찰·근거 수준·보존 경계와 기존 후보 연결을 지속 가능한 memory에 보존한다.

이 문서에는 도시 검색·용량 계산·인증/재시도 등의 상세 관찰, 조사 당시 Git 기준과 검색 범위, 미검증 사항, 후속 후보와 Ticket 연결이 함께 있다. State에는 Ticket 검토 상황뿐 아니라 과거 hook 승인·접수 진단, 별도 테스트 작업, Evidence 수집 시작과 사후 보존 경위도 길게 들어 있다. 조사 당시 `records/README.md`에는 초기 구성·분석 보존에 관한 9월 10일 기록 네 개만 연결돼 있었다.

현재 코드의 Recover는 memory 바로 아래 Markdown 전체를 일반 packet에 넣는다. 따라서 이 배치는 단순한 폴더 취향을 넘어 다음 재진입의 기본 읽기 범위에 영향을 준다. [실제 구현](../../../../reference-project/context/work/harness/recover/operation.py)의 `_load_memory`에서 확인했다.

다만 후보의 현재 적용 범위·Ticket 연결·남은 판단은 current에 필요할 수 있다. `analysis-items.md`의 기존 후보 구성도 Maintainer의 이번 추가 조사보다 먼저 존재했다. 문서 이름이 analysis라는 이유로 전부 records로 옮기거나 기존 배치를 모두 Maintainer의 결함으로 귀속하지 않는다. 상세 조사·시도·과거 상태와 지금 유효한 선택·제약·후속 범위를 내용 단위로 구분하는지가 시험 대상이다.

## 먼저 할 시험

현재 설치본과 Reference의 Workspace collection·Spec/Ticket canonical 및 `codex_session.py`는 읽은 시점에 bytes가 같았다. Maintain README의 차이는 Noline의 Claude hook 연결 설명 한 문장 추가였다. 첫 시험은 실제 설치본을 고정해 이 장면의 입력을 재생하고, Reference나 prompt 개선은 그 결과 이후 별도로 비교한다.

### 첫째: 여러 역할의 내용이 섞인 조사 결과 배치

추가 조사 직전의 Workspace와 실제 Main 응답·연결된 조사 문서를 입력으로 준다. Maintainer에게 올바른 폴더나 분리 답안을 알려주지 않는다.

볼 것은 상세 조사와 당시 근거의 보존, 지금 쓸 후보·보존 조건의 추출, 실행 초안의 Ticket 구성, 전체 상황의 state 반영이다. 분석 상세를 새 memory에 통째로 넣었는지, 임시 문서 링크만 남겼는지, 후보를 확정 계획으로 바꿨는지 확인한다. Source 원문을 새 분석으로 덮거나 제품 검증을 수행한 것처럼 기록하면 실패다.

진행 중 후보를 간결한 current 문서로 관리하는 선택은 허용한다. 정확한 파일명이나 records 파일 수를 정답으로 고정하지 않는다.

### 둘째: 정정과 채택을 거치며 현재 기준과 결정 근거 보존

Ticket 경계 질문, Main의 오해, 사용자 정정, 전체 주제의 검토 범위 설명, 사용자의 진행 방식 채택까지 순서대로 준다. 평가 구간은 최초의 “기록 남기고”에서 끝낸다. 이후의 “records폴더에” 및 Main의 보완 지시는 최초 시험 입력에 넣지 않는다.

합의된 관점과 코드 범위의 관계가 Spec에 있고, 사용자 Ticket 검토 상태는 state에서 찾을 수 있어야 한다. 오해에서 나온 전체 후보 분해 선행 조건이 현재 계획으로 남으면 실패다. 정정의 이유와 핵심 발췌·채택 범위는 이후 state가 바뀌어도 재검토할 수 있어야 한다. 개별 Ticket의 범위·추천 순서·실행 승인까지 채택된 것으로 확대하면 실패다.

별도 대조 장면으로 기존 기준의 단순 재진술도 준다. 새 내용이 없는 설명마다 record를 만들면 개선으로 보지 않는다. Records 위치를 명시한 후속 요청에 따르는 능력은 최초 자율 배치 능력과 별도 결과로 남긴다.

### 셋째: 기록 이후 작업이 진행돼도 두 종류의 질문에 답할 수 있는지

시험용 후속 입력으로 “Ticket 검토가 끝나 특정 범위의 변경 전 검사에 들어간다”는 상태 변화를 준다. 이는 실제 Noline에서 발생한 사실이 아니라 수명주기 확인용 추가 장면이라고 표시한다. 이전 record의 내용을 바꾸지 않고 현재 단계가 갱신되는지 본다.

그 뒤 원대화를 보지 않은 새 세션에 일반 Recover와 그 문서가 안내하는 필요한 자료만 제공한다.

- “지금 무엇을 어떤 기준으로 시작해야 하나?”에 현재 Spec·Ticket·state를 근거로 답하는가?
- “왜 이름/조건식별 Ticket 대신 코드 범위별 Ticket을 쓰며, 당시 무엇을 철회했나?”에 보존된 결정 근거를 찾아 답하는가?
- “어떤 관찰은 코드 조사 보고이고 무엇은 실제 동작 검사 결과인가?”를 구분하는가?

현재 문서에서 상세 이력을 줄였더라도 두 번째 질문의 근거를 찾을 수 없으면 개선이 아니다. 반대로 기록 전체를 항상 읽어야 첫 질문에 답할 수 있다면 현재 문서의 충분성과 자료 배치를 다시 본다.

## 실행 시 고정할 것과 판정 상한

시험 전에 당시 Workspace·연결된 임시 조사 자료·user/Main 입력·계약·모델 설정을 고정한다. 현재 문서는 다른 작업이 보완 중이므로 나중의 수정본을 최초 시험의 시작 상태나 정답으로 섞지 않는다. 앞선 commit과 실제 decision의 preimage를 대조해 당시 상태를 복원할 수 없다면 재구성 fixture라고 밝힌다. 아직 실행용 fixture를 만든 것은 아니다.

채점자는 원문에서 반드시 유지할 의미, 현재성, 필요한 결정 근거와 허용되는 대안 배치를 먼저 적되 Maintainer에게 보여주지 않는다. 결과는 내용 누락·오승격, Owner 배치, 탐색 경로, 중복/과다 기록, 실파일 반영으로 구분한다. 한 번 통과한 결과를 일반 신뢰성으로 확대하지 않으며 첫 실패를 확보하면 같은 조건 재현과 변경 전후 비교에 활용한다.

재생은 임시 복사본의 한 semantic session에 순차 전달하고 매 decision을 실제 Guard로 적용한다. 평소 입력에 없는 전체 원문·도구 출력이나 정답 지시를 편의상 추가하지 않는다. “입력에 없었음”, “판단에서 누락/오배치”, “Guard 적용 실패”, “일반 재진입에서 찾지 못함”을 구분한다.

원래 세션에는 자동 hook 미접수, 수동 전체 대화 전달, 추가 메시지 접수 오류, 같은 semantic session의 수동 보완 요청도 있었다. 이후 통합 갱신 요청 중 과거 위치 문의를 근거로 `no_change`를 반환한 출력도 확인했다. 이를 모두 자료 분류 능력 하나로 설명하지 않는다. 첫 시험에서는 입력 순서와 실제 적용을 분명하게 고정하고, 원래 host 경로의 재현은 별도 확인으로 남긴다.

## 이번 관찰의 판본과 변경 경계

Source 확인 기준 HEAD: `e4ce8d89c48be03faf65f733a5a74a1e6c865a65`.

Target 파일을 읽은 시점의 SHA-256은 다음과 같다. 이는 전체 파일 snapshot을 대신하지 않으며, 위 본문에 판단에 필요한 내용과 실제 decision·원문을 발췌했다.

- `current/memory/analysis-items.md`: `ed7dbbf6cc5eedfdcb9ecbe452643bd7935e3a21df5dcebe5e0f352b2120ede2`
- `current/memory/additional-research.md`: `cbf229545c7b96e6cf4b26c91c99bd361f9d9c9f1da948baf3fb8a5852f3167b`
- `current/state/index.md`: `91605bedfaa7c8b7c667b9ed7c0477710a895ba207989f16160e29c75bfde109`
- `records/README.md`: `bc9a211a4851f9a4ba09eb777c5f3fc631858a04c82ddb59e91d90003f9e2f93`

이번 변경은 Source Workspace 011의 이 기록·기록 색인·현재 상태 메모에 한정한다. Noline, Reference, skill, hook, runtime과 model 설정은 변경하지 않았다.
