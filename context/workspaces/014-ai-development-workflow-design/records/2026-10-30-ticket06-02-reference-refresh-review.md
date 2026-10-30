# 06-02 — 보완된 Reference와 Noline 고유 기준의 재대조

후속: 사용자가 이 적용안의 반영을 승인해 [Noline 부분 적용과 확인](2026-10-30-ticket06-02-noline-partial-application.md)을 마쳤다. 아래는 반영 전 검토 당시의 판단이다.

**결론:** 기존의 독립 묶음·좁은 병합·옛 경로 호환 방향을 유지한다. 최신 Reference의 코드 표현·진단, 이름·완료, 공통화·오류 계약 보완과 본문 형식을 적용안에 포함한다. Noline 자체의 제품·개발 기준과 더 구체적인 Project 관리 기준은 보존한다. 이번 결과는 적용안의 재점검이며 **Noline에는 아직 쓰지 않았다.** Maintain·Work 기록/전환 계약·host 통합 테스트는 계속02가 맡는다.

사용자 요청:

> 그럼 이제 06-02로 돌아가서 이번에 보완한 Reference 기준으로 Noline 적용안도 다시 점검해보자. 기존 Noline 고유 기준도 확인하면서, Maintain 관련은 계속 02에 두고.

## 이번 기준판과 실제 확인 범위

| 대상 | 확인한 상태 |
| --- | --- |
| Reference | `f5082bc30ab3470a3e3a4a895cfcb6cb50b3af81`. Reference 안의 미커밋 변경 없음. 첫 적용 `e38ce52b`, 품질 보완 `19225e0d`, 형식·이름 보완 `02ea702c`, 공통화·오류 계약 보완 `f5082bc3`를 함께 받는다. |
| Noline | `main @ 4fb309d2ba50afaca44019879d7161964b9b2328`. 추적·스테이징 변경 없음. 이전 적용안과 동일한 판본이다. |
| 보호 상태 | 기존 계획141개 경로의 변경 전 상태와 범위 밖 tracked954개가 모두 이전 관찰과 같다. 전체 tracked980개와 untracked976개는 이번 조사 전후 해시·kind 대조에서도 동일했다. `.pnpm-store/`·`artifacts/`의 untracked976개는 별도 preflight에 고정했다. |
| 범위 | 실제 Noline의 root·Project 관리/구성/읽기·제품별 가이드·스킬/bridge·검사기와 옛 경로 소비자를 읽었다. 관련 fetcher 구현은 문서의 대상과 사례 차이를 확인하는 범위로 읽었으며 제품 동작을 시험하지 않았다. |

[첫 적용안](2026-10-29-ticket06-02-noline-preflight-and-plan.md)과 당시 JSON은 역사적 관찰로 보존한다. 최신 경로·source 해시·target 변경 전 상태·적응 메모는 [갱신한 계획 JSON](receipts/noline-reapplication/2026-10-30-phase1-plan-refresh.json), 새 관찰 원본은 [preflight](receipts/noline-reapplication/preflight-20261030T053910705923Z-40bbe8ecaefa4b9789f292859838082c.json)에 있다. 임시 원본과 보존본의 SHA-256은 같다. 이 자료는 최종 patch, 적용 승인이나 설치 결과가 아니다.

## 이전 적용안에서 달라지는 것

이전 source `a26d2f95` 뒤 Reference 변경은27개 경로다. 아래 분류로 모두 대응한다.

| 변경 묶음 | Noline 적용안 |
| --- | --- |
| 기존 계획에 들어 있던 source10개 수정 | Personal·개발 안내, 이름·완료, 공통화, 계약·수명과 관련 형성 맥락·context 배경 안내의 해시를 최신판으로 바꾼다. 사례와 주제 background를 형식 때문에 다시 쓰지 않는다. |
| 새 코드 표현 주제5개 | `context/personal/development/code-expression/`의 본문·안내·형성 맥락·근거를 추가한다. 중괄호·개행·배치·주석·진단의 판단과 제품 계약/도구 설정의 경계를 함께 가져간다. |
| 본문 형식과 형성 자료7개 | `context/WRITING-FORMAT.md`와 `_background/writing-format/`의6개 문서를 추가한다. 이름 본문의 강도 보정과 공통화·오류 계약의 부분 대조 기록도 포함된다. |
| 진입·구성3개 | Reference `AGENTS.md`의 연결은 Noline 원본 `CLAUDE.md`에, context 안내와 Project composition 연결은 각각 기존 Noline 본문에 좁게 병합한다. |
| Reference 자체 반영 기록2개 | Noline 적용 결과로 복사하지 않는다. 원래 Reference 기록은 source의 근거로 연결하고 Noline에서 실제 수행한 결과는 해당 Workspace에 남긴다. |

