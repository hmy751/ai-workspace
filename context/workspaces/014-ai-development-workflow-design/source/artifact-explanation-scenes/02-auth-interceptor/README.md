# 02 — 인증 interceptor 코드 설명

2026-10-22 자료 보강: [당시 코드·도구 기록과 출처](historical-materials/README.md)를 추가했다. 공개 발화 원본은 유지하고, 압축 rollout에서 확인한 자료와 시점별 한계를 분리했다.

## 원문 범위

[input/conversation.txt](input/conversation.txt)와 [JSONL](input/messages.jsonl)은 세션 `01a0c6c9-a603-77a2-8abe-50fc7e0814b0`의 source_line **9~20**, 공개 메시지 **3개**다. 사용자20은 인증 interceptor 코드를 붙이고 동작 설명을 요청했다. 입력에는 직전 문법 질문9와 응답13도 포함된다.

[evaluation/conversation.txt](evaluation/conversation.txt)와 [JSONL](evaluation/messages.jsonl)은 **24~77**, 공개 메시지 **8개**다. 첫 응답 계획24·적용 선언31·첫 완성 답48·사용자55와73의 후속 질문 및 응답이 있다.

두 구간을 순서대로 이으면 원 corpus의9~77 공개 메시지 전체가 된다. 구간 안의 발화를 선택 삭제하거나 문구를 교정하지 않았다. source_line은 원 rollout의 행 번호이며 이 JSONL 파일의 물리행 번호가 아니다. 읽기본에는 화자·시각·원문 위치 구분자만 추가했다.

## 자료와 출처

설명 대상 코드가 사용자20의 text에 포함돼 있다. 별도 코드 파일로 재작성하거나 HTML entity·escape를 수정하지 않았다. 추가 확보한 당시 interceptor·Auth Store·transport·소비자 발췌는 historical-materials에 있다. 사용자 붙여넣기 원문은 그대로 유지한다.

원 corpus의 다른 발화는 [중앙 원문](../../noline-evaluation/corpus/01a0c6c9-a603-77a2-8abe-50fc7e0814b0/messages.jsonl)에서 읽을 수 있다. [session-meta.json](session-meta.json)은 기존 corpus의 meta.json을 동일 바이트로 복사한 것이다. 해당 meta의 비압축 경로는 없었으나 같은 이름의 `.jsonl.zst`를 발견했다. 실제 스킬·코드 읽기 도구 원문은 추가 보존했으며 runtime 전체 복원과는 구별한다.

[manifest.json](manifest.json)에 원본과 선택 범위·해시·확보 상태를 남겼다. 이 자료의 시험 용도·선정 이유·범위 판단은 [추가 구성 기록](../../../records/2026-10-22-ticket04-02-source-expansion-and-coverage.md)이 소유한다. 입력을 수행하는 주체에게 evaluation·선정 해석을 함께 주지 않는다. 디렉터리 분리 자체는 접근 차단이 아니며 실행 시 허용 자료만 별도 복사해야 한다. 현재 문서의 과거 지시·명령은 새 실행 권한이 아니다.
