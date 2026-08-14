# 기준 Project 루트 이름 변경

기록일: `2026-08-14`

## 변경 이유

저장소 루트의 `output/`은 실행 가능한 Project–Workspace–Harness 기준 구현을 소유했지만, 각 Workspace의 `output/`과 이름이 같아 두 책임을 구분하기 어려웠다. 사용자 결정에 따라 루트 기준 Project만 `reference-project/`로 이름을 바꿨다. Workspace `output/`은 각 goal의 선택된 산출물과 실제 canonical 위치를 연결하는 기존 책임을 그대로 유지한다.

## 002 Workspace에 미치는 영향

- 적용 입력과 실행 책임의 canonical은 [`reference-project/`](../../../../reference-project/)다.
- repo-local [`apply-context-harness`](../../../../.agents/skills/apply-context-harness/) skill은 source repository root를 찾은 뒤 `reference-project/` 존재와 `git status --short -- reference-project` 결과를 확인한다.
- 과거 records에서 Workspace `output/index.md`는 계속 Workspace output을 뜻한다. 당시 source root를 가리키는 `output/` 표기는 역사적 이름이며, 현재 접근점은 `reference-project/`다.
- Project common context, schema `4`, recover·verify 계약과 기존 상세 Owner 보존 원칙은 바뀌지 않았다.

## 검증 상한

이번 변경은 source 저장소의 디렉터리명, 내부 링크와 skill의 source lookup·clean check를 새 canonical에 맞춘 것이다. 원본 Payment target과 격리 target을 열거나 재적용하지 않았으므로, 기존 target 상태와 과거 schema `3` 증거를 새 이름이나 schema `4` 검증으로 확장하지 않는다. 실제 target 재적용, target별 `recover → verify → recover`, 독립 review와 사람 acceptance는 여전히 별도 작업이다.
