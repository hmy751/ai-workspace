# Active와 history 층위 분리

날짜: `2026-08-12`

## 발단

작업 문서가 계속 쌓일 때 현재 유효한 내용과 과거 작업 결과가 섞이지 않도록, 사용자가 context 아래에 두 층위를 두자고 제안했다.

- active: 현재 유지되는 내용 중심
- history: 평소 작업하면서 만든 문서와 판단의 누적 기록

## 반영한 결정

- `context/active/`를 재진입 시 먼저 읽는 현재 상태 owner로 둔다.
- `context/history/`를 작업·판단·검증의 시간순 기록으로 둔다.
- `context/source/`는 이 두 층과 섞지 않고 근거 원본 계층으로 유지한다.
- 작업 중 생긴 상세 내용은 history에 남기고, 검증 후 현재도 유효한 부분만 active에 반영한다.
- 과거 history를 지우거나 현재형으로 고치지 않고, 상태 변화는 새 history와 active 갱신으로 표현한다.

## 최초 active owner

- `active/project.md`: 장기간 유지되는 목표·기준·제약과 source 경계
- `active/work.md`: 현재 문제·상태·근거·불확실성·다음 행동
- `active/index.md`: 재진입 순서와 load route

## 아직 결정하지 않은 것

실제 harness가 history 작성이나 active 반영을 어느 시점에 요구하고, 어떤 검증 실패에서 자동 또는 수동 갱신을 일으킬지는 후속 운영 구조 설계에서 정한다.