계획은 **153개 경로**다. 새 본문·스킬·지원 자료121개, 기존 파일의 제한된 수정26개, 새 bridge2개, 실제 적용 시 만들 기록·관찰 사본4개로 구성된다. 이전141개보다12개 늘었으며 삭제 계획은 없다. 날짜가 들어간 신규 결과 기록은 이번 계획의 예약 경로이고 실제 적용일이 달라지면 실행 전에 맞춘다. 이 수치는 설치 수나 테스트 수가 아니다.

Reference의 형식 도입 자료는 형성 경위를 설명하고, Noline의 적용 기록은 실제 반영을 설명하도록 첫 안내와 링크를 적응한다. source에 남은 외부 형성 링크5개는 모두 실제 원자료가 존재한다. 복사 위치에서 잘못 해석되지 않게 원자료 절대 경로·source 판본으로 연결하며, 새 실행 의존이나 현재 Noline의 관찰 결과로 바꾸지 않는다. 필요한 핵심 발췌는 기존 가까운 형성 자료에 유지한다.

## Noline에서 그대로 보존할 기준

| 현재 Owner와 기준 | 최신 Reference와 함께 적용하는 판단 |
| --- | --- |
| [root 핵심 불변식](</Users/hammyeong-yeon/Desktop/10_work/noline/CLAUDE.md>): Selective Local-First, Activation Router와 Service Layer의 구별, transaction+queue, client ID, schema·인증·소유권 | Personal은 이 제품 계약을 검토하는 관점이다. 계약을 대체하거나 구현 변경을 이번 설치에 포함하지 않는다. 날짜의 세부 의미는 이미 연결된 Project 본문에서 확인한다. |
| [Form](</Users/hammyeong-yeon/Desktop/10_work/noline/.claude/context/form.md>)·[Component](</Users/hammyeong-yeon/Desktop/10_work/noline/.claude/context/components.md>)·[UI guide](</Users/hammyeong-yeon/Desktop/10_work/noline/packages/ui/CLAUDE.md>): React Native Controller·Field 조합, hook/data의 부작용, domain-free primitive와 app composition | 새 공통화 표는 이 기본 구성을 없애라는 요구가 아니다. 함께 필요한 형식은 제공하고 실제 차이가 필요한 사용처를 구별한다. 예제의 web 입력·Hook 구조를 Noline에 복사하지 않는다. |
| [API 계약](</Users/hammyeong-yeon/Desktop/10_work/noline/context/project/guidance/api-contracts.md>): request/response 검증·serializer·ownership, 일반 조회와 sync의 삭제 처리 차이 | 새 오류 본문은 실패 단계·상태·전달 의미를 대조하는 기준이다. Noline의 Axios `APIError`, `AuthRequiredError`와 React Query/UI 책임을 fetch 예제로 교체하지 않는다. 오류 클래스 개수·재시도·await 추가를 의무화하지 않는다. |
| 같은 API 가이드의 열린 서버 오류 정책: `AppError + errorHandler`와 일부 Data route의 `try/catch + sendInternalError` | 아직 어느 구조를 서버 전체에 채택할지 결정하지 않았다. Personal 추가나 형식 정리로 이 미정을 닫거나 catch를 일괄 없애지 않는다. |
| [동작 보존 리팩터링](</Users/hammyeong-yeon/Desktop/10_work/noline/context/project/guidance/behavior-preserving-refactoring.md>): 관찰 가능한 결과·부작용·부분 실패·최신성, 동작 보존과 개선 효과의 별도 확인 | 최신 품질 본문과 양립한다. Noline 사례·위험별 검증·native/DB/auth의 확인 상한을 유지한다. 새 Personal을 이유로 이 제품별 기준을 중복·낡은 문서로 제거하지 않는다. |
| [TypeScript/Zod](</Users/hammyeong-yeon/Desktop/10_work/noline/.claude/context/typescript.md>): type 기본값, import 순서, Boolean/handler/상수 표기, 중괄호, console.log 금지 | 실제 제품 규약을 보존한다. Personal의 ‘console 전면 금지를 이 기준만으로 요구하지 않는다’는 문장이 이미 존재하는 Noline의 더 엄격한 규칙을 해제하지 않는다. formatter·lint 설정도 변경하지 않는다. |

