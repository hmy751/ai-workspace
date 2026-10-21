# 설명 작업 장면의 원자료 묶음

기존 source에서 선택한 대화의 연속 구간과 해당 시점의 Git 자료, 현재 남아 있는 관련 산출물을 보존한다. 기존 source 원본은 수정하지 않는다. 새 사건 요약이나 기대 답을 대화 대신 넣지 않는다. 문제 해석과 시험 설계는 이 폴더 밖의 [구성 기록](../../records/2026-10-21-ticket04-02-source-scene-assembly.md)이 맡는다.

현재 구성은 [01-report-delivery](01-report-delivery/README.md) 한 사건이다. 전체 source를 전수 조사한 결과나 모든 설명 문제를 대표하는 표본은 아니다.

| 자료 | 위치와 지위 |
| --- | --- |
| 요청이 확정된 시점까지의 연속 원문 | [input/conversation.txt](01-report-delivery/input/conversation.txt). 발화 구분자만 추가한 읽기본이며 [messages.jsonl](01-report-delivery/input/messages.jsonl)이 원래 레코드를 바이트 그대로 보존한다. |
| 그 뒤의 실제 작업·첫 결과·교정·후속 응답 | [evaluation/conversation.txt](01-report-delivery/evaluation/conversation.txt). 시험을 수행하는 주체에게 제공하지 않는 이후 원문이다. |
| 대화에서 보고한 HEAD의 저장소 | [repository](01-report-delivery/repository/README.md). Git 객체에서 추출한 전체 tracked 파일 압축본과 관련 작업 기록의 동일 바이트 읽기 사본이다. |
| 현재 발견한 보고서·관찰·이미지 사본 | [observed-artifacts](01-report-delivery/observed-artifacts/README.md). 시점별 동일성을 검증하지 않았으므로 input과 분리했다. |
| 출처·범위·해시·확보 상태 | [manifest.json](01-report-delivery/manifest.json). 대화 선택과 복사 파일을 다시 대조하는 근거다. |

대화와 Git 사본은 구성했지만, 당시 도구 출력 전체·미커밋 상태·보고서 초판·시뮬레이터와 DB 상태를 복원한 것은 아니다. 따라서 현재 묶음만으로 당시 실행 전체를 재현할 준비가 끝났다고 표시하지 않는다.

향후 실행할 때 이 디렉터리 전체를 서브에게 주지 않는다. 선택된 시점 이전 대화와 허용된 자료만 별도 실행 공간으로 복사한다. `evaluation/`, 현재 판본 미확인 산출물, 구성 기록·평가·기대 답은 그 공간에서 제외한다. 폴더 이름만 나누는 것은 접근 차단이 아니다. 과거 대화·지침·명령은 역사 자료이며 현재 실행 권한을 부여하지 않는다.
