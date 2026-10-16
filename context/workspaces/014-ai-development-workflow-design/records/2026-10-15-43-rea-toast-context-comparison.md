# Toast에서 REA와 직접 분석으로 컨텍스트 준비하기

**보존 지위 — 참고 조사.** 2026-10-16 사용자 요청에 따라 이번 결과는 보조 도구를 이해하기 위한 조사 자료로만 남긴다. 아래 추천은 실험 당시의 해석이며 정식 도입·운영 기준·Ticket 진행으로 채택하지 않았다. [마무리 기록 46](2026-10-16-46-rea-reference-research-close.md).

2026-10-15. **이번 작은 React/Zustand 사례에서는 직접 코드 분석과 필요한 동작 검사가 개발 컨텍스트 준비에 더 적합했다.** REA는 타이머 생성·취소를 출처가 있는 관계로 저장하고 재조회하는 데 도움이 됐지만, 직접 분석에 없던 핵심 동작이나 설계 조건을 추가 발견하지 못했다. 분석 자료를 구조화하는 가치와 개발 판단에 바로 쓰이는 설명의 가치는 구별한다.

이것은 Main의 실험 후 추천이며 REA 미도입의 영구 결정이나 01-03 완료가 아니다. 동일 세션의 순차 비교이므로 독립 A/B 또는 속도·토큰 우열을 입증한 실험도 아니다.

후속: 사용자가 작은 코드로 일반화할 수 있는지 지적해 [무한 스크롤 실험 44](2026-10-15-44-rea-infinite-scroll-context-comparison.md)에서 전체 src와 더 연결된 기능으로 비교했다. 이 문서는 Toast의 당시 관찰로 유지한다.

## 요청과 실제 비교 범위

사용자:

> 그럼 template 코드 하나를 대상으로 REA 쓰는 거랑 그냥 직접 분석하는 거랑 실제로 비교해볼 수 있어? 컨텍스트 준비에 뭐가 더 도움이 되는지 보고 싶어

대상은 template의 Toast다. 핵심 3개 파일은 store 30줄, 표시 컴포넌트 53줄, story 40줄로 총 123줄이다. 로컬 UI 의존 파일과 package.json·tsconfig.json을 포함한 12개 파일, 11,253바이트를 동일 입력 사본으로 보존했다. 원본 HEAD는 `8a200e050debc355150b9a67f68b140214197f7f`이며 사본의 개별 hash를 보존했다. 이 수치는 분석 범위를 나타내며 코드 품질 점수가 아니다.

양쪽 질문은 호출·상태·표시·삭제 경로, 기본값·사용 계약, 상태·타이머 수명, 유지·변경 조건, 근거·미확인을 개발 컨텍스트로 준비하는 것이다.

1. 소스와 호출부를 직접 읽어 [직접 분석 초안](experiments/rea-toast-20261015/direct-context.md)을 먼저 작성하고 hash를 고정했다.
2. 공식 npm `rea-agents@6.5.0`을 `/tmp`에 설치했다. `setup`·전역 MCP·스킬 등록은 하지 않았다. 정적 분석 1회 성공 후 summary·feature trace·semantic trace 등 8개 조회를 실행했다.
3. [REA 보조 분석 초안](experiments/rea-toast-20261015/rea-context.md)을 작성·고정하고 양쪽에서 필요한 미확인 동작을 별도로 실행 검증했다.

완전한 실험 조건과 학습 효과의 한계는 [protocol](experiments/rea-toast-20261015/protocol.md)에 있다. 같은 Main이 앞서 Workspace의 Toast 설명도 읽었다. 두 번째 방법의 성공을 독립 발견으로 세지 않는다. 입력은 직접 선택한 작은 소스 묶음이며 전체 저장소나 설치 라이브러리 내부를 분석한 것은 아니다.

## 실제로 무엇이 달랐나

