# 현재 상태

마지막 갱신: 2026-11-15

사용자는 `ai-workspace`를 선택했고, Matt Pocock의 공개 `skills` 저장소처럼 자신이 실제 개발에 쓰는 재사용 가능한 AI 도구·작업 방식의 저장소로 공개하려는 의도를 밝혔다.

루트 README를 공개 개발도구의 진입점으로 다시 작성했다. Project context, Workspace, Recover, Maintain, Verify와 Skills의 역할과 Reference 실행 명령을 설명한다. 사용자 정정에 따라 다른 Project 이식 안내와 현재 상태 섹션은 공개 진입점에서 제외했다. 루트 AGENTS 제목, repo-local skill 색인과 Workspace 색인의 현재 저장소명 표기도 `ai-workspace`로 바꿨다.

실제 루트 디렉터리는 `/Users/hammyeong-yeon/Desktop/ai-workspace`로 변경했다. 이름 변경 전 HEAD는 `dfa94962ebd6d959801387536601cbc338993acb`, 이름·공개 진입점의 첫 commit은 `8546023693c28f344fcb50dcde9abf3e87451a1c`, 공개 README 정정은 `00f0786fd8c610eb1363d7df670cee519bf2e9cf`다. `.DS_Store`는 기존 untracked 상태로 변경 대상에 포함하지 않았다.

GitHub 저장소 `https://github.com/hmy751/ai-workspace.git`을 `origin`으로 연결하고 기존 61개 commit을 포함한 `main`을 push했다. 로컬 `main`은 `origin/main`을 추적한다.

공개 전 점검에서 현재 tree는 tracked 파일 1,562개, `context/source/` 파일 55개, Workspace records 파일 1,300개를 포함했다. 원자료·기존 Project snapshot·대화 transcript·prompt·AI 실행 출력·평가 archive와 로컬 절대경로가 이미 Git 이력에 있다. 단순한 파일 삭제 commit은 과거 blob의 공개를 막지 않으므로, 게시 범위를 정할 때 기존 이력 보존과 원자료 공개 범위를 함께 판단해야 한다.

## 검증

새 README에 적은 명시 Workspace Recover를 직접 실행해 15개 current·Project context 경로가 선택되는 것을 확인했다. 첫 전체 Reference 검사에서는 기존 descendant timeout timing 테스트 한 건이 실패했다. 해당 테스트 단독 실행은 통과했고 이어 전체 126개를 다시 실행해 모두 통과했다. README와 새 Workspace의 로컬 링크 대상, `git diff --check`도 통과했다.

## 2026-11-15 루트 README 재구성

9월 15일 뼈대 위에 11월 4일 문장 교체만 얹혀 앞 절반은 설명문, 뒤 절반은 내부 변경 공지로 갈라져 있었다. 사용자는 독자를 개발자로, 기준을 "방식 이해 중심"으로 선택했고 이식 안내는 뒤쪽의 짧은 절로 두었다. 실제 적용 제품은 이름 없이 표현하기로 했다.

새 구성은 정의, 문제 장면, Personal·Project·Work 세 층, 작업 한 번의 흐름, 스킬 여덟 개, 직접 보기, 바꿔 온 것, 확인한 것과 아닌 것, 저장소 지도다. 실행기 세 개를 내린 이유와 잃은 보장은 014의 2026-10-30·2026-11-04 기록을 근거로 썼다.

확인: README 상대 링크 15개 존재, `reference-project`의 제품 검사 7개 통과, 기준 프로젝트 문서 링크 661개(records·`_background` 제외) 누락 없음. 처음 읽는 개발자가 실제로 이해하는지는 확인하지 않았다.

## 다음 행동

원격 게시까지 완료했다. 재사용 허용 범위를 명시할 필요가 생기면 공개 라이선스를 별도로 선택한다.
