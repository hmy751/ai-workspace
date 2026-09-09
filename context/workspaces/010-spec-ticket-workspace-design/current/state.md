# Spec·Ticket 설계 state

마지막 갱신: 2026-09-09

## 현재 단계

**외부 연구 08의 후속 합의와 네 스킬을 Reference에 반영했다.** 사용자는 처음에는 커밋을 보류했으나 2026-09-09 “그럼 됐고 커밋 하자”라고 요청해 분석·통합 변경과 기록의 커밋을 승인했다. 적용 전 기준은 `9505bf3`이며, 통합 판본은 이 state 파일과 Reference 변경을 함께 담은 Git 이력에서 확인한다. 적용과 검증은 [통합 기록](../records/2026-09-08-15-skills-spec-ticket-reference-integration.md)에 있다.

입력은 `memory-harness-research`의 08 준비본이며 분석 기준은 `1e07f58`이다. 이식 중 원본 HEAD가 `6bd06b5`로 바뀌었으나 가져온 스킬·호출 설정·공통 기준 본문·상대 연결은 분석 기준과 동일함을 확인했다. 후속 Work당 Spec 하나, Ticket 네 구성과 실행 내부 설계·공통 설계 구별을 상위 canonical과 생성 안내에 반영했다. 네 스킬·guidance·Reference 진입점과 바깥 이식 절차도 연결했다. 기계 schema·Python runtime·제품 코드·hook 설정은 변경하지 않았다.

Main 결과 전달과 실제 문서 준비 확인은 기존 책임이다. Maintain에 중복 갱신을 맡기는 운영 선택을 새 Workspace 초기 구성 금지나 전역적인 독점 작성권으로 확대하지 않았다. Reference의 default-unbound와 허용된 문서 반영의 Main 수동 fallback을 연결했다. 이 연구 작업대 root의 자동 Maintain은 비활성 상태로 유지한다.

**설계 기록은 `4fe8694`로 커밋했고, 합의한 Spec·Ticket 구조를 Reference에 적용했다.** 후속 사용자가 Project context 파일 번호 정리와 커밋을 요청했다. `03-project-context.md`를 `project-context.md`로 바꾸고 실제 읽기 경로·테스트를 맞췄으며, 적용 결과와 검증 기록을 **`dcd3c6f`로 커밋했다.**

위 커밋은 앞선 구조 적용 이력이다. 2026-09-09의 후속 요청으로 이번 통합 변경에 대한 커밋 보류는 해제됐다. 유지할 합의는 [memory](memory.md), 실제 결과와 canonical 위치는 [output](../output/index.md), 최신 변경·판단·검증은 [08 통합 기록](../records/2026-09-08-15-skills-spec-ticket-reference-integration.md)에 있다.

## 적용한 동작

- Spec 다섯 파일이 샘플 Workspace의 goal·작업별 constraints를 대체했다. `project-context.md`는 유지한다. Ticket은 memory의 별도 폴더에 정의·진행을 함께 남기는 구조다.
- Recover는 Spec 전체와 Ticket 색인을 기본으로 읽고, 작업 주체가 필요한 Ticket 본문을 선택한다. 아직 Ticket이 없는 샘플에 과거 실행 Ticket을 소급 생성하지 않았다.
- Maintain은 같은 역할로 Spec·Ticket을 생성·갱신한다. 새 Ticket은 Ticket 색인에, 새 Spec·기타 memory 문서는 memory 색인에 연결한다. 기존 Ticket의 상태 갱신만으로 색인·state를 함께 바꾸지는 않는다.
- Workspace의 Spec·Ticket canonical을 Maintain의 규칙 입력에도 연결했다. Main은 계속 작업을 조율하며 다른 실행자 결과의 자동 수집이나 새 조율 runtime을 만들지 않았다.
- 생성·전환 canonical을 새 구성에 맞췄다. 생성·이식 skill은 live canonical을 읽는 기존 경로를 유지한다.
- 후속 Ticket 네 구성·Spec과 실행 내부 설계의 관계를 canonical에 적용했다. 문서 유지의 운영 선택과 생성·작업 조율·수동 fallback 책임을 연결했다.
- `work-discussion`, `reconsider-work`, `work-artifact-briefing`, `explanation-recovery`의 원본·호출 설정과 도구별 상대 연결을 설치했다. 공통 설명 기준을 기존 guidance 색인에 병합하고 바깥 이식 절차가 전체 Reference skill 색인을 사용하도록 보완했다.

## 검증 결과와 한계

- 통합 뒤 전체 124개를 한 번 실행해 123개 통과, 기존 Verify `test_timeout_covers_descendant_after_group_leader_exits` 한 개 실패였다. 해당 검사 단독 한 번은 통과했다. 전체 재실행·코드 수정·시간 제한 변경으로 실패를 없애지 않았다. 앞선 변경 전 재현 근거는 [12 적용 기록](../records/2026-09-08-12-reference-spec-ticket-implementation.md)에 보존돼 있으며 원인·해결을 확정하지 않는다.
- default/explicit Recover와 Maintain bootstrap은 성공했다. 필수 Spec 다섯 파일·Project 선택·Ticket 색인이 포함되고 explicit Recover와 bootstrap packet이 같았다. 기존 `verification_passed`와 현재 `stale`을 보존했으며 실제 Workspace의 status·receipts 일반 파일 14개의 inventory·SHA-256은 모든 검증 전후 동일했다.
- scripted runner에서 start·resume 각각이 새 Spec·Ticket canonical을 다시 읽어 prompt에 전달함을 확인했다. 실제 Codex나 hook을 실행한 증거는 아니다.
- 네 스킬과 이식 skill의 형식 검사, 일반 파일 hash·상대 연결·로컬 링크·diff 검사를 수행했다. 독립 변경 리뷰에서 수정이 필요한 회귀·합의 누락을 찾지 못했다. 세 스킬을 직접 읽힌 제한 평가에서는 실제 구현·완료 범위, 열린 제품 선택, 앞선 설명의 뜻과 검증 상한을 구별했다.
- 실제 host의 discovery·호출·비동기 Maintain 갱신과 새 실행자에게 문서가 준비되는 효과는 확인하지 않았다. 샘플에 실제 Ticket을 소급 생성하거나 이 연구 작업대 root의 Maintain을 활성화하지 않았다.

## 다음에 이어갈 일

통합 변경의 Git 이력과 [적용 기록](../records/2026-09-08-15-skills-spec-ticket-reference-integration.md)에서 이어간다. 이번 커밋 승인은 실제 host acceptance나 외부 제품 적용의 완료를 뜻하지 않는다. Reference 통합과 이 연구 작업대 root의 직접 사용은 별도 적용 범위다.

실제 사용하는 대상 session에서 스킬 발견·호출, bound/unbound·수동 fallback, Main 결과가 Maintain 입력과 실제 문서까지 이어지는지, 새 실행자에게 필요한 본문이 준비되는지를 확인할 수 있다. 개별 실행자의 입력·실행·검토 배치는 작업에 맞게 정한다. 기존 Verify timeout 검사 실패와 Project 경로 이동에 따른 과거 receipt stale도 별도 후속 조사로 남는다.

초기 분석·후속 합의·현재 구현의 관계는 [재이식 분석](../records/2026-09-08-14-skills-spec-ticket-reintegration-assessment.md)과 [output](../output/index.md)에서 찾는다. 외부 연구 수정·실제 제품 적용·host acceptance를 이 Reference 변경으로 완료 처리하지 않는다.
