# Harness maintenance bottleneck state

마지막 갱신: `2026-08-17`

## 현재 문제

V3 blind 재적용은 링크형·첫 Workspace 요약형 common context를 개선했지만, target 원자료에 독립된 공통 product criteria와 recovery decision이 있는데도 `README.md`·`overview.md`·`architecture.md`만 만들고 대응 `prd/`·`decisions/` Owner를 생략했다. 따라서 v3는 semantic content closure의 완전한 통과가 아니다.

## 현재 상태

- Reference 책임 재배치는 commits `638bfbc`, `7793bab`에 보존됐다.
- V3의 Project common README·overview·architecture는 링크-only 문제를 개선했고 당시 Product Verify `11/11`과 Recover snapshot `35/35 fresh`를 보존했다. 이 실행 증거는 유효하지만 누락된 공통 Owner의 의미 충분성을 증명하지 않는다.
- Main은 [skill 본문](../../../../.agents/skills/apply-context-harness/SKILL.md)과 [application contract](../../../../.agents/skills/apply-context-harness/references/application-contract.md)에 overview 합본 금지, 구분되는 공통 책임별 대응 Project context Owner 의무, 독립된 공통 내용 부재가 원자료로 확인된 경우만 omission 허용, manifest·application record에 생략 근거 보존을 추가했다.
- 최신 skill 교정 뒤 실행 테스트·Terra 재시험은 하지 않았다. Skill과 Workspace 문서는 Git history에 보존했지만 사람 acceptance는 없다.
- 최신 결론은 [`2026-08-16-03`](../records/2026-08-16-03-project-context-owner-omission-loophole-correction.md), 상세 사용자 정정과 target 근거는 [`Workspace 002 correction record`](../../002-project-application/records/2026-08-16-03-project-context-owner-closure-correction.md)가 소유한다. V2·v3 records는 각각 당시 사건으로 보존한다.
- Skill 간소화와 Workspace 002·004 정합화는 commit `f082035`에 보존됐다.
- 사용자는 이후 운영 지연과 지속 context 관리 논의를 새 작업으로 분리했다. 일반 운영 cadence, background maintainer와 Verify 범위는 [`Workspace 005`](../../005-context-continuity-maintenance/)에서 이어 간다.

## 검증 상한과 남은 판단

- 최신 Owner closure 교정은 아직 target에 재적용하지 않아 omission loophole 해소를 실행으로 증명하지 않았다.
- 앞선 재적용은 같은 Payment target의 새 사본을 사용했으므로 서로 다른 Project portability나 generalization을 증명하지 않는다.
- 새 target-scoped Codex role discovery, 실제 PG·DB·WebView·브라우저와 사람 acceptance는 검증하지 않았다.
- 이 Workspace에는 사람 acceptance, 최신 skill 교정의 재시험과 서로 다른 Project에서 portability를 다시 볼지에 대한 판단이 남아 있다.
- 같은 timing test의 반복 실패를 일반 운영 결함으로 다루는 문제는 Workspace 005로 옮겼다. 다만 그 결함이 최신 skill 재시험을 실제로 막으면 결과만 이 Workspace의 검증 상태에 다시 반영한다.

## 다음 행동

현재 active action은 없다. 이 Workspace를 재개할 때 최신 Owner closure 교정을 별도 blind target에 재시험할지 먼저 결정한다. 재시험 전에는 semantic content closure 완료나 acceptance로 올리지 않는다.
