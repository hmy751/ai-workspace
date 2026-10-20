# 일반 본문 이동을 마치고 절차·관리 진입을 복구

후속 상태: Work에 형성 자료를 남긴 아래 복구 결과도 사용자가 다시 정정했다. 현재는 [116](2026-10-20-116-defer-work-content-policy.md)에 따라 Work의 이번 구성 적용 전체를 되돌리고 별도 논의로 유보한다. 아래는 그 전 진입 복구와 당시 확인 기록이다.

[114의 재적용](2026-10-20-114-durable-body-policy-and-reapplication.md) 결과를 본 사용자는 `management`와 `spec-and-tickets`가 합쳐진 이유, 옛 `code-readability.md`가 새 폴더와 함께 남은 이유를 물었다. 설명 뒤 일반 본문의 이동은 마무리하고, 기존 진입 문서의 재편은 되돌려 먼저 논의하라고 요청했다.

## 사용자 요청과 정정한 판단

> 일단 이렇게 하자 code-readability.md 이건 잘못됐다고 봐 저렇게 나눌거면 나눠야지 애매하게 돼서 어쨋든 본문 적용하자고 햇으니 적용하고 남은 저 파일은 없애는게 맞다고보고 이것도 정책 보완하야한다고 봐
>
> 그리고 진입 문서 성격있잖아? 기존에 DEVELPMENT 라던가 SPEC_AND-Tickets 뭐 이런 문서들 이걸 원복하고 논의 한다음에 작업하자

일반 본문에 폴더·본문·형성 자료 구성을 적용하는 방향은 유지한다. 옛 파일을 안내로만 남겨 읽는 위치가 모호해지는 상태를 정리한다. 반면 DEVELOPMENT·Spec·Ticket 작성 기준 등 이미 절차와 관리 기준의 진입점인 문서는 원래 위치에서 실제 내용을 소유하도록 복구하고, 통합·이름·위치 변경은 논의 뒤로 미룬다. 이를 지속 본문 전체의 적용 철회나 앞으로 모든 진입 문서를 변경할 때마다 승인받으라는 규칙으로 확대하지 않는다.

Main은 앞선 설명에서 옛 파일의 참조 유무를 확인했지만, 링크를 보존할 이유가 있다는 것과 현재 읽기 구조를 이렇게 유지해야 한다는 판단을 충분히 구별하지 못했다. 또한 워커의 관리 단위 선택을 검토 가능한 시안으로 보고하면서도, 미정인 진입 구조의 통합을 실제 읽기 경로에 먼저 반영했다.

## 실제 반영 범위

- Project의 `common/device-session.md`, `guidance/authentication-and-session.md`, `guidance/code-readability.md`, `current/authentication-flow.md` 옛 연결 파일을 제거했다. 실제 본문은 각각 같은 이름 폴더의 `index.md`가 계속 소유한다.
- Work의 `DEVELOPMENT.md`, `workspaces/spec-and-tickets/README.md`, `workspaces/README.md`, `AGENTS.md`를 재배치 전 `33c1fee`의 이름·위치·실질 책임으로 복구했다. 최신 일반 본문과 개별 작업의 Spec·Ticket 묶음을 가리키는 링크는 현재 위치에 맞췄다.
- 같은 성격의 Project `MAINTENANCE.md`, `REFERENCE/README.md`, `REFERENCE/reading.md`, `REFERENCE/composition.md`도 복구했다. 새 `project/management`, `work/management`, `work/development`의 본문·안내 중복을 없앴다.
- 수집한 형성 자료는 버리지 않았다. DEVELOPMENT 근거는 `work/background/development`, Spec·Ticket과 Workspace 관리 근거는 기존 `workspaces/spec-and-tickets/background`, Project 관리 근거는 기존 `REFERENCE/background`에서 찾게 했다. 이는 기존 진입을 유지하며 자료를 보존한 위치이며 최종 관리 구조의 확정이 아니다.
- Personal·일반 Project 본문과 실제 작업의 Spec·Ticket 구성, 제품 실행 코드·검사는 유지한다. 외부 원본 Noline이나 글로벌 하네스는 수정하지 않는다.

