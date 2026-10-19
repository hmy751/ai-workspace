# 개인 기준·Project·한 작업을 실제 배치와 장면으로 구체화

> 후속 정정: 이 기록에서 전제로 둔 ai-workspace 내부 Personal 위치와 Project의 개인 기준 직접 참조는 [84](2026-10-19-84-personal-project-ownership-and-format-correction.md)에서 최신 사용자 정정에 따라 대체했다. 아래는 당시 판단·작성·확인 이력으로 보존한다.

2026-10-19. 사용자는 [82의 세 본문 비교](2026-10-19-82-naming-responsibility-completion-draft.md)를 본 뒤 다음과 같이 요청했다.

> 좀 더 구체적으로 보고 싶어 context/workspaces/014-ai-development-workflow-design/records/prototypes/applied-criteria-2026-10-17 이것 처럼

앞선82는 개인 본문·Project 가이드·읽기 안내를 별도로 작성하고 대조했다. 이번 요청은 [기존 적용 시안](prototypes/applied-criteria-2026-10-17/README.md)처럼 문서가 놓인 배치와 실제 의뢰·읽기·판단·변경·검토·남는 기록까지 구체적으로 보려는 것으로 해석했다. 기존 파일을 옮기거나 합치지 않는 제약은 유지했다.

## 새로 만든 비교 실물

[새 시안 입구](prototypes/personal-project-applied-2026-10-19/README.md)에서 개인 기준을 가진 작업대와 이를 채택한 가상 noline-demo Project, 로그인 완료 표현을 정리하는 한 Work를 연다. [단계별 화면](prototypes/personal-project-applied-2026-10-19/viewer.html)은 실제 Markdown의 표시 사본이고 본문 정본은 각 Markdown이다.

- 개인 정본 위치를 보여 주는 `ai-workspace/context/personal/development/naming-and-completion.md`에 일반 기준을 둔다.
- Project의 `guidance/code-readability.md`가 개인 원문을 실제 상대 링크로 참조하면서 적용 범위·인증에서의 구별을 설명한다.
- Project README는 읽기 안내, common은 기기 세션의 제품 의미, 인증 guidance는 개발 계약, current는 실제로 배치한 가상 함수·사용처의 연결과 근거 범위를 각각 맡는다.
- Work는 Ticket·현재 상태·구현 기록·검토 기록을 갖는다. 같은 요구를 역할마다 별도 정본으로 만들지 않고 Main의 채팅 의뢰로 구현·검토 역할을 전달한다.
- [작업 장면](prototypes/personal-project-applied-2026-10-19/walkthrough.md)은 이름과 callback을 바꾸는 판단, 구현 후 남은 과장 문구를 검토자가 직접 고치는 예시, 유지할 기준과 바꿀 현황·Work 기록을 연결한다.

운영 Personal context를 설치한 것이 아니라 records 아래에서 배치까지 보여 주는 시안이다. 앞선82와 기존 적용 시안은 이력·비교 대상으로 유지하며, 현재 구체 예시는83을 통해 찾는다. 개인 기준 원문이 이 가상 Project 안에 또 하나의 독립 정본으로 복제되지는 않는다. 서로 다른 시안에 있는 본문은 판본 비교 자료다.

## 근거 있는 계약과 장면을 위한 가정

인증 저장·상태 적용 이후 Query 실패를 인증 저장 실패로 재분류하지 않는다는 계약, Store의 일부 책임과 전체 세션 조율의 구별은 Noline 보존 문서가 지지한다. 원자료 경로와 구별은 새 시안 README에 있다.

로그인 서비스가 정확히 어디서 해소되는지, wrapper가 Query 재조회를 기다리지 않는지, 내부 사용처가 두 곳인지, 실제 함수명이 무엇인지는 기존 자료에서 확인한 사실이 아니다. 이 내용은 가상 장면의 입력으로 명시했다. 함수·callback의 변경 이름과 완료 문구도 설명용 선택이다. 예시의 비대기 선택을 실제 Noline 정책이나 개인 기준의 일반 규칙으로 올리지 않는다.

