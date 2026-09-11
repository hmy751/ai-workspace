# Maintainer 자료 구분 보완과 재적용

2026-09-11, 실제 Noline `002 작업 현황 파악` 재생 시험에서 확인한 자료 구분 결함을 Reference Maintain 계약에 보완하고 Noline 설치본에 재적용했다. 기존 [평가 기록](2026-09-11-02-maintainer-material-classification-evaluation.md)의 의미 분류 결함과 첫 실행의 상대 링크 Guard 실패는 별도 문제로 유지했다. 이번 변경은 의미 분류와 정정 영향 범위에 한정하며 Guard의 링크 생성·자동 재시도 동작은 바꾸지 않았다.

## 적용한 기준

- current에는 현재 유효한 기준·계약·실행 범위·진행·결과와 다음 행동을 정규화한다.
- current가 바뀐 뒤에도 다시 살펴야 할 조사 과정, 선택·탈락 이유, 철회된 전제, 실패와 상세 근거는 records에 둔다.
- 같은 사건이 두 층을 모두 바꾸면 current에는 현재 의미, record에는 과정 근거를 두며 같은 서술을 복제하지 않는다.
- 채택 날짜·turn·발화 원문·대화 순서는 계속 필요한 근거일 때 records에 두며, 사용자의 `기록해 달라`는 요청만으로 current에 옮기지 않는다.
- state를 갱신할 때는 파일 전체의 끝난 진행 경위·접수 이력·일회성 보고를 확인해 현재 단계·다음 행동·유효한 제약·실제 결과와 미확인만 남긴다.
- 정정이나 단계 변화에서는 바뀐 의미를 직접 사용한 선택된 Workspace의 current 문서를 제한적으로 찾아 교정할 수 있다. 색인은 변동 상태의 두 번째 정본으로 만들지 않는다.
- 임시 전달 파일과 제거될 수 있는 session 경로를 current의 지속 근거로 삼지 않는다. 필요한 최소 원문과 출처는 Workspace record에 보존한다.

Reference의 `context/work/harness/maintain/README.md`와 수동 fallback role인 `workspace-context-maintainer.toml`에 같은 의미 기준을 반영했다. 실제 자동 semantic 경로의 `codex_session.py`에는 정정·단계·선택 변화가 직접 의존한 current 문서를 선택된 Workspace 안에서만 찾을 수 있는 read-only 범위를 추가했다. prompt 계약 테스트는 두 새 규칙이 실제 입력에 들어가는지 확인한다.

## 같은 사례의 재시험

첫 보완본은 고정한 역사 fixture와 같은 여덟 입력으로 `run02`에서 다시 실행했다. 실제 여섯 입력과 합성 대조 두 입력이 모두 Guard 오류나 Main의 수동 보조 없이 끝났다.

- 추가 조사에서는 과정 근거 문서를 records에 만들고 current의 후보·Spec·Ticket·state에는 현재 유효한 내용을 연결했다.
- 사용자 정정에서는 현재 Spec·state를 긍정적인 유효 기준으로 고치고, 오해와 철회 이유는 별도 correction record에 보존했다.
- 단순 설명과 합의 재설명은 `no_change`였다.
- 첫 대상 선택은 Ticket·state만 변경했고, memory 색인은 진행 상태를 복제하지 않아 충돌이 남지 않았다.
- 새 reader는 원대화나 평가 자료 없이 records의 조사·정정 근거를 선택해 첫 범위, 정정된 Ticket 의미, 조사와 실행 증거의 차이, 전체 완료 상한을 복구했다.

이 실행에서 채택 날짜와 발화 원문이 여전히 Spec에 들어가고, state가 과거 운영 경위를 길게 유지한 잔여 결함을 확인했다. `correction-scope`가 요구하는 같은 어긋남의 반복 조건에 따라 `ai-self-check`를 한 번 적용했다. 독립 auditor는 실제 완료 artifact부터 다시 확인하고 의미 분류와 링크 집행 실패를 분리하며, 확인된 반복 결함에만 최소 변경을 적용한 뒤 같은 replay와 fresh reentry로 확인하라고 판정했다.

잔여 결함을 보완한 뒤 `run02`의 정정 완료 시점에서 채택·재설명·첫 대상 선택 세 입력을 새 semantic session의 `run03`으로 재생했다. 채택된 현재 기준은 Spec과 품질 기준에 정규화됐고, 날짜·turn·정확한 발화와 임시 전달 자료의 최소 내용은 새 record로 분리됐다. 재설명은 `no_change`, 첫 대상 선택은 Ticket·state 갱신이었다. state는 UTF-8 8,336 bytes에서 4,254 bytes로 줄었고 현재 단계·다음 행동·유효한 한계는 유지됐다. 정확한 채택 발화는 current에서 사라지고 records에 남았으며 current에 `/private/tmp` 경로는 없었다.

`audit-v3.json`은 세 decision의 선언 경로와 실제 변경, preimage·최종 content hash, Guard 뒤 fixture, 네 Maintainer turn과 fresh reader 한 turn의 read-only runtime을 대조한다. fresh reader도 새 record를 근거로 세 질문을 복구했다. 이 결과는 고정한 한 Workspace 사례와 두 합성 lifecycle 입력의 동작을 증명하며, 장기 운영의 모든 자료 유형이나 실제 host lifecycle 전체를 증명하지 않는다.

## Noline 설치본과 검증

Reference 보완 뒤 실제 Noline 설치본의 고유한 Claude 연결 설명과 Noline용 role 이름은 유지하고 동일한 행동 기준을 적용했다. `codex_session.py`와 해당 test는 Reference와 같은 bytes이며 README·TOML은 Noline 고유 문구 때문에 전체 hash는 다르다. 적용 전부터 사용자가 수정 중이던 `context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/01-expense-totals.md`는 건드리지 않았다.

Reference와 Noline에서 Maintain의 `test_codex_session`·`test_operation` 22개가 각각 통과했고 양쪽 `git diff --check`도 통과했다. 적용 기준 Noline HEAD는 `25d401f1d7b42d843500a7b66fc9087574a176d5`였고, 적용분은 `dac4e60` (`fix: Maintainer 자료 구분 기준 보완`)으로 커밋했다. 실제 host activation, 제품 코드·검사, Noline의 현재 002 문서 자체 재작성은 이번 범위가 아니다.

Reference 전체 `test_*.py` 124개에서는 123개가 통과했고 `test_timeout_covers_descendant_after_group_leader_exits` 한 건이 실패했다. 0.4초 timeout 전에 descendant pid 파일이 생성되지 않은 Verify timing 실패이며 이번 수정 파일을 사용하지 않는다. 이번 변경 전 전체 실행과 해당 test의 단독 실행에서도 같은 실패를 확인했으므로 Maintain 보완의 회귀로 판정하지 않았다.

전체 실행물은 [시험 evidence 진입점](receipts/maintain-eval/2026-09-11-material-classification/README.md), 최종 좁은 실행 요약은 [`run03/summary.json`](receipts/maintain-eval/2026-09-11-material-classification/run03/summary.json), 파일·runtime 대조는 [`audit-v3.json`](receipts/maintain-eval/2026-09-11-material-classification/audit-v3.json), fresh 답변은 [`reentry03/answers.json`](receipts/maintain-eval/2026-09-11-material-classification/reentry03/answers.json)에 있다.
