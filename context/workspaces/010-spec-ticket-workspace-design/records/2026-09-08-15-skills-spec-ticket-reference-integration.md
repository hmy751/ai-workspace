# 08의 Spec·Ticket 후속 합의와 네 스킬의 Reference 통합

2026-09-08. [재이식 분석](2026-09-08-14-skills-spec-ticket-reintegration-assessment.md) 뒤 사용자가 다음과 같이 요청했다.

> 일단 반영해봐 커밋은 하지말고

Reference의 상위 기준·네 스킬·공통 설명 기준·도구별 연결을 반영하고 바깥 이식 절차까지 보완했다. 현재 결과는 working tree에 있으며 stage·commit하지 않았다. 연구 저장소 root의 자동 Maintain과 외부 연구 원본·전역 설정은 변경하지 않았다.

## 실제 변경과 역할

[Spec·Ticket canonical](../../../../reference-project/context/work/workspaces/SPEC-AND-TICKETS.md)에 Work당 Spec 하나, 기능 구현·코드 개선·결함 수정에서 확인 가능한 결과를 만드는 Ticket의 정의, 네 기본 구성, 실행 내부 설계와 공통 설계의 반영 위치를 적용했다. 다섯 Spec 파일과 Ticket 폴더·읽기·보존 구조는 유지했다. Ticket의 정확한 제목·순서·세부 필드·상태 이름을 검사하는 새 schema는 만들지 않았다.

Spec의 다섯 부분은 조사·논의로 적극적으로 구체화하는 관점으로 두고, 확인한 사실·채택·제안·미확정을 구별했다. Ticket은 맡은 결과·범위, 실행 맥락·접근, 완료 조건·확인 방법, 현재 상태·실제 결과를 함께 유지한다. 실행 내부 설계·이유는 Ticket에 남기며 공통 전제를 흔드는 근거가 있을 때 관련 Spec과 의존 결과를 다시 본다.

[생성·전환](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md)은 초기 Spec·Ticket 구성을 Main/생성 skill이 맡도록 유지하면서 후속 의미를 참조하게 했다. [Maintain](../../../../reference-project/context/work/harness/maintain/README.md)은 자동 연결을 사용하지 않는 session에서도 허용된 문서 반영에 기존 bounded bootstrap·semantic 판단·guarded apply의 수동 fallback을 사용할 수 있음을 명시했다. 수동 처리가 자동 binding을 만들지는 않는다.

준비된 Workspace의 문서 갱신은 Maintain에 맡겨 중복 수정을 피한다. Main은 채택한 판단·근거·실제 결과·미확인 또는 정확한 로컬 결과 문서를 최종 응답에 연결하고, 다음 실행자가 문서를 사용하기 전에 필요한 실제 반영을 확인한다. 생성·작업 조율까지 Maintain으로 옮기거나 스킬 호출을 activation 승인으로 바꾸지 않았다.

[Reference skill 색인](../../../../reference-project/.agents/skills/README.md)을 만들고 기존 두 관리 스킬과 새 네 스킬의 역할·canonical·도구 연결을 안내했다. 새 스킬 원본은 다음과 같다.

- [work-discussion](../../../../reference-project/.agents/skills/work-discussion/SKILL.md): 명시 호출로 Work와 Spec을 구체화한다.
- [reconsider-work](../../../../reference-project/.agents/skills/reconsider-work/SKILL.md): 실제 결과와 조건에서 판단·후속 행동을 다시 본다.
- [work-artifact-briefing](../../../../reference-project/.agents/skills/work-artifact-briefing/SKILL.md): 기존 작업물의 역할·연결·상태와 근거 한계를 설명한다.
- [explanation-recovery](../../../../reference-project/.agents/skills/explanation-recovery/SKILL.md): 앞선 실제 설명에서 뜻·전제·논리 연결을 복구한다.

네 스킬의 `SKILL.md`와 `agents/openai.yaml`, `.claude/skills/`·`.codex/skills/`의 상대 symlink를 준비본 그대로 가져왔다. 공통 [설명과 근거 기준](../../../../reference-project/context/project/guidance/explanation-and-evidence-criteria.md)은 본문을 그대로 두고 기존 [guidance 색인](../../../../reference-project/context/project/guidance/README.md)에 병합했다. 조건에 맞는 이해 지원 세 스킬의 소비만 연결하고 모든 Recover의 필수 입력으로 추가하지 않았다.

