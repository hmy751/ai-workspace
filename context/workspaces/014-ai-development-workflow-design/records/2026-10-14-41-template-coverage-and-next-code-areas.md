# template의 조사 범위와 추가 논의 후보

2026-10-14. 01-02에서 탐색을 더 할 필요가 있는지 판단하기 위해 지정 템플릿의 컴포넌트 밖 코드와 메모를 확인했다. 실행·수정은 하지 않았다.

사용자:

> 근데 template에 컴포넌트 말고도 여러 코드가 있는데 더 논의가 필요하진 않은거야?

## 충분성 판단의 보정

기록 40은 컴포넌트 사례에서 얻은 기준으로 다음 초안을 만들 수 있다는 사실을, 추가 사례 탐색보다 구체화가 먼저라는 순서 판단으로 넓혔다. 다른 코드 영역의 대표성을 확인하지 않은 상태였다. 버튼 설계의 목적 연결이 흐려졌다는 정정은 다른 코드 영역의 탐색까지 불필요하다는 뜻이 아니다.

ai-self-check의 별도 report-only auditor는 바로 앞 교환과 상속된 대화를 보고 이 범위 전환을 확인했다. 컴포넌트에서 얻은 기준과 템플릿 전반의 충분성은 구별하고, 실제 코드의 주요 책임을 먼저 확인한 뒤 새 판단 차이가 있는 부분만 논의하도록 기준을 회수했다. 감사는 코드 탐색·파일 수정을 하지 않았으며 아래 코드는 Main이 읽었다.

## 실제로 남아 있는 범주

원자료는 `/Users/hammyeong-yeon/Desktop/20_lab/template`, 확인 HEAD는 `8a200e0`이다. src의 TS/TSX와 메모, package·설정, doc 파일 목록을 확인했다. App은 Hello React App 수준의 진입 예시다. 실행 코드와 문서 안의 설명용 예제를 구별한다.

| 범주·실제 파일 | 확인한 내용 | 추가로 판단할 가치 |
| --- | --- | --- |
| [useToastStore](/Users/hammyeong-yeon/Desktop/20_lab/template/src/store/useToastStore.ts), useAlertDialogStore, useConfirmDialogStore | 전역 store가 상태와 액션을 보관한다. Toast는 store에서 추가·삭제하고, ToastItem effect에서 타이머를 등록·정리한다. Confirm store에는 callback도 들어간다. | 무엇을 전역으로 공유할지, 상태 수명과 초기화, 데이터 변경 액션과 시간·외부 동작의 배치를 살필 수 있다. Confirm은 앞서 일부 봤으므로 Toast 연결이 우선 후보다. |
| [fetcher](/Users/hammyeong-yeon/Desktop/20_lab/template/src/api/fetcher.ts) | 공통 요청 옵션·타임아웃·응답 파싱·오류 표현·제네릭 반환을 묶는다. 앞서 실패 경로는 읽었다. | 공통 요청 계층의 계약, 개별 요청에 열어 둘 설정과 취소, 타입 선언과 실제 응답 확인의 경계를 더 살필 수 있다. 현재 동작을 아직 사용자 선호로 판단하지 않았다. |
| [useClickOutsideEffect](/Users/hammyeong-yeon/Desktop/20_lab/template/src/hooks/useClickOutsideEffect.ts), [useFloatingPosition](/Users/hammyeong-yeon/Desktop/20_lab/template/src/hooks/useFloatingPosition.ts) | DOM 이벤트 등록·해제와 외부 클릭 판별, 위치 계산·상태 변경·resize/scroll 처리가 있다. Dropdown·MultiSelect가 호출한다. | Hook 유무를 넘어 이벤트 수명·외부 환경 의존, 계산과 effect 분리, 재사용 입력 계약을 확인할 수 있다. |
| [날짜 계산 메모](/Users/hammyeong-yeon/Desktop/20_lab/template/src/utils/date.md) | 월 인덱스 변환, 기간 겹침, 달력 데이터 생성의 코드 예제가 있다. getCalendarDataWeeks의 일부 반환은 생략돼 있다. | 계산 함수의 입력·출력·경계값과 타입 표현을 볼 수 있다. 완성된 실행 유틸 구현으로 취급하지 않는다. |
| [React Query 메모](/Users/hammyeong-yeon/Desktop/20_lab/template/src/store/react-query/index.md) | 주문 mutation의 성공 callback이 캐시 무효화·장바구니 초기화·이동을 연결한다. Suspense·데이터 가공 예제도 있다. | 데이터 변경 이후 여러 효과를 어디에서 조율하는지 볼 수 있다. 문서 속 예제이며 실제 연결된 제품 기능은 아니다. |
| [Zustand 메모](/Users/hammyeong-yeon/Desktop/20_lab/template/src/store/zustand/index.md), doc/react-query/ | 액션 분리·slice·persist 등 상태 관리 예제와 서버 상태 가이드가 있다. | 실행 store의 실제 선택과 메모의 대안을 비교할 때 선택한다. 문서 권고를 사용자의 채택된 규칙이나 정확성이 검증된 API 설명으로 읽지 않는다. |

