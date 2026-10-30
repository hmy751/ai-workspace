# 06-01 — 채택된 품질 기준의 Reference 후속 반영

2026-10-30. **01-02의 후속 품질 기준을 Reference Personal에 반영하고 직접 확인했다.** 사용자는 “01-02 보완된 거부터 Reference에 반영하고 확인해봐. 기존 합의 잘 지키고 Maintain 관련은 계속 02에 두자”라고 요청했다. 이번 결과는 문서 기준·형성 근거·읽기 연결의 적용이며 전체06-01 완료나 실제 개발 효과의 검증은 아니다.

## 무엇을 반영했나

[prototype 반영](2026-10-29-ticket01-02-code-expression-prototype-adoption.md) `10153862`와 [설계 마감](2026-10-29-ticket01-02-closeout.md) `6e6dccb8`을 입력으로 사용했다. 첫 Reference 적용 이후 Personal에서 달라진13개 파일을 대조했고, 기존8개 수정·신규5개를 반영했다. 기존 Reference의 차이는 Personal README의 context-update 상대 링크 한 곳이었으며 이를 유지했다. 나머지12개는 채택된 prototype과 같은 바이트다.

| 내용 | Reference에서 읽을 위치 |
| --- | --- |
| JS/TS 중괄호, 관련 변수 묶음과 처리 구간의 빈 줄, 코드 배치·주석·실패 진단 | [코드 표현과 진단](../../../../reference-project/context/personal/development/code-expression/INDEX.md) |
| 같은 값인 상수의 의미·변경 이유, 주석 상세 연결 | [이름·책임·완료](../../../../reference-project/context/personal/development/naming-and-completion/INDEX.md) |
| catch의 실패 분류 범위, void와 비대기 실패 책임, await 추가의 동작 영향 | [계약과 수명](../../../../reference-project/context/personal/development/contracts-and-lifetime/INDEX.md) |
| 네 주제의 선택과 형성 근거 | [개발 기준 안내](../../../../reference-project/context/personal/development/README.md), [Reference 후속 반영 기록](../../../../reference-project/context/_background/records/2026-10-30-personal-quality-update.md) |

새 형성 자료의 사용자 발화·과거 가이드 발췌·사용자 가독성 평가는 당시 prototype의 근거로 보존했다. 이번 Reference에서 발생한 새 사건이나 효과로 바꾸지 않았다. Reference 자체의 후속 반영 기록과 그 진입2개를 더해 Reference 변경 경로는 총15개다.

## 기존 합의와 경계

- Personal은 개인 판단 기준을 맡는다. 실제 formatter·logger·민감 정보와 제품 완료·오류 계약은 Project가 소유한다. JS/TS 표현을 Reference의 Python 제품에 기계적으로 적용하지 않는다.
- 새 원칙·날짜 사례를 추가하거나 기존 코드 전체를 정리하지 않는다. 책임 배치의 기존 기준 유지라는01-02 마감 판단도 보존한다.
- Work·Maintain·Recover·Verify·machine JSON·스킬·도구 연결·제품·Project 본문은 그대로다.02의 기록/전환 계약과 통합 테스트를 앞당겨 실행하지 않았다.
- Noline은 수정하지 않았다.06-02의10월29일 계획은 이전 Reference 판본을 기준으로 한 제안이다. 실제 적용 전에 이번15개 경로와 새 source 판본을 반영해 계획·해시를 갱신해야 한다. 기존 계획 receipt를 새 적용 완료 증거로 고치지 않는다.

## 확인한 것

[경로별 source/target 해시와 검사 결과](receipts/reference-application/2026-10-30-personal-quality-update.json)에 범위와 한계를 남겼다.

- Personal과 관련 배경 진입52개 Markdown의 로컬 링크328개·앵커135개를 확인했다. 누락은 없었다. 기존 두 링크는 Reference 밖의 당시 prototype 원자료를 가리키므로, 원래 문맥과 파일 동일성을 확인해 provenance 경로로 별도 표시했다. 새 실행 의존이나 새로 생긴 외부 링크가 아니다.
- 반영13개 source/target을 바이트·해시로 대조했다. 유일한 차이는 기존 Reference용 context-update 링크다. prototype은 수정하지 않았다.
- 변경 대상 밖 파일·symlink420개가 동일했다. 이 중 Work 경로264개, 스킬·도구 경로64개, 제품·Project 경로25개를 포함한다. 파일 수는 관찰된 로컬 파일 기준이며 테스트 수나 효과 측정치가 아니다.
- Main은 root의 Personal 진입에서 개발 기준 안내·새 표현 본문·이름/계약 연결을 따라 읽었다. 관련 변수는 묶되 선언·검사·실행의 경계를 띄우는 선택, 진단과 실패 처리의 구별, 같은 값만으로 상수를 합치지 않는 판단, catch가 후속 적용 오류를 잘못 분류할 위험과 void/await의 차이가 해당 본문에서 설명되는지 대조했다. 사례의 코드 모양을 강제하거나 단순 가독성 변경으로 동작을 바꾸지 않는 제약을 유지했다.
- `git diff --check` 통과. 문서 변경이며 제품·실행 코드가 동일하므로 제품 테스트·Harness 전체 검사를 반복하지 않았다. 실제 host 호출·사용감·장기 효과는 확인하지 않았다.

적용 확인 당시에는 커밋하지 않았다. 후속으로 사용자가 “이번 반영한 거 기록하고 커밋하자. 병렬 작업 변경은 빼고”라고 요청했다. 이번 Reference15개 경로와 적용 기록·증거·직접 연결된 재진입 안내만 커밋 대상으로 분리한다. 병행02 문서와 앞선06-02 조사 자료·공유 문서의 해당 변경은 작업 트리에 보존하며 push는 하지 않는다. 다음06-02 반영에서는 이 결과까지 포함한 Reference 판본을 고정하고 Noline의 기존 기준·호환 경로·진행 작업을 다시 대조한다.

## 최종 확인 중 들어온 별도 변경

다른 작업에서 본문 형식 기준 `WRITING-FORMAT.md`·형성 자료와 이름·완료 본문 재편을 `3a28e6a1`로 커밋했다. 최초 검사 이후 live source의 이름·완료 본문 해시가 달라져 재검사가 이를 탐지했다. 이번 적용을 최신 prototype 전체와 같다고 보고하지 않고, 입력 `6e6dccb8`의 Git 원문과13개 target을 다시 대조해 통과했다. 새11개 경로 변경은 이번 요청의01-02 마감판 보완과 구별해 보존했으며 자동 편입하지 않았다. 새 형식 기준·형성 자료·관련 본문의 적용 여부는 후속 차이로 함께 검토한다.
