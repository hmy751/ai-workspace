---
name: review-tour-purchase
description: 투어·액티비티를 고르거나 결제하기 전에 목적지·날짜·일행·숙소 위치·포기할 수 없는 조건·원하는 경험을 받으면 현재 MyRealTrip 검색·상세·날짜별 option으로 추가 검토 후보를 좁히고, 이미 고른 상품 URL은 같은 live 근거로 깊게 검토한다. 선택 후보의 결제 중요 미확정을 판매자 질문으로 만들고 사용자가 붙여넣은 답변 범위 안에서 구매 검토·보류·다른 상품 검토를 다시 판단한다. 투어 후보 추천·비교, 상품 URL 결제 전 검토, AI 조건·질문 승인, 저장된 검토에 판매자 답변 반영을 요청할 때 사용한다. 자동 예약·결제·메시지 전송, 여행 품질 보장, 의료·안전 적합성 판단에는 사용하지 않는다.
---

# Review Tour Purchase

자연어의 의미와 원하는 경험에서 운영 조건 후보를 도출하는 일은 직접 수행한다. 같은 raw MCP 입력에서 같아야 하는 상품·URL·날짜·option·가격 의미·말줄임 경계와, 사용자 승인·provenance·질문 맥락·claim scope·상태 전이·decision card·저장은 bundled Python으로 고정한다. 사용자가 JSON이나 내부 ID를 먼저 만들게 하지 않는다.

## 실행 경로를 준비한다

1. 이 `SKILL.md`가 있는 디렉터리를 `<SKILL_DIR>`, 그 두 단계 위를 `<PLUGIN_ROOT>`로 사용한다. working directory나 설치 cache의 버전 이름을 경로 계산에 사용하지 않는다.
2. 새 후보 또는 URL 검토라면 `<SKILL_DIR>/references/acquisition-contract.md`와 `<SKILL_DIR>/references/state-contract.md`를 읽는다. 저장된 review에 답변만 이어 붙이면 `state-contract.md`만 읽는다.
3. `<PLUGIN_ROOT>/scripts/tour_purchase_review.py`가 없으면 자연어 판정으로 우회하지 말고 plugin source가 불완전하다고 알린다.
4. 새 후보 또는 URL 검토인데 MyRealTrip MCP 도구를 발견할 수 없으면 도구가 있다고 가장하지 않는다. URL·사용자 제공 본문 보완 경로는 유지하되 live 후보 검색·날짜 option 확인을 완료했다고 말하지 않는다.
5. 기존 review 상태가 있으면 먼저 `show`로 검증한다. schema `1.1`이면 그 파일을 그대로 사용한다. schema `1.0` 상태는 이 source에서 reload하거나 migration하지 않는다. `UNSUPPORTED_SCHEMA_VERSION`을 그대로 알리고 원본 파일을 바꾸지 않은 채, compatible `0.1.x` source로 읽을지 새 `1.1` review를 만들지 사용자에게 선택을 요청한다.
6. 새 review라면 작업을 방해하지 않는 임시 디렉터리에 acquisition bundle·selection·상태 파일을 만들고, 답변이 이어질 수 있게 상태 경로와 `review_id`를 알려 준다.

## 1. 사용자 장면에 맞춰 live 후보를 좁힌다

### 아직 상품을 고르지 않은 경우

1. 목적지, 절대 날짜, 실제 일행 수와 사용자가 알고 있는 연령 구분, 필요한 pickup 위치, 포기할 수 없는 조건, 원하는 경험을 확보한다. option 확인에 필요하지 않은 개인정보는 받지 않는다.
2. 상대 날짜를 절대 날짜로 바꿔야 할 때는 `getCurrentTime`을 먼저 사용한다. 사용자가 정한 날짜를 임의의 기본 날짜로 바꾸지 않는다.
3. 도시 category로 좁혀야 할 때만 `getCategoryList`를 호출하고 실제 `value`를 `searchTnas`에 전달한다. category 값을 추측하지 않는다.
4. `searchTnas`로 후보를 찾는다. 요청한 `perPage`, widget에 실제 담긴 수, 복사용 요약 수가 다를 수 있으므로 전체 결과를 평가했다거나 검색 상위가 사용자 최적 순위라고 말하지 않는다.
5. 제목·URL·검색 시작가만으로 결론을 내리지 않는다. 사용자 조건과 관련성이 있는 소수 상품을 골라 `getTnaDetail`과 정확한 날짜의 `getTnaOptions`를 호출한다. 결과 첫 화면에는 최대 3개만 남기고, 그보다 적다면 option 없음·명시 충돌·근거 부족 이유를 말한다.

