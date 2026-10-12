# Workspace 공통 실행 계약

Recover·Maintain·Verify에서 실제로 공유하는 값 검사, Workspace 식별,
안전한 파일 읽기, status 인계만 소유한다. Context의 의미·Owner·acceptance나
Recover·Verify 전용 설정·프로세스 실행은 소유하지 않는다.

## 내부 구성

- [validation.py](validation.py): `HarnessError`, exact key·schema·문자열 검사
- [paths.py](paths.py): 선언된 root의 상대 경로·regular file·symlink 방어와 UTF-8·JSON 읽기
- [identity.py](identity.py): 명시한 id를 우선하는 Workspace 선택과 frozen identity
- [status.py](status.py): 현재·과거 status schema, result 정합성, 제품 Verify receipt namespace
- [__init__.py](__init__.py): 공통 공개 계약. 기존 [workspace_contract.py](../workspace_contract.py)는 같은 객체를 재노출하는 호환 경로

어느 책임의 전용 구현도 이 공통 경계로 올리지 않는다. 과거 schema의 읽기
호환은 유지하지만 역사 파일을 수정하거나 새로운 실행 책임을 추가하지 않는다.

## 검증

[tests/test_contracts.py](tests/test_contracts.py)는 값·identity·status 계약과
기존 import 경로의 동일성을 확인한다. [tests/test_paths.py](tests/test_paths.py)는
실제 임시 파일에서 root 이탈·symlink·형식·읽기 실패를 확인한다. Recover·Verify의
통합 테스트는 이 계약이 각 공개 진입점에서도 적용되는지 검증한다.

Project root에서 실행한다.

```bash
python3 -B -m unittest discover -s context/work/harness/workspace/tests -t . -p 'test_*.py'
```
