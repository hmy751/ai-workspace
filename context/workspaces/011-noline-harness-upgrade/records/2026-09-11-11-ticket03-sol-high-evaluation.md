# Ticket 03 독립 작성: Sol high 추가 시험

2026-09-11, `011-noline-harness-upgrade`.

Sol high는 앞선 Terra xhigh·Sol medium보다 논의 기록의 내용이 뚜렷하게 나아졌다. 같은 원문과 작성 요청으로 Jest 설정 선택 이유, mock 공유 단계, package별 공통 설정 조건, 사용자 수락 발화와 원문 위치를 보존했다. 이번 표본에서는 Sol medium보다 약 7% 높은 전체 추정 비용으로 중요한 설명이 살아났으므로, 다음 Maintainer 후보로는 Sol high를 우선 권한다. 다만 초안을 무수정 반영할 수준으로 판정하거나 실제 기본 설정을 바꾸지는 않았다.

## 요청과 시험 조건

사용자는 두 후보의 병렬 시험 뒤 “그럼 sol high 로 테스트 해보자 추가로”라고 요청했다. 앞선 [모델 비교](2026-09-11-10-ticket03-model-comparison.md)와 같은 runner를 재사용하며 새 시험 폴더와 `gpt-5.6-sol / high`만 지정했다. Sol medium과 모델은 같고 추론 수준만 다르게 요청했다. 세부적인 누락 목록이나 정답 예시, 앞선 초안·평가를 입력에 추가하지 않았다.

새 session `01a09077-eccf-7cb1-a502-2485806bc383`의 시작·재개 로그 모두 Sol high와 read-only를 확인했다. 실제 도구 호출은 0건이다. 두 user prompt는 최초 Terra high 표본과도 바이트 단위로 같고 실제 session 입력에 포함됐다. 현재 Reference의 runtime·역할 설정·계약 여덟 파일도 이전 판본과 동일하다. 직전 두 후보는 병렬, 이번 high는 단독으로 실행했으므로 지연 시간 차이를 effort의 고정 효과로 해석하지 않는다.

기존 작성본과 코드 도구 원출력을 주지 않은 입력 범위, 빈 Ticket·색인의 시험용 bootstrap, 자동 AGENTS와 shell/web 비활성, 최초 임시 cwd와 parent 저장소 cwd로 재개된 제한은 앞선 시험과 같다. 실제 Noline Recover·hook 연결·Guard apply는 수행하지 않았다. 첫 초안만 회수하고 고치거나 다시 작성시키지 않았다.

- [Ticket 초안](receipts/maintain-writing-eval/2026-09-11-ticket03-sol-high/sol-high/preview/current/memory/tickets/03-storage-stats.md)
- [논의 record 초안](receipts/maintain-writing-eval/2026-09-11-ticket03-sol-high/sol-high/preview/records/2026-09-11-02-storage-stats-test-strategy.md)
- [실제 decision](receipts/maintain-writing-eval/2026-09-11-ticket03-sol-high/sol-high/02-decision.json), [설정·입력·사용량·연결 검사](receipts/maintain-writing-eval/2026-09-11-ticket03-sol-high/checks.json), [Noline 보존 확인](receipts/maintain-writing-eval/2026-09-11-ticket03-sol-high/completion.json)
- [공통 원문 입력](receipts/maintain-writing-eval/2026-09-11-ticket03/inputs.json), [앞서 고정한 평가 기준](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/review-criteria.json)

## 실제로 개선된 설명

Record 81행은 `jest.config.cjs`가 단순한 파일 선택이 아니라 preset 외에 경로·alias·transform 설정을 맡아 package.json의 역할을 흐리지 않게 하는 선택이라고 설명한다. Medium에는 초기 파일 목록은 있었지만 이 비교 이유가 빠져 있었다. 원본 L174의 선택 이유가 이번에는 남았다.

Record 85행은 mock 공유를 같은 파일의 builder, 같은 feature helper, 여러 feature의 공용 mock으로 나누고, 93행은 서로 다른 workspace에서 실제 React Native Jest 설정이 반복되는 경우에만 공용 test-config를 검토한다. 변환 오류 대응은 29행·81행에서 따로 다룬다. Medium record 40행처럼 mock·fixture·coverage까지 모두 “설정 오류가 실제로 나타나기 전에는” 추가하지 않는다고 묶지는 않았다.

Record 7–9행은 session id와 원문 범위, “전반적으로 다 좋아”, “그래 좋아”라는 사용자 발화와 수락 범위를 함께 남겼다. 그 수락을 모든 package의 영구 공통 정책이나 제품 완료로 확대하지 않는다. 원본 L181·209·242·254에 재접근해 확인할 수 있는 근거가 생겼다는 점에서 앞선 두 후보보다 낫다.

Ticket 28–34행은 `1,024 → 1 KB`, `1,536 → 1.5 KB`, 불필요한 `.0` 배제, DB 실패 뒤 이후 DB·지도 미조회, refresh 비누적을 판별 가능한 사례로 보존했다. 38행은 중복 제거와 실패 흐름의 가독성을 별도로 평가한다. 이는 원본 L127·174의 실행 기준을 이어받는 데 유용하다.

