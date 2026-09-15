# 범위 정정과 runtime 근거

날짜: `2026-09-15`

상태: **문제·대상 재기준화 완료 / 구현 미착수**

## 이 기록의 역할

백그라운드 token 소비를 단순히 기능 호출 횟수나 모델 등급 문제로 다루던 초기 관점에서 벗어나, Maintain의 목적에 필요한 의미 연속성과 전체 transcript 누적을 분리한다. 이 정정이 구현 대상, 설계 우선순위와 검증 기준을 어떻게 바꾸는지 고정한다.

## 사용자 원문과 바뀐 판단

이번 범위를 바꾼 직접 발화는 다음과 같다.

> “그럼 결국 동작보다는 컨텍스트 누적이 문제라는건가?”

> “근데 일단 그냥 계속 기록을 한다는건 이전 내용을 을아야 하니까 아마 그냥 누적처리를 햇던것 같아”

> “여기서 궁금한거 해당 스레드 에이전트는 우리처럼 기본 compact이런건 못하나?”

> “난 이 이슈를 /Users/hammyeong-yeon/Desktop/ai-workspace/context/workspaces 여기 프로젝트에서 하는게 맞아보여 그래야 또 개선하고 둘 다 적용될거고 그래서 너가 여기에 하나 워크스페이스를 추가해서 만들어놔주면 좋겠어 활성화 까진 아니고”

여기서 `둘 다`는 현재 대화와 기존 이식 관계에 따라 **ai-workspace의 Reference Maintain과 Noline의 설치된 Maintain**으로 해석한다. evidence collector는 최초 사용량 비교 근거지만 같은 코드 두 벌을 뜻하지 않는다.

이 정정으로 다음 전제를 폐기했다.

- 호출이 많다는 이유만으로 response-end 판단을 먼저 skip하면 된다는 전제
- 같은 agent가 이전 내용을 아는 것과 전체 transcript·도구 출력을 영구 보존하는 것이 같은 요구라는 전제
- automatic compact가 있으므로 별도 context lifecycle이 불필요하다는 전제
- Sol high를 medium으로 내리는 것이 구조 개선보다 먼저라는 전제
- Noline 설치본만 고치면 공통 개선이 된다는 전제

대신 의미 연속성은 보존해야 할 제품 목적이고, 비용 문제는 그 목적을 구현한 context lifecycle에서 찾는다. 공통 계약은 Reference가 소유하고 Noline에는 target 차이를 보존해 다시 적용한다.

## Maintain 실측

2026-09-14에 Noline Maintain runtime과 Codex session transcript를 대조했다. 최근 한 binding generation은 grounding 1회와 response-end 4회, 모두 5개의 Codex task turn을 처리했지만 내부 모델 처리는 11회였고 read-only shell 파일 읽기가 6회였다.

| 측정 항목 | 값 |
|---|---:|
| 총 input token | 1,382,751 |
| cached input token | 1,133,056 |
| uncached input token | 249,695 |
| output token | 16,181 |
| reasoning output token | 5,706 |
| 결과 | `no_change` 1, `updated` 2, `needs_user_decision` 1 |

첫 모델 처리는 cache 없는 68,709 input token이었다. 같은 response-end 안에서도 파일을 읽을 때마다 모델 처리가 추가됐고 마지막 두 처리는 각각 172,943과 179,594 input token을 보고했다. Reasoning 출력 5,706보다 반복 input이 훨씬 크므로, high reasoning을 첫 원인으로 확정할 근거는 없다.

역사상 정상 해결된 effect 100건은 `no_change` 40, `updated` 54, `needs_user_decision` 6이었다. 변경 또는 사용자 판단이 필요한 60건을 놓칠 수 있으므로 표면 키워드 hard skip은 replay 없이 채택하지 않는다.

### Automatic compact가 실제로 한 일

같은 semantic thread transcript에서 다음 순서를 확인했다.

1. compact 직전 모델 입력: 245,929 token, cached 216,064
2. compact 처리: input 246,234, cached 0, output 2,177
3. `compacted` event의 replacement history: 9개
4. 다음 모델 입력: 86,490, cached 12,032
5. 같은 root turn 전체 input: 667,478

따라서 이 host의 Maintainer도 기본 compact를 수행한다. 다만 context window가 약 95% 찬 뒤 큰 uncached pass를 한 번 더 사용해 history를 교체했다. 이는 capacity와 대화 지속성을 위한 fallback이며, compact에 도달하기 전의 누적 재입력과 compact 자체의 비용을 줄이는 장치는 아니다.

## Evidence collector 비교 근거

최초의 백그라운드 사용량 의심에는 Noline evidence collector도 포함됐다. `evidence-collector/store`의 event, record와 Codex receipt를 전수 집계한 값은 다음과 같다.

| 사건 종류 | 모델 처리 | input token | cached input | uncached input | output |
|---|---:|---:|---:|---:|---:|
| 2분 checkpoint | 135 | 2,035,592 | 182,528 | 1,853,064 | 101,001 |
| response end | 110 | 1,285,353 | 130,944 | 1,154,409 | 79,128 |
| interrupted | 12 | 127,793 | 11,904 | 115,889 | 8,004 |
| 합계 | 257 | 3,448,738 | 325,376 | 3,123,362 | 188,133 |

사건은 256개이고 모델 처리가 257회인 것은 한 사건의 재시도 때문이다. `spool/queued` 256개는 backlog가 아니라 원본 접수 보존본이며 같은 256개의 submitted receipt와 완료된 store job이 있었다. 256개 사건 중 250개가 `record`, 6개가 `index_only`였다.

Checkpoint의 독립 모델 처리는 전체 호출의 52.5%, uncached input의 59.3%다. 수집기는 raw capture와 model interpretation의 1:1 결합이 주된 비용이고, Maintain은 warm semantic identity와 literal transcript의 결합이 주된 비용이다. 두 장치는 같은 “백그라운드 token” 현상으로 보였지만 해결 책임은 같지 않다.

## 근거 위치와 상한

- Maintain semantic thread: `01a09e12-eaca-7033-bf81-09ad6fe03915`
- 당시 local Codex transcript: `/Users/hammyeong-yeon/.codex/sessions/2026/09/14/rollout-2026-09-14T13-00-35-01a09e12-eaca-7033-bf81-09ad6fe03915.jsonl`
- Evidence collector 집계 원천: `/Users/hammyeong-yeon/Desktop/10_work/noline/evidence-collector/store/`
- 집계 helper: `/Users/hammyeong-yeon/Documents/Codex/2026-09-14/new-chat/work/evidence_efficiency_audit.py`
- 선행 분석: `/Users/hammyeong-yeon/Documents/Codex/2026-09-14/new-chat/outputs/background-token-improvement-analysis.md`

Token은 receipt에 보고된 모델 처리량의 합이며 결제 금액이나 wall-clock time이 아니다. Transcript와 Noline store는 이 Workspace에 복제하지 않았다. 위 수치는 2026-09-14 시점 snapshot의 분석 근거이며 후속 실행으로 누적 store가 바뀌면 같은 helper와 판본 식별자로 새 baseline을 만든다.

## 활성화 상태

2026-09-15 문서 작성 직전 `~/.local/state/ai-native-moment-review/config.json`과 `~/.local/state/ai-native-moment-review-claude/config.json`의 `enabled`는 모두 `false`였다. 이번 작업은 해당 파일, Maintain hook·binding 또는 Noline collector 설정을 수정하지 않았다. Workspace 문서를 생성했다는 사실만으로 어떤 자동 검토도 활성화되지 않는다.
