# 현재 상태

마지막 갱신: `2026-09-15`

## 준비 상태

- Workspace 013을 새로 만들고 범위·근거·설계·검증 계획을 기록했다.
- 루트 Workspace 색인에는 `prepared, inactive`로만 연결했다. active는 계속 `012-ai-workspace-publication`이다.
- Reference·Noline Maintain 코드, hook, binding, runtime과 모델 설정은 수정하지 않았다.
- AI-native moment reviewer의 Codex·Claude 상태 파일은 문서 작성 직전 모두 `enabled: false`였다. 설정을 쓰거나 자동 재활성화하는 작업은 하지 않았다.

## 확인된 문제

Maintain의 같은 semantic thread는 이전 의미뿐 아니라 전역 instruction, 과거 prompt·response, decision, 파일 읽기 요청과 도구 출력까지 함께 누적한다. 최근 Noline generation은 grounding 1회와 response-end 4회를 처리하면서 내부 모델 처리가 11회로 늘고 총 입력 1,382,751 token을 보고했다.

같은 thread에는 Codex 자동 compact도 실제 발생했다. compact 직전 입력은 245,929 token이었고, compact 처리 자체가 cache 없이 246,234 input token을 사용한 뒤 replacement history 9개로 줄었다. 다음 입력은 86,490 token으로 낮아졌지만 같은 root turn 전체 입력은 667,478 token이었다. 이는 자동 compact가 실행 불능을 늦추지만, compact 전 반복 비용과 compact 자체의 큰 uncached pass를 피하지 못한다는 근거다.

전체 해결된 Maintain effect 100건은 `no_change` 40, `updated` 54, `needs_user_decision` 6이었다. 60건이 변경 또는 사용자 판단을 요구했으므로 response-end를 표면 규칙으로 대량 skip하는 방식을 첫 개선으로 쓰지 않는다.

## 아직 확인할 것

- 전용 runner에서 일반 Codex instruction discovery를 어느 설정 경계까지 끌 수 있는지와 실제 첫-call token 차이
- 현재 Source와 Noline 적용본의 차이, Noline 고유 Claude hook과 evidence 연결 중 보존할 부분
- semantic checkpoint를 모델 출력만으로 만들지 않고 host의 generation, effect ID, Owner hash와 결합할 최소 schema
- rollover 전후 판단 동등성을 비교할 replay corpus와 사람이 검토할 대표 ambiguity·update 표본
- 모델 cycle 상한에 걸린 사건을 `needs_context`로 보존하고 다음 처리에서 안전하게 재개할 lifecycle

## 다음 행동

1. Source와 Noline의 현재 Maintain 코드를 대조하고 이번 범위의 preimage와 target-specific 차이를 고정한다.
2. 기존 effect와 원자료에서 replay fixture를 만들고 비용·정확성 baseline을 다시 산출한다.
3. Source에 사용량 receipt와 instruction isolation을 먼저 넣어 고정비를 측정한다.
4. batched Owner read와 response-end당 최대 2 model cycle을 구현한다.
5. 검증 가능한 semantic checkpoint와 bounded rollover를 구현하고 automatic compact 전후와 비교한다.
6. Reference 회귀·replay가 통과하면 이식 절차로 Noline에 적응하고 Noline host lifecycle을 별도로 검증한다.
7. 구조 개선 뒤에만 Sol high와 더 낮은 reasoning effort를 같은 fixture로 비교한다.

구현을 시작하기 전에는 Workspace를 활성화하지 않는다. 이후에도 activation은 구현·검증과 별개의 명시적 사용자 선택으로 남긴다.
