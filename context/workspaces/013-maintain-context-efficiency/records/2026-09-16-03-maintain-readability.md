# Maintain 가독성 후속 정리

사용자는 책임 분리 뒤에도 코드의 개행과 읽는 흐름이 부족하다고 지적했고, LLM용 영문 메시지·프롬프트 바로 아래에 한국어 번역 주석을 요청했다.

Reference Maintain의 import 그룹, 모듈·클래스·메서드 간격, 긴 생성자·호출·조건식과 상태 상수의 간격을 정리했다. 짧은 표현은 불필요하게 나뉜 줄을 합쳤다. 공통 `testing.py`는 import와 클래스 속성 사이의 빈 줄만 정리했다. 이름·책임 경계·테스트 assertion은 바꾸지 않았다.

`semantic/prompt.py`의 초기 맥락 정립·응답 종료 판단·공통 권한 제한과 runtime 및 Codex/Claude hook의 알림문에 의미 단위별 한국어 번역 주석을 붙였다. 영문 문자열은 그대로이고 번역은 LLM에 전달되지 않는다. JSON 필드·태그·일반 오류 문자열까지 일률적으로 번역하지 않았다.

루트 `CODE-QUALITY.md`에도 읽는 흐름의 정리와 영문 LLM 문자열 아래 번역 주석 기준을 반영했다. 기존 AGENTS 연결과 CLAUDE symlink를 그대로 사용한다. 전역 사용자 지침은 수정하지 않았다.

## 검증

수정 전후 Maintain Python 파일 59개와 공통 `testing.py`의 AST를 비교해 실행 구문·문자열·이름이 동일함을 확인했다. `git diff --check`도 통과했다.

`reference-project/`에서 다음 Maintain 검사를 Python 3.14.3과 3.11.15로 실행했고 각각 82개가 통과했다.

```bash
python3 -B -m unittest discover -s context/work/harness/maintain/tests -t . -p 'test_*.py'
```

Python 3.11은 현재 pyenv 기본 선택에 포함되지 않아 shim으로 호출할 수 없었으며 설치된 3.11.15 실행 파일로 검증했다. 프로젝트 Python 설정은 변경하지 않았다.

Python 3.14의 전체 회귀 141개 중 140개가 통과했다. 기존 기록에서 변경 전에도 실패했던 Verify의 `test_timeout_covers_descendant_after_group_leader_exits` 한 건이 다시 실패했다. 전체 통과로 기록하지 않으며 Recover·Verify 내부 수정은 여전히 후속 범위다.
