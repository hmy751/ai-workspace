# 06-02 Noline 재적용 — 현행 대조와 첫 적용안

**최신 적용안:** 2026-10-30 [Reference 보완·Noline 고유 기준 재대조](2026-10-30-ticket06-02-reference-refresh-review.md)에서 source `f5082bc3` 기준으로 계획을 갱신했다. 아래141개 경로·판본·실행 결과는 당시 관찰로 보존한다.

**2026-10-30 후속:** [Reference 품질 보완 반영](2026-10-30-ticket06-01-personal-quality-update.md)으로 source에 변경이 생겼다. 아래 판본·141개 경로 계획과 JSON은10월29일 관찰 그대로 보존한다. 다음 Noline 적용 전 새 Personal·관련 진입/기록을 포함해 계획을 갱신해야 하며, 이 문서를 최신 payload 확정이나 적용 승인으로 읽지 않는다.

06-01에서 실제 반영한 Personal·Project 관리·읽기·한정 갱신·설명 묶음은 Noline에도 적용할 수 있다. 다만 Noline의 스킬 원본 위치, 자체 보완한 Project 기준, 옛 경로를 소비하는 검증·기록은 보존해야 한다. 이번 문서는 **적용 전 검토안**이다. Noline 파일은 수정하지 않았고, 스킬 호출·Maintain 활성화·제품 검증·커밋도 하지 않았다.

사용자 요청은 “그래 그럼 06-02 진행해보자”다. 앞서 정한 Maintain·Work 기록/전환과 통합 테스트의02 책임을 유지하면서, 전달 가능한 첫 묶음부터 대조했다.06-01 전체 완료나02 완료를 기다려야만 현행 대조를 시작할 수 있는 것은 아니다.

## 판본과 보호할 상태

| 대상 | 확인한 상태 |
| --- | --- |
| Source | ai-workspace `a26d2f954099f4db50f9109f416d59fafa657402`. 실제 첫 적용은 `e38ce52b`. `reference-project/`에 미커밋 변경 없음. |
| 이전 공통판 | `e38ce52b^`의 Reference와 현재 Noline을 대조했다. Work 논의·재판단·작업물 설명·설명 복구 본문과 설명 공통 기준은 같은 바이트였다. |
| Noline | `/Users/hammyeong-yeon/Desktop/10_work/noline`, `main @ 4fb309d2ba50afaca44019879d7161964b9b2328`. tracked·staged 변경 없음. |
| Noline 자체 변경 | `33bde33` 등에서 Project 구성·관리·읽기 기준을 보완했고 `ee1c005`에서 start-app을 추가했다. 이전 이식판이나 현재 Reference로 통째로 덮어쓰지 않는다. |
| 기존 untracked | `.pnpm-store/`, `artifacts/`. Preflight의976개 dirty entry는 이 두 디렉터리 아래의 개별 경로이며 이번 payload와 겹치지 않는다. |
| ignored 운영 자료 | `evidence-collector/`, `.claude/settings.local.json`, `.codex/maintain-runtime/` 존재 확인. 변경·삭제·활성화하지 않는다. ignored 전체를 조사한 것은 아니다. |

[경로별 계획·해시·보호 목록](receipts/noline-reapplication/2026-10-29-phase1-plan.json)에 계획141개 경로와 그 밖의 tracked954개 경로를 남겼다. 추가·적응109개, 기존 수정26개, 연결2개, 적용 기록4개다. 추가 예정 경로의 기존 파일 충돌, ancestor symlink 충돌, ignore 충돌은 없었다. 숫자는 계획의 파일·연결 수이며 설치 완료 수가 아니다.

[원본 preflight](receipts/noline-reapplication/preflight.json)는 helper가 `/private/tmp`에 만든 관찰 결과와 동일한 바이트다. 이는 atomic snapshot·저자·ignored 전체를 증명하지 않는다. 실제 반영 직전에 source와 target 판본, 계획 경로의 해시·kind·동시 변경을 다시 대조한다. 실제 적용 시 target001의 source에 같은 receipt를 보존하고 적용 기록은 Noline을 정본으로 둔다.