빌드 설정·Storybook·문서 표시 스크립트도 존재한다. 파일이 있다는 이유로 모두 다음 인터뷰 대상으로 올리지 않는다. 특히 doc/doc-script.js·doc/doc-filelist.js는 문서 표시용 코드로 확인되며, 작성 주체·역할 확인 없이 사용자 제품 설계 기준을 추출하지 않는다. 기존 미추적 doc/FORM_IMPLEMENTATION_GUIDE.md·doc/react-query/는 변경하지 않았다.

## 다음에 볼 대상과 이유

추가 논의할 가치가 있는 영역이 실제로 남아 있다. Main의 우선 추천은 **useToastStore와 그 호출·타이머 연결**이다. 기존 구현과 사용 예제가 모두 있고, 전역 상태의 범위·수명과 액션·부수 효과를 볼 수 있다. Toast의 시각 디자인이나 슬롯 API를 다시 설계하는 논의가 아니다.

그다음은 상태 논의에서 드러난 공백에 따라 요청 계층 또는 날짜 계산·데이터 변환을 선택할 수 있다. 모든 범주를 순서대로 인터뷰할 의무는 없다. Main이 코드에서 확인할 사실은 먼저 설명하고, 목적·선택 이유·상황 조건에서 결론을 바꾸는 부분만 사용자에게 묻는다. 이미 정리한 책임·합성 기준은 계속 활용하지만, 새 코드가 그 기준으로 충분히 설명되는지도 확인한다.

기록 40의 확보한 기준과 검토·수정 방법의 남은 작업은 유효하다. 다만 추가 탐색보다 초안을 먼저 만들자는 순서는 충분성 근거가 부족해 현재 기본 다음 행동에서 내린다. 01-02는 컴포넌트 중심으로 파악한 기준을 보존하면서 다른 코드 영역에서 새 판단이 필요한지 탐색하는 상태다. 사용자 선호 수집뿐 아니라 실제 책임 배치·변경 조건·판단 근거의 복원이라는 목적을 유지한다.

## 확인 범위

코드 읽기·호출 위치 검색과 별도 판단 회수만 수행했다. 템플릿 설치·런타임 실행·코드 수정·커밋은 없다. Workspace의 현재 진입점과 충분성 판단을 갱신했다. 문서 링크·공백 확인은 state에 남긴다.

2026-10-19 보존 경로 보완: 당시 state에 남겼던 이 기록의 문서 검사 결과는 [81의 당시 검증 이력 보존 절](2026-10-19-81-personal-context-direction-and-next-step.md#이전-state에서-옮긴-당시-검증-이력)으로 옮겨 보존했다. 위 문장의 실행·검사 범위와 당시 상태를 바꾸는 것은 아니다.
