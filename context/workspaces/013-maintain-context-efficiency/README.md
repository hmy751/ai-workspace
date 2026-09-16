# Maintain context efficiency Workspace

Maintain이 이전 대화의 의미를 이어 가는 목적은 보존하면서, 같은 semantic thread에 전체 transcript와 도구 출력을 계속 누적해 매 판단마다 다시 처리하는 비용을 제한하는 작업이다. `ai-workspace`의 Reference 구현에서 공통 구조를 먼저 개선하고, 검증된 변경을 Noline 설치본에 적응해 적용하는 두 대상을 한 작업 경계에서 관리한다.

현재는 **Reference Maintain 책임·테스트·도구 연결 리팩터링 구현 / 비용 개선 미착수 / 자동 Maintain 비활성** 단계다. 사용자는 비용 개선 전에 기존 기능을 유지하면서 코드와 테스트의 가독성·응집도 및 Codex·Claude 연결 의존성을 정리하도록 결정했다. active Workspace, 실제 Maintain binding·hook·runtime, Noline 설정, AI-native moment reviewer 설정은 변경하지 않았다.

## 재진입

1. [`current/index.md`](current/index.md)
2. [`current/memory.md`](current/memory.md)
3. [`current/state.md`](current/state.md)
4. [`output/index.md`](output/index.md)
5. [`책임 분리와 검증 기록`](records/2026-09-16-01-maintain-refactoring.md)
6. [`records/2026-09-15-01-scope-correction-and-runtime-evidence.md`](records/2026-09-15-01-scope-correction-and-runtime-evidence.md)
7. [`records/2026-09-15-02-improvement-design-and-validation-plan.md`](records/2026-09-15-02-improvement-design-and-validation-plan.md)

## 책임 경계

- 공통 계약과 기준 구현은 [`reference-project/context/work/harness/maintain/`](../../../reference-project/context/work/harness/maintain/)가 소유한다.
- 실제 Noline 적용본은 Noline 저장소의 `context/work/harness/maintain/`이 소유한다. Source와 target의 판본·적응·검증은 구별한다.
- 과거 Reference 동작 계약은 [Workspace 007](../007-maintain-clean-room-reimplementation/)에서, Noline 이식 경계와 과거 모델 설정은 [Workspace 011](../011-noline-harness-upgrade/)에서 필요한 기록만 읽는다. 두 Workspace의 현재 상태를 이어 쓰지 않는다.
- `evidence-collector` 사용량은 최초 문제 발견과 비교 근거로 보존하지만, 이 Workspace의 기본 구현 대상은 Maintain의 Reference와 Noline 적용본이다. 수집기의 capture/interpretation 분리는 별도 변경 범위를 명시적으로 열 때만 함께 구현한다.
- 자동 compact는 실제로 동작하지만 일상적인 비용 제어 수단으로 보지 않는다. 연속성에 필요한 의미 상태를 명시적으로 checkpoint하고 새 semantic thread로 넘기는 구조를 검증한다.
- 모델 등급이나 reasoning effort 하향은 구조 개선을 대신하지 않는다. 먼저 반복 instruction·도구 출력·과거 decision의 재입력을 줄인 뒤 같은 replay에서 품질과 비용을 비교한다.
- 활성화, 실제 background 실행, 기존 runtime 정리, 원격 push는 별도 사용자 지시 전에는 하지 않는다.
