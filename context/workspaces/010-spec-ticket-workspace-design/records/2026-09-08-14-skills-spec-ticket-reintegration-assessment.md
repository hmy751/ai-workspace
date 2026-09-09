# Reference 재확인과 08 스킬·Spec·Ticket 재이식 분석

2026-09-08. Reference와 외부 연구의 현재 파일·계약·검증을 대조한 분석이다. 이번에 Reference의 코드·운영 계약·스킬·hook을 변경하거나 설치하지 않았다.

## 결론과 조사 범위

**08의 후속 합의와 네 스킬은 현재 Reference에 통합할 수 있는 상태다. 실제 변경의 중심은 Spec·Ticket 운영 기준, 스킬과 공통 설명 기준의 배치, 일반 진입점과 이식 절차의 연결이다.** 현재 근거에서 Recover·Maintain·Verify의 기계 schema나 실행 구조를 새로 만들 필요는 찾지 못했다. 실제 스킬 호출과 Main 결과 전달·Maintain 반영의 운영 효과는 아직 검증되지 않았다.

사용자 요청의 핵심은 다음과 같다.

> 여기 프로젝트 refence-project 면밀히 다시 확인하고
> 그 다음 context/analysis/07-tripproof-spec-driven-continuity/08-skills-spec-ticket-integration
> 여기 확실히 분석해봐 우리 한테 다시 이식하려고 하거든 확인해봐

지정 상대 경로는 이 저장소에 없었다. 기존 010 전달 문서와 009 기록이 가리킨 `memory-harness-research`의 동일 경로에서 찾았다. 재이식의 우선 대조 대상은 사용자가 먼저 지목한 `reference-project/`로 잡았으며, 연구 작업대인 이 저장소 root에 직접 설치할 경우의 차이도 아래에 분리했다. 이 분석을 실제 설치나 root Maintain 재활성화로 확대하지 않았다.

- 대상 기준: `context-harness` HEAD `9505bf31521ec40e09a9608c815566f2d89e3dc1`. 조사 시작 시 추적 파일 변경 없음. 기존 untracked `.DS_Store` 보존.
- 입력 기준: `memory-harness-research` HEAD `1e07f589b0f63094cf34ad0e95cbd039ed1e3bb2`. 지정 08 하위는 clean이며 payload 일반 파일이 이 HEAD와 같다.
- [08 진입점](../../../../../memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/08-skills-spec-ticket-integration/README.md), 01·02·03·04, v0 README·manifest·네 실제 SKILL·호출 설정·공통 guidance·상대 연결을 읽었다. 원래 06 입력은 payload 차이·해시 확인에 필요한 파일만 대조했다.
- Reference의 상위 README·AGENTS, Project·Work·Workspace 계약, Spec·Ticket·생성·전환, Recover·Maintain·Verify 코드와 검증, 기존 생성·Project 갱신 스킬 및 바깥 이식 절차를 확인했다.
- private JSONL, archive 전체, 다른 Desktop 제품 저장소는 읽지 않았다. Matt의 외부 저장소를 새로 조사한 작업은 아니며, 이번 판단은 08에 보존된 후속 합의와 실제 payload·Reference 대조에 근거한다.

## Reference가 이미 맡는 것

`context/project/`는 여러 작업에 지속되는 제품 의미를 `common/`, 현재 구현·지원 경계를 `current/`, 특정 작업에서 적용하는 판단 기준을 `guidance/`에 둔다. 중요한 선택의 이유는 `decisions/`가 맡는다. 개별 Workspace는 필요한 Project 본문만 선택한다. [Project 계약](../../../../reference-project/context/project/README.md).

`context/work/workspaces/`는 각 작업의 Spec·Ticket, 전체 상황, 원자료, 산출물 지도와 기록을 유지한다. `context/work/harness/`는 그 내용을 읽고 갱신하고 검증 증거를 남기는 장치다. Main의 목표 해석·작업 조율·실제 결과 판단을 대신하지 않는다. [Work 계약](../../../../reference-project/context/work/README.md), [Workspace 계약](../../../../reference-project/context/work/workspaces/README.md).

