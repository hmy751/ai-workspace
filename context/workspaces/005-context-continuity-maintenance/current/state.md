# Context continuity maintenance state

마지막 갱신: `2026-08-17`

## 현재 문제

Root Observe를 최종 구조로 확대하지 않고, Workspace 005에서 확정한 세션형 Maintainer 운영 전체를 `reference-project/`에 재사용 가능한 구현으로 완성해야 한다. 사용자의 동작 의미와 단계형 구현 계획은 다시 맞췄다. 현재 커서는 이전의 ownership 재계획이 아니라 Reference Harness·Maintain 계약을 먼저 수정한 뒤 Reference 안에서 실행 가능성을 확인하는 단계다.

## 확정된 사실

- 재사용 가능한 Maintain·Verify 구현 전체는 `reference-project/`가 소유하고 root는 Workspace 005 thin dogfood adapter만 소유한다.
- Maintainer는 task 세션마다 생기는 agent다. 기존 Workspace에서는 첫 작업 전에 `current/index` 중심으로 bounded grounding하고 짧은 시작 상태를 보여 주며, 새 Workspace에서는 대화를 따라 identity·goal·Owner가 형성된 뒤 지속 Context를 관리한다.
- 같은 task·Workspace·worktree에서는 Maintainer의 이해를 유지한다. 새 작업 세션에서는 새 Maintainer가 외부 canonical에서 다시 이해하며, Main compaction만으로 살아 있는 Maintainer를 reset하지 않는다.
- 매 Main 응답 종료마다 활동하되 초기 grounding 이후에는 Main을 기다리게 하지 않는다. Event·delta는 이 동작을 연결하는 구현 입력이지 별도 사용자-facing 역할이나 durable Context가 아니다.
- Durable 변화 없음은 no-write·무보고다. 사소한 명확 반영은 조용히 처리하고, 중요한 명확 반영은 수정 후 짧게 보고하며, ambiguity는 write 전에 즉시 질문한다.
- Transient 실패는 먼저 자동 복구한다. 복구 뒤에도 freshness를 다시 세우지 못할 때만 짧게 경고하고 false success를 만들지 않는다.
- Root `.codex/hooks.json`과 `.codex/context_maintainer/`에는 Workspace 005 고정 Observe가 있다. Git에서 제외된 runtime에 event·queue·cursor를 관리할 뿐 LLM 판단이나 Context write를 하지 않는다.
- Internal unit test 28개와 compile·JSON·diff 검사는 통과했지만 Git fingerprint 실패 오표시, queue·ledger crash 무결성, 잘못된 `next_sequence`의 status crash, 대화-only event의 전체 repository Git scan을 검출하지 못했다.
- Live smoke에서는 async Stop이 취소돼 sequence 1이 `waiting_stop`이고 cursor 파일이 없다. Repo-global FIFO라 다른 session까지 막을 수 있으며, end-to-end pairing과 운영 acceptance는 실패 상태다.
- Root `.DS_Store`는 별도 untracked 파일이므로 구현 산출물로 포함하거나 되돌리지 않는다.
- `apply-context-harness` skill, Verify 구현·schema와 memory 구조도 이번 slice에서 수정하지 않았다.

## 확정된 구현 순서

1. Reference Harness·Maintain의 사람용 진입 문서와 계약을 세션형 Maintainer 의미로 수정한다.
2. Reference Maintain 안에서 session lifetime, background 비차단, 보고와 restart 복구 가능성을 time-boxed spike로 확인한다.
3. 근거를 보고 trigger, agent continuity, checkpoint, retry와 reporting adapter의 최소 구조를 결정한다.
4. Initial sync, warm continuity, no-change, 좁은 `current/state` write, 중요 반영 보고, ambiguity 질문과 자동 복구를 첫 vertical slice로 구현한다.
5. Root를 Reference thin adapter로 전환해 실제 여러 turn·Main compaction·Maintainer restart·failure를 dogfood한다.
6. Memory와 index, 집계 records, 확정 output routing 순서로 write 범위를 확장한다.
7. 축소 Verify와 기존 Verify·Recover 호환을 구현·검증한다. Recover 역할은 실제 결함 없이 확대하지 않는다.
8. `apply-context-harness` 갱신, root 중복 runtime 정리, 전체 validation과 fresh-task acceptance를 수행한다.

## 구현 후보와 미결정점

- Reference canonical의 exact 파일 배치와 root adapter가 공유할 코드 경계
- Session 시작·response-end를 관찰할 실제 hook과 보고 integration point
- 같은 Maintainer 이해를 이어 쓸 정확한 Codex adapter 방식
- Queue, locking, storage, transaction과 processing cursor의 구체 schema
- 현재 root dogfood state와 uncommitted 변경을 재배치할 migration 순서
- Session별 queue/cursor 격리와 cross-session gap 차단
- Maintainer compaction, cursor gap과 Owner·routing 변경의 rebootstrap 방식
- 향후 `memory/` 폴더와 index routing의 Owner 분리·선택 read 규칙
- Main과 maintainer가 동시에 쓸 때 target revision 표현과 stale-write 방어
- 중요 반영·ambiguity·복구 실패를 보여 줄 정확한 채널과 중복 보고 방지
- 축소 Verify evidence의 선택 조건, 보존 형식과 retention
- Descendant timeout timing flake의 synchronization 수정
- Baseline 측정 뒤 정할 latency, stale-context 발견과 handoff 성공 지표

## 다음 행동

이번 문서 갱신과 현재 Workspace 005 변경을 검증·commit한 뒤, `reference-project/context/work/harness/maintain/` 계약과 관련 Harness 진입 문서를 수정한다. Root Observe 결함부터 국소 수정하거나 기술 후보를 계약으로 먼저 고정하지 않는다.
