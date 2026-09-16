# Maintain 테스트

테스트는 구현 책임에 따라 `runtime`, `adapters`, `contracts`, `semantic`, `apply`로 나뉜다. 최상위 `test_cli.py`는 공통 Harness CLI를 통한 Maintain 호출을 검증한다. 실행 명령과 코드의 대응 위치는 [구현 안내](../STRUCTURE.md#검증)를 따른다.

- `runtime/`: 명시적 연결, generation 전환, hook 순서, 중복, 실패 차단, 알림, 기존 상태 호환과 잠금
- `adapters/`: Codex 명령·출력, Claude prompt/응답 연결, 도구별 설정 격리와 실제 CLI·worker 프로세스 진입
- `contracts/`: 결정의 exact 필드와 outcome별 허용 조합
- `semantic/`: 실행 도구 없이 공통 판단 입력 구성
- `apply/`: 무변경·사용자 판단의 zero-write, preimage, 경로·링크 정책, Spec·Ticket Owner 연결

`support/host.py`는 runtime 시나리오 준비, `support/semantic.py`는 외부 모델과 프로세스를 대신하는 fake, `support/apply.py`는 결정 생성과 파일 관찰을 맡는다. 공통 Project·Workspace 준비는 상위 Harness의 `testing.py`가 계속 소유한다. Maintain은 `include_verification_scenarios = False`로 Verify 전용 실행물을 생략한다.

기존 결과 assertion을 유지하면서 파일을 나눴다. 파일 수나 테스트 수 자체를 품질 지표로 삼지 않는다. 새 검사는 도구별 상태 혼선, 잘못된 입력, 변경 손상과 같이 실제 회귀 위험이 있는 경계를 검증한다. 테스트용 subprocess는 임시 Project에서 실행하며 실제 모델 호출이나 활성 Workspace 변경을 하지 않는다.
