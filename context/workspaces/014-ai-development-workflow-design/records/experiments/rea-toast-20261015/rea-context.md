# REA를 보조 도구로 사용해 준비한 Toast 컨텍스트

2026-10-15. REA 6.5.0 CLI의 실제 결과를 읽고 작성했다. 런타임 검사 전에 고정한다. `direct-context.md`를 이미 읽은 Main의 순차 비교이므로 독립 해석 결과가 아니다. 아래에서 REA 결과로 얻은 것과 추가 원문·프레임워크 해석이 필요한 것을 구별한다.

## 도구가 제공한 근거

입력 12개 파일 중 TS/TSX 6개를 파싱했고 parse failure는 0이었다. semantic graph는 노드 506개, 관계 453개, unknown 139개를 기록했다. 이것은 구현 결함 수가 아니다. 입력 사본의 application graph coverage는 complete지만 semantic coverage는 unknown이므로 실행 의미를 모두 이해했다는 뜻이 아니다.

- **R1 — 경로 재접근:** store를 module seed로 조회해 관련 import·export·파일 관계를 얻었다. 파일별 hash와 원본 위치가 보존돼 있다. 양방향 조회는 이 작은 사본의 54개 application node와 55개 edge를 모두 반환했다. store와 무관한 UI 구현까지 포함하므로 이 결과 자체를 기능 설명으로 쓰지는 않는다.
- **R2 — 타이머 연결:** `src/component/Toast/index.tsx:33`의 setTimeout을 timer node로 식별한다. backward-provenance 조회는 생성 호출(33행)과 취소 호출(34행)을 `schedules-timer`, `cancels-timer` 두 관계로 연결했다. 첫 ownership 조회에서는 node 하나만 나왔고, 질문에 맞게 조회 방향을 바꾼 후 관계를 확인했다.
- **R3 — duration의 일부 흐름:** duration parameter를 seed로 조회하면 5개 node·4개 관계를 반환한다. 읽기·closure capture 등을 확인할 수 있으나 결과는 ambiguous다. timer의 `delay_milliseconds`는 null이다. story의 literal 3000을 seed로 한 최초 조회는 0 match/partial이었고, 도구가 값의 전체 전달 경로를 복원했다고 볼 수 없다.
- **R4 — 해석하지 못한 연결:** `addToast`, `removeToast` 호출 대상을 ambiguous/unsupported로 기록한다. `useToastStore`·`useEffect`·`createPortal`·Zustand `create`는 해당 소스 밖의 import이고 `set`에는 local initializer가 없다는 call-flow unknown이 남았다. property removeToast의 backward 조회는 node 하나·관계 0개이고, story의 addToast 인자에서 시작한 조회도 node 하나·관계 0개다.

## 개발에 사용할 설명과 추가 해석

REA가 연결한 타이머 생성·취소 위치에서 원문으로 돌아가면, effect의 setup이 삭제 예약을 만들고 반환 함수가 그 예약을 취소하는 것을 읽을 수 있다. 목록 추가·삭제 동작, 5000ms 기본값, story의 3000ms, portal 렌더링은 원문을 확인하고 React·Zustand 계약을 적용해 설명해야 한다. 이 해석을 REA가 자동으로 산출한 사실로 세지 않는다.

표시부가 사라질 때 store도 비워지는지, 재마운트 시 타이머가 어떻게 되는지는 위 관계만으로 확정되지 않는다. 원문과 프레임워크 계약을 함께 적용하면 직접 분석과 같은 가설 — store는 남고 표시부의 타이머는 취소되며 재마운트 시 전체 duration으로 재시작 — 에 도달한다. 실제 실행 전의 추론이다.

‘추가한 시각부터 만료’와 ‘표시된 뒤 일정 시간 유지’ 중 어떤 계약이 필요한지는 도구가 결정하지 않는다. 이 조건이 향후 상태·타이머 책임 변경의 판단점이며 사용자 요구 또는 제품 문서에서 확인해야 한다.

## 이번 방법이 더해 준 것

타이머의 생성·취소 관계, 파일 hash와 위치, 미확인 관계를 기계가 다시 조회할 수 있는 자료로 남겼다. 반면 직접 초안에 없던 핵심 동작·설계 조건은 이번 조회에서 추가 발견하지 못했다. 관계 저장의 이점과 개발 설명을 만드는 이점은 구별한다. React·Zustand 라이브러리 내부를 분석 입력에 포함하지 않은 조건과 해당 버전·질의 범위에 한정된 결과다.

## 원자료

`../../receipts/rea-toast-20261015/`의 `rea-analysis.json`, `summary.json`, `feature-store.json`, `timer-provenance.json`, `duration-parameter-influence.json`, `removeToast-provenance.json`, `addToast-argument-influence.json`에서 확인한다. `query-executions.json`에 성공한 8개 조회의 입력 선택·시간·출력 크기가 있다. API 입력 탐색과 첫 샌드박스 실패는 실제 준비 비용이지만, 결과 정확성의 결함으로 세지 않는다.
