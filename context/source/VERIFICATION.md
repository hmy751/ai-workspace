# Source intake verification

검증 시각: `2026-08-12T21:28:16+0900`

## 통과한 확인

- 사용자 붙여넣기 attachment와 `00-intake/2026-08-12-pasted-reference-bundle.txt`의 SHA-256이 `a46e6fcb3c5d601e370b0f7f3669fe7ca0736e6729c7b0ce03a1040bccf90e39`로 일치한다.
- Anthropic 공식 문서와 사용자가 지정한 블로그는 각각 HTTP `200`으로 가져왔고, 로컬 HTML에서 기대한 문서 제목을 확인했다.
- 외부 HTML snapshot의 size와 SHA-256을 각 `source-record.md`에 기록했다.
- 사용자 선택 읽기본은 intake 원문과 비교했다. 문구 차이는 없고 wrapper 앞뒤 빈 줄과 한 줄의 Markdown blockquote trailing space만 정규화됐다.
- `manifest.json`은 `jq`로 유효한 JSON임을 확인했다.
- AX 대표 snapshot 18개와 cofathon 대표 snapshot 18개는 각 `snapshot-manifest.tsv`의 SHA-256 및 byte size와 모두 일치한다.
- 두 prior-work snapshot에서 `API key`, `access token`, `secret`, `password`, private-key header의 고신뢰 문자열 패턴을 검색했고 일치 항목은 없었다.
- 새로 작성한 Markdown·JSON 색인 파일에서 줄 끝 공백이 없음을 확인했다.
- `/Users/hammyeong-yeon/Desktop/context-harness`를 독립 Git 저장소(`main`)로 두고, 작업 계층을 `context/source/` 아래에 배치했다.

## 이 확인이 증명하지 않는 것

- 외부 문서의 모든 주장이나 블로그에 인용된 모든 수치가 사실임을 판정한 것이 아니다. 이번 단계는 사용자가 지정한 레퍼런스와 중요 선택을 보존하는 단계다.
- 고신뢰 문자열 검색 0건은 민감정보가 절대 없다는 증명이 아니다. 그래서 비공개 대화 로그는 대표 snapshot에 복사하지 않았다.
- prior-work snapshot은 전체 저장소 복사본이 아니라 운영 방식을 보여 주는 대표 원본 집합이다.
- AX 기록에 적힌 test·validator·ZIP 검증과 cofathon의 hook·test는 이번 intake에서 재실행하지 않았다.
- Git clean은 의미상 최신을 보장하지 않는다. AX `current.md`는 후속 process보다 오래되며, cofathon snapshot은 dirty working tree에서 가져왔다. 각 `source-map.md`에 상태를 명시했다.
- 아직 project common context / work context / harness의 새 운영 구조를 설계하거나 구현하지 않았다.
