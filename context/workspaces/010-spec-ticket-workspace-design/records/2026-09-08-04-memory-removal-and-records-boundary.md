# memory 폴더 제거 후보와 records·current 경계 재검토

날짜: 2026-09-08

## 대화의 진행과 현재 지위

[Ticket 외부 용례 조사](2026-09-08-03-ticket-references-and-placement.md) 뒤 사용자는 Ticket을 state에 두어도 되는지 물었다. Main은 Ticket의 정의와 진행을 한 문서로 관리한다면 state 배치도 타당하고, 정의를 memory에 두고 진행을 분리하는 안보다 인계가 간단할 수 있다고 설명했다.

사용자는 이어 memory·state 분류 자체를 재검토했다.

> 아 근데 그러면 state, memory 를 굳이 나눠야 하는 생각이드네 음

> 그럼 그냥 memory를 없애고 자연스레 유지되는 자룓ㄹ을 두고 나머지 현재 상황 판단은 state에 두고?

Main이 설명한 후보는 `current/`에 Spec·Tickets·project-context와 필요한 주제 문서를 직접 두고, state가 Workspace 전체 상황·판단·다음 행동을 맡는 구조다. Ticket별 진행은 Ticket에서 관리하며 state에 전체 목록의 상태를 중복 관리하지 않는다. 이때 `state.md`라는 파일 예시는 사람용 전체 상황 문서를 뜻하며, 기존 기계 status의 저장 위치까지 정한 것은 아니다.

사용자는 이 후보를 결정하기 전에 원래 records·current 구분에서 memory가 생긴 이유도 보자고 요청했다.

> 이게 메모리가 records current 분류하다가 나오기도 했던것 같은데 records를 감안해도제거해도 되는지 생각해보자

따라서 이전에 채택한 memory 배치는 현재 재검토 중이다. Spec의 다섯 구성요소·기존 goal/constraints 대체·project-context 유지·Workspace별 독립 스냅샷 조건은 재개방하지 않는다. memory 제거와 새 배치를 확정하거나 실제 Reference 구조를 바꾸지는 않았다.

## 기존 선택에서 확인한 역할

- [8월 12일 active/history 분리](../../001-reference-implementation/records/2026-08-12-02-active-history-separation.md): 작업 문서가 쌓일 때 현재 유효한 내용과 과거 작업 결과가 섞이는 문제에서 출발했다. 상세 내용은 history에 남기고, 현재 유효한 부분을 active에 반영했다.
- [8월 13일 current/records 명명](../../001-reference-implementation/records/2026-08-13-02-current-records-migration.md): records를 지속 가능한 문서·분석·중간 산출물·검증의 누적층으로 정했다. 완료 여부만으로 나누지 않고, 완료 후에도 다음 행동에 영향을 주는 효과와 후속 작업은 current에 남겼다.
- [같은 날 memory/state 합의](../../001-reference-implementation/records/2026-08-13-03-project-workspace-context-agreement.md): memory는 목표·기준·유지할 결정·제약·계속 영향을 주는 결과·선택한 Project 맥락, state는 현재 문제·진행·근거·불확실성·다음 행동을 맡았다. 특히 “상세 과정과 근거는 records에 남기고, 그중 계속 유효한 효과만 memory에, 현재 후속 행동만 state에 압축한다”고 명시했다.
- [같은 날 폴더화](../../001-reference-implementation/records/2026-08-13-05-workspace-current-folder-migration.md): 주제별로 내용을 늘릴 수 있게 memory·state를 파일에서 폴더로 바꿨다. 의미 구분과 폴더화는 별도 선택이며, memory에 모든 과거를 쌓지 않는 조건을 유지했다.
- [8월 14일 최소 memory](../../001-reference-implementation/records/2026-08-14-01-workspace-source-layer-and-minimum-memory.md): goal·constraints·project-context 세 파일의 기본 읽기와 누락 검사를 추가했다. 이는 앞선 의미 구분을 구현한 당시 runtime 계약이다.
- [8월 14일 output/records 경계](../../001-reference-implementation/records/2026-08-14-02-workspace-output-layer-and-record-boundary.md): 현재 선택한 goal 산출물은 output에서 찾고, 후보 비교·선택 근거·시행착오·실행 검증은 records에서 찾는다. 오래 보존한다는 이유만으로 current 자료가 되지는 않는다.

