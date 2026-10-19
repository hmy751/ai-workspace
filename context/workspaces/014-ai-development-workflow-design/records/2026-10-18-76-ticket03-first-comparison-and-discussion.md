# 03 시작 — 기존 Project 본문과 읽기·갱신을 대조한 첫 논의

2026-10-18. 사용자는01-02 기록을 확인한 뒤 다음을 요청했다.

> 그래 이제 03 시작하자 01-02에 이어서 어떻게 하면 좋을지 얘기해봐

03과04-03의 Project 읽기·갱신 부분을 시작했다. 이번에는 보존된 실제 문서와 스킬의 첫 대조를 수행하고 논의 방법을 제안한다. 대표 본문을 새로 작성하거나 문서 배치·스킬 변경안을 채택한 단계는 아니다.01-02는 중간 정리·미완료로 유지한다.

## 기존 구성에서 확인한 출발점

| 보존 자료 | 실제로 제공하는 내용 | 03에서 이어서 판단할 부분 |
| --- | --- | --- |
| [Noline Project 입구](../source/noline-baseline/context/project/README.md), [Reference 구성 기준](../source/ai-workspace-baseline/reference-project/context/project/REFERENCE/composition.md) | 제품 의미·현재 구조·개발 가이드·선택 이유를 구별하며, 작업 주제에서 본문으로 가는 읽기 안내가 있다. 별도 파일은 읽는 상황·의미·갱신 책임의 이점으로 판단한다. | 기존 분류가 실제 본문을 이해하고 사용하는 데 충분한지,01-02 기준과 사례를 더할 때 어떤 내용을 유지·통합·보완할지 본다. 현재 폴더 이름을 최종 답으로 고정하지 않는다. |
| [제품 본문](../source/noline-baseline/context/project/common/product.md), [날짜 의미](../source/noline-baseline/context/project/common/date-and-time.md), [현재 구조](../source/noline-baseline/context/project/current/architecture.md), [선택 이유](../source/noline-baseline/context/project/decisions/0001-selective-local-first.md) | 오프라인 제품 장면, 데이터 관계, 시점과 달력 날짜의 차이, 코드·도구의 책임과 선택 근거를 설명한다. 날짜 본문에는 필드 의미뿐 아니라 호환·저장·응답 경계의 구체 계약도 함께 있다. | 각 본문에서 함께 이해해야 할 의미와 일부 작업에서만 필요한 상세를 구별한다. 상세하다는 이유만으로 분리하거나, 제품 이해를 다음 작업 요약으로 축소하지 않는다. |
| [API 변경 가이드](../source/noline-baseline/context/project/guidance/api-contracts.md), [동작 보존 리팩터링](../source/noline-baseline/context/project/guidance/behavior-preserving-refactoring.md) | schema·serializer·route 책임, 오류 전달, 동작 보존과 가독성 개선의 차이, 이름·간접 호출·수정 부담, 검사별 확인 범위를 이미 다룬다. |01-02의 일반 기준과 겹치는 내용이 있다. 기존 가이드가 충분한 부분과 일반화·보완할 부분, 제품 고유 계약을 구별한다. 별도 quality 본문을 추가하는 것만으로 해결됐다고 보지 않는다. |
| Noline·Reference의 [읽기 스킬](../source/noline-baseline/.claude/skills/read-project-context/SKILL.md)·[갱신 스킬](../source/noline-baseline/.claude/skills/update-project-context/SKILL.md), [읽기 기준](../source/noline-baseline/context/project/REFERENCE/reading.md)·[관리 계약](../source/noline-baseline/context/project/MAINTENANCE.md) | 필요한 본문을 선택·추가하고 이미 유효하게 읽은 맥락을 재사용한다. 지속되는 의미는 Project에 통합하고 작업 이력은 Work에 남긴다. 적용 조건·제품 계약을 스킬에 복제하지 않는다. | 이 기존 행동과 실제 본문을 연결해 어떤 작업 단서로 일반 기준·사례·제품 계약을 발견하고 적용하는지 본다. 가상 develop을 기존 스킬의 대체물로 전제하지 않는다. |

두 기준판의 읽기 스킬은 거의 같고 Noline에는 실제 구현 확인 때 app/package guide를 대조하는 설명이 추가돼 있다. 두 갱신 스킬의 차이는 링크 표기 수준이다. 이번 대조는 보존 본문의 계약을 확인한 것이며 실제 host 호출·읽기·적용 성공은 확인하지 않았다.

## 기존 문서 개선에서 보존할 이득

[문서 지침 전후 비교](../source/reading/noline-evaluation/reviews/document-guidance-followup.md)와 [별도 worktree 자료의 지위](../source/supplement/README.md)를 읽고 통화·기기 세션의 대표 본문을 대조했다.

통화는 [main 보존판](../source/noline-baseline/context/project/common/currency.md)보다 [worktree 관찰판](../source/supplement/worktree-project-context/context/project/common/currency.md)의 분량이 늘면서 기본 통화·실제 경비 통화·대표 표시의 관계, schema·DB·계산·표시의 정밀도 차이와 미정이 더 구별됐다. [기기 세션 관찰판](../source/supplement/worktree-project-context/context/project/common/device-session.md)은 로그인·로그아웃·삭제의 조건과 실패 위치별 결과를 가까이 배치했다. 유지할 이득은 짧은 분량 자체가 아니라 필요한 의미·조건·결과·예외를 이해하고 비교하기 쉬운 구성이다.

