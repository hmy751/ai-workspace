# 현재 상태

마지막 갱신: 2026-09-14

## Project 주제별 Owner 이동 계약 보완

Noline `002-code-readability-refactoring`의 완료 Ticket 01~05 자료를 Project context에 반영한 결과를 다시 검토했다. 새 `current` 문서가 Ticket 근거 묶음을 한 파일에 나열하고 상세 문서 링크에 의미 설명을 맡겨, 공통 계약으로 재사용하기 어렵고 주제별 routing·authority도 닫히지 않았다. 이는 기존 계약을 충분히 따르지 않은 적용 문제와, 설치 후 승인된 일부 주제의 Owner를 점진적으로 옮기는 절차가 원천 계약에 명시되지 않은 문제를 함께 드러냈다.

Reference Project README·MAINTENANCE에는 각 내용 문서의 주제별 authority와 승인된 Owner 이동 절차를 추가했다. `update-project-context`와 이식 skill·application contract는 Ticket·Workspace·evidence 묶음이 아니라 지속 주제·판단 질문·수명·갱신 Owner로 문서를 구성하고, `common/current/guidance/decisions`에 나누며, 이전 canonical과 live consumer까지 전환하도록 맞췄다. 확인되지 않은 제품 선택은 계속 열린 판단으로 남기고, 승인 범위 밖 상세 문서 전체 이동은 하지 않는다.

이 문단은 source `7040d1c` 시점의 앞선 단계다. 이후 Noline은 설치본 재적용에 그치지 않고 주제별 구성·읽기 기준과 제품 본문을 여러 차례 수정했다. 후속 commit range와 원천 재반영 결과는 아래 새 상태와 [후속 반영 기록](../records/2026-09-14-02-project-composition-and-reading-integration.md)이 소유한다.

## Project 본문 구성·읽기 계약의 후속 역반영

Source `7040d1c` 이후 Noline commit `26350d6`부터 `30deac5`까지의 문서·기록을 대조했다. 최종적으로 확인된 공통 변화는 물리적인 `common/current/guidance` 경계를 유지하면서도 작업·주제에서 본문을 찾게 하는 routing, guidance를 계약·이유·적용·검증을 포함한 작업 가이드로 보는 책임, 본문 구성과 읽기 기준의 분리, 읽기 전용 `read-project-context`, 갱신 전 의미·사실·진입점 대조와 갱신 후 의미·범위·routing 검증이다.

Reference Project에는 `context/project/REFERENCE/`와 읽기 스킬을 추가하고, Project README·MAINTENANCE·층별 README·갱신 스킬·root routing을 같은 계약으로 맞췄다. 이식 skill과 application contract도 target에서 이 책임들을 함께 설치·적응하고 producer 본문과 consumer route를 일관된 변경 단위로 처리하도록 보완했다. Noline의 통화·날짜·API·도시 검색 같은 제품 내용과 Workspace 002·004의 상태는 가져오지 않았다.

Noline의 첫 독립 재시험에서는 기존 의미 누락·사실 범위 확대·기존 진입점 누락·판단 효용 없는 current 실행 이력이 개선됐다. 그러나 뒤의 별도 실제 구성에서도 같은 네 종류의 문제가 다시 드러나 Main이 최종 문서를 고쳤으므로, 새 계약의 독립 실행 효과는 아직 잠정적이다. 구조·skill·Recover·회귀 검증과 실제 새 target 적용 효과를 구별한다.

변경 Markdown 24개의 local link 258개, 관련 skill 네 개의 YAML shape, 기본·명시 Recover와 전체 Reference 테스트 126개가 최종 통과했다. 첫 전체 테스트에서 기존 descendant timeout timing 시험 한 건이 실패했으나 단독 재실행과 뒤의 전체 재실행 두 번은 통과했다. 공식 skill 검사기는 PyYAML 부재로 시작하지 못해 같은 조건을 Ruby YAML로 대체 확인했다. 실제 host skill 호출과 새 target 이식 효과는 확인하지 않았다.

## Noline Spec·Ticket 실행 기준의 Reference 역반영

사용자가 지정한 Noline 커밋 `d7223b7b6622f625e26f7e7457f6eb1373cf91d9`의 diff, 부모 판본, Ticket 03 최초 범위 재확인과 일반화 후보·fresh-Main 계획 검토를 대조했다. 핵심은 Spec 이름이나 Ticket 크기를 바꾸는 것이 아니라, 결과 달성을 맡긴 Ticket에서 필요한 일을 발견하고 수정 목록이 아니라 실제 결과와 근거로 완료하도록 실행 기준을 보강한 것이다.