### 이미 상품 URL을 가진 경우

1. URL을 사용자가 고른 정상 진입으로 존중한다. search-first보다 낮은 경로로 취급하거나 검색을 억지로 다시 시키지 않는다.
2. URL에서 product ID를 임의로 만들지 않는다. 알려진 MyRealTrip URL 형식의 gid를 확인하고, `getTnaDetail`과 정확한 날짜의 `getTnaOptions` request·response가 같은 gid인지 검증한다.
3. MCP 상세가 잘리거나 필드가 없으면 같은 상품의 공개 URL·사용자 제공 본문으로 필요한 구역을 보완한다. URL·본문 보완은 MCP를 깎아내리는 대체물이 아니라 현재 후보의 누락을 메우는 근거다.
4. 현재 bundled canonical acquisition compiler는 search-first receipt join만 지원한다. URL-first에서는 검색 응답을 만들어 넣지 말고, 실제 detail·option request·response와 확인 시각을 review provenance에 보존한 뒤 기존 `start-review`로 단일 상품 검토를 시작한다. 이 경로를 live 검색 후보 검증까지 끝난 것처럼 표현하지 않는다.

### raw receipt를 보존하고 후보를 판정한다

1. 각 MCP 호출의 tool 이름, 실제 request args, 시작·완료 시각, 성공·실패, 원래 `CallToolResult`를 `<ACQUISITION_JSON>`에 그대로 보존한다. 보기 좋은 요약만 옮기거나 raw text를 다시 작성하지 않는다.
2. search-first에서는 다음 명령으로 raw에서 canonical candidate를 재계산한다.

```bash
python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py validate-acquisition \
  --bundle <ACQUISITION_JSON>
```

3. 같은 bundle의 기본 사용자 화면은 다음 명령으로 만든다. 이 출력에 사용자 원문의 필수 조건·원하는 경험과 detail 근거의 대조를 덧붙이되, 내부 ID를 다시 전면에 꺼내지 않는다.

```bash
python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py show-shortlist \
  --bundle <ACQUISITION_JSON>
```

4. 후보마다 다음 세 구역을 근거와 함께 만든다.
   - `확인된 적합`: 현재 응답에 직접 있는 option·포함·조건이 사용자 요구와 정확히 맞는 범위
   - `명시적 충돌`: 날짜 option 없음, 최소 인원 미달, option의 보고 구매 가능 수량 0, 사용자가 밝힌 성인·아동 구분과 option 참가자 구분의 직접 충돌, 응답에 명시된 제한과 사용자 필수 조건의 직접 충돌
   - `결제 전 확인 필요`: 데이터가 없거나 잘렸거나, 판매자·공식 권위·checkout만 답할 수 있는 범위
5. 필드가 없으면 허용으로 바꾸지 않는다. detail 최상단 title을 상품명·기본 option으로 쓰지 않고, 상세 본문이 비면 검색 제목을 완전한 상품 근거로 승격하지 않는다. `availablePurchaseQuantity=999`를 좌석 999개나 예약 확정으로 표현하지 않고, `availablePurchaseQuantity=0`인 option은 선택 가능하게 보여 주지 않는다. 잘린 취소 정책을 전체 규정으로 쓰지 않는다.
6. 검색 시작가, 날짜별 option 단가, `단가 × 수량`의 단순 계산, checkout 최종 합계를 서로 다른 값으로 표시한다. option 단가의 과금 단위를 응답이 닫지 않으면 총액을 확정하지 않는다.
7. 첫 결과는 상품 목록 요약이 아니라 사용자가 지금 할 행동 하나와 최대 3개 추가 검토 후보다. 사용자에게 `더 검토 / 보류 / 제외`를 묻고, 내부 product ID·option ID·bundle path는 요청하거나 오류를 진단할 때만 보여 준다.