- **Recover:** Spec 다섯 파일과 `project-context.md`, Ticket 색인을 필수로 확인한다. Spec 전체와 추가 memory·Ticket 색인·state·output 색인·선택된 Project 본문을 읽는다. Ticket 본문은 실행 주체가 필요한 것을 추가로 선택한다. 근거: `recover/operation.py:138–174`.
- **Maintain:** Spec·Ticket 본문을 생성·갱신할 수 있다. 의미를 판단하는 agent는 읽기 전용이고 guarded apply가 허용 경로·기존 SHA-256·symlink·문서 연결을 검사해 쓴다. 새 Ticket에는 같은 decision의 Ticket 색인 갱신·링크가 필요하다. 기존 Ticket 상태 변화마다 색인·state의 중복 갱신을 강제하지 않는다. 근거: `maintain/operation.py:222, 368, 450, 561`.
- **Verify:** 제품의 고정 검증 명령과 선언된 기준·evidence snapshot, 실행 결과를 보존한다. Ticket 상태나 Spec의 의미 충분성·전체 완료를 판정하는 기능은 아니다. 근거: [Verify 계약](../../../../reference-project/context/work/harness/verify/README.md).
- **생성·전환과 Project 갱신:** 기존 두 스킬이 새 Workspace 구성과 Project-wide 맥락 갱신을 각각 맡는다. Workspace Maintain이 Project 본문까지 쓰는 구조는 아니다.

샘플 `001-default-timeout`은 실제 설정 loader의 기본값·오류 처리 요구로 Spec을 구성했다. 아직 Ticket 본문은 없으며 과거 작업을 소급해 완료 Ticket으로 만들지 않았다. 따라서 Ticket 생성·갱신의 현재 증거는 fixture 검사이고, 실제 Ticket 운용 성공 사례는 아니다.

## 08에서 새로 이어받을 의미

[03 정의·범위](../../../../../memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/08-skills-spec-ticket-integration/03-spec-ticket-definition-and-scope.md)와 [04 Ticket 구성](../../../../../memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/08-skills-spec-ticket-integration/04-ticket-components-and-rationale.md)은 최초 08 스킬 연결 이후의 후속 합의다. `7fa7bde`는 최초 v0와 합의 문서를 보존한 비교 기준이며, 최신 세 스킬 변경도 현재 입력 HEAD에 커밋돼 있다. 02의 “그 뒤 작업 트리에 작성했다”는 당시 진행 설명을 현재 미커밋 상태로 읽으면 안 된다.

**Work당 Spec 하나를 유지한다.** 현재 Reference의 `SPEC-AND-TICKETS.md:9`는 “일단 … 하나”라는 가정과 개수 제한을 두지 않는 이전 문구다. 03:7·74와 04는 Work당 하나를 확정·재확인했다. 실제 이식에서는 이 차이를 상위 운영 기준에 반영한다. 다섯 파일이 다섯 개의 Spec이라는 뜻은 아니며, 하나의 Spec을 다섯 관점으로 구성하는 형태는 유지한다. 새 강제 분할 schema나 자동 Workspace 생성 규칙까지 요구한 합의는 아니다.

**Spec은 여러 실행이 함께 지킬 결과와 판단 기준, Ticket은 그 기준 안에서 확인 가능한 결과를 만드는 실행 단위다.** 기능 구현뿐 아니라 구조 개선·결함 수정도 포함한다. 기능 작업은 필요한 계층을 연결하는 좁은 동작을 우선하고, 코드 개선은 보존할 동작과 개선할 책임·구조를 함께 확인한다. API 자체가 전달 결과라면 그 계약으로 Ticket을 구성할 수 있다. 기반 작업의 완료를 전체 기능 완료로 확대하지 않으며 실제 수행을 이어갈 담당 범위도 드러낸다.

Ticket의 기본 구성은 다음 네 부분이다. 정확한 제목·순서·세부 필드나 상태 이름을 기계적으로 강제하지 않는다.

1. **맡은 결과와 범위:** 이번 실행으로 달라질 것, 관련 Spec 요구와 필요한 제외·후속 범위.
2. **실행 맥락과 접근:** 필요한 입력·의존 관계·선행 결과, 이번 실행의 설계와 이유·가정, 실행하면서 정할 부분.
3. **완료 조건과 확인 방법:** 관찰할 결과와 확인 방법. 동작 보존과 구조 개선의 근거는 각각 다룬다.
4. **현재 상태와 실제 결과:** 실제 수행·확인 근거, 보고받은 내용, 막힘·남은 일·미확인. 확인 계획을 실행 결과로 쓰지 않는다.

**세부 설계도 Ticket에서 발전시킨다.** Ticket의 입력을 잠정적으로 신뢰하며 실행하고, 공통 요구·계약·설계 전제를 흔드는 근거가 나왔을 때 관련 Spec과 의존 결과를 다시 본다. 모든 설계 변경을 Spec으로 올리거나 매 Ticket 완료마다 재판단을 발동하는 절차는 채택하지 않았다.

