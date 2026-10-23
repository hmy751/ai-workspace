# 읽기 기록

- `prompt.txt`, `README.md`, `inventory.json`을 이 실행 디렉터리에서 확인했다. `README.md`는 이후 `read_material.py`로도 전문을 읽었다.
- 질문 조사 전에 `skill/SKILL.md` 2/2조각과 `shared/explanation-and-evidence-criteria.md` 1/1조각을 전문으로 읽고 적용했다.
- `inventory.json`의 `required_text_files` 60개, 총 108조각을 `read_material.py`로 모두 읽었다. 각 조각은 별도의 `tools.exec_command`와 `functions.exec` 호출로 출력했고 모든 출력에서 `END OF CHUNK`를 확인했다. 출력 잘림과 조각 누락은 없었다. `read-events.jsonl`과 inventory를 대조한 누락 목록도 비어 있었다.
- 디렉터리 밖 자료·상위 Workspace·다른 실행 폴더·외부 저장소·웹에 접근하지 않았다. 제품 실행·수정·시험 및 추가 서브 호출은 하지 않았다.
- 제공 자료의 공백: 일부 변경 테스트와 `.claude/context/activation-system.md`, `.claude/context/selective-activation-architecture.md`의 본문은 제공되지 않았다. 자동 검사 출력과 과거 앱 관찰은 제공된 기록으로만 확인했으며, 마지막 보완 뒤 실앱 재검증·실제 통신 단절은 기록되지 않았다. 제공 snapshot은 전체 당시 dirty tree나 현재 제품 working tree가 아니다.
