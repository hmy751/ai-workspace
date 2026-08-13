# Workspace current 폴더화와 사람·기계 상태 분리

날짜: `2026-08-13`

## 변경 이유

기존 `current/memory.md`는 목표·완료 기준·제약·Project 접근점을 한 파일에 모아 Workspace가 커질수록 읽고 관리하기 어려웠다. `current/state.md`는 사람이 읽는 설명과 harness가 갱신하는 JSON marker를 섞어 두 역할의 경계도 화면에서 잘 드러나지 않았다.

## 변경한 구조

- Workspace 루트 `README.md`: 사람이 가장 먼저 읽는 위치와 순서
- `current/memory/index.md`: 현재 memory 지도와 추가 기준
- `current/memory/01-goal.md`, `02-constraints.md`, `03-project-context.md`: 계속 유효한 맥락을 주제별로 분리
- `current/state/index.md`: 사람이 유지하는 현재 문제와 해석 경계
- `current/state/status.json`: harness가 갱신하는 최근 결과, receipt, 완료 시각, 다음 행동
- `records/`: 이전 상태와 상세 검증 결과를 계속 누적

`recover`는 memory index와 같은 폴더의 direct-child Markdown을 파일명 순으로 읽는다. 중첩 폴더, Markdown이 아닌 파일, records 전체는 기본 context에 넣지 않는다. `verify`는 사람용 `state/index.md`를 수정하지 않고 `status.json`만 atomic하게 교체한다.

## 실행 검증

- 제품 테스트 7개와 harness 테스트 15개, 총 22개 unittest 통과
- 실제 Workspace recovery packet schema `2`로 재복구 성공
- 실제 로드 순서: memory index → 번호가 붙은 memory 3개 → state index → status JSON → 선택된 Project 문서 2개
- 연결 receipt는 state 정합성 확인용 control path로만 읽고 context 본문에는 싣지 않음
- 같은 고정 제품 검증 7개 통과, exit `0`
- 새 receipt: [`verify-20260813T045930913927Z-e6a729ee16834df8a16d1fc7d412e5ab.json`](verify-20260813T045930913927Z-e6a729ee16834df8a16d1fc7d412e5ab.json)
- 검증 전후 `state/index.md` SHA-256이 `3360a031e6054e594d94ace6b4007dafad422e83883241017b94c1aacbe81ead`로 같아 사람용 문서가 보존됨
- 검증 뒤 `status.json`이 새 pass receipt를 가리키고 후속 `recover`가 이를 다시 확인함
- 독립 검증에서 Workspace README의 명령 실행 기준 디렉터리가 모호해 Workspace 안에서 실행하면 실패하는 문제를 발견했고, `output/` root에서 실행한다고 명시함

## 경계

memory 폴더는 과거를 쌓는 곳이 아니다. direct-child Markdown이 모두 기본 recovery에 포함되므로, 지금도 유효하고 매 재진입에 필요한 주제만 남겨야 한다. 과거 상태와 상세 결과는 records가 소유한다.

현재 runtime에는 memory 문서 수나 전체 byte 상한이 없다. Workspace가 커질 때 무조건 파일을 늘리면 context가 다시 비대해질 수 있으므로, 실제 사용에서 문제가 확인되기 전까지는 index와 현재성 규칙으로 관리한다. receipt 작성과 status 갱신은 하나의 transaction이 아니며 동시 `verify`도 조정하지 않는다.
