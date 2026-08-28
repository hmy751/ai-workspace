# Workspace transition continuity memory

마지막 갱신: `2026-08-28`

## 목표

새 Workspace가 이전 작업의 후속일 때 필요한 현재 의미를 직접 소유하고 상세 근거만 선택적으로 참조하게 하는 생성·전환 canonical을 한 진입점에 응집하고, 이미 설치된 Project에서 그 canonical을 실행하는 repo-local skill을 제공한다.

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

- Workspace collection의 구조는 Reference의 `context/work/workspaces/README.md`, 생성·전환 책임은 같은 경계의 `CREATE-AND-TRANSITION.md`가 소유한다.
- Work 운영 지침은 새 Workspace 생성 요청을 repo-local `create-context-workspace` skill과 canonical로 routing한다.
- Skill은 의미 기준을 복제하지 않고 live canonical과 Workspace contract를 읽어 successor를 구성하고 bounded Recover만 받은 별도 주체의 재진입 검토를 시도한다.
- `apply-context-harness`는 최초 이식과 첫 Workspace를 계속 소유하며, 새 운영 skill과 target root routing을 이후 Workspace용 책임으로 설치·적응·제외한다.
- Recover·Maintain 문서는 누락 복구, Workspace 생성, 동기화와 Project context 승격이 자기 책임이 아님을 밝힌다.
- 이번 단계에서도 machine code, schema, hook과 deterministic 생성기는 추가하지 않는다. Skill은 모델이 canonical을 적용하는 교체 가능한 실행 adapter다.
- `memory-harness-research`는 후속 적용 전까지 읽기 근거일 뿐 수정하지 않는다.
- 이전 문서 계약은 사용자 요청에 따라 commit `1a4a9ff`로 먼저 분리했다. 현재 skill 변경은 별도 working tree 변경으로 유지한다.
- 격리 forward test는 successor current의 직접 의미와 exact 원문 접근점, predecessor·index·binding 불변과 packet-only 재진입을 확인했다. 이 결과는 actual target discovery·활성화나 모든 후속 goal의 의미 충분성을 보장하지 않는다.
