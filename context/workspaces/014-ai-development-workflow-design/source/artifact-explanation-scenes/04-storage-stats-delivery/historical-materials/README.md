# 저장 용량 최초 변경의 코드·diff·검사 근거

원 `.jsonl` 경로 대신 같은 이름의 `.jsonl.zst` 압축본이 남아 있었다. 압축 해제 SHA-256은 기존 corpus 메타와 정확히 일치한다. 최초 변경을 후대 커밋으로 대신하지 않고 원 도구 출력에서 확보했다. [manifest](manifest.json)에 출처·해시·추출 범위를 기록했다.

| 시점 | 자료 | 확인된 범위 |
| --- | --- | --- |
| 2456 직후, 제품 코드 수정 전 | [hook](pre-change/pre-2456-tool-read-useStorageStats.ts), [테스트](pre-change/pre-2456-tool-read-useStorageStats.test.ts) | 실제2468 출력. hook은 직전309b9e6 Git 파일과 바이트 일치. 테스트는 당시 미커밋 파일. |
| 첫 적용 | [도구 patch](first-change/first-application-tool-patch.patch) | 2472 호출 인자. 이후 포맷 작업이 있었으므로 최종 diff와 구별. |
| 첫 보고 직전 | [실제 diff](first-change/first-application-actual-hook.diff), [결과 코드](first-change/first-application-final-useStorageStats.ts) | 2537 diff 출력과2555의81줄 파일 출력. Main이 수정 전 코드에 실제 diff를 적용한 사본이 결과 코드와 바이트 일치함을 확인. 원 repo에 적용하지 않음. |
| 검사 결과 | [2513](first-change/readings/2513.txt), [2523](first-change/readings/2523.txt) | Jest2 suites·7 tests, ESLint·Prettier·diff check 통과. 전체 typecheck는 다른 파일 오류3개로 실패. 당시 도구 결과이며 이번에 재실행한 것이 아님. |
| 당시 Ticket·Spec | [pre-change](pre-change/pre-2456-last-commit-ticket03.md) | 직전309b9e6의 정확한 문서. Ticket의 실제 읽기2530 및 갱신 후 일부2555도 보존. 전체 working tree 동일성은 별도. |
| 원래 첨부 이미지 | [prior-images](prior-images/1720.jsonl) | 1720·1933·2089의 원 user 레코드와 이미지 픽셀을 복원. 이전 공개 corpus의 이미지 공백을 보강. |
| 추가 개선 뒤 | [later-reference](later-reference/post-2645-a147a42-parent-diff.patch) | a147a42는 사용자2645 뒤의 개선 전체다. 첫 변경으로 사용하지 않는다. 후대 재분석 문서도 입력에서 제외. |

첫 보고2560·사용자2632·2645는 기존 `evaluation/`에 있다. `first-change/tool-events.jsonl`은2465~2555 중 도구 호출·결과 레코드를 바이트 그대로 보존한다. AI의 진행 서술과 첫 답을 생성 입력 대신 넣지 않는다. 해당 도구 원문에는 Ticket 갱신처럼 결과를 서술한 자료도 있으므로 시험에 폴더 전체를 공급하지 않고 코드·diff·검사 결과만 선택한다.

`prior-images`는 과거 에디터 문제의 시각 입력이다. 이 이미지를 복원했다고 이번 시험에서 그 오류 수정부터 전부 재현할 필요는 없다. 실제 비교 경계는 [설계 기록](../../../../records/2026-10-22-ticket04-02-historical-materials-and-comparison-design.md)에 있다.
