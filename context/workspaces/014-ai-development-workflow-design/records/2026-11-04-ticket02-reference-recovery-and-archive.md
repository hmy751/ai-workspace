# Reference의 재개 안내와 Recover·Verify 아카이빙

2026-11-04. 사용자는 prototype 반영과 기록을 먼저 커밋한 뒤 Reference 전환을 진행하자는 제안에 “그래 진행해줘”라고 답했다. 기준 commit은 `f3d13f23`이다. 이번 범위는 Reference의 현재 운영본과 이를 이식하는 root 소비자이며 Noline에는 쓰지 않았다.

## 반영한 결과

[Prototype의 선택과 읽기 확인](2026-11-04-ticket02-recovery-guide-prototype.md)을 Reference의 default-timeout 작업에 적용했다. 예제 제품의 목표와 코드, 기존 검증 근거를 유지하며 재개·생성·기록·검증 연결을 전환했다.

| 책임 | 현재 위치와 반영 |
| --- | --- |
| 재개 공통 기준 | [Reference Work AGENTS](../../../../reference-project/context/work/AGENTS.md). 일반 재개와 한정 과업, 충분한 이해와 공백 시 확장, 안내 구성·조건부 갱신을 연결 |
| 실제 재개 자료 선택 | [001 recover.md](../../../../reference-project/context/work/workspaces/001-default-timeout/recover.md). 기본 목표·상태·산출물 지도와 요청별 Spec·Project·실행 근거를 연결 |
| 정체성·기본 선택 | Workspace README와 collection README. 이전 identity/default JSON의 역할을 사람이 읽는 기존 진입점에 통합 |
| 생성·기록 | 생성 계약과 create-context-workspace가 초기 안내를 만들고 record-work가 읽을 대상·이유가 달라졌을 때 갱신 |
| 검증 | development와 실제 제품 검사. 필요한 판본·조건·결과·미확인을 Ticket·records·state에 연결하며 새 Verify나 machine status를 요구하지 않음 |
| 외부 적용 | root apply-context-harness가 현행 Reference를 기준으로 적응. 기존 대상 runtime·사용자 변경·증거는 실제 소비자를 대조해 승인된 전환 범위만 처리 |

Prototype의 로그인 Work를 Reference 제품 사건으로 옮기지 않았다. Reference의 `request_timeout_ms` 생략·명시값·거부 입력·불변 반환 계약에 맞춰 안내를 구성했다. Project의 본문 선택과 이유는 기존 선택 문서에 두고 recover에는 그 문서를 읽을 조건을 연결했다.

## 아카이빙과 보존

[보존본](archives/2026-11-04-recover-verify/README.md)은 기준 commit의 Reference 전체와 당시 root 이식 스킬·AGENTS·README를 담는다. Runtime만 떼면 기존 테스트의 import·상대 경로·Workspace 의존이 깨지므로 원래 의존 관계를 복원할 수 있는 묶음으로 보존했다. 활성 Reference에서는 runtime 61개·기계 계약 5개·runtime 전용 package 표식 2개, 총68개 파일을 내렸다. [원래 경로와 SHA-256](receipts/recovery-transition/2026-11-04-archive.json)으로 보존본과 제거 전 bytes를 대조했다.

기존 제품·source·날짜별 record·receipt 89개 파일은 변경 전과 같은 bytes다. 과거 Verify receipt 12개는 원래 Workspace 경로에 남겼으며, Spec·Ticket HISTORY의 원래 내용은 그대로 두고 새 전환 항목만 추가했다. 색인은 현재 지위를 설명하도록 갱신했다. 이전 성공·freshness·status가 현재 완료를 뜻하지 않게 sample state와 기록 안내를 맞췄다.

새 안내·스킬은 옛 Verify의 자동 snapshot·bounded 출력·process-group timeout·receipt/status·freshness 계산을 동일하게 제공하지 않는다. [기능 비교](2026-11-04-verify-removal-tool-comparison.md)에서 확인한 차이는 실제 실행 도구의 조건 확인과 근거·한계 기록으로 이어진다. 별도 범용 Verify를 스킬 안에 다시 구현하지 않았다. Root의 독립 Python Harness 검사 helper는 기존 대상의 장치를 유지·수정할 때만 선택하는 보조로 남았고 신규 설치의 필수 단계에서 내렸다.

## 직접 확인

