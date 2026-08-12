# goal — Mission과 Campaign Goal

상태: **현재 운용 기준 — Goal 계층과 Campaign Goal 작업판**

이 문서는 프로젝트가 향하는 Mission과, 이번 지원 실행이 직접 닫을 Campaign Goal을 함께 소유한다. 현재 위치와 다음 행동은 [current.md](./current.md), Goal 아래의 반복 운용은 [core/loop.md](./core/loop.md)가 소유한다. Goal의 문구와 완료 의미는 현재 근거에 따라 다시 열 수 있지만, 경로 수정과 구분해 변경 근거를 남긴다.

## Mission

> **Cofathon 본선 참가자로 선발된다.**

수상·채용·포트폴리오는 그다음이다. Mission은 조사·문제 설정·엔지니어링·지원 제출과 외부 심사까지 이어지는 프로젝트 전체 방향이다.

## Campaign Goal

> **지원 마감 안에, Q1만 읽어도 내가 AI Native인 이유와 증명 논리가 이어지고, 선택한 실제 사용자 문제·workflow에서는 지원 증거물 계약에 따른 작동 결과와 AI 제작 과정의 인과를 실제 근거로 확인할 수 있는 지원안을 제출해 접수를 확인한다.**

Campaign Goal은 이번 지원 실행의 조사·문제 설정·솔루션·엔지니어링·제출을 가로지른다. 각 단계나 loop가 새 Campaign Goal을 만들지 않는다.

## 완료를 확인하는 상태

- [current](./current.md)에서 선택한 실제 사람의 문제와 제안한 해결의 직접 작용이 각각 근거로 성립하고, 사용자가 방향을 선택했다.
- [지원 증거물 계약](./core/support-evidence-artifact.md)의 두 증거 채널이 실제 실행·기록으로 성립하며, 확인하지 못한 범위와 보장하지 않는 범위가 구분돼 있다.
- Q1은 링크 없이도 주장과 증명 논리가 이어지고, 링크는 실제 결과와 근거로 주장을 보강한다.
- 제출 직전 [공식 요구사항](./core/requirements.md)을 라이브 원문과 다시 대조하고, 사용자 승인 뒤 제출 성공과 접수 상태를 확인한다.

여기서는 각 조건의 상세 판정 기준을 복제하지 않는다. 문제–솔루션의 현재 닫힘 조건은 `current`, 증거물의 형태와 두 증거 채널은 `support-evidence-artifact`, 공식 제출 조건은 `requirements`가 각각 소유한다.

## Campaign Goal이 미리 정하지 않는 것

- 최종 사용자·문제·후보
- 플러그인의 기능·host·입력·출력
- 공개 링크의 구체 형식과 마스킹 방식
- 구현 순서와 각 반복의 판별 질문·판별 실행

이 항목들은 최신 증거와 산출물에 따라 바뀔 수 있다. 경로가 바뀌어도 Mission과 Campaign Goal의 완료 의미가 자동으로 바뀌지는 않는다.

## 엔지니어링 단계와의 관계

- [engineering/](./engineering/README.md)은 엔지니어링 문서와 기록 경계를 안내한다. `engineering/00-top-level-goal.md`는 2026-07-17 사용자 결정으로 자연어 여행 상황에서 live 상품·option 후보를 좁히는 진입까지 확장됐다. `engineering/01-purchase-decision-slice/goal.md`는 완료됐고, 현재 활성 leaf Goal은 `engineering/03-live-purchase-entry/goal.md`다. 수행 뒤 폐기한 Loop 02의 번호는 재사용하지 않는다.
- 독립된 상태·평가·증거 계약이 필요한 구현 loop만 `engineering/NN-short-name/goal.md`로 추가한다. 번호는 실제로 연 순서를 식별할 뿐 다음 loop의 주제와 순서를 미리 정하지 않는다.
- `current.md`는 활성 최상위 구현 Goal을 요약하고, 활성 leaf Goal이 있으면 그 Goal을, 없으면 다음 loop를 고르는 현재 판단점을 단일 커서로 가리킨다.
- 엔지니어링의 구현 목표와 반복은 Campaign Goal에 기여하지만 Mission이나 Campaign Goal을 대신하지 않는다.

## 유실 방지 계약

- `current.md`는 Mission과 Campaign Goal의 짧은 요약·이 문서 링크를 항상 유지한다.
- 프로젝트 세션 시작 시 `current.md`와 함께 이 문서를 읽는다.
- 엔지니어링이 활성일 때 `current.md`는 현재 구현 목표와 미충족 상태를 요약하고 단일 커서를 유지한다.
- Goal의 문장·완료 의미·필수 증거가 바뀌면 사용자가 확인하고 `context/process/`에 `이전 Goal → 새 Goal`, 변경 근거, 영향 범위를 남긴다.
- 경로 수정과 Goal 변경을 구분하고, 현재 결과를 통과시키기 위해 완료 기준을 약하게 만들지 않는다.
