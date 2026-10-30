# 2026-10-30 본문 형식 기준과 이름·완료 본문 반영

## 무엇을 반영했나

프로토타입의 형식 도입 `3a28e6a1`을 바로 복사하지 않고, 01-02 마감 판 `6e6dccb8` 및 이름 기준의 background와 대조·보정한 뒤 Reference에 반영했다. 개인 판단의 내용·강도와 제품·Work 책임을 유지하면서 조건·할 일·순서를 찾기 쉽게 하는 변경이다.

- [WRITING-FORMAT](../../WRITING-FORMAT.md): 실제 갈림길·순서·비교에 맞는 형식을 선택한다. 기준 본문의 역할로 적용하며 파일명·같은 목차·부정문 비율을 목표로 삼지 않는다.
- [이름·완료 본문](../../personal/development/naming-and-completion/INDEX.md): “가능한 한”과 설명 의존의 개선 지향을 함께 유지했다. 반환·예외를 이름 하나에 반드시 표현하도록 강해진 문장을 보정했고, 기존 상수·주석·대기 범위와 두 코드 예시를 보존했다. [전체 대조와 대표 질문](../writing-format/records/2026-10-30-format-preservation.md)에 판본·보정·한계를 남겼다.
- [Project 작성 기준](../../project/REFERENCE/composition.md#한-주제의-의미가-이어지게-쓴다): 중복된 형식 안내를 공통 문서로 연결했다. 정의·규칙·이유·예외·주의를 함께 이해하게 구성하는 책임, 제품 설명의 읽기 흐름, 주제 분할·층별 책임·근거 범위는 유지했다.

## 읽기 경로와 대상 적응

[Project root 지침](../../../AGENTS.md)과 [context 입구](../../README.md)에서 작성·수정 시 형식 기준을 찾는다. context-update가 기존에 안내하는 대상 root·context 입구를 통해서도 같은 기준을 읽는다. 스킬 본문이나 실행 담당을 새로 나누지 않았다.

형식의 [형성 맥락](../writing-format/context.md)·[사용자 발화](../writing-format/evidence.md)·도입과 대조 기록을 함께 옮겼다. 초기 실험의 외부 경로는 출처 식별자로 남기고, 필요한 이유·발췌·최종판 대조는 이 Project 안에서 읽을 수 있게 했다. prototype 당시 선택과 Reference의 현재 적용은 구별한다. 개인 이름 기준의 형성 의미는 그대로이므로 그 background는 형식상 다시 쓰지 않았다.

## 확인 범위와 남은 일

원본과 보정본의 판단·강도·조건을 문서로 대조하고, 문자열 isError·저장 후 조회·상태 표현·상수·필수 결과 누락의 다섯 질문에서 같은 판단을 찾았다. 이 과정은 Main의 직접 읽기이며 독립 AI 세션의 동등성 시험이나 사용자 이해 속도 측정은 아니다.

형식 기준과 이름 본문은 보정한 prototype과 같은 내용이다. Reference에서는 기존 root·context 진입과 Project 작성 기준을 맞췄다. 원문 대조·링크/앵커·범위 밖 파일 보존의 실행 결과는 ai-workspace Workspace 014의 `2026-10-30-ticket06-01-writing-format-application.md`와 receipt에 남긴다.

Work·Maintain·제품 구현·다른 개인 기준 본문을 이 형식으로 일괄 바꾸지 않았다. 실제 host의 자동 호출·연속 작업·기록·재개를 함께 확인하는 통합 테스트는02에서 이어가며, 이번 문서 반영을 전체06-01 완료나 운영 효과 확인으로 올리지 않는다.