**Spec을 적극적으로 구체화한다.** 다섯 관점은 조사·논의로 빠진 요구와 사례를 발견하는 데 사용한다. 지금 쓸 내용이 없다는 이유로 성급히 생략하지 않으며, 무관한 내용이나 근거 없는 결정을 채우지도 않는다. 확인한 사실·채택·제안·미확정의 차이를 유지한다.

기존에 열린 채 두었던 Ticket 구성과 Spec 개수에 후속 합의가 생긴 것이므로, 010의 과거 기록을 소급 수정하거나 후속 합의를 다시 미정으로 돌리지 않는다. 현재 Reference에 반영되기 전이라는 상태를 구별한다.

## 네 스킬의 역할과 서로의 관계

`work-discussion`은 구현 전에 Work를 구체화하고 Spec과 연결한다. 사용자가 직접 호출할 때만 적용하며, 매 작업의 강제 인터뷰나 Ticket 자동 분해기로 만들지 않는다. `reconsider-work`는 실제 결과·막힘·변경 부담이 원래 기대를 뒷받침하는지 다시 판단한다. 구현 누락이면 목표를 유지해 빠진 실행을 맡기고, 가정의 문제이면 그 판단과 영향을 다시 본다.

`work-artifact-briefing`은 실제 작업물과 Spec·Ticket의 관계·상태·근거 한계를 설명한다. `explanation-recovery`는 앞선 실제 발화에서 시작해 뜻과 빠진 연결을 복구하고, 필요한 경우에만 관련 문서를 읽는다. 현재 Spec으로 과거 발화의 뜻을 덮지 않는다.

이 네 스킬에 고정 호출 순서나 통합 라우터는 없다. 설명 요청 자체로 구현·상태 변경·acceptance를 시작하지 않으며, `reconsider-work`도 검토자로 호출됐다면 제안까지 Main에 반환한다. 공통 설명 기준의 consumer는 `work-discussion`, `work-artifact-briefing`, `explanation-recovery` 세 스킬이다. 이를 모든 응답의 강제 입력이나 `reconsider-work`의 새 필수 입력으로 확대하지 않는다.

이식의 실질적인 가치는 실제 결과와 요구의 차이를 다음 행동·문서에 연결하는 데 있다. 예를 들어 모델 연결용 interface와 테스트만 있고 요구한 실제 모델 판단이 없다면, 어느 Ticket이 그 수행을 맡는지 확인하고 실제 의미 판단까지 이어가야 한다. 정확한 미완료 보고만 남기거나 Spec을 현재 구현 수준으로 낮추는 것으로 끝내지 않는다. 이 효과는 현재 지침의 의도와 분석상 기대이며 실제 운영으로 입증한 결과는 아니다.

## Main·Maintain 연결에서 지켜야 할 차이

[01 논의 결정](../../../../../memory-harness-research/context/analysis/07-tripproof-spec-driven-continuity/08-skills-spec-ticket-integration/01-discussion-decisions.md)의 사용자 선택은 Main이 논의·실행을 이어가고 문서 갱신을 Maintain에 맡겨 중복 수정을 피하는 운영 방식이다. Main만 작성할 수 있다거나 Maintain만 쓸 수 있다는 전역적인 독점 권한을 신설한 것이 아니다. 기존 Reference는 다른 실행자의 직접 수정도 preimage 검사로 다룬다.

새 Workspace의 초기 구성은 Main/생성 skill이 맡는다. Maintain의 작업 중 기록·갱신과 혼동해 초기 Spec·Ticket 작성까지 Main에게 금지하면 기존 생성 계약을 깨뜨린다. 또한 Work당 Spec 하나는 각 작업 Workspace에 적용하는 의미이며 상위 `context/work/` 디렉터리 전체에 Spec 하나를 두는 뜻이 아니다.

현재 adapter의 후속 입력은 사용자 prompt와 Main 최종 응답이다. 도구 출력·서브 대화가 자동으로 모두 전달되지는 않는다. Main은 채택한 판단·결과·근거·미확인 또는 정확한 로컬 결과 문서를 그 입력에 연결하고, 문서에 의존하는 다음 실행 전에 실제 반영을 확인한다. 이 책임은 이미 `SPEC-AND-TICKETS.md:74`에 있다. 같은 책임을 새로운 인계 절차로 중복 도입할 필요가 없다.

