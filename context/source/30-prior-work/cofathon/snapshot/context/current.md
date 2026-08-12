# current — 현재 그림

Cofathon 참가자로 선발되기 위한 전체 작업에서 지금 어디에 있고, 무엇을 향하며, 다음에 무엇을 판단할지 사용자와 AI가 같은 그림으로 보는 자리다.

> - 본체는 아래 지도 트리다. 첫 뎁스에는 전체 흐름을 두고 현재 판단점에서만 깊어진다.
> - 완료된 가지는 현재 효력과 상세 원본 링크만 남긴다. 이 문서는 이력을 쌓지 않는 덮어쓰기 전용 지도다.
> - 방향 변경은 AI가 제안하고 사용자가 확정한다. 실제 상태와 지도가 다르면 작업 전에 지도부터 고친다.
> - 진행 커서는 아래 지도에 하나만 둔다. 경로에서는 `context/`와 `.md`를 생략한다.

## 지도

- **[Goal] — 현재 운용 기준**
  - **Mission** — Cofathon **본선 참가자로 선발되는 것**. 수상·채용·포트폴리오는 그다음이다.
  - **Campaign Goal** — Q1만 읽어도 AI Native인 이유와 증명 논리가 이어지고, 선택한 실제 사용자 문제·workflow의 작동 결과와 AI 제작 과정의 인과가 실제 근거로 연결되는 지원안을 제출해 접수를 확인한다. 완료 조건은 [goal](./goal.md)이 소유한다.

- **[공식 지원 요구사항] — 현재 확인·제출 전 재확인**
  - 직접 요구되는 핵심은 Q1(`AI Native인 이유와 증명 방법`)이다. 결과물 링크는 허용된 증명 수단이지만 새 결과물 자체가 공식 필수는 아니다.
  - Q1 문구·입력 제한은 제출 직전에 라이브 원문을 다시 확인한다. 심사자의 링크 열람 방식과 배점은 공개되지 않았다. (→ [core/requirements](./core/requirements.md) · [research/00](./research/00-current-synthesis.md) · `cofathon-main/` · `cofathon-apply/`)

- **[트랙] — 확정·닫힘**
  - **KRAFTON FDE**를 선택했다. 현업 문제를 다시 정의하고 작동 결과까지 닫는 방향과의 정합성은 보되, 트랙 선택이나 FDE 직무 신호를 사전 선발의 숨은 우대로 바꾸지 않는다. (→ [research/01-first-pass/02](./research/01-first-pass/02-existing-evidence-and-track-decision.md))

- **[지원 증거물] — search-first 통제 기술 slice·별도 공개본 배포 / 실제 사용자 결과 열림**
  - 공식 필수와 별개로 AI Native 주장을 구체화할 **Codex plugin**을 만든다. 작동 결과와 AI 제작 과정은 실제 사용자 workflow에 연결된 근거가 생겼을 때만 지원 증거로 사용한다. (→ [core/support-evidence-artifact](./core/support-evidence-artifact.md))
  - 정적 심사자 페이지와 통제 비교 산출물은 사용자의 제품 기대와 맞지 않아 폐기했다. 현재 보존한 결과는 `src/tour-purchase-review/`의 기능 코드·60개 test, search-first raw fixture와 통제 설치 host 결과다. 현재판은 원본과 분리한 공개 저장소에 배포했으며, 실제 사용자 작동 결과는 아직 남아 있다. (→ [process/36](./process/36-discard-evidence-cycle-and-preserve-feature-core.md) · [process/39](./process/39-publish-sanitized-public-copy.md) · [engineering/03/02](./engineering/03-live-purchase-entry/02-search-first-slice-implementation.md))

- **[리서치] — 조사 본체 완료 / 현재 필요한 실제 입력 확인만 열림**
  - Q1은 직접 요구, Probe는 공식 배점표가 아닌 강한 방향 힌트, KRAFTON FDE는 선택 트랙의 공식 맥락으로 구분한다. `50/40/7/3`은 출처 신뢰 비중이지 공식 배점이나 후보 점수가 아니다. (→ [research/00](./research/00-current-synthesis.md))
  - Cofathon·Probe·FDE와 마이리얼트립 회사·서비스·사용자 자료를 확보했다. 과거 형태·장면·문제 후보의 발산과 순위는 현재 후보판이 아니며, 필요한 교정과 이력만 상세 원본에 남는다. (→ [research/](./research/README.md) · [problem/](./problem/README.md) · [process/](./process/README.md))

