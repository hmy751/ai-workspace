# Improvement Loop의 구조·본문 편집 반영

**후속 정정:** 루트 유지와 Personal context 내 근거 통합은 [2026-10-29 재검토·반영](2026-10-29-improvement-loop-consistency-adoption.md)에서 대체됐다. 이 문서는 당시 판단과 수행 기록이다.

2026-10-28. 사용자는 [구조 제안](2026-10-28-improvement-loop-structure-proposal.md)을 설명받고 “그래 반영해봐”라고 요청했다. **루트 안내 유지·역할 정리, references의 실행 방법/확인 이력 구별, Personal 근거 소유와 진입 목록 정리를 반영했다.** 새 폴더나 Personal evidence 파일은 만들지 않고 기존 context에 최소 근거를 두었다.

## 반영한 결과

- [당시 전체 안내 보존판](reviews/improvement-loop-2026-10-29/input/improvement-loop-before-integration.txt)는 ‘작업 체계 개선 루프 — 구성과 적용 사례’로 제목과 내용을 정리했다. 전체 관계·읽을 질문·대표 선택·적용 범위를 설명하고, 이번 작성 목록과 다음 검토 지시는 Workspace에 맡긴다. 대표 사례는 확인 조건·가능한 선택·실제 변경 대상의 표로 비교한다.
- prototype와 skills README는 루프를 기존 질문별 진입에 통합했다. 최근 추가 공지와 어긋나던 수동 실행 본문 열거는 정리했다.
- [SKILL](prototypes/development-workflow/skills/improvement-loop/SKILL.md)과 [effects](prototypes/development-workflow/skills/improvement-loop/references/effects.md)는 읽는 목적에 맞춰 소제목만 보완했다. 실행 문장은 그대로다.
- [conversation](prototypes/development-workflow/skills/improvement-loop/references/conversation.md)은 환경 조건을 확인해 사용하는 절차로 읽히게 다듬었다. 세션 식별·메시지 필드·중복·압축·fork/재개·입력 공백의 기존 의미는 유지했다. 특정 날짜의 파일/형식 확인 이력은 [가까운 구조 반영 기록](prototypes/development-workflow/skills/improvement-loop/_background/records/2026-10-28-structure.md)에 보존했다. 과거 기록과 고정판은 다시 쓰지 않았다.
- [Personal 형성 맥락](prototypes/development-workflow/noline-demo/context/personal/_background/experience-collection/context.md)에 범위 확대와 Work 강제 등록 정정의 직접 발췌를 보존했다. 루프 evidence가 이 근거를 참조하며 Personal은 루프 스킬 없이도 해당 경계의 이유·원문을 찾는다.
- 루프의 형성 안내를 현재 검토 경과와 맞추고, 외부 원형의 관점과 우리 파일 형식의 차이를 evidence에 보완했다. 이번 구조 검토의 재대조를 최초 작성 당시 조사로 소급하지 않았다.

## 확인

- 기존 고정 검토판과 비교해 SKILL·effects는 소제목과 빈 줄을 제외한 내용이 동일하다. 루트 해설이 실행 규칙의 새 정본이 되지 않도록 담당 본문을 연결했다.
- Personal의 두 인용은 인터뷰 발췌와 일치한다. Personal 형성 README/context에 루프 스킬을 필수로 따라가야 하는 링크가 없음을 확인했다.
- 고정 검토 입력 220개 파일은 원래 manifest와 모두 일치한다. 현재 prototype의 편집 결과와 과거 검토판을 구별한다.
- viewer 재생성과 검사 통과: Markdown 208개·코드 파일 5개의 원문/SHA 일치, 내부 링크 1,205개·앵커 302개 확인, 경로/앵커 누락 0, 모든 로컬 문서 링크가 prototype 안에 있음, 화면 스크립트 문법 통과. 브라우저 렌더링과 제품 동작 검사는 이번에 실행하지 않았다.
- skill-creator의 `quick_validate.py`는 환경의 PyYAML 부재로 실행되지 않았다. Ruby YAML 파서로 frontmatter를 읽고 name·description을 확인했다. 이 대체 확인을 원 검증기 통과로 표기하지 않는다.

갱신한 Workspace 진입·티켓·제안·반영 기록 9개 문서의 로컬 링크 경로 730개에서 누락이 없었고 `git diff --check`를 통과했다.

## 현재 남은 것

[앞선 실행 개선 두 안](2026-10-28-improvement-loop-review-synthesis.md)의 한정 시도 소비/종료 경로 구체화와 같은 목적에서 수행 수단을 비교하는 사례 교체는 여전히 미반영이다. 이번 요청은 직전의 파일 배치·형식 제안 반영으로 해석했다. 루트 사례의 표 편집은 그 두 안의 채택·완료를 뜻하지 않는다.

05의 다음 판단은 남은 실행 보완의 채택 여부와 완료 조건 대조다. 전역 설치·실제 루프 수행 효과·05 전체 마감은 아직이며 커밋은 만들지 않았다.
