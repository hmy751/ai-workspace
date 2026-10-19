# 기존 Project의 전체 내용·제공 방식과 01-02의 접점

2026-10-18.03의 첫 대조76 다음으로, 사용자는 기존 Project가 무엇을 어떻게 제공하는지 먼저 전체적으로 보고01-02와 겹치는 부분·유지·보완을 함께 판단하자고 요청했다. 이번 문서는 보존된 구성의 지도와 Main의 첫 비교 의견이다. 새 Project 배치나 본문 통합을 채택한 결과가 아니다.

## 사용자 요청과 분류의 의미

> 먼저 기존 Project가 어떤 내용을 어떻게 제공하고 있는지 전체적으로 보여줘. 그걸 보고 01-02 기준과 겹치는 부분, 유지하거나 보완할 부분부터 같이 보자.

> 한번에 애매하게 다 합치지 않았으면 좋겠어 예를 들어 뭐 제품 정책 뭐 코드 가이던스 다 있다고 애매하게 본문을 합치지말고 이걸 분류는 되는 형태인걸 인지하면 좋겠어

사용자는 함께 읽어야 한다는 이유로 제품 정책·코드 가이던스 등의 본문을 모호하게 합칠 것을 우려했다. 따라서 이번 전체 지도에서는 내용의 역할과 판본을 구별한다. 연결해서 사용하는 관계와 같은 본문으로 합칠 필요는 별도로 판단한다. 이 요청을 모든 종류마다 파일 하나를 의무화하거나 기존 폴더를 영구 고정하라는 뜻으로 확대하지 않는다.

현재 순서는 **전체 제공 내용 확인 → 기존 내용과01-02의 겹침·유지·보완 논의**다.76에서 Main이 추천했던 API 변경 장면은 그 이후 사용할 수 있는 후보이며 먼저 진행할 확정 작업이 아니다.

## 어떤 자료의 전체인가

| 자료 | 확인한 구성 | 이번 역할과 한계 |
| --- | --- | --- |
| [Noline 기준판](../source/noline-baseline/context/project/README.md) | Markdown19편. 내용 본문10편과 색인·구성·관리9편 | 실제 제품 내용이 채워진 기존 Project. 아래 기준판 열이 이19편의 범위다. |
| [별도 worktree 관찰판](../source/supplement/worktree-project-context/context/project/README.md) | Markdown33편. 내용 본문24편과 색인·구성·관리9편. 기준판보다14편 추가 | 더 넓은 주제와 문서 개선 모습을 확인하는 별도 자료. 기준판과 합친 최신 정본이 아니다. [보존 경위](../source/supplement/README.md)의759cba3 기반 미커밋 관찰판이며10월1일의 정확한 역사판으로도 단정하지 않는다. |
| [Reference Project](../source/ai-workspace-baseline/reference-project/context/project/README.md) | 같은 역할 구분과 읽기·관리 기준, 작은 실행 예제 | 구성 기준과 내용·코드·검증의 연결을 보여 주는 참고. Noline 제품 내용과 섞어 하나의 제품으로 설명하지 않는다. |

Noline 입구는 아직 옮기지 않은 상세를 기존 `.claude/context`, `rules`, `runbooks` 등으로 안내한다. 기준판 snapshot에는 이 상세 디렉터리가 없으므로 해당 원문까지 조사한 것은 아니다. 원본 Noline에 없다는 뜻도 아니다. 이번 지도는 보존된 Project 본문 전체와 그 본문이 밝힌 외부 소유 범위를 다룬다.

## 내용의 전체 지도

`common`은 일반 코드 원칙 모음이 아니라 **제품·데이터가 뜻하는 바**다. `current`는 이번 작업의 진행 상황이 아니라 **제품의 현재 구현·지원·근거 범위**다. `guidance`에는 코드 판단, 제품별 개발 계약, 설명 기준처럼 역할이 다른 가이드가 들어 있다. 아래 표에서는 이 차이도 나눠 표시한다. 새 폴더 배치 제안은 아니다.

