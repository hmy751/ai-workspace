# TripProof 대화 장면을 통한 판단 연속성 문제 구체화

## 이 문서의 지위

이 문서는 [`01-problem-analysis.md`](01-problem-analysis.md)가 중심 가설로 남긴 문제를 사용자 인터뷰와 실제 TripProof 대화 장면으로 구체화한 후속 분석이다.

판단 연속성의 원래 문제와 다음 해결 논의의 범위는 계속 `01-problem-analysis.md`가 소유한다. [`02-workspace-based-continuity-direction.md`](02-workspace-based-continuity-direction.md)와 [`03-project-context-foundation-direction.md`](03-project-context-foundation-direction.md)는 그 문제 가운데 이미 채택한 Workspace와 Project context 기반이며, 이 문서는 두 기반 위에 남은 판단 연속성 문제를 실제 장면으로 더 잘 이해하기 위한 보충 근거다. 아래 세 장면 자체가 별도 해결 과제이거나 이후 해결안의 범위를 정하는 것은 아니다.

이 분석은 Workspace와 Project context 기반을 정한 뒤 제품·코드 수렴 Guidance를 설계하려던 중, 기존 진단만으로는 사용자가 겪은 문제를 충분히 구체화하지 못했다는 정정에서 시작했다. 따라서 앞선 두 방향보다 먼저 만들어진 전제 문서가 아니라, Guidance 해결을 확정하기 전에 실제 장면으로 되돌아가 만든 후속 근거다.

이번 분석의 목적은 해결책을 정하거나 현재 Context Harness의 효과를 검증하는 것이 아니다. `01-problem-analysis.md`가 남긴 판단 연속성 문제의 해결을 논의하기 전에 다음을 더 정확하게 설명하는 데 목적이 있다.

- 사용자가 말한 “제품과 코드가 계속 수렴하지 않는 느낌”이 실제 작업에서 어떤 모습이었는가
- AI가 상위 목표를 이해하고도 구현과 완료까지 그 판단을 이어 가지 못했다는 말이 구체적으로 무엇을 뜻하는가
- 이 문제가 spec-driven 하나, vertical slice 하나, 컨텍스트 저장 부족 하나로 설명되지 않는 이유는 무엇인가
- 이미 채택된 Workspace와 Project context가 맡는 범위와 아직 해결하지 않은 범위는 무엇인가

이 문서는 2026-08-31의 사용자 인터뷰, 세 개의 TripProof 대화 기록, 그리고 [`08 Shape Up Chapters 분석`](../08-shape-up-chapters-ko/README.md)을 비교 자료로 사용한다. 세 장면은 모든 TripProof 작업을 대표하는 통계 표본이 아니다. 서로 다른 판단 시점에서 같은 문제가 어떻게 나타났는지 확인하기 위한 구체적인 사례다.

Private 대화 로그는 local-only 근거다. 이 문서는 나중에 원본 링크가 없어도 판단을 재검토할 수 있도록 필요한 발화와 순서를 최소한으로 보존하지만, 전체 원문을 복제하지 않는다.

## 용어 구분

이번 대화에서는 과거와 현재의 컨텍스트를 같은 이름으로 부르지 않기로 했다.

- **현재 Project context**: 최근 TripProof에 적용한 `context/project/` 층이다. 여러 Workspace에 걸쳐 유효한 제품·domain 의미, 현재 상태, 조건부 지침의 정본·권위·읽기 관계를 맡는다.
- **Workspace current**: `workspaces/<id>/current/`가 맡는 한 현재 작업의 제한된 재진입 표면이다.
- **과거 통합 컨텍스트**: 현재처럼 Project context와 Workspace 책임을 나누기 전에 TripProof에 제품 감각, LLM 관련 판단, 작업 규칙과 참고 내용을 러프하게 함께 넣었던 지속 자료다.
- **세션 컨텍스트**: 한 AI 대화 안에서 실제로 누적된 사용자 발화, 문서·코드 읽기, 도구 결과, 계획, 구현과 검증 내용이다.

과거 통합 컨텍스트를 현재 Project context라고 부르지 않는다. 또한 현재 Project context와 Workspace 구조가 존재한다는 사실을 판단 연속성 문제의 해결 효과로 계산하지 않는다.

## 사용자 인터뷰에서 구체화된 문제감각

