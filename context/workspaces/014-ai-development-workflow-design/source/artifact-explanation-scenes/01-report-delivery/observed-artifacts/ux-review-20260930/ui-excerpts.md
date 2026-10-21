# 실제 UI 발췌 — 2026-09-30

MobileBuildMCP runtime snapshot과 Simulator native AX에서 화면 수집에 필요한 부분만 발췌했다. 화면 판정/원인 추론은 포함하지 않는다.

## 시작 홈

screenHash: `05vvy7n`

```text
e40|text|text|온라인||
e50|text|text|파리, 프랑스||
e58|text|text|9월 30일 - 10월 2일||
e71|text|text|온라인 전용||
e75|text|text|일정||
e78|text|text|경비||
e76|text|text|2개||
e80|text|text|EUR 25.00||
e84|text|text|다른 여행||
e87|text|text|파리, 프랑스||
e88|text|text|1월 6일 ~ 1월 9일||
```

## 온라인 일정 목록

screenHash: `14u8han`

```text
e50|text|text|온라인||
e63|text|text|2026-09-29||
e65|text|text|0개||
e67|text|text|이 날의 일정을 추가해보세요||
e72|text|text|2026-09-30||
e74|text|text|2개||
e81|text|text|2026-10-01||
e83|text|text|0개||
e85|text|text|이 날의 일정을 추가해보세요||
```

## 온라인 일정 상세

screenHash: `0rbo8q1`

```text
e49|text|text|온라인||
e56|text|text|검증 일정 A||
e63|text|text|루브르||
e64|text|text|Paris||
e72|text|text|2026-09-30||
e74|text|text|17:00||
e78|text|text|EUR 25.00||
e85|text|text|총 경비||
e79|text|text|(1개)||
e92|text|text|경비 내역||
e94|text|text|1개||
```

## native AX 보완

온라인 일정 목록: 파리, 프랑스 메인 / 2026-09-29 0개 / 이 날의 일정을 추가해보세요 / 2026-09-30 2개 / 검증 일정 A 루브르 2026-09-30 17:00 / 검증 일정 B 오르세 2026-09-30 21:00 / 2026-10-01 0개.

온라인 일정 상세: 검증 일정 A / 루브르 / Paris / 2026-09-30 / 17:00 / EUR 25.00 / 총 경비 (1개) / 지도에서 보기 / 경비 추가 / 경비 내역 1개 / 검증 입장료 EUR 25.00 기타.

복구 후 홈: 온라인 / 파리, 프랑스 / 9월 30일 - 10월 2일 / 온라인 전용 / 일정 2개 / 경비 EUR 25.00 / 홈 탭 selected. 기존 Controller/CreateScheduleScreen 경고는 하단 Minimize 상태.

