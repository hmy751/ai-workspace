# 실제 Maintainer 시험 입력과 실행 증거

현재 상태: **기존 계약의 여덟 입력·재진입 시험과, 수정 계약의 전체 재시험·잔여 결함 좁은 재시험·fresh reentry를 완료했다.** 첫 실행만 상대 링크 한 곳의 Main 보조가 들어갔고 수정 뒤 `run02`·`run03`은 Guard 오류 없이 끝났다. 기존 판정은 [평가 기록](../../../2026-09-11-02-maintainer-material-classification-evaluation.md), 보완과 재검증은 [수정 기록](../../../2026-09-11-03-maintainer-material-classification-correction.md)이 소유한다.

## 실행 내용과 모델에 제공한 자료

설치된 Codex CLI의 기존 `CodexMaintainSession` 경로로 OpenAI의 `gpt-6-astra`를 호출했다. 명시적인 model·effort override 없이 기존 bridge의 기본값을 사용했다. 결과 문서의 재진입도 새로운 모델 세션에서 확인했다.

처음 전달하는 [준비된 grounding prompt](prepared-grounding-prompt.txt)는 88,473 bytes이며 다음 내용이 들어 있다.

- Maintain와 Spec/Ticket 계약 본문
- Noline 002의 memory 색인, Spec 다섯 문서, 기존 후보 목록, Project context 선택 문서, Ticket 색인
- 당시 state, 제품 검증의 기계 status, output 색인과 Workspace·Recover metadata
- 선택된 Project README, 제품 공통 맥락, 현재 아키텍처

이 내용에는 비공개 제품 구조, 작업 판단, 사용자 발췌, 로컬 경로와 과거 운영 경위가 포함돼 있다. [실제 recovery packet](prepared-bootstrap.json)에서 전부 확인할 수 있다.

이후 [cases.json](cases.json)의 실제 user/Main 응답 여섯 쌍과 합성 대조 입력 두 쌍을 같은 semantic session에 차례대로 전달한다. 실제 구간은 추가 조사, Ticket 경계 설명, 오해, 사용자 정정, 전체 분석 범위 설명, 진행 방식 채택이다. “records폴더에”라는 후속 정답 힌트는 포함하지 않았다.

필요한 로컬 읽기 대상으로 당시 [조사 원문](research-original.md), [합의 전달 원문](agreement-original.md)과 임시 Workspace의 관련 Context Owner를 제공한다. 여기에도 코드 경로·관찰·미검증 범위가 들어 있다. 모델이 문서 수정안을 만들면 실제 Guard가 임시 복사본에 반영한다. 생성된 문서와 재진입 packet도 후속 평가 모델의 입력이 된다.

## 준비 근거

- Target commit `a612ba4c49b92b1193e75e1d56bdefcdcd86bbda`의 local Git archive에서 분리된 임시 Project를 만들었다.
- Commit 뒤의 실제 state decision을 Guard로 적용했고, 다음 조사 당시 state preimage의 SHA-256과 일치했다.
- 사라진 조사 원문은 Main의 과거 apply_patch 입력에서 복원했다. 원문 hash는 당시 Maintainer가 읽은 hash와 일치한다. 합의 전달 원문도 같은 방식으로 당시 hash를 대조했다.
- 당시 Maintainer의 이전 warm 대화를 모두 이어받지는 않는다. 해당 시점의 current로 새로 grounding하고 이후 여섯 입력을 순차 재생한다. 경로는 격리된 임시 Project와 입력 파일로 치환했다.
- [rubric.md](rubric.md)에 자료 역할·내용 보존·정정 영향·과다 기록·재진입을 실행 전에 고정했다. correction-scope는 첫 실행의 prompt에 주입하지 않고 채점 관점으로 사용한다.

## 실행과 증거

[prepare.py](prepare.py)는 fixture·원문·입력을 준비하고 [run.py](run.py)는 실제 모델 호출·각 decision·Guard 결과·파일 diff를 보존한다. [setup.json](setup.json)은 경로와 역사 기준, [fixture-manifest.json](fixture-manifest.json)은 초기 파일 hash를 소유한다. baseline.tar는 로컬 복원용 전체 Git archive이며 모델 prompt 자체가 아니다.

준비 중 결과 필드명을 `status`로 잘못 읽어 한 번 중단했다. 실제 Guard의 `context_status`로 수정한 뒤 새로운 fixture 경로에서 재준비했다. 이 준비 오류는 Maintainer의 의미 판단 결과가 아니다.

첫 실행을 위한 escalation은 프로세스 생성 전에 자동 승인 심사에서 거절됐다. 당시 거절 사유는 다음과 같다.

> 격리된 fixture의 비공개 프로젝트·문서 내용을 실제 Codex 모델로 전송할 수 있지만, 사용자가 해당 payload를 외부 모델 destination에 보내는 것을 구체적으로 승인하지 않았습니다.

