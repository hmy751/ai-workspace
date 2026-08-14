# Harness maintenance bottleneck state

마지막 갱신: `2026-08-14`

## 현재 문제

Machine receipt 저장 경로를 바꾸는 작업은 실제 runtime 테스트보다 같은 계약을 여러 문서와 Workspace에 반영하고 순차 maintainer·review를 기다리는 데 더 많은 시간이 들었다. 어떤 반영이 필수 정합성이고 어떤 반영이 중복인지 아직 구분 규칙이 없다.

## 현재 확인된 사실

- 직전 변경은 commit `179bdc2`에 보존됐다.
- Reference 전체 40개 테스트는 약 4초 안에 끝났고 helper 테스트도 Python 버전별 약 2초였다. 이번 약 20분 작업의 주된 지연은 제품 build나 Harness runtime 실행이 아니었다.
- 한 machine receipt 경계 변경이 runtime·테스트, 기준 Project 문서, 이식 skill, 기존 receipt 10개와 직접 링크, 001·002 Workspace current·records까지 전파됐다.
- 001과 002 context maintenance를 한 실행 주체에 순차로 맡겼고, 최종 독립 review까지 기다렸다.
- 같은 계약을 `reference-project/`, skill, 001 current, 002 current에서 다시 설명해 변경 전파면이 커졌다.

## 아직 확인할 것

- 각 반복 문장이 실제로 독립 Owner 책임인지, 다른 canonical을 가리키면 충분한 파생 설명인지
- Context maintainer를 Workspace별 병렬 실행해도 의미 결정이나 같은 파일 충돌이 생기지 않는 범위
- 독립 review가 필요한 변경과 일반 test·link check로 충분한 변경의 기준
- Context를 옮기거나 새 Workspace를 만들 때 main이 과도한 공통 체크리스트 없이 변경 성격에 맞는 최소 확인을 선택하는 기준
- 약 20분 중 문서 편집, agent 대기, review, 재검증이 각각 차지한 정확한 시간. 현재 수치는 정밀 계측이 아니라 이번 실행 관찰에 기반한다.

## 다음 행동

직전 machine receipt 변경을 한 사례로 삼아 변경된 규칙마다 다음을 표시한 병목 지도를 만든다.

1. 실제 canonical Owner
2. 반드시 함께 바뀌어야 하는 consumer
3. 링크만 갱신하면 되는 기록
4. 갱신할 필요가 없었던 중복 설명
5. 필요한 검증과 생략 가능한 반복 검증

이 지도를 먼저 검토한 뒤에만 root 지침, skill, context maintainer routing 또는 문서 배치를 수정한다.

이번 Workspace 생성은 문서·routing 변경이므로 로컬 링크, active 표기, Git diff만 확인한다. Reference runtime과 receipt 계약은 바뀌지 않아 full test와 독립 review를 다시 실행하지 않는다.