상위 기준 변경의 전달 경로도 구현돼 있다. `codex_session.py:215–289`는 최초 grounding과 매 response-end prompt에서 Maintain README와 `SPEC-AND-TICKETS.md`의 현재 본문을 다시 읽는다. 후속 정의를 전달하려고 별도 규칙 주입 runtime을 만들거나 매번 새 session을 강제할 근거는 없다. 규칙 전달과 실제 Spec·Ticket 내용 갱신은 여전히 다른 사건이다.

다만 **Reference의 새 session은 기본 unbound**다. 사용자가 현재 Workspace 연결을 명시하지 않으면 스킬을 호출해도 자동 Maintain 가입이 생기지 않는다. 설치 시 bound 상태의 갱신, unbound 상태의 정상 no-op, 자동 lifecycle을 사용할 수 없는 경우 기존 Main 수동 fallback을 구별해 안내해야 한다. 스킬 호출을 activation 승인으로 확대하거나, 아무에게도 전달되지 않은 내용을 저장됐다고 보고해서는 안 된다. [Reference routing](../../../../reference-project/AGENTS.md), [Work 운영 지침](../../../../reference-project/context/work/AGENTS.md).

Claude·Codex symlink가 같은 스킬 원본을 가리킨다는 사실도 동일한 Maintain 동작을 뜻하지 않는다. 현재 Reference의 자동 adapter와 설정은 Codex용이고 Claude의 동등한 runtime은 확인하지 않았다.

## 실제 이식에 필요한 변경 범위

변경은 책임을 소유한 기존 문서에 먼저 반영하고, 스킬·생성·이식 consumer가 같은 기준을 찾게 하는 것이 적절하다. 아래는 위 의미 차이를 파일에 대응한 것이다.

| 위치 | 필요한 반영 |
| --- | --- |
| `reference-project/context/work/workspaces/SPEC-AND-TICKETS.md` | 후속 Spec·Ticket 정의, Work당 Spec 하나, Ticket 네 구성, 작업별 결과 범위, 공통 설계와 실행 내부 설계 구별을 canonical에 반영한다. |
| `reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md` | 현재 4번 단계의 “설계는 Spec, 실행·진행은 Ticket” 안내가 상세 설계를 전부 Spec으로 올리는 뜻이 되지 않게 상위 기준에 맞춘다. |
| `reference-project/.agents/skills/` | 네 실제 스킬과 호출 설정을 기존 두 스킬과 함께 배치한다. 상세 Spec·Ticket 계약의 두 번째 정본으로 운영하지 않는다. |
| `reference-project/context/project/guidance/` | 공통 설명 기준을 추가하고 기존 README의 책임·추가·제거 조건을 보존해 색인을 병합한다. payload README로 덮어쓰지 않는다. |
| `reference-project/context/project/README.md` 및 일반 진입점 | “별도 guidance 없음” 상태를 수정하고 네 스킬·상위 계약을 발견할 경로를 연결한다. 적용 조건에 맞지 않는 모든 Recover에 guidance를 강제 추가하지 않는다. |
| 도구별 skill 연결 | 같은 `.agents` 원본에 연결하며 실제 host 발견·호출을 확인한다. 링크 존재와 Maintain runtime 호환을 구별한다. |
| 바깥 `.agents/skills/apply-context-harness/`와 skill 색인 | 현재 절차가 명시하는 생성·Project 갱신 두 스킬 외에 새 네 스킬·공통 기준의 설치/적응/제외·충돌 대조를 다루게 한다. 미래 target 이식에서 묶음이 빠지지 않게 한다. |

현재 Reference에서 발견된 payload의 동명 충돌은 `context/project/guidance/README.md`다. 네 스킬과 공통 설명 기준 본문은 아직 없다. 상위 계약은 payload에 없으므로 파일 충돌이 적다는 사실만으로 의미 통합이 끝나지 않는다.

Root 연구 작업대는 별도로 봐야 한다. 이 저장소의 `context/README.md`는 Reference machine 계약을 복제하지 않도록 하고, root `.codex/hooks.json`은 빈 hooks, `.codex/config.toml`은 Maintainer 미등록 상태다. `context/workspaces/010/current/memory.md` 구조도 Reference의 `context/work/.../memory/spec/`와 다르다. 따라서 Reference 통합을 root에 같은 경로로 복사하거나 root 자동 Maintain을 재연결하는 작업으로 해석하면 안 된다. Root에서 네 스킬을 직접 사용할 목적이라면 이 연구 작업대의 실제 계약과 수동 유지 방식에 맞춘 별도 적응이 필요하다.

## 이번에 실행한 확인과 증명 상한