전송 자료와 이유를 설명한 뒤 사용자가 “해봐”라고 재승인했다. 같은 실행기로 재개했고 `run01/`의 실제 semantic thread `01a08e25-2d26-7f32-bfd2-544667ef4c79`가 grounding과 여덟 판단을 마쳤다. 실행 환경은 Codex CLI `0.153.4`, OpenAI provider, `gpt-6-astra`다. Grounding과 여덟 판단의 실제 turn_context 모두 read-only였다.

첫 조사 decision은 상대 링크에서 `../` 한 단계가 부족해 Guard가 거부했다. 실패 시 파일 변경은 없었다. [continue_after_link_failure.py](continue_after_link_failure.py)가 원안과 [링크 한 곳의 수정](run01/01-research-assisted-link-repair/assistance.json)을 구분해 보존하고 같은 session을 이어갔다. 의미·Owner 선택에 힌트를 추가하지 않았다. 자동 실패 복구를 증명하지는 않는다.

- [run01/summary.json](run01/summary.json): 최초 실패·수동 보조·여덟 결과와 변경 경로.
- `run01/<phase>/`: 실제 prompt·명령·모델 출력·decision·실행 시간. 반영 성공 단계에는 Guard 결과·diff·전후 hash·current/records 사본도 있다.
- [run01/before/](run01/before/)와 [run01/after/](run01/after/): Workspace 전후 사본. 원래 상대 링크를 보존한 비교용 사본이므로 독립 실행 Project는 아니다.
- [reentry01/answers.json](reentry01/answers.json): 원대화 없는 새 세션의 세 질문 답변.
- [reentry01/audit.json](reentry01/audit.json): 실제 읽기 명령·모델 실행 설정·근거 발췌 17개 대조.
- [audit.json](audit.json): decision과 실제 변경·preimage·최종 파일·runtime 대조. [audit.py](audit.py)로 다시 확인할 수 있다.

새 reader `01a08e37-2594-7141-8628-056cb380608c`도 read-only로 실행됐다. 일반 packet 외에는 첫 Ticket과 기존 Workspace 구성 기록만 읽었고, 색인의 오래된 상태를 발견하며 세 질문을 복구했다. 전체 변경은 임시 Workspace의 current Markdown 11개이며 source·제품·기계 status·기존 records는 같았다. 첫 링크 보조와 평가용 두 합성 입력을 포함한 단일 실행이라는 한계를 유지한다.

## 수정 계약 재시험

[`prepare_retest.py`](prepare_retest.py)는 같은 역사 baseline에 수정한 Reference Maintain 파일만 덮어 `run02-project`를 만들었다. [`run_retest.py`](run_retest.py)는 기존과 같은 여덟 입력을 새 semantic session `01a08e4d-b203-79b2-8656-8134d2a92e7a`에서 처리했다. 모든 decision은 수동 보조 없이 Guard 반영에 성공했다. 조사·정정 과정은 Workspace records로 분리됐고, 현재 색인의 진행 상태 중복은 제거됐다. [`reentry02/answers.json`](reentry02/answers.json)의 새 reader도 records를 근거로 현재 작업을 복구했다.

`run02`에서 채택 발화 원문이 Spec에 남고 state가 과거 운영 경위를 계속 보유한 잔여 결함을 확인해 계약을 한 번 더 좁혔다. [`prepare_targeted_retest.py`](prepare_targeted_retest.py)는 `run02`의 정정 완료 시점 fixture를 만들고, [`run_targeted_retest.py`](run_targeted_retest.py)는 채택·재설명·첫 대상 선택만 새 session `01a08e63-c125-74d2-8f30-d02b14b6bf58`에서 재생했다. 채택 근거는 새 record로 분리됐고 current에는 정규화한 기준만 남았다. state는 8,336에서 4,254 UTF-8 bytes로 줄었으며 재설명은 `no_change`, 단계 변화는 Ticket·state에 반영됐다.

[`audit-v3.json`](audit-v3.json)은 `run03`의 decision·실제 변경·hash·read-only runtime과 exact 발화의 current 제거·records 보존을 대조한다. [`reentry03/answers.json`](reentry03/answers.json)은 새 reader `01a08e69-28d2-7f81-b265-dadb09ca4a2c`의 세 질문 복구 결과다. `reentry02-sandbox-failure/`는 read-only 모델 실행 전 Codex 로컬 state DB 접근이 막힌 실패를 보존한 폴더이며, 같은 명령을 허용된 실행으로 다시 수행한 성공본은 `reentry02/`다.

대조 스크립트의 첫 실행은 `.git`과 symlink의 포함 기준이 실행기와 달라 실패했다. 실행기의 scan과 같은 기준으로 수정한 뒤 전부 일치했다. Maintainer의 파일 변경 실패와는 별개의 평가 도구 오류다.
