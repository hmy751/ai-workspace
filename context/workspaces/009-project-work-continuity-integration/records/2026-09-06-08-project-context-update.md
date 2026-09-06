# Project 맥락 보존 기준과 갱신 skill 보완

날짜: `2026-09-06`

## 결정의 배경과 원문

사용자는 첫 분석 뒤 `memory-harness-research`의 Workspace 개념과 연구 01·02·03의 결정 내용을 다시 읽도록 요청했다. Main은 Project 관리 기준을 주로 확정 여부와 변경 권한으로 설명했고, 사용자가 반복해서 구체적인 의미와 기존 문구를 물은 뒤 원자료를 다시 대조했다.

연구 [`03-project-context-foundation-direction.md`](/Users/hammyeong-yeon/Desktop/memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/03-project-context-foundation-direction.md)의 핵심 원문:

> 선택한 책임 범위에서 다음 판단에 필요한 근거가 있는데도 불확실하다는 이유만으로 조용히 빼서는 안 된다. 현재 답, 역사 근거, 열린 판단 중 어느 역할인지 권위와 수명에 맞게 드러낸다.

연구 [`2026-08-30-03-judgment-recoverability-and-blind-rebuild.md`](/Users/hammyeong-yeon/Desktop/memory-harness-research/workspaces/003-tripproof-context-application/records/2026-08-30-03-judgment-recoverability-and-blind-rebuild.md)의 실패 근거:

> 첫 Project context 재구성은 `common/current/guidance` 층위와 색인을 만들었지만, 제품 목적·사용자 문제·대표 장면과 핵심 domain 의미보다 코드로 검증하기 쉬운 사실과 방어적 제한을 우선했다. 다음 작업자가 파일 위치는 찾을 수 있어도 제품 의미를 다시 추측해야 했으므로, 구조는 통과했지만 07이 해결하려던 판단 연속성은 복원하지 못했다.

사용자의 핵심 정정 원문:

> 이근거도 중요하네 자꾸 빼버리니까 방어적으로

사용자는 층위가 이 문제를 보완하는지, 불확실한 것을 모호하게 표현하기보다 구체적으로 구분하면 되는지를 논의했다. 보존 원칙을 먼저 두도록 문장 순서를 바꾸고 Project context README에 둔다는 설명 뒤, 최종적으로 “그래 보완하자”라고 반영을 요청했다.

## 채택한 내용

- 필요한 맥락의 충분한 보존을 먼저 밝히고, 근거가 지지하는 내용과 미정·미확인·충돌이 남은 부분을 구체적으로 표현한다.
- 층위는 제품 의미·현재 구현·조건부 기준의 책임 구분이다. 확실성 등급이나 문장마다의 필수 상태 schema로 바꾸지 않는다.
- 현재 사용하는 제품 이해를 남길 수 있으며, 일부 미정인 선택 때문에 전체 의미를 지우거나 모든 내용을 확정된 규칙으로 바꾸지 않는다.
- 보존·변경·갱신 기준과 실패 이유는 Reference Project README에 둔다. 배포되는 문서에는 로컬 연구 경로를 넣지 않고 이 기록에 상세 provenance를 남긴다.
- TripProof의 `project-context-maintainer`는 선택적 pilot 후보가 아니라 이번에 가져올 운영 책임으로 확정했다. 이름은 `update-project-context`, 사람용 이름은 `Project 맥락 갱신`으로 바꾼다. 관리 기준의 소유는 Project README에 남기고 skill은 짧은 실행 절차로 유지한다.
- 작업 중 여러 Workspace에 계속 유효할 변화나 사용자가 요청한 누락 복원을 처리하며, 종료 시점에 묶지 않는다. Root 호출 경로와 다른 Project로의 이식 절차까지 연결한다.

Workspace·Spec 관계는 사용자가 생각을 더 열어 두되 지금은 유지하도록 했다. Verify는 현재대로 둔다. `decisions/` 기록 항목 자체의 추가 보완, 새 reviewer·hook·상태 schema는 이번 범위로 승격하지 않았다.

## 실제 원자료와 지위

- 연구 01·02·03의 SHA-256은 최초 intake와 동일하다. 이번 확인 시 연구 HEAD는 `d80f571`이며 HEAD만으로 읽은 전체 working tree를 재현한다고 주장하지 않는다.
  - 01: `8017201ad2e93d6f67a13321dd99f77943257b65332a7e85165e2fa13e4fba64`
  - 02: `f4bab25385a968780015f07ccabcc7a7f333360e8672c4459819ed0ee05ddb85`
  - 03: `893e1d4c739abe3044c8e19a8dc464ec2c2d708e4a0c0ea9fe6a0d0f275ff9c8`