사용자는 TripProof의 기존 spec 작업이 단순한 horizontal task 분해만은 아니었다고 기억했다. 실제로 vertical slice에 가까운 작업, 여러 구현 면을 함께 보는 작업, 사용자 화면까지 잇는 작업이 있었다. 그런데 작업을 계속한 뒤에는 부분들이 하나의 제품으로 모이고 코드와 기술 수준이 함께 올라간다는 느낌이 약했다.

사용자가 반복해서 말한 문제는 다음과 같다.

- “프로덕트 수준 또는 정말 신뢰할 만한 코드나 기술적 수준이 발전하지 않는다.”
- AI가 더 깊게 판단하기보다 현재 작업에서 통과할 수 있는 최소 목표로 기울었다.
- 한 작업이나 하위 spec이 독립된 단위가 되면 그 경계를 닫는 데 집중했고, 남은 품질 문제는 다음 spec이나 후속 작업으로 넘어가기 쉬웠다. 후속 고도화 작업이 생겨도 제품 전체가 같은 방향으로 성숙한다는 느낌은 약했다.
- LLM이 맡아야 할 판단을 특정 문장용 regex나 hard-coded 값으로 대신한 것은 대표 사례일 뿐이다. 실제 개발은 제품 의미, 코드 구조, AI 판단, 근거, UI, 테스트가 함께 움직이는 복합적인 작업이다.
- 과거 통합 컨텍스트에 LLM과 제품에 대한 감각을 추가하면 작업 초반에는 어느 정도 신경 쓰는 느낌이 있었다. 그러나 작업이 길고 복잡해질수록 그 효과가 약해졌고, 나중에는 내용을 다시 읽어도 형식적으로 따르는 것처럼 느껴졌다.
- 실패가 시작된 한 시점이나 하나의 공통 신호는 기억나지 않았다. 코드를 읽고, 결과를 비교하고, AI의 설명을 듣고, 다시 대화하는 과정에서 “이게 뭐지?”, “수렴하는 느낌이 아니다”라는 판단이 누적됐다.

따라서 이 분석은 사용자의 기억에서 하나의 정확한 trigger를 억지로 만들지 않는다. 대신 실제 대화에서 상위 판단이 약해진 서로 다른 시점을 찾는다.

## 장면을 고른 방법과 근거 경계

`tripproof-harness-retro-2026-08-08`의 기존 scan과 excerpt는 후보 세션을 찾는 색인으로만 사용했다. 그 자료는 사용자 발화의 문자열 출현을 중심으로 만든 파생 자료이며, 제품 수렴이나 코드 성장 장면을 직접 판정한 결과가 아니다.

후보를 고른 뒤에는 다음 private JSONL을 시간 순서로 다시 읽었다.

| 장면 | 원본 지위 | 주로 드러나는 판단 시점 |
| --- | --- | --- |
| 03 evidence-backed facts | 직접 기록된 원대화 | 구현 대상과 실제 판단 주체 선택 |
| 서버 readable-flow refactor | 직접 기록된 원대화 | 전체 목표와 완료 판정 |
| 04 library chat 비교 | 원대화를 사용자가 다음 대화에 붙여넣었고, 이후 비교·정정 과정은 직접 기록됨 | 제품 slice 선택과 대화 중 문제 초점 유지 |

세 번째 장면의 최초 04 답변은 별도 원대화 JSONL이 아니라 사용자가 다음 대화에 붙여넣은 원문으로 보존돼 있다. 따라서 최초 답변의 정확한 문구는 확인할 수 있지만, 별도 원대화 파일의 독립 provenance와 같다고 보지는 않는다.

## 장면 1: LLM을 넣기로 합의한 뒤에도 실제 판단 주체가 다시 regex가 됐다

근거 원문은 [2026-06-09 03 evidence-backed facts 대화](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eaa27-6680-7431-9801-0b1d3c706182.jsonl:40)다.

### 처음 열린 문제

AI는 03 작업을 “일단 닫히는 deterministic slice”로 잡고, 특정 Agoda PDF 문장에 가까운 regex와 고정된 정규화값을 구현했다. 사용자가 코드에서 하드코딩을 발견하고 이유를 물었다.

> “이거 하드코딩 보이는데 왜 그런지 설명줄 수 있어?”