Reference root AGENTS·README와 Project README에서 새 역할·기준·현재 상태를 찾게 했다. 바깥 [이식 skill](../../../../.agents/skills/apply-context-harness/SKILL.md)과 [적용 계약](../../../../.agents/skills/apply-context-harness/references/application-contract.md)은 live Reference skill 색인에서 각 스킬·공통 기준·도구 연결의 설치·적응·제외를 판단하도록 보완했다. 기존 동명 Owner 보호·guidance 병합·실제 호출과 문서 유지의 증명 구별을 유지하며 Spec·Ticket 내용을 이식 skill에 재정의하지 않았다.

## 원본과 이식 판본

입력은 `memory-harness-research`의 `context/analysis/07-tripproof-spec-driven-continuity/08-skills-spec-ticket-integration/v0/payload/`다. 분석 기준 commit은 `1e07f589b0f63094cf34ad0e95cbd039ed1e3bb2`, 대상 이식 전 HEAD는 `9505bf31521ec40e09a9608c815566f2d89e3dc1`이다.

작업 중 외부 연구 HEAD가 `6bd06b50704bb7984384043999e03ef5f35b4299`로 이동했지만 설치한 네 스킬·호출 설정 8파일, 공통 기준 본문과 상대 symlink 8개는 분석 기준 commit과 동일함을 확인했다. 일반 파일은 승인 기준 Git blob·현재 원본·manifest SHA-256·설치본을 대조했다. 기존 guidance 색인은 source의 전용 색인으로 교체하지 않고 대상의 기존 책임·내용에 병합했다. 외부 원본을 수정하지 않았다.

## 실행 검증

Reference root에서 다음 전체 검사를 한 번 실행했다.

```bash
python3 -B -m unittest discover -s . -p 'test_*.py' -q
```

결과는 **124개 중 123개 통과, 기존 Verify timeout 테스트 1개 실패**다. 핵심 출력은 다음과 같다.

```text
FAIL: test_timeout_covers_descendant_after_group_leader_exits
  descendant_pid_path.is_file()
AssertionError: False is not true
  "exit_code": 124,
  "status": "verification_failed",
  "timed_out": true
Ran 124 tests in 9.074s
FAILED (failures=1)
```

같은 검사를 단독으로 한 번 실행한 결과는 통과했다.

```bash
python3 -B -m unittest \
  context.work.harness.verify.tests.test_verify.VerifyTests.test_timeout_covers_descendant_after_group_leader_exits \
  -v
```

```text
Ran 1 test in 0.397s
OK
```

앞선 분석과 변경 전 기록에서도 관찰한 PID 파일 미생성 증상이다. 전체 재실행·검사 생략·시간 제한 변경·Verify 코드 수정은 하지 않았다. 실패 원인을 확정하거나 이번 변경에서 해결됐다고 보고하지 않는다.

기본 Recover, explicit `recover 001-default-timeout --json`, `maintain bootstrap 001-default-timeout --json`은 모두 exit 0이었다. Spec 다섯 파일·Project 선택·Ticket 색인이 포함되고 explicit Recover와 bootstrap packet은 같았다. 기존 `verification_passed`와 현재 `stale`—선언된 snapshot 다섯 개 중 변경 하나·누락 둘—을 보존했다.

실제 `001-default-timeout`의 machine status와 receipts 디렉터리 내 일반 파일 14개의 경로·크기·SHA-256은 모든 검증 전후 동일했다. 실제 Workspace에서 새 Verify나 activation을 수행하지 않았다.

현재 `SPEC-AND-TICKETS.md`를 start와 resume 각각 다시 읽어 prompt에 넣는 경로는 scripted runner와 파일 읽기 관찰로 확인했다. 실제 canonical·grounding prompt·resume prompt에 든 본문의 SHA-256은 모두 `5bf952a44487f42f311c14d0c11c1f1392f2050b31a584e400b5a9b64cb35d6f`였다. 실제 Codex를 호출한 결과나 host acceptance는 아니다.

