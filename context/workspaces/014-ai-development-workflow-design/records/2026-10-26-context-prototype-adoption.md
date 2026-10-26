# 04-03 — 네 맥락 구체안의 프로토타입 적용

2026-10-26. 사용자는 계획 기록을 먼저 커밋하고 프로토타입에 적용하라고 요청했다. 적용 전 기록은 `9eb012f3`(`맥락 연결의 프로토타입 적용 계획을 기록`)로 보존했다. [적용 계획](2026-10-26-context-prototype-integration-plan.md)에 따라 기존 단일 prototype의 실행 본문·관리 계약·진입·형성 자료를 연결했다. 전역 설치나 실제 Noline 변경은 이 작업의 대상이 아니다.

직접 요청:

> 먼저 커밋할거 부터 하고 그럼 프로토 타입 적용해봐

작업이 중단된 뒤 사용자의 “프로토 타입은?”을 새 상태 설명만의 요청으로 좁히지 않고 원래 승인된 적용과 확인을 이어갔다.

## 실제 구성과 책임

| 책임 | 적용한 본문과 바뀐 행동 |
| --- | --- |
| 수행의 시작·배정·재탐색·종합·완료 | [development](prototypes/development-workflow/skills/development/SKILL.md)와 세 역할 상세. 담당자는 원문을 직접 읽고, 구현자가 제안한 지속 변화는 Main이 전체 맥락에 대조해 반영한다. 기존 구현 완성·개선 검토·독립 검증·explain은 유지한다. |
| 질문별 공통 읽기 | [USAGE](prototypes/development-workflow/noline-demo/context/USAGE.md). 일반 read 방법을 공통화하고 제품 고유 질문은 Project 읽기 기준에 남겼다. 직접 설명 요청에도 같은 방법을 쓰며 Work 생성·전체 인수·별도 보고서·읽은 기록을 강제하지 않는다. |
| 지정된 지속 본문 반영 | [context-update](prototypes/development-workflow/skills/context-update/SKILL.md). 근거·허용 범위·내용 선별·실제 읽기 확인을 수행한다. Personal·Project의 내용/권위는 영역 관리 계약에 남는다. 같은 Main이 가진 근거로 읽기에서 반영까지 이어갈 수 있다. |
| 현재 Work 유지와 새 목표 계승 | [Work 지침](prototypes/development-workflow/noline-demo/context/work/AGENTS.md), [생성·전환 계약](prototypes/development-workflow/noline-demo/context/work/workspaces/CREATE-AND-TRANSITION.md), [create-context-workspace](prototypes/development-workflow/skills/create-context-workspace/SKILL.md). 기존 Work 구조를 유지하며 새 목표의 의미 구성·인수·생성과 전환을 구별한다. 일반 재개의 기본 선택은 Work 목록 한곳에서 관리한다. |
| 일반 진입·관리·설명 예시 | prototype README, demo root/context와 각 영역 안내, [walkthrough](prototypes/development-workflow/walkthrough.md), [열람 화면](prototypes/development-workflow/viewer.html). 본문을 찾는 진입과 현재 수행 예시가 새 책임으로 이어진다. |

공통 읽기와 갱신을 다른 파일에 둔 현재 형태를 사용자가 매번 둘 중 하나를 골라 재입력해야 하는 절차로 만들지 않았다. USAGE/context-update의 사용감과 정확한 이름에 관한 유보는 유지한다. 개발 중의 시점·담당은 development, 영역에 무엇을 남길지와 어떤 권한으로 바꿀지는 각 관리 계약, 한정 편집 방법은 context-update가 맡는다.

Project에는 계속 쓸 제품 의미·구조·계약·제약·이유와 필요한 공통 지원 사실을 선별한다. 이번 구현·검사의 진행을 자동으로 옮기지 않는다. 이 기준을 [2번 현행 설계](2026-10-26-context-02-role-execution-proposal.md)의 예시와 development·walkthrough에도 맞췄다. 늦은 결과의 원 Work 귀속과 계속 수정할 최신 권한도 구별했다.

새 USAGE·두 스킬에는 가까운 형성 자료를 두고 기존 development·Project 관리의 형성 이유를 보완했다. 바깥014 기록을 prototype 독자의 필수 입력으로 만들지 않았고 기존 Work에는 새 `_background` 구조를 추가하지 않았다. 원형 source, 제품 코드·검사, 실제 runtime·자동 Maintain·전역 브릿지는 수정하지 않았다.

## 검토와 직접 확인

[독립 개선 검토](2026-10-26-context-prototype-integration-review.md)에서 현재 walkthrough에 남은 Project 자동 갱신 예시를 찾아 고쳤다. 같은 검토자의 후속 대조는 이 불일치 해소와 Project 무수정 종료·부분 반영 뒤 재개의 책임 연결을 확인했다. 후자의 두 장면은 지침의 의미 대조이며 실제 중단·복구 수행 시험은 아니다.

