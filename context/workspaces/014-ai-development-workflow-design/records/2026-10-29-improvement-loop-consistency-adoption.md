# 05의 관리 단위·근거·현재성 재검토와 반영

2026-10-29. **루트 improvement-loop.md를 제거하고 스킬의 적용 사례와 기존 진입에 통합했다. Personal의 형성 맥락/원문 근거를 분리하고, 평가 주체·낡은 현재 설명·중복 수행 순서를 함께 정정했다.** 사용자 요청에 따른 prototype·기록 수정이며 05 전체 마감·운영 설치·실제 루프 효과 확인은 아니다.

## 사용자 요청과 판단 변화

사용자는 루프가 스킬에 할당돼 있는데 루트 문서가 별도로 필요한지, 같은 이유라면 development에도 대응 문서가 필요한지, 대문자와 CONTENT-POLICY의 일관성이 맞는지 재검토를 요청했다. 독립 감사는 여러 영역을 함께 설명한다는 이유만으로 독립 문서를 두는 근거가 부족하고, Personal을 참조하는 설명과 그 영역을 소유하는 일을 혼동했다고 판단했다. Main은 실제 정책과 대조해 이 판단을 수용했다.

Personal 발췌가 짧다는 이유로 context에 합친 절충도 정책이 구별한 맥락·기록·근거의 책임과 맞지 않았다. 추가 대조에서는 설명 효과 주제의 평가 주체 혼동, 현재 문서의 과거 미정 상태 잔존, 스킬 밖에 반복된 전체 루프 순서를 찾았다. 사용자 반영 요청은 다음과 같다.

> 좋아 그럼 루트 문서 통합이랑 Personal 근거 분리하고 방금 추가로 찾은 것들도 같이 수정해줘. 수정한 뒤에 전체적으로 다시 확인하고 기록도 갱신해줘

이 선택은 기존 두 실행 보완 제안의 채택과 구별한다. 한정 시도의 일반 작업 소비/종료 경로 구체화와 같은 목적에서 수행 수단을 비교하는 사례 교체는 여전히 미반영이다.

## 실제 변경과 현재 읽는 곳

| 정정한 문제 | 반영 결과 |
| --- | --- |
| 스킬 사용 해설이 별도 루트 관리 단위에 있음 | 전체 수행은 [SKILL](prototypes/development-workflow/skills/improvement-loop/SKILL.md), 조건별 사례는 [application](prototypes/development-workflow/skills/improvement-loop/references/application.md), 발견은 기존 prototype/skills README가 맡는다. 옛 파일을 연결 안내로 남기지 않았다. |
| Personal 형성 이유와 직접 발췌 혼합 | [context](prototypes/development-workflow/noline-demo/context/personal/_background/experience-collection/context.md)는 현재 선택 이유, [evidence](prototypes/development-workflow/noline-demo/context/personal/_background/experience-collection/evidence.md)는 두 사용자 발췌, [records](prototypes/development-workflow/noline-demo/context/personal/_background/experience-collection/records/2026-10-29-ownership.md)는 중요한 정정 경과를 맡는다. |
| 사용자 반응에 Main의 평가를 포함 | [설명 효과 주제](prototypes/development-workflow/noline-demo/context/personal/experience/topics/explanation-effects.md)에서 사용자 발화·Main 해석·현행 유지 선택을 나눴다. 원 [10월25일 비교](experiments/explain-flow-readability-60high-2026-10-25/comparison.md)의 사용자 발화와 Main 판단을 대조했다. |
| 수행 순서가 여러 본문에 반복 | SKILL이 대화 전체·관련 본문 검토와 선택·반영·종료를 맡는다. USAGE는 호출 연결과 평소 읽기, Personal MAINTENANCE는 경험의 조회·보존·갱신을 설명한다. |
| current의 과거 미정·검토판 유지 문구 | Spec·memory·state·티켓 색인·05 및 현재 진입을 작성된 실물과 남은 실행 보완/운영 미확인에 맞췄다. 과거 방향이 현재 결론과 섞인 인접 _background/context도 현재 이유로 종합했다. |
| 변경 이력과 현재 경로의 혼동 | 현재 실행 링크는 SKILL/application으로, 과거 판본을 설명하는 기록은 보존판으로 연결했다. 독립 보고와 기존 입력 snapshot은 그대로 두고 companion 안내에서 재접근을 제공한다. |

현재 규칙을 사용하는 사례는 본문 상세이므로 `_background`로 옮기지 않았다. 소문자 application은 스킬의 조건별 상세이며 독립적인 대표 체계 지침이 아니다. development에 대응 루트 파일을 만들거나 모든 스킬의 파일 구조를 같게 맞추지 않았다.

경험 주제 본문에 관찰·현재 해석·열린 후보를 함께 두는 합의는 유지했다. 그것은 경험을 사용하는 본문이며, 관리 계약을 형성한 맥락·원문·기록과 구별한다. 모든 주제에 형식적인 README/INDEX/background 묶음을 추가하지 않았다.

## 보존과 확인 범위

