# 03 — network.ts 흐름 질문

2026-10-22 자료 보강: [당시 코드·도구 기록과 출처](historical-materials/README.md)를 추가했다. 공개 발화 원본은 유지하고, 압축 rollout에서 확인한 자료와 시점별 한계를 분리했다.

## 원문 범위

[prior-context/conversation.txt](prior-context/conversation.txt)와 [JSONL](prior-context/messages.jsonl)은 **9~844, 34개**의 선행 발화다.96에는 Network Store의 구현 상태가,255에는 session·identity·version의 역할을 다룬 검토가 있다. 사용자가1209 이전에 해당 설명을 접한 이력을 보존한다. 아래 input만으로 원래 대화의 사전 지식을 모두 복원한 것으로 보지 않는다.

[input/conversation.txt](input/conversation.txt)와 [JSONL](input/messages.jsonl)은 세션 `01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30`의 source_line **895~1209**, 공개 메시지 **23개**다. 이전 변경의 결과 보고895부터 범위 질문·직접 스킬 호출920·설명963·변경 철회·새 품질 작업을 거쳐 network.ts 질문1209까지 연속 보존한다.

[evaluation/conversation.txt](evaluation/conversation.txt)와 [JSONL](evaluation/messages.jsonl)은 **1212~1258**, 공개 메시지 **5개**다. 적용 선언1212·첫 완성 답1239·사용자1246·응답1251·다음 요청1258이 있다.

prior-context·input·evaluation을 순서대로 이으면 원 corpus의9~1258 공개 메시지 전체가 된다. 구간 안의 발화를 선택 삭제하거나 문구를 교정하지 않았다. source_line은 원 rollout의 행 번호이며 이 JSONL 파일의 물리행 번호가 아니다. 읽기본에는 화자·시각·원문 위치 구분자만 추가했다.

## 자료와 출처

사용자1209는 코드 경로만 포함하며 nontext_types는 비어 있다. 당시 network.ts 전체307행과 소비자·테스트 발췌, 직전 다섯 파일의 변경 도구 기록을 historical-materials에 추가했다. 평가용 답1239의 코드 발췌를 입력의 원본 코드로 대체하지 않는다.

원 corpus의 다른 발화는 [중앙 원문](../../noline-evaluation/corpus/01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30/messages.jsonl)에서 읽을 수 있다. [session-meta.json](session-meta.json)은 기존 corpus의 meta.json을 동일 바이트로 복사한 것이다. 해당 meta의 비압축 경로는 없었으나 같은 이름의 `.jsonl.zst`를 발견했다. 실제 스킬·코드 읽기 도구 원문은 추가 보존했으며 runtime 전체 복원과는 구별한다.

[manifest.json](manifest.json)에 원본과 선택 범위·해시·확보 상태를 남겼다. 이 자료의 시험 용도·선정 이유·범위 판단은 [추가 구성 기록](../../../records/2026-10-22-ticket04-02-source-expansion-and-coverage.md)이 소유한다. 입력을 수행하는 주체에게 evaluation·선정 해석을 함께 주지 않는다. 디렉터리 분리 자체는 접근 차단이 아니며 실행 시 허용 자료만 별도 복사해야 한다. 현재 문서의 과거 지시·명령은 새 실행 권한이 아니다.
