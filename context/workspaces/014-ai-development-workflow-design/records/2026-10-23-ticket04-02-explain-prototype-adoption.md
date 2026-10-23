# 04-02 — explain 생성과 기존 두 실행 경로의 통합

**사용자 요청에 따라 리뷰를 반영한 explain prototype을 만들고 현재 연결을 이전했다.** [본체](prototypes/development-workflow/skills/explain/SKILL.md), [작성 상세](prototypes/development-workflow/skills/explain/references/constructing-explanations.md), [앞선 발화 상세](prototypes/development-workflow/skills/explain/references/prior-explanation.md), [형성 자료](prototypes/development-workflow/skills/explain/_background/README.md)가 현재 산출물이다. 기존 두 스킬 폴더는 후속 요청으로 삭제했고 배경·원문은 explain의 `_background/legacy/`로 옮겼다.

이는 prototype 생성·연결 정리 완료이며 운영 설치·실제 사용자 이해·안정된 수행 개선의 확인은 아니다. 새 응답 비교·추가 리뷰는 하지 않았다. 후속 요청으로 이번 변경을 커밋한다.04-02 전체 완료를 이번 생성으로 자동 선언하지 않는다.

## 요청과 생성 중 정정

사용자 원문:

> 좋아 그럼 리뷰 반영한 구성으로 스킬 만들어봐 본체랑 상세, _background까지 잘 구성하고 기존 두 스킬이랑 연결도 정리해줘

본체와 상세 작성 뒤 사용자 확인:

> 근데 이거 기존에 두 스킬 제거하는걸 감안해서 만든거야? 예상보다 간략한것 같아서

Main이 ‘빠짐없이 대체하는지 확인하겠다’고 답한 뒤 사용자 정정:

> 근데 또 무지성으로 빠짐없이 채우란건 아니고 감안을 했냐이거지

Main은 기존 두 실행 스킬 없이 새 구성으로 설명을 수행해야 한다는 전제를 확인하고, 모든 옛 조항을 이식하는 요구로 확대한 답을 정정했다. 이 발화는 본체 분량을 늘리거나 기존 목차 전체를 복구하라는 지시가 아니다. 새 구성의 목적·행동·조건을 기준으로 작성했고 이 정정을 가까운 형성 근거에도 남겼다.

## 실제 만든 구성과 선택

| 위치 | 현재 책임 |
| --- | --- |
| `explain/SKILL.md` | 질문과 공유 맥락에서 설명 중심을 잡고, 필요한 자료와 실제 대상을 연결해 답을 구성한다. 상세 선택·깊이·첫 결과 연결·마무리와 권한을 직접 다룬다. |
| `references/constructing-explanations.md` | 관계·동작·조건·선택 이유·관찰과 결론을 함께 구성한다. 무엇을 골랐고 왜 필요한지부터 실제 짧은 설명까지 이어지는 작성 과정 예시를 둔다. |
| `references/prior-explanation.md` | 실제 발화의 원뜻과 현재 타당성을 대조하고 보완·정정한다. 후속 질문 전체를 이 상세로 보내지 않는다. |
| `_background/README.md`, `context.md`, `evidence.md`, `records/2026-10-23-unification.md` | 진입과 읽을 조건, 선택 이유, 실제 발화·관찰·예시의 출처, 변경 경과와 적용 한계를 구별한다. |

[한 번의 개선 리뷰](2026-10-23-ticket04-02-composition-improvement-review.md)를 반영했다. 기존 방법이 없었다고 가정하지 않고 작성 과정 예시를 구체화했다. 관계와 이유·근거를 별도 파일로 쪼개지 않았고, 첫 결과에서 원래 질문과 관찰을 연결하다 사실 공백이 드러나면 작업 담당자가 추가 확인 여부를 판단하도록 했다. 실제로 설명을 수행하는 절은 본체에 남겼다.

작성 예시의 여행 코드는 보존 source에서 발췌하고, 보고서 예시는 실제 후속 대화에서 핵심 관계를 추린 문장임을 표시했다. 앞선 발화의 두 예시는 이전 형성 자료의 설명용 사례이며 실제 사용자 반응이나 새 시험으로 취급하지 않았다. 모든 예시를 현재 제품 사실이나 필수 출력 형식으로 승격하지 않았다.

## 기존 두 스킬과 호출자 정리

- [이전 브리핑 경로](prototypes/development-workflow/skills/explain/_background/legacy/work-artifact-briefing/records/2026-10-23-before-explain.txt)와 [이전 복구 경로](prototypes/development-workflow/skills/explain/_background/legacy/explanation-recovery/records/2026-10-23-before-explain.txt)는 실행 스킬 frontmatter와 행동 본문을 제거했다. 새 explain·당시 본문·형성 자료를 찾는 문서다. 독립 설치 대상이 아니다.
- 각 폴더의 `_background/records/2026-10-23-before-explain.txt`에 직전 본문을 바이트 그대로 보존했다. 브리핑은 당시 채택 prototype, 복구는 당시 보류 후보라는 지위를 유지했다. 기존 형성 자료·실험 입력·원응답을 현재 판본으로 덮어쓰지 않았다.
- [현재 스킬 안내](prototypes/development-workflow/skills/README.md)는 development·work-discussion·explain만 현재 실행 본문으로 안내한다. 이전 안내 전문도 explain 형성 기록에 보존했다.
- [공통 기준](prototypes/development-workflow/skills/shared/explanation-and-evidence-criteria.md)의 현재 consumer를 work-discussion·explain으로 갱신하고 기준 내용은 별도 정본에 남겼다.
- development의 결과 전달 문단만 새 explain과 첫 결과의 사실 공백 판단에 연결했다. 병렬 세션의 개발·검토 설계나 다른 역할 본문은 덮어쓰지 않았다.
- prototype README와 열람 화면을 갱신했다. 화면 검사에서 확인한 기존 배경 문서의 바깥 경로 링크5개는 출처 식별자로 정리하고, 잘못된 시험 README 경로는 실제 comparison 파일 식별자로 바로잡았다. 핵심 발췌와 당시 판단·결과를 유지했다.

