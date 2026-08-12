# Current work context

마지막 갱신: `2026-08-13`

## 현재 문제

정리된 source와 context 층을 사용해 `output/`에 만들 첫 실제 운영 산출물의 범위를 정한다. 아직 어떤 작업 장면이나 구현 형태도 채택하지 않았다.

## 현재 상태

- context 층을 `current/records`로 정리하고 완료 상태 처리와 maintainer 계약을 맞췄다. 상세 변경과 검증은 [`migration record`](../records/2026-08-13-02-current-records-migration.md)에 있다.
- source 원본과 36개 prior-work snapshot은 변경 뒤 해시가 그대로다.
- 기존 source 분석 문서는 [`../records/2026-08-13-01-source-to-work-direction.md`](../records/2026-08-13-01-source-to-work-direction.md)로 옮겼고, 그 안의 첫 실패 장면은 채택된 설계가 아니라 AI 제안으로 남아 있다.
- 루트 `output/`은 실제 목표 산출물 자리로 비워 두었으며, 아직 실제 운영 산출물은 만들지 않았다.

## 현재 필요한 접근점

- source를 사용한 첫 분석: [`../records/2026-08-13-01-source-to-work-direction.md`](../records/2026-08-13-01-source-to-work-direction.md)
- source 권위와 위치: [`../source/manifest.json`](../source/manifest.json)

## 불확실성과 검증 상한

- 사용자 원문에는 “context의 세 가지 역할”이라고 적혀 있지만 이름과 설명이 확인된 역할은 Project common context와 Work context 두 가지다. 저장 층위를 세 번째 역할로 만들지 않는다.
- 실제 작업에서 `복구 → 필요한 정보 선택 → 행동 → 검증 → records 누적과 current 갱신 → 다음 재진입`이 끝까지 작동한다는 증거는 아직 없다.
- 기존 분석이 제안한 첫 실패 장면을 채택할지, 다른 실제 산출물에서 시작할지는 아직 정하지 않았다.
- maintainer 파일과 routing의 정합성은 로컬에서 확인했지만, 현재 런타임에서는 repo-local custom agent 이름을 직접 로드하지 못했다. 전역 trust를 추가하지 않았으며, 모든 새 세션이 agent를 자동 소비하고 행동을 바꾼다는 지속 효과는 별도 검증이 필요하다.

## 다음 행동

source 분석을 참고하되 기존 AI 제안을 정답으로 두지 않고, `output/`에 만들 첫 실제 운영 산출물의 범위를 사용자와 논의한다.