[복사본 수행 기록](experiments/context-prototype-integration-2026-10-26/README.md)에서 요청·입력·실제 답·변경·한계를 보존했다. 읽기 요청은 파일을 바꾸지 않았고, 오류를 심은 지원 설명은 실제 근거와 대조해 한 문장만 정정했다. 별도 Work 생성은 기존001과 기본 선택을 보존했고, 이어 명시 전환을 요청한 뒤에만002를 기본으로 바꿨다. 새 Work는 필요한 의미를 직접 구성했으며 기존 메모리 가정·검사 통과를 상속하지 않았다. 원본 prototype에는 시험용 오류나002를 추가하지 않았다.

Main은 전후 파일 해시·diff와 새 current의 의미를 직접 대조했다. 갱신 수행자의 기존7개 검사·정상/실패 데모 실행 보고는 보존하되 Main이 다시 실행한 결과로 표시하지 않는다. 여러 역할의 전체 개발 수행·실제 중단 복구·새 세션의 독립 인수 시험은 수행하지 않았다.

열람 화면을 현재 원문으로 재생성하고 검사했다. 문서188개·코드5개의 내용/해시, 내부 링크1083개·앵커293개가 일치하며 누락0이고 로컬 링크는 prototype 안에 있다. 브라우저 렌더링 실측은 하지 않았다. 다섯 SKILL의 YAML을 파싱해 이름·설명이 유효함을 확인했고 공백 검사도 통과했다. skill-creator의 quick_validate는 PyYAML 부재로 실행되지 않아 제공된 Ruby YAML 파서로 메타데이터를 확인했으며 패키지를 설치하지 않았다.

## 기존 완료 조건 대조

| 04-03의 원래 조건 | 현재 근거와 완료 범위 |
| --- | --- |
| 기존 세 스킬 조항·조건·입력·산출물·기록과 Noline/Reference 차이 확인 | [전체 책임 대조](2026-10-26-context-whole-scope-reconciliation.md)와 적용 계획에서 read의 공통 방법 이관, update의 한정 반영, create의 수동 demo 계약 적용을 비교했다. 원형의 runtime 의존을 새 실행에 가짜로 넣지 않았다. |
| 재개·본문 적용·공통 갱신·Workspace 생성의 대표 비교 | 네 상세안과 현재 walkthrough, 직접 요청 네 번의 복사본 수행에서 현재/보완 대응을 연결했다. 실제 host 재개는 후속으로 구별한다. |
| 계약·예외·현재 차이가 실제 작업에 쓰임 | 설명 답에서 비대기 조건과 실패 분리를 적용했고, 지원 설명 오류를 실제 코드/검사 범위로 정정했다. 새 Work에서 메모리 가정·기존 pass를 계승하지 않았다. |
| 비적용·중복·책임·비용 | 읽기만이면 무편집, 지속 의미 변화 없으면 Project 무수정, 같은 수행자의 근거 재사용, 생성과 전환 분리, 조건부 형성 자료 읽기를 연결했다. 반복 사용감·장기 비용 개선을 실측했다고 주장하지 않는다. |
| 02·03 정본 및06 전환과 연결, 남은 선택·host 확인 경로 | 내용 관리와 수행의 정본을 유지하고 아래 후속을 각 수신 Ticket에 연결했다. 현재 packaging 사용감 유보·실제 설치/호출·host 확인은 남긴다. |

기존 완료 조건에 비춰 **04-03의 설계와 prototype 실행 연결을 마감한다.** 실제 운영 설치·일반 효과와 상위04·Workspace014 전체 완료를 뜻하지 않는다. 이번 반영에서 구체 결함이 드러나면 해당 본문을 보완하며, 후속 관찰이 남았다는 이유만으로 같은 설계를 전부 미정으로 되돌리지 않는다.

## 후속 책임

- 02: 기존 Work 구조 안의 현재 의미·중요한 제안·처리 근거 보존을 입력으로 받는다. 전체 구성·분량·보존·재개 운영과 새 background 적용 여부는 여기서 완료하지 않았다.
- 05: 이미 반영한 선택·근거·결과도 후일 검토할 수 있게 연결했다. 대화 기준의 명시적 개선 단계·담당·발동 시점은 여전히 이 Ticket의 설계다. 일상 정정은 그 단계를 기다리지 않는다.
- 06: 실제 대상의 기존 read/update/create 호출·설치·bridge·Recover/Verify·자동 장치 의존을 새 묶음과 대조하고 전환·복구 범위를 정한다. 수동 Work 목록 변경을 host activation으로 보고하지 않는다.
- 07: 자동 발견과 실제 여러 역할의 개발 수행, 실제 host 재개·전환, 반복 사용감·유지 비용을 관찰할 경로를 정한다. 이번 국소 수행을 일반 효과로 확대하지 않는다.

01-02 전체 품질 기준 종합과 상위01·04·Workspace014 전체의 남은 설계도 유지한다. 이번 적용을 네 개의 새 스킬이나 네 번의 의무 관문으로 해석하지 않는다.
