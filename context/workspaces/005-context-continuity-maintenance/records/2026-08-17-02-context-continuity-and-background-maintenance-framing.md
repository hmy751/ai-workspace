# Context continuity와 background maintenance framing

기록일: `2026-08-17`

## 이 기록이 보존하는 것

[운영 지연 진단](2026-08-17-01-harness-operation-latency-and-role-diagnosis.md) 뒤 이어진 다음 논의를 보존한다.

- Recover·Verify·Maintain을 없애지 않고 언제 실행할지
- `current/records`가 stale해지는 위험과 다른 세션 handoff
- 현업의 agent context·CI·provenance 흐름과 현재 시스템의 위치
- main을 막지 않는 background maintainer 아이디어
- 명확한 항목의 자동 반영, memory 축적 방지, 애매한 항목 보고 방식

## 사용자 발화의 최소 원문

정확한 판단 뉘앙스를 잃지 않도록 핵심 부분만 보존한다.

> 딱 지금 시스템 current records 에서 걱정되는건 C, E이고
>
> 평소 작업할 때 우려되는거 또는 힘들었던건 A, B, C, E정도일 것 같아

C에 관해 사용자는 “이거 자체가 깨지면 다 깨지는 것 같아서”라고 설명했다. E에 관해서는 “다른 세션이 들어오면 어느정도 유지는되어야 하지 않나”, “안 그럼 핸드오프가 안되잖아”라고 했다. Recover가 이미 일부 해결하는 것 같지만 current가 완벽하지 않다는 조건도 함께 말했다.

A에 관해서는 재조사가 가능하다고 보되 “너무 오래걸리거나 병목이면 안된다”, 현재 시스템이 있으니 “적절히 빨리 대처할수 있는 상태”여야 한다고 했다. B에 관해서는 100% 계속 유지하기 어렵고 대화 끝이나 적절한 타이밍, 중간중간의 갱신으로 어느 정도 유지할 수 있다고 보았다.

Verify와 test에 대해서는 다음 우려를 추가했다.

> 오히려 verify 에 막 테스트 쌓이는게 더 우려돼 나한테 마치 관심사가 좀 커진것 같은느낌이야

Background 방향에 대해서는 구현 지시가 아니라 rough idea로 다음을 제시했다.

> 에이전트를 지금처럼 두는데 maitian이든 다 커버하는 에이전트 든 다만 작업 끝나고 지금처럼 병목생기게 하는게 아니라 백그라운드에서 계속 알아서 작동해서 작업 적절히 하고 애매하면 보고하는 메인나와 작업에 집중하고

명확한 state 변화를 maintainer가 직접 쓰는 안에는 A를 선택했다. 이유는 매번 review하면 오래 걸리기 때문이다. 장기 memory도 A 쪽이지만 다음 조건을 붙였다.

> A이긴 한데 막 쌓이면 안되니까 뭔가 더 생각할 조건을 줘야할 것 같아 대화 맥락과 판단해서 추가하는?

이 발췌의 A/B/C/D/E는 앞선 대화의 선택지 라벨이다. 이 Workspace에는 원 선택지 문장 전체가 없으므로 라벨을 새 정의로 고정하지 않고 사용자가 직접 설명한 우려를 기준으로 유지한다.

## 우려의 현재 해석

### C가 E보다 선행한다

Recover는 handoff를 빠르게 만드는 reader다. `current`가 실제 상태와 맞아야 다른 세션이 올바르게 이어 갈 수 있다. 따라서 “Recover가 있으니 E는 해결됐는가”에 대한 현재 답은 “부분적으로만”이다. C의 freshness가 무너지면 E도 무너진다.

### A는 제거보다 시간 상한이 중요하다

새 세션이나 main이 필요한 원자료를 다시 조사하는 것 자체는 허용할 수 있다. 문제는 전체 history를 다시 읽거나 넓은 review가 동기식 gate가 되는 것이다. `current`는 조사 자체를 0으로 만드는 저장소가 아니라, 다음 조사 범위와 첫 행동을 짧게 만들어야 한다.

### B는 완벽한 실시간 정합성이 아니다

모든 발화마다 지속 문서를 갱신하면 비용과 noise가 폭증한다. 반대로 끝까지 미루면 stale risk가 커진다. 의미 있는 변화와 자연스러운 경계를 구분하는 cadence가 필요하다.

### Verify의 관심사 팽창을 막아야 한다

