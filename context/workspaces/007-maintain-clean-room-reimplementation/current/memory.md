# Maintain clean-room reimplementation memory

마지막 갱신: `2026-08-18`

## 목표

Workspace 005에서 사용자와 합의한 Maintainer 경험을 `reference-project/`에 재사용 가능하게 구현한다. 이전 구현을 줄이는 작업이 아니라, 사용자 장면과 글로벌 책임 원칙에서 필요한 구조를 다시 도출하는 작업이다.

## 이어받을 핵심

- 사용자 동작과 직접 근거는 [`record 01`](../records/2026-08-18-01-clean-room-source-and-behavior-contract.md)이 소유한다.
- Reset된 code baseline과 제외할 과거 구조는 [`record 02`](../records/2026-08-18-02-code-reset-baseline-and-excluded-topologies.md)가 소유한다.
- 005·006의 hook, queue, cursor, transaction, attention과 recovery topology는 요구사항이 아니다.
- 새 세션은 이 요약으로 architecture를 정하지 않고 `reference-project/`와 글로벌 AI-system references를 직접 읽어 판단한다.
- 현재 선택된 구현은 없으며, root automatic Maintain은 actual acceptance 전까지 비활성이다.
