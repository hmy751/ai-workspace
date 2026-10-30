# 06-01 — 본문 형식을 prototype에서 보완하고 Reference에 반영

**결과:** `3a28e6a1`의 형식 도입을 01-02 마감 판·관련 background와 대조해 보정하고, prototype 확인 뒤 Reference에 반영했다. 이름 기준의 내용·강도와 기존 제품·Work·Maintain은 유지했다. 전체06-01 완료나 실제 host 효과 확인은 아니다.

## 요청과 기준판

사용자는 형식 도입 커밋을 먼저 이해하고 적용 방향을 검토하도록 요청했다. 최종 문안의 강도, 초기 시안에 한정된 대조 기록, Project 작성 기준의 보존 범위를 설명한 뒤 다음과 같이 승인했다.

> 그래 그럼 프로토타입부터 보완하고 확인한 다음 Reference에 반영해봐. 기존 판단과 강도 잘 지키고 background잘 보고

- 형식 도입: `3a28e6a149bbada963f22d6916392f4b936e4036`.
- 판단 보존 원본: 01-02 마감 `6e6dccb8`. 형식 변경 직전 prototype과 이번 작업 시작 시 Reference의 이름 본문이 이 판본과 바이트 단위로 같았다.
- 직전 Reference 반영: `19225e0d`. 그때 제외한 형식 도입 차이를 이번에 처리했다.
- 작성·관리 기준: recall-document-guidance, 전역 지침 명확성·사람용 구성 기준, 각 대상의 CONTENT-POLICY·SYSTEM-GUIDANCE·Personal 관리·context-update와 Reference Project 작성 기준을 적용했다. 이름 기준의 형성 맥락·사용자 발화, 형식 도입의 맥락·근거·초기 대조표를 함께 확인했다.

## 보완과 반영

| 대상 | 바꾼 내용과 보존한 경계 |
| --- | --- |
| [prototype 형식 기준](prototypes/development-workflow/noline-demo/context/WRITING-FORMAT.md) | 파일명 대신 본문 역할로 범위를 구별했다. 실제 갈림길·순서·비교가 있을 때 형식을 고르고, 국소 조건과 필요한 사례 링크는 그 판단 곁에 둔다. 동일 목차·부정문 비율은 목표로 삼지 않는다. |
| [prototype 이름 본문](prototypes/development-workflow/noline-demo/context/personal/development/naming-and-completion/INDEX.md) | “가능한 한”과 기존 코드에서도 명료함을 살피는 조건을 복원했다. 반환·예외를 이름 하나에 반드시 표현하라는 추가 의무를 제거하고, 출력 문구를 화면으로 좁힌 표현과 옵션 확인의 우선순위 표현 등을 보정했다. 상수·주석·상태·대기·동작 수정과 두 코드 블록은 유지했다. |
| [최종판 대조](prototypes/development-workflow/noline-demo/context/_background/writing-format/records/2026-10-30-format-preservation.md) | 최신 원본 전체와 문장·조건·강도를 직접 대조했다. 초기 57개 판단의 대조는 과거 시안에 한정되므로 최종판 확인과 구별했다. 원본/결과 해시와 대표 질문을 남겼다. |
| [형식의 형성 자료](prototypes/development-workflow/noline-demo/context/_background/writing-format/README.md) | 원인 분석의 관찰과 인과 가설을 구별하고 보완 이유·사용자 요청을 보존했다. 바깥 실험 경로는 출처 식별자로 남기고 필요한 근거·대조는 가까이 배치했다. 이름 기준 자체의 background는 변경하지 않았다. |
| [초기 실험 기록](experiments/principle-readability-2026-10-29/README.md) | 당시 시안·판단·수치는 그대로 두고 최신 대조로 가는 후속 판본 안내만 추가했다. |
| [Reference 형식 기준](../../../../reference-project/context/WRITING-FORMAT.md)·[이름 본문](../../../../reference-project/context/personal/development/naming-and-completion/INDEX.md) | 확인한 prototype의 두 본문과 형성 자료를 반영했다. root·context에서 작성 시 찾도록 연결하고, 형성 자료 입구에는 prototype 당시 선택과 Reference의 현재 적용을 구별하는 안내를 더했다. |
| [Reference Project 작성 기준](../../../../reference-project/context/project/REFERENCE/composition.md) | 중복된 기준 본문의 형식 안내만 공통 지침으로 연결했다. 제품 의미·이유·예외를 함께 구성하는 책임, 제품 설명의 읽기 흐름, 주제·층별 책임·근거 범위는 유지했다. |

