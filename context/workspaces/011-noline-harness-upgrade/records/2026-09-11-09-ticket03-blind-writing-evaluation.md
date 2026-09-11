# Ticket 03 원문을 준 Maintainer 독립 작성 시험

2026-09-11, `011-noline-harness-upgrade`.

Terra high로 실행되는 것은 확인했다. 그러나 원문과 새 작성 지침을 모두 제공한 첫 초안도 논의의 선택 이유·조건을 충분히 보존하지 못했다. 핵심 실행 방향은 남았지만, 현재 Noline의 Main 수정본보다 전반적으로 나아졌다고 판단하지 않는다. 이번에는 작성 결과를 보정하거나 지침을 다시 수정하지 않고 표본 그대로 보존했다.

## 어떤 조건으로 작성했나

사용자는 “저 티켓3 대화 세션 전문을 주고 기존 자료보여주지 말고”, 필요한 지시만으로 독립 작성한 품질과 Terra high 실행을 확인하라고 요청했다. 작성자는 이 평가 대화나 기존 작성본·Main 수정본·이전 비평을 받지 않았다.

입력은 원 Main session `01a08ff3-0e91-7921-afe4-69f0968638ef`의 원본 L9–254에서 사용자·Main의 가시 발화 23개를 선택했다. Ticket 확인 요청부터 기록 요청까지 commentary를 포함하며, 선택한 각 발화의 text는 원문과 일치한다. 이후 실제 문서 작성·비평·수정 대화는 제외했다. System/developer 지침, 도구 호출·결과, L133의 환경 메타데이터는 대화 발화에 포함하지 않았다. 따라서 이는 해당 논의의 발화 전문이지 session JSONL 전체 복사는 아니다. 코드 관찰은 당시 Main의 보고로 전달됐고 도구 원출력이나 현재 제품 파일을 작성자에게 추가로 주지 않았다.

현재 Reference의 `CodexMaintainSession.start()`와 같은 session의 `resume()`을 실제 호출했다. 모델·추론 수준과 출력 schema는 원래 adapter가 선택한 그대로 사용했다. Maintain·Workspace·DOCUMENT-WRITING·Spec/Ticket 계약 전문도 adapter의 기존 입력 경로로 제공했다. 별도 답안 목차·누락 목록·분량 제한·평가 예상 결론은 주지 않았다.

독립 작성을 위해 제목만 있는 Ticket과 records 색인을 임시 폴더에 만들었다. 시험용 bootstrap이며 실제 Noline Recover packet은 아니다. 후보 범위는 Ticket 03 본문, 테스트 전략 record, records 색인의 해당 항목으로 한정했다. 실제 Noline에 Guard apply·hook 연결·문서 반영은 하지 않았다.

