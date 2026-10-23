# 2026-10-04 Noline 여행 작업 자료 복원

기준은 사용자 질문 source_line 3905 직전의 작업물이다. 첫 답변 source_line 3937 이후는 사용하지 않았다. 3910~3932의 읽기 명령과 출력은 같은 시점의 관측으로 사용했다. 현재 Noline working tree는 복원 원천으로 사용하지 않았다.

## 확보한 상태와 복원 방법

- 당시 HEAD: `ee798e7` (`events/3921-stdout.txt`). 추적 파일 21개의 미커밋 변경과 결정 문서·API 오류 클래스·테스트 파일 등의 미추적 항목은 `status-3921.txt`에 보존했다. `.pnpm-store/`는 제품 코드와 무관한 미추적 항목이다.
- 당시 전체 dirty tree를 한 번에 담은 **완전한 최종 diff는 관측 구간에 없다.** `3696`은 이른 시점의 client/server diff이며, `3781`·`3782`는 최신 로컬 저장소와 여행 data/repository/router의 완전한 개별 diff다. `3832`에서 API 오류 클래스 분리와 router의 fallback 조건 수정이 추가됐다. `3931`의 server diff는 `3696`의 server 변경과 일치한다.
- `files/`는 `ee798e7:path` Git 객체를 기준으로 위 기록 diff와 패치를 적용한 관련 파일이다. `related-source-reconstructed.diff`는 복원 파일과 해당 Git 객체를 비교해 새로 조합한 **관련 소스 diff**이며 당시 `git diff`의 단일 원출력이 아니다. 파일별 출처·방법·SHA-256·불완전 여부는 `manifest.json`에 있다. symlink인 AGENTS.md는 당시 Git link target을 복원했다.
- 원 도구 사건은 `events.jsonl`, 개별 명령의 stdout과 command는 `events/`에 분리했다. `3915`와 `3923`의 합성 도구 출력에는 잘림 표시가 있지만 개별 명령 사건 `3912`~`3914`, `3921`~`3922`의 stdout에는 잘림 표시가 없다. `3932`의 원 합성 출력에도 잘림 표시가 없다. 사건 기록은 선별한 관련 도구 호출·결과만 포함한다.

## 파일별 관측 대조

- `trip-repository.ts`와 `useGetTrips.ts` 복원 전문이 `3913`, `3922`의 연속 `cat` 출력에 정확히 포함된다.
- `trip-local.ts`의 첫 140줄과 `useTripSelection.ts` 전문을 당시 `3931`의 줄번호 출력과 대조해 일치했다. 두 파일의 전체 변경은 `3781`·`3782` diff에서 복원했다.
- `router.ts`의 첫 80줄과 `useGetTrips.ts` 첫 40줄은 `3871` 줄번호 출력과 일치한다. router의 이후 부분은 `3782` 전체 diff 및 `3832` 후속 패치에 근거한다. `3843`은 후속 포맷이 변경 없음이라고 기록한다.
- `query-refresh.ts` 전문은 `3893` 출력, `trips.ts` 전문은 `3800` 출력, Ticket 06 전문은 `3914` 출력에 각각 정확히 포함된다. `apps/server/src/routes/trips.ts` 변경 diff는 `3931`과 대조했다.
- 변경 목록에 없는 호출부·인증·DB 유틸·Spec·Work 안내는 HEAD 객체와 `3921` 상태 출력의 비변경 확인으로 복원했다. `TripDateForm`, `EditTripDrawer` 일부는 `3930`에도 관측된다. `shared/db/utils.ts`, `services/auth/local-access.ts`는 거래·인증 경계 확인에 필요한 같은 HEAD 객체다.
- 미추적 결정 문서는 `3930`의 `cat` 전문, 미추적 `shared/api/errors.ts`는 `3832`의 생성 패치로 확보했다.

## 검사 관측과 공백

- `3853`과 `3931`의 당시 테스트 로그 말미: client 51 suites 통과, 578 tests 통과·1 skipped. `3861`의 `git diff --check`는 출력 없이 종료했고, `3864`의 변경 파일 Prettier 검사는 통과했다.
- client 타입 검사는 `3870`에 Mapbox/offline-map 및 UI package rootDir 관련 오류가 남았다. `3846`의 client+server 합동 ESLint 실행은 server 설정 로딩 오류로 실패했다. 이 검사를 통과로 바꾸어 말할 근거는 없다.
- 당시 변경된 tracked 테스트와 새 untracked 테스트 **전문**은 이 자료에 없다. `manifest.json`의 `missing_full_files`에 목록을 두었다. 테스트 결과 stdout은 그 공백과 별개로 확보되어 있다. `.claude/context/`의 두 dirty 설명 문서 전문도 빠졌다. 따라서 이 보존물은 제품 관련 소스와 당시 검사 결과를 재검토할 수 있지만, 전체 dirty tree나 테스트 구현을 완전히 재구성하지는 않는다.

## 재검증

`manifest.json`의 각 SHA-256을 `files/`의 바이트와 비교한다. symlink 항목은 링크 대상 문자열을 해시한다. 변경 파일은 `ee798e7:path` 객체에 `events/3696`, `3781`, `3782`의 해당 diff와 `events.jsonl`에 든 `3832` 패치를 순서대로 적용해 대조한다. 최종 파일 읽기와의 일치 여부는 위 source_line의 stdout에서 확인한다. 명령 출력의 잘림은 합성 출력과 개별 명령 출력을 구별해 판단한다.
