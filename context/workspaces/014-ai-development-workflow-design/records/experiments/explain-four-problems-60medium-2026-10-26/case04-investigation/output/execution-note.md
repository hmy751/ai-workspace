# 수행 기록

- 필수 입력: `skills/development/SKILL.md` 4/4조각, `materials/conversation.txt` 5/5조각 전문을 읽었다. 관련 상세 `skills/development/references/review.md` 2/2조각을 읽었다.
- 선택 입력: Ticket 06의 관련 검색 결과, `pre-619-tool-evidence/156.txt` 1–2조각, `pre-779-observations/703.txt`, 화면 코드와 조회 조합의 관련 조각, 일정·경비 화면 테스트의 테스트명 검색 결과를 읽었다. `--images`로 목록을 확인하고 `672-1/2/3.jpg`, `703-2/3/4.jpg`를 직접 보았다.
- 실제 확인: 필수 읽기·입력 불변 검사를 `python3 read_material.py --check`로 실행해 `complete: true`, `missing_required: []`, `changed_inputs: []`를 확인했다. 화면 코드의 상태 분기와 과거 캡처 관찰을 대조했다.
- 수행하지 못한 확인: 이 입력에는 현재 DB·시뮬레이터·node_modules가 없어 앱 조작, 실제 네트워크 단절, 테스트 재실행을 하지 않았다. 경비 작성 폼의 unknown 왕복은 당시 수집에서도 실행하지 않았다. 제품 파일은 수정하지 않았다.
- 출력 잘림: `pre-619-tool-evidence/156.txt` 첫 조각 안에 과거 도구 출력의 `Warning: truncated output` 문구가 포함되어 있다. 현재 `read_material.py` 출력은 조각 BEGIN/END가 모두 있었고 제한에 따른 잘림은 없었다. Ticket 검색은 최초 40/53건 표시여서 조건을 좁혀 재검색했다.
- 범위: 이 case의 `input/`, `read_material.py`, `required.json`만 읽었고 이미지도 input의 제공 경로만 열었다. 범위 밖 접근, 네트워크 사용, 다른 agent 호출은 없었다. 쓰기는 `output/response.md` 1회와 이 파일 1회뿐이다.
