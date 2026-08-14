# 기준 Project 루트 이름 변경

날짜: `2026-08-14`

## 사용자 결정과 이유

사용자는 저장소 루트의 `output/`이 각 Workspace가 가진 `output/`과 같은 이름이라 역할이 헷갈린다고 지적했다. `starter-kit/`도 후보였지만, 통째로 복사해 새 Project를 시작하는 재료로 오해하지 않도록 실행 가능하고 검증된 기준 구현이라는 책임을 드러내는 `reference-project/`를 선택했다.

## 변경 범위

- 저장소 루트 `output/`을 `reference-project/`로 이름 변경했다.
- Workspace별 `output/`은 각 goal을 위해 선택된 현재 결과와 실제 canonical 위치를 연결하는 기존 책임을 유지한다.
- 루트 진입 문서, repo-local 적용 skill, context 문서와 현재 유효한 링크를 새 경로에 맞췄다.
- Project common context, Work context, Workspace, Harness의 내부 계약과 schema는 바꾸지 않았다.
- 과거 record에서 당시 경로를 설명하는 `output/` 문구는 역사적 사실로 남길 수 있으며, 현재 파일로 다시 들어가는 링크만 `reference-project/`를 향한다.

## 검증

- `reference-project/`에서 `python3 -B -m unittest discover -s . -p 'test_*.py' -v`: 제품 7개, recover 21개, verify 9개로 총 37개 통과
- `reference-project/` Markdown 로컬 링크 90개 검사: 누락 0개
- 실제 `recover -> verify -> recover`: 통과
- 최신 pass receipt: [`verify-20260814T064854356201Z-2b17198a679c47e0ba9f7bbc23aefad6.json`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/verify-20260814T064854356201Z-2b17198a679c47e0ba9f7bbc23aefad6.json)
- machine status: 같은 receipt를 가리키는 `verified_waiting_acceptance`
- 후속 recover: packet schema `5`, current 6개·Workspace output index 1개·Project context 2개 로드

## 검증 상한

이 검증은 이름 변경 뒤 기준 Project의 구조·명령·recovery 링크가 계속 동작함을 확인한다. 사람 acceptance, 다른 실제 Project에서의 이식 의미 정확성, 운영 효과를 증명하지 않는다.