## 원자료 참조와 정책

가상 시작 입력 `scenario-input.md`에는 현재 Project 본문을 읽는 링크가 세 개 있었다. 초기 코드·가정·문구는 그대로 두고 이 세 링크의 목적지만 새 본문으로 바꿨다. 과거 판본의 링크를 현재 본문에 보내는 것을 당시 본문판 보존으로 표현하지 않는다. 루트 `context/source/`와014의 보존 source는 수정하지 않는다.

[CONTENT-POLICY](prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md)의 기존 적용 범위·구성·읽기·갱신·확인 절을 고쳤다. 일반 본문의 이동은 참조 갱신과 옛 파일 제거까지 끝내고, 이미 진입을 맡는 문서의 책임 재편은 형성 자료 보완과 구별한다. 현재 읽을 링크와 당시 원문판 출처를 구별해 다룬다. 이미 허용된 진입 변경에 반복 승인을 요구하지 않는 조건도 유지한다.

정책 자체의 [형성 맥락](prototypes/development-workflow/noline-demo/context/_background/content-policy/context.md#본문-이동을-마치는-것과-기존-진입을-바꾸는-것), [사용자 원문](prototypes/development-workflow/noline-demo/context/_background/content-policy/evidence.md#본문-이동의-완결과-진입-문서의-원복), [선택·정정 기록](prototypes/development-workflow/noline-demo/context/_background/content-policy/records/2026-10-20-entry-restoration-and-complete-moves.md)도 함께 갱신했다. 데모 안에서 핵심 이유와 근거를 읽을 수 있으며 이 바깥 기록을 필수 입력으로 삼지 않는다.

## 확인과 남은 논의

별도 검토자가 사용자 요청·정책·실제 문서와 `33c1fee`를 대조했다. 일반 규칙이 모든 진입 변경에 재논의를 요구하는 것으로 읽힐 수 있다는 지적은 작업 범위에 이미 포함된 변경과 이번 데모의 유보를 구별해 수정했다. 최종 검토에서 8개 진입 본문의 복구, 형성 자료12개 보존, 원문·해석·검증의 지위와 정책 일치를 확인했고 남은 필수 수정은 없다고 보고했다.

7개 복구 문서는 링크 외 기존 실질 문장을 유지했다. Spec·Ticket 작성 기준은 현재 실제 Spec의 `index.*` 파일명과 시작 본문 설명을 맞췄다. 형성 evidence3개는 이동 전 사본과 링크 외 내용이 같았다. [경로 매핑](receipts/entry-restoration-2026-10-20/paths.json)과 [실물·원자료 대조](receipts/entry-restoration-2026-10-20/result.json)를 보존한다. 초기 입력의 변경이 링크 목적지3개뿐이라는 것은 Main이 정확한 문자열 비교로 확인했다.

[표시 검사](receipts/entry-restoration-2026-10-20/viewer-check.json)는 현재 문서131개·코드5개의 원문·해시 일치, 내부 링크739개·앵커198개, 경로·절 누락0개를 확인했다. 모든 로컬 링크가 대상물 안에 있고 공백 검사도 통과했다. 제품 코드·테스트와 루트·014의 보존 source에는 변경이 없다. 브라우저 렌더링 실측과 제품 테스트 반복은 하지 않았다.

앞선114의 복사본 실험과 검사는 그 시점의 관찰로 보존하며, 이번 정정 뒤 구성까지 검증한 것으로 재사용하지 않는다.

다음 논의는 DEVELOPMENT와 Spec·Ticket 기준·Project 관리 진입이 맡는 범위, 유지할 이름·위치, 다른 본문과의 관계다. 현 형성 자료의 보존 위치도 그 논의에서 판단할 수 있다. 이번 작업을 새 management 구조의 재확정이나 운영 설치로 올리지 않는다. 이번 요청에는 커밋을 포함하지 않았다.