Reference의 기존 단일 Spec·Ticket 계약은 Noline 부모와 같은 blob이어서 공통 후속 구조를 적용했다. [새 Spec·Ticket 진입 문서](../../../../reference-project/context/work/workspaces/spec-and-tickets/README.md)가 실행·Spec·Ticket·갱신·이력의 관계를 소유하고, 기존 파일은 호환 안내로 남는다. Root·Work·Workspace·skill 링크, Recover, Maintainer role·자동 grounding, fixture와 회귀 검사를 새 경로에 맞췄다. Noline의 제품별 `002` Workspace 내용과 receipt는 가져오지 않았다.

첫 전체 검사에서는 기존 descendant timeout timing 시험 한 건이 실패했고 단독 재실행은 통과했다. 이후 전체 126개가 통과했으며 명시/기본 Recover와 Reference Markdown 57개의 local link 검사도 통과했다. 실제 제품 Ticket 실행 품질과 host Maintain apply는 아직 이 Reference 반영으로 새로 입증하지 않았다. [반영 기록](../records/2026-09-12-01-noline-spec-ticket-execution-criteria-integration.md)이 근거·범위·검증 상한을 소유한다.

사용자 정정에 따라 Noline commit과 외부 파일명을 유일한 상세 근거 경로로 두지 않도록 바꿨다. Ticket 03 최초 완료·사용자 정정의 최소 원문, 다섯 원기록의 blob, 중간 후보 해시, 일반화 후보의 fresh-Main 계획 검토와 입증 한계를 Reference 폴더의 [내부 근거 snapshot](../../../../reference-project/context/work/workspaces/spec-and-tickets/2026-09-12-NOLINE-EVIDENCE.md)에 보존하고 HISTORY와 output 진입점을 그 기록에 연결했다. Noline의 제품별 현재 상태·전체 Ticket·receipt는 공통 판단 근거와 구별해 복제하지 않았다.

## Workspace 문서 작성 기준 보완과 Maintainer 설정

Reference의 사람용 Workspace 문서 작성 기준을 [DOCUMENT-WRITING.md](../../../../reference-project/context/work/workspaces/DOCUMENT-WRITING.md)로 분리했다. Workspace README는 층의 의미·Owner·보존 경계와 기준의 읽기 경로를, 새 문서는 내용 충분성·이유와 조건의 보존·구성·편집 판단을 소유한다. 서로 다른 판단 조건을 압축해 합치지 않는 기준, 이해·판별에 필요한 구체 사례와 결정 범위의 최소 원문 보존 기준도 기존 문단에 통합했다. Spec·Ticket과 생성·전환 기준, Work 운영 진입점과 Maintainer의 소비 경로는 유지한다.

Noline 03 Ticket 기록을 대조하며 Main의 수동 요약에서 선택 이유가 빠진 사실과 기록의 설명 비중·내용 충분성 문제를 구별했다. 이번 보완은 그 기록 자체를 고치는 작업이 아니라 Reference의 작성 기준을 정비한 것이다. 자동 Maintainer는 정본 파일에서 읽은 본문을 입력으로 받고 같은 파일을 도구로 재독하지 않으며, 본문이 제공되지 않는 수동 경로에서는 직접 읽는다. 현재 구현의 매 응답 계약 본문 주입은 유지한다.

Maintainer 모델은 비교 시험 뒤 사용자가 선택한 Sol high로 설정했다. [역할 설정](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml)이 모델·추론 수준을 소유하고 자동 bridge도 시작·재개마다 같은 값을 명시한다. 기존 thread identity와 read-only·guarded apply 경계는 유지한다. 자동 bridge는 설정을 읽기 위해 Python 3.11 이상이 필요하다.

작성 지침의 최초·후속 입력 단일 포함과 로컬 링크 검사를 마쳤으며, 모델 설정 반영 후 Maintain 테스트 67개와 전체 재실행 126개가 통과했다. 첫 전체 검사에서 Verify 시간 제한 테스트 한 건이 실패한 사실은 [모델 설정 기록](../records/2026-09-11-07-maintainer-model-settings.md)에 보존했다. 이후 작성 지침의 조건·사례·원문 보존 보완 뒤에도 입력 단일 포함과 Maintain 67개 검사를 다시 통과했다. 작성 기준의 책임 분리는 [분리 기록](../records/2026-09-11-06-workspace-document-writing-contract.md), Noline 수정본 대조와 후속 보완 이유는 [압축 기준 보완 기록](../records/2026-09-11-08-writing-conditions-examples-evidence.md)에서 찾는다.

