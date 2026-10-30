# 06-01 — 형식 반영 뒤 전체 읽기 점검

**판정:** 확인한 Personal·Project 본문과 공통 진입·형성 자료에서 `02ea702c`의 형식 반영을 되돌릴 만한 내용 충돌은 찾지 못했다. 모든 문서를 naming처럼 다시 쓸 필요는 없다. 공통화의 선택 조건과 계약·수명의 오류 처리 부분은 다음에 가독성을 보완할 후보이며, 이번에는 본문을 추가 수정하지 않았다.

## 요청과 확인 범위

사용자는 naming만 전환한 이유를 확인한 뒤 기록·커밋과 전반 점검을 요청했고 “괜찮아지긴 한 것 같아”라고 말했다. [앞선 반영 기록](2026-10-30-ticket06-01-writing-format-application.md)에 요청·해석 범위를 보존했다. 이번 변경29개 파일은 `02ea702c5135e7575870fd1bc23030c215c64687`로 커밋했다. 준비 중 병렬02의 `04daae75`가 만들어져 그 커밋을 부모로 유지했으며, 공유 state·output·records 색인의 이번06-01 문장만 골라 반영했다.

Main이 아래 본문을 직접 읽고 적용 시점, 조건·행동의 분리, 이유·예외와 관련 링크의 위치, Personal·Project·Work 책임이 이어지는지를 살폈다. 공통 정책·관리 기준과 관련 background는 앞선 반영에서 읽은 내용을 활용하고 공통화·계약/수명의 형성 맥락을 추가 대조했다. 모든 과거 원문·사례·스킬 실행의 전수 재검증은 아니다.

## 본문별 판단