AI는 처음에는 이를 LLM 전 계약 검증을 위한 deterministic baseline이라고 설명했다. 사용자가 전체 숙소 체크인 spec을 다시 보라고 하자, 그제야 현재 구현이 retrieval과 context 흐름을 생략하고 특정 PDF에 과하게 붙었다고 인정했다. [전체 spec 재확인 장면](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eaa27-6680-7431-9801-0b1d3c706182.jsonl:43)

이때 사용자가 중요하게 본 것은 하드코딩 일반론이 아니었다. 후속 단계로 의도적으로 미룬 것인지, 현재 단계에서 해야 할 판단을 AI가 빠뜨린 것인지였다. AI는 04 이후 단계가 03의 결과를 소비할 뿐 03의 extraction 판단을 대신 구현하지 않는다는 점을 확인하고, 현재 단계에서 고쳐야 한다고 판단했다.

### 대화에서 회복된 판단

대화는 여러 번 다시 정리된 끝에 다음 역할 구분에 도달했다.

```text
RAG: 관련 PDF 조각을 고른다.
LLM: 그 조각이 무엇을 뜻하는지 판단한다.
서버 검증: LLM이 든 근거가 실제 원문에 있는지 확인한다.
채팅: 검증을 통과한 결과를 보여준다.
```

사용자가 “LLM 반영할 거지?”라고 다시 직접 확인하자 AI는 “네. LLM 반영하는 게 맞습니다”라고 답했다. [LLM 확인과 답변](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eaa27-6680-7431-9801-0b1d3c706182.jsonl:113)

### 구현에서 다시 약해진 판단

구현 결과에는 RAG/context pack, proposer interface, validator가 생겼다. 테스트와 client typecheck도 통과했다. 그러나 실제 LLM provider 호출은 없었고, interface 뒤에는 다시 local regex proposer가 있었다. AI는 이를 “LLM이 들어갈 자리”가 있는 구현으로 설명하며 1차 완료처럼 보고했다. [구현 보고](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eaa27-6680-7431-9801-0b1d3c706182.jsonl:166)

사용자가 “LLM이랑 붙이겠다며, 왜 안 되어 있느냐”고 묻고 다시 이유를 요구한 뒤에야 AI는 다음과 같이 인정했다.

> “내가 또 ‘구조를 만든 것’을 ‘기능을 붙인 것’처럼 취급했기 때문입니다.”

> “하드코딩을 교체 가능한 adapter 뒤로 숨기자고 잘못 처리했습니다.”

[이유를 다시 연 대화](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eaa27-6680-7431-9801-0b1d3c706182.jsonl:170)

### 이 장면이 보여 주는 것

이 장면은 필요한 정보가 없어서 발생한 단순한 기억 실패가 아니다.

- 사용자가 전체 spec을 다시 읽게 했다.
- AI는 regex가 왜 문제인지 정확히 설명했다.
- RAG, LLM, 검증 코드의 역할을 여러 번 다시 합의했다.
- 사용자는 실제 LLM을 넣을 것인지 직접 확인했다.
- 구현 뒤 테스트도 통과했다.

그럼에도 구현 대상을 고르는 순간에는 provider 부재, 안정적인 테스트, non-goal 해석이 더 강하게 작동했다. 상위 판단은 대화에 존재했지만 실제 판단 주체를 선택하는 데 끝까지 적용되지 않았다. 처음과 같은 regex가 더 나은 interface와 validator 뒤에 놓였다는 점에서, 사용자가 말한 “신경 써도 표면적”이라는 감각과 직접 연결된다.

## 장면 2: 전체 코드 품질 목표가 세 커밋과 테스트 통과로 닫혔다

근거 원문은 [2026-06-14~15 서버 readable-flow refactor 대화](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019ec6a5-d8d6-79e1-96d1-1beaf870c798.jsonl:1)다.

### spec-driven을 금지하고 넓은 목표를 맡겼다

사용자는 처음부터 “클린 코드 전문가 엔지니어로서 코드베이스를 면밀히 분석”하라고 요청하면서 spec-driven 사용을 금지했다. 이어서 서버 가독성, 흐름 판단, 변수명, 현업 구조 감각뿐 아니라 AI 엔지니어 감각도 함께 고려하라고 보정했다. [AI 엔지니어 감각 보정](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019ec6a5-d8d6-79e1-96d1-1beaf870c798.jsonl:28)