- 위 08-30 실패·교정 기록의 SHA-256: `aeeabb0d6425057cbfcb7335aa6f804520206e8b8d93ec5628c2aa47814d6c85`.
- 연구 [`Workspace 003 current`](/Users/hammyeong-yeon/Desktop/memory-harness-research/workspaces/003-tripproof-context-application/current/state/index.md)는 다음 작업에서 쓸 working product model과 미확정 제품 판단을 함께 남겼다. 이 적용은 미확정 의미를 전부 제외하는 계약이 아니었다.
- TripProof HEAD는 `8b1418d`였다. [`Project README`](/Users/hammyeong-yeon/Desktop/10_work/tripproof/context/project/README.md)의 SHA-256은 `e93b1a9a486aad6aa497d6159d5591c46861be2e8ac8017f55a96563f2d84461`, [`관리 skill`](/Users/hammyeong-yeon/Desktop/10_work/tripproof/.agents/skills/project-context-maintainer/SKILL.md)은 `f3d08d5633061167e8b61a8a28cf9248f5c3f1ae973eec57a44171777252da99`다. 이번 작업에서 외부 저장소는 수정하지 않았다.

## 반영 위치와 책임

- [`Project README`](../../../../reference-project/context/project/README.md): 합의한 보존 문구·배경, 층위와 표현, 기존 의미 복원과 새로운 결정의 구분, 갱신 시점·선택 읽기·보고·관리 장치의 경계
- [`update-project-context`](../../../../reference-project/.agents/skills/update-project-context/SKILL.md)와 UI metadata: 위 계약을 적용하는 repo-local 절차와 발견 설명
- [`Reference root 지침`](../../../../reference-project/AGENTS.md)과 [`README`](../../../../reference-project/README.md): 작업 중 Project-wide 변화·명시 갱신·복원 요청의 호출 경로
- [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/SKILL.md)와 [`이식 판단 계약`](../../../../.agents/skills/apply-context-harness/references/application-contract.md): 기존 동일 책임 skill의 다른 이름까지 확인하고 개별 설치·적응·제외·fallback·정적 검증을 연결
- 이 Workspace의 README·current·output: 물리 layer의 실제 commit `7bd5089`와 이후 미커밋 보완, 관리 skill을 pilot로 남겼던 이전 판단의 대체 관계

Skill 작성에는 `skill-creator`의 짧은 절차·정확한 discovery·canonical 중복 방지 기준을 적용했다. 배포되는 Reference의 문구는 `write-for-others`에 따라 독립적으로 읽히게 작성하고, 이 작업대 기록에만 로컬 provenance와 대화 발췌를 뒀다. 지속 기준·관리 장치의 책임 분리와 제거 가능성은 전역 AI-system 기준과 대조했으며 전역 파일은 변경하지 않았다.

## 검증과 상한

- 공식 `quick_validate.py`로 새 skill과 수정한 이식 skill이 모두 `Skill is valid!`를 반환했다. 기본·bundled Python에는 PyYAML이 없어 기존 TripProof `.venv/bin/python`을 검증 실행기로 사용했고 새 dependency를 설치하지 않았다.
- Explicit `recover 001-default-timeout --json`과 default `recover --json`은 모두 exit `0`, schema `6`이며 같은 Workspace와 같은 네 Project 문서를 선택한다. Packet에서 새 보존·관리 기준과 기존 제품 목적·범위·현재 구현·timeout 결정을 함께 읽을 수 있었다.
- 기존 Verify snapshot은 이전 경로 이동에 따른 `stale` 상태를 유지한다. 이번에는 제품 실행·receipt·status를 새로 만들거나 변경하지 않았다.
- 변경·추가된 Markdown 14개에서 local link 132개를 검사해 누락 target이 없었고, 배포 Reference의 링크가 자체 root를 벗어나거나 로컬 절대 경로를 포함하지 않음을 확인했다. UI metadata의 YAML, 설명 길이, skill 호출명과 implicit invocation 설정도 통과했다.
- `git diff --check`를 통과했다. 변경 목록은 Markdown과 새 skill의 UI YAML뿐이며 제품·Harness 코드, Workspace machine 계약·status·receipt에는 diff가 없다.

Main은 원자료와 diff를 대조해 필요한 제품 이해의 보존, 미정 부분의 구체화, 기존 승인 범위의 반영, Project/Workspace 경계와 skill 제거 후 계약 접근을 검토했다. 이는 독립 행동 eval이나 실제 host discovery·자동 호출을 입증하지 않는다. Runtime·schema·제품 코드 변경이 없어 full suite와 durable Verify를 반복하지 않았다.

구현·검증 보고 시점에는 `7bd5089` 위 미커밋 변경이었고 staging·commit·push를 하지 않았다. 이후 사용자가 “그래 커밋까지 하자”라고 요청했다. 이번 보완 파일과 현재 상태 기록을 commit 대상으로 선택하며, 기존 untracked `.DS_Store`는 제외한다. 정확한 revision은 새 skill의 Git 이력에서 확인한다. Push는 요청 범위에 포함하지 않는다.
