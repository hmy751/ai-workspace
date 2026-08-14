# Workspace 생성과 병목 문제 정의

기록일: `2026-08-14`

## 사용자 결정

직전 작업을 먼저 커밋하고, context+harness 유지보수 병목 개선을 기존 reference 구현이나 Project application과 섞지 않는 새 Workspace에서 진행하기로 했다.

## 시작 장면

Machine receipt를 `records/receipts/<종류>/`로 분리하는 작업이 약 20분 걸렸다. 사용자는 recover·verify의 큰 흐름을 다시 확인한 뒤, 실제 runtime보다 같은 하네스 계약이 Project와 skill, 여러 Workspace에 분산되어 유지 비용이 커지는 문제를 별도 작업으로 개선할 필요가 있다고 판단했다.

정밀 timing 계측은 없으므로 약 20분을 구성 요소별 수치로 확정하지 않는다. 다만 실제 명령 결과는 reference 40개 테스트가 약 4초, helper 7개가 Python 버전별 약 2초였고, 작업 범위는 58개 파일과 기존 receipt 10개 이동까지 넓어졌다. 순차 context maintenance와 최종 review 대기도 있었다.

## 초기 판단

- 병목의 중심은 recover·verify 실행 속도가 아니라 계약 변경의 전파 범위와 작업 배치다.
- 같은 설명이 여러 곳에 있다는 사실만으로 바로 삭제하지 않는다. 먼저 canonical Owner, 실제 consumer, historical record, 현재 상태 설명을 구분해야 한다.
- 속도를 위해 evidence, path 방어, 사용자 파일 보호, proof ceiling을 약화하지 않는다.
- 첫 분석 사례는 직전 machine receipt 경계 변경으로 제한한다.
- 사용자는 Context 이동이나 새 Workspace 구성 때 모든 항목을 타이트하게 일괄 검사하기보다, main이 변경 성격을 판단해 필요한 수준으로 만들어 가기를 요청했다. 따라서 문서·routing 변경은 링크·경로·diff부터 확인하고, 실행 의미나 안전 경계가 바뀔 때만 full test·durable verify·독립 review로 확대한다.

## 첫 산출물 후보

변경된 규칙마다 canonical Owner, 필수 consumer, 링크 갱신 대상, 중복 설명, 필요한 검증을 한 화면에서 판단할 수 있는 병목 지도를 만든다. 이 지도는 아직 선택된 output이 아니며 검토와 수정 뒤에만 `output/index.md`에서 연결한다.
