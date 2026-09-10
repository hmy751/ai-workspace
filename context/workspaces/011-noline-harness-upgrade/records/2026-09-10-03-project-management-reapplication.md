# Noline Project 관리 기준 배치 재적용

사용자는 source의 README·관리 계약·이식 및 갱신 skill 수정 완료 보고 뒤 “재적용까지해”라고 요청했다. 직전 변경을 Noline에 적용하는 승인으로 받아 기존 target 담당 worker에게 현재 이식 skill을 읽고 재적용하도록 맡겼다. 새로운 제품 결정이나 사용자 변경 충돌은 이번 승인에 포함하지 않는다.

Source는 `main @ 87d21023f6acd8ae709322d48da9851594f9acb0`에 이번 사용자가 요청한 미커밋 변경을 더한 판본이다. [파일별 SHA-256](receipts/project-management-reapplication/source-input.json)과 [새 파일을 포함한 diff](receipts/project-management-reapplication/source.diff)를 적용 전에 고정했다. 직전 source 설계 변경의 이유와 검증은 [배치 수정 기록](2026-09-10-02-project-management-layout.md)이 소유한다.

## 위임과 책임

기존 `noline_document_reapply` worker에게 target 경로, 현재 이식 skill, source 변경의 재적용 범위와 승인, 기존 작업 보존을 전달했다. 이번에는 새로운 최소 맥락 실험이 아니라 같은 담당자의 후속 적용이다. Worker는 fresh preflight·manifest와 실제 target 변경·기록·검증을 맡고, Main은 source 판본 고정·결과 판단·이 작업대의 기록을 맡는다.

Target는 `/Users/hammyeong-yeon/Desktop/10_work/noline`이다. 관리 기준의 배치와 직접 소비 연결을 적용하며 제품 리팩토링·host activation·stage·commit으로 확대하지 않는다. 관리 계약은 Project가 소유하고 이번 실행 결과는 이식 Workspace가 소유한다.

## 적용과 최종 회수

Target에 재적용을 완료했다. Project README의 실제 Noline layer·상세 Owner는 보존하고 상세 기준을 `context/project/MAINTENANCE.md`로 옮겼다. README는 96줄에서 68줄로 바뀌었다. Source의 root 관리 진입 역할은 Noline의 기존 CLAUDE·context 진입점에 적응했고, 갱신 skill·skill 색인·Work 및 Workspace 문서의 직접 소비 연결을 맞췄다. 이전 문서 전환 결과는 기존 적용 기록에 남아 있다.

구체 manifest는 문서·machine 선택 이유·검증 입력·기록과 원본 보존을 포함한 21개 경로를 제시했다. Verify는 별도로 status와 새 receipt를 생성했고 직접 검사 증거는 같은 application receipt 폴더에 남겼다. 기존 Recover의 Project 선택 목록은 유지하고 새 regular Markdown 3개를 Verify evidence에 추가했다. Claim·basis·argv·실행 제한은 유지했다.

Worker는 fresh preflight에서 기존 변경 113개 entry를 관찰하고 별도로 기존 tracked/non-ignored 618개 경로를 고정했다. Main은 manifest·주요 patch와 실제 target README·관리 계약·갱신 skill·bridge·routing을 직접 대조했다. 승인 변경과 Verify 상태 파일을 제외한 기존 602개 경로의 kind·hash와 Git index hash가 그대로였다. 관리 계약과 갱신 skill은 승인된 source bytes와 일치했다. [Main 검토](receipts/project-management-reapplication/main-review.json)에 별도 확인 결과를 보존했다.

직접 구조 검사와 local link 226개, skill 연결 검사가 통과했다. Worker가 관찰한 Node regular input 113개는 선언 basis+evidence 125개에 모두 포함됐다. 최종 구조 Verify는 `pass`이며 receipt는 `verify-20260910T055624834459Z-835ff0c90b444b908d8943a3d23d2196.json`이다. Main도 후속 explicit/default Recover를 실행해 같은 context 경로 15개, MAINTENANCE의 자동 입력 제외, snapshot 125개 모두 fresh와 변경·누락·확인 불가 각각 0을 확인했다. [Main의 최종 Recover](receipts/project-management-reapplication/main-final-recover.json)에 실제 결과를 보존했다.

Target의 [재적용 기록](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/001-noline-context-harness-application/records/2026-09-10-02-project-management-contract.md)에서 exact manifest·source/preflight 보존본·직접 검사·입력 closure·최종 Recover를 찾는다. 구조와 선언 snapshot의 확인이며 실제 host discovery·호출·문서 유지나 제품 acceptance를 증명하지 않는다. Stage·commit·host activation·제품 리팩토링과 Workspace 완료는 수행하지 않았다. 이번에 승인한 관리 기준 배치 재적용의 필수 작업은 끝났다.
