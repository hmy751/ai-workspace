# Maintain 책임·테스트·도구 연결 리팩터링

## 승인된 범위

사용자는 비용 개선 전에 코드와 테스트를 읽고 검토하기 쉽게 책임별로 정리하도록 요청했다. Recover·Verify 내부 개선은 미루고 Maintain, 필요한 공통 fixture, 호출 진입점과 문서를 범위로 확정했다. 도구 지원은 Codex·Claude의 실제 의존성을 분리해 같은 기능을 연결하는 목적이며 호스트·실행기의 자유 조합 시스템은 요구하지 않았다. 기존 기능을 보존하고 설명 주석과 docstring은 한국어로 정리한다.

## 구현

- 기존 `host_adapter.py`의 1,783줄은 runtime의 연결·이벤트·상태 저장·조회·worker·알림으로 분리했다. 명시적인 생성자 의존성을 사용하며 다중 상속이나 동적 서비스 탐색을 도입하지 않았다.
- 기존 `codex_session.py`에서 공통 입력 구성과 응답 검증을 분리하고 Codex 실행·재개는 `adapters/codex_session.py`에 배치했다.
- 기존 `operation.py`는 bootstrap, 엄격한 결정 검증, 변경 정책·준비·transaction·service로 분리했다. 기존 bootstrap/decision/apply 함수 18개의 실행 본문은 docstring을 제외한 AST 비교로 동일함을 확인했다.
- 기존 공개 모듈 세 개와 공통 Harness CLI 호출은 유지했다. JSON schema·role 설정·runtime v1/v2 형식은 유지한다.
- Noline의 기존 Claude hook과 5개 테스트를 읽고 Reference에 적응했다. `.claude/maintain.json`과 `.claude/maintain-runtime/`을 사용하고 worker에도 원래 설정 경로를 전달한다. 기존 의미 판단 실행기는 두 호스트 모두 Codex다. Claude 모델 실행 기능을 새로 구현한 것으로 해석하지 않는다.
- Claude hook에서 잘못된 payload는 실패 notice로 처리하고, 재귀 Stop은 pending turn을 소비하지 않도록 했다. 명시한 빈 session id를 주변 환경의 session으로 대체하지 않는다.
- 테스트를 runtime/adapters/contracts/semantic/apply/support에 배치했다. 기존 67개 중 이동한 64개 시나리오의 본문과 assertion이 동일함을 구문 비교로 확인했다. 나머지 3개는 공통 Harness CLI 검사다. 새 배치와 원본을 함께 실행해 136개 통과를 확인한 뒤 중복 원본 파일을 제거했다.
- 공통 `harness/testing.py`의 준비 단계를 작은 메서드로 나누고 Verify 전용 실행물 생성을 선택 가능하게 했다. 기본 동작은 유지하고 Maintain만 이를 생략한다. Maintain host fake는 각 테스트가 독립적인 타입과 호출 기록을 가진다.
- 코드 구조·검증 진입점은 [STRUCTURE](../../../../reference-project/context/work/harness/maintain/STRUCTURE.md), 테스트 지원 역할은 [테스트 README](../../../../reference-project/context/work/harness/maintain/tests/README.md)가 안내한다.

## 검증 결과

명령은 `reference-project/`에서 실행했다.

```bash
python3 -B -m unittest discover -s context/work/harness/maintain/tests -t . -p 'test_*.py' -q
python3.11 -B -m unittest discover -s context/work/harness/maintain/tests -t . -p 'test_*.py' -q
python3 -B -m unittest discover -s . -p 'test_*.py' -q
python3 -B -m unittest context.work.harness.verify.tests.test_verify.VerifyTests.test_timeout_covers_descendant_after_group_leader_exits -q
```

- Maintain: Python 3.14.3과 Python 3.11.15에서 각각 82개 통과.
- 전체: Python 3.14.3에서 141개 중 140개 통과. Verify의 descendant timeout 테스트 한 건 실패.
- 변경 전 전체 baseline에서도 126개 중 같은 Verify 테스트 한 건 실패. 변경 뒤 해당 테스트 단독 실행은 통과했다. 전체 green으로 기록하지 않는다.
- 외부 모델 호출 없이 임시 Project에서 두 도구의 동일 session id 격리, Claude 설정 독립, 중복·subagent·재귀 hook, 잘못된 입력, 실제 CLI와 별도 worker 프로세스 진입을 검증했다.
- `git diff --check` 통과. 정적 이름 검사에서 미정의 전역 이름이 발견되지 않았다.

자동 승인 검토가 테스트 일괄 삭제를 차단해, 기존 67개 통과 복원 → 새 배치 추가 → 시나리오 동일성·양쪽 실행 확인 → 중복 제거 순서로 진행했다. 추가적인 전체 메서드 이름 변경은 API 변경 위험으로 차단되어 적용하지 않았다. 현재 서비스 호출 이름을 유지하며 추가 변경 없이 검증했다.

## 변경하지 않은 범위와 검증 상한

Recover·Verify 구현·테스트, 제품 코드, Noline 적용본, 실제 hook 등록·binding·runtime, 모델 설정은 변경하지 않았다. Reference에는 Claude wrapper와 admission 설정만 추가했으며 실제 Claude hook을 활성화하지 않았다. 전역 하네스와 reviewer도 변경하지 않았다.

실제 host의 신뢰·hook 호출 순서·권한 유지·UI 전달과 의미 판단 품질은 자동 테스트가 입증하지 않는다. Noline 이식과 비용 receipt·instruction isolation·checkpoint·rollover·semantic replay는 후속 단계다. 이 기록 시점의 코드 변경은 미커밋 상태다.
