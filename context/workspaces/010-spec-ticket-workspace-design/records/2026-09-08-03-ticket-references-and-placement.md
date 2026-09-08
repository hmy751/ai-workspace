# Ticket 외부 용례와 memory·state 배치 의견

날짜: 2026-09-08

## 요청과 확인 범위

사용자는 앞선 결정을 먼저 커밋하고, Ticket 구성·진행 상태 설계에 들어가기 전에 기존 외부 자료와 Desktop의 Matt 한국어 독해본에서 Ticket을 어떻게 다루는지 설명해 달라고 했다. 사용자의 이해는 ‘Spec 하위에 task 같은 작업’이며, memory·state 중 적절한 위치에 대한 Main의 의견도 요청했다. 전체 저장소 정독이나 실제 Ticket 체계 구현 요청은 아니다.

Spec의 배치·수명·기존 current 대체·다섯 Markdown 파일 결정은 commit `5320930`으로 남겼다. 커밋 직후 tracked 변경은 없었고 기존 `.DS_Store`만 untracked였다. 아래 조사는 그 커밋 이후 작업이다.

로컬 자료는 `/Users/hammyeong-yeon/Desktop/matt-skills-한국어-독해본`에서 README와 `skills/engineering/to-tickets/SKILL.md`를 확인했다. 실제 디렉터리명은 macOS 한글 분해형이다. 독해본 기준 commit은 `068b6e0c62393147daf03530149cdce209c93da8`이다. 자료 속 skill은 연구 대상으로 읽었으며 호출하거나 tracker에 게시하지 않았다.

## 외부 자료에서 확인한 의미

- **Matt Pocock의 개발 skill**: Spec·plan·대화에서 실행할 Ticket을 만든다. Ticket마다 전달할 동작·완료 조건·선행 Ticket을 둔다. 로컬 template에는 `Status`도 들어가므로 정의와 진행을 함께 담는 방식이다. 새 세션 하나가 수행할 크기와 여러 구현 층을 거쳐 독립 확인할 수 있는 동작 단위를 선호하지만 이는 해당 skill의 분해 규율이다. [to-tickets 설명](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/docs/engineering/to-tickets.md), [실제 skill과 template](https://github.com/mattpocock/skills/blob/068b6e0c62393147daf03530149cdce209c93da8/skills/engineering/to-tickets/SKILL.md).
- **GitHub Spec Kit**: Spec·plan 등을 입력으로 `tasks.md`를 구성한다. 사용자 이야기별 작업 묶음과 개별 ID, 병렬 가능 표시, 의존 관계 등을 둔다. Matt처럼 모든 개별 Task를 독립 기능 Ticket으로 구성하는 같은 단위는 아니다. [Task template](https://github.com/github/spec-kit/blob/main/templates/tasks-template.md).
- **Kiro**: requirements·design 이후 실행할 `tasks.md`에 작업 설명, 기대 결과, 의존 관계와 선택/필수 구분을 둔다. [Requirements-First의 Tasks 단계](https://kiro.dev/docs/specs/feature-specs/requirements-first/).
- **OpenSpec**: `tasks.md`를 구현 단계의 체크리스트로 설명하고 완료 시 체크한다. [Artifacts의 Tasks 설명](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md).

공개 자료는 이날 다시 열어 해당 부분을 확인했다. Matt는 위 고정 revision을, 다른 세 자료는 접근 당시 페이지를 근거로 삼았다. 서로 같은 Ticket schema나 memory/state 분리를 정의하지 않는다. 이 자료들에서는 요구 정의와 실행할 일의 구별을 확인할 수 있지만, 단위의 크기와 저장·추적 방식은 다르다.

## Main의 제안 — 아직 사용자 채택 전

사용자가 이해한 ‘Spec을 수행하기 위해 나눈 작업’은 이번 설계의 출발점으로 적절하다. Ticket으로 식별하고 맡기고 추적할 수 있도록 실행 범위·필요한 입력·완료 조건 등을 구체화한다. Spec 본문의 한 항목과 Ticket 하나가 반드시 일대일인 것은 아니다. 외부 자료에서 Ticket 입력이 항상 Spec인 것도 아니다.

현재 구조를 이어가는 제안은 **Ticket의 작업 정의는 `memory/tickets/`, Ticket별 진행·막힘·결과와 다음 행동은 state**다. 정의도 필요하면 수정할 수 있다. 완료 조건과 실제 완료 여부는 다른 정보이므로, 수정 가능성만으로 둘을 같은 위치에 둘 필요는 없다.

이 배치의 이점은 기존 memory가 맡은 작업 기준과 state가 맡은 실행 현황을 유지하면서 같은 진행 상태를 두 곳에서 관리하지 않는 것이다. 비용은 Ticket 파일 하나만 읽어서는 현재 실행 상황까지 알 수 없다는 점이다. 새 실행자에게 Ticket을 전달할 때 해당 상태도 함께 읽히도록 해야 한다. 정확한 읽기·갱신 계약은 후속 설계 사항이다.

Ticket 자체에 상태를 함께 두면 한 문서로 인계하기 쉽다. 대신 memory 안에도 진행을 갱신하는 문서가 생기며 Workspace state와의 중복을 정리해야 한다. 이는 가능한 대안이고 외부 용례에도 부합한다. 정의와 진행의 물리적 분리는 보편적인 Ticket 정의가 아니라 우리 책임 구분을 유지하려는 운영 선택이다.

Ticket 완료는 그 Ticket의 완료 조건을 충족했다는 판단이다. Spec 전체 목표와 남은 핵심 문제의 판단을 대신하지 않는다. 이번에는 비교와 배치 의견만 기록했으며 Ticket 구성·상태 schema나 Reference 변경을 확정하지 않았다.
