# 구조화 상태 계약

사용자가 아니라 Codex가 자연어와 도구 결과를 이 계약으로 바꾼다. Python은 자연어 의미를 해석하지 않고 이 구조의 provenance, 허용 수정, claim scope와 상태 전이만 검증한다.

## CLI 계약

`<PLUGIN_ROOT>`는 현재 skill 디렉터리의 두 단계 위다. working id나 호출한 셸의 현재 디렉터리에 기대지 말고 이 실제 경로를 사용한다.

```bash
python3 <PLUGIN_ROOT>/scripts/tripproof.py evaluate \
  --case <CASE_JSON> \
  --plan <PLAN_ID>

python3 <PLUGIN_ROOT>/scripts/tripproof.py evaluate \
  --case <CASE_JSON> \
  --plan <PLAN_ID> \
  --reply <REPLY_JSON> \
  --include-reply-decisions

python3 <PLUGIN_ROOT>/scripts/tripproof.py compare \
  --case <CASE_JSON> \
  --before-plan <BEFORE_PLAN_ID> \
  --after-plan <AFTER_PLAN_ID> \
  [--after-reply <REPLY_JSON>]
```

- `evaluate`는 검증된 현재 snapshot을 JSON으로 출력한다. `--reply`가 있으면 답변을 적용한 snapshot을 출력하고, `--include-reply-decisions`가 있으면 claim별 `accepted`/`rejected`와 거부 이유도 포함한다. 적용 전후 `decision_diff`가 필요하면 `compare`를 사용한다.
- `compare`는 두 snapshot과 안정적인 `decision_diff`를 JSON으로 출력한다. 같은 plan을 before·after에 두고 `--after-reply`만 지정하면 답변 전후 비교가 된다.
- 범위가 부족한 답변은 audit에는 남아도 `decision_diff`를 만들지 않는다. 같은 충분 답변을 같은 base에 다시 적용한 snapshot과 diff는 같아야 한다.
- schema나 provenance가 잘못되면 0이 아닌 종료 코드로 실패해야 한다. Codex는 이 실패를 자연어 추정으로 우회하지 않고 payload를 고치거나 필요한 입력을 요청한다.
- stdout은 기계가 읽는 JSON에만 사용한다. 설명과 검증 오류는 stderr로 분리한다.

## Case의 필수 구성

- `schema_version`: 현재 `1.0`
- `case_id`: 대화 안에서 안정적인 식별자
- `product`: `product_id`, `name`, 공개 `url`
- `evidence_acquisition`: MCP·공개 URL·사용자 본문 시도 순서와 성공/실패 이유
- `public_facts`: 상품 사실 claim 배열
- `travel_party`: 사용자 일행 master 배열
- `requirements`: 사용자만 아는 필수 조건 배열
- `plans`: 원안과 사용자가 허용한 revision 배열
- `not_assessed`: 이 판정이 다루지 않는 영역

실제 필드 모양은 `fixtures/loop-01/case.json`을 복사해 값만 바꾸지 말고, 의미에 맞는 claim만 남겨 구성하라.

## Provenance 종류

- `public_fact`: 공개 URL 또는 MCP 결과. `source_url`, `retrieved_at`, `retrieval_path`, `evidence`를 기록한다.
- `user_input`: 사용자 발화. `source_ref`와 뜻을 바꾸지 않은 `excerpt`를 기록한다.
- `seller_reply`: 사용자가 붙여넣은 실제 답변. 답변 원문과 대화 turn을 reply에 보존한다.
- `seller_reply_fixture`: 자동 검증용 합성 답변. 실제 재고나 판매자 발화가 아니라는 `fixture_notice`가 필수다.
- `demo_assumption`: 시연을 위해 둔 가정. 공개 사실이나 사용자 입력으로 승격하지 않는다.

`public_fact`, `user_input`, `seller_reply`, `seller_reply_fixture`, `demo_assumption`을 서로 바꾸지 마라.

## Public fact 종류

Loop 01 고정층은 다음 claim을 판정에 사용한다.

- `stroller_allowed`: boolean
- `default_start_time`: `HH:MM`
- `alternate_start_requires_confirmation`: boolean
- `flat_group_price_through`: 1 이상 정수
- `minor_ticket_preparation`: `procedure`가 비어 있지 않은 object. 확인된 사용자 부담이 있으면 `burden` 문자열로 함께 보존한다.

