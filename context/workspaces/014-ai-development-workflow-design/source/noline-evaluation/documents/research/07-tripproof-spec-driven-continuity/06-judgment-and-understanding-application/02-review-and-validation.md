# 리뷰와 확인 기록

2026-09-08. 이 기록은 **원본을 함께 둘 수 있는지 본 제3 리뷰**, **일반화한 준비본의 원본 대조**, **실제로 수행한 파일 검사**를 구분한다. 대상 프로젝트 설치·host 발동·사용 효과에 대한 시험 기록은 아니다.

## 원본 스킬과 구성 파일만 본 제3 리뷰

사용자는 다음과 같이 요청했다.

> “이 스킬들 가지고 하나의 프로젝트에 넣을건데 겹치는 부분이나 판단할게 있는지”
>
> “저 스킬들과 구성 파일들만 가지고 근거 분석 파일 이런거 말고”

Main은 앞선 대화 이력을 상속하지 않은 새 reviewer에게 이 요청과 원자료 접근점·읽기 경계만 주었다. 네 스킬을 한 프로젝트에 함께 둘 때 겹침이나 판단할 점이 있는지 독립적으로 검토하게 했으며, Main의 앞선 원인 가설이나 예상 결론은 주지 않았다. 여러 스킬이 관여한다는 사실만으로 결함을 가정하지 않도록 했다. 적용 프로젝트는 미정이고 maintainer는 별도라는 사용자 제약을 전달했다.

reviewer가 읽은 원본은 다음 **문서 10개와 상대 symlink 6개**다.

- [reconsider-work 폴더](../05-judgment-continuity-solution-direction/v0/skills/reconsider-work/): `SKILL.md`, `agents/openai.yaml`
- [work-discussion 폴더](../../09-tripproof-cognitive-debt/v0/payload/.agents/skills/work-discussion/): `SKILL.md`, `agents/openai.yaml`
- [explanation-recovery 폴더](../../09-tripproof-cognitive-debt/v0/payload/.agents/skills/explanation-recovery/): `SKILL.md`, `agents/openai.yaml`
- [work-artifact-briefing 폴더](../../09-tripproof-cognitive-debt/v0/payload/.agents/skills/work-artifact-briefing/): `SKILL.md`, `agents/openai.yaml`
- [지침 README](../../09-tripproof-cognitive-debt/v0/payload/context/project/guidance/README.md), [설명과 근거 기준](../../09-tripproof-cognitive-debt/v0/payload/context/project/guidance/explanation-and-evidence-criteria.md)
- [09 payload](../../09-tripproof-cognitive-debt/v0/payload/)의 `.claude/skills/`와 `.codex/skills/`에서 위 이해 지원 세 스킬로 향하는 상대 연결

상위 README·OUTPUT-PREVIEW·배경 분석·archive·Workspace current/records·기존 리뷰·대화 기록·적용 후보 프로젝트·maintainer 계약은 제외했다. 허용 파일이 이 자료를 링크하더라도 따라가지 않게 했다. 아래 내용은 reviewer가 보고한 범위이며 Main도 위임 입력과 보고를 대조했다.

리뷰 결론의 원문:

> 네 스킬은 함께 둘 수 있습니다. **겹친다는 이유로 합치거나 호출 순서를 강제해야 할 근거는 없습니다.** 다만 대상 프로젝트를 정하면 문서 연결을 맞춰야 하고, `reconsider-work`의 직접 문서 반영 책임을 유지할지는 확인할 만합니다.

핵심 발견과 Main의 처리는 다음과 같다.

1. **프로젝트 의존 관계:** 고정 `CLAUDE.md`·Project context 읽기와 동반 색인의 `ChatAnswer`·`EvidenceState`·prompts/eval/fixtures 항목은 실제 대상과 맞춰야 한다. 대상 문서를 읽지 않았으므로 ‘대상에서 깨진 링크’라고 판정한 것은 아니다. 공동 준비본에서는 고정 진입 안내와 전용 색인을 일반화했다.
2. **Main의 문서 반영:** 원본 `reconsider-work` 59행은 채택한 내용을 기존 계획/current에 직접 남기라고 하고, 57행은 검토만 요청받으면 제안까지만 반환하라고 한다. 설명 요청만으로 수정하지 않는 세 스킬의 경계와 곧바로 상충하지 않는다. 별도 maintainer의 계약은 읽지 않았으므로 실제 책임 중복을 판정하지 않았다. 준비본은 기존 Main 책임을 보존하고 구체적인 연결은 후속으로 남겼다.
3. **같은 요청에서의 관여:** 앞선 완료 설명의 오류를 바로잡는 일과 실제 다음 작업을 다시 정하는 일은 연결될 수 있는 다른 책임이다. 현재 문구만으로 새 우선순위 규칙이나 통합 절차가 필요하다고 보지 않았다. 준비본에 이를 추가하지 않았다.
4. **설정과 노출 경로:** 이해 지원 세 스킬의 자동 선택 허용 여부는 본문과 맞고, `reconsider-work`에는 같은 설정 항목이 없다. 생략 자체를 오류나 실제 비발동으로 판정하지 않았다. 기존 네 설정을 보존하고, 공동 payload에 `reconsider-work`의 Claude·Codex 연결 두 개를 추가했다.

