# Goal·loop·engineering 구조 main 이식

날짜: 2026-07-17

상태: **main 작업 트리 이식·정합성 검토 완료**

## 계기

별도 worktree `cofathon-core-goal-loop`에는 Mission–Campaign Goal–엔지니어링 최상위 Goal–loop Goal의 관계, 최신 상태에서 다음 행동을 다시 고르는 반복 운용, 개발·조사 원칙, 비활성 engineering 구조가 제안돼 있었다.

최신 main은 그 worktree의 기준 commit 이후 다음 상태까지 진행했다.

- 개인 조건과 원하는 경험에서 나온 운영 조건을 판매자가 답할 최소 질문으로 닫고 구매·보류·다른 상품을 다시 고르는 후보를 선택했다.
- 현재 커서는 실제 사용자와 현재 판매 투어 한 건의 입력을 정하는 지점이다.
- 후보 발산 중의 주장별 근거 판정과 마지막 후보 단위 종료를 분리하는 core 기준이 추가됐다.
- 로컬 조사 도구와 process 20~26이 추가됐다.

따라서 worktree의 tracked 파일을 merge하거나 전체 복사하지 않고, 새 문서의 설계 본체를 최신 main 위에 이식하고 기존 current·core·process·CLAUDE 규칙을 보존했다.

## 사용자 요청으로 확정한 적용 방향

사용자는 Goal이 현재 상황에서 달라졌을 수 있고 용어 충돌과 소유권 문제에는 동의하지만, 이를 이유로 loop 설계를 임의로 축약하지 말고 한 번 실제로 이식해 보라고 요청했다.

이에 따라 다음을 적용했다.

- Goal 계층과 상세 loop 운용은 보존한다.
- 일곱 종류의 진전 delta, 결과물 보정·평가 정밀화·공유 기준 승격·Goal amendment의 구분, terminal state, 문서 소유권을 삭제하지 않는다.
- dev-principles와 반복 공개 페이지 조사 원칙도 함께 이식한다.
- engineering은 아직 열지 않고 README에 진입 조건과 기록 경계만 둔다.
- 오래된 worktree의 current·CLAUDE·core README를 덮어쓰지 않는다.

이번 요청은 main이 current를 바탕으로 Campaign Goal 내용을 교정해 실제 운용 작업판을 만드는 데 대한 승인으로 해석했다. 아래 정확한 문장과 완료 목록이 영구 불변이라는 뜻은 아니다. 지금 작업판의 두 증거 채널은 기존 지원 증거물 계약을 연결한다. 이를 별도 `Goal 확인 단계`로 만들지 않으며, 사용자가 문구나 필수성을 바로잡으면 그때 Goal amendment로 기록한다.

## Campaign Goal 현재판 교정

Goal **계층**은 사용자가 확정했지만, 별도 worktree의 Campaign Goal 문구를 영구 확정된 내용처럼 옮기지 않았다. 최신 선택 후보가 여행자의 구매 판단 장면이므로 `실제 업무 문제`를 `실제 사용자 문제·workflow`로 고쳤다. 같은 이유로 기존 지원 증거물 계약의 `실제 업무 문제·업무 순간`도 `실제 사람의 문제·workflow·판단·행동 순간`으로 일반화했다. 증거 강도나 두 증거 채널은 바꾸지 않았다.

현재 Campaign Goal은 다음 상태를 지향한다.

> 지원 마감 안에, Q1만 읽어도 내가 AI Native인 이유와 증명 논리가 이어지고, 선택한 실제 사용자 문제·workflow에서는 지원 증거물 계약에 따른 작동 결과와 AI 제작 과정의 인과를 실제 근거로 확인할 수 있는 지원안을 제출해 접수를 확인한다.

상세 닫힘 조건은 Goal 문서가 다시 정의하지 않고 canonical 문서에 위임했다.

- 문제–솔루션의 현재 닫힘 조건 — `context/current.md`
- 플러그인의 형태와 두 증거 채널 — `context/core/support-evidence-artifact.md`
- 공식 제출 조건 — `context/core/requirements.md`

## 용어 교정

main에서 `Probe`는 Cofa가 공개한 본선 측정 제품의 고유명사다. worktree의 loop 문서는 제한된 조사·비교·실행까지 같은 단어로 불렀다.

이식본에서는 일반 운용 단위를 다음처럼 쓴다.

- 판단을 바꿀 질문 — `판별 질문`
- 그 질문을 판정하기 위한 제한된 조사·비교·실행 — `판별 실행`
- Cofa가 공개한 제품 — `Probe`

한 판별 실행의 보류·기각은 Goal이나 후보 전체의 종료가 아니다. 후보 단위 선택·미선택·종료는 기존 `candidate-exploration-judgment-order.md`의 마지막 수렴 계약이 계속 소유한다.

## 소유권 교정

### Goal과 현재 지도

- `context/goal.md` — Mission, Campaign Goal의 현재판과 상위 완료 상태
- `context/current.md` — Goal의 짧은 요약·링크, 실제 진행 상태, 현재 판별 질문, 단일 커서
- `context/core/loop.md` — Goal을 세우고 보정하는 감각과 반복 운용

### 후보와 개발 원칙