| 역할·현재 위치 | Noline 기준판의 본문 | 별도 관찰판에서 추가된 본문 | 실제 제공하는 이해 |
| --- | --- | --- | --- |
| 제품 목적·정책·데이터 의미 / `common` | 제품, 통화·금액, 날짜·시각 | 여행 이용, 기기 세션, Local 데이터 보존 | 오프라인 여행과 데이터 관계, 통화별 합계, 시점과 달력 날짜의 차이. 추가 본문은 연결 제한 때의 선택·입력 보존, 인증 만료·재로그인·계정 종료, 기기 저장과 서버 반영·정리의 의미를 설명한다. |
| 실제 구조·지원·근거 / `current` | 전체 구조, 도시 검색, 저장 용량 집계 | 네트워크·화면 접근, 세션·Local 데이터, 동기화·정리 | client·server·schema·UI가 맡은 일, 검색 선별·실패 반환, 저장 집계의 부분 실패·최신 결과 반영. 추가 본문은 관측과 화면 연결, 세션 보호·복구 공백, 실행 잠금·queue·pull·cleanup의 실제 보장을 설명한다. |
| 코드 설계·표현 판단 / `guidance` 일부 | 동작 보존 리팩터링 | 코드 가독성 | 줄일 이해·수정 부담, 보존할 동작, 실제 개선 비교. 추가 기준은 중괄호·빈 줄·배치·이름·주석·로그·catch·await/void를 다룬다. |
| 제품별 개발 계약·작업 방법 / `guidance` 일부 | API 계약 | Network·Policy, 인증·세션, Local 데이터·동기화, 앱 준비 | schema·route·serializer 책임, 요청·응답과 접근 범위. 추가 가이드는 관측·정책·화면 책임, 로그인·종료 순서, 원자적 저장·동기화·삭제, DB 준비·인증 복원·재시도 계약과 검증을 설명한다. |
| 설명·근거 판단 / `guidance` 일부 | 설명과 근거 기준 | 없음 | 사실·해석·실행 결과·사람의 결정을 구별해 설명하는 기준. 지정된 설명 관련 스킬에서 조건부로 사용하며 모든 작업 응답에 자동 적용하는 문서가 아니다. |
| 선택 이유·기각안·재검토 / `decisions` | 선택한 여행만 Local 기준으로 관리하는 이유 | 네트워크 불확실성과 복구, 기기 세션과 Local 지속, 앱 준비 실패와 재시도 | 선택한 대안과 제외한 대안, 바꿔 볼 신호를 보존한다. 현재 계약은 원칙적으로 연결된 내용 본문이 맡는다. |

### 본문별 원자료 경로

관찰판에 같은 이름으로 있는 기존 본문도 내용이 보완됐으므로, 추가 파일 수가 변경 전체를 뜻하지는 않는다.

| 구분 | 기준판 본문 | 관찰판의 추가 본문 |
| --- | --- | --- |
| 제품 의미 | [제품](../source/noline-baseline/context/project/common/product.md), [통화](../source/noline-baseline/context/project/common/currency.md), [날짜](../source/noline-baseline/context/project/common/date-and-time.md) | [여행 이용](../source/supplement/worktree-project-context/context/project/common/travel-access.md), [기기 세션](../source/supplement/worktree-project-context/context/project/common/device-session.md), [Local 데이터 보존](../source/supplement/worktree-project-context/context/project/common/local-data-preservation.md) |
| 현재 구현 | [구조](../source/noline-baseline/context/project/current/architecture.md), [도시 검색](../source/noline-baseline/context/project/current/city-search.md), [저장 집계](../source/noline-baseline/context/project/current/storage-statistics.md) | [화면 접근](../source/supplement/worktree-project-context/context/project/current/network-and-screen-access.md), [세션·데이터](../source/supplement/worktree-project-context/context/project/current/session-and-local-data.md), [동기화·정리](../source/supplement/worktree-project-context/context/project/current/sync-and-cleanup.md) |
| 코드 판단 | [리팩터링](../source/noline-baseline/context/project/guidance/behavior-preserving-refactoring.md) | [코드 가독성](../source/supplement/worktree-project-context/context/project/guidance/code-readability.md) |
| 제품별 개발 | [API 계약](../source/noline-baseline/context/project/guidance/api-contracts.md) | [Network·Policy](../source/supplement/worktree-project-context/context/project/guidance/network-and-policy.md), [인증·세션](../source/supplement/worktree-project-context/context/project/guidance/authentication-and-session.md), [데이터·동기화](../source/supplement/worktree-project-context/context/project/guidance/local-data-and-sync.md), [앱 준비](../source/supplement/worktree-project-context/context/project/guidance/app-startup.md) |
| 설명 | [설명과 근거](../source/noline-baseline/context/project/guidance/explanation-and-evidence-criteria.md) | 없음 |
| 선택 이유 | [Selective Local-First](../source/noline-baseline/context/project/decisions/0001-selective-local-first.md) | [네트워크](../source/supplement/worktree-project-context/context/project/decisions/0002-network-uncertainty-and-recovery.md), [기기 세션](../source/supplement/worktree-project-context/context/project/decisions/0003-device-session-and-local-continuity.md), [앱 준비](../source/supplement/worktree-project-context/context/project/decisions/0004-startup-failure-and-retry.md) |

