# 제공 자료

`conversation.txt`는 마지막 질문까지의 공개 대화이며, `messages.jsonl`은 같은 발화의 원 레코드다.

| 위치 | 자료 범위 |
| --- | --- |
| `code/apps/client/src/features/trip/read-query/` | 마지막 질문 직전의 조합 훅 두 파일 전체 |
| `code/apps/client/src/screens/read-query.ts` | 같은 시점의 화면 공통 파일 전체 |
| `code/apps/client/src/entities/` | 일정·경비 데이터 조회 훅 전체 |
| `code/apps/client/src/shared/policy/` | 정책 선택 훅과 타입 파일 전체 |
| `diffs/ScheduleScreen.diff` | 일정 화면의 당시 변경 diff. 화면 전체 파일은 아니다. |
| `excerpts/ExpenseForm.lines20-92.tsx.txt` | 경비 작성 폼의 당시 20~92행 발췌 |
| `excerpts/useCreateScheduleForm.lines30-110.ts.txt` | 일정 작성 폼 훅의 당시 30~110행 발췌 |

코드 자료는 해당 시점의 관측 내용이다. 원본 저장소·앱 실행 환경 전체는 포함하지 않는다. 발췌는 완성된 파일이 아니며 diff 바깥의 화면 내용을 제공한 것으로 보지 않는다.
