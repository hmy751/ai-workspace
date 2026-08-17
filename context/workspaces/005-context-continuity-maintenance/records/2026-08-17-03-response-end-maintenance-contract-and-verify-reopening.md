# 응답 종료 Maintain 계약과 Verify 논의 재개

기록일: `2026-08-17`

## 이 기록의 경계

[Background maintenance framing](2026-08-17-02-context-continuity-and-background-maintenance-framing.md)의 마지막 미결정점이던 ambiguity 보고 시점부터, Maintain의 점검·갱신 기준을 닫고 Verify를 다시 논의하기로 한 시점까지를 보존한다. 이 기록은 합의된 운영 기준과 아직 구현되지 않은 구조를 구분하며, background runtime이나 Verify의 새 책임을 대신 확정하지 않는다.

## 최소 사용자 발화 근거

Ambiguity는 나중까지 쌓지 않아야 한다는 판단은 다음 발화에서 확정됐다.

> 애매하면 보고는 해야 될 것 같아 너무 쌓이는 것도 문제야
>
> 그정도는 보고 받아서 풀수 있게 하는게 맞아보여

사용자는 애매한 반영만 보류하고 무관한 작업은 계속하며, 현재 방향을 바꿀 위험이 있을 때만 main도 멈추는 안에 “그래 그정도로 하자”고 답했다. `current/state`, 장기 memory, 필요한 records와 확정 output routing의 자동 수정 범위에도 “그래 이정도 좋아”라고 확인했다.

Memory의 파일 수를 인위적으로 제한할 필요가 있는지에는 다음처럼 정정했다.

> 난 개인적으로 meory를 폴더로 계속 늘려도 상관 없다 생각해
>
> 그리고 index에 처리할거 아닌가? 구조 연결로? 그러면 색인처럼 확인할거라 그렇게 무리가 가나 싶어

매 응답 종료 점검은 다음 발화들로 명시됐다.

> matitnianer는 매 대화 세션 마다 계속 점검하고 해야돼 이건 이해 돼?
>
> 그래도 대화 응답 끝나면 점검하게 그래야 잘 유지될 것 같은데?

Main이 “매번 점검하지만 매번 문서를 수정하거나 records를 만들지는 않는다”고 확인하자 사용자는 다음처럼 재확인했다.

> 그러니까 매번 점검하는데 아까 나눈 기준들로 갱신하는거고 없으며 그냥 점검하고 지나가는거고 이게 맞는거 맞지?

Verify는 결론을 내리지 않고 다음 설계 주제로 돌렸다.

> 난 verify 도 더 얘기좀 나눴으면 좋겟어 지금 뭔가 과정이 되게 애매하고 그런것 같아서
>
> 일단 recover는 딱히 문제가 없었던것 같고 maintain에 대해서는 지금 얘기를 많이 나눴고

## 확정된 Maintain 운영 기준

### 점검과 write를 분리한다

- Background maintainer는 매 AI 응답 종료마다 활성화되어 그 응답에서 생긴 delta를 점검한다.
- 매번 활성화된다는 것은 매번 persistent file을 수정하거나 record를 만든다는 뜻이 아니다.
- Durable 변화가 없으면 아무것도 쓰지 않고 종료한다.
- 전체 history나 모든 records를 매번 다시 읽지 않고, 해당 응답 delta와 영향받을 가능성이 있는 Owner부터 확인한다.

### 명확한 변화의 자동 쓰기 범위

- 지금의 문제·상태·불확실성·다음 행동: `current/state`
- 작업 뒤에도 유지되는 명시적 장기 기준: memory
- 판단 과정·근거를 후속 작업에서 다시 볼 필요가 있는 중요한 사건: 필요한 경우 관련 변화를 하나로 집계한 record
- 이미 선택이 확정된 산출물의 경로·상태: `output/index`