## 내용을 어떻게 제공하는가

**입구는 작업 주제, 본문은 역할별 설명이다.** 기준판 README는 제품·API·리팩터링 같은 작업 단서에서 본문으로 보낸다. 관찰판은 여행 이용·인증·저장·앱 준비를 제품 의미 / 변경할 때 / 실제 지원·남은 차이의 세 열로 연결한다. 해당 관계를 찾을 수 있게 하되 모든 작업이 세 층 전부를 읽는 순서는 아니다.

예컨대 인증 만료를 다룰 때 다음 내용은 서로 연결되면서도 별도 본문에 있다.

| 알고 싶은 것 | 안내하는 본문과 내용 |
| --- | --- |
| 사용자가 어떤 경험을 해야 하는가 | `common/device-session`: 만료·재로그인·종료와 Local 데이터 보존의 제품 의미 |
| 변경할 때 무엇을 지켜야 하는가 | `guidance/authentication-and-session`: 계정 검사·저장·공개 순서, 요청 보호, 로그인·종료 책임 |
| 실제 구현은 어디까지 되는가 | `current/session-and-local-data`: Store·기기 저장·DB·요청의 보호 범위와 reset 뒤 복구 공백 |
| 왜 그 선택을 했는가 | `decisions/0003`: Local 지속, 명시적 종료, 제외한 대안과 재검토 조건 |

**본문에는 다음 판단에 필요한 설명이 있다.** 통화 문서는 기본 통화·경비별 통화·대표 표시·합계의 차이와 미정을, 날짜 문서는 시점·date-only 의미와 저장·응답 경계를 함께 설명한다. API 본문은 역할 설명과 제품별 계약, 검사별 증명 범위를 제공한다. 관련 내용이 한 문서에 있다고 모두 같은 역할인 것은 아니다. 문서의 주된 질문과 내부 절에서 제품 계약·관찰된 구현·미결정을 구별할 수 있는지도 함께 본다.

**찾는 방법·쓰는 방법·갱신 방법은 내용 본문과 분담한다.** 두 판본의 관리9편은 root README1편, 네 분류의 README4편, MAINTENANCE1편, REFERENCE3편이다. README는 위치·역할·권위를, REFERENCE는 내용 선별·구성과 읽기의 판단 기준을, MAINTENANCE는 갱신 시점·권한·영향·완료 확인을 맡는다. [읽기 스킬](../source/noline-baseline/.claude/skills/read-project-context/SKILL.md)은 필요한 본문을 고르고 새 질문이 생기면 추가하며 이미 유효한 이해를 재사용한다. [갱신 스킬](../source/noline-baseline/.claude/skills/update-project-context/SKILL.md)은 지속되는 의미의 변경을 기존 소유 본문에 반영한다. 제품 계약·기준 자체를 스킬에 다시 정의하지 않는다. 한 작업의 시도·후보·검증 이력은 Work에 남긴다.

**Reference는 이 관계를 작은 예제로 제공한다.** [제품 요구](../source/ai-workspace-baseline/reference-project/context/project/common/prd.md)는 요청 정책 설정의 의미·제약을, [구조](../source/ai-workspace-baseline/reference-project/context/project/current/architecture.md)는 구현·테스트와 증거 범위를 설명한다. 결정 문서가 특정 값의 정본이라고 명시하는 예외도 있다. 따라서 기존 구성 자체도 단순히 폴더 이름만으로 모든 권위를 결정하지는 않는다.

## 01-02와 겹치는 부분·유지·보완에 대한 첫 의견