- 변경 전 Reference root의 제품·Harness 검사95개 통과.
- 변경 후 Reference root의 직접 제품 검사7개 통과. 제품 코드는 변경하지 않았으며 새 Verify receipt·machine status를 만들지 않았다.
- 보존본을 별도 임시 위치에 풀어 이전 전체 검사95개 통과. 현재 Reference를 덮어쓰거나 옛 실행기를 재설치하지 않았다.
- Reference의 로컬 경로1258개·앵커268개 확인에서 누락0개. Root 이식 관련 링크·앵커34개, 수정한 skill·UI YAML과 diff whitespace 확인 통과. 공식 skill validator는 기존 PyYAML 부재로 실행하지 못했고 Ruby로 YAML을 확인했다.
- 별도 검토에서 활성 소비자·권한/routing·archive와 삭제 파일 대응·기존 증거 보존을 대조했고 수정이 필요한 회귀는 발견하지 못했다. 검토자의 직접 테스트·host 실행은 포함하지 않는다. [원보고](experiments/reference-recovery-2026-11-04/transition-review.md)에 확인 범위·한계를 보존했다.
- 부모 대화와 기대 답을 받지 않은 두 읽기 담당자에게 일반 재개와 한정 설명을 맡겼다. 일반 독자는 현재 구현·새 검사 기록·과거 receipt·사람 수락의 차이와 다음 판단을 복원했고, 정확히 왜5000인가의 비교·정량 근거가 없음을 드러냈다. 한정 독자는 생략과 boolean 입력의 차이를 제품 기준·코드에서 설명했으며 Work 재개를 시작하지 않았다.

읽기 담당자들은 제품 검사·수정을 하지 않았고 기록된 통과와 자신이 직접 확인한 본문을 구별했다. 한정 독자의 첫 파일 목록 탐색에 Workspace014 파일명 일부가 노출됐지만 해당 본문·이력은 읽지 않았다. 두 실행의 구체적인 읽은 파일과 제한은 [시험 자료](experiments/reference-recovery-2026-11-04/README.md)에 남긴다. 전체 파일 읽기도 포함되어 있으므로 읽기량·토큰·시간 절감을 입증한 비교 시험으로 해석하지 않는다.

Root·014의 변경 문서까지 넓힌 링크 확인에서 새 누락은 없었다. 기존 current의 원자료 `#L` 접근점4개는 현재 파일의 실제 줄 앵커로 확인되지 않아 기존 상태로 구별했으며 이번 작업에서 원문·옛 의미를 추정해 수정하지 않았다. [링크 판정](receipts/recovery-transition/2026-11-04-link-check.json)에 위치를 남겼다.

격리한 Reference 복사본에서는 환경 변수 지원 여부를 논의할 새 Work를 생성했다. 새 문서15개와 목록 한 줄만 추가·수정됐고 기본001과 기존 제품·정책을 유지했다. 기존273개 항목 중 목록1개만 바뀌고 나머지272개는 동일했다. Main의 최종 대조에서도 같은 범위를 확인했다. 별도 독자가 현재 목표·미정·첫 행동을 인수했으며 생성 기록의 확인 근거 누락은 보완·재독했다. 새 기계 계약·제품 구현·정책 채택·테스트 재실행은 없었다. [생성 보고와 결과 사본](experiments/reference-recovery-2026-11-04/README.md)에 실제 범위·한계를 남긴다. 이번 확인은 새 host 전체의 discovery·각 스킬 실행·원문 접근·반복 기록·장기 재개 효과를 포괄하지 않는다.

## 다음 책임

이번 적용으로 Reference의 기존 CLI·기계 계약·생성/이식 소비를 새 흐름에 맞추는 작업은 마무리한다. 전체02의 문서별 보존·중복과 Workspace 구성, 실제 사용의 기록 품질·재개 비용 논의는 남는다. [문서별 비교안](2026-10-30-ticket02-document-duplication-comparison.md)을 이번 변경만으로 전체 채택한 것은 아니다.

06-01에는 실제 적용과 확인 결과를 연결했으며 전체 host 통합·최종 완료는 따로 판단한다. Noline은 그 대상의 기존 상태와 병렬 변경을 확인하는 후속 적용으로 남는다. 별도015의 `.gitignore`·Workspace 목록·문서는 수정하지 않았다. 이번 변경의 commit·push는 하지 않았다.
