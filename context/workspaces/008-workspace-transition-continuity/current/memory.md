# Workspace transition continuity memory

마지막 갱신: `2026-08-28`

## 목표

새 Workspace가 이전 작업의 후속일 때 새 goal에 필요한 현재 의미를 직접 소유하고 상세 근거만 선택적으로 참조하게 하면서, 과거 Workspace 상속·상호 동기화·연쇄 Recover와 Project context 자동 승격을 막는 Reference 계약을 만든다.

## 확정된 의미

- 문제는 `apply-context-harness`나 bounded Recover의 읽기 정의가 아니다. Workspace 내부 Owner 원칙에는 필요한 요소가 있었지만, 후속 Workspace를 만들 때 무엇을 현재 의미로 다시 서술할지 정하는 생성·전환 기준이 충분히 구체적이지 않았다.
- 후속 Workspace도 독립된 지속 단위다. 이전 Workspace의 문서나 current를 상속하지 않고 새 goal을 기준으로 의미를 다시 선별한다.
- 다음 세션의 goal·제약·첫 판단·현재 산출물 해석·다음 행동을 바꾸는 의미는 링크로 대신하지 않고 새 Workspace current의 적절한 Owner에 직접 적는다.
- 원문 전체가 기본 current에 불필요하지만 특정 판단 전에 읽어야 하면 원래 canonical을 source로 선택하고 current에도 exact 경로나 직접 링크, 그 역할, 필요한 이유와 읽을 시점을 남긴다.
- 이전 Workspace만 소유하는 선택 이유와 상세 과정은 exact output·record·source로 단방향 참조할 수 있지만 이전 Workspace를 수정·동기화하거나 successor가 자동 추종하게 하지 않는다.
- Workspace 밖 Project 전체에도 적용될 후보는 기존 Project context Owner와 domain canonical, source 권위가 Project-wide 적용을 뒷받침하는지 별도로 판단한다. 여러 Workspace가 사용했다는 이유만으로 자동 승격하지 않는다.
- Recover는 이미 선별된 bounded current를 읽고, Maintain은 explicit Workspace 하나의 변화만 관리한다. 둘 다 Workspace 생성·전환의 의미 선별이나 cross-Workspace 동기화를 소유하지 않는다.
- 실제 활성화는 같은 Main session에서 binding만 바꾸는 동작이 아니다. 이전 session을 끝내고 successor binding을 맞춘 뒤 새 Main session이 explicit Recover와 Maintain grounding으로 시작한다.

## 구현 경계

- 의미 계약의 canonical은 Reference의 `context/work/workspaces/README.md`가 소유한다.
- Work 운영 지침은 AI가 이 canonical을 적용하도록 routing만 한다.
- Recover·Maintain 문서는 누락 복구, Workspace 생성, 동기화와 Project context 승격이 자기 책임이 아님을 밝힌다.
- 이번 단계에서는 문서 계약만 정리하고 code, schema, hook, skill과 자동 생성기는 추가하지 않는다.
- `memory-harness-research`는 후속 적용 전까지 읽기 근거일 뿐 수정하지 않는다.
- 사용자가 요청하지 않은 commit을 만들지 않는다.