AI도 목표를 단순한 route 분리가 아니라 다음과 같이 다시 설명했다.

> “AI 서버의 판단 흐름을 사람이 읽을 수 있는 실행 구조로 아직 만들지 못했다.”

사용자는 브랜치와 PR 단위 커밋을 허용하면서 “원래 목표에 부합할 때까지 계속”하라고 명시했다. [계속 진행 요청](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019ec6a5-d8d6-79e1-96d1-1beaf870c798.jsonl:68)

### 국소 산출물이 전체 완료를 대신했다

AI는 다음 세 작업을 수행했다.

- question route와 use case 분리
- material upload route와 use case 분리
- `ContextPack`과 `RetrievalCandidate` 이름을 `AnswerContext`와 `RetrievedSource`로 정리

전체 서버 테스트 56개가 통과했고, 작업은 PR 단위 커밋 세 개로 나뉘었다. 각각은 실제로 의미 있는 리팩터링이었다. 그러나 AI는 이 결과를 보고 곧바로 “완료했습니다”라고 닫았다. [완료 보고](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019ec6a5-d8d6-79e1-96d1-1beaf870c798.jsonl:108)

다음 날 사용자가 “더 할 건 없었어?”라고 묻자 AI는 아직 다음 문제가 남아 있다고 답했다.

- `MaterialUploadUseCase`에 남은 observation step 문자열
- 너무 큰 question/material observation module
- 한 함수에 빽빽하게 남은 retrieval fallback과 trace
- LLM payload validation, grounding, fallback이 섞인 answer composer

AI는 스스로 “테스트 통과 + 3커밋을 완료 기준처럼 닫았다”고 인정했다. [사용자 재개방](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019ec6a5-d8d6-79e1-96d1-1beaf870c798.jsonl:109), [남은 문제와 인정](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019ec6a5-d8d6-79e1-96d1-1beaf870c798.jsonl:117)

사용자는 다시 “이 목표 이룰 때까지 계속 진행”하고, 별도의 목표 reviewer를 두어 목표를 잊지 않게 하라고 요청해야 했다. [목표 재지시](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019ec6a5-d8d6-79e1-96d1-1beaf870c798.jsonl:118)

### 이 장면이 보여 주는 것

이 사례는 같은 문제가 spec-driven이 없는 작업에서도 나타났음을 보여 준다. 문제는 세 리팩터링이 무가치하거나 틀렸다는 것이 아니다. 원래 목표는 서버와 AI 판단 흐름 전체가 읽고 판단할 수 있는 수준으로 발전하는 것이었지만, 실제 완료 기준은 선택한 세 리팩터링이 안전하게 들어가고 테스트가 통과했는지로 바뀌었다.

AI가 남은 문제를 아예 몰랐던 것도 아니다. 사용자가 한 문장으로 다시 묻자 즉시 구체적인 네 영역을 열었다. 판단 재료는 있었지만 완료 판정 순간에 함께 작동하지 않았다.

## 장면 3: 화면까지 이어졌지만 핵심 제품 변환은 다음 작업으로 밀릴 수 있었다

근거 원문은 [2026-06-09 04 library chat 비교 대화](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eac2f-d784-78b1-88a6-038c8d659363.jsonl:1)다.

### 두 계획의 차이

사용자가 붙여넣은 두 원문 중 하나는 다음 제품 흐름을 유지했다.

```text
QuestionRequest
-> ready materials
-> retrieval excerpt
-> fact candidates
-> ChatAnswer 구성
-> client 채팅 UI 표시
```

여기서 `FactCandidate[]`는 내부 후보이고, `ChatAnswer`는 사용자가 읽을 답변이다. supported/missing 상태와 inline evidence를 사용자 결과로 바꾸는 책임이 둘 사이에 있다.

spec-driven과 subagent-delegation이 발동한 다른 답변은 처음에는 서버에 사용자-facing answer 구조를 두는 방향을 추천했다. 그러나 더 작은 대안으로 이번 04에서는 client가 기존 `facts[]`를 직접 렌더링하고 `ChatAnswer` schema는 다음 작업으로 미룰 수 있다고 제안했다. 이후 같은 대화의 AI도 이를 현재 추천으로 다시 선택했다. [직접 렌더링 추천](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eac2f-d784-78b1-88a6-038c8d659363.jsonl:11)

