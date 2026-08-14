# Recover·verify 목적과 활성 시점 가설

기록일: `2026-08-14`
상태: 목적 근거 확인, 활성 시점·책임 분리는 사용자와 논의 중인 후보

## 기록 경계

이 기록은 두 종류의 입력을 섞지 않는다.

- 저장된 [이전 대화 원문](../../../source/00-intake/2026-08-14-harness-maintenance-background/previous-task-transcript.txt)은 약 20분의 machine receipt 경계 변경과 그 뒤 병목 설명을 보존한 배경 source다. 그 안의 시간·원인 설명은 당시 UI와 AI 보고이며 정밀 계측이나 canonical truth로 승격하지 않는다.
- 이번 세션에서 이어진 Recover·verify 설명과 사용자의 문제 감각은 Workspace 004의 현재 분석 입력이다. 사용자는 아직 분리 설계나 구현 변경을 승인하지 않았다.

## 현재 근거에서 확인한 원래 목적

초기 방향 기록은 `Project common context와 현재 Work context 복구 → 필요한 기준과 근거만 선택 → 실제 Project에서 행동 → 실제 결과 검증 → Work context와 records 갱신 → 다음 세션 재진입` 순환을 목표로 삼았다. 특히 현재 설명에는 검증 준비라고 적혀 있지만 실제 검증이 실패할 때, 완료로 보고하지 않고 지속 상태·불확실성·다음 행동을 바꾼 뒤 다음 세션이 그 상태를 다시 읽는 장면을 첫 시험으로 정했다. [초기 방향 기록](../../001-reference-implementation/records/2026-08-13-01-source-to-work-direction.md)

첫 reference 구현은 이 장면을 의도적인 `5000 → 3000` 불일치로 실행해 실패 receipt와 `verification_failed` 상태를 남기고, 수정 후 새 성공 receipt와 `verified_waiting_acceptance`를 다음 recovery가 복구하는 데까지 확인했다. [첫 output reference 기록](../../001-reference-implementation/records/2026-08-13-04-first-output-reference.md)

따라서 현재 근거로 압축한 Harness의 목적은 다음과 같다.

> 다음 작업자가 낡은 작업 설명이나 근거 없는 완료 상태에서 시작하지 않도록, 행동에 필요한 맥락을 선택적으로 복구하고 실제 검증 결과를 지속 상태와 다음 행동에 반영해 다음 세션으로 넘긴다.

이 목적은 `recover`·`verify`라는 명령 이름, Python CLI, JSON schema, 정확한 파일 경로와 동일하지 않다. 그것들은 현재 목적을 실현하는 방법이며 목적을 지키는 범위에서 교체·완화·재배치할 수 있는 검토 대상이다.

## 현재 구현 방법에서 확인한 책임

현재 canonical 설명과 책임 경계 기록에서 확인한 구현은 다음과 같다. 이는 이번 기록에서 runtime을 다시 실행해 검증했다는 뜻이 아니라, 현재 저장소의 구현 설명과 기존 검증 기록이 일치하는 범위의 파일 근거다.

### Recover

현재 [`recover` 설명](../../../../reference-project/context/work/harness/recover/README.md)은 다음을 한 명령에 둔다.

- active 또는 명시된 Workspace의 identity와 `recover.json` 계약 확인
- `current/memory/`의 필수 구성과 사람용 state·machine status 로딩
- 선택된 Project context와 Workspace `output/index.md` 로딩
- status가 가리키는 receipt의 schema·Workspace id·result·finished time 최소 대조
- 선택한 내용과 provenance를 recovery packet으로 출력
- root 이탈·symlink·형식 오류처럼 안전하게 읽을 수 없는 입력 거부

`source/`, 과거 `records/`, output artifact 본문, `verify.json` 전체를 자동으로 읽지 않고 파일을 갱신하지 않는다.

### Verify

현재 [`verify` 설명](../../../../reference-project/context/work/harness/verify/README.md)은 다음을 한 명령에 둔다.

- Workspace identity와 `verify.json` 계약 확인
- argv·경로·shell trampoline과 receipt 디렉터리 안전 조건 확인
- evidence 파일의 실행 전 hash와 byte size 확보
- 고정 argv를 timeout·출력 상한 아래 실행
- 성공과 실패 모두 append-only receipt로 추가
- 최신 result·receipt·다음 행동을 machine status에 atomic 반영

검증 성공은 `verified_waiting_acceptance`이며 사람 acceptance나 `completed`를 대신하지 않는다. 반복 개발 확인은 durable verify가 아니라 기존 Project test 명령을 직접 실행하도록 현재 계약이 구분한다.

기존 책임 경계 refactor도 Recover와 verify가 공유할 기반을 Workspace 선택·안전한 접근·machine status·`status → receipt` 인계 필드로 제한하고, Project canonical·제품 코드·제품 테스트·Workspace 의미의 Owner가 되지 않는다고 정했다. [책임 경계 기록](../../001-reference-implementation/records/2026-08-13-06-harness-responsibility-boundary-refactor.md)

