# 개발 공통의 참고 관계와 이름 유지 판단 근거 보완

2026-10-20. 사용자가 [123의 점검](2026-10-20-123-other-formation-materials-audit.md)에서 찾은 누락을 수정하고 커밋하도록 요청했다. 개발 공통과 이름·완료 기준의 가까운 형성 자료를 보완했다. 기존 원칙의 의미를 바꾸거나 외부 지침을 새 규칙으로 채택하는 작업은 아니다.

## 실제 반영과 이유

| 대상 | 반영한 내용과 이유 |
| --- | --- |
| [개발 공통 맥락](prototypes/development-workflow/noline-demo/context/personal/development/_background/context.md) | 책임 설명에 토스 초대 예제·작성자 변형·사용자 조건을 연결했다. 구성 설명에는 일반 기준·질문·사례·선택적 읽기를 구체화할 때 사용한 외부 비교와 가져오지 않은 한정을 통합했다. |
| [개발 공통 근거](prototypes/development-workflow/noline-demo/context/personal/development/_background/evidence.md) | 외부 예제와 Main 변형을 구별하고 당시 사용자 발화를 보존했다. Matt·Vercel·pstack·Anthropic의 재접근 경로, 당시 참고한 내용·조정·확인 한계를 남겼다. 단순 참고 목록이나 모든 개인 기준의 외부 권위로 만들지 않았다. |
| 개발 공통의 기존 형성 기록·입구 | 책임 논의와 주제 복원 기록의 해당 과정에 빠진 비교를 보완하고, 2026-10-20 재대조로 복원한 부분임을 밝혔다. 입구에서 외부 예제와 형식 선택에 관한 질문으로 찾아갈 수 있게 했다. |
| [이름 기준의 맥락](prototypes/development-workflow/noline-demo/context/personal/development/naming-and-completion/_background/context.md)·[근거](prototypes/development-workflow/noline-demo/context/personal/development/naming-and-completion/_background/evidence.md) | 문자열 `isError`의 유지 판단을 이득·비용 설명에 연결했다. 당시 코드 관찰과 사용자 원문을 보존하고, 이후 명료함 지향과 함께 읽는 설명은 작성자의 종합이라고 구별했다. |
| [유지 판단 기록](prototypes/development-workflow/noline-demo/context/personal/development/naming-and-completion/_background/records/2026-10-16-iserror-retention.md)·입구·사례 | 비교·유지·후속 지향과 재검토 조건을 기록했다. 사례의 현재 설명은 유지하며 근거와 맥락으로 연결했다. 유지 사례를 영구 허용으로 만들거나 후속 지향을 일괄 개명 명령으로 바꾸지 않았다. |

형식 참고는31·45·61·66·72·97의 보존 기록에 있는 내용으로 복원했다. 외부 웹 원문·외부 템플릿 코드를 이번에 새로 조사하지 않았다. 고정판이 있는 Matt 설계 자료와 당시 main 조회를 사용한 자료를 구별했으며, 이 차이와 재확인이 필요한 조건은 데모의 근거에 남겼다. 데모 독자는 바깥014의 기록 번호를 따라가지 않아도 비교의 핵심·선택 이유·확인 한계를 읽을 수 있다.

본문·사례·형성 자료의 역할과 기존 정책을 유지한다. Project·Work·제품 코드·전역 지침은 수정하지 않았으며, 병렬04-01의 티켓·조사 기록·공용 문서 내 해당 문단은 이번 커밋에서 제외한다.

## 확인

- 두 evidence 파일의 기존 인용14행을 변경 전과 대조해 모두 보존했다. 새 토스 비교 조건 발화와 `isError` 발화는 각각31·45에 보존된 원문과 행 단위로 일치한다.
- Main이 외부 예제와 작성자 변형, 외부 자료의 기여와 미채택 범위, 당시 유지와 후속 명료함 지향을 구별해 읽을 수 있는지 문서 관계를 대조했다. 새 독립 작업자 실험은 이번에 하지 않았다.
- 열람 화면을 재생성했다. 문서120개·코드5개의 원문·해시가 일치하고, 내부 링크727개·앵커238개에서 경로·절 누락이 없다. 모든 로컬 문서 링크는 prototype 안에 있다. 이름 비교는 두 이름 쌍 외에 주석을 포함한 코드가 동일하다.
- 브라우저 화면 실측·제품 테스트·장기 유지 효과 확인은 수행하지 않았다. 이번 변경은 근거와 연결의 보완이며 이전 변경 실험을 이번 결과의 새 검증으로 재사용하지 않는다.

123은 점검 당시의 발견을 보존하고 이 기록으로 실제 반영을 연결했다. current와 기록 색인도 현재 결과에 맞췄다. 사용자 요청에 따라 점검·보완·열람 화면·워크스페이스 기록을 함께 커밋으로 남긴다.
