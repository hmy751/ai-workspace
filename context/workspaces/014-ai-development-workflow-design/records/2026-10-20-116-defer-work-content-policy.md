# Work의 본문·형성 자료 구성 적용을 되돌리고 논의 보류

[115의 진입 복구](2026-10-20-115-complete-body-moves-and-restore-entries.md) 뒤 사용자는 데모의 `context/work/workspaces/spec-and-tickets/background`를 보고 Work 전체에는 이번 구성을 적용하지 말라고 요청했다.

> 여기 왜 spec-and-tickets에 background를 둬?
> 일단 work쪽에는 두지말자 원래 형태와 제약등이 이미 있어서 혼합돼서 안될 것 같아 되돌려놔주고 이건 또 논의를 해봐야할 것 같아

## 현재 경계와 복구

Work는 기존 형태와 제약을 유지하고, 형성 자료 방식의 적용 여부·방법은 별도로 논의한다. `spec-and-tickets` 한 곳만의 삭제나 진입 파일명만의 복구로 좁히지 않았다. 이번에 추가한 Work의 모든 background와 관련 읽기 안내, 개별 Spec·Ticket의 새 index·README 구성도 되돌렸다. Personal·Project와 공통 context의 현재 적용은 유지했다.

복구 기준은 이번 정책 재적용 전 판본 `33c1fee`의 데모 `context/work/`다. Spec은 기존 번호 파일 다섯 개, Ticket은 기존 단일 본문으로 돌리고, current·source·output·records와 개발 절차·작성 기준의 역할을 보존했다. 유지되는 Project의 현재 본문을 읽기 위한 링크 목적지만 현재 위치에 맞췄다. 그 밖의 Work 내용은 기준판과 같게 복구했다.

앞선 Main은 “수집한 근거를 가까이 보존한다”는 판단으로 새 형성 자료를 Work에 남겼다. 별도 self-check는 진입 문서 위치만 복구하면서 Work의 기존 관리 체계와 혼합되는 범위를 해소하지 못했다고 판단했다. 이번에는 자료를 Work 안의 다른 위치·다른 이름으로 옮겨 남기는 방식도 사용하지 않는다.

## 정책과 기록

[CONTENT-POLICY](prototypes/development-workflow/noline-demo/context/CONTENT-POLICY.md)와 [context 진입](prototypes/development-workflow/noline-demo/context/README.md)에 Work 적용 보류와 현재 적용 범위를 일치시켰다. 지속 본문 전반을 검토한다는 방향을 모든 기존 체계에 즉시 같은 형식을 적용하는 규칙으로 해석하지 않는다. 또한 Work의 영구 제외로 확정하지 않는다.

정책의 [현재 형성 맥락](prototypes/development-workflow/noline-demo/context/background/content-policy/context.md#work의-기존-체계와-형성-자료는-별도로-논의한다)과 [사용자 근거](prototypes/development-workflow/noline-demo/context/background/content-policy/evidence.md#work-전체의-구성-적용-보류), 기존 정정 기록에는 이번 선택을 이어 남겼다. 이는 공통 정책의 적용 경계를 설명하는 자료이며 Work의 형성 자료를 다른 활성 위치로 옮겨 대신 사용하게 하는 구성이 아니다.

114·115의 구성과 검토 결과는 당시 관찰로 보존한다. 현재 적용 상태를 그 기록의 과거 완료 표현에서 복원하지 않고 이 기록과 current에서 찾는다.

## 확인과 다음 논의

Main과 별도 검토자가 기준판을 직접 대조했다. Work의 파일 목록26개가 `33c1fee`와 정확히 같고, 새 파일·누락·background 폴더는 없다. 현재 Project 본문을 읽는 링크15곳을 제외하면 모든 파일의 내용이 바이트 단위로 같다. 차이는7개 파일에 한정되며, 초기 입력의 코드·가정과 과거 판단 기록도 보존됐다. [직접 비교 결과](receipts/work-policy-deferral-2026-10-20/baseline-check.json), [전체 경로 매핑](receipts/work-policy-deferral-2026-10-20/paths.json)

복구 전 Work45개 파일은 [보류된 구성 사본](receipts/work-policy-deferral-2026-10-20/work-before-deferral.zip)으로 바깥 작성 기록에만 보존했다. [사본 식별과 해시](receipts/work-policy-deferral-2026-10-20/preservation.json)가 그 지위를 설명한다. 현재 Work나 데모의 필수 읽기 경로에서 이 사본을 사용하지 않는다.

들어오는 Spec·Ticket 링크와 표시 화면의 경로도 원래 본문에 맞췄다. [표시 검사](receipts/work-policy-deferral-2026-10-20/viewer-check.json)는 문서112개·코드5개의 실제 원문·해시 일치, 내부 링크643개·앵커191개, 경로·절 누락0개를 확인했다. 모든 로컬 링크가 대상물 안에 있고 공백 검사도 통과했다. 제품 src·tests와 루트·014의 보존 source에는 변경이 없다. 브라우저 렌더링 실측과 제품 테스트 반복은 하지 않았다.

다음 논의는 Work가 이미 가진 Spec·Ticket·current·source·output·records의 형태·제약과, 그 안에서 의도·배경·선택 근거를 어떻게 다룰지다. 지금은 새 배치나 자동 갱신 방법을 정하지 않는다. 이번 요청에는 커밋을 포함하지 않았다.
