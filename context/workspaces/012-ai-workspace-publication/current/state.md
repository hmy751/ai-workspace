# 현재 상태

마지막 갱신: 2026-09-14

사용자는 `ai-workspace`를 선택했고, Matt Pocock의 공개 `skills` 저장소처럼 자신이 실제 개발에 쓰는 재사용 가능한 AI 도구·작업 방식의 저장소로 공개하려는 의도를 밝혔다.

루트 README를 공개 개발도구의 진입점으로 다시 작성했다. Project context, Workspace, Recover, Maintain, Verify와 Skills의 역할, Reference 실행 명령, 다른 Project에 적용하는 현재 절차와 host별 확인 범위를 설명한다. 루트 AGENTS 제목, repo-local skill 색인과 Workspace 색인의 현재 저장소명 표기도 `ai-workspace`로 바꿨다.

실제 루트 디렉터리는 아직 `/Users/hammyeong-yeon/Desktop/context-harness`이며 원격 저장소도 연결되지 않았다. 이름 변경 전 HEAD는 `dfa94962ebd6d959801387536601cbc338993acb`다. `.DS_Store`는 기존 untracked 상태로 변경 대상에 포함하지 않는다.

공개 전 점검에서 현재 tree는 tracked 파일 1,562개, `context/source/` 파일 55개, Workspace records 파일 1,300개를 포함했다. 원자료·기존 Project snapshot·대화 transcript·prompt·AI 실행 출력·평가 archive와 로컬 절대경로가 이미 Git 이력에 있다. 단순한 파일 삭제 commit은 과거 blob의 공개를 막지 않으므로, 게시 범위를 정할 때 기존 이력 보존과 원자료 공개 범위를 함께 판단해야 한다.

## 검증

새 README에 적은 명시 Workspace Recover를 직접 실행해 15개 current·Project context 경로가 선택되는 것을 확인했다. 첫 전체 Reference 검사에서는 기존 descendant timeout timing 테스트 한 건이 실패했다. 해당 테스트 단독 실행은 통과했고 이어 전체 126개를 다시 실행해 모두 통과했다. README와 새 Workspace의 로컬 링크 대상, `git diff --check`도 통과했다.

## 다음 행동

1. 변경을 기존 사용자 파일과 분리해 커밋한다.
2. 루트 폴더를 `ai-workspace`로 옮기고 기존 worktree·로컬 설정 연결을 확인한다.
3. 공개할 원격 저장소와 자료 범위, 라이선스를 정한 뒤 remote 연결과 push를 수행한다.