상세 임시 출력은 `/private/tmp/reference-integration-validation-7vmyv6_2/`의 `unittest-full.log`, `unittest-timeout-isolated.stderr.log`, `validation-summary.json`, `recover-bootstrap-summary.json`, `prompt-delivery-summary.json`, `machine-inventory-final.json`에 생성했다. 임시 경로 없이도 확인 범위를 재검토할 수 있도록 주요 명령·출력·상태 보존 범위를 위에 남겼다.

## 검토와 남는 한계

네 스킬과 수정한 이식 skill은 `quick_validate.py`를 통과했다. 네 호출 정책·본문과 상대 연결을 보존했고 현재 파일·index·canonical 관계를 대조했다. 기존 임시 Python 환경을 사용해 전역 환경을 바꾸지 않았다.

최종 변경 Markdown 24개의 로컬 링크 234개와 파일 끝·공백을 확인해 오류가 없었고 `git diff --check`도 통과했다. 검증한 canonical SHA는 최종 파일과 같았다. Git HEAD는 이식 전 `9505bf3` 그대로이며 staged 파일은 없었다.

별도 읽기 전용 검토자는 사용자 적용 요청·08 후속 합의·현재 diff·상위 계약을 대조해 수정이 필요한 P1·P2 회귀, 합의 누락, 이중 정본이나 책임 충돌을 찾지 못했다. 같은 검토자에게 설치된 스킬을 직접 읽혀 다음 세 요청의 첫 응답을 평가했다.

- `work-artifact-briefing`: default-timeout의 완료 범위와 HTTP 적용 여부를 물었다. 응답은 “현재 구현과 검증 기록이 뒷받침하는 범위는 설정을 검사해 timeout 값이 담긴 변경 불가능한 policy를 반환하는 데까지”라고 설명했다. Spec·현재 code/test·정확한 receipt hash를 대조하며 과거 pass·현재 stale·실제 HTTP 실행을 구별했다.
- `work-discussion`: 환경변수에서도 timeout을 받고 누락 시 기존 동작, 잘못된 값은 드러내려는 평가용 요청을 제시했다. 응답은 기존 Project 범위가 확장되는 점을 확인하고, dict와 환경변수 값이 함께 있을 때의 우선순위만 선택으로 남겼다. 빈 문자열 처리는 제안으로 표시하고 열린 선택이 있는 응답을 최종안으로 부르거나 Spec을 쓰지 않았다.
- `explanation-recovery`: “직접 fixture에서 검증 경로가 통과했습니다. 실제 host의 자동 갱신은 아직 확인하지 않았습니다.” 다음에 “자동 갱신도 이제 검증 끝났다는 거야?”를 제시했다. “확인한 것은 시험용 환경에서 검증 절차가 통과했다는 것뿐”이라고 답하고 실제 자동 갱신은 미확인임을 유지했다. 이 사례는 저장소 추가 탐색 없이 두 발화만 사용했다.

위 요청과 응답은 제한된 평가 자료이며 실제 사용자 제품 결정·환경변수 개발 요청으로 승격하지 않는다. 모델에게 스킬 본문을 직접 읽힌 결과로서, 실제 host discovery·자동 호출·Maintain 전달·문서 갱신이나 사용자의 이해 개선을 검증하지 않았다.

스킬·Main·Maintain·guarded apply·사람의 책임을 기존 Owner에서 이어지게 했으며, 지속 Spec·Ticket·state나 조건부 기준을 스킬 안의 별도 장부로 옮기지 않았다. 스킬을 제거해도 Workspace와 문서 관리 계약은 남고, 공통 기준은 consumer·제거 조건으로 수명을 판단할 수 있다. 전역 하네스·색인·bridge는 수정하지 않았으므로 전역 snapshot을 만들지 않았다.

실제 host의 discovery·정해진 호출 방식·Main 결과 전달·비동기 갱신·다음 실행자의 문서 준비와 장기 효과는 아직 별도 확인 범위다. 현재 설치 상태와 실제 자동 Maintain 운영 성공을 구별한다. 연구 작업대 root는 기존 수동 관리 구조를 유지한다.
