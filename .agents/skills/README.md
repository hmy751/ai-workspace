# Repo-local skills

이 디렉터리는 `context-harness` 저장소에서 반복할 작업 절차를 Codex가 명시 호출하거나 설명 기반으로 선택할 수 있게 하는 repo-local skill 경계다.

- [`apply-context-harness/`](apply-context-harness/): `output/`의 실행 가능한 책임을 대상 Project의 기존 canonical과 사용자 변경을 보존하며 이식하고, recover·verify·receipt·재진입까지 검증한다.

`output/`은 실행 원형, `.agents/skills/`는 원형을 다른 Project에 적용하는 절차, `context/workspaces/`는 실제 적용 과정과 결과 기록을 소유한다. 같은 내용이나 target 산출물을 skill assets로 복제하지 않는다.

위치는 2026-08-14 확인한 [OpenAI Build skills 문서](https://learn.chatgpt.com/docs/build-skills)의 repository scope 검색 경로인 `$REPO_ROOT/.agents/skills`를 따른다. 다른 저장소에 일반 배포할 시점이 오면 여기서 바로 전역 복사하지 말고 plugin 또는 별도 승인된 배포 경계를 다시 판단한다.
