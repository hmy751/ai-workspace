# Workspace transition continuity memory

마지막 갱신: `2026-09-01`

## 목표

새 Workspace가 이전 작업의 후속일 때 필요한 현재 의미를 직접 소유하고 상세 근거만 선택적으로 참조하게 하는 생성·전환 canonical을 유지하면서, Project-wide 자동 오연결 없이 session별 명시적 admission과 same-session Workspace 전환을 실제 host adapter에서 지원한다.

## 확정된 의미

- 문제는 `apply-context-harness`나 bounded Recover의 읽기 정의가 아니다. Workspace 내부 Owner 원칙에는 필요한 요소가 있었지만, 후속 Workspace를 만들 때 무엇을 현재 의미로 다시 서술할지 정하는 생성·전환 기준이 충분히 구체적이지 않았다.
- 후속 Workspace도 독립된 지속 단위다. 이전 Workspace의 문서나 current를 상속하지 않고 새 goal을 기준으로 의미를 다시 선별한다.
- 다음 세션의 goal·제약·첫 판단·현재 산출물 해석·다음 행동을 바꾸는 의미는 링크로 대신하지 않고 새 Workspace current의 적절한 Owner에 직접 적는다.
- 원문 전체가 기본 current에 불필요하지만 특정 판단 전에 읽어야 하면 원래 canonical을 source로 선택하고 current에도 exact 경로나 직접 링크, 그 역할, 필요한 이유와 읽을 시점을 남긴다.
- 이전 Workspace만 소유하는 선택 이유와 상세 과정은 exact output·record·source로 단방향 참조할 수 있지만 이전 Workspace를 수정·동기화하거나 successor가 자동 추종하게 하지 않는다.
- Workspace 밖 Project 전체에도 적용될 후보는 기존 Project context Owner와 domain canonical, source 권위가 Project-wide 적용을 뒷받침하는지 별도로 판단한다. 여러 Workspace가 사용했다는 이유만으로 자동 승격하지 않는다.
- Recover는 이미 선별된 bounded current를 읽고, Maintain은 explicit Workspace 하나의 변화만 관리한다. 둘 다 Workspace 생성·전환의 의미 선별이나 cross-Workspace 동기화를 소유하지 않는다.
- 실제 활성화는 새 Main session을 보편적으로 강제하지 않는다. 현재 binding과 Maintain의 처리 중·pending·failed 상태가 successor 판단에 미치는 영향을 먼저 확인하고, 관련 의미만 보완한 뒤 같은 Main session을 이어 갈지 새 session으로 격리할지 정한다. 같은 session을 이어 가면 현재 turn은 predecessor로 마감하고, successor의 explicit Recover와 새 Maintain grounding이 실제로 성공한 뒤 다음 작업을 시작한다.
- 새 Main session은 기본 unbound다. Active index, Project 기본값, `.codex/maintain.json`의 Workspace id나 대화 주제로 자동 가입시키지 않고, 사람과 main이 현재 작업에 Workspace를 명시한 경우에만 `CODEX_SESSION_ID`를 activate한다.
- 같은 outer session의 binding은 일회성 고정값이 아니라 generation 이력이다. Prompt와 Stop·worker는 접수 당시 generation·Workspace·semantic thread snapshot을 사용하고, successor grounding 성공 뒤 다음 prompt부터 새 generation을 쓴다. 실패하면 predecessor를 보존하며 A→B→A 반복 이동을 허용한다.
- 이전 generation의 late worker와 blocking failure는 자기 generation 안에 남는다. 관련 없는 pending의 존재는 successor 이동을 막지 않으며 runtime 삭제나 Project 공통 config 변경을 rebind 방법으로 사용하지 않는다.
- Session binding은 독립된 Harness peer가 아니라 Maintain의 host 연결·운영 truth를 담당하는 내부 하위 경계다. Maintain README가 Maintain 전체 정체성·범위와 내부 책임 관계를, `CREATE-AND-TRANSITION.md`가 새 Workspace를 왜·언제 만들고 successor로 전환할지의 의미 판단을, `SESSION-BINDING-AND-LIFECYCLE.md`가 explicit admission·generation·hook·worker·notice·민감 runtime lifecycle을 소유한다.