**남겨 둘 오해 가능성:** TypeScript 가이드의 비동기 예시는 catch·로그·null 반환을 좋은 예, 직접 Promise 반환을 나쁜 예로 대비한다. 이를 모든 비동기 함수의 의무로 읽으면 Expense API의 오류 전파 계약과 충돌할 수 있다. 같은 문서의 중괄호 없는 예시도 명시된 중괄호 규칙과 맞지 않는다. 이는 이번 설치에서 새로 발생한 코드 결함이나 검증된 실행 실패가 아니다.

이번 적용안에서는 Noline Personal 안내에 실제 TypeScript·폼·API Owner로 가는 조건부 연결을 보강한다. API 오류 반환·전파는 구체적인 API 계약과 해당 구현에서 확인하고, 일반 예제만으로 null 반환이나 매 catch 로그를 도입하지 않는다. 기존 제품 가이드의 예시 정비와 서버 오류 정책 선택은 이번 payload 밖이며, 제품 가이드 자체의 의미를 바꾸려면 해당 범위를 별도로 다룬다.

## Project 작성·읽기·관리 문서는 Noline 본문에서 병합한다

새 Reference로 파일을 교체하면 Noline이 이미 보강한 구체적인 판단과 사례가 빠진다. 세 문서의 실제 차이를 대조해 다음처럼 좁힌다.

| 문서 | 병합할 변경 | 보존할 Noline 내용 |
| --- | --- | --- |
| `context/project/REFERENCE/composition.md` | CONTENT-POLICY 연결, 형식 문단에서 WRITING-FORMAT의 적용 범위를 따라 선택하도록 연결 | API·Schedule/Expense·일반 조회/sync·날짜 경계 사례, 의미를 문장별 layer로 흩뜨리지 않기, current의 추가 판단 가치·재확인 조건·갱신 비용, 제품 언어로 열린 범위 설명하기 |
| `context/project/REFERENCE/reading.md` | 별도 읽기 스킬 대신 USAGE를 공통 읽기 방법으로 연결하고 관련 절·표현만 조정 | API에서 날짜 의미로 질문이 달라질 때 읽기를 넓히는 예, 기존 runbook/guide에서도 같은 Owner에 도달하는지 확인, 코드와 문서의 권위·충돌 대조, Recover와 Work Owner의 경계 |
| `context/project/MAINTENANCE.md` | 공통 내용 관리 연결, update-project-context 호출을 context-update의 Project 범위로 연결 | form/request/local/server를 각각 확인, helper/API/날짜 변경별 영향 예, Owner 이동 전후 의미 대조, 기존 진입과 Workspace 선택 이유, current의 가치/비용, 제품·machine·Maintain 쓰기 권한 한계 |

본문 형식은 조건과 할 일을 찾기 쉽게 만드는 기준이다. 모든 제품 설명·현재 구조·사례·스킬을 표로 바꾸거나 Noline 기존 본문을 전수 재작성하는 계획이 아니다. Work는 현재 적용 대상에서 제외한다.

## 스킬·호환·제외 범위 재확인

스킬 원본은 Noline의 `.claude/skills/`, Codex 연결은 `.agents/skills/`의 상대 symlink로 유지한다. `context-update`·`explain`과 공통 기준·관리 정책을 추가하되 별도 `.codex/skills/`는 만들지 않는다. root와 harness의 ‘얇은 dispatcher만 소유’라는 설명은 호출·수행 방법과 제품 정책의 책임을 구별하도록 한정해서 조정한다. report-only agent의 권한은 유지한다.