## 기계 정합성과 의미 정합성의 구분

현재 Verify가 직접 연결하는 것은 다음 검증 사건의 기계 정합성이다.

- 고정된 argv
- 실행 전에 snapshot한 evidence
- 실제 실행 결과
- 그 결과를 보존한 receipt
- 최신 receipt와 다음 행동을 가리키는 status

Verify 하나가 다음 의미 판단까지 자동으로 보장하지는 않는다.

- Project 결정이 제품 test에 올바르게 표현됐는지
- 선택한 test가 제품 목표를 충분히 증명하는지
- 사람용 current와 historical records, 이식 skill 설명이 모두 최신 의미와 일치하는지
- 사람이 결과를 수락했는지

따라서 “Verify가 코드와 Context를 모두 정합화한다”는 표현은 범위가 넓다. 현재 목적에 더 가까운 표현은 “제한된 제품 검증 사건을 지속 evidence와 다음 상태에 연결한다”다.

## 사용자가 제시한 활성 시점 가설

사용자는 병목을 책임 이름만이 아니라 **언제 활성화되는 행동인지**로 다시 나눠야 한다는 문제 감각을 제시했다. 현재 후보 시점은 다음 다섯 가지다.

1. Workspace 생성·이식 시점: 필수 구조와 계약이 제대로 설치됐는지 확인
2. 새 세션이나 새 작업 주체의 기존 Workspace 진입 시점: 현재 목표·상태·근거·다음 행동 복구
3. 작업 중 반복 확인 시점: 기존 Project test를 직접 실행
4. 상태 전환·인계 시점: durable verify로 실제 결과와 evidence·status 연결
5. Harness 계약 변경 시점: schema·path 방어·호환성·Harness 전체 회귀 확인

이 분류는 아직 채택된 lifecycle이나 새 명령 설계가 아니다. 현재 동작을 어느 시점에서 수행해야 목적에 충분한지 확인하기 위한 분석 프레임이다.

### Recover에 대한 후보 판단

Recover의 본래 활성 시점은 Workspace 생성 자체보다 새 세션·새 주체가 **이미 존재하는 Workspace에 진입하는 때**로 보인다. 생성 직후 recover는 설치 결과 smoke check로 사용할 수 있지만 목적의 중심과는 구분할 수 있다.

현재 Recover에는 실제 재진입에 필요한 선택·로딩·최신 receipt 연결 확인과 함께, exact schema·필수 파일 구성·overview 순서 같은 구조 완전성 검사도 들어 있다. 이 중 무엇이 매 진입의 안전 조건이고 무엇이 생성·이식·migration 시점의 검사인지는 아직 분류하지 않았다. root 이탈이나 symlink처럼 읽기 자체의 안전을 지키는 검사를 단순히 제거한다는 결정도 하지 않았다.

### Verify에 대한 후보 판단

Verify의 중심 활성 시점은 개발 중 매 확인이 아니라 **상태 전환이나 다른 세션·주체로 인계할 때**로 보인다. 이 시점에는 이번에 넘길 주장, 그것을 확인하는 Project 명령, 실행 당시 evidence, 실제 결과, 다음 행동을 하나의 지속 사건으로 연결하는 책임이 필요하다.

다만 현재 한 실행에는 계약 검사, 경로·명령 안전 검사, 제품 test 실행, evidence snapshot, receipt 생성, status 갱신이 함께 묶여 있다. 사용자는 이 결합이 목적보다 지나치게 타이트할 수 있다는 감각을 제시했지만, 어느 항목을 분리하거나 다른 시점으로 옮길지는 아직 정하지 않았다.

## 아직 결정하지 않은 것

- Recover의 각 검사를 매 진입에 유지할지, 생성·이식·migration 검사로 옮길지
- Verify의 계약·안전 검사를 실행마다 유지할지, Harness 계약 변경 검증과 나눌지
- 어떤 검사가 상태 인계의 신뢰성을 위해 반드시 같은 transaction 또는 명령에 있어야 하는지
- 새 명령이나 책임 이름이 필요한지, 기존 명령 안의 단계·조건만 조정하면 되는지
- 실제 runtime·schema·문서·skill을 어떻게 변경할지
- 활성 시점 분리가 직전 약 20분 병목을 얼마나 줄이는지

## 다음 논의용 분석 단위

현재 `recover`와 `verify`의 동작을 하나씩 펼쳐 다음 기준으로 분류한다.

1. 수행하는 구체 행동과 보호하는 실패
2. 필요한 활성 시점
3. 매번 유지해야 하는 동작
4. 생성·migration·Harness 변경 시점으로 옮길 후보
5. 다른 책임과 중복되어 제거할 후보
6. 이동·제거했을 때 잃는 증거와 위험

사용자와 이 지도를 검토하기 전에는 분리 명령, schema 완화, path 방어 제거 또는 Harness 구현 변경으로 넘어가지 않는다.
