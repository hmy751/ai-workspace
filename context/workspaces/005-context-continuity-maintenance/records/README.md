# Records

이 폴더에는 context continuity와 background maintenance 운영을 구체화하며 만든 지속 가능한 진단, 사용자 판단, 외부 자료 대조, 후보와 결정 근거를 누적한다.

- 파일명은 `YYYY-MM-DD-NN-주제.md` 형식을 사용한다.
- 긴 대화는 trigger·확인된 사실·사용자 판단·미결정을 구분해 남긴다.
- 대화의 정확한 뉘앙스가 판단 근거면 최소 발화 발췌를 보존하고, AI의 해석은 별도로 표시한다.
- 같은 사건을 여러 Workspace에 다시 서술하지 않고, 원래 구현·적용 record를 링크한다.
- 임시 명령 출력이나 매 test 결과를 자동 record로 만들지 않는다.
- 현재 채택된 기준은 `../current/memory.md`, 작업 커서는 `../current/state.md`, 선택된 결과는 `../output/index.md`에서 찾는다.

## 기록

- [`2026-08-17-01-harness-operation-latency-and-role-diagnosis.md`](2026-08-17-01-harness-operation-latency-and-role-diagnosis.md): 30분·26분 문제에서 분리한 Recover·Verify·Maintain·validation 역할, 실제 시간 근거, flake와 반복 비용
- [`2026-08-17-02-context-continuity-and-background-maintenance-framing.md`](2026-08-17-02-context-continuity-and-background-maintenance-framing.md): 사용자 C/E 우선순위와 A 방향, 현업 자료 대조, background maintainer의 자동 쓰기·축적 방지·보고 cadence 후보
