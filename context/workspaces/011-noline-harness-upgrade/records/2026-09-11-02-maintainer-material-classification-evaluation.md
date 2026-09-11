# Maintainer 자료 구분 실제 시험 결과

2026-09-11, Noline의 `002 작업 현황 파악`을 참고해 기존 Maintainer를 실제 모델로 시험했다. **현재 의미를 이해하고 정정을 반영하는 능력은 확인됐지만, 현재 정보와 과정 기록을 구분하는 능력은 부족했다.** 단계 전환 뒤 현재 문서 사이에 서로 다른 상태도 남았다. 새로운 세션은 그 불일치를 알아채고 작업을 복구했다.

첫 수정안은 잘못 만든 상대 링크 때문에 Guard가 거부했다. 그 실패를 보존한 뒤 Main이 링크 한 곳만 수정하여 나머지 시험을 이어갔다. 따라서 아래는 **한 번의 수동 보조가 들어간 의미 판단·재진입 시험**이며, 자동으로 끝까지 성공한 실행은 아니다.

## 무엇을 실행했나

사용자는 Maintainer의 기록 능력과 Workspace 내부 자료 구분을 의심하며 위 작업을 참고로 지정했고, 실제 시험과 결과 확인 및 correction-scope 관점을 요청했다. 최초 자료 전송은 자동 승인 심사에서 거절됐으나, 전송 범위 설명 뒤 사용자가 “해봐”라고 승인해 실제 실행했다. 초기 관찰과 핵심 원문은 [시험 설계 기록](2026-09-11-01-maintainer-material-classification-test-design.md)에 있다.

Noline commit `a612ba4c49b92b1193e75e1d56bdefcdcd86bbda`를 임시 Project로 복원하고, commit 뒤 실제 Maintainer의 state 변경을 적용했다. 다음 조사 시점의 state 원문 hash와 일치했다. 사라진 임시 조사·합의 문서도 당시 Main의 파일 작성 입력에서 복원하여 과거 hash와 대조했다. 원래 Noline 작업과 실제 문서는 수정하지 않았다.

기존 `CodexMaintainSession`과 Guard를 변경 없이 사용했다. Codex CLI `0.153.4`가 OpenAI의 `gpt-6-astra`를 선택했으며 모델·추론 설정을 별도로 지정하지 않았다. 같은 semantic session에서 실제 대화 여섯 쌍을 차례로 재생하고, 반복 설명과 첫 실행 대상 선택이라는 합성 입력 두 쌍을 추가했다. 마지막에는 대화 이력이 없는 새 모델 세션에 일반 Recover packet과 선택할 수 있는 Workspace 문서만 주었다.

자료 역할·정정 영향·과다 기록·재진입의 [판정 기준](receipts/maintain-eval/2026-09-11-material-classification/rubric.md)은 실행 전에 고정했다. correction-scope는 기존 Maintainer의 능력을 채점하는 데 적용했으며 모델 prompt에 새 지침으로 넣지 않았다. “records폴더에”라는 원래 대화의 후속 힌트도 시험 입력에서 제외했다. 이전 Maintainer의 전체 대화 기억을 재현한 것은 아니며, 해당 시점의 현재 문서에서 새로 시작했다.

## 실제로 확인된 동작

추가 조사에서 다섯 Ticket 초안과 현재 후보·Spec·state를 갱신했다. 추천 순서와 사용자 확정, 정적 코드 관찰과 실행 검증을 구별했고, 저장 용량의 부분 실패 보존 같은 중요한 차이를 유지했다. 단순 설명인 두 실제 입력과 명시적인 반복 설명 대조 입력에는 모두 `no_change`를 반환했고 실제 파일 변경도 없었다.

사용자 정정은 작업의 기준과 다음 행동을 바꿨다. Spec에는 다음 관계를 반영했다.

> 이름·조건식·기본값·값 변환·타입·작은 함수·책임 분리는 코드를 살펴보는 개선 관점이다. 경비 합계 표시 같은 Ticket은 그 관점들을 적용할 실제 작업 범위다.

오해로 생겼던 “전체 후보를 Ticket에 모두 배치한 뒤 실행 순서를 정한다”는 계획을 state의 필수 선행 조건에서 해제했다. 기존 다섯 범위와 후속 후보, 동작 보존, 필요한 부분만 개선한다는 기준은 유지했다. [정정 전후 실제 diff](receipts/maintain-eval/2026-09-11-material-classification/run01/04-correction/changes.diff)에서 확인할 수 있다.