작성 지침·실행 설정·평가 기록은 source `5f6db35`로 커밋했고 Noline에는 `309b9e6`으로 적용·커밋했다. 공통 변경과 적용 기록 16개 파일만 포함했으며, 다른 session이 진행 중인 Ticket 03 코드·테스트·문서는 수정하거나 커밋하지 않았다. Noline Maintain 72개와 전체 Harness 재검사 124개, 구조·로컬 링크·명시/기본 Recover 검사가 통과했다. 기존 Verify timeout 시험의 최초 실패와 단독 재실행 통과도 보존했다. [적용 기록](../records/2026-09-11-13-noline-writing-and-settings-application.md)이 판본·기존 작업 분리·검증 한계를 소유한다. Source의 `.DS_Store`와 평가 Python 캐시는 커밋에서 제외했다.

Ticket 03 논의의 사용자·Main 발화 전문 23개와 새 계약으로 독립 작성 시험을 수행했다. 기존 작성본은 제공하지 않았고 첫 초안도 수정하지 않았다. [최초 Terra high 평가](../records/2026-09-11-09-ticket03-blind-writing-evaluation.md)에서 확인한 내용 부족을 바탕으로, 사용자 요청에 따라 동일 prompt의 Terra xhigh와 Sol medium을 병렬 비교했다. 실제 시작·재개 로그의 모델·effort, 추가 도구 호출 없음과 Noline·Reference 보존을 확인했다.

[두 후보 비교](../records/2026-09-11-10-ticket03-model-comparison.md)에서는 Sol medium의 일부 정확성 개선에도 공통적인 record 내용 부족이 남았다. 이어 사용자가 요청한 [Sol high 추가 시험](../records/2026-09-11-11-ticket03-sol-high-evaluation.md)에서는 Jest 설정 이유, mock·공용 설정의 서로 다른 도입 조건, 사용자 수락 발화와 원문 위치가 살아났다. 전체 표준 단가 환산은 Terra xhigh 약 6.39, Sol medium 약 11.72, Sol high 약 12.57크레딧이었다. 이 사례의 다음 모델 후보로는 Sol high를 우선 권하지만, 디렉터리 선택 비용 누락과 조건부 권장의 강화·전후 검사 기준 약화는 여전히 보완할 점이다.

사용자의 후속 요청으로 Reference 기본값을 Sol high로 변경했다. 작성 지침에는 선택 비용·조건·결정 강도 보존과 문서 간 중복 제거 기준이 이미 있어 이번에는 본문을 더 수정하지 않았다. [채택 기록](../records/2026-09-11-12-maintainer-sol-high-adoption.md)에 변경·검증과 지침 유지 판단을 남겼다. 시험의 어느 초안도 Noline에 반영하지 않았다. 설치 후 Noline의 읽기 전용 Recover는 확인했지만 실제 모델의 Guard apply·host 전체 흐름, 여러 문서 유형의 일반 효과와 반복 실행 안정성은 확인하지 않았다.

Noline에는 앞선 자료 구분 보완 `dac4e60`과 문서 통합 편집 보완 `37c1fc5`가 적용돼 있다. 당시 source 기준과 적용·보호·검증은 [앞선 문서 편집 기록](../records/2026-09-11-04-maintainer-readable-editing-guidance.md)과 [Noline 적용 기록](../records/2026-09-11-05-noline-maintainer-readable-editing-application.md)에서 찾는다. 이전 시험의 상대 링크 Guard 실패와 실제 자동 host 흐름의 전체 검증은 별도 후속 판단으로 남긴다.

## 커밋과 제외 범위

사용자가 양쪽 저장소의 이번 작업을 커밋하되 기존 코드베이스 분석 기록은 제외하도록 요청했다. Noline의 이식·문서 전환·관리 계약 재적용과 Python cache ignore는 `aa2314c` (`feat/noline-context-harness`)로 커밋했다. `.claude/sessions/2026-09-06-codebase-analysis.md`와 같은 이름의 하위 분석 문서 6개는 기존 untracked 상태와 내용을 그대로 유지했다.

