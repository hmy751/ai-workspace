# 2026-09-04 source intake

## 목적

이번 도입 판단이 실제로 읽은 자료와 그 권위 범위를 고정한다. 외부 저장소의 working tree가 진행 중이므로 commit 경로만 남기지 않고 핵심 파일 hash와 문서 지위를 함께 기록한다.

## 읽은 범위

중심 입력은 다음 경로의 Markdown 12개다.

- [07 분석 진입점](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/README.md)
- [문제 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/01-problem-analysis.md)
- [Workspace 기반 방향](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/02-workspace-based-continuity-direction.md)
- [Project context foundation](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/03-project-context-foundation-direction.md)
- [대화 장면 분석](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/04-conversation-scene-analysis.md)
- [판단 연속성 해결 방향 묶음](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/05-judgment-continuity-solution-direction/README.md)
- 같은 묶음의 `01-current-direction.md`부터 `05-solution-design.md`
- [Work-first와 Spec/Ticket-first 비교](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/06-work-first-spec-ticket-tradeoff-analysis.md)

문서가 직접 연결한 운영 맥락은 다음 범위에서 선택해 읽었다.

- [Workspace 006 Work·Spec·Ticket 비교](/Users/hammyeong-yeon/Desktop/memory-harness-research/workspaces/006-work-spec-ticket-tradeoffs/README.md)의 goal, constraints, Project context 선택, state와 output
- [Workspace 007 판단 연속성 후속 연구](/Users/hammyeong-yeon/Desktop/memory-harness-research/workspaces/007-tripproof-judgment-continuity-research/README.md)의 goal, constraints, Project context 선택, state, output와 2026-09-04 최신 records
- `memory-harness-research/context/source/07-tripproof-spec-driven-continuity/`와 `context/source/05-tripproof-harness-retro/` 안에서 source 지위와 보존 한계를 설명하는 문서
- 현재 저장소의 live `reference-project/` Project·Work·Workspace·Recover·Maintain·Verify canonical, 구현과 tests
- 현재 저장소 Workspace 001과 008의 정확히 관련된 current·output

## 초기 source intake에서 제외한 범위

- 분석 문서가 연결한 `/Users/hammyeong-yeon/Desktop/10_work/tripproof` private JSONL과 제품 저장소
- 분석 문서가 연결한 별도 `/Users/hammyeong-yeon/Desktop/skills` clone과 번역 저장소
- 사용자가 지정하지 않은 다른 Desktop 저장소
- 네트워크의 외부 reference 원문

초기 독립 검토에서 분석 문서의 일부 직접 링크가 범위 밖 원대화까지 열린 뒤 local source boundary를 다시 확인했다. 그 원대화 인용과 직접 확인 판정은 철회했고, 최종 채택 판단과 이 Workspace 문서에는 사용하지 않았다. 따라서 대화 장면과 수치는 `memory-harness-research` 안에 보존된 분석·내부 감사의 결과로만 사용한다. 이 **초기 intake 단계**가 private 원대화, 실제 TripProof 코드나 Matt 원문을 독립 재검증했다고 말하지 않는다.

이후 사용자가 실제 TripProof 적용을 직접 대조하라고 범위를 넓혔다. 그 후속 조사는 `/Users/hammyeong-yeon/Desktop/10_work/tripproof`의 tracked 파일·Git 이력·보존 receipt와 private payload를 제외한 runtime metadata를 read-only로 확인했으며, 범위와 결과는 [`TripProof 실제 적용 평가`](2026-09-04-04-tripproof-application-assessment.md)가 별도로 소유한다. private 원대화와 private prompt/response는 계속 제외했다.

## 외부 working-tree 지위

- branch: `main`
- HEAD: `f9a397d75d99da9c42aa2eac0562eb6d7d204dda`
- 상태: 지정 분석, Workspace 004·005·007과 인접 분석에 수정·추가 파일이 있는 dirty working tree
- 판단 영향: `05-solution-design.md`와 2026-09-04 records는 HEAD만으로 재현할 수 없는 새 파일이다. 아래 hash는 이번에 읽은 snapshot을 식별하지만 원문 자체를 복제하지는 않는다.

