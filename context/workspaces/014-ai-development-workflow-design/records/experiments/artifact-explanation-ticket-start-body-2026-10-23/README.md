# Ticket 06 처음 파악 요청 — 기존·현재 브리핑 본문 비교

사용자는 보고서 작성보다 앞선 최초 Ticket 파악 요청에서 기존판과 수정판을 비교하도록 요청했다. GPT-6-sol medium 새 컨텍스트 두 개로 각1회 실행하며 이후 대화·교정·기대 답은 제공하지 않는다.

## 입력과 적용 시점

원 대화 source_line12의 질문 하나만 준다.

> context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/06-app-startup-lifecycle.md
>
> 여기 작업을 이어가려고해 파악해줘

질문을 받은 뒤 조사 시작에 briefing과 read-project-context를 명시 적용한다. 당시15의 두 스킬 적용 선언과16→19의 읽기 근거를 참고한 동일 배치다. 실제15 이후 응답·도구 읽기 목록은 입력에 포함하지 않는다. 양쪽에 같은 당시 저장소 전체 tracked snapshot을 주고 필요한 맥락·코드는 스스로 선택하게 한다. briefing만 바꾸며 다른 스킬·공통 기준은 동일하다.

- r23:0b3b167의 원 briefing.
- r76:현재 prototype의 briefing. 공통 기준 상대 링크만 snapshot의 기존 소유 경로로 조정했다. 형성 자료·현재 설계 논의는 제공하지 않는다.
- 저장소 원본은 [보존 archive](../../../source/artifact-explanation-scenes/01-report-delivery/repository/noline-0b3b167.tar.gz)이며 각input의 repository-manifest.json으로 실행 사본을 재구성·대조할 수 있다. 동일 archive를 실험 폴더에 중복하지 않는다.
- .git·설치 의존성·DB·시뮬레이터·비추적 보고서는 없다. 원 저장소나 웹을 추가 조회하지 않는다. 이번에 앱이나 검사를 재실행하지 않는다.

## 읽기·보존

실행자는 먼저 두 스킬 전문·질문·root 지침·대상 Ticket을 읽는다. 이후 필요한 파일을 선택하되 선택한 파일은4000문자 이하의 조각으로 끝까지 확인한다. 호출당 한 조각·출력8000토큰 이상을 지정하고 잘림이 생기면 보고한다. 전 파일951개를 전수 읽는 조건은 아니다.

[조건과 판본 해시](conditions.json)에 공통 입력·유일한 본문 차이를 보존했다. 완료 후 선택한 자료·조각 누락·입력 변경을 확인하고 최초 응답·읽기 기록·근거 사본을 보존한다. 이 비교는 최초 파악 응답의 본문 효과이며 네 보고서 작성의 실패 원인이나 자동 스킬 선택을 검증하지 않는다.

## 완료 결과

[두 응답과 Main 대조](comparison.md), [선택 파일·조각·출력 해시](results.json)에 실제 실행을 보존했다. 기존판29파일·51조각,수정판22파일·43조각을 확인했고 선택 파일 누락·입력 변경은 없었다. 두 응답은 현재 단계·다음 작업에서 대체로 같았으며 기존판의refresh 호출 범위 표현 오류를 별도로 기록했다.