| 개발 컨텍스트에 필요한 내용 | 직접 분석에서 얻은 것 | REA 실행에서 얻은 것 |
| --- | --- | --- |
| 파일·책임 찾기 | store·Toast·ToastItem·story의 역할과 연결을 원문에서 설명 | import/export·파일 관계를 hash와 위치를 가진 graph로 보존. store 양방향 trace는 사본 전체 관계까지 포함 |
| 추가·삭제 동작 | 배열 추가, 내부 id 생성, id로 filter 삭제를 설명 | 선언·표현식·위치가 있으나 Zustand의 set과 selector 이후 액션 호출은 해석되지 않은 연결로 남음 |
| 타이머 생성·취소 | effect 33~35행에서 예약·cleanup·의존성을 읽음 | 같은 timer node에 `schedules-timer`·`cancels-timer`를 연결. 재조회 가능한 근거로 유용 |
| 기간의 실제 의미 | 기본값 5000ms, story 3000ms, 표시부 수명과의 관계를 설명 | timer delay 값은 null. duration parameter의 일부 읽기·capture 관계는 나오지만 결과 ambiguous |
| 표시부 제거·재마운트 | store 항목 유지와 전체 duration 재시작을 검증할 가설로 남김 | React effect·Zustand 계약의 해석은 추가 필요. 타이머 graph만으로 이 동작을 결론 내리지 못함 |
| 설계 변경 조건 | ‘추가 시각부터 만료’와 ‘표시 후 유지’의 차이를 판단점으로 제시 | 해당 제품 요구나 변경 판단은 도구 결과에 없고 AI·사람이 해석해야 함 |
| 근거 재사용 | 소스 위치와 설명을 작은 본문에 정리 | 동일 Evidence의 부분 조회, 원본 hash, 관계별 출처·unknown을 체계적으로 보존 |

REA에서 실제로 확인한 중요한 결과:

- 6개 TS/TSX 파일을 parse failure 없이 분석했다. semantic node 506개, relation 453개, unknown 139개를 보존했다. unknown은 버그 수가 아니며 해석 범위의 표시다.
- application graph의 complete와 semantic graph의 unknown이 구분된다. 소스 목록·구조를 다뤘다는 것과 실행 의미 전체를 이해했다는 것은 다르다.
- timer의 backward-provenance 조회는 node 3개와 생성·취소 관계 2개를 반환했다. ownership 조회에서는 관계가 없어서 목적에 맞게 질의를 바꿨다. 첫 조회의 빈 결과만으로 지원 불가라고 판단하지 않았다.
- removeToast property의 backward 조회는 node 1개·관계 0개였다. 전체 graph에는 `Call target removeToast has ambiguous or unsupported assignments.`가 남았다. addToast에서도 비슷한 미확인이 있었다.
- story의 3000 literal 조회는 match 0개/partial이었다. duration parameter를 찾아 재조회하면 5개 node·4개 관계가 나오지만 ambiguous였다. 이를 기간 전달의 완전한 복원으로 세지 않는다.

결과 원문은 [REA 분석](receipts/rea-toast-20261015/rea-analysis.json), [질의와 실행 수치](receipts/rea-toast-20261015/query-executions.json), [타이머 관계](receipts/rea-toast-20261015/timer-provenance.json), [duration 추적](receipts/rea-toast-20261015/duration-parameter-influence.json)에 있다. 코드 위치는 결과에서 `src/component/Toast/index.tsx` 33·34행으로 재접근할 수 있다.

## 양쪽 분석 뒤 수행한 동작 확인

원본과 같은 소스 사본을 메모리에서 TypeScript 변환해 실제 React 19.1.0·React DOM 19.1.0·Zustand 5.0.5로 실행했다. JSDOM과 가상 타이머를 사용했고 CSS는 class 이름만 대신했다. 브라우저의 실제 화면·레이아웃·실시간 스케줄링 acceptance는 아니다. 의존성은 manifest 범위 안의 고정 버전을 임시 설치했으며 기존 template 설치를 그대로 실행한 것은 아니다.

| 시나리오 | 확인한 결과 |
| --- | --- |
| 원본 story 버튼 클릭 | 목록과 DOM에 추가되고 2999ms에는 남으며 3000ms에 삭제됨 |
| duration 생략 | 4999ms에는 남으며 5000ms에 삭제됨 |
| duration 3000ms, 1000ms 후 표시부 제거 | 제거 뒤 10초가 더 지나도 store에 남음. 재마운트 후 2999ms에는 남고 3000ms에 삭제됨 |
| 표시부 없는 동안 추가 | 10초 후에도 store에 남음. 마운트 후 3000ms에 삭제됨 |