## 2. 선택 후보의 검토 시작 입력을 확보한다

1. 선택한 candidate·option과 acquisition provenance를 사용한다. MCP를 사용할 수 없어 URL·사용자 제공 본문으로만 진행한다면 접근한 구역과 확인하지 못한 live 범위를 분리한다.
2. 상품 사실마다 원문, MCP call 참조, URL 또는 사용자 제공 본문 참조, 확인 시각을 보존한다. 원문에 없다는 사실을 허용·금지·확정으로 바꾸지 않는다.
3. 상품·날짜·참가자·선택 option을 하나의 적용 범위로 고정한다. 다른 날짜·인원·option으로 자동 확대하지 않는다.
4. 사용자가 이미 아는 개인 조건과 원하는 경험을 서로 다른 입력 배열로 보존한다. 발화 excerpt와 turn 참조를 뜻이 바뀌지 않게 남긴다.
5. fixture나 과거 snapshot을 현재 판매 상태나 실제 사용자 입력이라고 표현하지 않는다.

## 3. 개인 조건, 직접 원하는 요구, AI 해석 후보를 분리한다

### 개인 조건

- 사용자가 이미 아는 인원·체력·동행·일정·이동 보조 조건에서 출발한다.
- 상품 근거로 닫히는지, 판매자가 예외를 답할 수 있는지, 다른 공식 권위가 답해야 하는지 구분한다.
- 원하는 경험에서 만든 운영 조건을 개인 조건의 직접 근거로 붙이지 않는다.

### 원하는 경험에 이미 명시된 직접 요구

- 사용자가 말한 원하는 경험 자체가 상품 근거나 판매자 답변으로 확인 가능한 요구이고 새 수치·운영 기준·해석을 만들 필요가 없으면 `direct_requirement`으로 보존한다.
- condition 문구를 원하는 경험 원문 그대로 유지하고, `direct_requirement.statement/provenance`도 참조한 `desired_experiences[]`의 값과 정확히 같게 복사한다. 문구를 바꾸거나 새 기준을 더해야 하면 direct 경로를 쓰지 않는다.
- 상품 snapshot이 원문 요구를 닫으면 `satisfied` condition과 근거를 decision card에 바로 보여 준다. 판매자가 확인해야 하면 AI condition 승인 없이 질문 승인 단계로 가지만, 질문 자체의 사용자 승인은 생략하지 않는다.
- 하나의 원문이 `풀코스와 영어 인솔`처럼 중요도가 다른 요구를 접속한 경우, 원문을 고치지 않고 각 접속항만 그대로 분리하는 lossless conjunct split을 사용할 수 있다. 각 split은 별도 `desired_experiences[]`와 direct condition을 만들고 같은 원문 provenance를 보존한다.
- `purchase_critical`은 split마다 사용자의 전환 기준으로 따로 정한다. 원하는 경험이라는 이유로 모두 `true`로 올리지 않는다. 풀코스 불충족 시 다른 상품을 검토하지만 영어 인솔은 선호라면 각각 `true`, `false`다. 중요도가 확인되지 않으면 critical로 승격하지 말고 사용자에게 확인한다.

### 원하는 경험에서 나온 운영 조건 후보

- `충분히 머물고 싶다`, `혼자 길을 찾고 싶지 않다` 같은 표현을 판매자가 답할 수 있는 체류 시간·이동 방식·가이드 동행 후보로 풀 수 있다.
- 원래 발화, AI가 제안한 조건, 제안 이유를 각각 남긴다.
- 사용자가 말하지 않은 `최소 90분` 같은 수치나 경계값을 권장 기본값, 상품 사실, 승인 전 active purchase-critical 조건으로 표현하지 않는다. immutable start input에는 승인될 경우의 proposed `purchase_critical` 값을 넣을 수 있지만, current projection은 승인 전 이를 항상 비활성화한다.
- AI 제안은 immutable input의 audit 후보다. 사용자가 확인하기 전에는 active condition이나 판매자에게 보낼 질문이 아니다.