위 문서의 해당 결정과 이유를 다시 읽었다. 당시 대화 원문 전체나 과거 runtime의 실제 동작을 재검증한 것은 아니다.

## records를 감안한 Main의 판단

**memory 폴더를 없앨 수는 있지만, records에서 현재에도 적용할 의미를 선택해 유지하는 역할은 남아야 한다.** 지금 제안에서는 Spec·Ticket·project-context와 필요한 current 주제 문서가 그 의미를 맡을 수 있다. 이는 폴더 제거의 타당성 판단이며 새 구조의 운영 효과가 입증됐다는 뜻은 아니다.

‘자연스럽게 유지되는 자료’라는 설명만으로는 부족하다. records의 분석과 판단 근거도 장기 보존되는 자료다. current에는 이 Workspace가 지금 기준·작업 정의·상태로 사용하는 내용이 있어야 한다. records에는 그 내용이 나온 분석·비교·실행·변경 경위를 남긴다. records에 있다는 이유로 틀렸거나 효력이 없다는 뜻도, 최신 record라는 이유로 채택됐다는 뜻도 아니다.

예를 들어 예외 조건을 누락한 답변을 발견했다면, 당시 자료와 응답·분석 과정은 records에 남는다. 이후에도 지킬 조건은 Spec의 해당 항목과 이유에 반영하고, 수정할 Ticket은 작업 범위·완료 조건·현재 상태를 유지한다. state는 이 문제가 전체 목표 판단과 다음 행동에 어떤 영향을 주는지 다룬다. 이후 세션이 records를 처음부터 다시 해석해야만 유효한 조건을 알 수 있어서는 안 된다.

현재 문서에는 적용할 내용과 이해에 필요한 이유를 남기고, 상세 근거를 records로 연결한다. 반대로 모든 분석 문서를 current에 복사하거나 Ticket·state에 시간순 작업 일지를 누적하면 current가 다시 records와 겹친다. Spec 밖에 지속할 판단이 있다면 그 내용의 역할에 맞는 current 문서에서 소유해야 하며 state의 긴 과거 기록이나 records 링크만으로 대신하지 않는다.

완료된 Ticket은 후속 Ticket의 의존 관계·범위·결과 판단에 필요하면 현재 구성에 남을 수 있다. 완료만으로 자동 records 이동이나 삭제를 정하지 않는다. Workspace 전체가 스냅샷처럼 남는 기존 조건도 유지한다. 내부 자료를 후속 Project 변화에 맞춰 영구적으로 최신화한다는 뜻이 아니다.

memory를 유지하면 지속할 현재 의미를 모으는 공통 위치가 명확하다. 제거하면 Spec·Ticket을 다시 memory/state로 분류하거나 나누는 비용을 줄인다. 대신 current의 진입점과 운영 지침에서 어떤 자료가 현재 기준이고 무엇을 읽고 갱신해야 하는지 찾을 수 있어야 한다. 관리 규칙은 기존 Workspace 책임 문서가 소유하며 Spec 본문에 반복하지 않는다.

## 남은 결정

memory 폴더를 실제로 제거할지, current 아래 문서들의 관계와 읽기·갱신 책임을 어떻게 정할지가 다음 결정이다. Ticket 구성·진행과 전체 state의 관계도 이 배치에 맞춰 이어간다. 이번 작업은 010의 분석·재진입 기록만 갱신했으며 Reference·Recover·Maintain·Verify·hook·schema를 변경하지 않았다.

## 후속 교환: 유지안과 제3 리뷰 요청

사용자는 위 설명 뒤 다음과 같이 물었다.

> 그럴거면 memory 유지하고 그안에두면 되지않나?

Main은 “방금 내가 확인한 것은 ‘memory를 없어도 되게 만들 수 있다’는 것이었는데, 그것만으로 제거하는 편이 더 낫다고 결론 낸 건 성급했어”라고 답했다. 이어 memory에 Spec·Ticket·project-context를 두고, Ticket의 정의와 진행을 함께 관리하며 state가 전체 상황·판단을 맡는 안을 추천했다. Main의 이 추천 변화도 후속 검토 대상이며 사용자 채택은 아니다.

> 그럼 마지막으로 이상황을 제3리뷰한테 줘봐 필요한 근거 논의들 줘서

사용자가 독립 검토를 요청했다. [제3 리뷰 기록](2026-09-08-05-memory-ticket-independent-review.md)에 입력·범위·결과와 Main의 채택 여부를 남긴다.
