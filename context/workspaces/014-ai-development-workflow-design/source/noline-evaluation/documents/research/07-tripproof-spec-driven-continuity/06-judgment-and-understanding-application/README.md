# 판단 연속성과 이해 지원 공동 적용 준비본

이 폴더는 판단 연속성의 `reconsider-work`와 이해 지원의 세 스킬을 한 프로젝트에서 함께 사용하기 위한 **판단 기록과 공동 배포용 v0**를 소유한다. 네 스킬의 책임은 유지하고, 프로젝트에 의존하는 진입 안내와 동반 지침 색인만 최소한으로 일반화한다.

2026-09-08 대화에서 함께 두는 방향을 정하고 준비본을 만들었다. **적용 대상은 미정이고 실제 설치는 하지 않았다.** TripProof와 context-harness는 적용 후보이며, 이 이름만으로 대상 저장소·경로·운영 계약을 확정하지 않는다. Maintainer 선택과 연결은 별도다.

이후 Workspace 012에서 Spec·Ticket과 Main·Maintain의 관계를 스킬에 연결하고 [08의 통합 준비본 v0](../08-skills-spec-ticket-integration/README.md)를 만들었다. [후속 논의 결정](../08-skills-spec-ticket-integration/01-discussion-decisions.md)에 합의와 정정 근거를 보존했다. 이 폴더의 v0는 입력 판본으로 유지하며, 실제 대상의 설치·운영 연결은 미정이다.

## 읽을 곳

- [공동 적용 판단 기록](01-joint-application-decisions.md): 두 연구에서 이어받는 책임, 대화에서 정정한 전제, 원문 대조, 제3 리뷰를 거쳐 유지한 선택과 남은 판단
- [리뷰와 확인 기록](02-review-and-validation.md): 배경 분석을 제외한 제3 리뷰의 입력·결론·한계와 준비본에 실제 수행한 검사
- [Spec·Ticket 통합 결과](../08-skills-spec-ticket-integration/README.md): 후속 논의 결정과 Main·Maintain 관계를 반영한 별도 v0. 이 폴더의 기존 v0는 수정하지 않았다.
- [v0 준비본](v0/README.md): 실제 파일 구성, 원본 대비 변경, 나중에 대상 프로젝트에 이식할 방법
- [v0 manifest](v0/manifest.json): 입력 판본과 파일별 출처·차이·해시, 배포 연결 목록

지금 함께 넣어도 되는지와 왜 크게 바꾸지 않았는지는 판단 기록에서, 이식할 파일과 조정할 위치는 v0에서 확인한다. 배경 분석 전체를 설치 시 필수 읽기로 넘기지 않는다.

## 원본과 준비본의 관계

판단 연속성의 개별 설계와 원본은 [05의 현재 v0](../05-judgment-continuity-solution-direction/v0/README.md), 이해 지원의 개별 설계와 원본은 [09의 현재 v0](../../09-tripproof-cognitive-debt/v0/README.md)가 계속 소유한다. 이번 작업에서 두 원본을 수정하지 않았다. 이 폴더는 포함한 원본 판본과 일반화한 사본을 고정하며 자동 동기화하지 않는다.

`v0/payload/`만 이식할 실행 지침·설정·상대 연결이다. 상위 판단·리뷰 문서와 manifest는 연구 및 배포 근거이며, 프로젝트의 전역 규칙이나 새 스킬 호출 절차가 아니다. 네 스킬을 하나의 스킬로 합치거나 maintainer·hook·고정 reviewer를 추가하지 않는다.

준비본의 수정과 출처 관리는 이 공동 적용 작업의 담당자가 맡고, 실제 설치 후의 관리 위치는 대상 프로젝트에서 정한다. 작업 진행과 산출물 지도는 [Workspace 010](../../../../workspaces/010-tripproof-joint-application-v0/README.md)이 소유한다. 문서 작성·정적 검사·독립 리뷰는 실제 host 발동이나 판단·이해 효과를 증명하지 않는다.