## 구현 경계

- Workspace collection의 구조는 Reference의 `context/work/workspaces/README.md`, 생성·전환 책임은 같은 경계의 `CREATE-AND-TRANSITION.md`가 소유한다.
- Work 운영 지침은 새 Workspace 생성 요청을 repo-local `create-context-workspace` skill과 canonical로 routing한다.
- Skill은 의미 기준을 복제하지 않고 live canonical과 Workspace contract를 읽어 successor를 구성하고 bounded Recover만 받은 별도 주체의 재진입 검토를 시도한다.
- `apply-context-harness`는 최초 이식과 첫 Workspace를 계속 소유하며, 새 운영 skill과 target root routing을 이후 Workspace용 책임으로 설치·적응·제외한다.
- Recover·Maintain 문서는 누락 복구, Workspace 생성, 동기화와 Project context 승격이 자기 책임이 아님을 밝힌다.
- 이번 단계는 Maintain host adapter와 session state를 schema v2로 확장하고 `status|activate|deactivate` control CLI와 회귀 테스트를 추가한다. Workspace 의미 선별과 새 Workspace 생성은 계속 canonical·skill 책임이며 deterministic 생성기는 추가하지 않는다.
- Session lifecycle의 문서 진입점 분리는 기존 기능 구현과 별개인 Owner 정렬이다. `host_adapter.py`, `codex_session.py`, `.codex` wrapper와 `maintain` runtime·CLI 이름을 이동하거나 바꾸지 않고, Maintain 내부에서 각 구현이 어느 계약을 집행하는지만 명시한다.
- `memory-harness-research`에는 2026-08-31 전환 규칙 재보정 때 root routing, canonical, repo-local skill과 Maintain 비소유 문구만 먼저 반영했고 당시에는 제품·연구 내용, Workspace current와 runtime을 범위 밖에 뒀다.
- 이전 문서 계약은 commit `1a4a9ff`, canonical·skill 응집은 `51c42fb`, 전환 규칙 재보정은 `338b51c`로 보존돼 있다. 사용자는 2026-09-01 session binding 구현과 target 적용을 검토해 commit을 승인했고, target 적용분은 commit `08a1f0b`로 보존됐다. Reference 변경은 이 Workspace current·records와 같은 commit에서 보존한다.
- 격리 forward test는 successor current의 직접 의미와 exact 원문 접근점, predecessor·index·binding 불변과 packet-only 재진입을 확인했다. 이 결과는 actual target discovery·활성화나 모든 후속 goal의 의미 충분성을 보장하지 않는다.
- 2026-08-31 재검토에서 기존 새-Main-session 절대 규칙은 current adapter의 미지원 상태에서 reviewer가 제시한 두 해결책 중 문서-only 범위에 맞춰 고른 보수적 경로였음을 확인했다. 사용자 결정이나 기술적 불가능으로 승격하지 않고 조건부 fallback으로 되돌렸다.
- 2026-09-01 구현은 schema v1 Project config를 migration 동안 읽기만 하고 새 session binding에는 사용하지 않는다. 기존 v1 `session.json`은 generation 1로 lazy 해석해 continuation과 delivery truth를 보존한다.
- `memory-harness-research`에는 v2 adapter와 설정·운영 문서를 적용하고 오연결 사고 session `01a05864-3539-7f92-91fa-71734ed867d0`만 명시적으로 deactivate했다. 기존 runtime 전체와 사용자의 연구 문서 변경은 보존했다.
- 2026-09-01 전체 책임 재검토에서는 session lifecycle을 별도 Harness로 떼는 안을 채택하지 않았다. 실제 binding runtime이 Maintain의 response-end 책임만 지원하고 Recover·Verify나 일반 Workspace routing의 독립 lifecycle을 소유하지 않으므로, 새 peer를 만들면 전체 행동 Owner를 오히려 분산시킨다고 판단했다.
