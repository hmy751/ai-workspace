# 여행 중 일정과 경비를 이어가는 제품 기준

새 작업의 제품 목적·보존할 동작·데이터 경계를 판단할 때 읽는다. 이 본문은 Noline의 제품 개관을 소유한다. 여행 이용, 기기 세션, 로컬 변경 보존의 상세 의미는 아래에서 연결하는 common 본문이 소유하며, 관련 코드의 적용·변경 기준은 [guidance](../guidance/README.md)에서 찾는다.

## 사용자 장면과 성공 기준

**Noline은 연결이 끊겨도 여행의 일정 확인·기록과 경비 관리를 이어가는 앱이다.** 사용자가 필요한 여행 하나를 활성화해 오프라인 데이터를 준비하고, 복구 뒤 변경을 서버와 맞출 수 있게 한다. 모든 여행을 Local에 쌓는 대신 활성 여행에 저장·동기화 책임을 집중한다.

| 개념 | 제품에서 맡는 역할 |
| --- | --- |
| Trip·Schedule·Expense | 여행과 그 여행의 일정·경비. 활성 여행은 Local SQLite, 비활성 여행은 Server API가 기준 |
| 여행 선택 | 지금 보고 작업하는 대상. 활성 여행과 달라도 됨 |
| 여행 활성화 | Local 준비·저장·동기화를 책임질 대상 지정 |
| 지도·검색·길찾기 | 사용자 소유 Entity와 별도인 외부 서비스. Policy에 따라 온라인 Network-First 또는 제한된 기능 사용 |

Activation Router가 Entity의 Local/Remote 출처를 고른다. 온라인 비활성 여행도 조회·수정·삭제할 수 있다. 연결 변화로 선택·활성화를 자동 변경하지 않는다. 지도·경로 다운로드는 여행 준비에 연결되지만 Entity 저장·sync와 같은 완료를 뜻하지 않으며, 여행 활성화 여부가 온라인 서비스 사용을 막는 조건도 아니다.

### 여행 중 이어갈 수 있는 작업

- **Offline 활성 여행:** 제목·날짜·금액 등 핵심 입력을 이어 간다. 온라인 보강 정보는 복구 뒤 보완하는 장면을 지원 목표로 둔다.
- **Offline 비활성 여행·새 여행:** 편집과 여행 생성은 지원 범위가 아니다.
- **인증 만료:** 같은 계정 활성 여행의 Local 조회·생성·수정·삭제를 별도 기한 없이 유지한다. 같은 계정 재로그인으로 인증을 복구한다.
- **계정 변경·명시적 로그아웃:** 로그아웃 뒤 다른 계정으로 로그인한다. 종료는 Local 준비와 미전송 변경을 폐기한다.
- **경비:** 통화별로 관리하고 자동 환산 합계로 섞지 않는다.

제한·입력 보존·복구는 [여행 이용](travel-access.md), 계정·종료 실패는 [기기 세션](device-session.md), 금액은 [통화와 금액](currency.md)이 소유한다.

성공 기준은 연결이 불안정해도 핵심 입력을 잃지 않고 서버와 다시 맞출 수 있는 것이다. 기능이나 이식 검사 통과만으로 달성됐다고 판단하지 않는다. 현재 배포 대상은 iOS이며 Android 설정의 존재를 동등한 배포·검증으로 보지 않는다.

## 함께 지킬 데이터 관계

| 관계 | 지킬 기준 |
| --- | --- |
| Local 변경과 전송할 기록 | 같은 transaction에 Entity·sync_queue를 저장해 한쪽만 남지 않게 한다. |
| ID와 타입 | 클라이언트가 generateId()로 ID를 만들고 서버가 수용한다. Client/server 타입은 @repo/schema의 Zod 계약에서 추론한다. |
| 시각 | 한 시점은 timezone 포함 ISO datetime으로 저장·전송한다. Expense date의 경계 차이·열린 선택은 [날짜와 시각](date-and-time.md)을 따른다. |
| 서버 접근 | 인증과 사용자 소유권을 확인한다. |
| 미전송 변경 | PENDING·IN_PROGRESS·FAILED를 보존 판단에 포함한다. 응답 유실 가능성이 있어 서버에 변경이 없다는 뜻은 아니다. |

삭제·비활성화·정리는 미전송 변경을 보존한다. 원본 row·queue, soft delete·물리 삭제와 명시적 폐기 예외는 [Local 보존](local-data-preservation.md)이 소유한다.

Policy는 허용·모드·이유를, Router는 출처·실행 순간의 거절을 맡는다. UI는 이유와 다음 행동을 안내하고 useAppPolicy·PolicyErrorDisplay·NetworkStatusIndicator 등의 기존 패턴을 사용한다. 작업별 보호 지점은 [Rules](../../../.claude/rules/README.md)·[Guard Map](../../../.claude/guards/README.md)에서 찾는다.

## 범위와 갱신

특정 릴리스의 완성, 실제 동기화 성공, 외부 지도·OAuth·DB의 운영 상태와 사람 acceptance는 이 문서가 보장하지 않는다. 현재 구조·확인 범위는 [구현 지도](../current/architecture.md), 선택 이유는 [Decision](../decisions/0001-selective-local-first.md)에 있다.

활성화·다운로드의 실행 세부는 [Activation System](../../../.claude/context/activation-system.md), 폼 구성과 필수 입력은 [Manual Input](../../../.claude/context/manual-input.md)과 [Form](../../../.claude/context/form.md)에 남는다. 해당 문서는 이곳에서 연결한 제품 의미를 전제로 상세 책임을 설명한다.

제품·domain 의미를 바꾸는 책임자가 영향받는 common 본문과 적용 가이드를 함께 갱신한다. 2026-09-25에 기존 제품 개관과 [승인된 구성안](../../work/workspaces/002-code-readability-refactoring/records/2026-09-23-01-project-context-composition-proposal.md)의 여행 이용·세션·데이터 보존 의미를 통합했다. 날짜·금액의 열린 선택과 작업별 검증·수락 상태는 이 편입으로 바꾸지 않는다.