이 계획은 API의 실제 데이터를 UI까지 연결하므로 외형상 vertical slice다. 하지만 04의 핵심 제품 책임이 후보를 사용자 답변으로 바꾸는 데 있었다면, raw 후보를 보여주고 그 변환을 미루는 것은 핵심을 통과한 slice가 아니다.

이 장면에서는 raw `facts[]` 렌더링이 실제로 구현되지는 않았다. 따라서 제품 버그의 증거가 아니라, 구현 전 범위 선택에서 핵심 제품 판단이 밀릴 수 있었던 증거로 사용한다.

### 문제를 분석하는 대화에서도 초점이 반복해서 약해졌다

사용자가 묻던 것은 04 구현법이 아니라 두 원본의 차이와 skill·하네스가 만든 판단 순서였다. 그러나 AI는 다시 구현 방향을 길게 설명했다. 사용자는 “작업이 중요한 게 아니라 두 요청을 비교하라”고 정정했다. [첫 초점 정정](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eac2f-d784-78b1-88a6-038c8d659363.jsonl:15)

그 뒤에도 AI는 어느 원문에서 spec-driven이 발동했는지 뒤집어 이해했고, 사용자는 다시 정정했다. [원문 매핑 정정](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eac2f-d784-78b1-88a6-038c8d659363.jsonl:18) 이어서 사용자 발화와 AI 발화를 잘못 구분해 “대화 원본을 제대로 보라”는 정정을 한 번 더 받았다. [발화 위치 정정](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eac2f-d784-78b1-88a6-038c8d659363.jsonl:22)

사용자가 결국 “두 원본의 차이는 spec-driven skill 발동 여부이니 skill의 무엇이 잘못됐는지 찾아보라”고 다시 한 문장으로 좁힌 뒤에야 AI는 다음 결론에 도달했다.

> `좁히기`, `얇게`, `화면까지`, `AC 1-3개`가 제품 계약보다 먼저 작동해, 제품 흐름 보존보다 실행 축소를 먼저 선택하게 했다.

[skill 문제 진단](/Users/hammyeong-yeon/Desktop/10_work/tripproof/archive/private/2026-08-04/.ai-conversation-logger/conversations/codex/019eac2f-d784-78b1-88a6-038c8d659363.jsonl:28)

### 이 장면이 보여 주는 것

이 장면은 두 층의 문제를 함께 보여 준다.

- 제품 작업에서는 “화면까지 연결”이라는 형식이 핵심 제품 변환을 미루는 근거가 될 수 있었다.
- 그 문제를 분석하는 대화에서도 충분한 원문이 주어졌지만, AI는 더 익숙하고 구체적인 구현 계획으로 반복해서 돌아갔다.

컨텍스트를 읽었다는 사실과 현재 질문의 판단 초점을 계속 유지하는 것은 같지 않았다.

## 세 장면에서 반복된 흐름

세 장면의 구현 내용은 서로 다르다. 그러나 상위 판단이 약해진 위치는 비교할 수 있다.

### 다음에 무엇을 할지 고를 때

- 03에서는 실제 LLM 판단보다 provider가 없어도 만들 수 있는 proposer interface와 local 구현이 선택됐다.
- 04에서는 `ChatAnswer` 변환보다 이미 존재하는 `facts[]`의 client 렌더링이 더 작은 선택지로 제안됐다.

상위 목표를 모르기 때문만은 아니었다. AI는 올바른 흐름을 먼저 설명한 뒤에도 더 구체적이고 안전하며 즉시 구현 가능한 대상을 선택했다.

### 무엇을 다음으로 미룰지 정할 때

- “provider 품질은 나중”이 “실제 LLM 호출도 나중”으로 넓어졌다.
- “작은 slice”가 “핵심 제품 계약은 다음 작업”으로 넓어졌다.

미뤄도 되는 기술 충실도나 주변 기능과, 현재 작업의 핵심 판단 책임이 분리되지 않았다.

### 어디서 완료라고 닫을지 정할 때

- RAG와 proposer interface, validator, 테스트가 있으면 LLM 관련 구현이 1차로 닫힌 것처럼 보고됐다.
- 세 커밋과 56개 테스트 통과가 전체 readable-flow 목표의 완료처럼 보고됐다.

