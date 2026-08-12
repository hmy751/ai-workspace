# Loop 01 교정 cycle — 제출 가능한 한 경로를 먼저 닫기

작성일: 2026-07-10

상태: 완료. 교정 구현, 설치된 자연어 E2E, 짧은 fresh 회귀 판별을 통과해 Loop 01 게이트를 닫는다.

## 한 것

- 첫 구현의 자동 테스트 9개, 정적 plugin/skill validator, 실제 공식 MCP와 공개 URL 접근은 통과했지만 설치된 새 Codex 작업의 자연어 전체 흐름은 증명하지 못했음을 다시 확인했다.
- fresh 판별에서 다음 결함을 적대 입력으로 재현했다.
  - 문자열 `"false"`가 boolean 사실처럼 흘러 유모차 충돌을 없앤다.
  - C 한 명의 티켓 claim이 C·D 전체 상태를 바꾼다.
  - 같은 범위의 상반된 시간 claim은 배열의 마지막 값에 따라 결론이 뒤집힌다.
  - revision이 자기 자신을 base로 삼아도 통과한다.
- 사용자는 티켓 한 항목만이 아니라 아래 전체를 이번 교정 범위로 명시했다.
  - 실제 plugin 설치와 새 작업 감지
  - 자연어 URL 입력부터 원안·허용 수정·판매자 답변까지의 E2E
  - 상태 엔진 안전성
  - 심사자가 그대로 재현할 README
  - 짧은 worker 소유 단위와 짧은 fresh 회귀 검사
- 공개 상품 사실에 이미 `티켓 개별 구매·예약 후 메시지 안내·미성년자 사전 메시지`가 있으므로, 티켓을 판매자에게 다시 물을 미확정 변수로 두지 않기로 교정했다.

## 기준 갱신

- 이전: `16:00 가능 여부`와 `아동 티켓 절차` 두 항목을 판매자에게 묻고 답변 뒤 두 상태를 갱신한다.
- 갱신: 아동 티켓은 공개 사실로 확인된 `정상 + 별도 준비 부담`으로 유지한다. 판매자에게 묻는 유일한 결정 변수는 공개 정보로 닫히지 않은 `2026-08-12 16:00 시작 가능 여부`다. 충분한 답변은 시간 상태만 바꾸며, 티켓 부담·기본 투어비·원안 충돌은 그대로 남는다.
- 이전: worker 하나가 큰 Loop 01 전체를 맡고 fresh 판별자가 구현·제품 매력까지 한 번에 넓게 본다.
- 갱신: worker는 `계약/엔진`, `설치/E2E`처럼 겹치지 않는 짧은 산출물만 소유한다. 첫 체크포인트는 계획이 아니라 첫 파일 또는 첫 명령 결과다. Loop 01 회귀 판별은 `설치 / 자연어 E2E / 상태 정확성 / 치명 결함 최대 3개`만 보고, 데모 임팩트·창의성은 통과 뒤 별도 제출 점검에서 본다.

## 펼친 후보

- 티켓 공개 문구를 boolean `준비 필요`로만 유지하고 계속 판매자에게 묻기 — 구현 변화는 작지만 이미 아는 내용을 다시 물어 최소 질문 원칙을 깨므로 기각했다.
- 공개 문구의 절차와 부담을 구조화해 티켓 상태를 닫고 시간만 묻기 — 현재 근거와 사용자 행동에 맞아 채택했다.
- 티켓 seller claim을 여러 아동별로 일반화해 유지하기 — 다른 상품 확장에는 쓸 수 있지만 현재 대표 사건에는 필요하지 않고 scope 복잡성만 키우므로 Loop 01에서 제거한다.

## 기각한 후보와 이유

- Loop 02로 넘어가 기능 수를 늘리는 안: 설치된 자연어 실행이 없는 상태에서는 제출물의 핵심 작동을 증명하지 못한다.
- README와 자연어 E2E를 뒤로 미루는 안: 심사자 환경에서 plugin이 감지되고 재현되는 것이 현재 P0이므로 구현의 마지막 장식이 아니다.
- broad fresh review를 즉시 반복하는 안: 이미 드러난 P0/P1을 고치기 전에 같은 판정을 반복하게 되므로, 교정 후 짧은 회귀 판별로 제한한다.

## 막힌 지점과 해결

