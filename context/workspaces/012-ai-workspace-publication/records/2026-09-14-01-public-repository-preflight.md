# 공개 저장소 전환 전 자료 점검

날짜: 2026-09-14

## 확인 목적

기존 커밋 이력을 유지해 `ai-workspace`를 공개하기 전에, 현재 Git tree와 이력에 공개 범위를 별도로 판단해야 할 자료가 있는지 확인했다. 이 점검은 민감 자료를 자동 판정하거나 삭제하기 위한 작업이 아니다.

## 현재 Git 상태

- branch: `main`
- 기준 HEAD: `dfa94962ebd6d959801387536601cbc338993acb`
- remote: 없음
- 기존 untracked: `.DS_Store`
- tracked 파일: 1,562개
- Git object loose size: 약 26.77 MiB
- `context/source/` tracked 파일: 55개
- `context/workspaces/**/records/` tracked 파일: 1,300개

## 공개 범위를 판단할 자료

- `context/source/`에는 사용자 제공 원문, 이전 대화 transcript, 외부 페이지 원본 HTML과 과거 Project snapshot이 있다.
- Workspace records에는 prompt, AI 실행 stdout, 평가용 fixture·snapshot·hash 목록과 실제 적용 과정이 있다.
- 현재 tree에서 로컬 절대경로가 들어간 tracked 파일은 records와 source를 포함해 150개였다. records와 source를 제외한 현재 진입 문서에도 다른 Project의 로컬 경로를 가리키는 파일이 있다.
- 가장 큰 tracked 파일은 Maintain 평가 baseline archive이며 약 11.7 MiB다.
- 파일명과 대표적인 credential 문자열 패턴을 확인한 범위에서는 명시적인 `.env`, private key 또는 전형적인 access token 파일을 발견하지 않았다. 이는 모든 민감 정보가 없다는 보장은 아니다.
- Git author 이름과 이메일은 기존 commit metadata에 포함된다.

## 이력 보존과의 관계

새 commit에서 파일을 제거하거나 경로를 고쳐도 이전 commit의 blob과 commit metadata는 원격에 함께 게시된다. 기존 commit hash를 그대로 보존하면서 일부 과거 blob만 제외할 수는 없다. 원자료 전체를 공개하지 않기로 하면 원본 저장소를 별도로 보존하고 공개용 이력을 재작성하거나, 공개할 모듈을 새 저장소로 분리하는 선택이 필요하다.

현재 단계에서는 어떤 파일도 삭제하거나 이력을 다시 쓰지 않았다.