이 작업대는 Reference·이식 skill 수정과 010의 선행 조사·011의 적용 및 검증 기록을 함께 커밋 대상으로 고정했다. `.DS_Store`는 제외한다. Noline 커밋 전에 구조 검사와 Recover를 다시 확인했고 선언 125개 snapshot은 fresh였다. Source commit은 이 상태 문서를 포함한 Git 이력에서 확인한다. 기존 source/target 적용 기록의 미커밋 표기는 각 검증·적용 시점의 사실로 보존한다.

## Noline 관리 기준 배치 재적용 완료

사용자가 “재적용까지해”라고 요청해, 수정한 source 판본을 고정하고 기존 target 담당 worker가 현재 이식 skill로 후속 적용을 마쳤다. Project README·관리 계약의 배치와 직접 읽기 경로, 관련 target 기록·정합성을 반영했다. Main은 실제 Noline layer·상세 Owner 보존, 관리 계약·갱신 skill의 source 일치와 bridge·routing을 대조했다. 승인 변경·상태 파일 밖 기존 602개 경로와 Git index도 별도로 재계산해 같음을 확인했다. [재적용 기록](../records/2026-09-10-03-project-management-reapplication.md)이 source 판본과 실제 결과를 소유한다.

직접 구조·local link 226개·skill 연결 검사가 통과했고 Node regular input 113개가 선언 125개에 모두 포함됐다. 최종 Verify `verify-20260910T055624834459Z-835ff0c90b444b908d8943a3d23d2196.json`은 pass다. Main의 후속 explicit/default Recover는 같은 context 경로 15개를 읽고, 새 관리 계약은 자동 입력에 넣지 않았으며 125개 snapshot이 모두 fresh(변경·누락·확인 불가 각각 0)였다. 해당 검증 당시 source와 target은 미커밋이었다. Host activation·제품 리팩토링은 수행하지 않았다.

## Project 관리 기준의 source 배치 수정 완료

사용자가 Noline README에 길게 들어간 관리 기준의 위치를 물은 뒤 우리 레포도 수정하도록 요청했다. Reference의 Project README에는 구조·권위·작업 경계와 읽기 경로를 남기고, 상세 복원·변경·갱신 기준은 같은 Project의 `MAINTENANCE.md`로 옮겼다. Project 갱신 skill과 직접 소비 진입점을 연결하고, 이식 skill도 관리 계약은 해당 위치에 적응하며 이번 실행 결과는 Workspace 기록에 두도록 바꿨다. 이 source 수정 직후에는 Noline 재적용 전이었으며, 위 후속 재적용에서 target에도 반영했다.

이동한 본문 보존 대조, local link 138개와 diff 검사가 통과했다. Skill 표준 검사기는 PyYAML이 없어 실행되지 않았으며 frontmatter 동일성과 Ruby YAML 검사를 확인했다. Reference의 default/explicit Recover는 같은 context 경로 15개를 읽고 관리 문서는 자동 입력에 추가하지 않았다. 기존 sample receipt의 stale는 유지했다. 실제 변경·판단·검증 상한은 [관리 기준 배치 기록](../records/2026-09-10-02-project-management-layout.md)이 소유한다.

## 문서 전환 보완 완료

사용자가 기존 문서의 전환을 끝내지 못하는 이식 skill의 기준을 고치고, 수정한 skill을 새 subagent가 최소한의 배경만 받아 적용해 보도록 요청했다. Main은 이식 scope 안의 기존 문서를 현재 역할로 판단하고 내용 귀속·파일 처리·연결 정합성을 함께 마치도록 skill과 application-contract를 수정했다. Reference 원본은 바꾸지 않았다.

새 worker `noline_document_reapply`는 대화 이력을 상속하지 않고 target 경로·live skill 경로·문서 보완 범위·기존 변경 보존 조건만 받았다. 구체적인 결함 파일이나 처리 답안은 전달하지 않았다. Worker는 옛 `overview.md`·`prd.md`·`architecture.md`를 스스로 전환 대상으로 찾아 내용 귀속과 Git 원문 보존을 대조한 뒤 제거했다. 관련 Project·Workspace 문서와 Verify 입력도 함께 맞췄다. Main은 실제 원문·변경 내용과 최종 실행을 확인해 이번 문서 전환 결과를 회수했다. 정확한 요청·위임 입력·판본과 결과는 [이번 기록](../records/2026-09-10-01-document-transition-reapplication.md)이 소유한다.

