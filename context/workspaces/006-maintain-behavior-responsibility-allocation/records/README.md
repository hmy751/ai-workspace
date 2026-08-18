# Records

이 폴더에는 Reference Maintain 내부 책임 배치를 검토하며 만든 지속 가능한 동작 분석, 후보 비교, 사용자 결정, 변경 이유와 검증 결과를 누적한다.

- 파일명은 `YYYY-MM-DD-NN-주제.md` 형식을 사용한다.
- 운영상 하나인 동작, 지켜야 할 약속과 현재 책임 배치를 먼저 기록하고 구현 후보는 구분한다.
- 모델·규칙 기반 장치·사람에게 책임을 둔 이유와 이동·제거 시 영향을 남긴다.
- 코드·지침·prompt·schema·config·test가 표현·집행·검증하는 내용을 혼동하지 않는다.
- Workspace 005의 구현 이력을 복제하지 않고 필요한 baseline record를 링크한다.
- 임시 탐색과 아직 선택하지 않은 후보를 current나 output으로 올리지 않는다.

## 기록

- [`2026-08-18-01-initial-responsibility-scan-and-root-binding-test.md`](2026-08-18-01-initial-responsibility-scan-and-root-binding-test.md): 이전 Maintain 계약을 다시 고정한 작업 범위, 현재 기준선, 가변 root Workspace 선택과 portable Reference test의 결합, 본격 분석 순서를 기록
- [`2026-08-18-02-response-end-responsibility-map-and-first-slice.md`](2026-08-18-02-response-end-responsibility-map-and-first-slice.md): response-end 판단부터 write·report·checkpoint·intent cleanup까지의 책임 지도, 첫 fail-closed 개선과 검증 결과
- [`2026-08-18-03-self-check-and-purpose-first-reset.md`](2026-08-18-03-self-check-and-purpose-first-reset.md): self-check 판정, Workspace 005 records 01–09에서 복원한 사용자 목적과 실패 흐름, 현재 topology 보존을 중단하고 최소 책임 구조로 돌아간 기준
- [`2026-08-18-04-completed-response-and-workspace-attention.md`](2026-08-18-04-completed-response-and-workspace-attention.md): completed response에만 처리 순서를 부여하고 session report를 Workspace attention으로 교체한 첫 구조 개선, migration·crash 경계·검증과 남은 과제
- [`2026-08-18-05-clean-room-restart-decision.md`](2026-08-18-05-clean-room-restart-decision.md): 기존 구현 개선 접근을 중단하고 005 합의와 pre-implementation code baseline에서 별도 Workspace로 재시작하기로 한 결정
