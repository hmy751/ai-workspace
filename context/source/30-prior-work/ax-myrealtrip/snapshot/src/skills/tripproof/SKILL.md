---
name: tripproof
description: 선택한 마이리얼트립 투어·액티비티를 사용자의 실제 일행, 날짜, 시각, 필수 조건으로 결제 전에 실행해 보고 최초 충돌, 사용자 허용 수정의 후속 영향, 판매자 답변 범위를 재판정한다. 상품 URL과 자연어 여행 조건으로 결제 검토 가능 여부를 묻거나, 막힌 원안을 수정하거나, 판매자 답변을 이어 붙일 때 사용한다. 여러 상품 추천·비교, 예약·결제 실행, 의료·안전 적합성 판단에는 사용하지 않는다.
---

# TripProof

사용자의 자연어 원안을 공개 상품 사실과 분리한 뒤, 의미 해석은 직접 수행하고 같은 구조화 입력에서 같아야 하는 판정·답변 범위·diff는 bundled Python으로 고정하라. 사용자가 JSON이나 상품 규정표를 먼저 만들게 하지 마라.

## 경로와 상태를 먼저 준비하라

1. 이 `SKILL.md`가 들어 있는 디렉터리를 `<SKILL_DIR>`, 그 디렉터리의 두 단계 위를 `<PLUGIN_ROOT>`로 사용하라. 현재 working id나 현재 작업 디렉터리 이름을 경로 계산에 사용하지 마라.
2. `<SKILL_DIR>/references/state-contract.md`를 읽고, 상세 예시는 `<PLUGIN_ROOT>/fixtures/loop-01/case.json`에서 확인하라.
3. `<PLUGIN_ROOT>/scripts/tripproof.py`가 없으면 자연어 판정으로 우회하지 말고 설치가 불완전하다고 알리라.
4. 현재 작업을 방해하지 않는 임시 디렉터리에 case JSON을 만들고 대화가 이어지는 동안 같은 파일을 갱신하라. 사용자의 프로젝트 파일에 상태를 저장해야 한다면 먼저 알리라.
5. 사용자 발화의 원문 일부와 turn 참조를 `user_input` provenance로 보존하라. 구조화 과정에서 뜻을 확장하지 마라.

## 1. 상품 사실을 확보하라

1. 설치된 `myrealtrip` MCP 도구를 먼저 확인하라. 런타임에 실제로 보이는 tool schema만 사용하고, 확인하지 않은 tool 이름이나 URL 직접 상세 조회 기능을 약속하지 마라.
2. MCP가 해당 상품 또는 필요한 조건을 주지 못하면 사용자가 명시한 공개 URL을 읽어라. URL 접근도 실패하면 유모차·시각·가격·티켓처럼 현재 결정을 바꾸는 구역만 붙여 달라고 요청하라.
3. `evidence_acquisition`에 시도한 경로, 성공/실패, 실패 이유를 남겨라. fallback이 성공해도 앞선 실패를 지우지 마라.
4. 각 상품 주장을 `public_fact`로 기록하고 URL, 확인 시각, 근거 문구를 붙여라. 문구가 없다는 이유로 허용·금지·확정으로 바꾸지 마라.
5. 보존 fixture를 사용할 때는 현재 조회 결과처럼 말하지 마라. 판매자 답변 fixture도 실제 재고나 판매자 발화가 아닌 검증 입력임을 명시하라.

## 2. 원안을 구조화하고 실행하라

1. 일행, 날짜, 희망 시각, 함께 참여해야 하는 관계, 바꿀 수 없는 조건을 분리하라. 아직 사용자가 허용하지 않은 대안은 만들지 마라.
2. 상품 사실, 사용자 입력, 판매자 답변, demo 가정을 서로 다른 provenance로 유지하라.
3. 다음 명령으로 구조와 판정을 검증하라.

```bash
python3 <PLUGIN_ROOT>/scripts/tripproof.py evaluate \
  --case <CASE_JSON> \
  --plan <ORIGINAL_PLAN_ID>
```

4. Python이 거부하면 자연어를 키워드로 다시 추정하지 말고 구조화 payload를 고쳐라. 근거나 적용 범위가 없으면 `정보 부족` 또는 `답변 대기`로 남겨라.
5. 결과에서 `first_blocker`를 먼저 설명하고, 시간처럼 남은 미확정과 티켓처럼 이미 확인됐지만 사용자가 준비해야 하는 부담을 구분해 보여라. 상품 규정 요약으로 끝내지 마라.
6. 원안이 충돌하면 바꿀 수 없는 조건과 사용자가 허용할 수정 범위만 물어라. plugin이 일행 분리·시간 변경·양보 조건을 제멋대로 확정하지 마라.

## 3. 사용자 허용 수정안만 다시 실행하라

