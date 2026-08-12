# Source intake baseline

날짜: `2026-08-12`

## 작업

사용자가 지정한 자료만 대상으로 context+harness 설계를 시작할 source 작업대를 만들었다.

## 보존한 자료

- 사용자의 목표·source 경계·원하는 운영 구조 원문
- 블로그와 Anthropic 공식 문서의 로컬 HTML snapshot 및 사용자 선택 발췌
- 사용자가 공감해 가져온 Codex 의견
- AX MyRealTrip 작업본과 cofathon에서 운영 방식을 보여 주는 대표 원본 snapshot

## 분류 판단

- 외부 원본과 사용자 선택 발췌를 분리했다.
- AI 의견을 사용자 직접 결정으로 승격하지 않았다.
- AX와 cofathon은 정답이 아니라 기존 작업 방식 관찰 자료로 표시했다.
- 비공개 대화 로그, cache, 대용량 중복 fixture는 대표 snapshot에서 제외했다.

## 검증

- raw attachment와 보존본의 SHA-256 일치
- 외부 두 문서 HTTP `200` 및 문서 제목 확인
- AX·cofathon 대표 snapshot의 SHA-256과 byte size 확인
- manifest JSON과 모든 등록 경로 확인

세부 결과와 검증 상한은 [`../source/VERIFICATION.md`](../source/VERIFICATION.md)에 있다.

## 이 시점의 한계

source를 보존한 단계이며, 새 context+harness 운영 구조의 의미적 타당성이나 실제 작동을 검증한 것은 아니다.