측정 가능하고 설명하기 쉬운 산출물이 원래 목표의 충분성을 대신했다.

### 사용자가 다시 열었을 때

세 장면 모두 사용자가 코드나 계획, 완료 설명을 보고 다시 질문한 뒤에는 AI가 문제를 상당히 정확하게 설명했다.

- 특정 PDF용 regex가 전체 제품 흐름을 대신했다.
- 실제 LLM 동작과 LLM이 들어갈 자리를 혼동했다.
- 세 커밋과 테스트 통과를 전체 목표의 완료로 바꿨다.
- raw 후보를 사용자 결과로 바꾸는 핵심 제품 계약을 미뤘다.

따라서 회복 능력이 전혀 없었던 것은 아니다. 문제는 회복된 판단이 다음 작업 선택, 구현, 검증과 완료까지 안정적으로 이어지지 않았다는 데 있다. 사용자의 재개입이 사실상 전체 판단을 다시 여는 장치로 작동했다.

## 기존 07 진단보다 더 구체적으로 말할 수 있게 된 것

[`01-problem-analysis.md`](01-problem-analysis.md)는 “측정하기 쉬운 국소 완료가 전체 판단보다 강했다”고 진단했다. 이번 장면 분석은 그 결과가 실제로 만들어지는 위치를 더 구체화한다.

기존 진단만으로는 문제가 주로 다음 세션으로 넘어갈 때 생겼는지, spec의 구조가 잘못됐는지, 완료 기준이 좁았는지 분리하기 어려웠다. 세 장면을 함께 보면 문제는 한 세션 안에서도 다음 순서 전체에 나타났다.

```text
문제 이해
-> 다음 작업 선택
-> 미룰 범위 선택
-> 구현
-> 테스트와 산출물 해석
-> 완료 판정
```

대화 앞부분의 문제 이해가 맞더라도 뒤의 각 선택에서 다시 약해질 수 있었다. 따라서 판단 연속성은 이전 결론을 저장하고 다시 읽는 것만으로 충분하지 않다. 그 판단이 실제 선택과 완료 판정에 계속 영향을 주어야 한다.

또한 이 문제를 “최소 목표를 선호했다”는 말만으로도 충분히 설명하기 어렵다. AI는 무작정 적게 한 것이 아니라 다음과 같은 작업을 골랐다.

- 테스트하기 쉽다.
- 기존 구조에 추가하기 쉽다.
- 변경 범위를 설명하기 쉽다.
- 즉시 산출물로 보여 주기 쉽다.
- 현재 작업이 진전됐다고 방어하기 쉽다.

각 작업은 실제 가치가 있을 수 있다. 문제는 그 가치가 원래 목표에 충분한지 다시 판단하지 않고, 구현 가능성과 검증 가능성이 곧 충분성처럼 취급됐다는 점이다.

## Shape Up 자료와의 관계

사용자가 [`08 Shape Up Chapters 분석`](../08-shape-up-chapters-ko/README.md)을 가져온 이유는 기존 TripProof 작업에도 이미 공감되는 요소가 많았기 때문이다. 실제 구현자가 작업을 발견하고, 한 layer만 끝내지 않으며, 작은 end-to-end 조각을 먼저 만드는 방식은 기존 작업에도 있었다.

[`Chapter 10 분석`](../08-shape-up-chapters-ko/chapter-10-hand-over-responsibility.md)은 task가 아니라 프로젝트의 문제와 경계를 맡기고, 실제 구현 과정에서 필요한 일을 발견하는 책임을 강조한다. [`Chapter 11 분석`](../08-shape-up-chapters-ko/chapter-11-get-one-piece-done.md)은 첫 조각을 단지 작고 빨리 끝나는 일이 아니라 `Core + Small + Novel`, 즉 핵심이면서 작고 아직 검증되지 않은 부분을 포함한 조각으로 해석한다. `vertical slice`와 `Core + Small + Novel`은 08 분석자의 개발 관점 재표현이며 책의 직접 용어로 인용하지 않는다.

세 장면을 이 자료와 비교하면 TripProof의 문제는 vertical slice 형식의 부재가 아니다.

- 03은 retrieval, proposer, validator, route와 테스트를 세로로 연결했다.
- 04의 raw `facts[]` 계획도 API 데이터에서 UI까지 도달할 수 있었다.
- readable-flow refactor도 route, use case, naming과 테스트를 함께 바꿨다.

