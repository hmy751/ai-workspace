# 문서 전환 기준 보완과 Noline 재적용

## 요청과 변경

사용자는 지적한 모든 문제를 이식 범위 문제로 묶지 않았으며, 전체 문서 정비를 요구하지 않았다. 이전 이식의 낡은 문서까지 현재 위치에 남기는 것은 이식 skill의 허점이라는 정정이었다. 이후 다음과 같이 실행을 요청했다.

> 그래 그럼 기준 고치고 서브 다시 호출시켜서 시켜봐 스킬 읽게 하고 뭐 다른 상황은 너무 전달하지 말고 필요한것만 그래서 보자고 잘 나오는지

Main은 `.agents/skills/apply-context-harness/SKILL.md`와 `references/application-contract.md`를 수정했다. 계속 쓰는 상세 정본과 이번 이식으로 대체되는 문서의 역할을 구분하고, 후자는 유효한 내용의 현재 위치와 기존 파일 처리·소비 경로까지 함께 전환하도록 했다. 파일 나이나 생성 주체에 따른 일괄 처리는 하지 않으며, 기존 경로 유지에는 현재 책임이나 호환 필요가 있어야 한다. Manifest·실행·완료 조건을 이 기준에 연결했다. Reference 제품 원형, 다른 skill 설명과 실행 환경은 이번 수정에 포함하지 않았다.

수정된 source skill 두 파일의 SHA-256은 [source 입력 receipt](receipts/document-transition/source-input.json)에 있다. Source commit은 `87d21023f6acd8ae709322d48da9851594f9acb0`, Reference는 clean이며 skill 변경은 위 사용자 요청으로 승인된 미커밋 파일이다.

## 새 worker에게 전달한 입력

`noline_document_reapply`를 `fork_turns=none`으로 호출했다. 구체적인 결함 파일명·처리 방식·앞선 Main과 reviewer의 결론은 넣지 않았다. 전달한 원문은 아래와 같다.

```text
대상 `/Users/hammyeong-yeon/Desktop/10_work/noline`의 기존 Context Harness 이식을 보완해 주세요. `/Users/hammyeong-yeon/Desktop/context-harness/.agents/skills/apply-context-harness/SKILL.md`의 현재 파일을 읽고 적용하세요. 이번 범위는 이식에 따른 문서 구성·전환과 직접 연결된 정합성입니다. 제품 리팩토링이나 기존 상세 문서 전체 정비로 넓히지 마세요.

사용자는 이 보완의 실제 적용을 승인했습니다. 필요한 변경안은 Main에게 전달하고, 적용·검증 결과와 남은 판단을 회수해 주세요. 대상의 현재 미커밋 작업을 확인·보존하고, stage·commit이나 host activation은 하지 마세요. 대상의 이번 보완 파일·기록·검증을 담당하며 source 저장소와 이식 스킬은 Main이 담당합니다. 공유 작업 중이므로 다른 사람의 변경을 되돌리지 말고 현재 변경을 수용해 작업하세요.
```

Worker는 target에 존재하는 문서와 기록을 직접 읽을 수 있다. 대화 이력을 상속하지 않았다는 사실을 기존 산출물까지 가린 실험으로 해석하지 않는다.

## 확인 상태

Skill diff의 whitespace와 local link 11개는 통과했다. `quick_validate.py`는 기본·번들 Python 양쪽의 PyYAML 부재로 실행되지 않았다. Ruby의 YAML parser로 frontmatter를 읽어 허용 키·이름·description 길이·미완성 placeholder를 확인했고, Git HEAD와 frontmatter가 동일함도 확인했다. 이 검사를 위해 Project 실행 환경을 변경하지 않았다. 실제 내용 기준은 새 worker의 적용 결과에서 확인한다.

Worker는 fresh preflight에서 target HEAD `b4ed41f6`, branch `feat/noline-context-harness`, staged 0과 변경 104 entries를 고정했다. 이어 root의 `overview.md`, `prd.md`, `architecture.md` 세 문서가 과거 원문 안내만 붙은 채 남았고 현재 역할·호환 consumer가 없다고 스스로 보고했다. 내용 귀속과 Git 원문 보존을 대조한 뒤 세 파일을 제거하고 README·현재 Work 문서·관련 Decision의 후속 관계·Verify 입력을 맞추는 변경안을 제출했다. Main은 사용자 승인 범위에 맞아 진행하도록 했다. 구체 수정 지시는 추가하지 않았다.

## 실제 적용과 Main 회수

Worker는 세 기존 파일의 본문이 Git HEAD와 동일함을 확인하고 유효한 내용을 현재 layer에 귀속시킨 뒤 원래 경로에서 제거했다. 이전 prd의 여행 하나 활성화 조건과 이전 요약의 Network-First 의미는 common 본문에 보완했고, 특정 Work에만 해당하는 상태는 Workspace로 분리했다. Project README·guidance, 해당 Work의 Spec·Ticket·state·output, Decision의 후속 관계와 Verify 입력을 맞췄다. 새 제품 결정이나 기존 상세 문서 전체 정비는 하지 않았다.

Main은 Git의 원문 세 개, 준비 diff와 실제 common/current/guidance, 새 적용 기록을 직접 대조했다. 이번 문서 전환 범위에서 내용 귀속·기존 파일 처리에 추가 수정할 문제는 발견하지 못했다. 이 회수 판단은 worker가 최종 문서와 Verify를 만들기 전에 전달했다. 앞선 배경이나 답안을 더 전달해 처리 방식을 유도하지 않았다.

직접 구조 검사와 최종 local link 112개 검사가 통과했다. Node가 읽는 regular input 110개는 선언 basis+evidence 122개 안에 모두 포함된다. 최종 Verify는 `verify-20260910T035611188866Z-b0ce311e32474001a7ec5423c0f58869.json`이며 pass다. Main이 이후 explicit/default Recover를 직접 실행해 같은 context 경로 15개와 해당 cursor, snapshot 122개 전체 fresh·변경/누락/확인 불가 각각 0을 확인했다. 별도로 수정 대상 밖 baseline 591개 경로의 kind·hash와 실제 Git index 파일 SHA-256이 그대로임을 확인했다.

- [Noline 실제 적용 기록](/Users/hammyeong-yeon/Desktop/10_work/noline/context/work/workspaces/001-noline-context-harness-application/records/2026-09-10-01-document-transition.md): 내용 귀속과 target 검증 증거의 진입점.
- [Main 최종 확인](receipts/document-transition/main-review.json): 최종 Recover와 보존 대조 결과.

실행 의미는 바꾸지 않았으므로 전체 Harness tests나 별도 reviewer를 다시 호출하지 않았다. 제품 코드·기존 상세 문서·설치된 skill·runtime·설정, Git branch·index를 유지했고 stage·commit·host activation은 하지 않았다. 2026-09-09 기록은 당시 실행 증거로 유지한다.

이번 재적용에서는 최소 위임 입력으로도 worker가 대체 문서와 영향 범위를 찾아 전환을 끝내는 결과를 관찰했다. 기존 target 문서·기록에 접근할 수 있었으므로 이를 모든 상황에서의 skill 효과 증명으로 확대하지 않는다. Project 본문 전반의 내용 충분성, Workspace 생성 skill의 설명과 Python cache 문제는 이번 결과로 모두 해결했다고 보고하지 않는다.
