# Maintainer 문서 통합 편집 기준 보완

2026-09-11, 사용자는 Noline Ticket 사례에서 Maintainer가 새 정보를 기존 문맥에 정리하지 않고 뒤에 이어 붙여 가독성을 떨어뜨린다고 지적했다. 첫 판단에서 공통 정보 순서를 해법으로 제안했으나, 사용자는 문서마다 구조가 다르므로 고정 순서를 두는 문제가 아니라고 정정했다.

첫 보완에서는 일반 편집 기준을 Spec·Ticket 운영 문서에 두어 `current` 중심으로 범위를 좁혔다. 사용자는 가독성이 Spec·Ticket에만 관한 문제가 아니라고 다시 정정했다. 이에 직접 영향 범위를 Maintainer가 쓰는 모든 사람용 Workspace 문서로 넓혀, 최종 기준은 Workspace 전체 층을 소유하는 [Workspace collection](../../../../reference-project/context/work/workspaces/README.md)에 배치했다.

이 기준은 `current`의 Spec·Ticket·추가 memory·state, `source/index.md`, `output/index.md`, `records/README.md`와 새 날짜별 record에 적용한다. 각 문서는 자기 Owner 안에서 새 내용을 의미에 따라 조직하고, 기존 문서는 중복·대체된 내용을 정리해 통합한다. 새 record도 대화 순서를 전사하지 않고 재검토에 필요한 사건·근거·결과를 구성한다. Machine 계약·status·receipt, raw source와 제품 산출물은 이 작성 기준의 대상이 아니다.

[Maintain 계약](../../../../reference-project/context/work/harness/maintain/README.md)은 이 Workspace canonical을 적용하고 가독성의 맥락적 선택은 agent가, 경로·preimage 같은 결정적 거부는 Guard가 맡는 관계만 소유한다. 수동 Maintainer의 [`workspace-context-maintainer.toml`](../../../../reference-project/context/work/harness/maintain/workspace-context-maintainer.toml)도 canonical을 직접 가리킨다. 자동 semantic 경로에는 Workspace collection 계약을 추가해 Maintain README·Spec/Ticket 계약과 함께 실제 prompt에 포함되도록 했고, 해당 연결을 `test_codex_session`에서 확인한다.

글로벌 `ai-system_*` reference는 수정 대상이 아니라 이 배치를 재점검하는 읽기 전용 기준으로 사용했다. 그 결과 지속할 작성 기준을 Workspace canonical에 남겨 Maintain 제거 뒤에도 유지하고, agent의 맥락적 편집 판단과 Guard의 결정적 부작용 검사를 구별했다. 이번 Workspace state도 별도 최신 사건 구역을 추가하지 않고 기존 Maintainer 상태에 통합했다. 중단된 전역 연결 지도 수정 시도는 실제 변경을 남기지 않았으며 글로벌 reference 파일은 수정하지 않았다.

Reference Maintain 단위 테스트 65개와 TOML parse, `git diff --check`가 통과했다. Reference 전체 테스트는 124개 중 123개가 통과했고, 이번 변경과 무관한 Verify descendant timeout 시험 1개가 기존과 같은 타이밍 실패를 냈다. 이번 변경은 source Project 지침 구성에 한정하며 Noline 설치본과 사례 Ticket은 수정하지 않았다. 실제 semantic 재생 평가와 host activation은 수행하지 않았다.
