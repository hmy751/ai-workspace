# Noline Context Harness 적용 이후의 평가용 근거

**인터뷰와 보류했던 비교를 반영한 평가를 마쳤다.** 티켓·Work 기록은 이전 방식보다 재설명을 줄이고 편해졌다는 사용자 경험이 확인됐다. 구체적인 코드·설명 개선도 있었지만, 첫 결과와 보고의 충분성을 다시 요구해야 하는 문제는 남았다.

먼저 [Noline 구성의 성과와 한계](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/noline-assessment.md)를 읽으면 된다. 다음 논의는 [강연 대조와 개선 방향](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/improvement-directions.md)으로 이어진다. 실제 코드 품질과 첫 검토·설명, 적절한 시점의 기록 보완, 기존 문서 기준의 실제 적용을 제안하며 아직 제품·운영 스킬에 적용하지 않았다.

개발 근거 범위는 2026-09-04 최초 이식부터 2026-10-06 Ticket 06 종료까지다. 2026-10-11~12 [장면별 인터뷰](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/reviews/interview-20261012.md)를 별도 경험 근거로 반영했다. 기억이 불확실한 동기는 확정하지 않았고, 전체 시간·토큰 절감이나 스킬 단독 인과를 주장하지 않는다. 글로벌 문서 개선은 별도 워크트리의 결과와 main을 구별했다.

자체 평가는 실제 결과, 사람의 이해·결정, 반복 작업과 비용을 함께 본다. 07·09 연구는 설계 배경이며 판단 연속성만으로 성패를 결정하지 않는다. Maintainer 하네스는 평가·개선에서 제외하고 Work 기록은 포함한다. [강연의 독립 분석](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/lecture-perspective.md)은 Noline과 섞기 전 관점으로 보존했다. 전체 원문이나 89개 후보를 처음부터 읽을 필요는 없다.

| 확보한 것 | 범위와 의미 |
|---|---|
| 로컬 공개 대화 | 46개 세션, 4,156개 메시지. 자동 스킬 안내문과 명시적 서브에이전트 대화는 별도 처리했다. |
| Git | 이식 전 기준을 포함한 first-parent 85개 커밋. 그중 기준 이후 84개가 이식·후속 개발 범위다. |
| 문서 판본 | 선택한 경로 180개의 Git blob 472개와 연구 문서 32개. 같은 내용은 한 번 저장했다. |
| 의미 검토 | 본문 1,827,213자를 120개 구간으로 나눠 읽고 장면 후보 89개, 뚜렷한 후보로 고르지 않은 구간 29곳을 남겼다. |
| 인용 검증 | 최종 장면 인용 495개가 보존 원문의 정확한 부분문자열인지 확인했다. 메시지 위치·읽기 구간 누락 검사도 통과했다. |

장면 후보 수는 독립 사건 수, 문제 수, 성과 점수가 아니다. 하나의 흐름이 여러 관점과 batch에 걸쳐 있다. 문자 수도 토큰 수나 비용 절감률을 뜻하지 않는다.

## 현재 자료에서 드러난 평가 지점

- Ticket의 좁은 실행 범위와 사용자가 원한 개선 깊이가 어긋나, 구현·지침을 다시 검토한 장면이 있다.
- 설명 뒤 사용자가 구조를 자기 말로 재진술하고 다음 수정을 선택한 장면도 있다. 질문이 많다는 이유로 모두 이해 실패로 분류하지 않았다.
- 기록을 다음 세션이 활용한 흐름과, 기록이 있어도 중심 과제를 다시 설명해야 했던 흐름이 함께 있다.
- Ticket 06은 중간에 합의와 범위가 달라졌다. 사전 승인, 구현 결과를 본 뒤의 재판단, 철회를 함께 보존했다.
- 종료 직전에는 보류 문제·후속 작업·미실행 검증·원인 미확인 네트워크 오류를 설명한 뒤 마감 지시가 있었다. 범위 종료 선택과 기술적 미확정은 구분했다.

이 항목들은 초기 관찰이며 [평가 진입 문서](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/assessment-entry.md)는 장면을 찾는 경로다. 인터뷰로 보완한 현재 판정은 [자체 평가](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/noline-assessment.md)에서 확인한다. 원래 장면 후보를 최종 실패 목록으로 읽지 않는다.

