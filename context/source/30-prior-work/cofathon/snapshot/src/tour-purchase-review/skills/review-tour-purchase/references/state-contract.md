# 저장 상태와 CLI 계약

schema `1.1`에서 Codex가 자연어와 검증된 상품 근거를 구조화하고, Python은 그 의미를 다시 추정하지 않는다. MyRealTrip MCP를 쓴 새 review는 [acquisition 계약](./acquisition-contract.md)이 product·URL·날짜·option·가격·말줄임 경계를 먼저 고정한다. 이후 Python의 책임은 source-bound scope와 product snapshot, AI 도출 조건의 사용자 승인, 질문 맥락·승인, 답변 claim scope, 상태 전이, 사람이 읽는 decision card, revision과 원자 저장이다.

## Version compatibility

현재 plugin source는 schema `1.1` payload와 persisted state만 읽는다. source `0.1.x`가 만든 schema `1.0` state의 migration은 제공하지 않으며, `show`, `show-card`, 모든 변경 명령에서 `UNSUPPORTED_SCHEMA_VERSION`으로 거부한다. 오류는 받은 version, 필요한 `1.1`, 자동 migration이 없다는 사실, compatible `0.1.x` source로 원본을 읽거나 새 `1.1` review를 만들어야 한다는 경로를 함께 말한다.

schema `1.0` 원본을 `1.1`로 추정해 고쳐 쓰지 않는다. 오류가 나면 기존 state 파일을 그대로 보존한다.

## CLI

`<PLUGIN_ROOT>`는 `SKILL.md`가 있는 디렉터리의 두 단계 위다.

```bash
python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py validate-acquisition \
  --bundle <ACQUISITION_JSON>

python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py start-review-from-acquisition \
  --bundle <ACQUISITION_JSON> \
  --selection <SELECTION_JSON> \
  --state <STATE_JSON>

python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py start-review \
  --input <START_JSON> \
  --state <STATE_JSON>

python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py approve-derived-conditions \
  --state <STATE_JSON> \
  --approval <DERIVED_APPROVAL_JSON> \
  --expected-revision <REVISION>

python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py approve-questions \
  --state <STATE_JSON> \
  --approval <QUESTION_APPROVAL_JSON> \
  --expected-revision <REVISION>

python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py apply-seller-reply \
  --state <STATE_JSON> \
  --reply <REPLY_JSON> \
  --expected-revision <REVISION>

python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py show --state <STATE_JSON>
python3 <PLUGIN_ROOT>/scripts/tour_purchase_review.py show-card --state <STATE_JSON>
```

- `show-card` 성공 시 stdout에 Markdown decision card를 출력한다. 다른 명령은 전체 상태 JSON을 출력한다.
- 계약·revision·저장 오류는 stderr에 `error.code`, `error.message`, 필요하면 `error.path`가 있는 JSON으로 출력하고 0이 아닌 코드로 종료한다.
- schema `1.0` payload나 state는 `error.code: UNSUPPORTED_SCHEMA_VERSION`과 해당 `schema_version` path로 실패한다.
- `start-review`는 이미 있는 상태 파일을 덮어쓰지 않는다.
- 변경 명령은 lock 안에서 현재 상태를 다시 읽고 검증한 뒤 sibling 임시 파일과 `os.replace`로 저장한다.

## `start-review` 입력

필수 top-level 필드는 다음과 같다.

- `schema_version`: `1.1`
- `review_id`, `recorded_at`
- fixture일 때 `fixture_notice`
- `scope`, `product_snapshot`
- `personal_conditions`, `desired_experiences`
- `conditions`, `questions`

### 적용 범위

`scope`는 `product_id`, `date`, 중복 없는 비어 있지 않은 `participant_ids`, `option`을 가진다. 상품, condition, question, reply와 claim은 이 범위를 그대로 사용한다. 일부 범위나 다른 옵션을 같은 검토로 자동 확대하지 않는다.

### 상품 snapshot과 사용자 입력 provenance

`product_snapshot`에는 `product_id`, `title`, `snapshot`, `provenance`가 필요하다. `snapshot`은 `source_url`, `accessed_at`, `source_reference`, 하나 이상의 원문 `excerpts[].text`를 보존한다. 과거 자료와 fixture를 현재 라이브 상품 사실로 승격하지 않는다.