- 기본 personal marketplace가 없고 현재 plugin은 `src/`가 root라 바로 설치된 항목이 아니었다. 공식 plugin-creator scaffold로 `personal` entry와 `~/plugins/tripproof` staging을 만들고, repo `src/`를 복제한 뒤 staging manifest에만 cachebuster를 붙여 설치했다. 제출 manifest는 `0.1.0`을 유지한다.
- 첫 새 작업은 기본 model이 code-mode-only였지만 로컬 `/opt/homebrew/bin/codex-code-mode-host`가 없어 tool 실행이 막혔다. 제품 실패로 숨기지 않고 중단한 뒤 shell tool을 쓰는 `gpt-5.5` 새 작업으로 다시 실행했다. plugin·MCP·Python은 같은 설치 snapshot을 사용했다.
- 첫 resume 명령을 실수로 repo cwd에서 실행해 프로젝트 SessionStart 위치 보고가 개입했다. 해당 turn은 제품 성공 증거에서 제외하고, 같은 task를 temp cwd에서 다시 resume해 남아 있던 case 상태를 이어갔다.
- README placeholder를 제거하고 실제 자연어 입력, 수정 발화, seller 답변, 표준 demo·unittest 명령, 실패 경계를 작성했다.

## 실행 증거

### 고정층과 설치

- repo와 설치 cache 모두 `python3 -m unittest discover -s .../tests -v`에서 15개 테스트를 통과했다.
- plugin validator와 skill validator가 통과했다.
- 설치 ID: `tripproof@personal`, version `0.1.0+codex.20260710143224`, `installed: true`, `enabled: true`.
- 설치 cache: `~/.codex/plugins/cache/personal/tripproof/0.1.0+codex.20260710143224`.
- repo와 설치 cache의 `scripts/tripproof.py`, `skills/tripproof/SKILL.md`, 대표 `case.json` SHA-256이 각각 일치했다.

### 설치된 새 Codex 작업

- task id: `019f4c73-cfe6-7442-9174-86c3dc05b4e6`
- 원문 session: `~/.codex/sessions/2026/07/10/rollout-2026-07-10T23-34-46-019f4c73-cfe6-7442-9174-86c3dc05b4e6.jsonl`
- temp 상태와 사람이 읽는 결과: `/tmp/tripproof-e2e.xvAsRj/`
- 첫 자연어 요청은 URL·네 명 일행·D 유모차·2026-08-12·16:00만 제공했다. 설치 cache의 skill을 읽고 공식 `searchTnas`, `getTnaDetail`, `getTnaOptions`를 실제 호출한 뒤 case를 만들고 installed Python으로 검증했다.
- 상태 전이:
  - 원안: `보류 / 추가 확인`, 최초 충돌 `D 유모차`, decision variable `start_time_confirmation` 하나.
  - A+C 사용자 허용 수정: `확인 후 진행 / 추가 확인`, 참여 충돌 해소, 가격·티켓 부담 유지, 16:00만 답변 대기.
  - `네, 가능합니다`: 상품·날짜·참여자·시각 scope 부족으로 rejected, decision diff 없음.
  - 상품·날짜·A+C·16:00을 명시한 답변: 시간 claim만 accepted, `진행 가능 / 결제 검토`. 원안 충돌·기본 투어비·티켓 부담은 유지.

### 계약 결함 회귀

- 문자열 boolean·bool-as-int·잘못된 날짜/시각·중복 participant를 구조화 `ContractError`와 exit 2로 거부한다.
- seller ticket claim은 Loop 01에서 unsupported다. 공개 티켓 사실이 없으면 `minor_ticket_public_fact`로 사실층 재확보를 요구한다.
- 같은 범위의 중복·상반 시간 claim은 배열 순서와 무관하게 계약 오류다.
- revision은 original을 직접 base로 삼아야 하며, `authorized_options_exhausted: true`에는 사용자 provenance가 필요하다.

## 짧은 fresh 회귀 판별

작업 맥락과 이전 판정을 주지 않은 별도 판별자에게 repo 산출물, 설치 상태, 실제 E2E task와 temp artifact만 전달했다. 전략적 매력·창의성·시각성은 이번 회귀 범위에서 제외했다.

- 결론: 통과
- 설치: `tripproof@personal`의 installed/enabled 상태와 설치 cache의 skill·Python·MCP 실행을 확인했다.
- 자연어 E2E: JSON이나 규정표 선입력 없이 같은 task와 case에서 원안 → A+C 허용 수정 → 모호 답변 → 충분 답변이 이어졌음을 확인했다.
- 상태 정확성: 티켓은 공개 사실의 `정상 + 준비 부담`, 질문은 16:00 하나, 모호 답변 diff 없음, 충분 답변은 시간만 갱신함을 확인했다. 15개 회귀 테스트도 재실행했다.
- 제출 재현: README의 demo와 unittest 명령을 제출물 root에서 그대로 실행했고 현재 fixture 설명과 일치했다.
- 치명 결함 P0/P1: 없음.
- 판별자 한 문장: 상세 요약기가 아니라 `원안 보류 → 허용 수정 → 답변 적용 거부/수용 → 결제 검토`로 실제 다음 행동을 바꾸는 workflow다.

## 검증 안 된 것

- 제출 zip을 실제로 만들고 푸는 최종 제출 정합성은 Loop 01 이후 별도 바퀴다.
