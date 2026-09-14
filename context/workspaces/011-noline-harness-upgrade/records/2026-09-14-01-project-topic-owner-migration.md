# Project 주제별 Owner 이동 계약 보완

## 관찰한 문제

Noline `002-code-readability-refactoring`의 완료 Ticket 01~05 자료와 records를 Project context에 반영한 결과를 사용자와 검토했다. 새 `current/implemented-behavior-and-verification.md`는 여러 성격의 주제를 Ticket 근거 묶음이라는 이유로 한 문서에 모았고, 실제 의미 대신 기존 `.claude` 문서 링크를 주로 제시했다. 그 결과 다음 작업이 공통 계약으로 읽을 책임 단위, `common/current/guidance` 사이의 배치, 이전 문서와 새 문서의 authority 관계를 복원하기 어려웠다.

기존 Reference 계약에는 선택 문서가 링크 없이 의미를 설명해야 하고 수명·갱신 Owner가 다른 내용을 합치지 말아야 한다는 기준이 이미 있었다. 따라서 결과 전체를 원천 설계 부재로 해석하지 않았다. 다만 기존 계약은 초기 이식에서 상세 canonical을 보존하는 기본값과 승인되지 않은 Owner 이동의 차단에는 강했지만, 설치 후 사용자가 일부 주제만 Project 정본으로 옮기도록 승인했을 때 그 이동을 어떻게 구성하고 끝낼지는 충분히 명시하지 않았다.

## 채택한 판단

- Owner 이동은 Project 문서 전체가 아니라 사용자가 한정한 주제·책임 범위별로 승인할 수 있다. 이미 승인된 범위는 다시 묻지 않고 전환을 끝낸다.
- Ticket, Workspace, 회의와 evidence 묶음은 조사·근거 경계이며 문서 책임이 아니다. Project 본문은 다음 작업이 찾을 지속 주제, 판단 질문, 수명과 갱신 Owner를 기준으로 구성한다.
- 지속 의미는 `common/`, 교체되는 구현·지원·proof 경계는 `current/`, 조건부 판단은 `guidance/`, 별도로 보존할 중요한 선택 이유는 `decisions/`가 맡는다.
- 이동한 Project 문서는 자신이 맡은 현재 의미를 본문으로 설명하는 canonical이다. 상세 링크는 구현·원문·검증을 재대조하는 경로이며 내용의 대체물이 아니다.
- 이전 canonical은 유효한 뜻을 통합한 뒤 구현 상세, 근거·역사, 호환 routing 중 실제 남은 역할로 좁히거나 target 규칙에 따라 전환한다. 같은 현재 답의 active canonical을 둘 남기지 않는다.
- Owner 이동과 새로운 제품 결정은 구분한다. 충돌하거나 미정인 선택만 열린 판단으로 남기고, 확인된 나머지는 먼저 옮긴다.
- Path·책임·authority가 바뀌면 root·layer index뿐 아니라 현재 live Workspace의 Project 선택과 사람용 current·output도 Work reconciliation 계약에 맞춘다. 역사 Workspace 전체는 역동기화하지 않는다.

## Source 반영

- `reference-project/context/project/README.md`: 각 내용 문서의 주제별 authority와 이동된 범위·기존 상세 Owner의 관계를 명시했다.
- `reference-project/context/project/MAINTENANCE.md`: 승인된 주제별 Owner 이동의 구성·분리·이전 문서 처리·consumer reconciliation 완료 조건을 추가했다.
- `reference-project/.agents/skills/update-project-context/SKILL.md`: 일반 갱신·누락 복원·승인된 Owner 이동을 구분하고, 이동을 실제로 수행하는 절차와 fresh-reader 확인을 추가했다.
- `reference-project/AGENTS.md`와 `.agents/skills/README.md`: Project root와 skill 색인에서 승인된 주제별 Owner 이동 요청을 갱신 skill로 발견하게 했다.
- `.agents/skills/apply-context-harness/SKILL.md`와 `references/application-contract.md`: 초기 이식에서도 주제별 유지·이동 승인 범위, Ticket 묶음과 문서 책임의 구별, 이전 canonical의 disposition을 manifest·적용·완료 조건에 포함했다.

이번 변경은 문서 계약과 skill 실행 지침의 의미를 보완한다. Recover schema 6은 이미 `common/current/guidance/decisions` 아래의 실제 문서를 선택할 수 있고, nested Markdown과 ordered selection을 지원하므로 runtime·schema 변경은 필요하지 않았다. Maintain의 Project 문서 쓰기 금지와 Workspace reconciliation의 Owner 경계도 유지했다.

## 검증과 경계

변경 전 source 기준은 `9c2fa98108b7f0b5706589947a4c79e9b05dfa5b`이며 기존 working tree 변경은 untracked `.DS_Store` 하나였다. 이 파일은 읽거나 수정하지 않았다.

`git diff --check`와 변경 문서의 local link 140개 검사가 통과했다. Skill Creator의 `quick_validate.py`는 환경에 PyYAML이 없어 시작하지 못했으므로, 같은 frontmatter 허용 key·이름 형식·설명 길이·TODO 기준을 Ruby YAML로 대조해 두 skill이 통과함을 확인했다. 관련 과거 표현의 검색 결과는 현재 계약에서 제거됐고, 이전 적용 당시 receipt에 보존된 한 건만 역사 원문으로 남았다.

Reference 전체 126개 회귀 검사의 첫 실행에서는 기존에도 관찰된 `test_timeout_covers_descendant_after_group_leader_exits` 타이밍 테스트 한 건이 실패했다. 해당 테스트 단독 재실행은 통과했고 이어 전체 126개 재실행도 통과했다. 이번 변경은 문서·skill 지침뿐이며 Verify runtime은 수정하지 않았다. 이 검사는 지침 구조와 기존 runtime 회귀의 정합성을 확인하는 범위로, 실제 AI가 Noline 자료를 원하는 책임 단위로 재구성하는 품질이나 target live consumer 전환을 증명하지 않는다.

이번 단계에서는 Noline 파일을 수정하지 않았다. Noline 재적용에서는 현재 working tree와 기존 `.claude` canonical을 다시 대조하고, 완료 Ticket 01~05와 관련된 승인 범위만 `context/project`의 주제별 문서로 재구성한 뒤 이전 문서 역할·Recover 선택·live consumer를 함께 맞춰야 한다. Ticket 06 이후 미완성 작업과 Project 문서 전체 개편은 이번 source 반영의 자동 범위가 아니다.
