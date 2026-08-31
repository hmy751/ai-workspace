# Workspace 활성화 규칙 재보정

날짜: `2026-08-31`

## 다시 연 이유

`memory-harness-research`에서 이미 만든 `004-tripproof-judgment-continuity`로 현재 작업을 전환하려는 대화에서 여러 Main이 canonical의 “같은 Main session에서 바꾸지 않는다”는 문장을 기술적 불가능처럼 적용했다. 사용자는 새 Main session을 보편적으로 강제하기보다 현재 binding과 pending 상태를 확인한 뒤 핵심 영향만 처리하고 상황에 맞게 전환하기를 원했다.

## 기존 규칙의 기원

2026-08-19 Maintain 구현은 한 outer session의 runtime과 semantic thread를 explicit Workspace에 고정하고 config mismatch를 fail-closed했다. 같은 session의 자동 re-grounding은 기술적으로 불가능하다고 판정한 것이 아니라 당시 구현 범위에서 보류했다.

2026-08-28 Workspace 008의 독립 Owner reviewer는 초기 활성화 문구와 그 adapter가 충돌한다고 지적하며 두 해결책을 제시했다.

- 이전 Main session 종료 뒤 binding을 바꾸고 새 Main session에서 grounding
- same-session rebind를 별도로 구현

당시 작업은 문서 계약만 정리하고 새 code·schema·hook을 만들지 않는 범위였기 때문에 Main이 첫 경로를 선택했다. 사용자가 same-session 금지를 직접 결정한 근거와 actual host 전환 검증은 없었다. 따라서 “config만 바꾸는 전환은 현재 adapter가 지원하지 않는다”는 구현 한계가 “같은 visible Main task에서는 전환할 수 없다”는 보편 원칙으로 넓어졌다.

## 보정한 판단

- 새 Main session을 기본 의무로 두지 않는다.
- 전환 전에 현재 binding과 Maintain의 처리 중·pending·failed 상태를 확인한다.
- 미반영 내용이 successor의 goal·제약·첫 판단·다음 행동을 바꾸는 경우에만 predecessor current를 보완하거나 successor에 필요한 의미를 직접 남긴다.
- 관련 없는 미처리 상태는 predecessor에 보존할 수 있으며 존재 자체로 전환을 막지 않는다.
- 같은 Main session을 이어 가면 현재 turn은 predecessor로 마감하고, successor의 bounded Recover와 새 Maintain grounding이 실제로 성공한 뒤 다음 작업을 시작한다.
- Grounding이 실패하거나 host가 안전하게 재결합하지 못하면 기존 binding을 유지하고 새 Main session을 fallback으로 사용한다.
- 설정 파일 변경, Main의 warm 이해와 별도 bounded 재진입 검토를 서로 대신하는 증거로 사용하지 않는다.

## 반영 범위와 상한

이미 이식된 `memory-harness-research`의 root routing, 생성·전환 canonical, repo-local skill과 Maintain 비소유 문구에 먼저 같은 의미를 반영했다. 기존 `.codex/maintain.json`, `workspaces/index.json`, 004 내용과 사용자의 미추적 분석 파일은 수정하지 않았다.

그 뒤 Reference의 root·Work routing, 생성·전환 canonical, repo-local skill, Maintain 계약과 root proof ceiling을 맞췄다. 이 변경은 판단 규칙을 보정한 것이며 same-session rebind code, runtime generation, hook이나 자동 전환 command를 구현하거나 검증하지 않는다. 현재 Reference host adapter의 config-only 전환은 계속 자동 re-grounding을 지원하지 않는다.

## 검증

- `memory-harness-research`의 변경 Markdown local link와 `git diff --check`가 통과했다.
- Reference와 Workspace 008의 변경 Markdown local link와 `git diff --check`가 통과했다.
- 두 repo-local skill은 frontmatter name·description과 unfinished placeholder 대체 검사를 통과했다. 제공된 Python `quick_validate.py`는 현재 환경에 `PyYAML`이 없어 import 단계에서 시작하지 못했으므로 validator 성공으로 기록하지 않는다.
- Reference 전체 unit test `97`개는 최종 실행에서 통과했다. 첫 실행에서 기존 `test_timeout_covers_descendant_after_group_leader_exits`가 descendant PID 파일을 timeout 전에 만들지 못해 한 번 실패했지만 같은 test 단독 실행과 이어진 전체 실행은 통과했다. 이번 Markdown·skill 문구 변경의 회귀로 판정하지 않는다.
