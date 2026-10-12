# 대화 추출 기술 QA

검토 버전: 2026-10-11 초안 primary conversation 46개 기준. 이 문서는 본문 의미를 평가하지 않고 추출 범위와 구조만 점검한다. 원문 표본은 시작·끝 일부만 확인했고, 스크립트는 본문을 출력하지 않는다.

- Collector 원문 경로 17개는 discovery와 sessions에 모두 있고, primary 17개에 전부 포함된다. 누락 경로는 0개다.
- Source가 dict인 발견 세션 334개는 전부 `source.subagent`와 parent를 가진다(`guardian_review` 211, `subagent` 123). 직접 사람 대화 집계에서 제외하는 것은 타당하지만, 위임 결과를 읽는 별도 경로는 원본에 남아 있다.
- 아래 역할별 집계는 source가 subagent dict가 아닌 전체 74세션(메시지 있는 64세션)과 primary 46세션을 구분한다. `corpus-stats.json`의 primary 메시지 4156개와 아래 primary 합계는 일치한다.

| 모집단 | source 세션 | 메시지 있는 세션 | 원본 user | 제외 wrapper | 추출 user | 추출 assistant | 추출 합계 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| conversation | 56 | 46 | 1344 | 204 | 1140 | 3016 | 4156 |
| maintainer | 17 | 17 | 229 | 36 | 193 | 219 | 412 |
| support_conversation | 1 | 1 | 2 | 2 | 0 | 11 | 11 |
| 전체 non-subagent | 74 | 64 | 1575 | 242 | 1333 | 3246 | 4579 |

- 전체 non-subagent의 원본 user와 추출 user 차이 242개는 runtime wrapper 제외와 정확히 일치한다. 세션별 불일치 0개다.
- 제외된 wrapper 242개는 모두 닫는 태그가 있고 태그 뒤 비공백 텍스트가 0개다. 이 형식 검사에서 wrapper 뒤 사람 요청을 함께 제거한 사례는 발견되지 않았다.
- assistant message channel은 모두 `None`이다. channel 제한으로 제외된 assistant message는 0개다. 다른 `response_item` 유형 `agent_message` 590개는 이 대화 추출본에 들어오지 않는다.
- 원본 user role의 순수 `<skill>` 원문 37개는 모두 닫는 태그 뒤 요청이 없고 추출본에 남지 않는다. `<in-app-browser-context>` 35개는 주변 UI 블록과 실제 요청이 한 메시지에 함께 있다(35개에 `## My request:` 표시). 답변 wrapper `<send_user_message_question_reply>` 12개는 실제 답을 포함한다.
- 세션 간 시각·역할·본문이 완전히 일치하는 replay 묶음은 0개다. 시각을 빼고 본문만 일치하는 묶음은 8개, 중복 여분 10개다. 이 묶음 중 primary 밖 세션이 섞인 것은 0개다. 중복 여분 중 `<skill>` 원문은 0개이며, 나머지에는 짧은 사용자 표현과 한 건의 긴 동일 요청이 포함된다. 본문 동일성만으로 fork/replay라고 단정할 수 없다.
- `agent_created_thread` 세션 1개는 현재 `support_conversation`으로 별도 분류된다. 해당 세션의 user 메시지는 0개다.

남은 수정 제안: 브라우저 주변 상태·질문 답변 wrapper는 내부 실제 요청/답을 보존한 채 wrapper 부분과 구분해 해석한다. 단순 user role 수치를 사람 발화 수치로 그대로 부르지 않는다. `agent_message`는 원본 locator를 별도로 색인하면 위임 결과의 추적성이 높아진다.

상세 수치, 원본 line locator, 동일 본문 SHA-256은 `extraction-audit.json`에 있다.