[정정 전 원문과 재접근 안내](reviews/improvement-loop-2026-10-29/README.md)에 루트 문서·Personal context·평가 주제의 편집 전 원문을 보존했다. 각 원래 경로와 SHA는 input/manifest.json에 있다. 기존 10월28일 보고와 고정 입력을 새로운 결론으로 고치지 않았다. 역사적 보고의 제거된 실물 링크는 companion 안내에서 당시 보존판으로 찾는다.

현재 시행 범위는 문서·근거·읽기 경로의 정정이다. 전체 원문 훑기와 다음 실제 사용의 행동/효과, 다른 host 설치·활성화는 수행하지 않았다. 실제 확인 결과는 아래와 같다.

## 반영 후 전체 대조 결과

- **정책·책임:** 일반 진입에서 SKILL과 적용 사례를 구별하고, SKILL에서 조건별 상세와 Personal 관리 계약을 찾는다. Personal은 루프 스킬의 형성 자료 없이도 범위 선택의 이유·두 발췌·정정 경과를 복원한다. 루프 수행 순서와 경험 관리의 책임을 분리했으며, 사용자 요청·전체 대화/관련 본문 검토·공동 선택·즉시 반영·다음 실제 사용 관찰의 합의는 유지한다.
- **내용 보존:** 삭제 전 루트 안내의 세 적용 사례는 링크 위치를 제외하고 새 application의 해당 본문과 일치한다. 기존 고정판과 비교한 SKILL은 소제목·적용 사례의 조건부 연결 외 핵심 실행 내용이 동일하다. 루트에서 반복되던 일반 흐름은 기존 SKILL, 적용 범위와 근거 연결은 해당 본문/Personal 안내에서 찾는다.
- **근거:** Personal의 두 직접 발췌는 인터뷰와 일치하며 context에는 원문 발췌를 남기지 않았다. 설명 효과 주제의 사용자 인용은 10월25일 원 비교와 일치하고, Main의 판단은 별도로 설명한다. 과거 사건·원 비교·사용자 발화를 최신 해석으로 덮지 않았다.
- **현재성:** README·current/index·spec·memory·state·티켓 색인·05·output의 재개 안내를 서로 대조했다. 작성된 실물, 미채택 실행 보완, 운영 미확인을 나누며 과거 미정 문구를 현재 상태로 남기지 않았다. 06·07은 실제 배치/사용 관찰의 범위를 유지하며 실행 입력은 새 SKILL로 연결한다.
- **보존:** 기존 독립 보고와 고정 입력 224개 파일의 해시가 편집 전과 동일하다. 새 원문 보존 3개도 manifest와 일치한다. 제거 직전 판본, 이전 리뷰 판본, 현재 본문을 재접근 안내에서 구별한다.
- **표시·연결:** viewer 재생성·검사 통과. Markdown 211개와 코드 5개의 원문/SHA 일치, 내부 링크 1,215개·앵커 300개에서 누락 0, 로컬 링크는 prototype 내부, 화면 스크립트 문법 통과. 브라우저 렌더링과 제품 동작 검사는 하지 않았다.
- **Workspace:** 이번에 갱신한 진입·티켓·기록·보존 안내 18개 문서의 로컬 경로 918개에서 누락 0, 제거된 루트 파일을 향하는 현재 링크 0. 원문 형태를 유지한 과거 구조 리뷰의 옛 링크는 예외로 companion 안내에서 당시 보존판을 연결한다. 과거의 모든 실험 입력을 현재 경로 검사 대상으로 간주하지 않는다.
- **보조 검사:** Ruby YAML 파서로 스킬 frontmatter의 name·description을 확인했고 `git diff --check`를 통과했다. 원 quick_validate는 이미 확인한 PyYAML 부재 환경이며 그 검증기를 통과했다고 기록하지 않는다.

초기 간이 링크 검사는 과거 실험 입력·인용문까지 현재 문서로 잡고 URL 인코딩도 처리하지 않아 범위 밖 경로와 오탐을 함께 반환했다. 그 결과로 과거 원문을 수정하지 않았다. 이후 현재 prototype은 전용 viewer 검사, 이번 변경의 Workspace 문서는 인코딩을 처리한 경로 검사, 고정 원문은 해시 비교로 나눠 확인했다. 위 결과는 이 구별된 범위의 확인이다.

## 다음 상태

기본 운영 방향과 prototype 실물은 작성돼 있다. [앞선 두 실행 보완](2026-10-28-improvement-loop-review-synthesis.md)의 채택 여부와 05 완료 조건을 대조하는 단계다. 이번 근거 정정은 원 비교의 우열을 재평가하거나 새 사용자 만족을 추정한 것이 아니다. 새 커밋은 만들지 않았다.

## 후속 요청

사용자는 누적 작업과 기록을 커밋하고 첫 번째 실행 보완부터 기존 구조의 연결 위치와 종료 정리를 설명해 달라고 요청했다. 이 요청은 보존과 구체 설명이며 두 실행 보완의 채택·구현으로 해석하지 않는다. 커밋 결과는 이 기록을 포함한 Git 이력에서 확인한다.
