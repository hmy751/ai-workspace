# 개발 판단 — 공통 관점과 주제별 기준

여러 Project에서 가져갈 개인의 개발 판단을 제공한다. [공통 관점](index.md)은 책임·계약·코드 명료함을 보는 출발점을 설명하고, 아래 세 주제는 이번 쟁점에 적용할 기준과 조건별 사례를 소유한다. 필요한 판단에서 시작해 관련 본문을 고른다.

| 지금 판단할 일 | 시작 본문 | 선택 차이가 더 필요할 때 | 주제 구성·관리 |
| --- | --- | --- | --- |
| 공통 컴포넌트·Hook의 범위, 부품 교체, 같은 업무 흐름의 관련 개선 | [공통 제공과 사용처 선택](shared-boundaries/index.md) | [Field·Container·주문](shared-boundaries/index.cases.md) | [주제 안내](shared-boundaries/README.md) |
| 공통 오류의 형태·의미, 타이머·상태·자원 수명, 지원 범위 안 정확성 | [계약과 수명](contracts-and-lifetime/index.md) | [fetcher·Toast·이벤트 Hook](contracts-and-lifetime/index.cases.md) | [주제 안내](contracts-and-lifetime/README.md) |
| 함수·Hook이 맡은 일, 상태·오류의 표현, 반환·완료 알림 | [이름·책임·완료 범위](naming-and-completion/index.md) | [이름·완료 판단 사례](naming-and-completion/index.cases.md) | [주제 안내](naming-and-completion/README.md) |

일반 기준에서 판단할 조건을 잡고, 선택이 갈리는 이유가 더 필요할 때 관련 사례를 읽는다. 사례에는 확인한 코드의 동작과 비교를 위해 둔 가정을 구별했다. 가정한 사용처나 미정인 제품 조건이 현재 작업에서도 성립하는지 확인하며, 모든 주제와 사례를 기본 입력으로 만들지 않는다.

기준의 의미·조건을 고칠 때는 해당 주제 안내에서 관련 형성 자료를 찾는다. 현재 보존된 형성 자료는 [이름 기준의 background](naming-and-completion/background/README.md)에 있다. 공통 제공과 계약·수명에는 별도 형성 자료가 없으며, 사례를 과거 선택 기록으로 바꾸거나 빈 자료를 만들어 채우지 않았다.

이 영역의 구성·보존·갱신은 [공통 관리 원칙](../../CONTENT-POLICY.md)을 따른다. 개인 기준과 제품 계약·이번 작업의 책임 관계는 [Personal 안내](../README.md)에서 읽는다.
