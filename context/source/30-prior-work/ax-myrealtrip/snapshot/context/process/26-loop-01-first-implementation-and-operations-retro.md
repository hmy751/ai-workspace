# Loop 01 첫 구현·fresh 판별과 개발 운영 회고

작성일: 2026-07-10

상태: 첫 구현 checkpoint. fresh 판별은 미통과이며 수정 전 사용자 논의를 위해 멈춘다. Loop 01 goal은 완료하지 않았다.

현재 계약: `engineering/01-loop-01-goal.md`

## 한 것

### 첫 구현 산출물

- **[구현]** `src/`를 제출 규정상의 plugin root로 만들고 manifest, MyRealTrip MCP companion 설정, 명령형 skill, 구조화 상태 계약을 작성했다.
- **[구현]** 자연어 해석은 Codex에 남기고 Python은 구조화 입력의 provenance·사용자 허용 변경·상태 전이·seller claim scope·diff·결정성을 고정하는 `src/scripts/tripproof.py`를 만들었다.
- **[구현]** 우피치 가족 투어의 원안, A+C 허용 수정안, 모호 답변, 시간만 확인한 답변, 충분 답변 fixture와 black-box test를 만들었다.
- **[검증]** plugin validator와 skill validator가 통과했다.
- **[검증]** `python3 -m unittest discover -s src/tests -v`에서 9개 test가 통과했다.
- **[검증]** CLI demo에서 다음 상태가 재현됐다.
  - 네 명 원안: `보류 / 추가 확인`, 최초 중단은 D의 유모차 충돌
  - A+C 허용 수정안: `확인 후 진행 / 추가 확인`, 기본 투어비 유지·16:00·미성년자 티켓 부담 보존
  - 모호 답변: 판정 diff 없음
  - 시간만 충분한 답변: 시간만 국소 갱신
  - 충분 답변: A+C만 `진행 가능 / 결제 검토`, 원안 충돌 보존
  - 같은 충분 답변 반복: 같은 snapshot

### 실제 공개 입력

- **[검증]** 공식 MCP endpoint `https://mcp-servers.myrealtrip.com/mcp`의 initialize와 tools/list를 직접 실행했다.
- `searchTnas`가 대표 상품 `3886992`와 현재 상품 URL을 반환했다.
- `getTnaDetail`이 기본 15:00, 미성년자 티켓·예약비와 예약 후 메시지 절차를 반환했다.
- `getTnaOptions`가 2026-08-12 예약 가능, 1명 300,000원·2명 각 150,000원·3명 각 100,000원·4명 각 75,000원으로 1~4명 총액 300,000원 구조를 반환했다.
- 공개 상품 URL은 유모차 불가, 미팅 시간 조율 가능, 1~4명 동일 행사비, 미성년자 사전 메시지·개별 티켓 구매 절차를 현재도 노출했다.
- 현재 MCP와 URL 사실을 판별자가 메모리 case로 대입했을 때도 원안 `보류`, A+C `확인 후 진행`이 재현됐다.

### fresh 독립 판별

- 기존 대화와 worker 설명을 전달하지 않은 `fork_turns=none` read-only 판별자에게 Loop 01 계약, 최상위 goal, 실제 `src/`만 원천으로 줬다.
- 판별자는 test·CLI·validator·MCP 검색/상세/옵션·공개 URL을 독립 실행했다.
- **[판정] 미통과**: 고정 상태 엔진은 제품의 골격을 보여주지만 설치된 새 Codex 세션의 자연어 end-to-end가 없고, 계약·고정층에 필수 결함이 남았다.

## fresh 판별에서 확인된 결함

### P0 — 검증 공백

- plugin이 현재 설치 목록에 없고, 새 Codex 세션에서 `자연어 원안 → MCP/URL → 구조화 case → Python → 수정 발화 → seller 답변 → 결제 검토`가 이어지는 증거가 없다.
- 따라서 LLM이 실제로 허용 범위·최소 질문·raw seller 답변 claim을 올바르게 만드는지도 아직 증명되지 않았다.

### P1 — 계약·구현 결함