## 유지·교체·추가의 구체적인 선택

| 책임 | Noline 적용안 | 유지할 의미와 이유 |
| --- | --- | --- |
| Personal | Reference의 `context/personal/` 본문·사례·형성 자료를 추가한다. | 기존 target에 같은 경로가 없다.014·과거 Noline 경험의 출처·조건·열린 후보 지위를 유지한다. 새 Noline 실행에서 관찰한 경험으로 바꾸지 않는다.01-02 미채택 제안은 포함하지 않는다. |
| 공통 읽기·문서 관리 | `context/USAGE.md`, `CONTENT-POLICY.md`, `SYSTEM-GUIDANCE.md`와 필요한 `_background/`를 추가한다. | root·context·Project 입구에서 연결한다. Work 기록 담당과 생성/전환은 현행이다. Reference 전용 적용 기록은 그대로 복사하지 않고 Noline의 선택·한계를 별도 기록한다. |
| Project 관리 | 기존 `MAINTENANCE.md`, `REFERENCE/{README,composition,reading}.md`, Project README에 새 공통 읽기·내용 관리·context-update 연결만 병합한다. | Noline의 form/request/local/server 경계, API·날짜 사례, 의미 보존·기존 진입 대조·갱신 비용 기준을 유지한다. common/current와 제품별 guidance·decisions 본문은 그대로 둔다. |
| 한정 갱신·설명 | `.claude/skills/context-update/`, `explain/`을 원본으로 추가한다. | Reference의 `.agents/skills/` 원본 배치를 복사하지 않는다. Noline의 `.agents/skills/{context-update,explain}`은 기존과 같은 상대 symlink로 만든다. `.codex/skills/`는 추가하지 않는다. |
| 스킬 공통 기준 | `.claude/skills/shared/explanation-and-evidence-criteria.md`, `SKILLS-CONTENT-POLICY.md`와 형성 자료를 추가한다. | 스킬 색인·work-discussion·explain에서 실제 원본을 읽는다. Project 제품 기준과 스킬 수행 방법을 구별한다. |
| 기존 네 스킬 | read-project-context는 USAGE·Project 읽기 기준, update-project-context는 Project 범위의 context-update, work-artifact-briefing·explanation-recovery는 explain을 안내하는 호환 진입으로 바꾼다. | 옛 SKILL.md 경로와 bridge는 남기되 독립 실행 본문을 유지하지 않는다. 호출 설정은 자동 선택을 끄고 설명·기본 prompt도 대체 경로를 안내한다. 실제 host의 중복 노출·선택 효과는02에서 확인한다. |
| 옛 설명 기준 경로 | `context/project/guidance/explanation-and-evidence-criteria.md`를 새 shared 원본으로 연결하는 호환 안내로 바꾼다. | 현재 본문은 한곳만 소유한다. 과거 기록·검증 설정에 남은 regular-file 경로를 갑자기 없애지 않는다. |
| 기존 실행·제품 장치 | create-context-workspace, reconsider-work, start-app, deprecated noline-work, report-only agent를 유지한다. work-discussion은 shared 기준 링크만 바꾼다. | 명시 호출 조건과 기존 권한을 유지한다. 제품·rules·guards·runbooks·깊은 context를 새 Personal로 대체하지 않는다. |
| 자체 점검기 | `scripts/check-harness.mjs`의 스킬 목록에 두 새 원본·bridge를 추가하고 shared·정책·형성 자료를 비스킬 항목으로 구별한다. | 기존 bridge·agent parity·Maintain 설정·링크 검사를 유지한다. 새 부속 자료를 허용하려고 임의 디렉터리를 모두 허용하거나 기존 실패를 숨기지 않는다. |

### Noline에 별도 적응이 필요한 이유

