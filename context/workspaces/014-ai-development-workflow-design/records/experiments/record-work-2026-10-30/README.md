# Record Work의 두 번 호출 적용 시험

2026-10-30 현재 설계 대화의 원문 발췌와 임시 Workspace에서 기록 담당자를 두 번 호출했다. 현재 대화의 실제 subagent 생성·followup 기능으로 같은 담당자에게 후속 과업을 전달했다. 실제 prototype·Reference에 기록을 맡긴 시험이나 새 제품 세션의 자동 발견 시험은 아니다.

| 입력·결과 | 확인할 것 |
| --- | --- |
| [첫 입력](first-input.md) | 원본 세션 L951~L1025까지만 제공. 이후 발화는 파일에도 없었다. |
| [전체 입력](conversation.md) | 두 번째 호출에서 L1030~L1200을 추가. 필요한 앞선 원문도 접근 가능하게 유지했다. |
| [초기 memory](initial-workspace/current/memory/index.md.txt) | 기존 Main 기록 방식과 논의 중 상태 |
| [첫 memory](first-result/current/memory/index.md.txt) · [첫 과정 기록](first-result/records/2026-10-30-recording-responsibility.md.txt) | 원문 판단·직접 수정의 A 선택과 아직 제안인 입력/호출 세부 구별 |
| [후속 memory](second-result/current/memory/index.md.txt) · [후속 state](second-result/current/state/index.md.txt) · [후속 기록](second-result/records/2026-10-30-record-work-design.md.txt) | 재사용·입력·Work 중심 역할·이름과 적용 요청을 갱신하고 실제 실행 미확인을 유지 |
| [시험 스킬 입력](skill-input/SKILL.md.txt) | 시험 당시 본문. 실제 실행 정본은 prototype/Reference의 스킬이다. |

첫 호출은 사람용 문서6개, 두 번째도6개를 수정했다. 두 호출의 전체 변경은 지정 임시 Workspace 안에만 있다. 두 번째는 첫 날짜별 기록의 bytes를 보존하고 새 기록과 색인을 추가했다. 실제 제품·스킬·Reference 파일을 수정하지 않았다.

첫 호출에서는 원문에 아직 나오지 않은 같은 담당자 재사용을 미정으로 남겼고, 후속 호출에서는 뒤의 사용자 선택을 반영했다. 후속 원문에는 prototype→Reference 적용 요청까지만 있고 실행 결과가 없어서 그 구현·설치를 완료로 기록하지 않았다. Main이 실제 파일과 원문을 대조해 이 구별을 확인했다.

별도의 첫 시도에서는 L1025까지만 읽으라는 배정과 달리 파일에 이후 원문도 있었고 추출 오류로 L1200까지 노출됐다. 해당 담당자는 수정 전 중단했고 변경이 없었다. 이 시도는 구간 분리·독립 판단의 성공 근거에서 제외했다. 여기 보존한 두 호출은 새 입력과 새 담당자로 재시작한 결과다.

시험의 기록 품질과 동작은 한 대화·한 Workspace의 사례다. 재호출이 이전 읽기를 얼마나 줄였는지나 토큰 비용 절감은 측정하지 않았다. 다른 host의 원문 접근, 사라진 담당자 복구, 병행 파일 충돌, 실제 Noline 적용과 장기 재개 효과는 검증하지 않았다. 원래 파일의 내용·링크를 그대로 보존한 snapshot은 `.md.txt`이며 현재 실행 링크로 사용하지 않는다.
