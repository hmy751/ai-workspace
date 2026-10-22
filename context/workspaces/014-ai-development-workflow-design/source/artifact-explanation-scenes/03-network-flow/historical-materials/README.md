# Network Store의 당시 코드와 직전 변경

동일 세션의 `.jsonl.zst` 압축본에서 직접 도구 호출·결과를 찾았다. 압축 해제본 해시는 기존 corpus 메타와 일치한다. [manifest](manifest.json)에 원 경로·파일별 해시·원문 위치·추출 방식을 보존한다. `source_line`은 압축 해제 JSONL의 **1부터 시작하는 실제 줄번호**다. 이전 조사 임시본의0부터 시작한 ordinal과 혼동한 표기를 정정했다.

- `observed/network-observed-20260917-0331Z.ts`: 원1218의 줄 번호를 제거한 전체307행 코드. 이전02:28 수집 출력의 관측판과도 바이트 일치한다.
- `observed/network-consumers-observed-20260917-0331Z.txt`, `network-tests-observed-excerpts-20260917-0331Z.txt`: RootLayout·Debug·표시 코드와 테스트의 지정 범위 발췌.
- `observed/network-selected-raw-events.jsonl`: 원1213·1218·1222·1227.1213→1218에 실제 스킬·코드 읽기가 함께 있다.
- `preceding-change/tool-events.jsonl`: 사용자1111 뒤 다섯 파일의 수정 전 읽기·변경 명령·검사·추가 읽기.1115·1122·1130·1142·1159·1169·1183과 대응 출력. 모든 제품 파일의 완전한 diff로 확대하지 않는다.
- `git-baseline/network-head-7cfa7db.ts`: 당시 HEAD의118행 코드. 미커밋307행 설명 대상과 다르다.
- `later-reference/network-c578446.ts`: 다음 날 커밋. 당시 `observationVersion` 등이 뒤에 재배치·개명됐으므로 질문의 코드로 사용하지 않는다.

직전 다섯 파일 작업과 network.ts 자체의 변경을 혼동하지 않는다. 현재 질문의 network.ts 관측판과 사용처 발췌가 실제 설명 근거다. 선행 사용자920의 스킬 호출과963의 설명을 지우지 않는다. 질문1209 이후 첫 답1239·사용자1246·답1251은 생성 입력에서 제외한다.

관측판은 당시 도구가 읽어 반환한 텍스트에서 추출한 파일이다. 전체 working tree·실기기 동작 복원을 뜻하지 않는다. `observed`의 raw에는 당시 읽은 스킬 본문도 들어 있으므로 비교 실행자에게 폴더 전체를 주지 않는다. 코드 관측판과 필요한 소비자 발췌를 선택하고, 실행 스킬은 비교 조건에 따라 따로 고정한다.
