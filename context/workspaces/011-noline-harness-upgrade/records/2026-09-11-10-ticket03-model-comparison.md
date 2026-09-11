# Ticket 03 독립 작성: Terra xhigh와 Sol medium 비교

2026-09-11, `011-noline-harness-upgrade`.

Sol medium이 Ticket의 표시 사례·개선 완료 기준과 문서 링크에서는 더 정확했다. 그러나 두 후보 모두 논의 record에서 선택 이유·비용·조건과 최소 원문 근거를 충분히 남기지 못했다. Sol은 이번 시험에서 약 1.83배의 추정 비용이 들었으며, 그 차이로 사용자가 지적한 핵심 기록 문제가 해결되지는 않았다. 두 후보 중 어느 것도 충분하다고 판정하거나 기본 모델을 변경하지 않았다.

## 같은 입력으로 두 후보를 실행

사용자는 Terra xhigh와 Sol medium을 제안한 직후 “그럼 그 두개 후보 병렬로 테스트 해보자”라고 요청했다. [최초 Terra high 시험](2026-09-11-09-ticket03-blind-writing-evaluation.md)의 논의 발화 23개, 빈 문서 fixture, 최소 작성 요청과 계약 본문을 그대로 사용했다. 두 후보의 시작·재개 prompt는 최초 시험의 해당 prompt와 바이트 단위로 같았다. 기존 작성본, 이전 초안·비평과 이번 평가 기준은 작성자에게 제공하지 않았다.

실제 `CodexMaintainSession.start/resume`을 후보마다 새 session으로 호출했다. 실험 wrapper가 실행 명령의 모델·추론 값만 후보에 맞게 바꿨고, 실제 role 파일은 Terra high 그대로 보존했다. 첫 호출들은 약 0.001초 차이로 시작됐으며 후속 작성 구간도 겹쳤다. 후보별 첫 초안만 회수하고 교정·재실행하지 않았다.

시작·재개 네 실행의 실제 `turn_context`에서 요청한 모델·effort와 read-only를 확인했다. 각 후보의 도구 호출은 0건이었다. 자동 AGENTS 읽기와 shell/web을 비활성화하는 기존 시험 통제를 유지했다. 시작 cwd는 후보별 임시 폴더, 재개 cwd는 parent 저장소였으며 OS 수준 파일 읽기 격리를 입증한 시험은 아니다. 실제 Recover packet이나 Noline host 연결·Guard apply도 시험하지 않았다.

- [고정 입력 원본](receipts/maintain-writing-eval/2026-09-11-ticket03/inputs.json): 선택한 논의의 사용자·Main 발화 전문과 최소 요청. 도구 원출력과 이후 실제 작성·비평은 제외했다.
- [실행 manifest](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/manifest.json), [실제 설정·prompt·usage 대조](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/checks.json), [작성자에게 주지 않은 평가 기준](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/review-criteria.json).
- Terra xhigh: [Ticket](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/terra-xhigh/preview/current/memory/tickets/03-storage-stats.md), [record](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/terra-xhigh/preview/records/2026-09-11-02-storage-stats-test-strategy.md), [decision](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/terra-xhigh/02-decision.json).
- Sol medium: [Ticket](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/sol-medium/preview/current/memory/tickets/03-storage-stats.md), [record](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/sol-medium/preview/records/2026-09-11-02-storage-stats-test-strategy.md), [decision](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/sol-medium/02-decision.json).

## 문서 품질에서 실제로 달라진 부분

두 후보 모두 DB 중간 실패·getPacks 실패·개별 팩 실패를 구별하고 refresh 비누적, client 소유, native 검증의 한계를 보존했다. 제품 구현이나 테스트 실행을 완료했다고 쓰지는 않았다. 이 의미는 원본 L79·127·143과 Main이 다시 읽은 현재 hook의 분기·화면 소비에 부합한다.

Sol Ticket 17행은 `1,024 bytes → 1 KB`, `1,536 bytes → 1.5 KB`의 입력·결과를 남겼고, 46행은 동작 보존과 별도로 조립 중복 감소·실패 흐름의 가독성을 완료 판단에 포함했다. 원본 L127·174의 중요한 의미다. Terra는 단위 입력값과 일반 표시 규칙은 남겼지만 결과 사례는 덜 구체적이고, 별도 개선 효과의 완료 기준이 약하다.

Sol record 19행은 순수 함수 검사가 놓치는 hook lifecycle·상태 반영·refresh·import 연결을 설명한다. 43행은 `@repo/*`를 source로 강제 mapping하지 않는 package export 경계를 보존한다. 이 점도 원본 L143·202를 Terra보다 충실히 반영했다.

하지만 사용자가 문제 삼은 설정 논의의 충분성은 두 후보 모두 부족하다.

