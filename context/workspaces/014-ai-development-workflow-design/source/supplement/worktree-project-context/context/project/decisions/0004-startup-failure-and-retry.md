# 0004. DB 준비와 인증 복원 시도를 앱 진입 경계로 둔다

- 상태: 채택. 최초 인증 읽기 실패 처리와 Root 내부 배치는 후속 선택으로 구체화됐다.
- 결정 시점: 2026-09-18. Project 편입: 2026-09-25.
- 현재 기준: [앱 준비 가이드](../guidance/app-startup.md), [기기 세션](../common/device-session.md)
- 실제 적용: [현재 구조](../current/architecture.md), [세션과 로컬 데이터](../current/session-and-local-data.md)

## DB 실패를 진입 성공으로 다루지 않는다

SQLite와 보안 저장소는 별개다. 인증 정보를 복원할 수 있어도 여행 DB를 사용할 수 없으면 정상 앱 화면과 그 후속 작업을 시작할 수 없다. 사용자는 “실패 안내와 재시도 화면을 보여주고, DB 준비 성공 후 진입한다”를 선택했다.

DB 파일 열기·테이블 준비 실패는 Splash를 해제한 실패 안내와 재시도로 이어진다. 재시도는 저장된 여행·큐·인증을 삭제하는 reset이 아니다. 준비 성공 뒤 인증 복원 시도를 마치면 앱 진입을 판단한다. 네트워크 확정, 서버 토큰 검증, 로그인 후 여행 조회나 sync의 완료를 준비 조건에 추가하지 않는다.

## 인증 기록 부재와 복원 실패의 구체화

최초에는 보안 저장소 읽기 실패도 기존 로그인 화면으로 보내는 일반 흐름을 유지했다. 후속 세션 논의에서 기록 부재와 읽기·해석·계정 확인 실패를 다른 상태로 구분했다. 로그인 화면에 갈 수 있다는 UX는 유지하되, 후자는 `restore-failed`로 남겨 재시도·명시적 정리를 제공하고 자동 삭제하지 않는다. 과거의 “실패도 비인증으로 복원 완료”를 정상적인 `signed-out`과 같은 내부 상태로 구현하지 않는다.

초기 복원은 프로세스 시작과 실패 뒤 명시적 재시도에서 수행한다. 완료된 복원 Promise도 Store 수명 동안 유지한 이유는 로그인·로그아웃 뒤 초기 저장값이 다시 상태를 덮지 않게 하기 위해서다. 탭 이동·foreground·재렌더·토큰 갱신·재로그인마다 앱 전체 준비를 반복하지 않는다. ‘한 번’이라는 이름은 실패를 영구 고정한다는 뜻이 아니다.

## AppInitialization으로 준비 책임을 모은 이유

처음에는 layout 안에서 DB·인증 순서를 읽도록 정리했다. 사용자는 한 파일에서 읽는 것에 더해 초기화의 의미와 응집도를 요구했다. 앱 전체 준비를 `features/app-startup`에 두는 것은 feature 책임과 맞지 않았고, Expo의 `app/` 아래 일반 TSX는 route로 탐색될 수 있었다. 이후 사용자는 `application` 분리를 한정해 승인했다.

현재 배치는 `src/application/AppInitialization`에 준비 수명·네트워크 구독·DB와 인증 순서·실패·재시도·Splash를 함께 둔다. Root layout은 Provider·화면·인증 후 작업을 조립한다. `AppNavigation`은 화면과 인증 이동을, `AuthenticatedEffects`는 세션 동안의 작업 연결을 맡는다. 여행 선택·정리 실행의 상세는 각각 Entity·서비스에 남긴다.

이는 Noline의 이 책임에 맞춘 선택이다. 모든 내부 컴포넌트를 분리하거나 새로운 범용 FSD 계층·초기화 registry를 도입한 결정으로 확대하지 않는다. 준비 작업의 필수 여부나 수명이 바뀌면 [앱 준비 가이드](../guidance/app-startup.md)와 실제 호출 관계를 함께 검토한다.

## 근거와 대체 관계

[기존 앱 시작 결정](../../../.claude/decisions/2026-09-18-app-startup-failure-recovery.md)은 첫 구현부터 책임 변경까지의 이력과 당시 검사 범위를 보존한다. [초기화와 코드 표현 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-18-02-app-initialization-and-style.md)과 [기기 세션 논의](../../work/workspaces/002-code-readability-refactoring/records/2026-09-18-04-auth-session-policy-and-decisions.md)가 후속 선택의 근거다. 과거 검사 수치나 중간 종료 순서를 현재 코드의 전체 보장으로 읽지 않는다. 종료 조율과 sync 결과는 각각 [인증 가이드](../guidance/authentication-and-session.md), [동기화 현황](../current/sync-and-cleanup.md)에서 확인한다.