Runtime 확인과 payload 무결성 확인을 분리하고, 별도 읽기 전용 검토자에게 사용자 요청·08 후속 합의·Reference canonical을 제공해 이식의 의미와 최소 충분 범위를 검토했다. 후속 합의를 기존 유보보다 우선해 반영할 점, Ticket 내부 설계의 위치, 생성과 유지의 책임 구별, unbound와 수동 fallback의 차이를 독립 검토에서 확인했고 Main이 원문 대조 뒤 채택했다. 이는 08 후속본의 의미 대조를 보완하며 실제 host 실행을 대신하지 않는다.

별도 실행 담당이 payload를 대조했다. 일반 파일 10개는 manifest inventory·입력/결과 SHA-256·입력 Git blob·변경 표기와 일치했다. 상대 symlink 8개가 같은 `.agents` 원본으로 해석됐다. README·검토 기록·payload Markdown의 로컬 경로 42개가 존재했고 네 스킬의 `quick_validate.py`도 모두 통과했다. 기존 임시 Python 환경을 사용했으며 새 설치는 하지 않았다.

호출 설정은 기존 준비본과 같았다. `work-discussion`은 implicit invocation이 false, 두 설명 스킬은 true, `reconsider-work`는 해당 policy가 명시되지 않았다. 마지막 경우의 실제 자동 선택은 host 확인 대상으로 남긴다.

Reference 실행 담당은 아래 7개 모듈의 기존 fixture 회귀를 실행했다. Cwd는 `reference-project/`다.

```bash
python3 -B -m unittest \
  context.work.harness.recover.tests.test_recover \
  context.work.harness.maintain.tests.test_operation \
  context.work.harness.maintain.tests.test_codex_session \
  context.work.harness.maintain.tests.test_host_adapter \
  context.work.harness.maintain.tests.test_cli \
  context.work.harness.verify.tests.test_verify \
  context.work.harness.validation.tests.test_ephemeral_workspace_state_preservation \
  -q
```

첫 실행은 117개 중 116개 통과, 기존 descendant timeout 테스트 1개 실패였다. PID 파일이 짧은 실행 제한 안에 생성되지 않았으며 timeout exit는 124였다. 해당 테스트 단독 재실행과 같은 117개 재실행은 통과했다. 원인을 확정하거나 기존 불안정성을 해결했다고 판단하지 않는다. Main이 제품 테스트 `python3 -B -m unittest tests.test_config_loader -q`도 별도로 실행해 7개 통과를 확인했다. 전체 discover를 한 번에 실행해 124개가 모두 통과한 결과로 합치지 않는다.

읽기 전용 Recover에서는 예제의 Spec 다섯 파일·Project 선택·Ticket 색인이 포함됐다. 제품 machine status의 과거 `verification_passed`와 현재 freshness `stale`은 함께 보존됐다. 선언된 snapshot 다섯 개 중 변경 하나·누락 둘이 있으며 기존 Project 경로 이동에 따른 상태로 기록돼 있다. 실제 예제에 새 durable Verify를 실행하지 않았다.

재이식 완료 확인에서는 다음 의미를 구별해야 한다.

- Recover는 Ticket 색인 링크의 본문 존재까지 보장하지 않는다. 실행할 Ticket 본문은 실제로 열어야 한다.
- Guarded apply는 parent 폴더를 생성하지 않는다. 새 구조의 디렉터리 준비는 생성·이식 책임이며 이전 goal/constraints만 있는 Workspace의 자동 migration도 없다.
- 여러 문서 반영은 파일별 atomic write이며 전체 transaction은 아니다. 중간 실패가 있으면 실제 남은 반영을 확인해야 한다.
- 제품 receipt freshness는 선언된 기준·evidence의 일치만 뜻한다. Spec·Ticket의 의미 최신성이나 전체 목표 완료를 보장하지 않는다.
- 실제 host의 스킬 발견·호출, bound/unbound 구별, 서브 결과 전달, 비동기 갱신과 다음 실행자 입력 준비는 이번 정적 검사·fixture 테스트로 입증하지 않았다.

다음 실제 적용에서는 기능 구현 하나와 코드 개선 하나를 포함한 작은 작업으로 Ticket의 범위·확인 계획·실제 결과가 구별되는지 살펴보는 것이 유효하다. 공통 전제가 바뀐 장면과 Ticket 내부 설계만 바뀐 장면, 설명만 요청한 장면도 필요한 범위에서 대조한다. 이는 적용 후 확인할 제안이며, 이번에 실제 Ticket을 생성하거나 실행한 결과가 아니다.