원하는 경험 원문을 그대로 condition으로 쓸 수 있는지 먼저 확인한다. 그대로 쓸 수 있으면 direct, 수치·경계·운영 해석을 새로 더해야 하면 AI-derived로 분류한다. 단지 approval gate를 피하려고 AI 해석을 원하는 경험 원문처럼 다시 쓰지 않는다.

각 condition에 origin, 상품 근거 또는 근거 없음, 답할 권위, 정확한 범위, 결제 중요도와 초기 상태를 붙인다. 상태는 `satisfied / unsatisfied / needs_seller / needs_other_authority / indeterminate`만 사용한다.

## 4. draft review를 저장한다

`purchase_critical + needs_seller + seller authority`인 조건마다 하나의 draft question을 만든다. 이 draft는 전송 문구가 아니다. AI 도출 조건의 질문은 condition 승인 전까지 blocked이고, 직접 요구의 질문은 condition별로 질문 승인 가능 상태가 되지만 둘 다 질문 승인 전에는 전송할 수 없다. 한 review에 AI 도출 조건이 함께 있으면 전체 phase와 `approve-questions` 명령은 모든 AI 도출 조건 결정을 먼저 기다린다. Direct condition 자체를 AI approval payload에 넣는 것은 아니다.

AI 도출 condition의 승인 전·reject 후 current projection에는 원 evidence나 missing evidence를 복사하지 않는다. `authority: unknown`, `initial_status/current_status: indeterminate`, `purchase_critical: false`만 두고 원 제안·근거·상태는 immutable `review_input`에서만 audit한다. approve/revise 뒤에는 원 input에서 evidence와 상태를 다시 투영한다.

search-first MCP acquisition에서 선택한 후보라면 agent가 해석한 조건·질문을 `<SELECTION_JSON>`의 `review_input`에 넣고 다음 명령을 사용한다. 사용자가 scope·product snapshot을 직접 만들게 하지 않는다.

```bash
python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py start-review-from-acquisition \
  --bundle <ACQUISITION_JSON> \
  --selection <SELECTION_JSON> \
  --state <STATE_JSON>
```

현재 source에서 URL-first로 들어온 경우, 또는 MCP를 사용할 수 없어 사용자가 제공한 URL 본문으로 검토 범위를 명시적으로 제한한 경우에는 기존 `start-review --input <START_JSON>` 경로를 사용한다. URL-first에서도 사용할 수 있는 detail·option MCP는 먼저 활용하고 provenance에 남기되, deterministic search-first acquisition 검증을 통과한 것처럼 표현하지 않는다.

검증이 실패하면 자연어 결론으로 우회하지 말고 provenance와 구조를 고친다. 다음 명령으로 현재 card를 읽는다.

```bash
python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py show-card --state <STATE_JSON>
```

Card에는 근거로 닫힌 직접 원하는 요구를 확인된 근거에 보여 준다. AI 해석 후보가 있으면 정성적 사용자 원문과 “사용자가 기준을 정해야 함”을 먼저 보여 주고, 승인 전 AI 수치 제안이나 draft를 판매자에게 보낼 질문으로 보여 주지 않는다.

## 5. AI 도출 조건을 사용자에게 확인한다

1. 원하는 경험 원문, AI가 그렇게 해석한 이유, 상품 근거 유무를 보여 준다.
2. 사용자가 각 후보를 `approve / revise / reject`할 때까지 질문 승인으로 넘어가지 않는다.
3. `revise`이면 사용자가 정한 조건 문구와 그 조건을 묻는 질문 본문을 함께 기록한다.
4. 사용자가 정하지 않은 수치를 선택지의 기본값처럼 밀지 않는다. 먼저 정성적 원문에서 필요한 확인 기준을 묻는다.
5. 현재 `state_revision`을 expected revision으로 사용한다.

```bash
python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py approve-derived-conditions \
  --state <STATE_JSON> \
  --approval <DERIVED_APPROVAL_JSON> \
  --expected-revision <STATE_REVISION>
```

