# Workspace current 폴더화와 repo context 반영

날짜: `2026-08-13`

## 사용자 피드백

첫 output reference의 `memory/state`를 파일 하나씩 두기보다 폴더로 만들어 내용이 주제별로 자연스럽게 늘어날 수 있어야 하고, 현재 문서와 JSON marker가 섞여 사람이 보기 어려운 문제를 보완하라는 요청이 있었다. 동시에 이 작업을 하는 동안 이 저장소 자체의 context도 현재 상태에 맞게 유지하는지 확인했다.

## 반영한 판단

- Workspace의 memory와 state라는 역할은 유지하되 각각 폴더로 만든다.
- memory는 주제별 현재 문서를 둘 수 있지만 모든 과거를 쌓지 않는다. 과거와 상세 검증은 records에 둔다.
- state의 사람용 현재 문제·해석과 harness가 갱신하는 실행 상태를 각각 `index.md`와 `status.json`으로 분리한다.
- Workspace 루트 README를 사람용 첫 화면으로 둔다.
- root `context-harness/context/current/`는 이번 output Workspace의 구현 대상과 다른 이 저장소의 작업대다. 폴더 구조를 소급 적용하지 않고, `memory.md`와 `state.md`의 내용만 이번 작업의 현재 결론과 상태로 갱신한다.

## 구현과 검증

- output runtime의 recovery packet을 schema `2`로 바꾸고 memory 주제 문서·state index·status를 분리해 반환하게 했다.
- `verify`는 기존 Markdown marker 대신 `state/status.json`만 atomic하게 갱신한다.
- symlink memory 주제·current 디렉터리·status를 거부하고, status–receipt 정합성과 receipt 비노출 계약을 유지했다.
- 제품 7개와 harness 15개를 합친 22개 unittest가 통과했다.
- 실제 reference에서 post-migration `recover → verify → recover`를 실행했고 새 pass receipt와 `verified_waiting_acceptance`를 복구했다.
- 사람용 `state/index.md`의 검증 전후 SHA-256이 같았다.
- 독립 검증에서 사람용 Workspace README의 실행 위치가 모호한 문제를 발견해 명령을 `output/` root에서 실행하도록 명시했다.

실제 Workspace 내부 상세와 새 receipt는 [`output migration record`](../../../../reference-project/context/work/workspaces/001-default-timeout/records/2026-08-13-02-current-folder-migration.md)에 있다.

## 남은 범위

- memory direct-child Markdown은 모두 recovery에 들어가므로 문서 수·크기가 증가할 때의 선택 정책은 실제 사용으로 확인해야 한다.
- Workspace 생성·전환·acceptance·완료·보관과 Project canonical 반영은 여전히 미구현이다.
- receipt와 status의 단일 transaction, concurrent verify 조정도 아직 없다.