`personal_conditions[]`는 `personal_condition_id`, `statement`, 사용자 발화의 `provenance.kind/source_ref/excerpt`를 가진다. `desired_experiences[]`는 여기에 `desired_experience_id`와 `non_negotiable_reason`을 더 가진다.

### Condition 입력과 원하는 경험의 두 경로

각 `conditions[]`에는 다음이 필요하다.

- 고유 `condition_id`, 확인 가능한 `statement`
- `origin`, `authority`
- 정확히 하나의 `evidence` 또는 `missing_evidence`
- review와 같은 `scope`
- strict boolean `purchase_critical`
- 같은 값의 최초 `initial_status`, `current_status`

`origin.kind: personal_condition`은 실제 개인 조건을 가리킨다. `origin.kind: desired_experience`은 다음 관계 중 정확히 하나를 가져야 한다.

- `direct_requirement`: 사용자가 이미 명시한 원하는 경험 자체가 확인 가능한 요구이고 AI가 새 기준을 만들지 않은 경우
- `derived_operating_condition`: 정성적 경험에서 AI가 새 수치·경계·운영 해석을 만든 경우

`direct_requirement`은 다음 모양이다.

```json
{
  "kind": "desired_experience",
  "source_id": "desired-full-course-english-guide",
  "direct_requirement": {
    "statement": "상품에 적힌 가와산 풀코스와 캐녀닝 구간 영어 인솔을 원한다.",
    "provenance": {
      "kind": "controlled_scenario_operator_input",
      "source_ref": "원 사용자 입력 참조",
      "excerpt": "원 사용자 발화 발췌"
    }
  }
}
```

direct condition의 `statement`와 `direct_requirement.statement`은 참조한 `desired_experiences[].statement`와 정확히 같아야 한다. `direct_requirement.provenance`도 참조한 provenance 전체와 정확히 같아야 한다. 두 관계를 함께 넣거나 둘 다 생략하면 실패한다. 따라서 `derived_operating_condition`만 지워 approval gate를 우회할 수 없다.

하나의 사용자 원문이 중요도가 다른 여러 접속항을 담으면 structured input에서 lossless conjunct split을 할 수 있다. 원문 파일이나 provenance excerpt는 바꾸지 않고, 새 수치·수식어·기준을 만들지 않은 각 접속항을 별도 `desired_experiences[]` statement로 둔다. 각 direct condition은 자신의 split desired statement/provenance와 위 규칙대로 정확히 일치해야 한다. 여러 split이 같은 원문 provenance를 공유할 수 있다.

`purchase_critical`은 split condition마다 독립적으로 정한다. `origin.kind: desired_experience`이거나 `non_negotiable_reason` 필드가 있다는 사실만으로 `true`가 되지 않는다. 필수가 아닌 선호라면 해당 reason에 그 경계를 적고 condition은 `purchase_critical: false`로 둔다. 예를 들어 풀코스 불충족은 다른 상품 전환 기준이지만 영어 인솔은 단순 선호라면 각각 `true`, `false`다.

Validator의 trust boundary는 내부 상대 일관성이다. direct condition과 desired statement/provenance의 정확 일치, scope, evidence 구조, replay projection은 검사하지만 다음은 보장하지 않는다.

- split이 외부 원문의 의미를 실제로 lossless하게 보존했는지
- provenance excerpt와 외부 원문이 진짜인지
- evidence가 외부 상품 사실을 정확히 옮겼는지
- `purchase_critical`이 사용자의 실제 중요도와 맞는지

이 의미 판단과 외부 진위 확인은 caller가 원문을 보존해 수행하고, 결제 중요도는 사용자가 확인한다.

direct condition은 별도 AI condition 승인을 요구하지 않는다. 상품 근거로 닫히면 `satisfied`와 evidence가 current state와 decision card에 바로 나타난다. `needs_seller`이면 해당 question의 approval projection은 `pending`이 되지만 질문 승인과 답변 범위 제한은 그대로 적용된다.

AI가 만든 수치·운영 조건은 시작 입력의 audit 제안일 뿐 기본값이나 상품 사실이 아니다. 승인 전과 reject 후 current condition은 다음 neutral projection만 가진다.

- `statement`: 참조한 정성적 `desired_experiences[].statement`
- `purchase_critical: false`
- `authority: unknown`
- `initial_status: indeterminate`, `current_status: indeterminate`
- `evidence`와 `missing_evidence` 없음
- immutable `review_input.conditions[]`을 가리키는 audit ref와 confirmation 상태

