# pstack이 연결하는 코드 정리와 실행 확인 자료

pstack의 `poteto-mode`는 커밋 전 코드 정리에 `deslop`, 실제 화면·터미널 조작에 `control-ui`·`control-cli`를 연결한다. 같은 `Desktop/plugins` 클론의 **Cursor Team Kit**에서 이 세 본문과 연결된 `verify-this`를 보존했다. Eric Zakariasson의 별도 plugin이며 pstack이나 Lauren의 내부 도구와 동일한 자료가 아니다.

| 자료 | 읽을 내용 |
| --- | --- |
| [deslop](repository/skills/deslop/SKILL.md) | 변경 diff에서 불필요한 주석·방어 처리·타입 우회 등 검토 대상과 최소 수정 범위 |
| [control-ui](repository/skills/control-ui/SKILL.md) | 기존 프로젝트 도구를 우선 사용한 브라우저·Electron 조작, 관찰·증거 수집, 올바른 화면 선택 |
| [control-cli](repository/skills/control-cli/SKILL.md) | CLI·TUI의 재현 가능한 입력, 화면·transcript 관찰, 성능·메모리 확인 |
| [verify-this](repository/skills/verify-this/SKILL.md) | 반증 가능한 주장, 같은 조건의 변경 전후 근거, 확인·미확인·판정 불가의 구별 |

원래 연결은 [pstack 진입 본문](../pstack/repository/skills/poteto-mode/SKILL.md)에 있다. 제어 스킬이 사용하는 대상 앱·테스트 데이터·브라우저·PTY·런타임은 프로젝트와 실행 host의 자료이며 이 보존본에 설치하지 않았다. 예제 명령과 코드를 실행한 결과도 아니다.

## 판본과 보존 범위

2026-10-21 로컬 클론에서 파일 8개를 바이트 그대로 보존했다. 네 스킬 외에는 원 저장소 README·LICENSE·plugin metadata·로고를 포함한다. 원래 상대 경로는 `repository/` 아래 유지한다.

- 원본 경로: `/Users/hammyeong-yeon/Desktop/plugins/cursor-team-kit`
- 공개 저장소: [cursor/plugins](https://github.com/cursor/plugins)
- 로컬 plugin version: **1.2.0**
- Git commit: `190d28736eff128ec94f502a22c7fe0c4b56cd37`
- [파일별 manifest](manifest.json), [원 plugin 정보](repository/.cursor-plugin/plugin.json), [라이선스](repository/LICENSE)

다른 CI·PR·주간 회고·개별 리뷰 도구는 수집하지 않았다. 원 README의 해당 링크는 원문대로 남아 있다. 이 묶음은 pstack의 직접 참조를 확인할 연결 자료이며, Cursor Team Kit 전체를 사용하도록 선택한 결과가 아니다. 전체 자료 진입은 [상위 안내](../README.md)에서 찾는다.