직접 구조 검사와 local link 112개 검사, 입력 closure 대조가 통과했다. Main의 최종 explicit/default Recover는 같은 context 경로 15개를 읽었고 마지막 Verify `verify-20260910T035611188866Z-b0ce311e32474001a7ec5423c0f58869.json`을 연결했다. 선언 파일 122개가 모두 fresh이며 변경·누락·확인 불가 각각 0이다. 별도로 보존 대상 591개 경로와 Git index도 동일함을 확인했다. 제품 코드·기존 상세 문서·설치된 skill·runtime·설정은 이번에 바꾸지 않았으며 source의 이식 skill 변경과 target 보완은 미커밋 상태다.

## 직전 적용 결과

Noline 기존 설치의 최신 Reference 보완과 독립 검토를 마쳤다. Worker `noline_apply_resume`이 적용·검증했고 reviewer `noline_review_resume`은 실제 설치본에서 미해결 P1/P2가 없다고 판정했다. Main은 최종 Verify 뒤 기본·명시 Recover, 보호 대상과 변경 경계를 직접 확인해 이번 제한된 이식 결과를 회수했다. 상세 근거는 [완료 기록](../records/2026-09-09-01-upgrade-completion.md)에 있다.

Project common/current/guidance, Spec 다섯 파일·Ticket, Recover·Maintain 계약과 Reference skill 여섯 개를 반영했다. 기존 상세 문서 전체 정비와 제품 리팩토링은 하지 않았다. 기존 Noline 연결과 사용자 untracked 18개 entry를 보존했고, 교체한 이전 memory 세 파일도 원문 바이트를 source에 보존했다.

관련 tests 63개와 최종 전체 tests 122개가 통과했다. 첫 전체 실행의 timeout timing 실패 한 건도 그대로 보존했다. 직접 구조 검사와 최종 Verify가 통과했고 기본·명시 Recover는 같은 context 경로 15개를 읽었다. 마지막 receipt는 `verify-20260909T143800753938Z-1253979b56b74e5b95144fb136861b08.json`이며 Main 확인 시 snapshot 파일 123개가 fresh, changed·missing·unavailable은 각각 0이었다. 이는 선언 입력의 일치와 해당 실행 결과이며 실제 host 동작이나 리팩토링 효과를 증명하지 않는다.

Source는 `main @ 87d21023f6acd8ae709322d48da9851594f9acb0`이며 Reference와 이식 skill은 변경하지 않았다. Target은 `feat/noline-context-harness @ b4ed41f6e4bbae26fd45827b3b9063097a2c1ea4`를 유지한다. Target 변경은 미커밋·unstaged 상태다. 실제 host Maintain은 `activation_pending`이며 실행·활성화하지 않았다.

## 재개와 위임 경위

최초 worker의 변경안은 Main과 별도 reviewer가 검토했으나 중단 후 agent와 임시 준비 폴더가 사라졌다. 재개 시 target tracked/staged가 clean이고 기존 untracked 목록도 그대로임을 확인했다. 새 worker가 fresh preflight와 준비물을 `records/application/`에 보존하고 적용했다. 최초 준비·계획 검토를 설치 검증으로 간주하지 않았다.

사용자의 “너무 많은 제약은 주지말고”에 따라 상세 문서 전체 정비·제품 리팩토링 제외와 기존 작업 보존만 핵심 경계로 전달했다. 파일 구성·전환·조사·검증은 worker가 live skill에 따라 판단했다.

## 다음 행동

지정한 Noline Spec·Ticket 실행 기준과 Project 주제별 Owner 이동·구성·읽기·검증 기준의 Reference 역반영은 완료했다. Workspace 생성 계약과 sample consumer의 Project 선택 설명도 새 읽기 기준과 충돌하지 않게 맞췄다. 새 Reference 판본을 다른 target에 실제 이식해 본 효과와 새 session의 `read-project-context` 발견·호출·본문 적용은 아직 확인하지 않았다. Noline 최종 제품 문서는 Noline이 소유하며 source sample에 복제하지 않는다. 이번 보완을 Project 본문 전체나 제품 문제 전체의 해결로 보고하지 않으며, 제품 리팩토링과 실제 host activation을 자동으로 추가하지 않는다.

실제 skill 호출·Maintain 문서 유지 흐름, 제품 acceptance, 리팩토링 효과 평가와 target Workspace 완료는 아직 확인하거나 수행한 결과가 아니다.