- 후보 발산·교차 중의 근거 상태와 마지막 후보 단위 종료 순서는 기존 `candidate-exploration-judgment-order.md`가 계속 소유한다.
- `dev-principles.md`는 사람의 결과 변화, 가치 보존, 의미 판단과 결정론적 실행 분리, output-first, 근거·검증 원칙을 소유하고 후보 상세 순서는 링크로 위임한다.
- 결과 소비 형식은 README로 고정하지 않고, 설치를 전제하지 않는 첫 접촉에서 대표 결과와 근거를 확인할 수 있어야 한다는 원칙까지만 고정한다.

### engineering과 process

- engineering은 구현 산출물, 실행 명령, fixture, 실제 결과, 재현 증거를 소유한다.
- process는 선택·변경·기준 승격·Goal amendment·게이트 판정의 시간순 이유와 증거 링크를 소유한다.
- before/after 결과와 작업 맥락 밖 판별 장면은 engineering 진입 조건이 아니라 실제 엔지니어링에서 만들어야 할 완료 증거로 구분했다.

## 독립 판별 계약 보강

새 세션이나 다른 agent라는 사실만으로 독립 판별이라고 하지 않는다.

- 판별자는 결과물과 원자료에 접근한다.
- main의 예상 결론은 받지 않는다.
- 필요한 증거 범위를 스스로 정한다.
- main의 질문이나 평가 범위가 틀렸다면 기각하거나 수정할 수 있다.

이 기준은 `core/loop.md`, `core/dev-principles.md`, `engineering/README.md`에 반영했다.

## 이식한 문서와 연결

- `context/goal.md`
- `context/core/loop.md`
- `context/core/dev-principles.md`
- `context/core/research.md`
- `context/engineering/README.md`
- 별도 worktree 설계 이력 `context/process/19-loop-engineering-and-working-principles-redraft.md`
- 실제 main 통합 기록인 이 문서
- 최신 `CLAUDE.md`, `context/current.md`, `context/core/README.md`, `context/process/README.md`의 의미 단위 연결

## 현재 단계에 미치는 영향

- 최신 선택 후보와 실제 상품 표적 확인 입력 선택 커서를 유지한다.
- 실제 입력으로 개인·운영 조건의 미확정, 판매자가 답할 수 있는 범위, 답변 뒤 구매 판단 변화가 확인되기 전에는 engineering을 활성화하지 않는다.
- engineering README는 이후 단계의 진입 조건과 기록 경계만 안내하며, 현재 구현 순서나 backlog가 아니다.

## 검증 결과

로컬 형식 검사와 서로 다른 읽기 전용 판별자 두 갈래가 전체 작업 트리, 원본 current·candidate core·support contract·requirements, 새 Goal·loop·engineering 구조를 대조했다.

통과한 것:

- canonical 문서에서 일반 운용 단위의 `Probe` 충돌을 제거했고 Cofa 제품명에만 남겼다.
- 최신 선택 후보, 후보 판단 core, LazyCodex 규칙, process 20~26을 보존했다.
- 로컬 Markdown 링크와 공백·tracked diff 검사가 통과했다.
- dev-principles가 후보 상세 종료 규칙을 candidate core에 위임하고, 사실 모순·고정 경계 위반·실질적으로 같은 후보의 중간 종료 예외도 loop에 보존했다.
- engineering 진입 조건에서 before/after·판별 장면을 완료 증거로 내리고, 실행 증거는 engineering, 판단 이력은 process가 소유하게 통일했다.
- engineering은 아직 열지 않고 README만으로 진입 조건과 기록 경계를 남겼다.

검토 중 발견해 고친 것:

- Goal이 상세 완료 증거 전체를 소유하는 것처럼 읽힌 문제 — 상위 완료 상태와 증거 요구만 소유하고 상세 판정은 canonical 문서에 위임

남은 열린 상태:

- 실제 사용자–현재 판매 투어 입력 선택과 표적 확인
- 문제–솔루션 닫힘 뒤 엔지니어링 단계에서 실제로 만들 구현·검증 계약

## 후속 사용자 교정 — 실제 커서와 엔지니어링 선행 구조 원복

main이 마감 위험을 이유로 current 커서를 지원 제출 판단으로 옮기고, 아직 시작하지 않은 engineering에 top-level/loop Goal 문서를 미리 만들었다. 사용자는 실제 작업이 표적 확인 뒤 엔지니어링으로 이어져야 하며 이 선행 구조가 현재 상태를 왜곡한다고 교정했다.

- 단일 커서를 `문제 설정·솔루션 → 실제 상품 표적 확인 입력 선택`으로 되돌렸다.
- current와 core loop에서 제출 마감 하한선 경로를 제거했다.
- `engineering/00-top-level-goal.md`, `engineering/01-loop-01-goal.md`를 삭제했다.
- 파일 삭제는 엔지니어링 Goal 구조 자체를 버린다는 뜻이 아니다. `core/loop.md`의 엔지니어링 최상위 Goal·loop Goal 구조는 유지한다.
- engineering은 README만 남겨 현재 비활성 상태, 진입 조건, 이후 문서 형태와 기록 경계를 안내한다.
- 문제–솔루션이 닫혀 엔지니어링이 시작되면 `00-top-level-goal.md`를 먼저 만들고, 독립 계약이 필요한 구현 loop에만 `NN-loop-NN-goal.md`를 만든다. 지금은 이 파일들과 loop 순서를 선행 생성하지 않는다.
