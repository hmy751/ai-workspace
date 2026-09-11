# Noline 작성 지침·Maintainer 설정 적용과 커밋

2026-09-11 · Workspace 011

사용자가 “그래 커밋하고 이 작업한걸 noline에도 반영하자”라고 요청했다. Source를 커밋하고 이식 skill의 적용안을 제시한 뒤, 사용자는 “커밋해 니가 반영한 부분만”이라고 범위를 지정했다. Main은 공통 지침·Maintainer 설정을 Noline에 적용하고 해당 파일과 적용 기록만 커밋했다.

## 고정한 판본과 반영 범위

Source는 `5f6db35f82833704e3ffb0cc430fc9da98a4ac62`다. 작성 기준 분리·소비 경로, 단일 역할 설정을 읽는 실행 코드·테스트와 앞선 비교 시험 기록을 포함한다. `.DS_Store`와 평가 실행의 Python 캐시는 커밋에서 제외했다. 캐시는 디스크에 유지하고 평가 폴더 안에서 ignore했다.

Noline 적용 commit은 `309b9e6733e4322e70c65c7febeb381e0bcfe94a`, branch는 `refactor/codebase`다. 적용 직전 baseline은 다른 session의 테스트 기반 커밋이 반영된 `653f8b8`이었다. 첫 적용안의 이전 HEAD를 그대로 믿지 않고 preflight를 다시 생성했다.

공통 적용은 작성 지침·연결 문서·실행 설정과 테스트 9개 파일이다. 6개는 source와 바이트가 같으며, Work AGENTS·Maintain README·역할 설정 3개는 Noline 고유 역할 설명·Claude Code 연결·증거 수집 경로와 제품 검증 명령을 보존해 적응했다. 적용 Workspace의 상태·산출물 색인·새 기록과 receipt, Noline 지침이 요구하는 짧은 결정 기록까지 합쳐 16개 파일만 커밋했다. 상세와 실제 증거는 [Noline 적용 기록](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/001-noline-context-harness-application/records/2026-09-11-03-workspace-writing-and-maintainer-settings.md)이 소유한다.

Noline의 기존 코드·테스트·Workspace 002 문서는 다른 session에서 계속 바뀌었다. 따라서 preflight의 모든 hash가 최종까지 같다고 보고하지 않았다. 이번 patch와 commit은 그 경로를 포함하지 않았으며, 커밋 직전 staged 16개 경로를 확인하고 `git commit --only`에도 같은 경로를 명시했다. 완료 뒤 기존 제품 설정·Ticket·output·논의 기록의 변경과 새 테스트·`.pnpm-store/`가 별도로 남아 있음을 확인했다. 그 파일들을 되돌리거나 포함하지 않았고 push도 하지 않았다.

## 검증과 검토

Noline에서 Main이 Maintain 72개, 전체 Harness 재검사 124개, 직접 구조 검사와 변경 Markdown의 로컬 링크 123개를 확인했다. 첫 전체 검사에서는 기존 Verify descendant timeout 시험 한 건이 실패했고 단독 재실행은 통과했다. 같은 source 검사에서도 해당 실패가 있었으며 이번에 Verify 코드를 바꾸지 않았다. 통과한 전체 재검사는 실행 전 Python source 27개를 담는 별도 Harness receipt에 보존했다. Markdown·TOML까지 그 snapshot이 포함한다고 주장하지 않으며 source commit·target diff와 바이트 대조로 적용 판본을 구별했다.

최종 명시·기본 Recover는 같은 application Workspace의 context 15개를 읽었다. 새 작성 기준은 일반 Recover 선택을 늘리지 않고 작성 시점과 Maintainer prompt에서 사용한다. 기존 product Verify receipt는 stale이며 새 제품 검증·status 갱신은 수행하지 않았다.

이식 skill의 실행 변경 검토 기준에 따라 `noline_application_review`에게 read-only 검토를 맡겼다. 사용자 원문 두 발화, source commit, target baseline·실제 diff, 적용안과 fresh preflight를 입력으로 주고 제품 작업·private runtime·쓰기·activation은 제외했다. 검토자는 source/target 바이트, start/resume 설정 재읽기, 본문 단일 주입과 기존 권한·routing 보존을 직접 대조했고 도입된 P1/P2 결함은 발견하지 않았다. 테스트 실행은 Main 결과를 사용했다고 구별했다. Noline의 `decisions/` 기록 요구를 지적한 결과는 짧은 결정 기록 추가로 반영했다.

실제 Noline host의 모델 호출·hook trust·activation·response-end, 새 문서 품질과 자동 Guard 반영은 확인하지 않았다. 기존 binding·runtime·hook 설정은 변경하지 않았으며, Sol high와 작성 기준은 다음 Maintainer 호출부터 적용된다. 설치·단위 검사·커밋을 제품 acceptance나 전체 Workspace 완료로 보고하지 않는다.
