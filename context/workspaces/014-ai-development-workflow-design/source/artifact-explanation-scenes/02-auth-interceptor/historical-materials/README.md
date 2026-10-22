# 인증 코드의 첫 답 전 관측판

동일 세션의 `.jsonl.zst` 압축본에서 직접 도구 호출·결과를 찾았다. 압축 해제본 해시는 기존 corpus 메타와 일치한다. [manifest](manifest.json)에 원 경로·파일별 해시·원문 위치·추출 방식을 보존한다. `source_line`은 압축 해제 JSONL의 **1부터 시작하는 실제 줄번호**다. 이전 조사 임시본의0부터 시작한 ordinal과 혼동한 표기를 정정했다.

- `observed/auth-interceptor-observed-20260922-0155Z.ts`: 실제39 도구 출력에서 추출한 대상 전체 코드.
- `observed/auth-store-observed-20260922-0155Z.ts`: 39의1~250행과44의240~끝을 이어 복원했다. 중첩11행의 일치를 확인했다.
- `observed/auth-transport-observed-20260922-0155Z.ts`: 같은 읽기의 transport 전체15행.
- `observed/auth-consumers-observed-excerpts-20260922-0155Z.txt`: 관련 API·fetcher·Axios의 지정 범위 발췌. 전체 파일이라고 확대하지 않는다.
- `observed/auth-selected-raw-events.jsonl`: 원25·27·32·34·37·39·42·44 레코드.25→27의 스킬 본문 읽기,32→34의 미커밋 상태가 포함된다.
- `later-reference/`: 62ce226은 질문 뒤 커밋이다. 직접 읽기 관측판이 있으므로 당시 입력 대신 사용하지 않는다.

사용자20의 붙여넣기 코드와 위 도구 관측판이 설명 대상을 고정한다. 당시 interceptor·auth Store는 수정 상태, transport는 미추적이었다. 이 turn은 설명 요청이므로 새 제품 코드 변경 diff가 있는 사건은 아니다. 기존 Git 커밋만으로 당시 코드를 대신하지 않는다. 사용자55·73의 이후 요청은 평가 자료이며 생성자에게 주지 않는다.

관측판은 당시 도구가 읽어 반환한 텍스트에서 추출한 파일이다. 전체 working tree·실기기 동작 복원을 뜻하지 않는다. `observed`의 raw에는 당시 읽은 스킬 본문도 들어 있으므로 비교 실행자에게 폴더 전체를 주지 않는다. 코드 관측판과 필요한 소비자 발췌를 선택하고, 실행 스킬은 비교 조건에 따라 따로 고정한다.