Noline root와 `.claude/harness/README.md`는 스킬을 얇은 dispatcher로 설명한다. 새 스킬은 읽을 문서 안내뿐 아니라 공통 수행 방법도 소유한다. 따라서 이 두 진입의 설명을 **스킬은 호출·수행 방법, 제품 정책과 지속 맥락은 해당 문서 Owner**로 맞춘다. report-only agent를 쓰기 주체로 바꾸거나 제품 정책을 스킬로 옮기지 않는다. 변경 이유는 `.claude/decisions/2026-10-29-context-and-explanation-refresh.md`에 남긴다.

Reference처럼 옛 스킬을 바로 삭제하지 않는 이유는 실제 소비 경로가 남아 있기 때문이다. Noline001의 `verify.json`은 옛 스킬·설명 기준 regular file을 evidence로 선언하고, 2026-09-14 Decision과004 output은 옛 읽기·갱신 경로로 연결한다. 지금 삭제하면 이 경로와 기존 검증 입력이 끊긴다. 이번에는 얇은 호환 진입을 두고 machine JSON과 과거 기록은 유지한다. 호환 진입의 제거 시점은02 이후 검증 입력·역사 링크·실제 호출을 함께 전환할 때 판단한다. 영구적인 중복 구현을 채택하는 것은 아니다.

## 실제 수정 범위와 제외

기존 파일 수정은 root `CLAUDE.md`, `.claude/{README.md,harness/README.md,skills/README.md}`, context·Project 진입과 관리 기준, work-discussion의 공통 기준 링크, 네 옛 스킬의 본문·호출 설정, 자체 점검기, Noline001의 state·output·records 색인·source 색인으로 한정한다. 새 파일과 exact path는 위 JSON에 전부 나열했다. 계획에는 삭제 경로가 없다.

새 Workspace를 만들지 않는다. Noline001은 원래 “기존 설치를 최신 Reference로 보완하는 같은 작업”을 소유하므로 실제 적용 결과·보존·검사·후속은 그 current와 기록에 남긴다. 목표·제약은 이번 맥락·설명 갱신이며 제품 개발 Ticket을 착수하지 않는다.014에는 공통/대상 차이와 선택 근거만 연결한다.

아래는 이번 적용에서 제외한다.

- Maintain 코드·role·hook·설정·wrapper·session binding과 ignored runtime, 증거 수집기 연결.
- Recover·Verify 코드, 모든 Workspace의 machine JSON·receipt·status·active index. 기존 Verify를 새 성공·fresh로 만들지 않는다.
- development·새 work-discussion·create 적응·improvement-loop 활성화와 Work 본문 재편.02에서 기록·전환 계약을 연결한 뒤 판단한다.
- 제품 코드·테스트·app/package 지침·제품별 Project 본문, 기존 untracked 산출물, 전역 설치·배포·자동 동기화.
- 별도 host 통합 테스트, 앱 실행, Noline 커밋·push·제품 acceptance·Workspace 완료.

## Live consumer와 직접 확인

현재 default index는001이다. `.codex/maintain-runtime/*/session.json`만 읽어 current generation의 binding을 확인하니002에 연결된 metadata7개, current generation이 없는 metadata8개였다. session id·thread id·prompt·response는 복제하지 않았다. 이는 보존된 연결 정보이며 실행 프로세스 생존이나 현재 host 동작의 확인은 아니다. Claude 별도 runtime 디렉터리는 없고 다른 저장 위치의 부재까지 주장하지 않는다.

따라서 이번 읽기 경로 변경에서 최소 대조할 소비자는 **001(default와 적용 작업),002(persisted binding)**다. 실제 반영 전에 metadata를 다시 확인하고 새 소비자가 있으면 대조 범위에 포함한다.004는 이번 관찰에서 active/default 또는 current-generation binding으로 확인되지 않았으므로 과거 current·output을 역수정하지 않는다. 남아 있는 옛 링크는 위 호환 진입으로 해석된다.

