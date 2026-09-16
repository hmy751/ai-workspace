# 현재 상태

마지막 갱신: `2026-09-16`

## 현재 구현과 검증

- Reference Maintain의 책임·테스트·Codex/Claude 연결 리팩터링과 루트 코드 지침은 `3b588e3`, 저장소 전체 Black 설정·포맷 변경은 `e99965d`에 커밋했다. [Maintain 구현 안내](../../../../reference-project/context/work/harness/maintain/STRUCTURE.md)와 [Black 기록](../records/2026-09-16-05-repo-black.md)에서 앞선 변경을 찾는다.
- 후속 사용자 요청으로 Recover·Verify 내부, 공통 Workspace 계약·fixture, CLI·validation을 같은 기준으로 리팩터링했다. 사용자 커밋 요청에 따라 이 후속 코드와 검증 기록을 하나의 별도 커밋 단위로 관리한다. [전체 Harness 기록](../records/2026-09-16-06-harness-refactoring.md)과 [Harness 진입점](../../../../reference-project/context/work/harness/README.md)에서 구현·검증 위치를 찾는다.
- Recover는 계약·Context 읽기·연결 receipt 검사·packet 조립·출력으로, Verify는 계약·evidence·출력 수집·process 범위·실행·저장·실행 조정으로 나눴다. 공통 `workspace/`는 값·경로·identity·status만 소유한다. 기존 공개 함수·import 경로, 명령과 저장 schema, 제한값과 부작용 순서를 유지했다.
- 기존 Recover·Verify 테스트 메서드 51개는 누락·중복 없이 옮겼다. 50개는 AST가 같고 descendant fixture를 개선한 한 메서드도 기존 assertion은 그대로다. 공통·Verify·CLI 경계 검사 38개를 추가했다.
- Verify 전용 subprocess 시나리오는 `verify/tests/support.py`가 소유하고 필요한 테스트 묶음만 준비한다. 공통 fixture는 최소 기반을 유지하며 실패 시 임시 환경 cleanup을 등록한다. 설명 주석·docstring은 한국어로 정리했고 영문 Recover 안내 아래 번역 주석을 붙였다.
- 최종 Python 3.14.3과 3.11.15 전체 검사에서 각각 179개가 통과했다. 구성은 Recover 35개·Maintain 82개·Verify 33개·공통 Workspace 15개·validation 7개·제품 7개다. 이식 helper 7개, Black 전체 대상 126개와 `git diff --check`도 통과했다.
- 이전에 간헐적으로 실패하던 Verify descendant 검사는 시작 지연이 섞이는 shell launcher를 Python launcher로 바꾸고 assertion 전에 cleanup을 등록했다. 제품 deadline/종료 알고리즘은 그대로이며 0.3초, leader exit 0, timeout exit 124, descendant 종료와 receipt 검증을 유지했다. Python 3.11의 10회 연속 실행과 최종 두 버전 전체 실행에서 통과했다. 모든 OS·부하의 안정성을 입증한 것은 아니다.
- 변경 전 Recover와 새 구현은 미검증·과거 receipt·fresh·변경·누락 5개 상태에서 packet과 렌더 문자열이 같았다. 조립 변경 2개와 receipt의 불필요한 try 제거를 제외한 함수/클래스 47개는 docstring·경계 이름 변경 외 AST가 동일하다. AST 대조는 동작 검사와 함께 사용하며 의미 판단 품질의 보증으로 보지 않는다.
- 루트 [CODE-QUALITY](../../../../CODE-QUALITY.md)가 대화에서 합의한 코드 기준을 소유한다. AGENTS와 같은 본문을 읽는 CLAUDE에서 연결한다. [지침 명확성 검토](../records/2026-09-16-04-code-quality-instruction-clarity.md)는 대표 요청의 문서 대조이며 실제 AI 수행 개선의 평가가 아니다.
- 현재 Codex·Claude의 연결 코드는 같은 Maintain runtime과 apply를 사용하며 도구별 설정·runtime을 분리한다. 두 host의 의미 판단은 기존 Codex 실행을 유지한다. 실제 host acceptance와 hook activation은 소스·테스트 제공과 구별한다.
- Noline 적용본과 실제 binding·runtime·모델 설정, active index는 변경하지 않았다. 비용 개선·semantic replay·actual host acceptance는 미착수다. 자동 Maintain과 AI-native moment reviewer는 비활성이며 active 표기는 계속 `012-ai-workspace-publication`이다.

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

1. 전체 Harness 책임 분리 diff와 [진입점](../../../../reference-project/context/work/harness/README.md)을 바탕으로 후속 비용 개선 범위를 확인한다. 실제 hook 활성화와 Noline 적용은 이 소스 리팩터링의 자동 후속 동작이 아니다.
2. 다음 비용 개선 단계에서는 기존 effect와 원자료로 replay fixture와 비용·정확성 baseline을 만든다.
3. 사용량 receipt·instruction isolation, batched Owner read와 모델 cycle 상한, semantic checkpoint·bounded rollover를 순서대로 검증한다.
4. Reference 회귀·replay 뒤에 Noline 설치본의 차이를 다시 대조해 별도 이식하고 실제 host lifecycle을 검증한다.
5. 구조·비용 개선 뒤에만 reasoning effort 비교를 진행한다. Recover·Verify·공통 코드의 후속 내부 리팩터링은 이번 요청에 따라 구현·회귀 검증했다.

Workspace의 대화상 선택, active index 변경, 실제 Maintain activation은 서로 별개다. 이번 소스 구현·검증으로 어느 활성 상태도 변경하지 않았으며 activation은 별도의 명시적 사용자 선택으로 남긴다.