| 파일 | SHA-256 |
| --- | --- |
| `README.md` | `540abf1f6fb94baee6c92b795f84b5f235c596be56e61b4e33d34d846069da8` |
| `01-problem-analysis.md` | `8017201ad2e93d6f67a13321dd99f77943257b65332a7e85165e2fa13e4fba64` |
| `02-workspace-based-continuity-direction.md` | `f4bab25385a968780015f07ccabcc7a7f333360e8672c4459819ed0ee05ddb85` |
| `03-project-context-foundation-direction.md` | `893e1d4c739abe3044c8e19a8dc464ec2c2d708e4a0c0ea9fe6a0d0f275ff9c8` |
| `04-conversation-scene-analysis.md` | `fd0eccf1554689e9ae3df5cb25387f0b700706ad1b832e66091630131e06f2aa` |
| `05/README.md` | `73973a7b33bb85135635e696160f5572e0c7d0b31462d0302eb876164ed4360f` |
| `05/01-current-direction.md` | `49fac2d7aaa965545a61043667e20f408f5e3623dd6bcc850cec85d72363e56d` |
| `05/02-v1-v2-design-input.md` | `383111818cd2a409bf5d7d227042dc6d16a0d4e505d6af05fa177dfc312cb181` |
| `05/03-matt-design-input.md` | `7786dcf63c1142623089bd6ffbbef09cd9b063d26c53af3f289464566e01ab4c` |
| `05/04-combination-analysis.md` | `7c6e7eca50085d2b76f58dec5c8b1bb125813ae20b20fb7c3105af545d8d535e` |
| `05/05-solution-design.md` | `2c7913ffc42100d1edb917130ad60efe971afee1d0dd571be6fe69015f4aca59` |
| `06-work-first-spec-ticket-tradeoff-analysis.md` | `280de2a93929e9e2e15a6159f3dc64c480adfcef637cf9e32cedfb0ab4af2ee1` |

## 문서 지위의 구분

### 관찰·문제 근거

- 01과 04는 제품·코드·Spec·평가·Context 문제와 세 장면을 분석한다.
- 저장소 안 source는 07의 주장별 전체 추적성이 아직 완성되지 않았고, 05 내부 감사의 상세 evidence bundle을 이 연구 저장소에 복사하지 않았다고 밝힌다.
- 따라서 “국소 산출물이 넓은 완료를 대신한 장면이 있었다”는 문제 근거는 사용할 수 있지만, 세 장면의 일반 발생률이나 TripProof 전체 실패를 확정하지 않는다.

### 채택된 외부 연구 방향

- 02의 Workspace 기반 수명·권위 분리
- 03의 Project context foundation과 축소된 Project-local 관리 skill 경계

이 둘은 `memory-harness-research` 안에서 채택한 설계 방향이지만 실제 TripProof 적용 효과는 아니다.

### 적용 전 설계 후보

- 05의 `judgment-evidence-scope`, `claim-impact-review`, `direction-gap-review`
- 06의 Work-first/Spec-Ticket hybrid 관계와 적용 조건

05의 최신 설계는 내부 독립 검토에서 pilot으로 갈 수 있다는 판정을 받았지만 사용자 acceptance와 실제 replay·live 효과는 없다. 06도 구조적 trade-off 분석이지 Work 효능의 증거가 아니다.

## currentness 충돌

Workspace 007의 current state와 output은 `05-solution-design.md`가 아직 없다고 서술한다. 그러나 실제 working tree에는 해당 파일과 생성·독립 검토 records가 있다. 이 차이는 이번 snapshot이 진행 중임을 보여 주며, 자동으로 Workspace 관리 실패나 최신 설계의 채택을 뜻하지 않는다.

이번 판단에서는 다음 우선순위를 사용했다.

1. 실제 존재하는 최신 analysis 파일과 이를 설명하는 최신 dated record
2. 분석 묶음의 현재 README
3. Workspace current/output는 연구 목표·제약·근거 접근점을 복원하는 자료로 사용하되 최신 산출물 목록에는 사용하지 않음

외부 저장소를 수정하거나 이 불일치를 대신 정리하지 않았다.
