# Project 본문 구성·읽기 계약 후속 역반영

날짜: 2026-09-14

## 확인한 변화

Source의 앞선 Project Owner 이동 보완 commit `7040d1c516ac3b7184e00125a691cb623f5ea231` 이후 Noline의 다음 commit을 순서대로 대조했다.

- `26350d6b04763f8276314187087f8c0d6d45ea27`: 앞선 source 계약의 Noline 적용
- `3baa7b701a3f3eec5f2f1a27081a50212036e75c`: Project 구성 기준·읽기 기준·읽기 skill 도입
- `2937c252a735ecc6edbe1d3516659fcf459da970`: 대표 작업과 본문 자체로 확인하는 읽기 검증 보강
- `0e7b4bfb2fba9c6014b911d54fba5dd274c7ff3f`, `2a3ca27e30bf0d2b9872b7953d3893ddd7c8173a`: Workspace 002 수락과 열린 제품 판단의 Workspace 004 분리
- `33bde333bdd6168e6dc8bc0621e17bf432320b79`: 제품 본문·기존 진입점·의미와 사실 범위의 최종 보완
- `30deac5fc7aa97a5eae4d41b9c6aa7d2ca2e9531`: Workspace 004 session 상태 마감

사용자 정정에서 재사용할 핵심은 세 가지다. `common/current/guidance` 물리 폴더는 선택 사항으로 두었을 때 빠지는 문제를 막기 위해 의도적으로 요구한 경계다. Guidance는 조건부 조언이나 순서가 아니라 계약·이유·구체적인 적용과 검증을 포함하는 작업 가이드다. 이번 반영은 Workspace 002의 일부 완료 결과와 관련된 범위이며 Noline 제품 본문 전체 개편을 source에 복제하는 작업이 아니다.

## 공통 계약으로 채택한 내용

- 세 물리 층은 유지하지만 작업·주제의 질문에서 실제 본문으로 들어간다. 층은 모든 작업의 읽기 순서나 모든 주제의 파일 수가 아니다.
- Ticket·기록·검증 묶음은 근거이며 본문 구조가 아니다. 다음 관련 작업이 반복해서 물을 질문과 온전한 의미로 구성하고 주 책임 층을 고른다.
- `guidance`는 계약·이유·판단·적용·검증을 소유할 수 있다. 모든 가이드에 같은 고정 목차를 요구하지 않는다.
- `current`는 가이드와 코드를 읽은 뒤 추가로 바꾸는 판단과 재확인 신호가 있을 때 독립된 가치가 있다. 그 관계가 없는 테스트 수치·도구 오류·미실행은 Work 기록에 둔다.
- 쓰기 전에 보존할 기존 의미, 직접 확인할 사실과 구현 경계, 열린 제품 선택, 영향받는 실제 진입점을 대조 기준으로 잡는다. 쓰기 뒤에는 의미 보존, 문장과 근거 경계의 일치, Project README와 대표 기존 작업 진입점이 같은 Owner에 도달하는지를 따로 확인한다.
- Project 구성과 읽기는 제품 내용층이 아닌 `context/project/REFERENCE/`가 소유한다. `read-project-context`는 필요한 본문을 고르고 적용하는 읽기 전용 절차이며 Recover·Maintain·문서 갱신을 대신하지 않는다.

## 가져오지 않은 것

Noline의 통화·날짜·API·도시 검색·저장 용량·리팩터링 같은 제품 계약과 Workspace 002·004의 상태·Ticket·검증 수치는 source sample에 옮기지 않았다. 제품별 열린 선택도 source의 request-policy 예제로 일반화하지 않았다.

`0e7b4b`, `2a3ca27` 시점에는 Workspace 소비 문서가 새 Project 제품 문서를 참조했지만 해당 본문은 Git tree에 아직 없었고 `33bde33`에서 함께 들어왔다. 이 불완전한 중간 상태는 공통 패턴으로 채택하지 않았다. Source 이식 계약에는 producer 본문과 consumer routing을 하나의 일관된 변경 단위에서 처리한다는 기준을 남겼다.

## Source 반영

- Reference Project에 `context/project/REFERENCE/{README.md,composition.md,reading.md}`를 추가했다.
- Project README를 layer-first 목록에서 작업·주제별 진입으로 바꾸고, MAINTENANCE와 층별 README의 구성·완료 기준을 맞췄다.
- `.agents/skills/read-project-context/`를 추가하고 Claude·Codex가 같은 원본을 읽도록 상대 bridge를 연결했다.
- `update-project-context`에 쓰기 전 대조 기준, 의미·사실 범위·실제 진입점의 쓰기 후 확인을 반영했다.
- Root instruction·Reference README·skill 색인을 새 읽기 경로에 맞췄다.
- `apply-context-harness`와 application contract가 Project REFERENCE·읽기 skill을 설치·적응하고 대표 작업으로 의미·routing을 확인하도록 갱신했다.
- Workspace 생성 계약·skill과 현재 sample Workspace의 Project 선택 설명을 주제별 읽기 경로에 맞췄다.

## 검증과 증명 상한

`git diff --check`가 통과했다. 변경 Markdown 24개의 local link 258개는 lexical target과 실제 존재를 확인했고 끊어진 링크가 없었다. 새 `read-project-context`의 Claude·Codex 상대 symlink는 모두 `.agents/skills/read-project-context`의 같은 원본으로 해석됐다.

공식 `quick_validate.py`는 환경에 PyYAML이 없어 세 대상 모두 import 단계에서 중단했다. 제공 검사기의 frontmatter key·이름·설명 제한과 `agents/openai.yaml`의 `$skill-name` prompt 조건을 Ruby YAML로 대체 확인했고, 최종 변경된 `create-context-workspace`, `read-project-context`, `update-project-context`, `apply-context-harness` 네 skill이 통과했다. 이는 실제 host discovery나 invocation이 아니다.

Reference Project에서 기본 Recover와 `001-default-timeout` 명시 Recover가 모두 성공했다. 두 경로는 `context/project/README.md`, `common/prd.md`, `current/architecture.md`, `decisions/0001-default-timeout.md`만 Project context로 읽고 `MAINTENANCE.md`와 `REFERENCE/`를 기본 packet에 추가하지 않았다.

첫 전체 `python3 -m unittest discover -s . -p 'test_*.py' -q`에서는 기존 `test_timeout_covers_descendant_after_group_leader_exits`가 timing 조건에서 한 번 실패했다. 해당 test 단독 재실행은 통과했고, 그 뒤 전체 126개 재실행과 최종 문서·consumer 보완 뒤 전체 126개 재실행이 모두 통과했다. 제품 Verify는 실행하지 않았고 sample의 기존 durable receipt freshness도 갱신하지 않았다.

이 검증은 구조·link·skill 형식·Recover 선택·Reference 회귀를 확인한다. 새 target의 실제 이식 효과나 host의 자동 skill 발견·호출·본문 적용을 증명하지 않는다.

Noline의 지침 격리 재시험 한 번은 기존 의미 누락, 사실 범위 확대, 기존 진입점 누락, 판단 효용 없는 current 실행 이력의 네 문제를 개선했다. 그러나 뒤의 별도 실제 제품 본문 구성에서도 같은 종류의 문제가 다시 드러나 Main 수정이 필요했다. 따라서 이 source 반영은 확인된 계약 공백을 닫은 것이며 독립 실행 효과는 잠정적으로 남긴다. 같은 실패가 반복되면 문구를 더 추가하기보다 검증 배치와 독립성 필요를 다시 판단한다.
