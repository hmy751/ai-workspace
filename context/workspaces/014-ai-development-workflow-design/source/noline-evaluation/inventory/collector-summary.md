# Evidence collector 구조 인벤토리

- 이벤트 697개, 작업 `done` 475개, `failed` 222개, 기록 475개.
- 이벤트 시각 범위(UTC): 2026-09-10T13:50:32.452145+00:00 ~ 2026-10-02T11:48:57.712757+00:00. 기록 시각 범위(UTC): 2026-09-10T13:52:57.646704+00:00 ~ 2026-09-21T12:22:10.788192+00:00.
- 첫·마지막 이벤트 사이 저장 이벤트가 없는 KST 날짜: 2026-09-19, 2026-09-20, 2026-09-22, 2026-09-23, 2026-09-24, 2026-09-25, 2026-09-26, 2026-09-27, 2026-09-28, 2026-09-29. 이는 대화·사건 부재의 증거가 아니다.
- 작업별 완료/실패: {"002-code-readability-refactoring": {"done": 455, "failed": 222}, "004-project-context-contracts-and-guidance": {"done": 20}}.
- 실패 원인 문자열: {"runner exit code 1": 222}. 이는 job state의 진단값이며 실제 원인을 단정하지 않는다.
- 마지막 시도의 짧은 stderr 진단: {"codex_cli_unavailable": 221, "codex_exec_failed_1": 1}. `codex_cli_unavailable`은 CLI 이용 불가, `codex_exec_failed_1`은 종료 코드 1만 확인된 경우다.
- manifest gap이 있는 이벤트 0개, 기록의 capture gap 합계 0개. 캡처 gap이 0이라는 값은 의미상 누락이나 사건 부재의 증거가 아니다.
- artifact 항목 7726개; 현재 snapshot 파일 부재 0개, 원본 source 파일 부재 0개. `reference` 항목에는 snapshot이 원래 없다.
- spool queued 694개, submitted 694개, turn state 344개, 수동 full-scan manifest 3개.
- transcript 참조 경로 17개, 현재 파일 부재 0개. 원문 내용은 읽지 않았다.

기존 `record.json` 475개(`record` 469, `index_only` 6)는 이미 생성된 collector 결과로 다시 활용할 수 있다. 이 인벤토리는 기록의 내용이나 사건 적합성을 판정하지 않는다. `failed` 222개에는 대응 `record.json`이 없으므로, 원문·캡처에 사건이 없다고 해석해서는 안 된다.

## KST 이벤트 날짜별 작업 상태

| 날짜 | done | failed |
| --- | ---: | ---: |
| 2026-09-10 | 6 | 0 |
| 2026-09-11 | 71 | 0 |
| 2026-09-12 | 83 | 0 |
| 2026-09-13 | 34 | 0 |
| 2026-09-14 | 159 | 0 |
| 2026-09-15 | 31 | 0 |
| 2026-09-16 | 80 | 1 |
| 2026-09-17 | 8 | 0 |
| 2026-09-18 | 1 | 0 |
| 2026-09-21 | 2 | 0 |
| 2026-09-30 | 0 | 61 |
| 2026-10-01 | 0 | 19 |
| 2026-10-02 | 0 | 141 |

재현: `python3 scripts/collector_inventory.py`. 상세 이벤트·artifact 존재 여부는 `collector-inventory.json`, 입력 경로·해시는 `collector-inputs.json`, 대화 원문 경로는 `collector-transcripts.json`에 있다.
