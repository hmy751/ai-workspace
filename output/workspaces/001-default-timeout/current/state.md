# Workspace state

config loader와 Project 테스트를 대상으로 고정된 검증 명령을 반복 실행한다. 현재 cursor, 최근 결과, receipt와 다음 행동은 아래 marker가 소유한다.

아래 marker는 harness가 소유한다. 수동 편집하지 않는다.

<!-- workspace-state:begin -->
{
  "schema_version": 1,
  "workspace_id": "001-default-timeout",
  "status": "verified_waiting_acceptance",
  "result": "pass",
  "receipt": "workspaces/001-default-timeout/records/verify-20260812T184205182632Z-fdc6909a55634d82b1156fb825e490b3.json",
  "finished_at": "2026-08-12T18:42:05.182Z",
  "next_action": "receipt와 선택된 Project 기준의 정합성을 검토하고 이 작업을 수락할지 명시적으로 결정한다."
}
<!-- workspace-state:end -->

검증 뒤 상세 stdout, stderr, evidence hash는 marker에 복사하지 않고 연결된 receipt에서 확인한다.