Main은 위 원문과 설정을 직접 대조해 리뷰 결론에 동의했다. 앞선 원문 대조 보조 검토와 Main 설명에 대한 점검은 이번 공동 사용 제3 리뷰와 다른 검토다. 이 조건으로 원본 네 스킬의 공동 사용을 독립 검토한 것은 이번이 처음이다.

## 일반화한 준비본의 후속 대조

payload 작성자와 다른 reviewer가 원본 10개 문서와 [준비본](v0/README.md)의 대응 파일·README·연결을 읽기 전용으로 비교했다. 확인할 주장은 ‘큰 역할·발동·권한 변경 없이 프로젝트 진입 안내·표현·지침 색인만 일반화했고, 네 스킬을 함께 이식할 파일과 연결을 준비했다’였다. 배경 분석·archive·대상 프로젝트·Main 판단 기록은 입력으로 주지 않았다.

후속 리뷰 결론의 원문:

> **검토 주장은 실제 diff와 일치합니다. 현재 준비본에서 수정이 필요한 결함은 발견하지 못했습니다.** 네 스킬의 역할·발동·수정 권한을 유지하면서 프로젝트 진입 안내와 동반 색인을 일반화한 범위입니다.

reviewer는 맥락을 확인할 책임, 설명 복구의 대화 우선 조건, 공통 지침 접근, 근거를 구별하는 구체적인 대비, 권한 경계가 보존됐다고 판단했다. 기존 지침 색인을 통째로 덮어쓰지 않고 필요한 항목만 병합한다는 설치 안내와 미설치 상태도 실제 파일과 맞는다고 보고했다. 실제 대상의 root 지침이 충분한 맥락을 안내하는지와 기존 정책·스킬과의 공존은 확인하지 않았다.

별도 문서 검토자는 [판단 기록](01-joint-application-decisions.md)의 책임 구분·사용자 정정·철회한 제안과 원문 인용을 대조했다. 스킬 발췌 6개는 원본과 문자 단위로 일치했고, 판단 오류를 발견하지 못했다. 대화 조회 도구가 최근 네 turn의 본문을 반환하지 않아 이 검토자는 원본 제3 리뷰와 마지막 사용자 발화를 독립 재취득하지 못했다. 마지막 범위는 전달한 사용자 원문을 기준으로 검토했고, 해당 제3 리뷰 입력·결론은 Main이 직접 가진 실제 위임과 보고로 대조했다.

## 파일 검사

입력 원본 10개는 연구 저장소 commit `3d6facb75dd2e72a3001f24f29be09a92a1c20fc`의 파일 내용과 일치했다. [manifest](v0/manifest.json)는 각 원본 경로·SHA-256과 준비본의 경로·SHA-256, 변경 이유를 고정한다. 판본이 달라지면 manifest와 실제 diff를 먼저 확인한다.

- payload 일반 파일은 10개다. `reconsider-work/SKILL.md`와 네 `openai.yaml`의 5개는 원본과 byte 단위로 같다. 나머지 5개는 세 스킬의 시작 한 줄, 기준 문서 제목 한 줄, 동반 README 색인만 바뀌었다.
- Claude·Codex 상대 symlink 8개가 모두 `../../.agents/skills/<동명 스킬>`로 해결됐다. 원래 세 스킬의 연결 6개를 유지하고 `reconsider-work`의 연결 2개를 추가했다.
- payload의 상대 Markdown 링크 16개가 모두 준비본 내부의 실제 파일로 해결됐다. 특정 프로젝트 root 문서의 존재를 검사 완료로 오인하지 않도록 고정 링크를 실제 지침을 찾는 안내로 바꿨다.
- `skill-creator/scripts/quick_validate.py`를 네 스킬 각각에 실행해 모두 exit 0, `Skill is valid!`를 확인했다. 기본 Python에 없던 PyYAML은 이미 있던 로컬 캐시를 해당 검사 프로세스에서만 사용했다. 프로젝트·전역 의존성을 설치하거나 변경하지 않았다.
- Main은 원본과 준비본의 전체 파일 diff, 원본이 commit과 같은지, manifest의 해시·연결과 일반화 범위를 대조했다. payload 작성자는 공백 검사도 수행했다.
- 문서와 Workspace 지도 반영 후 일반 파일 25개의 공백과 상대 Markdown 링크 142개를 확인했고 오류가 없었다. manifest의 파일 10개와 symlink 8개도 실제 내용·연결과 일치했다. `git diff --check`도 통과했다. 링크의 존재 확인은 연결한 배경·archive 본문을 다시 읽었다는 뜻이 아니다.

검사 명령의 형태는 `python3 <skill-creator의 scripts/quick_validate.py> <payload/.agents/skills/스킬명>`이다. 이 validator는 스킬 형식에 대한 검사이며 실행 시 판단 품질이나 자동 선택의 정확성을 증명하지 않는다. 여기서는 새 제품 테스트나 host 발동 실험을 만들지 않았다.

## 이 결과로 확인하지 않은 것

실제 TripProof 또는 context-harness 설치, 대상 현재 지침·maintainer 계약과의 대조, host에서의 발견·발동, 실제 요청의 설명·판단·후속 반영, 장기 효과는 확인하지 않았다. 05 archive와 과거 판본의 시험도 이번 검사의 입력이 아니다.

따라서 현재 결론은 **원본 책임을 유지한 공동 준비본과 그 정적 확인이 있다**는 것이다. 이식한 프로젝트에서 효과가 입증됐다거나 모든 상황에서 충돌이 없다고 보장하지 않는다.