진행 방식 채택은 Spec과 state에 반영했다. 이어 합성 입력에서 사용자가 경비 합계 표시를 첫 대상으로 선택하자 해당 Ticket과 state를 변경 전 검사 준비 단계로 갱신했다. 제품 코드 수정·테스트 실행·검사 통과를 만들어 내지 않았다. 이 첫 대상 선택은 시험용 입력이며 실제 Noline 사용자의 새 지시가 아니다.

| 입력 장면 | 모델 판단과 실제 반영 | 판정 |
| --- | --- | --- |
| 추가 조사·다섯 초안 | current 문서 10개 제안. 원안 Guard 실패, 링크 보조 뒤 반영 | 내용 보존 확인, 집행 실패·자료 분리 부족 |
| Ticket 경계 설명 | no_change, 파일 변경 없음 | 불필요한 기록 억제 |
| 전체 후보 질문 오해 | state에 Main의 선행 계획 반영 | 이후 정정의 영향 대상 확보 |
| 사용자 정정 | Spec·state 갱신, 잘못된 선행 조건 해제 | 행동 교정 확인, 철회 경위는 current에 잔류 |
| 전체 분석 범위 설명 | no_change, 파일 변경 없음 | 불필요한 기록 억제 |
| 진행 방식 채택·기록 요청 | Spec·state 갱신 | 합의 보존, 과정 기록의 별도 귀속 부족 |
| 같은 기준 재설명 — 합성 | no_change, 파일 변경 없음 | 대조 장면 통과 |
| 첫 대상 선택 — 합성 | Ticket·state 갱신 | 준비·실행 구별, memory 색인에 오래된 상태 잔류 |

전체 decision과 반영 경로는 [실행 요약](receipts/maintain-eval/2026-09-11-material-classification/run01/summary.json)에 있다.

## 자료 구분에서 부족했던 부분

**조사 상세와 운영 경위를 current에 누적했다.** 새 조사 내용은 `current/memory/analysis-items.md`에 붙였고, state에는 조사 당시 Git 상태, Evidence 수집 문제, 수동 전달·사후 보존 경위가 남았다. 후보 문서는 UTF-8 기준 8,783에서 15,366 bytes로, state는 7,016에서 12,303 bytes로 커졌다. 크기 자체가 실패 기준은 아니다. 현재 후보의 보존 조건은 재진입에 유효하지만, 조사 당시의 관찰과 과거 운영 경위까지 함께 남겼다는 내용이 문제다. 현재 Recover는 memory 바로 아래 Markdown을 모두 읽으므로 이 상세도 매번 기본 입력이 된다.

**정정의 효과를 반영한 뒤에도 철회 경위를 현재 문서에서 계속 설명했다.** Spec의 “Main의 앞선 '한 가지 개선 목적'이라는 설명을 단일 관점 제한으로 적용하지 않는다”, state의 앞선 오해와 turn별 설명은 단계 전환 뒤에도 남았다. 잘못된 조건을 현재 지시로 유지한 실패는 아니다. correction-scope 관점에서는 유효한 기준을 현재 문서에 남기고 철회된 전제의 경위를 필요한 과정 기록으로 분리하는 처리까지 부족했다.

**채택 근거의 보존 경로가 임시 입력과 current에 의존했다.** 합의 핵심과 일부 사용자 원문은 Spec·state에서 복구된다. 다만 “합의 기록” 링크는 시험 fixture의 `eval-inputs/`를 가리켰다. 원래 장면에서는 `/private/tmp/`의 전달용 파일에 해당한다. Maintainer는 조사·정정·채택의 보존 자료를 Workspace records에 새로 만들지 않았다. 이번 시험에서 의미가 이미 사라졌다는 뜻은 아니다. state가 다음 상태로 대체될 때도 과정을 안정적으로 재검토할 Workspace 소유 경로를 확보하지 못했다는 판단이다. 기록 파일 수가 아니라 자료의 역할과 생명주기를 평가했다.

**단계 전환의 영향 범위를 일부 놓쳤다.** 마지막 Ticket과 state에는 첫 대상 확정이 반영됐지만, Maintainer가 첫 단계에 작성한 memory 색인에는 다음 문장이 그대로 남았다.

> 1차 Ticket 초안 다섯 개가 있으며 첫 구현 대상과 실행 순서는 사용자 확정 사항이 아니다.

최신 [state](receipts/maintain-eval/2026-09-11-material-classification/run01/after/current/state/index.md)와 [memory 색인](receipts/maintain-eval/2026-09-11-material-classification/run01/after/current/memory/index.md)이 충돌한다. 모든 Ticket 변경마다 색인을 갱신해야 한다는 요구가 아니다. 색인에 상태를 복제했다면 그 내용도 현재 판단과 일치시키거나 중복 상태를 걷어내야 한다. 이는 정정·단계 변화의 영향을 실제 의존 문서까지 확인하는 데 남은 결함이다.