- **Jest 설정 배치:** package.json 안에 둘 때 파일을 줄이는 이점과 별도 설정 파일로 책임을 나누는 이유가 원본 L174에 있지만, 둘 다 설정 파일을 채택한 결과 중심이다.
- **테스트 위치의 비용:** Terra record 52행은 제품 타입·Router 분리 이유를 설명하지만 구현과 테스트가 떨어지고 source 구조를 한 번 더 관리하는 비용은 빠졌다. Sol은 `tests/` 경로 중심이며 그 선택의 비교 근거가 더 약하다.
- **테스트 전용 타입 검사:** 원본 L174는 “앞으로 유지할 회귀 테스트로 본다면 `tsconfig.test.json`까지 만드는 편을 권합니다”라고 했고, Jest 실행과 타입 검사의 차이 및 추가 설정·스크립트 비용을 설명했다. 두 후보 모두 그 관계보다 초기 파일 구성으로 정리했다.
- **서로 다른 도입 조건:** Terra record 68행은 오류 발생 전에는 transform·setup·공용 mock을 추가하지 않는다고 묶는다. Sol record 40행은 “설정 오류가 실제로 나타나기 전에는” setup·공용 mock·fixture·coverage 등까지 추가하지 않는다고 적었다. 원문의 변환 오류 대응, 준비 코드의 반복, 여러 소비자의 공통 설정은 같은 조건이 아니다. Sol은 바로 앞 39행에서 mock 공유 단계를 잘 구별했지만 다음 행의 포괄 조건과 맞지 않는다.
- **기술 대안과 원문 근거:** 둘 다 Vitest/Node와 Maestro/Detox의 서로 다른 장점·비용을 한 묶음으로 압축했고, 사용자의 채택·기록 요청을 요약만 했다. 최소 발화 발췌와 정확한 session·원문 위치는 두 record 모두 없다. schema placeholder script의 직접 관찰과 recursive 실행 미실행 구분도 충분히 남기지 못했다.

두 후보는 Ticket과 record의 일부 설정 목록·검사 범위를 반복하면서, 그 공간에 있어야 할 선택 이유는 빠뜨렸다. 문서 길이가 늘거나 하위 제목이 많아진 것만으로 이 문제가 해결되지는 않았다.

링크는 차이가 명확하다. Terra Ticket 37행은 앞선 high 표본과 같은 `../../../../records/...` 오류를 반복했다. Sol Ticket 30행의 `../../../records/...`는 맞았다. 두 후보 모두 허용한 세 경로와 preimage, EOF·줄 끝 공백 검사는 맞았으며 Preview는 decision content와 동일하다. 링크 오류도 보정하지 않았고 Guard 전체 실행을 주장하지 않는다.

## 시간과 비용

아래 시간은 각 후보의 최초 grounding부터 작성 응답 완료까지이며, 토큰은 두 호출의 합계다. 출력 토큰에는 추론 토큰이 포함돼 따로 더하지 않았다. 네 호출의 캐시 입력·캐시 쓰기는 모두 0이었다. 병렬 실행 중 측정한 단일 표본이므로 반복 실행 속도 차이로 일반화하지 않는다.

| 후보 | 전체 시간 | 입력 토큰 | 출력 토큰 | 그중 추론 토큰 | 추정 크레딧 |
|---|---:|---:|---:|---:|---:|
| Terra xhigh | 105.7초 | 95,330 | 5,424 | 2,106 | 6.39 |
| Sol medium | 117.5초 | 95,446 | 4,353 | 478 | 11.72 |

문서 작성 호출만 보면 Terra는 97.8초·4.75크레딧, Sol은 105.0초·8.38크레딧이다. 같은 사용자 prompt라도 모델별 실행 문맥과 앞선 grounding 응답이 달라 입력 토큰 수까지 정확히 같지는 않다. 추론 토큰 수는 품질 점수가 아니며 모델 간 직접 역량 비교로 해석하지 않는다.

추정에는 2026-09-11 확인한 [Codex 표준 단가](https://learn.chatgpt.com/docs/pricing#token-rates)를 사용했다. 100만 토큰당 Terra 입력/캐시 입력/출력은 50/5/300, Sol은 100/10/500크레딧이다. [단가와 계산식](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/pricing-basis.json)에 의존 내용을 보존했다. 실제 계정 청구·플랜 차감·별도 계약이나 fast mode 청구를 확인한 값은 아니다.

## 다음 판단

Sol medium은 더 정확한 부분이 있었지만 이번 문서 전체를 그대로 채택할 수준은 아니다. 약 1.83배 비용을 지불한 결과에서도 설정 tradeoff와 결정 근거 문제가 공통으로 남았다. 따라서 앞선 Sol medium 우선 시험 제안을 기본 설정 상향으로 이어갈 근거는 아직 부족하다.

이번 결과는 모델 상향만으로 문제가 해결될 것이라는 기대를 약화한다. 다음에는 원문에서 비교한 이유·비용·조건과 초안 사이의 실제 누락을 어떻게 확인하게 할지, 현재 작성 요청과 계약 전달이 그 판단을 충분히 유도하는지 검토할 근거가 생겼다. 이를 당장 규칙 추가나 5.5·더 높은 effort의 자동 재시험으로 확장하지 않는다. 모델별 한 표본이고 지침을 만든 바로 그 사례이므로 일반 모델 우열이나 다른 문서 유형의 효과는 미확인이다.

Noline 비교 대상 세 파일과 Reference의 runtime·역할 설정·계약 여덟 파일은 시험 전후 동일하다. [실행 완료와 보존 확인](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/completion.json)에 실제 범위를 남겼다. 기본 Maintainer는 Terra high이며 이번 평가 기록은 미커밋이다.
