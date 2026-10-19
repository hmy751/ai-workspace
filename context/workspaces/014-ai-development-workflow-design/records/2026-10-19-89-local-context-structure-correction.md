# 로컬 context 안의 Personal·Project·Work로 구조 정정

2026-10-19. 사용자는 새 적용 프로토타입이 실제 구조를 반영하지 못했다고 지적하고, Noline에 어떻게 적용됐는지 직접 확인해 고치라고 요청했다. 이번 조사·수정·검사는 Main이 직접 수행했다. 앞선 별도 검토의 통과를 이번 정정의 근거로 대신하지 않았다.

## 직접 확인한 사용자 의도

> 자꾸 왜 제대로 안 만드냐? 너 실제 구조가 저래? 똑바로 파악해라 좀 폴더 계층도 그렇고 대충 하지말고 noline에는 어떻게 적용되어 있는지도 보고 폴더 구성을 왜 저따위로 하냐 noline-demo 안에 context에 구성하던지 시키지 말고 직접해라
> 그리고 물어볼거 있음 물어보고

Main은 Personal까지 demo context 안에 둘지, 앞서 기록한 ai-workspace 위치를 유지할지 한 가지를 확인했다. 사용자 답:

> 당연히 context안에 둬야지 아까 로컬은 니가 글로벌로 personal로 두려고 하니까 ai-workspace 쪽에 두라고 한거고 정확히는 context안에 둬야 할꺼아냐

따라서86을 근거로 별도 ai-workspace 모형을 Personal의 필수 호스트로 둔 해석은 대체한다. 사용자가 의도한 것은 글로벌 분리가 아니라 **로컬 context 안에서 관리·축적·수정하는 층**이다. 현재 실물은 `noline-demo/context/personal/`, `project/`, `work/`다. 이 정정은 세 본문의 내용 책임을 합치거나 Project가 개인 기준의 채택 목록을 관리하라는 뜻이 아니다.

## 실제 Noline에서 확인한 근거

조사 대상은 `/Users/hammyeong-yeon/Desktop/10_work/noline`이고 HEAD는 `4fb309d2ba50afaca44019879d7161964b9b2328`이다. 저장소의 root 가이드, 실제 context 계약과 Project 본문·관리 기준, Work 운영·Workspace 구조, 실제 Workspace의 memory와 Spec·Ticket 경로를 직접 읽었다. Noline의 원본 파일과 실행 상태를 변경하지 않았다.

| 실제 위치 | 확인한 관계와 이번 반영 |
| --- | --- |
| `context/README.md` | Project와 Work를 구별한다. Personal은 기존 구조가 아니라 사용자 정정에 따른 이번 추가다. |
| `context/project/README.md`, `MAINTENANCE.md`, `REFERENCE/` | 내용 층, 읽기·구성·갱신 책임을 구별한다. 기존 demo에서 빠졌던 layer 진입과 관리·읽기 기준을 채웠다. |
| `context/project/common`, `current`, `guidance`, `decisions` | 제품 의미·현재 구현·개발 계약과 선택 근거를 구별한다. 모든 층을 순차로 읽거나 주제마다 세 본문을 강제하지 않는다. |
| `context/work/workspaces/README.md`, `spec-and-tickets/` | current/memory와 current/state, source·output·records 관계를 확인했다. Spec 다섯 파일·Ticket 본문·선택한 Project·전체 state를 실제 내용으로 구성했다. |
| `context/work/workspaces/002-code-readability-refactoring`, `003-bug-investigation-and-fixes` | 실제 README·memory·Project 선택·Spec·Ticket·source·output 배치와 machine 계약을 대조했다. demo의 평면 ticket/state 구조를 대체했다. |
| `context/work/AGENTS.md`, `README.md` | 실제 Noline에는 Harness와 session 운영이 있다. 이번 demo에는 자동 실행기를 설치하지 않으며 존재하지 않는 runtime·기계 검증 결과를 꾸며 넣지 않는다. |

실제 Project README는 “common/current/guidance는 필수 물리 경계”라고 정의하고, Work collection은 current/memory가 Spec 다섯 파일·Ticket·Project 선택을 소유하고 current/state가 전체 상황·다음 행동을 소유한다고 정의한다. 직전 demo는 파일·동작 검사를 통과했어도 이 책임과 계층을 충분히 반영하지 못했다. 링크·검사 수만으로 적용 구조의 적절성을 확인했다고 판단한 것이 잘못이었다.

