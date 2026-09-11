# Maintainer Sol high 채택

2026-09-11, Workspace 011. 사용자가 [Sol high 추가 시험](2026-09-11-11-ticket03-sol-high-evaluation.md) 뒤 “그럼 일단 sol hight 로 바꿔줘 지침은 수정할필요는 없을까?”라고 요청했다. Reference Maintainer의 기본값을 Sol high로 변경하고 작성 지침의 추가 수정 필요성을 검토했다.

## 설정 변경

[역할 설정](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml)의 모델을 `gpt-5.6-terra`에서 `gpt-5.6-sol`로 바꾸고 추론 수준 `high`는 유지했다. 자동 bridge는 이 파일을 시작·재개마다 읽으므로 런타임 코드를 추가로 변경하지 않았다. 다음 호출부터 적용되며 실행 중인 판단을 재시작하지 않는다. 기존 thread 연결, read-only와 Guard 경계도 유지했다.

기본값을 확인하는 시작·재개·복원 후 재개 테스트의 기대 모델을 함께 변경했다. 과거 비교 시험과 설정 이력, 잘못된 설정을 검사하는 독립 fixture는 당시 의미를 보존했다.

## 작성 지침 판단

[DOCUMENT-WRITING.md](../../../../reference-project/context/work/workspaces/DOCUMENT-WRITING.md)는 이번에 변경하지 않았다. 추가 시험에 남은 문제를 기존 기준과 대조하면 다음과 같다.

- 디렉터리 선택 비용 누락: 선택 이유·받아들인 비용의 보존을 이미 요구하고, 구현과 테스트가 떨어지는 비용을 예시로도 설명한다.
- 조건부 권장의 확정과 전후 비교 검사의 선택 사항화: 조건을 함께 보존하고 권장을 계약으로 올리지 않으며, 작성 뒤 결정 강도가 달라졌는지 확인하도록 돼 있다.
- Ticket과 record의 상세 검사 목록 반복: 현재 기준과 선택 과정의 역할을 구별하고 같은 상세 서술을 복제하지 않도록 돼 있다.

따라서 현재 근거로는 새 원칙의 부재보다 기존 기준을 초안에 충분히 적용하지 못한 문제로 판단했다. 모델 변경만으로 해결됐다는 뜻은 아니다. 다른 문서에서도 같은 문제가 반복되면 기존 작성 뒤 확인 기준의 구체성이 부족한지 재판단한다. 이번 한 사례에 맞춘 규칙을 더 추가하거나 별도 검토 agent를 의무화하지 않았다.

## 확인 범위

모델 변경 뒤 Reference root에서 `python3 -m unittest discover -s context/work/harness/maintain/tests -t .`를 실행해 67개 검사가 통과했다. 시작·재개·복원 후 재개의 명시적 Sol high 인자와 설정 재읽기 검사가 포함된다. 실제 Sol high의 시작·재개 실행 근거는 앞선 추가 시험에 있으며, 이번 설정 변경 뒤 새 유료 모델 호출이나 실제 host 전체 검증은 하지 않았다. Noline 설치본·문서와 전역 reference는 수정하지 않았고 커밋하지 않았다.