옛 읽기·갱신·두 설명 스킬은 실제 경로를 남기고 새 본문을 안내하는 호환 진입으로 전환한다. 독립 실행 본문을 두 벌 유지하지 않으며 자동 선택은 끈다. 기존 설명 기준 파일도 shared 원본으로 이어지는 regular-file 안내로 남긴다. Noline001 `verify.json`의 evidence와09월14일 Decision,004 output이 이 경로들을 소비하는 사실을 다시 확인했다. 이 과거 입력·기록을 역수정하거나 단순 삭제하지 않는다.

기존 검사기는 두 스킬과 새 비스킬 항목만 정확히 추가한다. 기존 bridge·agent·Maintain·링크 검사를 통째로 완화하지 않는다. `start-app`, deprecated `noline-work`, 기존 생성·재판단·work-discussion의 역할은 유지하며 work-discussion은 공통 기준 링크만 바꾼다.

Maintain 코드·role·hook·설정·activation·수집기·ignored runtime, Recover/Verify 구현과 machine JSON·receipt·active index는 그대로 둔다. development·새 work-discussion·create 적응·improvement-loop의 실행 연결은02 결과와 함께 판단한다. 제품 코드·테스트·제품 가이드와 기존 artifacts도 변경 대상이 아니다. 실제 반영의 기록은 기존 Noline001에 남기되 Work 구성·담당 계약을 재설계하지 않는다.

## 확인 결과와 실제 반영 때의 확인

이번에는 source 차이27개 경로를 빠짐없이 분류하고, 예정153개 경로의 기존 상태·ancestor·ignore와 source 해시를 대조했다. 새 파일 충돌·ancestor symlink 충돌·ignore 충돌은 없었다. 갱신한014 문서8개의 로컬 링크678개에서 누락 경로가 없었고, 기존02 등 이번 수정 밖의 병렬 파일은 시작 시점과 동일했다. source가 있는 추가/적응 문서는 현재 Reference의 해시로 고정했다. 실제 병합 결과의 최종 바이트는 아직 만들지 않았으므로 최종 target 링크·본문 보존 검사를 통과했다고 쓰지 않는다.

10월29일의 Recover001/default·002 성공과 기존 링크8건 실패는 당시 증거로만 이어받았다. 이번에는 Recover·검사기·제품·host 테스트를 다시 실행하거나 session runtime metadata를 열지 않았다. 현재 active index가001임은 읽어서 확인했다. 과거에002로 이어진 binding 관찰은 실행 생존의 증명이 아니며 실제 반영 직전에 live consumer를 다시 확인한다.

실제 반영에서는 다음을 확인한다.

1. source/target 판본·미커밋 변경과 계획 경로를 다시 고정하고, Noline 문서에 좁은 patch를 만든다. 새 본문이 생긴 뒤 진입을 전환한다.
2. 원래 판단·조건·강도, 위 Noline 고유 기준, 제품·Work·Maintain·기존 사용자 파일의 보존을 대조한다. 형식의 ‘할 수 있다’를 의무로 바꾸지 않는다.
3. 추가/수정 Markdown의 경로·앵커, frontmatter·호출 설정, 원본/bridge와 옛 호환 진입, 자체 점검기의 정확한 항목을 확인한다. 과거 링크8건과 새 실패를 구별한다.
4. 기본001과 실제로 확인된 live consumer의 explicit/default Recover를 읽기 전용으로 대조한다. 새 Personal·관리 정책을 모든 recover.json 입력에 넣지 않으며 machine receipt를 새 성공·fresh로 바꾸지 않는다.
5. 실제 발견·호출·중복 표시·설명·맥락 갱신·Work 재개까지의 통합 확인은02로 연결한다. 제품 acceptance·Noline 커밋·push·Workspace 완료를 이번 검토로 대신하지 않는다.

이번 요청의 결과는 최신판 적용안과 Noline 보존·병합 판단이다. 다음 단계는 이 구체안에 따른 실제 반영이며, 아직 시행하지 않았다.014에서는06-02의 현재 진입과 이 기록만 갱신하고 병렬02의 문서·합의는 유지한다.