Project current가 작업 후에도 이전 이름을 현재값으로 보유하지 않도록, [시작 입력](prototypes/personal-project-applied-2026-10-19/scenario-input.md)과 [작업 후 현황](prototypes/personal-project-applied-2026-10-19/noline-demo/context/project/current/authentication-flow.md)을 구별했다. walkthrough의 초기 읽기는 시작 입력을 사용하며 사후 결과를 처음부터 알고 판단한 것으로 쓰지 않는다.

실제 제품 코드·검사를 만들거나 실행한 작업이 아니다. 문서 속 완료·확인 계획·예상 결과는 가상 작업의 상태이며 실제 제품 통과 증거를 대신하지 않는다. 별도 스킬·Harness 구현, 실제 Noline 이식, 기존 가이드 이동·통합, 최종 개인 기준 채택은 하지 않았다.

## 이어서 볼 판단

개인 기준이 실제 이름 선택에 어떤 판단을 보태는지, Project가 자신의 계약·적용을 이해할 만큼 충분한지, Work에 남을 결과가 Project·개인 기준으로 과잉 전파되지 않는지 구체 장면으로 검토한다. 단계·문서 수·역할 메시지 형식 자체는 최종 운영안으로 채택하지 않는다. 관련01-02·03·04-03·06의 미완료와 사용자 수용 유보는 유지한다.

## 작성 중 대조와 보완

별도 검토자는 초기 입력과 walkthrough의 Query 인자, 시작 시점·사후 Project 현황을 대조했다. 진행 중인 문서 맞춤이 끝난 뒤 모든 발췌가 `session-data` Query 범위를 유지하고 처음 입력과 사후 현황을 구별한다고 다시 확인했다. 이름만 바꾸는 장면에 무효화 범위 변경이 섞이지 않도록 했다.

사용자 화면의 최종 문구로 처음에는 ‘인증 적용 완료 · 조회 갱신 요청’을 제안했으나, 검토자는 개발용 처리 단계를 제품 사용자에게 노출할 필요가 없다고 지적했다. Main은 이를 수용해 최종 사용자 문구를 ‘로그인 완료’로 좁혔다. 함수·callback·개발 가이드는 상세 책임을 드러내고 사용자 안내는 사용자에게 필요한 성공을 과장 없이 전달한다. 이 보완을 새로운 전역 기준 설치로 확대하지 않았다.

최종 Markdown 재확인에서 검토자는 Query 범위 일치, 초기 입력·사후 현황의 구별, 최종 사용자 문구와 초기 구현 기록의 보존을 확인했다. 개인 기준·Project의 채택/제품 계약·Work의 선택/검토/확인 계획을 복원할 수 있었고, 실제 Noline 대기 동작과 추가 가정·예상 검사와 실제 실행이 섞이지 않았다고 보고했다. 확인한 범위에서 남은 수정 필요점은 찾지 못했다. 이는 문서 검토이며 제품 수행과 실제 사용 효과 검증이 아니다.

Main은 새 시안의 Markdown18개, 앞선82 시안과 진입점 변경을 포함한 미커밋 Markdown33개의 로컬 링크 대상521곳에서 누락이 없음을 확인했다. 변경은014 내부의 새 시안·기록과 현재 안내에 한정하며 기존 source·applied-criteria 시안은 변경하지 않았고 운영 `context/personal/`도 생성하지 않았다. 이번에도 stage·commit은 하지 않았다.

열람 화면 담당자는 확정 Markdown18개와 viewer 내장 원문·SHA-256의 일치를 확인했고 스크립트 구문 검사를 통과했다. 설치된 Chrome에서 로컬 파일을 열어1440×1050·390×844 크기로6단계·18문서 선택·세 본문 비교·원문 표시를 확인했다. 모바일 가로 넘침, pageerror와 HTTP 요청은 없었다. Main도 세 본문 비교 화면을 확인했다. 이 검사는 보조 열람 화면의 동작·원문 표시 검증이며 가상 제품 장면의 실행 검증이 아니다. `git diff --check`도 통과했다.