따라서 원 AI statement, evidence/missing evidence, authority, satisfied/unsatisfied/needs_seller 상태는 immutable `review_input` 밖의 current projection과 decision card에 나타나지 않으며 다음에도 들어가지 않는다.

- active purchase-critical condition 계산
- 판매자에게 전송 가능한 질문
- seller reply가 닫을 수 있는 condition 범위

immutable `review_input.conditions[]`에는 승인될 경우 사용할 proposed `purchase_critical`, authority, evidence 또는 missing evidence, initial/current status가 필요하다. 승인 또는 revise 뒤에는 이 immutable input에서 evidence와 상태를 다시 투영하고 승인된 statement를 적용한다. 승인 전에는 위 neutral projection만 사용한다.

원래 AI 제안과 draft question은 immutable `review_input`에서만 다시 볼 수 있다. 이 neutral projection은 기존 schema `1.1`의 `unknown / indeterminate` enum과 optional current evidence 필드를 사용하므로 schema bump가 없다. 이전 source가 만든 unneutralized schema `1.1` state는 current fields가 immutable input과 정확히 같을 때만 legacy replay로 읽고, 파일을 조용히 수정하지 않은 채 `show`와 이후 동작에는 canonical neutral projection을 반환한다.

`authority`는 `seller / product_snapshot / official_source / field_quality / unknown` 중 하나다. 최초 상태는 `satisfied / unsatisfied / needs_seller / needs_other_authority / indeterminate`이며 답변 적용 뒤 `conflict`가 추가될 수 있다.

## AI 도출 조건 승인

`derived_operating_condition`이 하나라도 있으면 시작 phase는 `derived_condition_approval_pending`이다. 이때 direct condition과 그 question projection은 각각 `confirmation: not_required`, `approval: pending`일 수 있지만, 전역 `approve-questions` 명령은 AI 도출 조건 결정이 끝날 때까지 거부한다. AI condition approval payload는 direct condition을 포함하지 않는다.

AI-derived condition이 없으면 `derived_condition_approval.status`는 `not_required`이고 시작 phase는 `question_approval_pending`이다. 모든 direct condition이 이미 근거로 닫혀 question이 0개여도 같은 phase이며, 빈 `decisions[]` question approval을 기록하면 `question_approval_completed_no_active_question`으로 간다. approval payload는 다음을 가진다.

- `schema_version: 1.1`
- 고유 `approval_id`, `recorded_at`
- 모든 AI 도출 condition을 정확히 한 번 결정하는 `decisions[]`

각 decision은 `condition_id`와 다음 action 중 하나를 가진다.

- `approve`: 제안을 사용자가 그대로 승인
- `revise`: `revised_statement`와 seller question이 있는 조건의 `revised_question_text` 필수
- `reject`: 비어 있지 않은 `reason` 필수

`revise` 뒤 current condition의 statement와 `origin.derived_operating_condition.statement`은 사용자 수정 문구가 된다. `origin.approval_provenance`와 `confirmation.provenance`는 approval ID, 시각, action, 원본 proposal의 audit 경로를 보존한다. 원래 AI 제안은 `review_input`과 approval history에만 남는다.

`reject`는 해당 조건을 위 neutral projection으로 되돌려 현재 판단에서 제외하고 대응 질문을 `not_applicable`로 만든다. 승인 전 질문 승인이나 판매자 답변 적용은 거부한다.

## Question과 판매자 메시지

입력 question은 `question_id`, `condition_id`, 같은 scope, draft `text`, `conditional_branches`를 가진다. `purchase_critical + needs_seller + seller authority`인 조건마다 정확히 한 질문이 있어야 한다.

current state는 draft 원문 대신 `draft_audit_ref`를 보존한다. AI 도출 조건은 condition 승인 뒤, direct condition은 시작 직후 `reviewed_text`가 생긴다. 어느 경로든 질문 승인 전까지 `seller_message`는 `null`이다.

질문 approval은 모든 현재 승인 가능 질문을 `approve / revise / delete` 중 하나로 정확히 한 번 결정한다. 활성 질문의 `seller_message`는 승인된 본문 앞에 판매자가 이해할 다음 맥락을 결정적으로 붙인다.

- 상품명
- 날짜
- 인원 수
- 옵션