적용 전 read-only Recover 결과:

- 001 explicit과 default: 동일한 loaded context15개. 기존 receipt는 `stale`이며125개 snapshot 중49개 변경, 누락0개다.
- 002 explicit: loaded context20개. receipt는 `not_applicable`이다.
- 선택된 Project 본문은 유지한다. 새 Personal·정책·관리 기준을 `recover.json`의 자동 입력으로 추가하지 않는다.

기존 `node scripts/check-harness.mjs`는 **끊어진 링크8건으로 실패**했다.002·003의 source/records와003의 Map Search Ticket에서 예전 코드 경로를 가리킨다. 정확한 출력은 위 계획 JSON에 보존했다. 변경 전에 존재한 실패이며 이번 이식을 이유로 역사 원문을 다시 쓰거나 실패를 검사에서 제외하지 않는다.

적용 뒤에는 바뀐 진입·스킬의 local link와 anchor, frontmatter·호출 설정, source와 bridge의 실제 목적지, 기존 내용 보존을 검사한다. 자체 점검기의 변경된 목록이 새 파일과 호환 경로를 검사하는지 확인하고, 전체 결과에서는 기존8건과 새 회귀를 구분한다. 실행 로직을 추가 변경해야 하면 영향받는 검사로 넓힌다. 이번에는 Maintain·제품 코드를 바꾸지 않으므로 전체 제품 테스트·자동 Maintain·durable Verify를 실행하는 계획이 아니다.

001·002 explicit와 default Recover를 다시 실행해 loaded 경로·내용 Owner·freshness의 의미를 대조한다. root·Project·기존 읽기 경로에서 같은 Noline 제품 본문에 도달하는지도 확인한다. 새 shared 기준이나 Personal 사례가 Noline 제품 약속을 덮지 않는지, 코드 확인 때 app/package guide를 계속 읽는지도 본다. 정적 대조를 실제 스킬 discovery·설명 효과·기록 유지 성공으로 보고하지 않는다. 그 통합 확인은02에 남긴다.

001 Verify의 argv는 자체 점검기를 실행하지만 evidence 목록은 현재 점검기가 읽는 모든 Markdown·새 파일을 포괄하지 않는다. 따라서 이번 직접 검사 결과를 기존 durable receipt의 최신성으로 바꾸지 않는다.02 이후 Verify를 실행할 때는 실제 입력 전체와 선언 범위를 먼저 맞추거나 claim을 한정해야 한다.

## 반영 순서·복구·다음 판단

이 적용안이 선택되면 최신 source·target과 exact path를 다시 확인한 뒤 신규 본문·스킬, target 기준 병합, 호환 진입과 연결, 점검기, Noline001 결과 기록 순으로 반영한다. 내용이 생기기 전에 consumer만 바꾸지 않는다. 이후 직접 검사와 보호 경로 해시를 대조하고 결과를014에 연결한다.

복구는 target 기준 commit과 이번 경로 목록을 사용한다. 이후 사용자 변경이 없는 기존 수정 파일만 이전 바이트로 복원하고, 이번에 추가한 파일·연결만 제거한다. 전체 reset·clean, runtime 삭제, untracked 정리는 사용하지 않는다. 원래 Noline001의 stale Verify나 제품 작업 상태까지 되돌리지 않는다.

현재 남은 선택은 **기존 제품·Work·Maintain을 유지하면서 위 독립 묶음과 호환 진입을 Noline에 실제 반영할지**다. 사용한 [이식 스킬](../../../../.agents/skills/apply-context-harness/SKILL.md)의 “사용자가 manifest를 승인한 뒤 쓴다”에 따라 target 쓰기 전에 이 구체안을 제시한다. 이번 착수 요청을 아직 제시하지 않은 target별 호환 처리까지 이미 선택한 것으로 기록하지 않는다. 실제 적용·검증·완료와 커밋은 아직 하지 않았다.
