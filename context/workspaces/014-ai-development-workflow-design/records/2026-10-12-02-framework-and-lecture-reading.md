# ai-workspace와 강연을 구체적으로 읽은 결과

이 기록은 설계 재료를 다시 조립하지 않도록 현재까지 읽은 내용을 보존한다. 아래의 연결과 후보는 AI의 분석이며 사용자가 채택한 전체 운영 방식이 아니다. 이번 단계에서 실제 하네스·앱 실행이나 파일 개편을 수행하지 않았다.

## ai-workspace의 현재 구성과 실제 동작

저장소 루트는 작업 방식의 연구·개발 공간이고 `reference-project/`는 이식할 기준 구현이다. 루트는 자동 Maintain을 연결하지 않고 Main이 Workspace를 직접 관리한다. Reference의 자동 장치와 현재 루트 운영을 동일하게 보면 안 된다. Noline은 Reference를 적응해 이식한 별도 저장소여서 이후 변경이 자동 동기화되지 않는다.

Project는 `common/current/guidance/decisions`에서 제품 의미·현재 구현·작업 가이드·선택 이유를 나누며, 실제 본문을 선택하는 진입 경로와 작성·갱신 기준이 있다. Work는 작업별 Spec·Ticket·state와 source·output·records를 구분한다. 기록 원칙은 이미 선택 이유·비용·조건·열린 판단·최소 원문과 직접 확인/보고/제안/채택의 구분을 요구한다.

Spec·Ticket 실행 기준에는 결과에 필요한 일을 찾아낼 책임, 초안 수정 목록으로 조사 범위를 제한하지 않기, 목표를 기존 구현에 맞춰 낮추지 않기, 동작 보존과 구조 개선을 각각 판단하기가 들어 있다. “개발 품질 기준이 없다”는 진단은 맞지 않는다. 기존 내용의 충분성, 필요한 구체화, 실제 수행과 장치의 문제는 사례에 따라 나누어 검토해야 한다.

소스와 관련 테스트를 읽어 확인한 동작은 다음과 같다.

| 장치 | 확인한 구현 | 의미·효과에 관한 한계 |
| --- | --- | --- |
| Recover | 명시 id 또는 기본 Workspace를 선택하고 `recover.json`의 Project 문서와 memory/spec·Ticket 색인·state·output 색인을 읽기 전용 packet으로 조립한다. | 문서 선택을 모델이 추론하지 않는다. bounded는 파일 종류·깊이·명시 선택의 제한이며 token/byte 상한이 아니다. 읽었다고 이해·적용을 보장하지 않는다. |
| Maintain | 명시적 세션 연결 뒤 Recover로 grounding하고, 같은 thread id를 `codex exec resume`하여 사용자 prompt와 Main 최종 응답의 변화를 판단한다. read-only 의미 판단과 제한된 파일 반영을 분리한다. | 전체 도구 trace·내부 위임·diff를 기본 수집하지 않는다. 운영 계약 전체는 매 start/resume에 다시 붙는다. 이 구조만으로 실제 토큰 손실 원인을 측정한 것은 아니다. |
| Verify | `verify.json`의 근거 파일 hash를 보존하고 고정 argv를 실행한 뒤 성공·실패 receipt와 machine status를 기록한다. | 실제 사용자 장면을 스스로 찾아 제어하는 도구가 아니다. 명령 성공은 기준의 충분성, 사용자 acceptance, 전체 완료를 뜻하지 않는다. |

Maintain의 guarded apply는 경로·preimage·형식 등을 검사하며 기록의 의미 충분성을 판별하지 않는다. Recover/Verify의 책임은 의미 판단 agent와 분리돼 있지만 공통 CLI import 등 결합은 있어서 폴더 삭제만으로 제거가 완성되지는 않는다. 사용자에게 필요한 것은 기존 Maintainer 재평가가 아니라, 기록 원칙을 남기며 향후 제거·대체를 설계할 때 이 관계를 아는 것이다.

기준판 진입: [Reference README](../source/ai-workspace-baseline/reference-project/README.md), [Spec 실행 기준](../source/ai-workspace-baseline/reference-project/context/work/workspaces/spec-and-tickets/EXECUTION-CRITERIA.md), [문서 작성 기준](../source/ai-workspace-baseline/reference-project/context/work/workspaces/DOCUMENT-WRITING.md). 실제 코드·테스트도 같은 baseline에 보존했다. 확인은 소스와 테스트의 의도까지이며 실제 host 동작을 새로 실행한 것은 아니다.

## PR 병목 강연과 관련 스킬

강연은 자동 검사, 별도 AI 리뷰, 사람의 리뷰를 조합해 사람이 처음 보는 결과의 품질과 판단 속도를 높이려 한다. 테스트가 구현을 그대로 반복하거나 mock으로 실패를 감추는 문제도 다룬다. Deep module은 코드 길이 비율이 아니라 호출자가 알아야 할 지식과 순서·오류·설정 부담을 작은 인터페이스 뒤에 모으는 설계 관점이다.

구현자의 탐색·작성·디버깅 부담이 크므로 세부 코딩 표준을 별도 reviewer에게 집중시키는 배치를 제안한다. 다만 필요한 제품 계약·구조 맥락까지 구현자에게 주지 말라는 일반 원칙으로 확대할 수는 없다. 강연은 reviewer가 수정까지 수행하는 쪽을 권하지만, 제공된 `code-review.ko.md` 절차는 Standards와 Spec 두 보고를 모으는 데서 끝난다. 시점·버전 차이인지 확인되지 않았으며 수정과 최종 판단의 배치는 남은 설계 선택이다.

