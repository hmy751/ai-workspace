from pathlib import Path
p=Path('/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/001-noline-context-harness-application/records/2026-09-09-01-reference-upgrade.md')
s=p.read_text();needle='Reviewer는 실패 test 본문과 Verify runtime이 baseline에서 달라지지 않았으며,'
s=s.replace(needle,'서면 provenance는 Source `context-harness`의 `context/workspaces/011-noline-harness-upgrade/records/review/2026-09-09-installed-independent-review.md`다. 이 기록에는 target에서 다시 판단할 핵심 결과와 한계를 직접 보존했다. Reviewer가 직접 대조한 이전 Verify는 `8e8696f` 사건이며, 이 결과를 현재 문서에 반영한 뒤 새 Verify→Recover로 최종 cursor를 연결한다.\n\n'+needle);p.write_text(s)
