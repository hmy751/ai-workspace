# AI Workspace

AI 에이전트와 실제 소프트웨어를 개발하면서 반복해 사용하는 작업 방식과 도구를 모은 저장소다.

개발 목표를 실행 가능한 Spec과 Ticket으로 구체화하고, Project와 진행 중인 Work의 맥락을 구분해 유지하며, 세션이 바뀌어도 필요한 판단과 검증 결과를 이어서 사용할 수 있게 한다. 이 흐름을 실행하는 repo-local skill과 Python Harness, 동작을 확인하는 Reference Project를 함께 제공한다.

## 제공하는 개발 흐름

- **Project context**: 여러 작업에 공통으로 적용되는 제품 의미, 현재 구현, 개발 기준과 결정 이유를 관리한다.
- **Workspace**: 하나의 Work에 필요한 Spec, Ticket, 현재 상태, 선택한 원자료, 산출물과 기록을 묶는다.
- **Recover**: 새 세션이나 실행 주체가 현재 작업에 필요한 내용만 다시 읽을 수 있는 packet을 만든다.
- **Maintain**: 작업 중 달라진 목표·판단·진행 상태를 기존 Context Owner에 반영한다.
- **Verify**: 정해진 검증을 제한된 조건에서 실행하고, 당시 입력과 결과를 지속 가능한 증거로 남긴다.
- **Skills**: 작업 논의, Project 맥락 읽기·갱신, Workspace 생성, 재판단과 설명 절차를 재사용 가능한 모듈로 제공한다.

## 저장소 구성

- [`reference-project/`](./reference-project/): Project context, Workspace, Skills와 Harness가 함께 동작하는 실행 가능한 기준 Project
- [`context/workspaces/`](./context/workspaces/): 이 도구를 만들고 검증하며 쌓은 작업 상태와 기록
- [`context/source/`](./context/source/): 설계와 재검토에 사용한 원자료와 provenance

## Reference Project 실행

Python 표준 라이브러리만 필요하다. 저장소를 받은 뒤 다음 명령으로 주요 흐름과 전체 검사를 확인할 수 있다.

```bash
cd reference-project

python3 -m context.work.harness recover 001-default-timeout
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Reference Project에는 다음 명령도 구현되어 있다.

```bash
python3 -m context.work.harness maintain bootstrap 001-default-timeout --json
python3 -m context.work.harness maintain apply 001-default-timeout path/to/decision.json
python3 -m context.work.harness verify 001-default-timeout
```

각 명령의 책임과 사용 조건은 [Reference Project README](./reference-project/README.md)와 [Workspace Harness](./reference-project/context/work/harness/README.md)에서 확인한다. `verify`는 실제 Workspace의 receipt와 machine status를 갱신하므로 상태 전환이나 인계 증거가 필요할 때 실행한다.
