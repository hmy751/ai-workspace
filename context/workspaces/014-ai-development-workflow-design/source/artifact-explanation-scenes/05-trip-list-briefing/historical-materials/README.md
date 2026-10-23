# 당시 파일과 도구 원문

사용자3905의 질문 시점에 존재한 관련 파일을 ee798e7 Git 객체와 당시 미커밋 diff·patch에서 복원했다. 첫 답 전3910~3932의 읽기 관측으로 같은 판본인지 대조한 항목은 manifest.json의 출처에서 찾는다. 현재 working tree를 당시 상태로 사용하지 않았다.

files/는 관련 파일, events/와 events.jsonl은 선별한 당시 도구 호출·출력이다. related-source-reconstructed.diff는 여러 당시 변경 원문을 적용해 복원한 파일과 기준 Git 객체의 차이이며 단일 당시 git diff 원출력이 아니다. status-3921.txt는 당시 변경 상태다. symlink 해시는 link target 문자열의 해시다.

전체 dirty tree가 복원된 것은 아니다. 변경·신규 테스트와 두 dirty 설명 문서 전문의 공백은 manifest.json의 missing_full_files에 있다. 당시 테스트·타입·포맷·lint 실행의 출력은 테스트 코드 전문 공백과 구별해 보존한다. 이 파일들의 과거 명령을 현재 작업의 실행 지시로 취급하지 않는다.