Records는 모든 memory 항목의 필수 부속물이 아니다. 장기 기준만으로 충분하면 memory에 직접 유지하고, 판단 과정이나 근거를 다시 확인할 필요가 있을 때만 record를 만들고 memory에서 연결할 수 있다. 또한 매 응답마다 record를 하나씩 생성하지 않는다.

### Ambiguity는 즉시 올린다

- 의미, Owner, 장기성 또는 사용자 의도가 애매하면 durable write를 추측해서 실행하지 않고 즉시 짧게 보고한다.
- 답을 기다리는 동안 해당 반영만 보류하고 관련 없는 main 작업은 계속한다.
- Ambiguity가 현재 작업 방향 자체를 바꿀 수 있을 때만 main도 그 판단이 풀릴 때까지 멈춘다.
- 따라서 이전 record의 “급하지 않은 ambiguity는 자연스러운 경계까지 batch한다”는 후보는 채택하지 않았다.

### Memory는 크기보다 routing으로 관리한다

Memory 파일 수가 늘어나는 것 자체를 결함으로 보지 않는다. 새로운 장기 기준은 추가할 수 있으며, 기존 기준이 바뀐 경우에는 모순되는 이전 기준을 그대로 누적하기보다 현재 기준으로 교체·정합화한다.

향후 `memory/` 폴더와 index를 두어 책임과 읽을 조건을 연결하고, 재진입 시 index를 통해 현재 작업에 필요한 memory만 선택해 읽는 방향을 채택했다. 이는 방향 결정일 뿐 현재 단일 `current/memory.md`를 migration하거나 선택 read runtime을 구현한 결과가 아니다.

### 갱신 workflow도 구현 범위다

향후 maintainer 구현에는 다음 순서를 포함한다.

1. 이번 응답 delta에서 durable 후보를 분류한다.
2. 각 후보의 Context Owner와 허용된 write 대상을 선택한다.
3. Main 또는 다른 maintainer가 같은 파일을 바꿨는지 다시 확인해 stale overwrite를 막는다.
4. 명확한 변화만 해당 Owner에 쓴다.
5. 로컬 링크와 실제 상태가 맞는지 확인한다.
6. Ambiguity는 즉시, 자동 반영 결과는 정해진 보고 경계에 알린다.

Trigger, 동시 수정 감지 방식, 실패 후 재시도와 보고 경계의 구체 구현은 아직 정하지 않았다.

## Recover와 Verify의 현재 위치

Recover는 현재 별도 문제가 없는 것으로 유지한다. 이는 새로운 효과 검증이 아니라 이번 논의에서 추가 변경 요구가 나오지 않았다는 뜻이다.

현재 Verify는 claim, canonical basis, fixed product argv와 evidence path를 입력으로 받고, 입력 snapshot을 만든 뒤 명령을 실행해 append-only receipt와 machine status를 남긴다. 코드·context 문서의 의미 정합성을 판단하거나 `current/records`를 고치는 역할은 아니다.

사용자는 이 과정과 책임을 애매하게 느껴 더 논의하기로 했다. 다음 대화에서는 direct product test가 이미 통과한 뒤 Verify의 추가 책임을 다음 중 어디에 둘지 실제 workflow로 구체화한다.

1. 신뢰 가능한 경계에서 제품 명령을 다시 실행하고 handoff용 증거를 남긴다.
2. 실제 변경, `current`, 검증 주장과 test 범위의 의미 정합성을 판단한다.
3. 실행 증거와 의미 정합성을 모두 유지하되 서로 다른 책임으로 분리한다.

이 세 방향은 질문의 구조이며 어느 것도 승인된 결론이 아니다.

## 구현 전 남은 일

- Verify의 기대 역할과 일상 활성 시점 구체화
- Response-end trigger와 main을 막지 않는 실행 방식
- `memory/` 폴더의 Owner 분리와 index 선택 read 계약
- 동시 수정·stale overwrite 방어와 maintainer 실패 시 fallback
- 실제 효과를 판단할 main blocking time, stale current 발견과 handoff 지표

현재 재진입 커서는 [current state](../current/state.md)에 둔다.