사용자의 긍정 평가는 첫11편 편집 직후이며 추가8편 전체나 장기 효과로 확대하지 않는다. main 평가판과 미커밋 worktree 관찰판은 서로 다른 자료이고, 보존된 worktree 전체가10월1일의 정확한 역사판이라는 증명도 없다.03에서 참고하되 최신 canonical로 합쳐 사용하지 않는다.

## 01-02에서 이어받는 의미

[72](2026-10-18-72-short-common-and-detail-prototype.md)의 짧은 공통·이름과 가독성 독립 절 반영 선택과 [73](2026-10-18-73-prototype-reservations-and-ticket03.md)의 전체 만족 유보를 함께 유지한다. 일반 기준·구체 사례·현재 제품 계약의 역할과 후보·채택의 지위는 별개다. 실제 Project 조건이 드러나면 기준의 추상도·설명량·분류·사례 연결까지 재판단할 수 있다.

필요한 판단에서는 [Field의 분리 의도35](2026-10-13-35-field-composition-and-design-flexibility.md), [Container의 다른 조건37](2026-10-14-37-infinite-scroll-container-and-hook-comparison.md), [형식 목표59](2026-10-16-59-format-design-objectives-advisor.md), [외부 비교61](2026-10-17-61-reference-comparison-for-format-design.md), [실제 적용 모습 요구63](2026-10-17-63-applied-criteria-project-example.md), [과정 재사용65](2026-10-18-65-criteria-status-and-cross-ticket-refinement.md), [공유 이득 재판단68](2026-10-18-68-principle-application-and-choice-basis.md)로 내려간다. 매 작업에 이 기록 전부를 읽히는 운영안을 만들지 않는다.

## Main이 제안하는 진행

먼저 Project가 제공할 전체 내용을 제품 이해·현재 구조와 계약·개발 판단·실행과 확인·선택 이유의 관계로 펼친다. 이 구분은 제공할 의미를 빠뜨리지 않기 위한 비교이며 새 폴더 다섯 개나 고정 목차의 제안이 아니다. 기존 본문에서 이미 충분한 내용과 새 기준을 연결할 부분을 드러낸다.

첫 대표 장면은 **공통 API 응답 처리를 수정하는 작업**을 추천한다. 기존 읽기 기준에도 있는 장면이며, 제품에서 값이 뜻하는 바와 현재 책임·계약, 일반 품질 판단, 검증 근거를 함께 사용할 수 있다. 예를 들어 날짜 필드를 포함한 응답이라면 시점과 달력 날짜의 제품 의미, schema·serializer·route의 현재 역할,01-02의 호출자가 믿을 계약과 책임 배치 관점을 대조할 수 있다. 이는 실제 버그 발견이나 Noline 수정 요청이 아니다.

이 장면에서 관련 본문 몇 편을 현재 모습과 보완 후보로 나란히 보여 주고, 필요한 뜻·조건·사례를 충분히 담았는지 논의한다. 외부 자료는61에서 비교한 의미와 조건을 함께 설명하기·필요할 때 찾아 읽기·작업 선택에 연결하기를 재사용한다. 외부 분류나 가상 shop-web의 배치를 그대로 복제하지 않는다.

이후 같은 내용을 구현자와 검토자가 어떤 요청에서 찾아 읽고 어떤 선택에 쓰는지04-03과 대입한다. 바뀐 것이 일반 기준인지, 제품의 현재 계약인지, 한 작업의 판단과 과정인지 구별해 갱신 위치도 연결한다. 다른 역할의 문서나 작업 장면에서도 성립하는지 확인한 뒤 전체 구성을 종합한다. 하나의 API 사례를03 전체 완료나 모든 문서의 의무 양식으로 올리지 않는다.

이 진행과 첫 사례는 이번 Main의 추천이다. 사용자가03 시작을 요청한 사실과 이 세부안의 채택은 구별한다. 다음 논의에서는 이 비교의 목적·범위와 첫 본문을 구체화하며, 실제 제품·스킬 개편은 아직 수행하지 않는다.

## 이번 확인 범위

Main은 Noline Project 입구·제품·날짜·구조·API·리팩터링·결정 본문과 Reference 구성 기준을 읽었다. 두 읽기 담당자는 지정 스킬·관리 기준 비교와 문서 개선 전후 비교를 각각 수행했다. 다른 담당자는 이미 읽은01-02 기록에서 넘겨받을 의미를 추출했다. 공개 웹이나 다른 Desktop 원본 저장소로 범위를 넓히지 않았고, source와 prototype은 변경하지 않았다. 이번 변경은03 시작 기록과 현재 진입 상태 갱신이다.

문서 확인: 변경·신규 Markdown10개의 로컬 링크 대상412곳이 존재했고 `git diff --check`를 통과했다. 이는 문서 연결·공백 확인이며 앵커 전체·제품 동작·스킬 호출·설계 효과를 검사한 결과는 아니다.