실험에서만 `project_doc_max_bytes=0`, shell 비활성, web 비활성과 Git 검사 생략 옵션을 추가했다. 이는 주변 AGENTS와 파일을 추가 입력으로 읽지 않게 하는 통제이며 production 설정 변경은 아니다. 첫 실행의 cwd는 임시 폴더였지만 `resume` 로그의 cwd는 parent 저장소였다. 두 실행 모두 read-only였고 실제 도구 호출은 0건이었다. 입력과 실행 로그로 기존 작성본 미노출을 확인했으며, OS 수준의 파일 읽기 격리까지 입증한 시험은 아니다. 해당 CLI 설정의 의미는 [공식 설정 문서](https://learn.chatgpt.com/docs/config-file/config-reference#configtoml)에서 확인했다.

## 실제 실행과 산출물

실제 Maintainer session은 `01a09066-daf2-7c80-8a89-fdb608275d7a`다. 시작과 재개 로그의 `turn_context` 모두 `model=gpt-5.6-terra`, `effort=high`이며 collaboration 설정도 같은 값이다. 명령 인자만 확인한 결과가 아니다.

첫 grounding은 `grounded`, 작성 결과는 세 경로에 대한 `update`였다. 작성 지침 본문은 각 호출 입력에 정확히 한 번 포함됐고, 보존한 prompt가 실제 session의 user 입력에 들어간 것도 대조했다. 재작성 요청이나 실패 후 답안 교정은 하지 않았다.

- [Ticket 초안](receipts/maintain-writing-eval/2026-09-11-ticket03/preview/current/memory/tickets/03-storage-stats.md): 작성자가 반환한 전체 content, 28행.
- [논의 record 초안](receipts/maintain-writing-eval/2026-09-11-ticket03/preview/records/2026-09-11-02-storage-stats-test-strategy.md): 작성자가 반환한 전체 content, 33행.
- [기록 색인 초안](receipts/maintain-writing-eval/2026-09-11-ticket03/preview/records/README.md): 작성자가 반환한 해당 색인, 3행.
- [입력 전문과 최소 지시](receipts/maintain-writing-eval/2026-09-11-ticket03/inputs.json), [판본 snapshot](receipts/maintain-writing-eval/2026-09-11-ticket03/source-snapshot.json), [원래 decision](receipts/maintain-writing-eval/2026-09-11-ticket03/02-decision.json), [기계 대조 결과](receipts/maintain-writing-eval/2026-09-11-ticket03/checks.json).

Preview 파일은 decision의 content와 정확히 같다. 아래에서 발견한 오류도 수정하지 않았다. Noline의 비교 대상 세 파일은 실행 전후 SHA-256이 같았다. [보존 확인](receipts/maintain-writing-eval/2026-09-11-ticket03/target-preservation.json)

## 남긴 의미와 잃은 의미

부분 실패 계약, hook을 주 검사로 삼는 선택, client가 설정을 소유하는 경계, 자동 검사가 실제 native 동작을 입증하지 않는 한계는 대체로 정확하다. 특히 Ticket 23행의 “이전 결과에 누적하지 않고 다시 계산”은 원본 L127의 refresh 사례를 보존했다. 현재 Noline Ticket의 단순한 “값 재계산”보다 이 부분은 구체적이다. 미착수와 테스트·실기기 미실행도 구별했다.

반면 논의 기록의 가장 중요한 부분은 다시 압축 과정에서 사라졌다.

**선택 결과가 선택 이유를 대신했다.** Record 25행은 `jest.config.cjs`, `tsconfig.test.json`, `tests/` 경로를 나열한다. 원본 L174의 package.json 내부 설정과 별도 파일 비교, source 옆 배치와 별도 tests 배치의 이익·비용은 거의 없다. Ticket 13행에 제품 TypeScript·Router 분리 이유는 있지만, 구현과 테스트의 물리적 거리 및 source 구조를 두 번 관리하는 비용은 어느 문서에도 남지 않았다. 현재 Noline Main 수정본은 이보다 설정 선택 이유를 더 설명한다.

**조건을 구별하라는 새 기준도 충족하지 못했다.** 원본 L174는 테스트 실행과 타입 검사가 다름을 설명한 뒤 “앞으로 유지할 회귀 테스트로 본다면 `tsconfig.test.json`까지 만드는 편을 권합니다”라고 했다. 초안은 이 목적과 비용을 지우고 초기 파일 구성으로만 적었다. 같은 record 25행에서 변환 설정, setup, 전역 mock, fixtures, coverage, 공용 test-config를 “실제 필요가 확인될 때만 추가”로 묶었다. 변환 오류 대응, 여러 테스트의 준비 반복, 서로 다른 package에서 실제 공통 설정이 생기는 조건이 구별되지 않는다. 단순히 기본안 채택을 틀렸다고 판정하는 것이 아니라, 채택 이유와 재검토 조건을 복원할 수 없다는 문제다.

**기술 선택지의 서로 다른 장점·비용도 합쳐졌다.** Record 19행은 Vitest와 Node runner를 함께 제외하고, Maestro와 Detox도 함께 설명한다. 원본 L143에서 구별한 Vitest의 속도·TypeScript 경험, Node의 외부 runner 의존성 감소, Maestro의 실패 주입 한계, Detox의 native 빌드·실행 환경 구성 비용은 남지 않았다. 원본 L202의 `@repo/*` exports 유지, schema 실패 placeholder 직접 관찰과 recursive 명령 미실행 구분도 문서에서 빠졌다.

**판정 가능한 사례와 개선 효과 기준이 부족하다.** 원본 L127의 `1,024 → 1 KB`, `1,536 → 1.5 KB`, `1.0 KB`로 바꾸지 않는 사례가 초안에서는 “단위·소수 표시 규칙”으로 줄었다. Ticket은 보존할 동작을 쓰지만, 이번 목표인 성공·실패 stats 조립의 변경 지점 감소와 실패 정책을 가까이에서 읽을 수 있는지를 완료 판단에 직접 적지 않았다. 원본 L174의 가독성 설명은 record 17행에 일부 남아 있으나, 실행 문서가 맡아야 할 개선 판정까지 대체하지 못한다.

**결정 근거에 다시 접근하기 어렵다.** Record 31행은 날짜와 “사용자는 … 수용한 뒤 기록을 요청했다”는 요약만 남겼다. 원본 L181의 “전반적으로 다 좋아”, L209의 “그래 좋아 … 결정사항들 논의 기록”, L254의 기록 요청 중 어떤 발화가 무엇을 지지하는지 확인할 최소 발췌·session 식별자·원문 위치가 없다. 이 정보는 작성 입력에는 있었다.

**연결 오류가 있다.** Ticket 15행의 record 링크는 `../../../../records/...`다. 해당 위치에서 Workspace records까지는 `../../../records/...`가 맞으므로 한 단계 더 올라간다. 제공한 두 기존 Owner의 SHA-256, 허용 세 경로, EOF newline과 trailing whitespace는 맞았지만 로컬 링크 두 개 중 한 개는 잘못됐다. 이는 읽기 경로 오류를 직접 확인한 결과이며 Guard 전체를 실제 실행한 결과는 아니다.

## 이번 시험으로 판단할 수 있는 것

이 표본에서는 모델·effort가 잘못 선택됐거나 작성 지침이 입력에서 누락된 것이 아니다. 원문에 있었고 실제 제공된 선택 이유·조건이 결과에 남지 않았으므로, 이번 부족함을 과거의 요약 입력 누락만으로 설명할 수도 없다. 문장은 짧고 읽기 편하지만, 논의를 이어받는 문서로서는 내용 충분성이 부족하다.

다만 원문 공급, 새 지침, 모델 설정을 함께 바꾼 단일 사례다. 각 변경의 독립 효과나 Terra high의 일반적인 한계를 분리하지 못한다. 새 지침을 설계한 바로 그 사례로 시험했으므로 다른 주제에 대한 일반화도 확인하지 않았다. 실제 문서 갱신 시 유효한 기존 내용을 보존하는 능력, 여러 turn 누적 관리, Guard apply와 Noline host 동작도 이번 평가 밖이다.

다음 보완 방향은 항목명을 더 많이 적게 하는 것보다, 초안이 판단에 필요한 이유·비용·조건을 실제로 담았는지 작성자가 원문과 대조하는 방식에 있다. 이것은 이번 결과에 대한 Main의 해석이며 아직 새 지침 변경이나 재시험을 승인·수행한 것은 아니다.
