# Noline demo context

이 context는 개인의 판단 기준과 협업 경험, 제품이 계속 지킬 의미, 각 작업의 현재 상태를 구별해 제공한다. 현재 담긴 대표 예제는 **로그인 함수·완료 알림이 인증 완료와 조회 갱신 완료를 혼동시키지 않게 하는 작업**이다. 실제 요청의 대상과 일반 재개의 기본 선택은 [Workspace 목록](work/workspaces/README.md)에서 구별한다.

| 필요한 것 | 시작점 | 담당하는 내용 |
| --- | --- | --- |
| 개인의 판단 기준과 협업 경험 | [personal](personal/README.md) | 적용할 기준·조건과 경험·현재 이해·열린 후보를 구별해 읽는다. |
| Noline demo의 제품 맥락 | [project](project/README.md) | 기기 세션의 의미, 인증 적용·조회 후속 실패 계약, 현재 예제의 구현 경계 |
| 이번 작업을 이어 가기 | [work](work/README.md) | 작업의 Spec·Ticket·현재 상태와 입력·결과·기록 |

Personal과 Project는 자기 내용만으로 담당 의미를 설명한다. 필요한 원문 선택·재사용·실물 대조는 [USAGE](USAGE.md)가 맡고, 개발 중 시점·역할·변화의 연결은 [development 스킬](../../skills/development/SKILL.md)이 맡는다. 이 context의 각 영역은 내용·권위·관리 기준을 계속 소유한다. Project가 개인 기준의 채택 목록을 관리하거나 개인 원문을 알아야 제품 계약을 이해할 수 있게 만들지 않는다.

| 이번 요청 | 이어갈 방법 |
| --- | --- |
| 맥락을 읽고 설명한다 | USAGE로 관련 본문·실물을 선택하고 필요한 답을 만든다. 전체 Work 인수나 갱신을 전제하지 않는다. |
| 기존 작업을 재개하거나 이번 상태를 정리한다 | [Work 지침](work/AGENTS.md)과 해당 Workspace의 현재 의미를 사용한다. |
| 사용자 요청으로 대화와 경험을 돌아보고 개선한다 | [improvement-loop](../../skills/improvement-loop/SKILL.md)로 현재 Main이 검토·선택·반영을 잇고 [경험 길잡이](personal/experience/README.md)를 함께 조회한다. |
| 확인한 의미를 Personal·Project에 반영한다 | 해당 영역의 관리 기준과 [context-update](../../skills/context-update/SKILL.md)를 사용한다. |
| 새 독립 목표의 Work를 만들거나 Work를 전환한다 | [Work 생성·전환 계약](work/workspaces/CREATE-AND-TRANSITION.md)과 요청된 생성의 [수행 스킬](../../skills/create-context-workspace/SKILL.md)을 사용한다. |

내용을 고칠 때에는 해당 영역에서 지속할 의미가 달라졌는지 먼저 판단한다. 이번 작업의 구현·검사 진행과 선택은 Work에, 여러 작업의 제품 이해·계약·구조·지원 제약의 변화는 Project에 남긴다. 기존 계약으로 충분하면 코드가 달라져도 Project 무수정으로 끝날 수 있다. 필요한 개인 기준의 변화는 Personal의 선택 권한과 관리 기준을 따른다. 운영 Harness·자동 hook은 이 demo에 연결하지 않았다.

Personal·Project·Work의 독립 책임과 같은 로컬 context에 둔 이유는 [형성 자료 안내](_background/README.md)에서 관련 맥락·기록·원문을 고른다. 이 자료는 현재 본문을 만든 이유를 복원하는 층이며, 평소 적용은 위 각 본문에서 시작한다.

Personal·Project와 공통 context의 본문·형성 자료를 구성하거나 수정할 때는 [본문과 형성 자료의 관리 원칙](CONTENT-POLICY.md)을 읽는다. 본문에서 나눈 상세·절차·사례의 배치와 형성 자료의 보존, 읽기·갱신 조건을 정한다. 그중 체계 지침을 새로 만들거나 진입·상세의 책임과 이름·위치를 바꿀 때는 [체계 지침의 역할과 구성](SYSTEM-GUIDANCE.md)을 함께 읽는다. 이 문서는 개발이나 문서 체계를 다루는 지침의 성격과 실제 본문·진입 역할을 구별한다.

본문을 새로 쓰거나 고칠 때는 [본문을 쓰는 형식](WRITING-FORMAT.md)에서 적용 범위와 문장·구성 기준을 확인한다.

**Work에 본문·형성 자료의 새 구성을 적용하는 일은 보류한다.** Work는 기존 Spec·Ticket·current·source·output·records와 갱신 제약을 유지하며, 그 체계와 형성 자료를 어떻게 다룰지는 별도로 논의한다. 일부 본문에 적용된 현재 배치가 모든 문서의 최종 분류를 뜻하지는 않는다.
