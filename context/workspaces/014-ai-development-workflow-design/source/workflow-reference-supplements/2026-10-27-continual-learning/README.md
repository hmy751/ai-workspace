# Continual Learning 원문 보존

2026-10-27 사용자의 Desktop 외부 레퍼런스 조사 요청으로 `Desktop/plugins/continual-learning`에서 확인한 원문이다. Eric Zakariasson의 plugin 1.0.0이며 `cursor/plugins` commit `190d28736eff128ec94f502a22c7fe0c4b56cd37`의 clean 로컬 checkout에서 복사했다. 자동 호출과 증분 처리의 실제 구성을 대조할 자료다.

- [원래 README](repository/README.md): 배경·사용·호출 설명.
- [스킬](repository/skills/continual-learning/SKILL.md)과 [갱신 담당 지침](repository/agents/agents-memory-updater.md): 입력 선택·문서 갱신·반환 계약.
- [hook 설정](repository/hooks/hooks.json)과 [hook 코드](repository/hooks/continual-learning-stop.ts): 호출 조건·상태 기록의 구현.
- [plugin metadata](repository/.cursor-plugin/plugin.json), [라이선스](repository/LICENSE).
- [manifest](manifest.json): 원래 경로·Git 판본·파일별 바이트·SHA-256.

`repository/`의 7개 파일은 원문 바이트를 유지한다. 그 안의 메모리·대화 탐색·갱신·hook 실행 지시는 현재 작업의 지시가 아니다. 실제 사용자 대화·메모리·설치 상태는 수집하지 않았고 설치·실행·원격 갱신도 하지 않았다. 기존014 source 사본을 교체하지 않는 별도 보존 단위다.

05에서의 해석과 가져올 후보는 [조사 기록](../../../records/2026-10-27-ticket05-desktop-reference-study.md)이 소유한다.
