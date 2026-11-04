# Verify 제거 시 기존 도구와의 기능 비교

2026-11-04. 사용자는 development의 검증 책임과 중복되는 별도 규칙을 만들기보다, Verify를 없앴을 때 실제로 곤란한 기능이 무엇이고 기존 도구로 가능한지 확인해 달라고 요청했다. 이 문서는 현재 구현·소비 경로와 한정 실행을 대조한 검토 결과다. Verify 제거·새 도구 설치·운영 전환은 수행하지 않았다.

## 판단

일반 제품 검사와 필요한 근거의 보존은 기존 실행 도구·Git/파일 해시·Work 기록으로 수행할 수 있다. 다만 개별 수단이 존재하는 것과 Verify가 자동으로 실행 전 식별·검사·제한된 출력·증거 저장·상태 연결을 묶어 수행하는 것은 다르다.

현재 Reference 제품 코드가 Verify status/receipt를 소비하는 경로는 확인되지 않았다. 실제 코드 소비자는 Harness의 Recover와 Verify 내부이고, 설치·생성 지침에도 의존성이 있다. 따라서 제품 실행 때문에 Verify 전체를 유지해야 한다는 근거는 발견하지 못했다. 자동 증거 보존과 프로세스 실행 제한의 차이는 제거 여부를 정할 때 함께 판단해야 한다.

## 기능별 대조

| 기능 | 기존 수단과 확인 범위 | 제거할 때 남는 차이 |
| --- | --- | --- |
| 제품 검사 실행 | sample의 고정 unittest 명령을 직접 실행해 7개 통과 | 검사 자체에는 Verify가 필요하지 않음 |
| 실행 결과·실패 출력 보존 | 현재 실행 도구는 종료 코드와 출력을 반환. Python 표준 라이브러리와 일반 파일 저장으로 stdout/stderr·실패 코드 보존을 임시 fixture에서 확인 | 실제 Work에 언제 어디로 보존할지는 별도 수행. 현재 도구 출력이나 대화가 durable receipt와 같은 수명을 제공한다고 보장하지 않음 |
| 검사한 파일의 식별 | Git 판본·변경분, git hash-object 또는 shasum 활용 가능. 임시 파일 변경이 해시로 구별됨을 확인 | 실행 전 수집·명령/결과와 연결·다음 재개 때 자동 비교는 자동으로 생기지 않음. 커밋 번호만으로 미커밋·미추적 파일이나 환경을 식별할 수 없음 |
| 이전 증거의 현재 유효성 | development가 관련 변경·검사 조건을 대조하고 재사용/재실행 판단 | Recover의 선언 파일 자동 변경 감지는 사라짐. 기존 자동 비교도 선언 밖 입력, 변경된 claim/argv, 의미적 충분성까지 확인하지 않음 |
| 실행 시간과 자식 프로세스 제한 | 현재 exec_command의 yield_time_ms는 반환 대기 시간. Python subprocess timeout은 직접 실행한 프로세스를 종료할 수 있음 | Verify의 POSIX 일반 자식 프로세스 묶음 종료와 동일하지 않음. 실제 차이를 아래 격리 실행에서 확인 |
| 출력 제한·경로 정규화 | 실행 도구의 max_output_tokens는 반환 출력량 제한. 파일 저장이나 기존 검사 helper 사용 가능 | 전체 로그 저장의 크기 한도, stdout/stderr별 보존량, Project root 치환까지 동등하다고 확인하지 않음 |
| 증거 덮어쓰기 방지와 상태 연결 | 고유 파일명·배타적 파일 생성 등 기존 파일 기능으로 구성 가능 | Verify의 증거 저장 후 atomic status 교체를 현재 일반 흐름이 자동 수행하지는 않음. 그 machine status를 없애면 같은 상태 계약을 재구현할 이유도 별도 판단 |
| 선언 경로·명령 형식 검사 | 대상 경로·명령을 담당자가 확인하고 현재 host 권한 안에서 실행 | Verify의 특정 argv/경로 거부와 동일한 기계 검사는 아님. 기존 Verify도 임의 프로그램의 전체 부작용을 격리하는 장치는 아님 |

현재 환경에는 git, python3, shasum, tee가 있고 timeout/gtimeout 명령은 발견되지 않았다. 다른 host나 설치 환경에 이 결과를 일반화하지 않는다.

## 직접 확인한 실행

### 동일 제품 검사

Reference Project root에서 실행했다. bytecode 생성을 피하기 위한 -B 외에는 sample verify.json이 지정한 제품 검사와 같다.

```text
python3 -B -m unittest tests.test_config_loader -v
Ran 7 tests in 0.000s
OK
exit_code: 0
```

### 일반 실행 도구의 대기는 종료 제한이 아님

유한한 1.2초 대기 프로그램을 yield_time_ms=250으로 실행했다. 250ms 뒤 실행 중 session을 반환했고, 후속 조회에서 `completed after yield`와 exit 0을 확인했다. 따라서 이 매개변수를 Verify의 timeout과 동등하게 해석할 수 없다.

### 직접 프로세스 제한과 자식 프로세스 묶음 제한