| 자료 | 실제 제공하는 방법 | 이 자료만으로 닫히지 않는 것 |
| --- | --- | --- |
| code-review | 기준 diff·저장소 표준·명세를 읽고 Standards/Spec 두 축으로 검토한다. | 미커밋 변경의 처리, 보고 이후 수정·수락 과정은 상세히 정하지 않는다. |
| codebase-design | module·locality·leverage·seam, 호출자의 부담과 테스트 경계를 판단한다. | 특정 실행 순서나 모든 프로젝트의 구조를 고정하지 않는다. |
| improve-codebase-architecture | 최근 변경 영역을 조사해 전후 구조·마찰·이점을 담은 후보를 제시하고 사람이 선택한다. | 상세 설계용 추가 references와 일부 후속 skills는 제공 폴더에 없다. |
| pr | 변경 전후 근거, 이유를 이해시키는 표현, 되돌릴 수 있는 정도와 영향 범위를 전달한다. | 검증이나 reviewer 지적 처리 자체의 전체 workflow는 아니다. |
| retro | 세션 원자료에서 탐색·검사·표준·도구 비용·효과 없는 지시·정보 접근의 개선 후보를 찾는다. | 후보의 채택·구현·다음 작업의 효과 확인까지 자동 완결하지 않는다. |

## Agent 신뢰 강연

반복 사용할 수 있는 앱 제어 CLI와 Feature Map을 결합한다. CLI는 실행·trace 등 경험적 근거를 얻는 경로이고, Feature Map은 어떤 기능이 있고 어떤 조작으로 도달하며 무슨 일을 하는지 설명한다. 같은 이름의 Verify receipt 장치와 역할을 혼동하지 않는다.

강연은 코드가 AI가 따라 하는 패턴이라는 점에서 코드 구조를 중요한 기억으로 본다. 나쁜 패턴을 구조적으로 어렵게 만들고, 기계적으로 검사할 수 있는 것은 lint·타입·CI로 다루며, 나머지를 rules·skills와 사람의 판단으로 보완한다. Dune의 엄격한 import 경계·주석 금지·대규모 에이전트 운영은 발표자의 환경과 선택이며 Noline에 곧바로 채택한 기준이 아니다.

Project context와 코드의 관계도 함께 설계할 수 있다. 코드가 반복할 실제 패턴을 제공하고, 문서가 제품 의미·선택 이유·예외·사용 및 변경 방법을 설명할 수 있다. 어느 내용을 코드·검사·가이드·워크플로가 맡을지는 실제 주제에 따라 구체화해야 한다.

## Vercel 제품 설계 자료

이 자료는 코드만으로 드러나지 않는 제품 판단을 실제 리뷰·대화·화면·PR 근거와 함께 보존한다. 반복되는 결정·이유·예외·좋고 나쁜 사례를 바탕으로, 기계적으로 판별할 수 있는 것과 맥락 판단이 필요한 것을 나눈다. collector는 근거를 모으고 별도 judge는 묶음과 열린 질문을 만들며, 새 표준으로 채택할지는 사람이 판단한다. 수집부터 매번 새 규칙을 확정하는 방식이 아니다.

평가에서는 skill 없는 실행과 기대 수정을 숨긴 사례를 비교하고, 규칙 준수와 이미 출시된 결과의 유사도를 구별한다. 출시 코드도 결함이 있을 수 있기 때문이다. 실제 공개 설명의 eval은 copywriting 범위이며 전체 제품 설계 workflow의 효과를 증명한 실행 결과·fixture·rubric이 제공된 것은 아니다.

이는 사용자 기준이 아직 모호한 부분을 실제 사례와 대비안으로 발전시키는 참고가 된다. 사용자가 추상적인 모든 기준을 먼저 정의해야 한다거나, AI가 인터뷰 한 번으로 전역 규칙을 확정해야 한다는 결론은 나오지 않는다.

## 이어서 판단할 차이

현재 작업의 맥락을 갱신하는 일, 산출물의 적절성을 검토하는 일, 경험을 다음 작업 방식에 반영하는 일은 서로 연결되지만 같은 판단은 아니다. 같은 대화 경계에서 함께 할 수도 있고, 필요한 때 나눌 수도 있다. 이를 서로 다른 agent나 고정 단계로 구현할지는 아직 열려 있다.

기존 briefing·recovery는 설명과 이해를 지원하고 reconsider는 선택·가정과 후속 책임을 재판단한다. 이 기능을 code-review나 architecture 탐색과 같은 것으로 보거나, 모든 완료 보고에 전체 briefing을 강제로 호출하는 것으로 연결하지 않는다. 반대로 기존 기준이 있다는 사실만으로 앞으로의 보완이 불필요하다고 보지도 않는다.

[강연·스킬 사본](../source/lectures/)에는 두 전체 번역과 상세정리, 관련 다섯 스킬, Vercel 글을 보존했다. 상세정리의 React/Next.js 적용 예와 코드 예시는 원 강연의 실제 구현 증거와 구별한다. `DEEPENING.md`, `DESIGN-IT-TWICE.md`, `HTML-REPORT.md`, grilling/domain-modeling 등은 원 제공 폴더에서 확인되지 않았다.