승인 뒤 active condition의 provenance가 사용자 approval을 가리키는지, 원 AI 제안이 `review_input`과 history에만 남는지 확인한다. `reject`한 후보의 질문은 `not_applicable`이어야 한다.

## 6. 판매자 질문을 승인한다

1. `show-card`로 현재 판단, 남은 조건, 승인 가능한 질문, 답변별 다음 판단을 보여 준다.
2. 사용자가 각 질문을 승인·수정·삭제할 때까지 답변 적용으로 넘어가지 않는다.
3. 사용자의 결정만 approval payload에 기록한다.

```bash
python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py approve-questions \
  --state <STATE_JSON> \
  --approval <QUESTION_APPROVAL_JSON> \
  --expected-revision <STATE_REVISION>
```

실제로 복사해 보낼 문구는 `approved_text`가 아니라 `seller_message`다. `seller_message`에는 질문마다 판매자가 이해할 상품명·날짜·인원 수·옵션을 붙인다. 내부 product ID·participant ID는 scope 검증에는 보존하되 판매자용 문구에 노출하지 않는다. 삭제·reject된 질문을 보냈다고 말하지 않는다. plugin은 메시지를 전송하지 않는다.

## 7. 판매자 답변을 claim별로 적용한다

1. 사용자가 붙인 답변 원문 전체와 source turn을 보존한다. 실제 답변과 fixture를 구분한다.
2. 문장에 없는 상품·날짜·참가자·옵션 범위를 대화 분위기로 채우지 않는다.
3. 답변을 조건별 claim으로 나누고 `satisfied / unsatisfied / unresolved`를 기록한다.
4. 현재 revision을 기준으로 답변을 적용한다.

```bash
python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py apply-seller-reply \
  --state <STATE_JSON> \
  --reply <REPLY_JSON> \
  --expected-revision <STATE_REVISION>
```

수용된 claim만 조건을 바꾼다. 부분 답변은 나머지를 열어 두고, 상반 답변은 `conflict`, 범위 부족은 거부 기록으로 남긴다. 같은 reply ID와 payload를 다시 적용해도 새 event가 생기지 않아야 한다.

## 결과를 decision card로 설명한다

각 상태 변화 뒤 `show-card`를 실행하고 다음 구역을 그대로 기준으로 설명한다.

1. 현재 판단과 판단 이유
2. 확인된 상품 근거와 수용된 판매자 claim
3. 남은 미확정
4. 판매자에게 보낼 승인 완료 질문 중 아직 닫히지 않은 것
5. 답변별 다음 판단
6. 판매자 답변 적용 전후의 판단·조건 변화
7. 현재 한계

`review_id`, revision, 상태 파일 경로는 대화를 이어 가는 데 필요할 때 host가 보존하며, 기본 사용자 결과의 중심에 두지 않는다. 사용자가 요청하거나 오류를 진단할 때만 알려 준다. `buy`는 현재 범위에서 결제를 검토할 수 있다는 추천일 뿐 재고·예약·결제·판매자 이행·현장 품질을 보장하지 않는다. 최종 선택은 사용자가 한다.

## 실패와 범위를 숨기지 않는다

- 상품 근거가 부족하면 미확정으로 남기고 필요한 본문 범위를 요청한다.
- 판매자 권위 밖의 공식 규정은 판매자 질문으로 만들지 않는다.
- 실제 답변이 없으면 fixture를 판매자 발화로 바꾸지 않는다.
- state validation, stale revision, 승인 미완료, claim scope 오류가 나면 기존 상태가 유지됐는지 알리고 입력을 교정한다.
- `UNSUPPORTED_SCHEMA_VERSION`이면 schema `1.0` payload나 persisted state를 `1.1`로 추정·변환하지 않는다. compatible source 사용 또는 새 review 생성 경로를 안내한다.
- 자동 예약·결제·메시지 전송, 의료·안전 적합성, 환불 결과, 현장 품질 보장을 요청받으면 판정 범위를 설명하고 공식 확인 경로로 넘긴다.
