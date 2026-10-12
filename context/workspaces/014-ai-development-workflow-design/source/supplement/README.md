# 후속 비교의 추가 근거

기존 평가가 원래 rollout이나 별도 worktree로만 연결했던 핵심 근거를 보완했다. 다음 자료는 새로운 전체 수집이 아니라 기존 세 비교를 재검토하기 위한 발췌다. 각 출처·범위·hash는 [supplement manifest](../supplement-manifest.json)에 있다.

## 기록과 재개 비교

먼저 [기록 시점 비교 읽기본](../reading/noline-evaluation/reviews/record-timing-followup.md)을 읽는다. 아래 JSONL은 `source_line` 값으로 찾으며, 추출 파일의 실제 줄 번호와 다르다. 원래 도구 호출·출력과 일부 공개 메시지를 보존했다.

| 세션과 발췌 범위 | 보존한 파일 |
| --- | --- |
| 01a0f20d — 원본 2874–2887, 2909, 3022–3033행 | [선택 사건](selected-rollout-events/01a0f20d-50a5-78e2-a665-e2c59c34987e/selected-events.jsonl) |
| 01a0f772 — 원본 30–35행 | [선택 사건](selected-rollout-events/01a0f772-73ab-7823-b282-bddb19124b7e/selected-events.jsonl) |
| 01a1052a — 원본 7264–7267행 | [선택 사건](selected-rollout-events/01a1052a-4e61-7072-9b81-ff44449e5b85/selected-events.jsonl) |
| 01a1109a — 원본 33–36행 | [선택 사건](selected-rollout-events/01a1109a-4735-7a13-adbf-08a9f84300b4/selected-events.jsonl) |

## 문서 기준 전후 비교

먼저 [문서 기준 비교 읽기본](../reading/noline-evaluation/reviews/document-guidance-followup.md)을 읽는다.

- [01a0c8eb 선택 사건](selected-rollout-events/01a0c8eb-70a7-75a2-9dfe-fd440b7c6bd7/selected-events.jsonl): 원본 2235–2260, 2336행의 지정 사건.
- [별도 worktree의 Project 문서](worktree-project-context/context/project/README.md): 33편의 현재 관찰판. HEAD는 `759cba3485b0e907c34fbd3a2c2cd136943c8716`이고 미커밋 변경을 포함한다. 10월 1일 당시와 동일한 판본이라고 증명한 것은 아니다.

## 철회한 기능과 후속 구현 비교

먼저 [철회와 후속 구현 비교 읽기본](../reading/noline-evaluation/reviews/withdrawal-followup-comparison.md)을 읽는다. [01a0ad3d 선택 사건](selected-rollout-events/01a0ad3d-d8d0-7f33-a3fa-c9eaf01d3f30/selected-events.jsonl)은 당시 미커밋 구현과 검증·철회의 직접 근거를 담는다. 원본 630–645, 865–875, 935–945, 985–1000행과 768·932·949·958행의 지정 사건을 보존했다.

## 연구의 직접 원문

- [07 연대기 원문](research-original/07-tripproof-spec-driven-continuity/original/spec-driven-retro-chronological.md), [07 개념별 원문](research-original/07-tripproof-spec-driven-continuity/original/spec-driven-retro-conceptual.md).
- [05 회고 원문 자료](research-original/05-tripproof-harness-retro/original/): 07·09 분석이 참고하는 일부 직접 근거다. 당시 자료이며 현행 실행 지시가 아니다.

## 판본과 추출의 한계

지정한 여섯 rollout에서 공개 메시지와 도구 사건을 보존했다. reasoning·analysis·summary·system/developer·자동 삽입 지침 등은 제외했다. 선택 payload가 현재 원본의 해당 행과 같음을 확인했다. 최종 사건 수와 선택 행은 manifest에 있다.

01a0f20d·01a0f772·01a0c8eb 원본 전체 파일은 기존 corpus meta에 기록된 hash·크기와 달랐다. 따라서 이번 발췌의 현재 원본 동일성은 확인했지만, 원본 전체가 최초 평가 수집 때와 동일한 판본임을 증명한 것은 아니다. 차이 원인은 판단하지 않았다. 이 한계와 worktree의 역사판 한계를 당시 효과에 대한 확신으로 덮지 않는다.