1. 후속 발화가 명시한 변경만 새 revision plan과 `authorized_changes`에 기록하라. 원안 plan은 수정하거나 삭제하지 마라.
2. 날짜·시각·필수 조건 등 바뀌지 않은 값도 그대로 복사해 고정하라.
3. revision을 실행하고 원안과 diff를 계산하라.

```bash
python3 <PLUGIN_ROOT>/scripts/tripproof.py evaluate \
  --case <CASE_JSON> \
  --plan <REVISION_PLAN_ID>

python3 <PLUGIN_ROOT>/scripts/tripproof.py compare \
  --case <CASE_JSON> \
  --before-plan <ORIGINAL_PLAN_ID> \
  --after-plan <REVISION_PLAN_ID>
```

4. 해소된 충돌만 말하지 말고 참여자, 기본 투어비 영향, 희망 시각, 티켓 준비, 남은 미확정을 함께 설명하라.
5. revision도 충돌하고 사용자가 허용한 다른 안이 없으면 진행안을 발명하지 말고 `다른 상품 검토`와 다음 상품에서도 유지할 조건을 남겨라.

## 4. 결정 변수만 질문으로 바꿔라

1. snapshot의 `decision_variables` 중 `start_time_confirmation`만 판매자 질문으로 바꿔라. `minor_ticket_public_fact`는 공개 입력을 다시 확보해야 한다는 뜻이며 판매자 질문으로 우회하지 마라. 일반 확인 목록을 덧붙이지 마라.
2. 질문에 상품, 날짜, 현재 참여자와 변수에 필요한 시각을 포함하라. 공개 사실에 이미 절차가 있는 아동 티켓을 다시 묻지 마라.
3. 메시지는 사용자가 복사해 직접 보낼 수 있게 한 덩어리로 작성하라. 전송하거나 답변을 자동 수신했다고 말하지 마라.

## 5. 판매자 답변을 claim별로 적용하라

1. 답변 원문 전체와 출처 turn을 보존하라. 문장에 없는 적용 범위를 대화 맥락만으로 채우지 마라.
2. 각 시간 주장에 공통 scope인 상품·날짜·참여자와 요청 시각을 붙여라. Loop 01에서 seller claim으로 지원하는 것은 공개 정보로 닫히지 않은 `start_time_approved`뿐이다.
3. `네, 가능합니다`처럼 무엇에 가능한지 모호한 답은 scope를 비워 두어 고정층이 거부하게 하라. 전역 `답변 충분` 플래그로 여러 셀을 한꺼번에 확정하지 마라.
4. 다음 명령으로 답변 적용과 전후 diff를 확인하라.

```bash
python3 <PLUGIN_ROOT>/scripts/tripproof.py evaluate \
  --case <CASE_JSON> \
  --plan <REVISION_PLAN_ID> \
  --reply <REPLY_JSON> \
  --include-reply-decisions

python3 <PLUGIN_ROOT>/scripts/tripproof.py compare \
  --case <CASE_JSON> \
  --before-plan <REVISION_PLAN_ID> \
  --after-plan <REVISION_PLAN_ID> \
  --after-reply <REPLY_JSON>
```

5. 거부된 claim은 부족한 scope를 설명하고 기존 상태를 유지하라. 충분한 claim은 시간 셀만 바꾸고 공개 사실로 확인된 티켓 준비 부담·원안 충돌·가격 영향·판정 밖 영역을 보존하라.
6. `진행 가능`은 확인된 조건 범위에서 `결제 검토`로 이동할 수 있다는 뜻으로 설명하라. 재고·예약·결제·판매자 이행을 확정하지 마라.

## 매 응답의 출력 순서를 지켜라

1. 현재 plan의 전체 상태와 지금 할 일 한 가지
2. 최초 충돌 또는 아직 결정을 막는 변수
3. 원안과 허용 수정안 또는 답변 전후의 변경
4. 가격·티켓·시간·인원에서 남는 부담
5. 근거 층위와 사용한 입력 경로
6. 판정하지 않은 영역
7. 필요할 때만 사용자에게 묻는 한 가지 또는 판매자에게 보낼 한 메시지

항목 상태는 `정상 / 충돌 / 정보 부족 / 답변 대기`, 전체 상태는 `진행 가능 / 확인 후 진행 / 보류`, 다음 행동은 `결제 검토 / 추가 확인 / 다른 상품 검토`만 사용하라.

## 실패를 숨기지 마라

- MCP가 보이지 않거나 호출이 실패하면 이유를 남기고 URL로 이동하라.
- URL도 실패하면 필요한 본문 범위를 정확히 요청하라.
- Python 검증 오류는 해당 필드와 provenance를 고친 뒤 다시 실행하라. 검증을 생략해 자연어 결론만 내리지 마라.
- 현재 사실을 거의 확보하지 못하면 상품을 진행 가능으로 만들지 마라.
- 사용자가 예약·재고·의료 적합성·환불 결과를 묻는다면 판정 범위를 설명하고 공식 확인 경로로 넘겨라.
