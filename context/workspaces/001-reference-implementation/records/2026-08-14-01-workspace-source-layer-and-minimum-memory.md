# Workspace source 층과 최소 memory 계약

날짜: `2026-08-14`

## 작업 목적

실행 가능한 reference의 각 Workspace에 `current/`, `source/`, `records/`를 형제로 두고, 다음 재진입에서 항상 필요한 memory 세 파일을 runtime 계약으로 고정한다.

이 변경은 source를 Harness의 입력으로 흡수하려는 것이 아니다. 작업이 실제로 선택한 원문과 snapshot의 provenance를 현재 판단·작업 기록과 분리해서 보존하되, 기본 recovery context는 작고 명시적으로 유지하기 위한 것이다.

## 확정한 책임

- `current/`: 지금도 유효하여 다음 행동에 필요한 목표, 제약, Project 선택 경계와 최근 상태
- `source/`: 해당 Workspace가 작업 입력으로 선택한 원문, 변경하지 않은 snapshot, provenance
- `records/`: source와 실제 작업을 바탕으로 만든 분석, 결정, 실행·검증 기록

`source/index.md`는 source inventory의 최소 진입점이다. 별도로 보존한 원자료가 없다면 그 사실과 Project canonical을 복제하지 않았다는 경계를 적는다.

원자료의 저자와 정본 권위는 원래 출처에 남는다. Workspace는 원자료 자체의 새 정본이 되는 대신 다음을 책임진다.

- 실제 사용한 선택 범위와 사용 시점
- snapshot 또는 원래 위치로 다시 접근할 경로
- 가능한 경우 commit, version, SHA-256 같은 무결성 근거
- 현재 판단·분석·결정·실행 기록과 source의 분리 유지

## 실제 reference 변경

- sample Workspace에 [`source/index.md`](../../../../output/context/work/workspaces/001-default-timeout/source/index.md)를 추가했다.
- [`Workspace collection 안내`](../../../../output/context/work/workspaces/README.md)와 각 상위 진입점에서 `current/source/records`의 형제 관계와 source 책임을 설명한다.
- sample Workspace의 [`README.md`](../../../../output/context/work/workspaces/001-default-timeout/README.md)에서 사람의 source 재확인 경로를 추가했다.
- `current/memory/`의 `01-goal.md`, `02-constraints.md`, `03-project-context.md`를 모든 Workspace recovery에 필요한 최소 memory로 정했다.
- recover는 최소 memory 세 파일 중 하나라도 없으면 실패한다.
- recover는 Workspace `source/`의 존재나 내용을 검사하지 않고, inventory나 원문을 기본 recovery packet에 싣지 않는다.
- repo-local `apply-context-harness` skill에는 같은 구조를 복제 보관하지 않고, 대상 Project의 실제 source와 canonical 경계에 맞춰 이식하는 절차와 검증 항목만 반영했다.

## 검증

### 자동 테스트

Project root인 `output/`에서 다음 명령을 실행했다.

```bash
python3 -B -m unittest discover -s . -p 'test_*.py' -v
```

총 31개가 통과했다.

- recover 책임 테스트: 15개
- verify 책임 테스트: 9개
- 제품 config loader 테스트: 7개

새 테스트는 최소 memory 세 파일이 각각 없을 때 recover가 실패하는지, `source/`를 제거해도 recover가 성공하는지, source inventory와 원문 표식이 recovery packet에 들어가지 않는지 확인한다.

repo-local application skill helper 테스트 7개도 통과했고 skill validator 결과는 `Skill is valid!`였다.

### 실제 reference 순환

`recover → verify → recover` 순환이 통과했다.

- 새 product receipt: [`verify-20260813T163439925334Z-bd9a7ed98d7c468797d2efc12d1505f4.json`](../../../../output/context/work/workspaces/001-default-timeout/records/verify-20260813T163439925334Z-bd9a7ed98d7c468797d2efc12d1505f4.json)
- receipt result: `pass`
- 제품 unittest: 7개 통과
- machine status: 같은 receipt를 가리키는 `verified_waiting_acceptance`
- 후속 recover: 새 status와 receipt header를 다시 연결하면서 Workspace source는 읽지 않음

## 검증 상한

- 이 검증은 한 reference Project에서 source 책임의 구조와 recover의 비의존성을 확인한다. 실제로 보존한 source의 provenance 품질이나 원래 출처의 가용성을 검증하지 않는다.
- 실행 산출물 `output/` 바깥에 있는 작업대의 공유 [`context/source/`](../../../source/)는 reference를 설계할 때 사용한 원자료 층이다. 이를 `output/` Workspace의 `source/`로 자동 복제하거나 migration하지 않는다.
- 이미 context harness를 적용한 기존 target은 이 reference와 skill 변경만으로 자동 migration되지 않는다. 대상별 기존 canonical과 사용자 변경을 다시 고정한 별도 적용 작업이 필요하다.
- 다른 실제 Project에서의 이식 가능성, Workspace 수명주기, acceptance, Project canonical 반영, concurrent verify와 receipt/status 단일 transaction은 이번 변경이 증명하지 않는다.
