# 2026-09-04 Project context 물리 layer 정정

## 정정

첫 반영은 `common/current/guidance`를 파일 경로가 아닌 책임 profile로만 사용하고, Project root의 평면 `prd.md`, `architecture.md`, 선택적 `overview.md`를 유지했다. 사용자는 “그냥 층위를 만들어라, 계속 헷갈린다”는 취지로 이 전제를 정정했다.

이 정정은 표현 수정이 아니라 책임 배치 변경이다. 따라서 profile-only 선택을 현재 계약에서 제거하고 Project canonical, Recover 경로 계약, sample live consumer, fixture·test, 이식·Workspace 생성 절차와 active Workspace current를 함께 바꾼다. [`06 구현 기록`](2026-09-04-06-reference-project-implementation.md)은 당시의 판단과 검증을 보존하지만 현재 구조를 지시하지 않는다.

## 구조 결정

```text
context/project/
├── README.md
├── common/
│   ├── README.md
│   └── prd.md
├── current/
│   ├── README.md
│   └── architecture.md
├── guidance/
│   └── README.md
└── decisions/
    ├── README.md
    └── 0001-default-timeout.md
```

- `common/current/guidance`는 필수 물리 탐색 경계다. 각 README는 책임과 현재 항목을 드러낸다.
- Guidance의 실제 본문은 조건부다. 현재 sample에는 적용할 독립 지침이 없으므로 `guidance/README.md`가 부재 상태와 추가·재검토·제거 조건을 소유한다.
- `decisions/`는 현재 답의 네 번째 layer가 아니라 중요한 선택의 이유·대안·재검토 신호를 보존한다. 기존 default-timeout 문서가 해당 값의 normative Owner라고 명시한 예외는 이번 정정과 별도 Owner migration이므로 유지한다.
- Root `overview.md`는 제품 의미·현재 구조·결정·routing을 다시 합치는 중복 표면이라 삭제한다. Redirect나 호환 symlink는 두지 않는다.

## 실제 이동과 계약 영향

- `context/project/prd.md` → `context/project/common/prd.md`
- `context/project/architecture.md` → `context/project/current/architecture.md`
- `context/project/overview.md` → 삭제
- Root와 네 하위 경계의 README에서 읽기 조건, authority·상세 Owner, 갱신 책임과 stale·재검토 신호를 연결한다.
- Recover contract는 schema `6`으로 올린다. Root `context/project/README.md`만 평면 예외로 허용하고 다른 선택은 `common/`, `current/`, `guidance/`, `decisions/` 아래 regular Markdown으로 제한한다. Recovery packet shape는 바뀌지 않아 schema `6`을 유지한다.
- 모든 Workspace가 모든 layer를 읽지는 않는다. Sample `001-default-timeout`은 root README, `common/prd.md`, `current/architecture.md`, default-timeout Decision만 선택하고 적용할 guidance가 없으므로 guidance README는 선택하지 않는다.
- Verify의 sample canonical basis는 `common/prd.md`와 normative Decision만 사용한다. Current architecture는 구현 지도이므로 basis에 넣지 않고, Verify 일반 경로에는 Recover의 layer 제한을 적용하지 않는다.

## 보존과 비도입

- 과거 receipt와 `status.json`은 다시 쓰지 않는다. 기존 receipt가 snapshot한 평면 Project 경로가 사라져 Recover가 `stale`로 판정하는 것이 정상이다.
- 완료되어 소비 경로에서 내려온 역사 Workspace와 과거 records의 당시 판단은 새 구조로 역동기화하지 않는다.
- TripProof 제품 내용·수치·Project maintainer, Work/Spec/Ticket 계층, 새 reviewer·hook·runtime은 이 정정으로 추가하지 않는다.
- 기존 untracked `.DS_Store`는 건드리지 않고 stage·commit하지 않는다.

## 검증

- Project root 전체 suite `119`개가 통과했다. 새 layer의 허용·거부와 미선택 문서 boundedness, Verify basis가 Recover layer로 제한되지 않는 경계, 제품 test `7`개를 포함한다.
- 관련 test 첫 묶음에서는 기존 descendant-timeout timing case 하나가 한 번 실패했지만 즉시 단독 재실행과 최종 전체 suite에서 통과했다. 재현되는 회귀로 판정하지 않았다.
- Explicit `001-default-timeout` Recover와 id 없는 active/default Recover가 모두 exit `0`, packet schema `6`으로 같은 네 Project 문서를 선택했다. 기존 receipt는 snapshot 파일 `5`개 중 변경 `1`, 이전 평면 경로 누락 `2`, unavailable `0`으로 `stale`이다.
- 물리 구조·Recover 경계·sample machine/human 선택·Verify basis·두 repo-local skill을 fresh read-only reviewer가 대조해 열린 P1/P2/P3 finding 없이 `PASS`로 판정했다. Recover가 미선택 layer README의 존재까지 막지 않는 것은 설치 완전성이 아니라 선택된 입력의 안전성을 맡는 bounded 책임으로 확인했다.
- 별도 재진입 표면 검토는 정정 전 records `02/04/05`가 output에서 현재 판단처럼 보이는 혼동을 `REVISE`로 찾았다. 과거 본문은 지우지 않고 현재성 메모를 추가하고 current·output·records index를 이 `07` 기록 우선으로 고쳤으며, 같은 reviewer의 재검토가 `PASS`했다.
- 변경 범위의 local Markdown link와 JSON parse, 제거된 active 평면 경로 residue, `git diff --check`가 통과했다. 두 skill의 공식 `quick_validate.py`는 환경에 PyYAML이 없어 시작하지 못했고, 같은 frontmatter 허용 key·name·description 조건을 Ruby 표준 YAML parser로 확인해 둘 다 통과했으며 unfinished TODO는 없었다.
- 실제 active Workspace에서 durable Verify는 실행하지 않았다. 과거 receipt와 `status.json`, 사람 acceptance, Workspace 완료와 commit은 이번 검증으로 갱신되지 않는다.