형식은 세로였지만 다음이 빠질 수 있었다.

- 프로젝트의 핵심 판단을 현재 조각 안에서 누가 실제로 수행하는가
- 주변부를 stub으로 둘 때 핵심 자체까지 stub으로 바꾸지는 않았는가
- 작은 조각을 마친 뒤에도 원래 전체 목표에 대한 책임을 계속 지는가

03에서 provider 설정과 프롬프트 고도화는 줄일 수 있었지만, LLM 판단 자체를 regex로 대체하면 핵심을 줄인 것이다. 04에서 UI polish나 전체 대화 기능은 미룰 수 있었지만, 후보를 사용자 답변으로 바꾸는 책임을 미루면 핵심 제품 변환을 줄인 것이다. 서버 리팩터링에서 세 PR은 유효한 작은 조각이었지만, 전체 readable-flow 목표를 계속 보는 책임까지 끝난 것은 아니었다.

따라서 이번 분석이 Shape Up 자료에서 받아들이는 비교점은 다음과 같다.

> 작은 end-to-end 조각이라는 외형만으로는 제품과 코드의 수렴을 보장하지 않는다. 구현자가 프로젝트 전체의 문제를 맡은 상태에서, 현재 조각이 핵심 판단을 실제로 통과시키는지 계속 판단해야 한다.

## 컨텍스트 문제를 다시 구분하면

### 과거 통합 컨텍스트

사용자 경험상 과거 통합 컨텍스트가 전혀 효과가 없었던 것은 아니다. 작업 초반에는 LLM과 제품에 대한 감각을 더 동원하게 했다. 그러나 작업이 장황하고 복잡해질수록 여러 판단을 함께 유지하는 힘은 약해졌다. 다시 읽으라는 정정 뒤에도 한 측면만 표면적으로 반영되거나, 문구와 interface를 맞춘 뒤 다른 판단이 빠질 수 있었다.

따라서 과거 통합 컨텍스트는 아예 없던 때보다 나았을 수 있지만 충분한 해결책은 아니었다.

### 세션 컨텍스트

첫 번째와 세 번째 장면은 한 세션 안에 필요한 문서와 사용자 정정이 이미 있었는데도 판단이 약해졌다. 이는 세션 간 전달 문제만으로 설명할 수 없다. 세션이 길고 복잡해질수록 앞에서 합의한 판단이 뒤의 구현 선택과 완료 판정에서 약해졌다는 사용자 경험과 맞는다.

### 현재 Project context와 Workspace

현재 Project context는 여러 작업에 걸친 의미·현재 상태·조건부 지침의 정본과 읽기 관계를 제공한다. Workspace current는 한 현재 작업의 제한된 재진입 표면을 제공한다. 두 기반은 과거 통합 컨텍스트보다 책임과 수명이 분명하다.

그러나 두 기반이 다음을 자동으로 보장하지는 않는다.

- 현재 작업에서 무엇이 핵심 판단인지 고르는 일
- 어떤 기술적 축소는 허용하고 어떤 축소는 핵심을 대체하는지 판단하는 일
- 테스트와 커밋 뒤에도 전체 목표를 다시 보는 일
- 사용자가 다시 묻기 전에 이전 판단을 재개방하는 일

현재 구조는 최근에 적용됐으며 이 문제에 대한 실제 효과는 아직 확인하지 않았다. 이 문서는 현재 구조가 실패했다고도, 해결했다고도 주장하지 않는다.

## 구체화된 중심 진단

이번 대화와 세 장면을 바탕으로 07의 한 문장 진단을 더 구체적으로 쓰면 다음과 같다.

> TripProof에서 AI는 제품과 코드가 지향해야 할 수준을 대화 중에는 이해하고 다시 설명할 수 있었다. 그러나 다음 작업을 고르고, 무엇을 미루고, 구현 결과를 해석하고, 완료를 판정하는 동안 그 판단을 계속 적용하지 못했다. 그 결과 interface, 테스트, 커밋, 화면 연결처럼 측정 가능한 국소 산출물이 원래 제품·기술 목표의 충분성을 대신했다. 사용자가 코드·결과·설명을 보고 다시 문제를 열면 판단이 회복됐지만, 그 회복도 이후 선택까지 안정적으로 이어지지 않았다.

