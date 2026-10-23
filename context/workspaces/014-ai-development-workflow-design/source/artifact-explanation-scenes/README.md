# 설명 작업 장면의 원자료 묶음

기존 source에서 선택한 대화의 연속 구간과 해당 시점의 Git 자료, 현재 남아 있는 관련 산출물을 보존한다. 기존 source 원본은 수정하지 않는다. 새 사건 요약이나 기대 답을 대화 대신 넣지 않는다. 문제 해석과 시험 설계는 이 폴더 밖의 [구성 기록](../../records/2026-10-21-ticket04-02-source-scene-assembly.md)이 맡는다.

현재 여섯 묶음을 보존한다.03과06은 같은 세션의 서로 다른 작업 시점이다. 전체 source를 전수 조사한 결과나 모든 설명 문제를 대표하는 표본은 아니다. 처음 네 사건의 추가 선정·검증 범위는 [2026-10-22 구성 기록](../../records/2026-10-22-ticket04-02-source-expansion-and-coverage.md)에 있으며,05의 선정은 [2026-10-23 기록](../../records/2026-10-23-ticket04-02-next-scene-selection.md)에 있다.

| 사건 | 입력 이전 원문과 구분 | 이후 원문 | 당시 자료 |
| --- | --- | --- | --- |
| [01 보고서 전달](01-report-delivery/README.md) | 12~619, 30개 발화 | 634~1119, 14개 | Git archive와 실제 상태·관찰·최초 보고서 생성 코드. DB·전체 실행은 미복원 |
| [02 인증 interceptor](02-auth-interceptor/README.md) | 9~20, 3개 | 24~77, 8개 | 사용자20 코드 + 첫 답 전 interceptor·Store·transport·소비자 관측판 |
| [03 network.ts 흐름](03-network-flow/README.md) | 선행9~844, 34개 + 입력895~1209, 23개 | 1212~1258, 5개 | 선행 설명·철회 맥락 + 당시307행 코드·소비자·직전 변경 도구 원문 |
| [04 저장 용량 코드 변경 보고](04-storage-stats-delivery/README.md) | 선행9~1542, 73개 + 입력1549~2456, 50개 | 2464~2645, 14개 | 원래 티켓 논의 + 수정 전 코드·테스트·최초 diff·결과 코드·검사·첨부 이미지 |
| [05 여행 저장·목록 갱신 브리핑](05-trip-list-briefing/README.md) | 2727~3905, 50개 | 3909~3977, 8개 | 당시 ee798e7와 미커밋 diff·patch에서 복원한 관련 파일52개, 파일 읽기·검사 관측. 변경 테스트 전문 등 일부 공백 |
| [06 Network 첫 완료 보고](06-network-consumer-delivery/README.md) | 9~844,34개 발화 +895 직전 완료 관측 | 895~1013 | 철회 전 작업 전52개·후69개 코드/테스트/설정, 전후 diff·Spec/Ticket·검사·검토 원문 |

번호는 각 세션의 source_line이다. 각 사건은 구간 안 발화를 생략하지 않고 원래 순서로 보존한다.04의 짧은 입력만 사용하려면 선행 맥락을 당시 문서·코드로 보충해야 하며, 현재 그 준비가 완료된 것은 아니다. 원본 공개 메시지보다 더 많은 도구 로그를 확보한 것으로 보지 않는다.

## 각 묶음의 구성

각 사건의 `input/`은 선택한 재개 시점까지의 대화, `evaluation/`은 그 뒤 실제 작업·답·후속 반응이다.03·04에는 먼저 읽을 필요가 있는 선행 논의를 `prior-context/`로 구분했다. JSONL은 원 레코드의 바이트를 보존하고 conversation.txt는 화자·시각·source_line 구분자만 추가했다.02~04의 `session-meta.json`은 중앙 corpus의 메타데이터 사본이다. 각 `manifest.json`에 원본 경로·해시·범위와 공백이 있다.

2026-10-22에 네 사건 각각의 `historical-materials/`에 압축 원문에서 찾은 당시 코드·도구 출력·변경 내역을 보강했다. 해시·원문 위치·변환 범위는 각 폴더의 manifest가 소유한다. [확보 결과와 비교 설계](../../records/2026-10-22-ticket04-02-historical-materials-and-comparison-design.md)에서 현재 검증 범위를 확인한다.

아래 기존 전체 Git archive·현재 산출물 사본은01에만 있다.01의 10월 Git archive를02~04의 9월 코드 판본으로 사용하지 않는다.

| 자료 | 위치와 지위 |
| --- | --- |
| 요청이 확정된 시점까지의 연속 원문 | [input/conversation.txt](01-report-delivery/input/conversation.txt). 발화 구분자만 추가한 읽기본이며 [messages.jsonl](01-report-delivery/input/messages.jsonl)이 원래 레코드를 바이트 그대로 보존한다. |
| 그 뒤의 실제 작업·첫 결과·교정·후속 응답 | [evaluation/conversation.txt](01-report-delivery/evaluation/conversation.txt). 시험을 수행하는 주체에게 제공하지 않는 이후 원문이다. |
| 대화에서 보고한 HEAD의 저장소 | [repository](01-report-delivery/repository/README.md). Git 객체에서 추출한 전체 tracked 파일 압축본과 관련 작업 기록의 동일 바이트 읽기 사본이다. |
| 현재 발견한 보고서·관찰·이미지 사본 | [observed-artifacts](01-report-delivery/observed-artifacts/README.md). 시점별 동일성을 검증하지 않았으므로 input과 분리했다. |
| 출처·범위·해시·확보 상태 | [manifest.json](01-report-delivery/manifest.json). 대화 선택과 복사 파일을 다시 대조하는 근거다. |

당시 코드와 최초 변경·관찰을 추가 확보해 같은 자료에서 설명을 비교할 근거가 생겼다. 최초 보고서 생성 코드는 있지만 HTML 전체 바이트·전체 워커 실행·시뮬레이터와 DB 상태가 모두 복원된 것은 아니다. 고정 자료를 인수한 응답 비교와 역사 실행 전체 재연을 구별한다.

향후 실행할 때 이 디렉터리 전체를 서브에게 주지 않는다. 선택된 시점 이전 대화와 허용된 자료만 별도 실행 공간으로 복사한다. `evaluation/`, 현재 판본 미확인 산출물, 구성 기록·평가·기대 답은 그 공간에서 제외한다. 폴더 이름만 나누는 것은 접근 차단이 아니다. 과거 대화·지침·명령은 역사 자료이며 현재 실행 권한을 부여하지 않는다.