## 실제 수정

같은 [development-workflow](prototypes/development-workflow/README.md) 폴더를 수정했다. 날짜별 새 현재 prototype은 만들지 않았다.

- 개인 본문은 `noline-demo/context/personal/`로 옮겼다. 내용의 조건부 적용·원래 대화·사례·새 문장의 지위는 보존했다.
- 별도 `ai-workspace/` 모형과 바깥 `workflow/`를 현재 구성에서 없앴다. 입력 선택·전달·반환 절차는 `context/work/DEVELOPMENT.md`가 맡는다. 실제 Noline 기존 skill이라고 표시하지 않는다.
- Project의 layer README·MAINTENANCE·REFERENCE·decisions 진입을 실제 책임에 맞춰 채웠다. 실제 Noline의 전체 domain을 옮긴 것은 아니며 인증 예제 범위의 본문을 유지한다.
- Work를 `001-login-completion-names`로 두고 memory/spec 다섯 관점, memory/tickets, Project·Personal의 현재 선택, state, source, output, records를 채웠다. 원래 초기 입력은 source, 산출물은 실제 코드·검사를 가리키는 output으로 연결했다.
- 작은 실행 코드는 `examples/authentication/`에 뒀다. 실제 Noline의 apps/client·server·packages를 재현했다고 보이지 않게 예제의 역할을 드러낸다. 코드 동작은 바꾸지 않았다.
- 화면은 실제 폴더 트리로 시작하고 단계별 적용·본문 비교를 함께 제공한다. 원본 Markdown과 표시 사본은 계속 구별한다.

변경 전 파일 내용·경로·해시는 [기계 보존본](receipts/prototype-layout/2026-10-19-89-before.json)에 남겼다. 파생 viewer.html은 원문과 당시 생성 도구로 재생성할 수 있으므로 별도 복제하지 않았다. 기존 날짜별 prototype와81~87 기록·source는 변경하지 않았다.88은 당시 판단으로 유지하며 옮긴 파일의 링크만 현재 재접근 위치에 맞췄다.

## 확인 범위

이동 뒤 Main이 현재 경로에서 Node 검사7개, 정상 demo, 조회 실패 demo를 직접 실행해 모두 성공 종료를 확인했다. 실제 입력·본문·산출물 경로와 남은 범위는 [Work의 후속 확인](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/records/2026-10-19-05-context-layout-check.md)에 남긴다. 이전 검토자의 기록은 당시 내용·동작 확인이며 이번 구조를 수락했다는 증거가 아니다.

화면을 재생성하고 문서48개·소스와 검사5개의 전체 원문·SHA 일치를 확인했다. 화면 안쪽 연결206곳·바깥 원문 연결23곳·제목 연결10곳, 잘못된 링크 형식12종의 거부와 스크립트 문법을 정적으로 확인했다. Workspace current·관련 안내·현재 prototype의 파일 연결890곳에도 누락이 없었다. 브라우저 렌더링·실제품 통합·사용자 수락을 확인한 것으로 보고하지 않는다. 실제 Noline, 바깥 운영 context, 글로벌 기준·skill·hook은 변경하지 않았으며 커밋하지 않는다.

직접 읽은 주요 Noline 문서의 경로·SHA-256은 [관찰 기준](receipts/prototype-layout/2026-10-19-89-noline-basis.json)에 남겼다. 해시는 구조 판단의 근거 범위를 식별하며 의미 검토를 대신하지 않는다.

예제 코드·검사5파일은 재배치 전과 내용이 같고, 보존된 이전 날짜별 적용 시안20파일과 직접 관찰한 Noline 주요 문서15파일의 해시도 같았다. Noline의 HEAD와 기존 untracked 두 경로 상태는 조사 전후 같았다. Project 본문에 Personal 직접 문서 의존이 없고, 이전 ai-workspace·외부 workflow 모형이 현재 prototype에 남아 있지 않음을 확인했다. 이 결과는 구조·본문·예제 범위의 확인이며 실제 운영 효과를 대신하지 않는다.
