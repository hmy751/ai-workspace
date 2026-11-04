# Reference Project skills

이 디렉터리는 이 Project 안에서 개발 수행·경험 개선·작업의 생성·논의·재판단·설명과 Personal·Project 맥락의 한정 갱신을 수행하는 스킬 원본을 소유한다. 각 `SKILL.md`가 해당 스킬의 호출 조건·실행 방법을, `agents/openai.yaml`이 Codex 호출 설정을 소유한다. Project·Workspace의 지속 의미와 문서 관리 계약은 해당 context Owner에 남는다.

스킬을 작성하거나 의미·구성을 바꿀 때는 [스킬 관리 정책](SKILLS-CONTENT-POLICY.md)을 읽는다. 평소 스킬 실행에서 모든 형성 자료를 먼저 읽지는 않는다.

## 설치된 역할과 진입점

- [record-work](record-work/SKILL.md): 기록 요청·작업 정리 시 같은 담당자를 재사용해 원문 판단과 Work 직접 갱신을 수행한다. 읽을 대상·이유·조건이 달라졌다면 `recover.md`도 Work 기준에 맞춘다.

- [development](development/SKILL.md): 개발 요청의 요구·맥락·구현·개선 검토·검증·결과를 연결한다. 모든 요청에 고정 인원·단계를 요구하지 않는다.
- [improvement-loop](improvement-loop/SKILL.md): 사용자가 대화를 돌아보고 개선을 찾자고 요청했을 때 선택한 개선·한정 시도와 경험을 잇는다. 자동 마무리 루프가 아니다.

- [create-context-workspace](create-context-workspace/SKILL.md): 새 독립 Workspace의 초기 구성과 README·`recover.md`를 통한 재진입 검토. [생성·전환 계약](../../context/work/workspaces/CREATE-AND-TRANSITION.md)을 적용한다.
- [work-discussion](work-discussion/SKILL.md): 사용자가 직접 호출했을 때 Work의 결과·선택을 구체화하고 Spec에 연결한다. 일반 작업 대화에서 자동으로 인터뷰를 시작하지 않는다.
- [reconsider-work](reconsider-work/SKILL.md): 실제 결과·새 조건·변경 부담·막힘에 따라 현재 판단과 후속 행동을 다시 본다.

- [context-update](context-update/SKILL.md): 허용된 Personal·Project의 본문·형성 자료·읽기 경로를 한정 반영한다. Work의 기록 담당은 바꾸지 않는다.
- [explain](explain/SKILL.md): 개념·코드·결과·앞선 말의 뜻과 선택 이유를 실제 근거로 설명한다.

맥락 읽기는 별도 스킬 없이 [USAGE](../../context/USAGE.md)와 [Project 읽기 기준](../../context/project/REFERENCE/reading.md)을 사용한다.

위 목록은 역할을 찾는 색인이다. 상세 호출 조건과 설명·검토의 권한 경계는 각 스킬을 따른다. 고정 호출 순서나 모든 작업에서 실행하는 공통 workflow는 두지 않는다.

## Context와 문서 갱신

작업을 다루는 스킬은 root [AGENTS.md](../../AGENTS.md)와 [Work 갱신 계약](../../context/work/workspaces/spec-and-tickets/MAINTENANCE.md)을 따른다. 새 Workspace 초기 구성과 준비된 Workspace의 기록을 구별한다. [record-work](record-work/SKILL.md)는 필요할 때 같은 담당자를 호출해 원문 판단·직접 반영을 수행하며 문서 기준은 Work가 소유한다.

`work-discussion`과 `explain`은 각 호출 조건에서 [설명과 근거 기준](shared/explanation-and-evidence-criteria.md)을 읽는다. 기준의 범위·수명·제거 조건은 그 본문이 소유한다. `reconsider-work`나 모든 재개에 새 필수 입력으로 추가하지 않는다.

## 도구 연결과 이식

`record-work`, `development`, `improvement-loop`, `work-discussion`, `reconsider-work`, `explain`, `context-update`는 `.claude/skills/`와 `.codex/skills/`에서 같은 `.agents/skills/` 원본으로 연결한다. `create-context-workspace`는 root 라우팅으로 찾는다. 연결·설정의 존재만으로 실제 host 발견·호출·원문 접근·재사용·기록 효과를 입증하지 않는다. [공통 원문 접근](shared/conversation-source.md)은 improvement-loop와 record-work가 공유하되 각 스킬의 읽을 범위는 유지한다.

다른 Project에 이식할 때는 이 목록과 실제 디렉터리·호출 설정·연결·공통 기준을 함께 확인한다. 기존 동명 또는 같은 책임의 스킬과 비교해 설치·적응·제외를 정하고, 기존 guidance 색인을 병합한다. 이 색인과 스킬 본문이 다른 Project의 현재 제품 맥락을 소유하지 않는다.

스킬을 제거하거나 교체해도 Spec·Ticket·state와 Project·Workspace 운영 계약은 그대로 남는다. 관련 스킬·도구 연결·이 색인을 함께 정리하고, 공통 설명 기준은 해당 문서의 consumer와 제거 조건을 따른다.
