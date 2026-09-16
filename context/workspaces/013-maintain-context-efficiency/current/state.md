# 현재 상태

마지막 갱신: `2026-09-16`

## 현재 구현과 검증

- Reference Maintain을 `runtime/`, `semantic/`, `contracts/`, `apply/`, `adapters/`로 분리했다. 기존 세 모듈은 공개 경로를 보존하는 연결 파일이다. 구현 위치는 [STRUCTURE](../../../../reference-project/context/work/harness/maintain/STRUCTURE.md)에서 찾는다.
- 기존 Maintain 테스트 67개를 보존하고 Claude 연결·도구 격리·CLI/worker·입력 경계 검사를 추가했다. Maintain 82개 테스트는 Python 3.14.3과 3.11.15에서 통과했다.
- Python 3.14 전체 141개 중 140개가 통과했다. Verify의 `test_timeout_covers_descendant_after_group_leader_exits`는 변경 전 전체 126개 실행에서도 실패했고 변경 뒤 단독 실행에서는 통과했다. 이 시간 민감 실패 때문에 전체 green을 주장하지 않는다.
- Noline의 기존 Claude hook을 Reference 공통 runtime에 적응했다. Claude 설정과 runtime은 `.claude` 아래에서 독립하고 기존 Codex 판단 실행은 유지한다. Reference Claude wrapper와 admission 설정은 제공하되 실제 hook은 등록·활성화하지 않았다.
- Recover·Verify·제품·설치 helper 코드에는 후속 전체 Black 요청에 따라 포맷만 적용했다. 내부 리팩터링이나 동작 변경은 하지 않았다. Noline 적용본, 실제 binding·runtime, 모델 설정은 변경하지 않았고 비용 개선·semantic replay·actual host acceptance는 아직 수행하지 않았다.
- 자동 Maintain과 AI-native moment reviewer를 활성화하지 않았다. active 표기는 계속 `012-ai-workspace-publication`이며 이 작업의 선택과 실제 hook activation은 별개다.
- 책임·테스트·도구 연결 리팩터링과 루트 코드 지침은 `3b588e3`에 커밋했다. 이후 Black 설정·전체 포맷 변경은 별도 후속 커밋 단위로 분리한다. 구조 변경의 상세 근거와 테스트 명령은 [리팩터링 기록](../records/2026-09-16-01-maintain-refactoring.md)에 남겼다.
- 대화에서 합의한 코드 기준을 루트 [CODE-QUALITY](../../../../CODE-QUALITY.md)에 정의하고 루트 AGENTS와 같은 본문을 읽는 CLAUDE에서 연결했다. 적용 범위와 연결 근거는 [루트 지침 기록](../records/2026-09-16-02-root-code-quality-rules.md)에서 찾는다.
- 후속 요청에 따라 Maintain의 import·간격·긴 표현을 정리하고 영문 LLM 프롬프트·hook 안내문 아래 한국어 번역 주석을 붙였다. 실행 구문과 전달 문자열은 동일하다. Maintain은 두 Python 버전에서 82개씩 통과했고 전체 회귀는 같은 Verify 실패 한 건이 남았다. [가독성 검증 기록](../records/2026-09-16-03-maintain-readability.md)에서 확인한다.
- 루트 코드 기준을 전역 AI 지침 명확성 레퍼런스와 대조해 목적·적용 조건·행동·예외와 조사·출력의 관계를 정리했다. AGENTS의 적용 대상도 맞췄다. 대표 요청의 문서 검토만 수행했으며 실제 AI 수행 개선은 검증하지 않았다. [지침 정리 기록](../records/2026-09-16-04-code-quality-instruction-clarity.md)에서 확인한다.
- 저장소 루트에 Black 공통 설정과 개발용 의존성을 추가하고 현재 Python 코드에 적용했다. 86개 대상의 포맷 검사가 통과했고 변경한 52개 파일은 커밋의 AST와 동일하다. helper 7개·Maintain Python 3.11 검사 82개는 통과했고 Reference 전체 141개에서는 기존 Verify 실패 한 건이 남았다. [Black 적용 기록](../records/2026-09-16-05-repo-black.md)에서 확인한다.

## 확인된 문제

Maintain의 같은 semantic thread는 이전 의미뿐 아니라 전역 instruction, 과거 prompt·response, decision, 파일 읽기 요청과 도구 출력까지 함께 누적한다. 최근 Noline generation은 grounding 1회와 response-end 4회를 처리하면서 내부 모델 처리가 11회로 늘고 총 입력 1,382,751 token을 보고했다.

같은 thread에는 Codex 자동 compact도 실제 발생했다. compact 직전 입력은 245,929 token이었고, compact 처리 자체가 cache 없이 246,234 input token을 사용한 뒤 replacement history 9개로 줄었다. 다음 입력은 86,490 token으로 낮아졌지만 같은 root turn 전체 입력은 667,478 token이었다. 이는 자동 compact가 실행 불능을 늦추지만, compact 전 반복 비용과 compact 자체의 큰 uncached pass를 피하지 못한다는 근거다.

전체 해결된 Maintain effect 100건은 `no_change` 40, `updated` 54, `needs_user_decision` 6이었다. 60건이 변경 또는 사용자 판단을 요구했으므로 response-end를 표면 규칙으로 대량 skip하는 방식을 첫 개선으로 쓰지 않는다.

## 아직 확인할 것

- 전용 runner에서 일반 Codex instruction discovery를 어느 설정 경계까지 끌 수 있는지와 실제 첫-call token 차이
- 현재 Source와 Noline 적용본의 차이, Noline 고유 Claude hook과 evidence 연결 중 보존할 부분
- semantic checkpoint를 모델 출력만으로 만들지 않고 host의 generation, effect ID, Owner hash와 결합할 최소 schema
- rollover 전후 판단 동등성을 비교할 replay corpus와 사람이 검토할 대표 ambiguity·update 표본
- 모델 cycle 상한에 걸린 사건을 `needs_context`로 보존하고 다음 처리에서 안전하게 재개할 lifecycle

## 다음 행동

1. 책임 분리 diff와 [구현 안내](../../../../reference-project/context/work/harness/maintain/STRUCTURE.md)를 검토한다. 실제 hook 활성화와 Noline 적용은 이 소스 리팩터링의 자동 후속 동작이 아니다.
2. 다음 비용 개선 단계에서는 기존 effect와 원자료로 replay fixture와 비용·정확성 baseline을 만든다.
3. 사용량 receipt·instruction isolation, batched Owner read와 모델 cycle 상한, semantic checkpoint·bounded rollover를 순서대로 검증한다.
4. Reference 회귀·replay 뒤에 Noline 설치본의 차이를 다시 대조해 별도 이식하고 실제 host lifecycle을 검증한다.
5. 구조·비용 개선 뒤에만 reasoning effort 비교를 진행한다. Recover·Verify 내부 리팩터링은 별도 후속 범위다.

구현을 시작하기 전에는 Workspace를 활성화하지 않는다. 이후에도 activation은 구현·검증과 별개의 명시적 사용자 선택으로 남긴다.
