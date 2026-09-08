# Workspace 담당과 Ticket 실행자의 읽기·결과 전달 구상

날짜: 2026-09-08

## 사용자 발화

memory 배치와 Ticket 구성 방향을 정한 뒤, 남은 읽기·갱신 책임을 논의하면서 사용자는 다음과 같이 구상했다.

> 뭔가 전체 스펙과 워크스프이스 맡을거면 ticket을 읽을거고 ticket 실행자체는 독립 에이전트나 세션이 맡을것 같아

전체 Spec과 Workspace를 맡는 주체가 Ticket을 읽고 전체 작업을 조율하며, 개별 Ticket 실행은 별도 에이전트나 세션에 맡기는 방향으로 이해한다. 아직 agent 수, 모든 Ticket의 위임 의무, 매번 새 세션 생성, 각 파일의 쓰기 권한이나 자동 실행 방식을 정한 것은 아니다.

## 이 구상에 따른 Main의 읽기·결과 전달 제안

- **Workspace 전체 담당:** Spec, 전체 state, 선택한 Project 맥락과 Ticket들의 범위·관계·진행을 읽고 다음에 무엇을 맡길지 판단한다. 개별 결과를 전체 목표와 대조하고, 남은 문제나 Spec 재검토 필요를 판단한다.
- **Ticket 실행자:** 담당 Ticket의 정의·현재 상태를 중심으로, 관련 Spec 요구·제약·완료 기준과 필요한 Project 맥락·실제 코드·자료·선행 결과를 읽고 실행한다. Ticket만으로 모든 맥락이 완결된다고 가정하지 않으며 전체 Workspace 이력을 기본으로 복제하지 않는다.
- **결과 전달:** 실행자는 수행한 변경·확인한 결과·남은 문제와 상위 기준에 영향을 주는 발견을 전체 담당에게 돌려준다. 전체 담당은 그 의미를 종합해 다음 실행이나 기준 재검토를 판단한다. Ticket 완료가 Spec 전체 완료를 대신하지 않는다.

Ticket의 정의·진행을 같은 문서에 남기는 기존 결정과 양립한다. 실제로 누가 Ticket을 직접 갱신하고 누가 Spec·state에 결과를 반영할지, Recover·Maintain이 어느 역할을 지원할지는 후속 계약으로 남긴다. 고정된 읽기 파일 목록이나 새 위임 체계를 구현한 것은 아니다.

## 적용 범위

사용자의 운영 구상과 Main의 해석·제안을 구분해 기록했다. 실제 독립 에이전트나 새 세션 실행 요청으로 해석하지 않았으며, Reference·runtime·설정은 변경하지 않았다.

## 후속 확인: 기존 Workspace 진입에서 Spec도 함께 읽는다

사용자는 역할별 읽기 범위를 제안한 Main에게 기존 진입 흐름을 다시 확인하도록 했다.

> 근데 어차피 이전에도 진입할때 current 전체 읽지 않았나? 그럼 spec도 자연스레 읽어야 할것 같은데?

Main은 실제 [Recover 계약](../../../../reference-project/context/work/harness/recover/README.md)과 [memory 읽기 구현](../../../../reference-project/context/work/harness/recover/operation.py), sample memory index를 읽었다. 기존 Recover는 memory index와 바로 아래 Markdown 전체를 읽고 goal·constraints·project-context의 최소 구성을 확인하며, state index와 machine status도 함께 싣는다. 선택한 Project 문서와 output index도 포함한다. 임의 하위 폴더·링크된 원문·records 전체를 재귀적으로 읽는 방식은 아니다. 실제 실행이나 제품 검증은 하지 않았다.

이 흐름에서 기존 goal·constraints를 대체하는 Spec 본문도 Workspace 기본 진입에 포함하는 것이 자연스럽다. 같은 Workspace에 진입하는 Ticket 실행자 역시 Spec 전체와 현재 맥락을 기본으로 이해한 뒤 담당 Ticket 범위에 집중하는 방향으로 정리한다. 앞서 Main이 제안한 ‘관련 Spec만 선택해서 읽는 실행자’ 구상을 기본 읽기 정책으로 채택하지 않는다. 전체 담당과 실행자의 책임이 다르다는 사실만으로 공통 진입 맥락을 축소할 필요는 없다.

현재 구현은 memory 바로 아래 Markdown만 읽으므로, 새 `memory/spec/`의 다섯 본문을 기본 진입에 포함하도록 Recover를 수정하는 일은 실제 적용 단계에 남아 있다. 폴더를 두기만 하면 기존 코드가 자동으로 하위 Spec을 읽는다는 뜻은 아니다. 모든 Ticket 본문의 기본 포함 여부나 추가 자료의 읽기 세부 정책까지 이번 확인으로 확정하지 않는다.

## 후속 범위 조정: Ticket 실행자는 구상으로 열어 둔다

> ticket 실행자 범위는 그냥 열어둬 뭐 그정도 될것 같은데 일단

사용자는 Ticket 실행자의 구체적인 범위를 고정하지 않도록 했다. 전체 담당이 Spec·Workspace와 Ticket을 보고 개별 실행은 별도 에이전트나 세션이 맡을 수 있다는 정도의 구상으로 둔다. 위에서 Main이 설명한 Ticket 실행자의 읽기·실행 범위는 예시이며, Spec 전체 또는 일부를 반드시 읽힌다는 정책이나 고정된 실행 단위를 채택한 것이 아니다.

기존 Workspace 진입에 goal·constraints를 대체하는 Spec 본문을 포함하는 방향은 유지한다. Ticket 실행자에게 전달할 정확한 입력·작업 범위는 실제 위임 상황에 맞춰 정할 수 있도록 열어 둔다. 이 범위를 지금 확정하는 절차를 다음 설계의 선행 조건으로 두지 않는다.