Workspace의 현재 계약도 분석·결정·선택 근거의 누적을 records에, 현재 기준·실행·전체 상황을 Spec·Ticket·state에 배치한다. 정확한 기준은 [Workspace 구성](../../../../reference-project/context/work/workspaces/README.md)과 [Spec·Ticket 유지 기준](../../../../reference-project/context/work/workspaces/SPEC-AND-TICKETS.md)에 있다. 이번 결과는 그 역할 구분을 충분히 구현하지 못했다.

## 원대화 없이 다시 들어가 본 결과

새 세션은 세 질문 모두에서 필요한 의미를 복구했다. 경비 합계가 첫 대상이고 변경 전 검사를 준비해야 한다는 것, Ticket은 여러 개선 관점을 적용하는 코드 범위라는 것, 현재 조사 보고와 실제 실행 검증을 구별해야 한다는 것을 답했다. 한 Ticket 완료로 전체 Work가 완료되지 않는다는 기준도 유지했다.

색인의 오래된 미확정 문구를 스스로 발견하고 최신 state와 Ticket 본문을 기준으로 판단했다. 이는 문서의 충돌이 없어졌다는 뜻이 아니라 **후속 모델이 충돌을 해석해서 복구한 성공**이다. 원대화나 임시 전달 원문을 읽지 않았으며 packet 외 추가 읽기는 첫 Ticket 본문과 기존 Workspace 구성 기록 두 파일이었다.

[새 세션 답변](receipts/maintain-eval/2026-09-11-material-classification/reentry01/answers.json)의 근거 발췌 17개를 실제 파일과 대조했다. 15개는 그대로 일치했고 두 개는 따옴표·공백을 정규화하면 일치했다. [읽기 명령과 발췌 대조](receipts/maintain-eval/2026-09-11-material-classification/reentry01/audit.json)에 남겼다. 이번의 한 번의 재진입은 성공했지만, current가 계속 바뀌는 장기 보존이나 다른 모델의 복구 신뢰도까지 증명하지는 않는다.

## 집행 실패와 확인 범위

첫 조사 decision의 state 링크에서 `../` 한 단계가 부족했다. Guard는 존재하지 않는 경로를 감지해 전체 변경을 거부했고, 반영 전후 파일 hash는 모두 같았다. [원래 실패](receipts/maintain-eval/2026-09-11-material-classification/run01/failure.json)와 [수정한 문자열 한 곳](receipts/maintain-eval/2026-09-11-material-classification/run01/01-research-assisted-link-repair/assistance.json)을 별도로 보존했다. 의미·Owner 선택을 수정하거나 모델에 답안을 추가하지 않고 같은 session을 이어갔다. 경로를 옮긴 fixture에서 나온 오류이므로 원래 Noline에서도 같은 오류가 발생한다고 단정하지 않는다. 자동 오류 복구는 시험하지 않았다.

최종 변경은 해당 임시 Workspace의 current Markdown 11개에 한정됐다. 기존 source·제품 코드·기계 status·records는 그대로였다. Grounding과 여덟 판단 turn, 새 재진입 turn의 실제 runtime metadata 모두 read-only였으며 모델이 Guard 전 직접 쓴 파일은 없었다. [파일·decision·runtime 대조](receipts/maintain-eval/2026-09-11-material-classification/audit.json)가 근거다. 대조 스크립트의 최초 비교는 `.git`과 symlink 포함 기준이 실행기와 달라 실패했으나, 실행기와 같은 파일 범위로 맞춘 뒤 일치했다. 이는 모델 변경 사건이 아니다.

원본 Noline·Reference·skill·hook·자동 host 연결은 변경하지 않았다. 이 결과는 기존 의미 판단과 Guard 경로에 대한 단일 재생 시험이며 실제 host의 시작·종료·재시작 전체를 검증한 것이 아니다.

다음 보완에서는 조사·합의가 현재 기준과 과정 근거 중 각각 어떤 역할을 하는지 기존 Owner 선택에 반영하고, 임시 원문을 계속 보존할 필요가 있으면 Workspace가 소유하는 경로를 확보해야 한다. 정정과 단계 변화 뒤에는 그 전제를 복제한 현재 문서를 함께 확인해야 한다. 개선안은 같은 입력으로 다시 시험하고, 새 records 개수보다 현재 기준의 명료함·보존 근거·중복 상태 충돌·재진입 결과로 비교하는 것이 적절하다. 이번 요청에서는 평가까지만 수행했다.
