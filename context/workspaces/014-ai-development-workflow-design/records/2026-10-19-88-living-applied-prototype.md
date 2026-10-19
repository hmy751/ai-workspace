# 하나를 계속 발전시키는 적용 프로토타입

2026-10-19. 사용자는 조건별 적용과 과정 근거를 보완한 내용을 단독 문서에 두는 데서 그치지 않고, 실제로 적용된 모습을 갖춘 새 프로토타입으로 만들고 하나를 계속 발전시키자고 요청했다. Main은 앞으로 수정할 실물을 [development-workflow](prototypes/development-workflow/README.md) 한 폴더로 정했다. 기존 날짜별 시안은 원형으로 보존한다.

## 사용자 요청과 이번 선택

사용자:

> 그럼 반영하는데 prototype에 잘 반영하면 좋겠어 단독으로 말고 실제 프로토 타입으로 가정하고 그리고 좀 정해서 하나 계속 발전시켜나가면 좋겠어 일단 새로 만들자

이어 적용 모습에 관해:

> 그래 shop web이라든가 noline demo 라든가 아무튼 적용한 못브으로

사용자가 선택한 것은 **적용 모습을 갖춘 새 프로토타입 하나를 만들고 계속 발전시키는 방식**이다. `shop web`과 `noline demo`는 그 모습을 설명한 예시이며 두 제품을 모두 만들라는 요청이나 실제 Noline에 적용하라는 권한이 아니다.

Main은 구체 경로를 `records/prototypes/development-workflow/`로, 이번 적용 대상 예시를 `noline-demo/`로 정했다. 이 이름과 대상은 요청을 구체화하기 위한 Main의 선택이다. 앞으로 개선할 때는 날짜별 유사 폴더를 새 현재 결과로 늘리기보다 이 폴더 안의 본문·적용 장면·화면을 함께 고친다. 판단 과정과 의미 있는 변경은 별도 기록으로 남긴다.

## 새 프로토타입에서 함께 볼 책임

새 폴더 안에는 다음 배치를 사용한다. 이 배치는 프로토타입 내부이며 실제 운영 위치에 설치한 결과가 아니다.

| 위치 | 보여 줄 내용과 책임 |
| --- | --- |
| `ai-workspace/context/personal/` | 작업대 아래의 개인 기준. 개발 공통·이름과 완료 범위의 의미·조건·근거를 제공한다. |
| `noline-demo/` | 대상 제품의 Project 계약·현재 현실과 이번 Work의 요구·선택·변경·검토 기록. 개인 기준의 관리 책임을 Project에 넘기지 않는다. |
| [workflow/development.md](prototypes/development-workflow/noline-demo/context/work/DEVELOPMENT.md) | 필요한 개인 주제와 대상 Project 본문을 별도로 선택하고 충돌을 판단해 구현·검토에 전달하며 결과별 갱신을 연결하는 절차. 실제 설치된 스킬은 아니다. |
| 적용 장면과 열람 화면 | 한 작업에서 어떤 본문이 왜 읽히고 이름·계약·동작·검토·기록으로 이어지는지 보여 준다. 본문 정본과 화면의 표시 사본을 구별한다. |

단독 기준의 내용만 다시 나열하지 않고 실제 적용의 입력·선택·변경·검토·남는 기록과 함께 본다. 예시에 부여한 초기 문제·사용처의 가정과 실제 작성·검사한 demo 코드를 구별한다. 로컬 demo의 검사 결과를 실제 Noline 제품 실행으로 확대해 보고하지 않는다.

## 이어받는 의미와 이전 자료의 역할

[87](2026-10-19-87-conditional-application-and-provenance.md)의 채택 후 조건별 적용, 원래 대화·사례로 돌아가는 경로, Main이 새로 쓴 문장·질문·사례의 지위 구별을 새 프로토타입에서도 유지한다. 기준이나 사례와 코드 모양이 다르다는 이유만으로 수정하지 않으며 현재 목적·사용처·비용에 따라 판단한다.

01의 [66](2026-10-18-66-principles-cases-and-refinement-prototype.md)·[68](2026-10-18-68-principle-application-and-choice-basis.md)·[72](2026-10-18-72-short-common-and-detail-prototype.md)의 형식·적용 의미 반영 선택과 [73](2026-10-18-73-prototype-reservations-and-ticket03.md)의 전체 만족·최종 수용 유보를 구별한다. 새로운 적용 실물을 만드는 선택이 개인 기준 내용 전체·현재 질문 문구·가상 사례의 최종 채택은 아니다.