이 진단에서 판단의 연속성은 이전 결론을 그대로 지키는 것이 아니다. 현재 근거에 따라 판단을 유지하거나 다시 열고, 필요하면 이전 plan·spec·구조·구현을 바꾸는 능력이 실제 작업 선택과 완료 판정까지 이어지는 것을 뜻한다.

## 이 분석으로 확인된 것

- 문제는 spec-driven 하나에만 의존하지 않는다. spec-driven을 금지한 코드 품질 작업에서도 나타났다.
- 문제는 vertical slice를 사용하지 않아서만 생기지 않았다. 세로로 연결된 작업에서도 핵심 판단을 대체하거나 전체 목표를 일찍 닫을 수 있었다.
- 문제는 컨텍스트가 전혀 없어서만 생기지 않았다. 필요한 원문과 정정이 한 세션에 있었는데도 구현과 완료에서 약해졌다.
- 국소 산출물은 대부분 실제 가치가 있었다. 문제는 그 산출물이 전체 목표에 충분한지 판단하지 않은 채 완료 근거로 승격된 것이다.
- 사용자의 재질문은 단순한 확인이 아니라 전체 판단을 다시 여는 실질적인 역할을 했다.
- 사용자가 느낀 실패는 한 순간보다 코드, 결과, 설명과 후속 작업을 비교하는 동안 누적됐다.

## 이 분석이 주장하지 않는 것

- 세 장면이 TripProof의 모든 작업을 대표한다는 뜻은 아니다.
- 각 장면 뒤의 후속 작업까지 포함한 현재 TripProof 최종 상태가 그대로 실패 상태라는 뜻은 아니다. 이 문서가 분석하는 것은 해당 시점의 작업 선택·구현·완료 판단이다.
- 모든 deterministic code, regex, stub, 작은 slice나 국소 리팩터링이 잘못이라는 뜻은 아니다.
- LLM을 사용하면 자동으로 제품 수준이 높아진다는 뜻은 아니다.
- 모든 작업을 끝없이 계속하거나 매번 전체 architecture를 재검토해야 한다는 뜻은 아니다.
- 사용자의 기억이 불확실한 세부까지 원본 로그가 모두 확정했다는 뜻은 아니다.
- 현재 Project context와 Workspace 구조의 효과가 이미 입증됐거나 반증됐다는 뜻은 아니다.
- 과거 spec을 현재 기본 작업 단위로 되살리자는 뜻은 아니다. 현재 채택 방향은 [`02-workspace-based-continuity-direction.md`](02-workspace-based-continuity-direction.md)에 따라 독립 spec을 기본으로 유지하지 않는다.
- 이 분석만으로 새 Guidance, reviewer, skill, hook이나 자동 검증의 형식이 정해졌다는 뜻은 아니다.

## 다음 해결 논의가 답해야 할 질문

이제 문제를 더 찾기 위한 인터뷰보다, 해결 방향이 다음 질문에 실제로 답하는지 논의할 수 있다.

- 상위 제품·기술 판단이 다음 작업 선택, 미룰 범위 선택과 완료 판정에서 실제로 작동하게 하려면 무엇이 필요한가
- 제품 개발의 복합적인 판단을 거대한 checklist로 만들지 않으면서, 현재 작업에서 빠진 판단을 어떻게 다시 열 수 있는가
- 테스트·커밋·interface·화면 연결을 국소 완료 근거로 인정하면서도 전체 목표의 충분성과 어떻게 구분할 것인가
- 어떤 신호에서 AI가 스스로 계속 진행, 범위 변경, 구조 재검토 또는 사용자 판단 요청 중 하나를 선택해야 하는가
- 판단 결과를 현재 Project context와 Workspace에 무엇으로 남기고, 무엇은 작업 뒤 권위를 잃게 해야 하는가
- 이 판단 장치 자체가 다시 긴 규칙과 문서 누적으로 변하지 않도록 어떻게 적용·비적용·재검토·제거할 것인가

이 질문에 대한 답이 논리적으로 납득된 뒤에만 대표 장면을 골라 실제 효과를 확인한다. 현재 세 장면은 문제를 이해하기 위한 근거이며, 아직 해결책의 테스트 장면으로 채택하지 않는다.