- **[문제 설정·솔루션] — live 후보 선택으로 주 장면 확장 / 실제 가치 미검증**
  - **선택한 문제** — 실제 날짜와 일행으로 투어를 결제하려는 사용자는 검색·상세·날짜별 option에 흩어진 판매 조건을 자기 개인 조건과 원하는 경험에 맞추고, 적합·충돌·결제를 바꿀 미확정과 답의 권위를 구분해 다음 후보와 확인 행동을 정하기 어렵다. (→ [problem/00](./problem/00-selected-problem.md))
  - **선택한 솔루션** — 자연어 여행 상황에서 현재 MyRealTrip 상품·상세·날짜별 option을 조회해 추가 검토 후보를 좁히고, 사용자가 고른 후보만 기존 질문 승인·판매자 답변 범위 재판정으로 잇는 Codex plugin이다. 상품 선택 전에는 MCP 검색, 이미 상품을 골랐다면 URL 입력과 MCP 상세·option 확인을 결합한다. 어느 한쪽을 억지로 낮추지 않는다. (→ [solution/00](./solution/00-selected-solution.md) · [process/37](./process/37-upgrade-solution-to-live-purchase-entry.md) · [process/38](./process/38-choose-entry-by-user-scene-and-use-mcp-fully.md))
  - 최소 2인 상품의 1인 참여를 가이드에게 확인한 사건과 임신 중 촬영 시간 조정을 외부에서 찾은 작가에게 확인한 사건은 각각 구매·이용으로 이어졌다. 기대한 체류·이동과 실제 경험이 달랐다는 주장 한 건도 있다. 서로 다른 사건이므로 반복 문제나 search-first 가치로 합산하지 않는다.
  - 현재 MyRealTrip MCP에서 검색·상세·날짜별 option의 live field와 말줄임·가격·수량 경계를 확인했다. MCP는 실제 제품 capability로 적극 사용하되 사용자 진입은 구매 단계에 맞춘다. 그 live 데이터가 실제 사용자의 후보 검토·제외·확인 행동을 바꾸는지는 아직 미검증이다.

- **[엔지니어링] — schema 1.1 core + search-first 통제 기술 slice / Loop 03 계속**
  - **최상위 구현 Goal** — 사용자의 자연어 여행 상황에서 현재 상품·option 근거로 추가 검토 후보를 좁히고, 선택 후보를 기존 단일 상품 review와 판매자 답변 재판정까지 이어 실제 사용자 판단 변화와 두 지원 증거 채널을 남긴다. (→ [engineering/00](./engineering/00-top-level-goal.md))
  - **Loop 01 — ACHIEVED** — 선택한 한 상품 이후의 조건 승인·질문 승인·답변 범위 재판정·저장 core를 구현했다. 이후 보강을 포함한 source `0.2.1`의 product test는 37개이며 기술 계약·회귀 범위만 뜻한다. (→ [engineering/01/goal](./engineering/01-purchase-decision-slice/goal.md))
  - **과거 Loop 02 — 폐기** — 수동 MCP 전사에서 공개 사실 누락과 raw 응답 미보존을 확인했고, 정적 reviewer artifact와 통제 비교 산출물은 현재 제품에서 제거했다. 실패 교훈만 새 acquisition 경계에 반영한다. (→ [process/36](./process/36-discard-evidence-cycle-and-preserve-feature-core.md))
  - `*-> 지금*` **Loop 03 — CONTINUE / search-first 통제 기술 slice·최신 설치 host 통과** — 자연어 search-first 요청에서 현재 MCP raw를 보존하고 최대 3개 추가 검토 후보를 만든 뒤, 선택 후보를 schema `1.1` 카드로 잇는 첫 slice를 구현했다. source `0.3.0+codex.20260717135144`, 60개 test와 최신 설치 cache replay host는 통과했다. URL-first canonical 경로, 실패·본문 보완 전 범위, 실제 사용자 한 명의 전후 판단은 남아 있다. (→ [engineering/03/goal](./engineering/03-live-purchase-entry/goal.md) · [engineering/03/02](./engineering/03-live-purchase-entry/02-search-first-slice-implementation.md))

- **[지원 제출] — 아직 열지 않음**
  - Q1은 링크 없이도 주장과 증명 논리가 이어지게 쓰고, 링크에서 plugin의 작동 결과와 그 결과를 만든 AI 작업 과정의 인과를 확인하게 한다.
  - 제출 직전 Q1 라이브 문구와 입력 제한을 다시 확인하고, 사용자 승인 뒤 제출과 접수를 확인한다.