Reference 안의 현재 배치와 형성 근거는 [대상 반영 기록](../../../../reference-project/context/_background/records/2026-10-30-writing-format-application.md)에서도 읽을 수 있다. 전체 작업 기록을 Reference에 복제하지 않았다.

## 실제 확인

기계 결과와 최종 파일 해시는 [receipt](receipts/reference-application/2026-10-30-writing-format-application.json)에 보존했다.

- **판단·강도:** Main이 원본 전체와 보정본을 대조했다. 문자열 isError, 저장 후 조회, 반복 방어와 상태 표현, 같은 값의 상수, 필요한 결과 누락의 다섯 질문에서 같은 조건별 판단을 찾았다. 독립 세션 비교 실험은 아니다.
- **코드 예시:** 이름 본문의 두 코드 블록이 `6e6dccb8`와 동일하다.
- **prototype 표시 사본:** 기존 로컬 marked 모듈로 [viewer](prototypes/development-workflow/viewer.html)를 재생성했다. 검사에서 문서·소스224개(코드5개)의 원문/해시 일치, 내부 링크1298개·앵커317개, 필수 연결13개와 화면 스크립트 구문을 확인했고 누락0이었다. 제품 검사 수가 아니다. 브라우저 표시·클릭은 실행하지 않았다.
- **Reference 경로:** 영향받는 진입·Personal·Project·공통 형성 자료97개 문서의 로컬 링크641개·앵커194개를 확인했다. 누락0. 이번에 도입한 자료에는 Reference 밖 로컬 링크가 없다. 기존 형성 출처 링크4개는 원래 파일/해시 그대로 보존한 외부 provenance로 구별했다.
- **읽기 경로:** root 또는 context-update의 기존 대상 입구에서 형식 적용 범위로, 이름 본문에서 필요한 사례·형성 맥락·최종 대조로 이동해 현재 판단과 변경 이유를 찾았다. Project 작성 기준에서 새 형식과 기존 제품 설명 책임을 함께 확인했다.
- **변경 경계:** Reference Work·Maintain264개, 도구 설정·스킬64개, 제품 구현·검사13개, prototype Work26개의 파일·symlink가 시작 시점과 같고 추가 파일도 없다. 각 수치는 보호 범위 파일 수이며 실행한 검사 수가 아니다. 시작 시점에 별도 변경이 있던 추적 문서7개도 아래 직접 갱신한 공유 상태를 제외하고 해시가 같다. 기존 미추적 병렬 기록에는 쓰지 않았다.
- **형식:** `git diff --check` 통과.

## 후속과 한계

반영한 것은 본문 형식과 이름 기준 하나, 관련 형성 근거·읽기 경로다. 다른 Personal 본문·Project 제품 사실·Work·스킬 전체를 새 형식으로 재작성하지 않았다. 새 AI 세션의 작성 효과·판단 동등성과 반복 사용의 일반 효과는 미확인이다. 통합 테스트와 Maintain 관련은 계속02에 두며 Noline에는 쓰지 않았다.06-02는 이번 Reference 판본과 기존 Noline 고유 기준을 대조해 이어간다.

공유 current/state의06-01 현황,06-01 Ticket, output의 반영 진입, records 색인만 이번 결과에 맞췄다. 병렬02 및06-02 문서의 기존 변경은 건드리지 않았다. 최초 반영 뒤에는 작업 트리에 두었고, 후속 사용자 요청으로 이번 변경과 기록만 골라 커밋한다.

## 후속 확인 — naming만 먼저 전환한 이유

사용자는 “근데 왜 naming 파일만 바꾼거야? 그게 적당해서?”라고 물었다. Main은 다른 본문이 충분하다고 비교·판정한 것이 아니라, 해당 커밋에서 실제 전환한 첫 사례가 naming이고 그 사례를 보완해 Reference에 옮기는 범위로 진행했다고 설명했다. 형식 지침·작성 경로는 공통으로 연결했지만 기존 본문 전체의 가독성 정비는 마치지 않았다.

후속 요청:

> 일단 기록할거 정리하고 커밋하고 전반적으로 한번 더 점검해봐 괜찮아지긴 한 것 같아

“괜찮아지긴 한 것 같아”는 이번 변화에 대한 잠정적인 긍정 반응으로 보존한다. 모든 본문의 충분성·최종 채택·실제 수행 효과가 확인됐다는 뜻으로 확대하지 않는다. 다음 점검에서는 나머지 기준과 Project 본문도 읽고 조건·행동이 묻힌 부분, 설명 흐름이 필요한 부분, 진입·형성 근거의 일치를 구별한다. naming의 모양을 일괄 복제하거나 Work·Maintain 보류를 해제하는 요청은 아니다.
