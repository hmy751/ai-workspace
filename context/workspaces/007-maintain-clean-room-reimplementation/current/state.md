# Maintain clean-room reimplementation state

마지막 갱신: `2026-08-18`

## 현재 상태

Workspace는 새 세션이 첫 구조를 도출할 준비가 됐다. 선택된 구현은 없고 automatic Maintain도 비활성이다.

- Workspace 006 중단 기록 commit: `0952b1d` (`docs: record stopped maintain restructuring attempt`)
- Workspace 005 최종 구현 commit: `9553d0a`
- 구현 전 부모 baseline: `2649e9b`
- Path-scoped 복원과 root 비활성화 commit: `b508d80` (`refactor: reset maintain implementation baseline`)
- `9553d0a`의 live 구현·실행 계약 45개 경로는 현재 worktree에서 `2649e9b`와 일치한다.
- Root `.codex/hooks.json`은 빈 hook 집합이고 Maintain agent·Workspace binding은 등록돼 있지 않다.
- 이전 root Observe runtime은 복원하지 않았다.
- Git에서 제외된 과거 Observe state `.context-harness/runtime/context-maintainer/v1/`에는 `control.json`과 빈 `runtime.lock`이 남아 있다. 자동 경로가 참조하지 않으며 새 state의 canonical이나 migration 입력으로 취급하지 않는다.
- Workspace 005와 006 문서는 현재 버전 그대로 보존했다.
- 사용자 소유 untracked `.DS_Store`는 작업 범위 밖이다.

정확한 경로와 검증은 [`reset baseline record`](../records/2026-08-18-02-code-reset-baseline-and-excluded-topologies.md)가 소유한다.

## 마지막 검증 지점

- 지정한 45개 복원 경로와 `2649e9b` 사이 diff 없음
- Root hook JSON과 agent TOML parse 통과
- Root에서 삭제된 Maintain config·agent와 Reference runtime entrypoint 부재 확인
- Reference 전체 test 최종 재실행 `53/53` 통과
- `git diff --check` 통과

첫 전체 test에서 timeout 하위 프로세스 생성 시점을 확인하는 기존 Verify test 1개가 한 번 실패했다. 같은 test의 단독 재실행과 전체 suite 재실행은 통과했다. 현재 baseline 변경과 직접 연결된 재현 결함으로 판정하지 않았지만, Verify process handling을 다시 바꿀 때는 이 타이밍 관찰을 재확인한다.

## 현재 proof ceiling

- 새 Maintain 구현·unit test·live host acceptance는 아직 없다.
- 과거 ignored Observe state는 삭제·migration하지 않았다. 새 runtime이 같은 위치를 선택하려면 collision과 역사적 원자료 처리 권한을 먼저 결정한다.
- 실제 host가 어떤 response-end signal과 session continuity를 안정적으로 제공하는지 새 baseline에서 결정하지 않았다.
- Warm continuity를 process·thread·resume 중 어떤 mechanism으로 만들지 선택하지 않았다.
- 의미 판단 품질, UI 보고와 실패 뒤 freshness 복구도 검증하지 않았다.
- 기존 005·006 test count는 역사적 구현의 내부 증거일 뿐 새 구현 acceptance가 아니다.

## 다음 원자 행동

새 세션은 먼저 [`source와 behavior contract`](../records/2026-08-18-01-clean-room-source-and-behavior-contract.md)에서 여섯 장면을 `입력 → 모델 판단 → deterministic guard → 사람 권한 → 관찰 가능한 결과`로 펼친 acceptance matrix를 만든다. 그 뒤에만 가장 작은 end-to-end vertical slice와 실제 host 확인 방법을 제안한다.

이 첫 설계가 나오기 전에는 `9553d0a` diff나 006 구현을 구조 후보로 읽지 않는다. 과거 기록은 사용자 발화, 실패 장면과 proof ceiling을 확인할 때만 사용한다.

## 중단 조건

- 첫 slice가 과거 queue·ledger·attention topology를 근거 없이 전제로 함
- 명확한 사용자 장면과 연결되지 않은 durable state·recovery protocol을 먼저 추가함
- 실제 host 검증 전에 root 자동 연결을 활성화함
- Global reference의 판단 원칙을 새 제품 요구사항처럼 확장함

현재 blocker는 없다.
