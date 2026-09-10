# Project 관리 기준의 배치와 source 수정

Noline의 Project README에 내용 복원·변경·갱신 기준이 길게 들어간 원인은 Reference 원본의 배치와 이를 target README에 적응하라는 이식 지시에 있었다. 앞선 문서 전환 worker는 이 긴 기준을 새로 만든 주체가 아니며, 이번 변경은 그 worker의 실행 보완과 구분한다.

사용자는 “그럼 어디에 배치하는게 낫겟고 이식 스킬도 고쳐야 하나?”라고 물었고, README에는 구조·권위 관계를 남기고 상세 관리 기준은 같은 Project 경계 안에 두는 배치를 제안했다. 이어 “근데 이 수정은 우리 레포에도 수정해야 되는거아닌가?”라고 요청해 source 원본과 이식 지시를 함께 수정했다.

## 반영한 책임

- [`Reference Project README`](../../../../reference-project/context/project/README.md): Project 정체성, 층별 책임, 실제 문서 위치, 권위·Workspace 경계와 관리 계약을 읽을 시점. 본문은 94줄에서 68줄로 바뀌었다.
- [`Project MAINTENANCE`](../../../../reference-project/context/project/MAINTENANCE.md): 작성·복원·재구성·갱신 때 필요한 내용 충분성, 근거·불확실성, 변경 범위와 갱신 기준. 기존 기준의 상세 내용은 이 위치에 보존했다.
- [`Project 갱신 skill`](../../../../reference-project/.agents/skills/update-project-context/SKILL.md): README와 관리 계약을 읽고 적용한다. Reference root·context·Work·Workspace와 skill 색인의 직접 소비 연결도 맞췄다.
- [`이식 skill`](../../../../.agents/skills/apply-context-harness/SKILL.md)과 [`application-contract`](../../../../.agents/skills/apply-context-harness/references/application-contract.md): 관리 계약을 target의 `MAINTENANCE.md`에 적응하고 해당 절차에서 읽도록 바꿨다. 이번 실행의 통합·이동·제거·보존 결과는 적용 Workspace 기록에 둔다.

관리 기준은 Project가 소유하며 skill의 내부 기준으로 옮기지 않았다. 제품 작업의 조건부 판단을 소유하는 `guidance/`와 context 자체의 관리 계약을 구분했다. 제품·domain 본문은 기존 책임 층에 두고 root에는 구조 진입점과 관리 계약을 둔다. 일반 Recover의 경로 허용 계약과 Workspace 선택은 바꾸지 않고 관리 주체가 필요한 시점에 직접 읽는다.

작업대인 이 저장소의 `context/`에는 Reference 구조를 복제하지 않았다. 현재 Workspace는 변경 이유·결과를, `reference-project/`와 이식 skill은 실제 산출물을 소유한다. 이 변경은 source에만 적용했고 Noline 재적용은 수행하지 않았다. 앞선 Noline 검증 결과가 이번 source 수정의 적용을 증명하지 않는다.

## 확인과 한계

옮긴 복원·갱신 문단을 변경 전 원문과 대조해 지시 대상 표현을 제외한 내용이 보존됐고, 기존 권위·작업 경계도 적절한 위치에 남았음을 확인했다. 변경한 source 파일의 local link 138개에 누락 경로가 없으며 `git diff --check`가 통과했다. 두 skill의 frontmatter는 변경 전과 같고 Ruby YAML 형식·이름·필수 설명·미완성 표시 검사가 통과했다. 표준 `quick_validate.py`는 PyYAML 부재로 실행하지 못했다.

Reference의 active/default consumer는 `001-default-timeout`이며 session runtime 디렉터리가 없어 별도 session-bound consumer는 없었다. Default와 explicit Recover는 모두 exit 0이고 같은 context 경로 15개를 읽었다. 관리 계약은 자동 입력에 들어가지 않았다. 기존 sample receipt의 freshness는 종전 상태 설명과 같은 stale이며 새 제품 Verify로 덮어쓰지 않았다. 처음에는 JSON 옵션 없이 Recover를 실행해 출력 파싱만 실패했으며, `--json`으로 다시 실행해 확인했다.

이 변경은 문서 배치·읽기 연결이며 runtime·제품 코드·machine 계약을 바꾸지 않았다. 제품 full suite, durable Verify, 실제 host activation이나 새로운 이식 실행은 하지 않았다. 변경 파일 hash와 검사 요약은 [검증 기록](receipts/project-management-layout/validation.json)에 있다. Source 변경은 미커밋이다.