- **[계약]** 공개 URL이 이미 `미성년자 사전 메시지·개별 구매·예약 후 안내`를 말하는데 fixture는 같은 티켓 절차를 `답변 대기`로 만들고 다시 묻는다. 최소 질문이 실제 미확정이 아니다.
- **[구현]** public fact와 plan의 boolean·integer·날짜·시각 타입 검증이 약하다. 예를 들어 문자열 `"false"`가 유모차 충돌을 없앨 수 있고 잘못된 가격 값은 구조화 오류 대신 traceback을 낼 수 있다.
- **[구현]** C에게만 scoped된 티켓 claim이 다른 미성년자까지 정상으로 바꿀 수 있다.
- **[구현]** 같은 타입의 상반 claim을 함께 accepted하고 배열의 마지막 값이 결론을 바꿀 수 있다.
- **[검증]** 실제 자연어 구조화와 seller raw text→claim 변환을 실행하지 않았다.

### P2 — 보강 필요

- 정상·정보 부족·허용안 소진·부정 seller 답변·MCP 실패→URL fallback이 checked-in fixture/test에 없다.
- 중복 참여자, revision이 자기 자신을 base로 삼는 lineage, 근거 없는 `authorized_options_exhausted`를 막지 않는다.
- seller 답변이 매번 상품·날짜·참여자를 문장 안에서 전부 반복해야 한다는 계약은 실제 같은 문의 thread의 짧은 답을 과도하게 거부할 수 있다.
- 사람에게 바로 보이는 자연어 출력과 재현 안내는 아직 없고 README는 placeholder다.

## 펼친 개발 운영 방식

1. 한 worker에게 scaffold·plugin workflow·state engine·tests·실입력·검증 전체를 맡긴다.
2. root가 goal과 계약을 들고 workflow owner와 engine owner를 병렬로 둔다.
3. engine도 code owner와 fixture/test owner로 더 나눈다.
4. 구현 팀과 분리된 fresh read-only 판별자를 마지막에 둔다.

두 번째와 네 번째의 방향은 유지할 가치가 있었다. 다만 실제 운영에서는 분할 시점과 worker의 첫 산출물 규칙이 늦어 root가 여러 번 개입해야 했다.

## 기각한 운영 방식과 이유

- **[기각] 하나의 거대 worker가 끝까지 소유**: 첫 worker는 계약 검토와 하위 reviewer까지 진행했지만 scaffold 뒤 실제 code를 쓰지 않고 내부 설계에 오래 머물렀다. 넓은 목표·긴 입력·자기 검토가 한 주체에 겹쳤다.
- **[기각] worker 아래 상시 leader/reviewer 계층**: 사용 가능한 동시 슬롯에서 중간 전달자가 한 자리를 차지하고, root가 실제 filesystem 진행을 늦게 보게 됐다. 이번 규모에서는 root가 두 artifact owner를 직접 조율하는 편이 낫다.
- **[기각] worker의 “통과” 보고를 증거로 채택**: validator 통과 보고 뒤 root가 기본 Python으로 재현하자 PyYAML 부재로 실패했다. 정확한 interpreter를 받아 root가 같은 명령을 다시 실행한 뒤에만 통과로 인정했다.
- **[기각] 모든 fresh 검사에서 전략 평가까지 반복**: 이번 종합 검사는 Loop 완료 후보를 보는 첫 검사라 가치가 있었지만 보고가 길어졌다. 수정 후 회귀 검사까지 데모 임팩트·해커톤 매력을 다시 보면 느리고 기준이 섞인다.

## 막힌 지점과 해결

### 1. 첫 worker가 설계에서 나오지 않음

- **막힘**: scaffold와 계약 review는 있었지만 engine·test 파일이 생기지 않았다.
- **해결**: 실제 filesystem을 기준으로 지연을 확인하고 worker를 중단했다. 대체 worker에는 작은 patch와 command output을 먼저 내도록 지시했다.
- **배운 점**: “계속 진행 중” 메시지가 아니라 첫 artifact와 실행 증거를 checkpoint로 삼아야 한다.

### 2. 병렬화 뒤에도 engine 작성이 느림

- **막힘**: workflow owner는 manifest·skill·contract를 완성했지만 engine owner는 exact CLI 합의만 반복하고 code를 쓰지 않았다. code/test로 더 나눈 뒤 fixture만 먼저 나왔고 engine·test code는 다시 지연됐다.
- **해결**: exclusive path를 보존한 채 해당 worker를 중단하고 root가 exact CLI와 tests를 직접 구현했다.
- **배운 점**: 일을 더 작게 나누는 것만으로 충분하지 않다. worker가 첫 보고 전에 실제 파일 하나와 실행 결과 하나를 내게 해야 하며, 두 번째 계획 보고가 오면 바로 교체해야 한다.

### 3. plugin과 engine의 CLI 이름 불일치