4개 모두 예상과 일치했다. 이는 직접 초안의 D7·D8 가설을 해당 환경에서 확인한 결과이며 REA가 실행한 검사가 아니다. 재마운트 정책이 제품 요구에 맞는지는 여전히 사용자·제품 맥락에서 판단해야 한다. [검사 코드](experiments/rea-toast-20261015/verify-runtime.cjs), [실제 결과](receipts/rea-toast-20261015/runtime-results.json)

## 비용과 도입 판단

REA 정적 분석 성공 실행은 약 4.19초였다. 전체 결과는 1,091,306바이트였으며 공식 summary 조회는 10,290바이트였다. 8개 후속 조회는 각각 약 0.44초 수준이었다. **1MB 전체를 AI에게 넣어야 한다는 뜻은 아니다.** summary와 선택 조회가 가능하다. 다만 이번 작은 소스에서는 결과의 질의 방법을 찾고 미확인을 해석하는 절차가 추가됐다.

첫 샌드박스 실행은 macOS process ownership helper 컴파일에서 실패했고, 권한을 갖춘 실행으로 성공했다. npm 네트워크 접근도 샌드박스 밖에서 수행했다. 설치·명령 탐색·환경 문제는 첫 사용 준비 비용이며 REA 분석 정확성의 결함으로 계산하지 않는다. 직접 분석의 인지 시간과 전체 작업 시간은 통제·계측하지 않았으므로 ‘몇 배 빠르다’는 결론을 내리지 않는다.

**실험 당시 Main의 제안(미채택):** 당시처럼 원본 소스와 사용 예시가 있고 특정 책임·계약을 논의하는 작업에서 직접 읽기·관련 문서·좁은 실행 검증으로 컨텍스트를 만드는 방식을 제안했다. 이번에 실제 효용이 컸던 추가 작업은 상태 수명 가설의 실행 확인이었다. REA의 구조화된 Evidence가 필요한 반복 관계 조사·배포 번들·소스 접근이 어려운 대상이 생기면 그 질문으로 다시 평가한다. 이 실험에서 큰 저장소의 탐색 누락 방지나 장기 재사용 비용을 측정한 것은 아니다.

조사 결과와 [컨텍스트 작성 참고 예시](experiments/rea-toast-20261015/prepared-context.md)는 이 실험의 참고 자료로 보존한다. 01-02·01-03·03의 공식 결과나 진행 근거로 편입하지 않는다.

## 재현과 보존

- [입력 manifest](receipts/rea-toast-20261015/input-manifest.json), [직접 초안 고정](receipts/rea-toast-20261015/direct-freeze.json), [REA 초안 고정](receipts/rea-toast-20261015/rea-context-freeze.json).
- [실험 실행기](experiments/rea-toast-20261015/reproduce.py)는 보존 입력을 REA로 분석하거나 저장된 질의를 재실행한다. 기본은 별도 `/tmp` 출력이어서 이번 증거를 덮어쓰지 않는다.
- [REA 설치 lock](receipts/rea-toast-20261015/rea-package-lock.json), [검사 의존성 lock](receipts/rea-toast-20261015/runtime-package-lock.json)에 실제 설치 버전과 integrity가 있다. 코드 사본과 분석 증거는 원본 변경 뒤에도 당시 판단을 재검토하기 위한 보존물이며 현재 template의 정본이 아니다.
- 원본 template 코드·기존 미커밋 파일·전역 MCP 설정은 변경하지 않았다. 기존 014 미커밋 문서를 보존하며 이번 기록과 필요한 진입 링크만 추가했다. 커밋은 만들지 않았다.

보존 확인: 입력 12개 파일의 원본·사본 hash와 고정 초안 2개의 hash가 일치한다. 별도 임시 폴더에서 재현 스크립트를 실행했으며 분석과 8개 조회 모두 처음과 동일한 Evidence ID를 반환했다. 관련 Markdown 11개에서 로컬 링크 190개의 대상 존재를 확인했고 `git diff --check`와 실행기 구문 검사를 통과했다. [검사 기록](receipts/rea-toast-20261015/validation.json)