제품 test는 제품 코드와 제품 test suite가 소유한다. Verify는 선택된 claim에 필요한 기존 명령·근거와 실행 receipt를 연결한다. Harness 자체 회귀 test와 제품 test catalog를 Verify 문서 아래에 계속 축적하지 않는다.

## 현업 자료와의 대조

사용자는 현업 흐름을 main의 단독 의견으로 답하지 말고 subagent 조사와 독립 review를 거치라고 요청했다. 이에 2026-08-17에 agent context·memory 운영과 delivery·assurance 관점을 두 개의 bounded subagent 조사로 분리하고, 별도 reviewer가 과도한 일반화와 현재 구조의 과설계 가능성을 다시 점검했다. 아래 내용은 그 결과를 main이 종합한 AI 분석이며 사용자 결정이나 보편 표준으로 취급하지 않는다. 자료는 vendor marketing보다 1차 문서와 표준을 우선했다.

- [DORA Continuous Integration](https://dora.dev/capabilities/continuous-integration/): 작은 변경과 빠른 자동 피드백을 일상 개발 경계에 둔다.
- [DORA Streamlining Change Approval](https://dora.dev/capabilities/streamlining-change-approval/): 모든 변경에 무거운 외부 승인을 붙이기보다 위험과 자동화된 증거에 맞춰 승인 흐름을 줄이는 방향이다.
- [DORA 2024 Accelerate State of DevOps Report](https://dora.dev/research/2024/dora-report/2024-dora-accelerate-state-of-devops-report.pdf): AI-assisted delivery에서도 작은 batch, 빠른 feedback과 안정적인 delivery foundation이 함께 필요하다는 조사 배경을 제공한다.
- [NIST Secure Software Development Framework](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf): 검증과 증거를 소프트웨어 위험·책임 경계와 연결한다.
- [SLSA Source Track v1.2](https://slsa.dev/spec/v1.2/source-requirements)와 [Verification Summary Attestation](https://slsa.dev/spec/v1.2/verification_summary): source revision, artifact와 검증 결과의 durable provenance를 formal boundary에 둔다.
- [Anthropic의 managed agents 글](https://www.anthropic.com/engineering/managed-agents): 장시간 agent 작업에서 state persistence, isolation, handoff와 관찰 가능성이 중요하다고 설명한다.
- [Gemini CLI Auto Memory 문서](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/auto-memory.md): 자동 memory는 실험적 기능이며 review 가능한 변경과 사용자 통제를 전제로 한다.

이 자료들과 비교한 결론은 다음과 같다.

- Repo-scoped instruction, bounded context 복구, test/log/trace, human approval은 현업 방향과 맞는다.
- 빠른 direct test는 commit/PR 또는 반복 개발에, durable provenance는 source revision·build·release·handoff 같은 경계에 두는 편이 일반적이다.
- 현재 Verify의 snapshot-bound append-only receipt는 소규모 Project의 보편 관행보다 엄격한 audit 설계다. 하지만 signer/verifier identity, artifact subject, policy digest가 없으므로 SLSA VSA와 동일하다고 부르지 않는다.
- 의미 문서를 자동 갱신하는 Maintain은 아직 성숙한 공통 표준이 아니다. Auto memory도 review·edit 가능한 advisory context로 다루는 흐름이 강하다.
- 따라서 역할 분리 자체는 타당하지만 모든 변경에 Recover·Verify·Maintain·review를 동기식으로 붙이는 topology는 작은 팀에서 과설계가 될 수 있다.

독립 reviewer가 확인한 핵심 구분은 “역할을 나눈 개념”과 “지금 저장소의 고정 topology”를 같다고 보지 않는 것이다. 전자는 현업의 빠른 feedback, 위험 기반 review, provenance, handoff 흐름과 맞지만, Recover·Maintain·Verify라는 이름과 `current/source/output/records`, local JSON receipt 조합은 이 Project의 구현 선택이다. 반대로 규제·다팀 환경의 강한 assurance와 비교하면 verifier identity·signature·root of trust·commit/artifact binding과 end-to-end traceability가 아직 없으므로 현재 구조를 공급망 attestation 수준으로 과장하지 않는다.

## Background maintainer의 최소 후보 모델

목표는 main을 대신 판단하는 agent가 아니라, 작업 delta를 관찰해 명확한 변화는 좁게 반영하고 애매한 변화만 사용자·main에 올리는 보조자다.

### 입력

- 사용자와 main이 명시한 결정·정정
- 실제 file diff와 Git 상태
- direct test와 durable Verify 결과
- 현재 선택된 Workspace의 `current`, output routing과 관련 Owner

전체 대화나 모든 records를 매 cycle 기본 입력으로 읽지 않는다. 마지막 처리 cursor 이후의 delta와 영향받은 Owner부터 본다.

### 분류와 행동 후보

1. 일시적 탐색·명령 출력·철회된 후보: 쓰지 않는다.
2. 명확한 현재 상태 변화: `current/state`를 직접 수정한다.
3. 미래 작업에도 남는 명시적 사용자 결정: memory 승격 gate를 통과하면 반영한다.
4. 재사용할 결정·실패·검증 사건: 매 발화가 아니라 자연스러운 경계에서 하나의 record로 집계한다.
5. 의미·Owner·권한이 애매한 후보: durable write를 보류하고 report queue에 둔다.

### Memory 축적 방지 후보

다음 조건을 모두 만족하는 항목만 memory로 승격하는 안을 검토한다.

- 현재 task가 끝나도 다음 행동을 바꾼다.
- 사용자가 명시했거나 실제 artifact와 반복 관찰로 확정됐다.
- 어떤 Workspace와 Owner의 사실인지 분명하다.
- 기존 memory와 중복되면 append하지 않고 교체·압축한다.
- 짧게 표현할 수 없으면 상세는 record에 두고 memory에는 판단 기준과 링크만 둔다.
- 적용 여부가 애매하면 자동 승격하지 않는다.

이 조건은 사용자가 “막 쌓이면 안 된다”고 한 문제를 해결하기 위한 제안이다. 아직 최종 승인된 계약이 아니다.

### Report cadence 후보

- 현재 작업 방향을 잘못 만들 수 있는 ambiguity만 즉시 보고
- 나머지 ambiguity는 대화 종료, handoff, commit 전 같은 자연스러운 경계에서 batch
- 직접 반영한 명확한 state 변화도 같은 경계에서 짧게 요약
- background 작업 때문에 main의 응답이나 사용자 작업을 기다리게 하지 않음

이 cadence가 현재 마지막 미결정 질문이다.

## Workspace 분리와 보존 결정

사용자는 cadence 질문에 답하기 전에, 앞선 skill 변경부터 commit하고 이 논의를 새 Workspace 005에 남기도록 작업 경계를 바꿨다.

> 이 논의사항을 일단 005에 다가 좀 남기자 이건 새로운 작업인것 같고 이렇게 길게 얘기만 하면 또 길어지면서 대화 컨텍스트를 읽을것 같다

이어 “저 대화 발화 이후부터 잘 남겨 로스트인더미들 나게 하지 말고”라고 보존 기준을 명시했다. 이에 직전 skill·Workspace 002·004 변경은 commit `f082035`로 먼저 분리했고, 005의 `current`에는 우선순위·선택된 방향·마지막 질문만 두며 시간 근거와 발화·외부 조사 상세는 두 records로 나눴다. 따라서 이 Workspace 생성은 background 모델 승인이나 구현 시작이 아니라, 긴 대화를 다시 읽는 비용을 막기 위한 재진입 경계 확정이다.

## 구현 전에 더 닫아야 할 문제

- Main과 background agent가 같은 current를 동시에 고칠 때 stale overwrite를 막는 baseline hash·재확인 방식
- Background agent가 오래 걸리거나 실패할 때 main이 잘못된 완료를 가정하지 않는 상태 표시
- `current/state` direct write와 memory·records write의 서로 다른 권한
- Record 집계 단위와 retention·compaction 기준
- Verify가 기존 제품 test를 참조하는 manifest와 새 test가 필요할 때 제품 Owner로 돌려보내는 routing
- 효과 측정: maintainer wall time, main blocking time, stale current 발견률, 다음 세션의 재조사 범위와 잘못된 handoff

## 현재 결론과 다음 질문

역할은 유지하되 동기식 full-cycle을 기본값으로 두지 않는다. 명확한 current state는 background에서 직접 반영하는 방향이 선택됐고, memory는 자동 append가 아니라 조건부 승격·교체·압축으로 다뤄야 한다. Ambiguity reporting cadence와 direct-write allowlist를 확정하기 전에는 runtime을 구현하지 않는다.

다음 대화는 [current state](../current/state.md)의 보고 cadence 질문 한 가지에서 재개한다.
