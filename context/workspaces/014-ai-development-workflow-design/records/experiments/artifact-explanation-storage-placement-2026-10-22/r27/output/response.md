`useStorageStats`의 중복된 표시값 조립을 정리한 결과입니다. [변경 코드](/private/tmp/0402-storage-placement-20261022/r27/result/useStorageStats.ts)에서는 DB·지도·합계 문자열을 `createStorageStats` 한 곳에서 만들고, 조회가 성공하거나 중간에 실패해도 `finally`에서 현재까지 모은 값으로 상태를 갱신합니다. DB 조회 실패 시 Mapbox를 시작하지 않고, 개별 지도 팩 조회 실패 시 다음 팩으로 계속하는 흐름은 유지했습니다. 변경 범위는 이 hook 파일 한 개입니다.

전달된 검사 기록에는 Jest 2개 suite의 7개 테스트, 대상 ESLint, Prettier, diff 공백 검사가 모두 통과한 것으로 남아 있습니다. 테스트는 DB 파일 선별·단위 표시, 부분 실패, 지도 팩별 실패, 새로고침을 다룹니다. 이 결과는 mock을 사용한 hook 동작 검증이며 실제 기기의 FileSystem·Mapbox 연결 확인은 포함하지 않습니다.

client 전체 타입 검사는 아직 실패합니다. 기록된 진단은 `mapbox.ts`의 tuple 타입 오류 1개와 `download.ts`의 `OfflinePack.size`, `OfflinePack.tileCount` 접근 오류 2개로, 앞선 대화에서도 별도 제품 코드 오류로 확인했던 항목입니다. 이번 결과 자료에는 이 세 파일의 수정이나 전체 타입 검사 통과가 없습니다. 위 검사 결과는 전달된 실행 기록을 읽어 보고한 것이며, 이번 답변을 위해 코드를 변경하거나 검사를 다시 실행하지 않았습니다.