| 점검한 대상 | 유지할 점과 보완 후보 |
| --- | --- |
| [Personal 공통 관점](../../../../reference-project/context/personal/development/INDEX.md) | 짧은 문단과 강조가 책임·코드 명료함·조건별 적용을 연결한다. 여러 판단의 공통 방향을 설명하므로 별도 ‘첫 갈림길’ 표를 억지로 만들 필요는 작다. |
| [이름·완료](../../../../reference-project/context/personal/development/naming-and-completion/INDEX.md) | 조건·행동·선택 표로 판단을 찾고, 사례·background로 내려갈 수 있다. 가능한 한·검토·가능성의 강도를 복원한 현재판을 유지한다. |
| [코드 표현·진단](../../../../reference-project/context/personal/development/code-expression/INDEX.md) | 이미 적용 시점·핵심 규칙, 주석 판단 표, 실패 처리/추가 진단 표가 있다. 마지막 예외 문단도 금지의 이유와 범위를 설명하므로 형식 통일을 위해 전부 목록으로 바꿀 필요는 없다. |
| [공통화](../../../../reference-project/context/personal/development/shared-boundaries/INDEX.md#함께-제공할-필요와-달라질-부분을-찾는다) | 같은 API/업무 흐름의 비교 표와 실제 교체 계약을 확인하는 기준은 명확하다. 첫 절에서 ‘모든 화면에 필요하면 기본 구성 제공’, ‘일부 화면만 다르면 개별 조합 경로 가능’, ‘필요가 사라지면 축소·제거 가능’이 한 문단에 모여 있다. 이 세 조건을 찾기 쉽게 분리하는 것이 유력한 후속이다. 가능성을 의무로 바꾸거나 두 방식의 양립을 잃지 않아야 한다. |
| [계약·수명](../../../../reference-project/context/personal/development/contracts-and-lifetime/INDEX.md#같은-형태와-같은-의미를-함께-보장한다) | 오류 의미·적용 순서·시간의 시작/종료·지원 범위를 가르는 판단과 질문은 갖춰져 있다. 오류 발생 단계, 분류할 의미, 실제 catch 경계, 사용처의 대응 필요가 긴 문단들에 이어져 있으므로 조건과 확인할 일을 묶는 보완을 우선 검토할 만하다. 자원 수명 절의 기존 목록은 유지할 수 있다. 새 오류 클래스·자동 재시도·전면 표준화를 요구하는 방향으로 넓히지 않는다. |
| [prototype 기기 세션 의미](prototypes/development-workflow/noline-demo/context/project/common/device-session/INDEX.md) | 인증 복구와 데이터 보존의 이유를 설명하는 문단이 필요하다. 규칙만 남긴 표로 치환하면 의미 연결을 잃는다. 조건별 선택이 필요한 부분만 나누는 방식이 적절하다. |
| [prototype 인증 계약](prototypes/development-workflow/noline-demo/context/project/guidance/authentication-and-session/INDEX.md)·[표현 가이드](prototypes/development-workflow/noline-demo/context/project/guidance/code-readability/INDEX.md) | 사건·보존 상태·전달 결과·다음 행동, 소비자 조건별 대기 판단, 실제 callback 순서를 이미 표·번호·설명으로 구별한다. naming 형식을 다시 입히는 이득이 작다. |
| [prototype 인증 현황](prototypes/development-workflow/noline-demo/context/project/current/authentication-flow/INDEX.md) | 책임·현재 구현·완료 보장 표와 실제 코드, 구현하지 않은 범위를 함께 보여 준다. 규칙 본문과 다른 역할을 유지한다. |
| [Reference 제품 요구](../../../../reference-project/context/project/common/prd.md)·[현재 구조](../../../../reference-project/context/project/current/architecture.md) | timeout 계약의 목록, 구현 책임과 실행 순서, 검증 경계가 이미 나뉜다. Noline demo의 인증 의미를 이 제품에 복사하지 않은 상태도 유지한다. |
| 공통 형식·CONTENT-POLICY·SYSTEM-GUIDANCE·USAGE·Project 구성/관리 진입 | 형식, 본문/형성 자료 관리, 체계 지침 역할, 읽기 선택, 제품 주제 구성의 책임을 구별한다. 일반 제품 작업마다 모두 읽게 하는 경로를 추가하지 않았다. 이 지침들과 스킬 전체의 형식 확대는 여전히 별도 판단이다. |

## 정합성과 실제 검사

- Reference Personal의 Markdown50개를 prototype과 비교했다.44개는 동일하고6개의 차이를 직접 확인했다. 차이는 context-update 설치 경로, 사례의 Work 비교 출처 연결, Reference에서 관찰한 사건으로 오해하지 않게 한 provenance, 경험 모음의 대상 표현 등 기존 대상 적응이었다. 새 판단 누락으로 판정할 차이는 찾지 못했다.
- 이번 반영 receipt의 파일28개 해시가 실제 `02ea702c` 커밋 내용과 일치한다. 공유 문서의 병렬 hunk는 receipt의 선택 내용에서도 제외했다.
- prototype viewer 검사를 다시 실행해 원문/해시·경로/앵커·필수 연결과 화면 스크립트 확인을 통과했다. 문서/소스224개, 누락0이다.
- Reference의 영향받는 문서97개 링크·앵커 검사도 다시 통과했다. 새 형식 묶음에 바깥 로컬 경로 의존은 없으며, 기존 외부 형성 출처4개는 그대로 구별해 남겼다.
- Reference 작업 트리는 커밋 후 깨끗했고 Work·Maintain·제품·도구/스킬 보호 범위는 이전 snapshot과 동일하다. 병렬 작업이 이후 독립적으로 갱신한 상태를 이번 작업의 변경으로 되돌리거나 포함하지 않았다.

기계 확인의 기준과 판본은 [반영 receipt](receipts/reference-application/2026-10-30-writing-format-application.json)에 있다. 링크 통과와 Main의 읽기 결과를 새 AI 세션의 수행 신뢰성이나 사용자의 실제 이해 향상으로 확대하지 않는다. 제품 동작·브라우저 표시/클릭·host 통합 테스트는 새로 실행하지 않았다.

## 다음 선택

전반 점검 결과의 우선 후보는 공통화 첫 절과 계약·수명의 오류 처리 부분이다. 다른 기준이나 제품 설명까지 일괄 재작성할 근거는 부족하다. 후속으로 보완한다면 각각의 원본·background에서 판단·조건·강도를 고정한 뒤 해당 부분만 다듬고, prototype 확인 후 Reference로 연결한다. 이번 점검은 그 추가 반영을 수행한 상태가 아니다.

Maintain·Work 계약과 실제 host 통합 확인은 계속02, Noline의 현행 대조·재적용은06-02에 둔다. 전체06-01·Workspace 완료나 다른 티켓의 승인 상태는 바꾸지 않는다.
