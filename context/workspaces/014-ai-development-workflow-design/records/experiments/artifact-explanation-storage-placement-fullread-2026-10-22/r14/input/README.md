# 제공 자료

- prior-conversation.txt: 원 대화 9~1542 공개 발화73개.
- conversation.txt: 1549~2456 공개 발화50개. 마지막 요청은 “그래 이제 코드 변경해봐”.
- pre-change/: 당시 수정 전 hook과 미커밋 테스트.
- documents/: 직전 commit 309b9e6의 Ticket·Spec. 현재 상태 문구는 그 commit 시점이므로 이후 대화와 구별.
- result/: 첫 제품 변경의 실제 diff·최종 hook과 당시 검사 원출력. 2513의 RESULT1~4는 Jest, 대상 ESLint, Prettier, diff 공백 검사. 2523은 프로젝트 TypeScript와 에디터 TypeScript 진단. 원문 그대로이며 이후 개선은 포함하지 않음.
- prior-images/: 선행 대화의 에디터 오류 첨부.
- skill/SKILL.md와 shared/: 제공된 비교 기준판 스킬·공통 기준. 스킬은 앞선 본문 비교와 같은 0b3b167 기준판이며 이 9월 사건의 실제 설치 판본과 동일했다고 가정하지 않음.

## 사용 가능한 스킬

- work-artifact-briefing (skill/SKILL.md): 사용자가 `/` UI에서 `$work-artifact-briefing` skill을 직접 호출했거나, 이미 존재하는 코드·변경·문서·분석·review 결과의 전체 역할·대표 흐름·실제 연결·현재 상태 또는 근거가 보장하는 범위를 이해하려 할 때 원자료를 조사해 설명한다. 한 값·위치 조회, 단순 요약·진행 보고, 구현·수정·진단·review·acceptance 판정이 주목적인 요청에는 자동 적용하지 않는다.
