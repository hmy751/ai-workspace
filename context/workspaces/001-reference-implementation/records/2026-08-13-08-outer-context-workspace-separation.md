# 저장소 context의 Workspace 분리

날짜: `2026-08-13`
상태: 구조 이동·검증 완료, commit 전
기준 commit: `e3c237b`

## 사용자 결정

저장소 바깥 context에 `output/context/project`·`output/context/work` 구조를 그대로 복제하거나 기존 내용을 여러 책임 파일로 다시 나누지 않는다.

- 지금까지 수행한 source 정리와 reference 설계·구현·검증의 `current/`와 `records/`를 하나의 기존 Workspace로 통째로 귀속한다.
- 다음 실제 Project 적용 작업은 별도 Workspace에서 새 current와 records로 시작한다.
- shared source와 실제 `output/` 산출물은 이동하지 않는다.

## 적용한 구조

```text
context/
├── README.md
├── source/
└── workspaces/
    ├── README.md
    ├── 001-reference-implementation/
    │   ├── README.md
    │   ├── current/
    │   └── records/
    └── 002-project-application/
        ├── README.md
        ├── current/
        └── records/
```

- 기존 `context/current/`와 `context/records/`는 `git mv`로 `001-reference-implementation/` 아래에 함께 이동했다.
- 날짜가 붙은 기존 records의 역사적 문장과 당시 상태는 다시 쓰지 않았다. 디렉터리 깊이가 바뀌어 깨진 shared source와 `output/` 상대 링크만 목적지에 맞게 고쳤다.
- [`context/README.md`](../../../README.md)와 [`workspaces/README.md`](../../README.md)가 shared source, Workspace 관계, active Workspace, 재진입 순서를 정의한다.
- [`002-project-application`](../../002-project-application/)은 001의 current를 복사하지 않고 실제 적용 목표·기준·현재 대기 상태로 새로 시작했다.
- `AGENTS.md`와 repo-local `context_maintainer`는 지정한 Workspace만 읽고 갱신하도록 단일 `context/current|records` 가정을 제거했다.
- outer context에는 Harness, JSON 계약, machine status, lifecycle 자동화를 추가하지 않았다.

## 검증

- `output/` 전체 unittest 29개 통과
- root README, AGENTS, outer context와 `.codex` 문서의 로컬 Markdown 링크 검사에서 broken link 0개
- `.codex/config.toml`, `.codex/agents/context-maintainer.toml` Python `tomllib` parse 통과
- `git diff --check`, `git diff --cached --check` 통과
- `context/source/`와 `output/`은 기준 commit 대비 변경 0건
- `context/source/`의 기준 tree hash `c2007327cdeb0c1f2955258f5036532399907a65` 유지
- 운영 문서와 maintainer 설정에서 singleton `context/current`·`context/records` 경로가 제거됐고, 남은 문자열은 과거 records의 당시 경로 설명뿐이다.
- repo-local `context_maintainer`를 002 대상으로 실행한 결과 `context_status: current`였고, 001·shared source·output을 수정하지 않았다.

## 검증 상한

이번 변경은 저장소 자체의 작업 context가 001과 002에서 섞이지 않도록 문서·경로·maintainer 범위를 분리한 것이다.

아직 실제 대상 Project를 선택하거나 적용 작업을 시작하지 않았다. active selector는 사람용 Markdown이며 machine lifecycle을 구현하지 않는다. maintainer의 이번 점검은 지정 Workspace 범위가 정적으로 일치하고 실제 실행에서 불필요한 수정이 없었다는 것만 확인하며, 이후 모든 세션의 지속적인 routing 효과까지 증명하지 않는다.
