# Project context Owner omission loophole 교정

## 사용자 정정

V3 blind 재적용은 링크-only Project common context를 개선했지만 `README.md`, `overview.md`, `architecture.md`만 만들었다. Target 상세 Owner에는 여러 Workspace가 반복해서 사용할 독립된 공통 product criteria와 recovery decision이 있었으므로 대응 `prd/`·`decisions/` Project context Owner를 생략한 상태였다.

따라서 [`v3 forward-test record`](2026-08-16-02-semantic-content-closure-correction-and-v3-forward-test.md)의 기술적 이식·검증 사건은 그대로 보존하되, semantic content closure가 완전히 통과했다는 결론은 현재 결론이 아니다. V3는 링크 문제를 개선했지만 “선택 문서가 내용을 채우면 나머지는 생략할 수 있다”는 omission loophole을 드러냈다.

상세 target 관찰과 사용자 정정은 [`Workspace 002 correction record`](../../002-project-application/records/2026-08-16-03-project-context-owner-closure-correction.md)가 소유한다.

## Skill 재보강

Main은 `apply-context-harness`와 application contract에 다음 규칙을 추가했다.

- Overview는 구분되는 Project common 책임의 진입 요약이며 독립 Owner를 없애는 합본이 아니다.
- Target 상세 Owner에 구분되는 제품 기준, 구현 구조 또는 채택 결정이 있으면 각각 대응하는 Project context Owner를 만들고 실제 내용으로 채운다.
- Owner omission은 원자료에 독립된 공통 내용이 없을 때만 허용한다.
- 조사한 상세 Owner와 omission 근거를 dry-run manifest와 application record에 남기고 책임별 closure를 검토한다.

이 보강은 exact Reference 실행 계약을 skill에 다시 복제하지 않고 target 내용 선택 방법을 강화한다.

## 현재 상태와 proof ceiling

최신 skill 교정 뒤 실행 테스트나 Terra blind 재시험은 하지 않았다. 이번 유지보수도 Workspace 004 문서 diff만 갱신했다. 따라서 새 규칙이 v3 omission을 실제 target에서 막는지, 다른 Project에서도 책임을 충분히 나누는지는 아직 증명하지 않았다.

Source skill과 Workspace 문서는 commit하지 않았고 target acceptance도 없다. V2·v3의 Product Verify와 Recover 결과는 당시 실행 사실이지만 Project context Owner completeness를 증명하지 않는다. 반복 Harness timing race, 서로 다른 Project portability, 외부 제품 경계와 사람 acceptance도 미검증으로 남는다.
