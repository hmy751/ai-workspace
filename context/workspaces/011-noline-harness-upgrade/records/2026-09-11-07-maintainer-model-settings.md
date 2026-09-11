# Maintainer 모델·추론 수준 명시

2026-09-11 · Workspace 011

## 선택과 이유

사용자는 Maintainer를 Terra medium으로 고정하려다가 역할에 필요한 추론 수준을 재검토했고, 최종적으로 “그럼 테라 하이로 설정하자”라고 선택했다. 이번 변경은 Reference에만 적용하며 Noline 재적용·전역 설정 변경·기존 session의 재실행은 포함하지 않는다.

Maintainer는 대화 요약만 하는 역할이 아니다. 선택 이유와 조건의 보존, 결정과 잠정안의 구분, current와 records의 귀속, 기존 문서와 새 의미의 통합을 판단한다. Main은 이 판단 비중을 이유로 high를 권했다. Medium은 시간·사용량을 줄일 비교 후보이지만 같은 입력으로 두 수준을 비교한 결과는 없다. High를 선택한 사실과 충분한 품질이 입증된 사실을 구별한다.

Noline 03 기록에서 확인한 원문 전달 누락과 작성 기준 문제는 추론 수준과 별개의 원인이다. 모델 설정이 [작성 기준 보완](2026-09-11-06-workspace-document-writing-contract.md)이나 필요한 원문 제공을 대신하지 않는다.

## 설정 원천과 실행 연결

기존 역할 파일과 자동 CLI 명령에는 모델·추론 수준 고정이 없었다. 수동 role 설정만 추가하면 별도로 실행되는 자동 bridge에는 반영되지 않으므로 두 경로의 설정 원천을 연결했다.

- [workspace-context-maintainer.toml](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml)에 `model = "gpt-5.6-terra"`와 `model_reasoning_effort = "high"`를 명시했다.
- [codex_session.py](../../../../reference-project/context/work/harness/maintain/codex_session.py)는 시작·재개마다 같은 TOML 값을 읽고 `--model`과 `-c model_reasoning_effort`로 전달한다. 복원한 thread도 같은 설정을 사용하며 thread identity는 유지한다.
- 설정 누락·읽기 실패·잘못된 TOML·필수 값의 잘못된 형식은 기본 모델로 대체하지 않고 실패한다. TOML 읽기에는 Python 3.11 이상의 표준 라이브러리를 사용하며 해당 기능을 호출할 때만 로드한다.

모델·추론 수준 외에 sandbox, hook 비활성 인자, 출력 schema와 guarded apply 경계는 바꾸지 않았다. 설정 변경은 다음 호출부터 적용되며 이미 진행 중인 호출을 다시 시작하지 않는다.

## 확인 결과와 한계

검사는 Python 3.14.3에서 수행했다.

- Maintain 테스트 67개가 통과했다. 시작·재개·복원 후 재개 인자, 설정 변경의 후속 호출 반영, 잘못된 설정의 실행 전 거부를 확인했다.
- 전체 테스트 첫 실행은 126개 중 Verify의 `test_timeout_covers_descendant_after_group_leader_exits` 한 건이 실패했다. 0.3초 제한 안에 descendant PID 파일이 생성됐다는 assertion을 충족하지 못했다. 해당 테스트를 수정하지 않았으며 단독 재실행과 전체 126개 재실행은 통과했다. 최초 실패의 정확한 원인은 이번에 확정하지 않았다.
- 설치된 CLI의 `exec --help`와 `exec resume --help`에서 모델·설정 인자 지원을 확인했고 `git diff --check`가 통과했다.

실제 모델을 호출해 실행 로그의 모델·추론 수준을 확인하거나 새 문서 품질·사용량·지연을 측정하지 않았다. 이번 결과는 설정과 명령 구성의 검증이며 실제 host activation이나 의미 품질 평가의 완료가 아니다. Reference 변경은 미커밋이고 Noline과 전역 파일은 변경하지 않았다.

## 참고 기준

2026-09-11에 읽은 [공식 custom agent 설정](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)은 역할 파일의 모델·추론 수준 override를, [추론 수준 안내](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning)는 medium의 기본 역할과 high의 복잡한 판단 용도·시간 및 사용량 부담을 설명한다. 전역 `reasoning-allocation.md`는 역할의 판단 난도에 맞춰 모델과 추론 수준을 따로 고르는 검토 기준으로만 읽었으며 수정하지 않았다.
