# TripProof 인지부채: 문제·설계·실행 후보

이 폴더는 AI의 응답·작업물·근거를 사람이 이해하고 자기 판단으로 다음 지시를 내리는 데 필요한 TripProof 연구와 실행 후보를 소유한다. 인지부채를 어려운 문장이나 정보량만의 문제로 좁히지 않으며, 이해 지원을 제품·코드 적합성 검토나 판단 연속성 전체의 해결책으로 확대하지 않는다.

현재 결과는 세 skill과 공통 설명·근거 기준을 담은 **미설치 v0**다. 두 차례 승인된 품질 보강을 포함하지만, 실제 사용 효과나 인지부채 감소를 검증한 것은 아니다.

## 먼저 읽을 것

1. [문제 분석과 해결 의무](03-integrated-causal-map-and-solution-obligations.md): 무엇이 손실됐고 이 연구가 어떤 책임까지 맡는가.
2. [현재 설계](05-current-solution-design.md): 왜 세 skill과 공통 기준을 선택했고, 무엇을 제공하며 무엇을 맡지 않는가.
3. [v0](v0/README.md): 현재 검토할 실행 파일과 출력 예시, 실제 설치 대상과 검토 자료의 차이.

현재 구성만 확인할 때는 설계나 v0에서 시작해도 된다. 모든 근거 문서를 순서대로 읽는 절차는 아니다. 실제 실행 지시는 `v0/payload/`가 소유하고, 긴 연구 분석을 매번 읽는 선행 조건으로 삼지 않는다.

## 이유를 다시 판단할 때 읽을 근거

- [자료별 근거와 한계](01-external-reference-insight-extraction.md): 각 자료의 원래 질문·직접 주장·이 연구의 적용·반대 근거와 증명 한계.
- [세 장면별 합성](02-three-scenes-reference-synthesis.md): 여러 자료를 함께 적용할 때의 설명 순서·종료·전환·비적용 판단. 외부 자료의 원문 자체나 현재 실행 절차가 아니다.
- [해결 후보 비교](04-integrated-solution-candidates.md): 사용자 요청, AI 자기 호출, 작업 경계 호출과 독립 finding의 차이. 현재 선택과 비채택 이유를 다시 검토할 근거.
- [구조 시각화 근거](06-work-artifact-briefing-visual-structure-analysis.md): 영상의 직접 근거와 조건부 구조 표현의 도출, 그림이 근거보다 강한 주장을 만들지 않게 하는 판단.

자료별 질문과 장면별 적용은 서로 다른 탐색 목적이므로 01·02를 각각 남긴다. 남은 여섯 분석 문서는 자료별 근거·장면별 합성·문제 분석·후보 비교·현재 설계·시각화 근거의 순서로 01~06을 붙였다. 이 배열이 모든 문서의 순차 정독을 요구하는 것은 아니다. 과거 기록의 번호와 현재 번호의 대응은 문서 이관 기록에서 확인한다.

## 기록과 현재 내용의 경계

이 폴더에는 지금도 필요한 문제 해석·선택 이유·근거와 한계가 남는다. 실제 검토 순서, 사용자 정정, 채택·기각·수정·검사 경위는 해당 작업의 records가 소유한다. 현재 선택의 중요한 이유를 과거 기록에서만 찾아야 하게 만들지는 않는다.

- [005 도출 당시 품질 검토·수정 경위](../../../workspaces/005-tripproof-cognitive-debt-skill/records/2026-09-06-01-package-quality-review-and-revision-history.md)
- [008의 후속 품질 리뷰·보강·채택·이식 기록](../../../workspaces/008-tripproof-cognitive-debt-package-adoption/records/README.md)
- [이번 문서 통합·이관과 이전 판본 접근](../../../workspaces/008-tripproof-cognitive-debt-package-adoption/records/2026-09-06-04-document-organization.md)

원문·번역·source별 분석의 canonical은 기존 `context/source/`와 `context/analysis/`다. 독립 연구 근거를 Workspace 기록에 일괄 이동하거나 복제하지 않는다. 통합 전 문서는 이관 기록의 고정 commit으로 다시 읽을 수 있다. 과거 리뷰의 입력 버전은 각 리뷰 기록의 기준을 별도로 따른다.

## 유지 책임

이 연구와 실행 후보의 현재 소유는 이 분석 폴더에 있다. 후속 작업인 [008 Workspace](../../../workspaces/008-tripproof-cognitive-debt-package-adoption/README.md)는 채택·수정·이식 판단과 작업 상태·기록을 맡고, 연구 본문이나 실행 파일을 Workspace에 복제하지 않는다.

설계 선택이 바뀌면 현재 설계와 실제 후보의 일치를 확인하고 변경 이유는 작업 기록에 남긴다. 연구 근거가 바뀌면 해당 분석과 그 근거에 의존한 설계를 재검토한다. 파일 수·작성 순서·최종이라는 이름만으로 문서를 보존하거나 제거하지 않는다. 보존 가치, 독립 문서의 필요와 기본 읽기 여부를 각각 판단한다.

실제 TripProof에 설치한 뒤의 canonical은 대상 Project의 원래 skill·guidance Owner다. 이 폴더의 존재, 문서 정리나 정적 검사를 실제 설치·발동·사용자 이해 개선의 증거로 취급하지 않는다.
