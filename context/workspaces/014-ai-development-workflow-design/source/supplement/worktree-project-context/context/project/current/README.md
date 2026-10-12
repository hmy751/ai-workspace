# Noline의 현재 구현 맥락

이 폴더는 Project 수준의 현재 구현·지원·적용 관계와 다음 판단에 필요한 검증 범위를 설명한다. 목적과 제품 의미는 [common](../common/README.md), 관련 작업의 계약·판단·적용은 [guidance](../guidance/README.md)가 맡는다. 현재 사실이 있다는 이유만으로 모든 주제에 별도 문서를 만들지는 않는다.

현재 본문은 다음과 같다.

- [구조·지원·검증 지도](architecture.md): client·server·schema·UI의 실제 책임과 제품·Harness 검증의 범위를 구별할 때 읽는다.
- [네트워크와 화면 접근](network-and-screen-access.md): 관측·override·Policy·Router·조회 출처가 실제 화면 접근과 선택·입력 보존에 어디까지 연결됐는지 확인할 때 읽는다.
- [기기 세션과 Local 데이터](session-and-local-data.md): 인증 복원·거부·재로그인·종료가 기기 기록·DB 소유권·진행 중 작업·화면을 어떻게 연결하는지 확인할 때 읽는다.
- [sync와 데이터 정리](sync-and-cleanup.md): 실행 조건·queue·pull·cleanup·vacuum의 실제 성공 범위와 미전송 보존의 남은 차이를 판단할 때 읽는다.
- [도시 검색의 현재 경계](city-search.md): 여행 생성의 GeoNames 요청·응답 선별, 변환과 실패 반환을 바꿀 때 읽는다.
- [저장 용량 집계의 현재 경계](storage-statistics.md): 프로필의 SQLite·Mapbox 집계, 부분 실패와 refresh 상태를 바꿀 때 읽는다.

구현·설정·테스트를 바꾸는 책임자가 [관리 계약](../MAINTENANCE.md)에 따라 관련 본문과 실제 Owner를 대조한다. 대조 대상·시점, 근거가 답하는 범위와 다시 확인할 변화를 찾을 수 있게 한다. 코드나 검증 경로가 달라지면 과거 pass를 현재 사실로 유지하지 않는다.

독립 본문의 필요성은 [구성 기준](../REFERENCE/composition.md)에 따라 가이드·코드와 함께 판단한다. 별도 현재 맥락이 주는 이해와 읽기·갱신 비용을 실제 적용에서 확인하며 문서 수·크기나 일률적인 편입 목록은 정하지 않는다.