claim이 없으면 허용이나 금지를 추정하지 않고 해당 셀을 `정보 부족`으로 둔다.

타입을 강제 변환하지 않는다. 문자열 `"false"`는 boolean이 아니고, `true`는 정수가 아니다. 발화에서 정확한 나이를 알 수 없으면 임의 숫자를 만들지 않고 `age: null`로 두며 `is_minor`는 strict boolean으로 보존한다. 날짜는 ISO `YYYY-MM-DD`, 시각은 24시간 `HH:MM`이어야 한다. participant·plan·claim ID는 비어 있지 않고 각 배열 안에서 고유해야 한다.

## Plan과 허용 변경

원안은 `kind: original`, revision은 `kind: revision`과 `base_plan_id`를 사용한다. Plan에는 `date`, `start_time`, `participant_ids`, `authorized_changes`, `provenance`가 필요하다.

revision에서 base와 다른 각 값은 `authorized_changes`에 정확한 `path`, `before`, `after`, `user_input` provenance로 있어야 한다. 고정층은 허용되지 않은 차이가 하나라도 있으면 실행을 거부한다. 현재 지원하는 변경 path는 `participant_ids`, `date`, `start_time`이다. schema `1.0`의 revision은 한 original plan을 직접 base로 삼아야 하며 자기 자신이나 다른 revision을 base로 삼지 않는다. plan 안의 participant ID도 중복할 수 없다.

사용자가 더 허용할 수정안이 없다고 명시한 revision만 `authorized_options_exhausted: true`를 사용할 수 있다. 이때 같은 사용자 발화의 `authorized_options_exhausted_provenance`가 필수다. boolean이 아니거나 출처가 없으면 `다른 상품 검토`로 이동하지 않는다.

## Seller reply claim scope

각 claim을 독립적으로 판정한다. Loop 01이 seller reply에서 지원하는 claim은 `start_time_approved` 하나다. 모든 claim에는 현재 plan과 일치하는 다음 공통 scope가 필요하다.

- `product_id`
- `date`
- `participants`: 순서는 무관하지만 구성은 정확히 일치

`start_time_approved`는 `scope.start_time`이 plan 시각과 같아야 하고 `value`는 boolean이어야 한다. 공통 scope가 충분해도 답변이 요청 시각을 말하지 않으면 claim을 거부한다. 같은 reply에 같은 범위의 중복 또는 상반 시간 claim이 있으면 배열 순서로 하나를 고르지 말고 계약 오류로 거부한다.

아동 티켓의 공개 절차는 seller claim으로 다시 열지 않는다. `minor_ticket_preparation` 공개 사실에서 `정상 + 준비 부담`으로 유지하며, 시간 답변이 이 셀을 바꾸지 않는다. 이 공개 fact가 없으면 상태는 `정보 부족`, decision variable은 `minor_ticket_public_fact`다. Codex는 판매자 claim을 만들지 않고 MCP·공개 URL·필요 본문으로 사실층을 다시 확보한다.

## 상태 관계

- 셀 하나라도 `충돌`이면 전체 `보류`다.
- 충돌이 없고 `정보 부족` 또는 `답변 대기`가 있으면 전체 `확인 후 진행`이다.
- 결정 셀이 모두 `정상`일 때만 전체 `진행 가능`이다.
- `진행 가능`은 확인된 조건 범위에서 결제를 검토할 수 있다는 뜻이다.

전체 `보류`라도 사용자가 허용할 수정 범위를 아직 확인할 수 있으면 다음 행동은 `추가 확인`이다. revision에 충돌이 남고 허용안이 끝났음을 구조에 표시하면 `다른 상품 검토`다. `진행 가능`의 다음 행동은 `결제 검토`다.

## 결정성과 diff

같은 case, plan, reply 배열에는 같은 snapshot과 diff가 나와야 한다. 자연어 설명 문장까지 동일할 필요는 없다. 부족한 reply는 판정 diff가 비어 있어야 하고, 같은 충분 reply를 다시 적용해도 snapshot이 바뀌지 않아야 한다.