[84](2026-10-19-84-personal-project-ownership-and-format-correction.md)의 Personal·Project 독립 책임과 workflow의 연결 책임, [86](2026-10-19-86-context-personal-choice-and-text-comparison.md)의 ai-workspace `context/personal/` 위치 선택도 유지한다. 프로토타입 내부에서 그 구조를 재현하는 일과 실제 `context/README.md` 계약을 바꾸거나 운영 Personal을 만드는 일은 다르다.

[이전 적용 시안](prototypes/personal-project-applied-2026-10-19/README.md)은87까지의 보완을 담은 원형으로 보존한다. [01 적용 시안](prototypes/applied-criteria-2026-10-17/README.md), [세 본문 시안82](prototypes/personal-project-naming-2026-10-19/README.md), [7쌍 비교](prototypes/criteria-format-comparison-2026-10-19/README.md)와 이전 기록·원자료도 바꾸거나 지우지 않는다.7쌍 비교는87 보완 전 원문과 평가의 snapshot이며 앞으로 현재 본문으로 자동 갱신하지 않는다.

## 확인과 남은 범위

새 프로토타입의 작업대 context·Personal, Noline demo의 Project·Work, 개발 workflow와 적용 장면, 실행 코드·동작 검사를 작성했다. 이제 이 폴더가 함께 검토하고 계속 발전시킬 현재 실물이다. 기존 날짜별 시안의 검사 결과를 새 프로토타입의 검증으로 재사용하지 않았다.

Node.js 내장 검사7개와 정상·조회 실패 demo를 실제 실행해 모두 성공 종료를 확인했다. 구현 담당과 별도로 실물 문서·코드를 읽은 검토자도 같은 검사와 두 demo를 직접 실행했다. 검토 범위에서 수정이 필요한 중요한 코드 결함이나 문서·실행 계약의 불일치는 찾지 못했다. 실행 명령·항목·결과·미확인은 [이번 Work의 실행 기록](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/records/2026-10-19-03-execution.md), 실제 입력·읽기 검토·수정 여부·한계는 [검토 기록](prototypes/development-workflow/noline-demo/context/work/workspaces/001-login-completion-names/records/2026-10-19-04-review.md)이 소유한다. 이전 가상 검토자의 수정 장면을 이번 이력으로 복사하지 않았다.

[열람 화면](prototypes/development-workflow/viewer.html)을 최종 생성했다. 문서28개와 데모 소스·검사5개, 총33파일의 전체 원문·SHA가 실제 파일과 일치하는지 확인했다. 내부 문서 연결134곳·바깥 원자료 연결27곳·제목 연결8곳, 잘못된 링크 형식12종의 거부와 화면 스크립트 문법도 정적 검사를 통과했다. 재생성과 검사 방법은 [viewer 안내](prototypes/development-workflow/viewer/README.md)에 남겼다. 브라우저 렌더링이나 실제 화면 조작은 확인하지 않았다.

현재 동작 확인은 메모리 기반 demo와 문서의 계약 범위다. 실제 Noline·UI·외부 저장소·DB/queue 통합, 새로운 작업자의 자율적인 발견·적용 효과, 사용자 수락이나 전체 기준 채택을 확인한 것은 아니다.

실제 운영 `context/personal/` 생성, 기존 파일 이동·통합, 실제 Noline 적용·실제 제품 실행, 스킬 설치와 전역 하네스 변경은 하지 않는다.01-02·03·04-03·06과 전체 시스템은 미완료다. 이번 기록·안내 작업에서는 stage나 커밋을 하지 않는다.

기록 담당자는 이 기록과 재진입 안내 여덟 문서의 로컬 파일 연결345곳·제목 연결1곳을 확인했고 누락은 없었다. 작업 시작 때 고정한 기존 기록·날짜별 시안133파일은 내용이 같았다. 공백 검사는 통과했고 바깥 실제 `context/personal/` 운영 폴더는 없었다. 이 확인은 기록·진입 경로와 이전 자료의 보존 범위이며, 새 demo 실행·표시 사본·전체 본문 검토 결과를 대신하지 않는다.


## 후속 구조 정정

이 기록은 첫 작성 당시의 배치와 판단을 보존한다. 사용자가 실제 구조와의 차이를 지적한 뒤 [89](2026-10-19-89-local-context-structure-correction.md)에서 Personal을 로컬 context 안에 두려던 뜻을 확인하고 같은 prototype의 구조를 직접 고쳤다. 위 ai-workspace 모형과 별도 workflow 배치는 현재 구성이 아니며, 이동한 파일 링크는 재접근을 위해 현재 위치로 맞췄다. 첫 검사·검토 통과가 그 배치의 적절성을 입증하지 않는다.