Record 33–35행은 순수 함수 검사의 입증 한계와 dependency adapter의 이익·비용을 설명한다. 39행은 Vitest와 Node의 추가 구성 부담을 일부 구별하고, 91–95행은 root 통합 테스트와 package별 테스트, 공용 설정 범위, exports 보존을 구분한다. 단순히 글이 길어진 것이 아니라 이전에 빠진 관계가 실제 본문에 들어왔다.

세 문서의 preview는 원래 decision과 정확히 같고, 허용 경로·preimage·EOF·줄 끝 공백 및 로컬 링크 세 개는 확인됐다. Record에서 Ticket으로 돌아가는 연결도 이번에는 있다. 이는 직접 검사 범위이며 Guard 전체가 실행·통과했다는 뜻은 아니다.

## 남은 부족함

**선택한 디렉터리의 비용은 아직 빠졌다.** Record 83행은 제품 타입·Router 경계 분리라는 이익을 설명하지만, 원본 L174에서 비교한 source 옆 배치의 탐색 이점과 별도 tests의 물리적 거리·source 구조 중복 관리 비용은 남기지 않았다. `jest.config.cjs`도 package.json 안에 두면 파일을 줄일 수 있다는 대안의 이익까지 충분히 다루지는 않는다.

**테스트 전용 타입 검사에 관한 조건이 단정적으로 바뀌었다.** 원본 L174는 “앞으로 유지할 회귀 테스트로 본다면 `tsconfig.test.json`까지 만드는 편을 권합니다”라는 조건부 권장이었다. High record 83행은 “테스트가 장기 회귀 자산으로 남을 예정이므로 … 방향을 채택했다”로 적었다. 전체 방향 수락의 근거는 있지만, 해당 유지 목적의 명시적 확정과 작성자의 해석을 구별하면 더 정확하다. Jest 실행이 타입 검사를 대신하지 않는다는 차이와 추가 설정·스크립트 비용도 여전히 약하다.

**전후 기준 검사를 선택 사항으로 읽히게 했다.** Ticket 36행은 현재 코드의 기준 검사와 리팩터링 후 재검사를 “가능하면” 수행한다고 썼다. 원본 L143의 제안 순서는 현재 hook 기준 검사를 먼저 실행하고 같은 검사를 다시 하는 것이다. 원문에서 선택적 보완으로 둔 것은 development build smoke test다. 실행 기준으로 채택할 때 이 강도는 구별해야 한다.

Record의 보호 동작·자동화 시나리오가 Ticket과 반복되고, Maestro와 Detox의 서로 다른 비용 및 schema placeholder script의 직접 관찰·recursive 명령 미실행도 충분히 남지 않았다. 따라서 중요한 실행 기준을 조정하고 남은 선택 비용을 보완할 편집은 필요하다. 모델 출력의 이러한 부분도 수정하지 않은 채 표본으로 보존했다.

## 가성비 비교

시간과 비용은 각 후보의 시작 grounding부터 첫 작성 응답 완료까지 합계다. 입력과 출력은 각 실행 로그에서 가져왔으며 캐시 입력·캐시 쓰기는 모두 0이다. 가격은 [앞선 단가 근거와 계산식](receipts/maintain-writing-eval/2026-09-11-ticket03-model-comparison/pricing-basis.json)에 따라 [Codex 표준 단가](https://learn.chatgpt.com/docs/pricing#token-rates)로 환산했다. 실제 청구나 플랜 차감을 확인한 값은 아니다.

| 후보 | 전체 시간 | 입력 토큰 | 출력 토큰 | 그중 추론 토큰 | 추정 크레딧 |
|---|---:|---:|---:|---:|---:|
| Terra xhigh | 105.7초 | 95,330 | 5,424 | 2,106 | 6.39 |
| Sol medium | 117.5초 | 95,446 | 4,353 | 478 | 11.72 |
| Sol high | 161.0초 | 95,395 | 6,055 | 1,092 | 12.57 |

High는 medium보다 전체 추정 비용이 약 7.2%, 작성 호출만 비교하면 약 10.4% 높았다. 최초 grounding 비용이 포함되는지에 따라 비율이 달라진다. 반복 운영의 캐시·문맥 길이·변화 없는 응답 비중은 이번 비용에서 평가하지 않았다. Terra xhigh와 비교하면 high의 전체 비용은 약 1.97배다.

이 사례에서 medium과 high 중에는 high의 추가 비용을 설명할 품질 차이가 있었다. 하지만 한 번의 표본이고 같은 user prompt라도 앞선 grounding 응답과 모델별 실행 문맥은 달라지므로 일반적인 우열이나 운영 월비용까지 확정하지 않는다. 이전 두 후보의 공통 실패만으로 모델 상향이 무효라고 결론 내릴 수 없듯, 이번 개선만으로 작성 지침과 검토가 불필요하다고 볼 수도 없다.

현재 제안은 Sol high를 우선 후보로 삼되 위의 남은 의미·조건 문제를 함께 다루는 것이다. 기본 모델 설정 변경, Noline 재적용, 추가 재시험은 아직 수행하지 않았다. 평가 기록은 미커밋이다.