## 의미 검토를 어떻게 점검했는가

스크립트가 추출·중복·출처 연결을 맡고, Sol high가 공개 대화 전체를 나눠 읽었다. Astra high는 기존 장면 분류를 보지 않고 내용과 무관하게 선정한 9개 원문 표본을 먼저 판단했다. 그 뒤 선정 장면 15개와 평범한 구간 3곳 등을 필요한 앞뒤 원문으로 대조했다. 이는 전체 장면의 독립 전수 검증은 아니다.

독립 검토 후 23개 필드를 보완했다. 사전 승인 경위, 사용자 평가의 주체, 테스트·구현의 보고 여부, 형식 채택과 내용 불만의 공존, 종료 선택과 오류 원인 미확정의 구분을 반영했다. 새로 연결한 인용 28개를 포함해 최종 인용 검사를 다시 통과했다. [독립 검토](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/reviews/semantic-audit.md) · [반영 내역](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/reviews/applied-review.json) · [기계 검증](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/reviews/validation.json)

## 읽는 순서

- [Noline 구성의 성과와 한계](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/noline-assessment.md): 현재 읽을 결론, 구성별 판정, 개입의 역할과 판단 한계.
- [강연 대조와 개선 방향](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/improvement-directions.md): 다음 개발 과제와 작은 운영 보완의 우선순위.
- [인터뷰와 원문 발췌](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/reviews/interview-20261012.md): 체감, 기억의 한계, 평가에 반영한 의미.
- 보류했던 비교: [철회·후속 코드](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/reviews/withdrawal-followup-comparison.md), [글로벌 문서 기준](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/reviews/document-guidance-followup.md), [기록 시점·재개](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/reviews/record-timing-followup.md).
- [강연과 관련 스킬의 독립 분석](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/lecture-perspective.md): 현재 읽을 요약, 자료별 관점, 원문 근거와 적용 한계.
- [평가를 시작할 다섯 흐름](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/assessment-entry.md): 핵심 장면, 짧은 원문, 다음 확인과 인터뷰 후보.
- [전체 장면 색인](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/scene-index.md): 89개 후보에서 [원문·관찰·해석·대안·미확정](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/scene-evidence.md)으로 이동.
- [대화 색인](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/session-index.md): 46개 공개 대화와 원본 위치.
- [수집 방법과 한계](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/method.md): 읽은 범위, 모델 배치, 원문과 해석의 구분.
- [Git 경계](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/inventory/git-provenance.md): 이식 전 상태, 후속 지침 변경, Ticket 01–06의 커밋 경계.
- [기존 collector 상태](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/inventory/collector-summary.md): 기록 생성에 실패한 222개 이벤트와 원문 접근 상태.
- [대화 추출 QA](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/inventory/extraction-audit.md): 자동 안내문 제외, 역할 구분, 중복·누락 점검.
- [문서 판본 색인](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/document-index.md): 당시 Spec·Ticket·지침과 연구 문서의 보존본.

`episodes/batch-*.json`과 `.md`는 의미 검토의 파생 결과다. 원문은 `corpus/`, 실제 입력 분할은 `packets/`, 독립 검토와 기계 검증은 `reviews/`에 있다. 독립 검토 전 산출물은 `reviews/pre-audit/`에 보존했다.

## 남은 한계

기존 collector의 697개 이벤트 중 222개는 파생 기록 생성에 실패했다. 원문 부재와 구별해 로컬 대화에서 보완했다. 이식 전에도 하네스가 있었고, 적용 뒤에도 지침이 바뀌었으므로 고정된 단일 개입의 전후 비교로 취급하지 않는다.

대화 속 코드·테스트·화면·기록 반영 보고를 전부 독립 재검증한 것은 아니다. 사용자 체감은 장면별 인터뷰로 보완했으며, 객관적인 부담 측정과 구별한다. 장기 이해 유지와 개별 스킬 인과는 미확인이다. 자세한 경계는 [수집 방법](/Users/hammyeong-yeon/Desktop/10_work/noline/artifacts/context-harness-review-20261011/method.md)에 있다.

이 작업에서는 이 artifact 폴더에만 파일을 썼으며 제품 코드와 collector 상태를 수정하거나 git commit을 만들지 않았다.