임시 프로그램은 자식을 생성한 뒤 2초 대기한다. 자식은 시작 표시를 남기고 0.7초 후 완료 표시를 남긴다. 제한은 0.3초이며, 두 실행 모두 자식 시작 표시를 확인했다.

| 실행 수단 | 시간 초과 | 시간 초과 뒤 자식의 완료 표시 |
| --- | --- | --- |
| Python subprocess.run(timeout=0.3) | 발생 | 생성됨. 직접 프로세스 종료 뒤에도 자식이 수행됨 |
| 현재 Verify의 run_bounded_verification | 발생, exit 124 | 생성되지 않음. 구현의 process group 종료와 일치 |

Verify 실행 엔진만 임시 입력으로 호출했으며 product receipt/status를 쓰는 verify_workspace는 실행하지 않았다. 스스로 별도 session으로 분리한 자식이나 다른 운영체제는 시험하지 않았다. 자식과 부모는 모두 유한한 프로그램으로 구성했다.

### 파일·출력의 일반 수단

임시 실패 명령의 exit 7, stdout `fixture output`, stderr `fixture failure`를 표준 라이브러리와 파일로 보존했다. 임시 파일 내용 변경 전후 git hash-object 결과가 달랐다. 이는 기존 수단의 수행 가능성 확인이며, 설치된 범용 기록 절차나 제한된 출력 수집기를 만들었다는 뜻이 아니다.

실행 전후 sample의 status 1개와 기존 Verify receipt 12개의 SHA-256을 비교해 모두 동일함을 확인했다. 제품·Harness 실행 본문은 수정하지 않았다.

## 이미 있는 helper와 실제 소비자

[record_harness_tests.py](../../../../.agents/skills/apply-context-harness/scripts/record_harness_tests.py)는 Python 소스 해시·unittest 결과·제한된 출력을 receipt로 저장하고, POSIX에서는 직접 프로세스 시간 초과 시 process group을 종료한다. 그러나 unittest discovery·Python 소스·harness_test 증거에 맞춘 도구다. claim/canonical basis나 product status는 맡지 않으며, 부모가 먼저 종료된 뒤 남는 자식까지 같은 deadline으로 기다리는 Verify 구현과도 다르다. 그대로 범용 제품 Verify의 대체라고 할 수 없다. 코드로 확인했고 이 helper의 새 실행 시험은 하지 않았다.

실제 연결은 [Recover packet](../../../../reference-project/context/work/harness/recover/packet.py), [receipt 비교](../../../../reference-project/context/work/harness/recover/receipts.py), [render](../../../../reference-project/context/work/harness/recover/render.py), [CLI](../../../../reference-project/context/work/harness/cli.py)에 있다. Verify 모듈만 제거하면 CLI import와 Recover의 status 요구가 남으므로 함께 전환해야 한다. 기존 증거는 역사 자료로 접근 가능하게 보존하고 현재 결과로 자동 승격하지 않아야 한다.

[Workspace 생성 스킬](../../../../reference-project/.agents/skills/create-context-workspace/SKILL.md), [생성·전환 계약](../../../../reference-project/context/work/workspaces/CREATE-AND-TRANSITION.md), [이식 스킬](../../../../.agents/skills/apply-context-harness/SKILL.md)과 그 application-contract, Harness 순환 검사도 전환 대상이다. 역사 records의 과거 실행 언급은 활성 의존으로 세지 않았다.

조사한 저장소 범위에서 기존 CI workflow·Makefile·package scripts·tox/pytest 실행 체계는 발견하지 못했다. 외부 CI가 대신 증거를 보존한다고 가정하지 않는다. Noline과 다른 Desktop 저장소는 조사하지 않았다.

## 논의에 제시할 안

development의 검증·근거 재사용과 record-work의 기록 책임은 유지한다. 별도 Verify 단계와 고정 Workspace 계약의 유지 필요는 확인되지 않았다. 자동 파일 비교·실행 증거 묶음은 편의와 보장 차이를 인정하고, 필요한 결과를 기존 도구로 확보하는 방식과 비교할 수 있다.

실제로 실행이 오래 걸리거나 자식을 남기는 검사, 출력량이 큰 검사에서는 적절한 실행 제한이 필요하다. 해당 검사 도구·실행 환경이 제공하는지 확인하고, 부족할 때 실행 도구 쪽에서 보완하는 것이 책임상 맞다. 이번 검토만으로 모든 host가 이를 제공한다고 주장하거나 새 공통 runner를 설치하지 않는다. 사용자의 제거 결정과 실제 전환은 아직 남아 있다.

구현 근거: [Verify 계약](../../../../reference-project/context/work/harness/verify/README.md), [실행 조정](../../../../reference-project/context/work/harness/verify/service.py), [프로세스 제한](../../../../reference-project/context/work/harness/verify/process_scope.py), [파일 식별](../../../../reference-project/context/work/harness/verify/evidence.py), [증거 저장](../../../../reference-project/context/work/harness/verify/storage.py), [development 검증](../../../../reference-project/.agents/skills/development/references/verification/INDEX.md).