일반 개념·결과·앞선말을 다루는 새 본문에는 이전의 작업물 대상 제한이나 직접 호출 제목을 옮기지 않았다. 고정 Main·Maintain 기록 배치는 실제 대상의 관리 규칙을 따르는 것으로 정리했다. 이것은 옛 조항의 전수 이식이 아니라 현재 책임에 맞춘 재구성이다.

## 확인한 내용

| 확인 | 결과와 한계 |
| --- | --- |
| YAML·스킬 선언 | Ruby의 YAML parser로 새 frontmatter를 파싱하고 필수 필드·허용 키·이름·설명 범위·미완성 scaffold를 확인했다. 현재 선언은 development·work-discussion·explain 세 개이고 이전 두 경로에는 선언이 없다. |
| 기본 quick_validate | 시스템·bundled Python 모두 PyYAML이 없어 제공된 스크립트는 시작하지 못했다. 의존성을 설치하거나 통과를 가장하지 않고 위 대체 형식 확인과 별도 링크·내용 대조를 수행했다. |
| 이전 본문 보존 | 두 원문 사본의 SHA-256을 전환 전 값과 대조해 일치를 확인했다. 값은 explain 형성 근거에 보존했다. |
| 실행 자료의 연결 | 본체·두 상세가 이전 두 SKILL.md를 실행 의존으로 갖지 않으며 필요한 현행 링크가 존재함을 확인했다. 과거 배경은 재검토 근거로만 연결한다. |
| 코드 예시 | 세 발췌의 실행 코드행과 순서를 보존된 원문과 대조했다. 처음의 연속행 검사에서는 helper의 주석 생략 때문에 불일치했으며, 주석·빈 줄을 제외한 코드행 대조에서 일치를 확인했다. 제품 실행 검사는 아니다. |
| 열람 화면 | 기존 build/check를 사용했다.157개 문서·코드 파일의 원문·해시,874개 내부 링크,260개 앵커와 경계를 확인했고 누락0으로 통과했다. 브라우저 렌더링·제품 동작 시험은 아니다. |
| 변경 형식 | `git diff --check` 통과. 별도 새로운 응답 실험이나 반복 리뷰는 수행하지 않았다. |

화면은 변경 전부터 이전 파일 목록과 맞지 않았다. 재생성 후 드러난 위 기존 바깥 링크를 정리해 최종 검사를 통과했다. 기본 모듈 탐색에 없던 `marked`는 기존 bundled runtime의 모듈 경로를 사용했으며 새 패키지를 설치하지 않았다. 검사 도구 자체는 수정하지 않았다.

## 현재 상태와 후속

이 요청 범위의 스킬 생성·상세·형성 자료·이전 연결 정리는 완료했다. 적용 위치는 Workspace014의 prototype이며 전역 하네스나 실제 Noline 운영 스킬은 변경하지 않았다. 실제 사용에서 판단할 수행 효과와 운영 이식은 별도다. 기존 Network A/B는 미실행 자료로 남으며 자동으로 다음 실행하지 않는다.

이번 생성본을 읽거나 사용한 결과에서 필요한 판단을 이어간다. 통합을 다시 미채택 제안 상태로 되돌리거나, 사용자 설명 기준을 추상적으로 다시 요구하거나, 예전 조항 전체를 채우는 작업을 다음 기본 행동으로 삼지 않는다.

## 후속: 기존 폴더 삭제와 커밋 요청

사용자는 “그럼 기록할거 하고 기존 스킬은 삭제 하자 prototyped에서 그리고 커밋 하자”라고 요청했다. 기존 두 스킬 폴더와 임시 이전 안내를 삭제하고, 형성 자료와 직전 본문 사본을 `explain/_background/legacy/` 아래로 옮겼다. 역사적 선택을 재검토할 자료는 보존하되 독립 스킬 경로는 남기지 않는다. 관련 링크와 현재 안내를 새 보존 위치로 정리했다. 위 이전 안내를 남겼다는 설명은 삭제 요청 전의 경과다.

이번 커밋은04-02 설명 구성·검토·생성·삭제 및 이에 필요한 연결 변경을 대상으로 한다. 다른 대화의 개발 검토 설계 변경은 제외한다. 실제 응답 효과·운영 설치의 확인 범위는 늘리지 않았다.

삭제 후 열람 화면 재생성·검사도 통과했다.155개 문서·코드 파일,870개 내부 링크,260개 앵커에서 누락0을 확인했다. 이전 본문 사본 두 개의 SHA-256은 이동 전과 같다.