- **막힘**: skill은 `scripts/tripproof.py`를 호출했지만 초기 engine 계획은 다른 파일명이었다.
- **해결**: 두 owner가 쓰기 전에 root가 exact CLI와 case/reply contract를 공유 인터페이스로 고정했다.
- **배운 점**: 병렬 시작 전에 전체 schema를 완성할 필요는 없지만, 파일 경로·명령·입출력 키처럼 접합면은 먼저 고정해야 한다.

### 4. validator 실행 환경 차이

- **막힘**: 기본 Python과 workspace bundled Python에는 PyYAML이 없어 creator validator가 시작 전 실패했다.
- **해결**: 새 설치 없이 기존 PyYAML이 있는 interpreter를 찾고 worker와 root가 같은 명령으로 재실행했다.
- **배운 점**: worker 착수 전에 validator runtime을 preflight하고 exact command를 공유해야 한다.

### 5. fixture test가 계약 자체의 오류를 놓침

- **막힘**: 9개 test는 설계한 happy/exception flow를 모두 통과했지만, 공개 사실상 이미 닫힌 티켓 절차를 다시 묻는 모순과 타입·아동 범위·상반 claim 공격을 잡지 못했다.
- **해결**: 구현 맥락이 없는 fresh 판별자가 실제 URL과 adversarial memory input을 대조해 발견했다.
- **배운 점**: fixture test는 “내가 만든 세계”를 확인한다. contract-to-source 대조와 schema fuzz/adversarial case를 별도 gate로 둬야 한다.

## 다음 구현부터 적용할 운영안

### Root

- Codex goal, 사용자 의도, acceptance, path ownership, 최종 완료 판정을 소유한다.
- worker의 설명이 아니라 `git status / 실제 파일 / 직접 재실행 output`으로 checkpoint를 닫는다.
- 계약을 바꾸는 판단과 source 경계는 worker에게 넘기지 않는다.

### Artifact owner

- worker마다 쓰기 경로 하나와 산출물 하나만 준다. 같은 파일을 두 worker가 수정하지 않는다.
- 첫 checkpoint는 계획이 아니라 `첫 파일 + 첫 실행 결과`다.
- worker가 임의로 하위 reviewer를 만들지 않는다. 독립 review는 root가 별도 fresh 주체로 띄운다.
- 두 번째 계획 보고가 오기 전에 artifact가 없으면 범위를 다시 자르거나 교체한다.

### Integration

- 병렬 시작 전에 `경로 / CLI / 최소 JSON keys / error contract`만 얇게 고정한다.
- 각 owner가 통과하면 integration worker를 잠깐 두되 새 설계가 아니라 접합과 end-to-end만 맡긴다.
- **fresh 검사 전에 설치된 새 Codex 세션 실행을 pre-gate로 둔다.** 이 증거가 없으면 verifier가 볼 준비가 안 된 것이다.

### Verifier

- 일반 구현 회귀 검사는 짧게 한다.
  - 게이트 결론
  - 실패·부분 항목만
  - 구현 결함 / 계약 결함 / 검증 공백
  - 필수 수정 최대 3개
  - 다음 한 동작
- `상세 요약기로 축소됐는가`만 매번 한 문장 확인한다.
- 사용자 현실성·데모 임팩트·창의성·해커톤 매력은 Loop 완료 종합 검사에서 한 번만 본다.

## 검증 안 된 것

- 실제 marketplace 또는 local install을 거친 plugin pickup.
- 새 Codex 세션의 자연어 구조화, MCP tool 선택, turn 간 상태 보존과 bundled Python 호출.
- 최소 질문 계약을 실제 공개 미확정에 맞게 고친 뒤의 end-to-end.
- 강화된 타입·lineage·claim conflict validation.
- 사람용 자연어 출력과 README 재현 절차.

## 재개할 때 볼 후보 — 아직 결정 아님

1. 실제 공개 근거와 겹치는 티켓 질문을 제거하거나, 진짜 미확정 변수를 다시 잡는다.
2. 타입·중복 참여자·revision lineage·claim 국소성·상반 claim을 먼저 고친다.
3. 정상·정보 부족·허용안 소진·fallback test를 추가한다.
4. 설치·새 세션 전체 흐름을 실행한 뒤 짧은 fresh 회귀 검사를 한다.

이 순서는 다음 논의에서 바꿀 수 있다. 현재 문서는 미통과를 숨기지 않고 첫 구현과 운영의 실제 증거를 보존하는 checkpoint다.
