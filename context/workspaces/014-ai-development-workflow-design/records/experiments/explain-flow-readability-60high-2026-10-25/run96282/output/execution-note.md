읽기: `prompt.txt`를 먼저 읽었다. 이후 지정된 `read_material.py`로 `skills/skill/SKILL.md` 3개 조각, `request.txt` 1개 조각, `code/config_loader.py` 1개 조각, `code/test_config_loader.py` 1개 조각을 각각 별도 호출로 모두 읽었다. 응답 전 `read_material.py --check` 결과는 `complete: true`, `missing: []`였다.

입력 공백: 응답에 필요한 질문·코드·테스트 사본이 제공되었고 확인된 공백은 없다.

잘림: 읽은 모든 조각에 BEGIN/END가 있었고 잘림 표시는 없었다.

경계: 지정된 실행 폴더 밖의 자료·평가·네트워크·다른 agent에 접근하지 않았다. 코드 수정이나 검사 실행은 하지 않았다.