비교 대상01-02는 [72의 시안](2026-10-18-72-short-common-and-detail-prototype.md)과 [quality 본문](prototypes/applied-criteria-2026-10-17/shop-web/context/project/quality.md)이다. 기준 전체는 미완료이며73의 사용자 유보가 있다. 기존 Noline에서 채택한 규칙과014에서 논의 중인 일반 기준을 같은 지위로 바꾸지 않는다.

| 기존 내용 | 01-02와의 관계 | 유지할 것 | 함께 판단할 보완 |
| --- | --- | --- | --- |
| 동작 보존 리팩터링 | 목적·사용처·이해/수정 비용, 유지·수정 판단이 직접 겹침 | 보존할 동작과 실제 줄일 부담, 동작 검사와 가독성 개선 확인의 구별 |01-02는 공통화·새 설계까지 다룬다. 넓게 쓸 기준과 리팩터링 작업에 필요한 설명을 나누고 중복 정의 여부를 비교한다. |
| 코드 가독성 | 이름이 보장하는 범위, 함께 바뀌는 책임, catch의 실패 분류, 비동기 완료가 직접 겹침 | 실제 예시·사용 조건, Noline에서 합의한 표현 규칙의 지위 | 일반 판단과 프로젝트별 스타일을 식별하고,01-02가 더한 공통화 목적·수명·사용처 선택까지 충분히 전달되는지 본다. “중괄호는 항상” 같은 기존 합의를 일반 원칙 후보와 같은 강도로 합치지 않는다. |
| API·인증·동기화 등 제품별 개발 가이드 |01-02의 책임·계약·수명 관점을 제품에 구체화하는 관계 | Noline의 실제 schema·serializer·route 배치, 저장·인증·실패 계약과 검증 경계 | 일반 기준에서 관련 제품 계약을 찾을 수 있는지, 구체 Noline 배치를 다른 제품의 의무로 올리지 않는지 확인한다. |
| 제품 의미·현재 지원 |01-02를 적용할 때 필요한 조건과 보존 대상 | 통화·날짜의 의미, 사용자에게 약속한 동작, 실제 구현·미지원·근거 시점 | 품질 기준이 이 조건을 찾아 쓰게 연결한다. 현재 구현과 바라는 계약이 다를 때 차이를 남긴다. 품질 원칙의 본문으로 흡수할 대상은 아니다. |
| 설명 기준·선택 이유 | 사실·판단·채택·검증을 구별한다는 접점이 있음 | 설명 스킬의 적용 조건, 선택 이유·기각안·재검토 근거 | 같은 구별의 중복 정의 여부를 본다. 선택 기록 전체를 매 작업의 필수 입력으로 만들거나 설명 기준을 코드 원칙으로 합치지 않는다. |

Main의 우선 비교 추천은 **동작 보존 리팩터링 + 코드 가독성 +01-02 기준**이다. 겹침이 가장 직접적이므로 기존에 충분한 판단,01-02에서 새로 얻은 판단, 제품별 스타일, 작업별 절차를 문장·절 단위로 대조할 수 있다. 그 비교를 보고 필요한 본문·연결·유지 위치를 정한다. 지금 별도 quality 파일의 신설·기존 가이드 삭제·본문 통합 중 하나를 미리 선택하지 않는다.

## 확인 범위와 현재 지위

이번 turn과76의 조사에서 Main·분담 조사자가 기준판의 내용10편과 구성·읽기·관리 안내를 나누어 확인했고, 관찰판 담당자는33편 전체를 읽었다.01-02 비교 담당자는 quality·리팩터링·API·코드 가독성의 실제 본문을 대조했다. Reference 구성·읽기·관리 기준과 대표 내용·읽기/갱신 스킬도 확인했다. 분담 조사 결과는 Main이 종합했으며 원본 제품의 최신 코드·실행 결과를 확인한 것으로 확대하지 않는다.

이번 산출물은 전체 지도와 첫 비교 의견이다. source·prototype·실제 Project·스킬은 변경하지 않았다.03은 설계 진행 중이고, 다음은 이 지도를 바탕으로 유지·보완 대상을 함께 좁히는 논의다.01-02 전체 기준 채택·실제 사용 효과·03 완료는 확인하지 않았다.