product ID와 participant ID는 내부 scope 검증에만 보존하고 판매자용 문구에는 넣지 않는다. 사용자가 본문을 수정해도 사용자용 맥락은 제거되지 않는다. 실제로 판매자에게 보여 줄 문구는 `approved_text`가 아니라 `seller_message`다.

각 질문의 세 branch는 다음과 같다.

- `satisfied` → condition `satisfied`, 전체 판단 재계산
- `unsatisfied` → condition `unsatisfied`, `consider_another_product`
- `unresolved` → condition `needs_seller`, `hold`

## 판매자 답변

reply payload는 `schema_version: 1.1`, 고유 `reply_id`, `source_kind`, `received_at`, review와 같은 `scope`, 원문 전체 `provenance.raw_text`, `claims[]`를 가진다. fixture이면 `fixture_notice`가 필요하다.

각 claim은 `claim_id`, 활성 질문이 덮는 `condition_id`, `satisfied / unsatisfied / unresolved` status, 원문에서 뽑은 `statement`, review와 같은 scope를 가진다.

reply와 claim scope를 각각 검사한다. 범위가 없거나 다르면 claim을 거부하고 조건을 닫지 않는다. 같은 condition에 수용된 `satisfied`와 `unsatisfied`가 함께 있으면 최신 답을 고르지 않고 `conflict`로 만든다. `unresolved` claim은 audit에 남지만 조건을 닫지 않는다.

## Decision card

`show-card`는 검증된 state에서만 다음 Markdown 구역을 파생한다.

1. 현재 판단
2. 판단 이유
3. 확인된 근거
4. 남은 미확정
5. 판매자에게 보낼 질문
6. 답변별 다음 판단
7. 판매자 답변 적용 전후
8. 현재 한계

승인 전에는 정성적 원하는 경험과 “사용자가 기준을 정해야 함”을 먼저 보여 주며 AI의 수치 제안을 card에 노출하지 않는다. 판매자 답변 전후는 마지막 `seller_reply_applied` history의 decision, condition change, claim audit에서만 만든다.
답변 적용 뒤 “판매자에게 보낼 질문”에는 `needs_seller` 또는 `conflict`로 남은 조건의 질문만 표시한다. 이미 `satisfied`나 `unsatisfied`로 닫힌 질문을 다시 보낼 대상으로 보여 주지 않는다.

## 판단 우선순위

사용자가 확정한 active condition에만 purchase-critical 우선순위를 적용한다.

1. active 결제 중요 `unsatisfied`가 하나라도 있으면 `consider_another_product`
2. 그렇지 않고 AI 도출 기준을 사용자가 아직 정하지 않았으면 `hold`
3. 그렇지 않고 active 결제 중요 `conflict / needs_seller / needs_other_authority / indeterminate`가 있으면 `hold`
4. 모든 active 결제 중요 condition이 `satisfied`일 때만 `buy`

모든 decision은 `requires_human_confirmation: true`다. `buy`는 현재 저장된 조건 범위에서 결제를 검토할 수 있다는 추천이며 재고·예약·결제·판매자 이행·현장 품질을 확정하지 않는다.

## Revision, idempotency와 reload

- AI 조건 승인, 질문 승인, 답변 적용은 현재 `state_revision`을 받는다.
- 오래된 revision이면 상태를 바꾸지 않고 `REVISION_CONFLICT`로 실패한다.
- 같은 approval/reply ID와 같은 canonical payload는 no-op, 다른 payload는 `IDEMPOTENCY_KEY_REUSE`다.
- 검증·승인·scope·revision 오류가 나면 기존 상태를 유지한다.

Reload 때 immutable `review_input`, raw AI 조건 approval, raw question approval, raw replies에서 다음을 전부 다시 만든다.

- 사용자 승인 provenance와 active/rejected condition projection
- 질문 reviewed text, 고정 context, seller message와 active/deleted/not-applicable 상태
- claim audit, current condition status와 decision
- phase, revision, condition/decision 전후와 append-only history

저장값이 projection과 다르면 `show`, `show-card`, 모든 변경 명령이 상태를 거부한다. 이는 JSON 내부의 반복 가능성과 상대적 무결성을 보장하지만 외부 원문의 진위를 인증하지 않는다.

검증용 전체 예시는 `<PLUGIN_ROOT>/fixtures/loop-01/`에 있다. 그 파일들은 현재 라이브 상품·실제 여행자·실제 판매자 답변 증거가 아니다.
