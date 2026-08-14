# Context Harness 재테스트를 위한 rollback

날짜: `2026-08-14`

## 목적

첫 context harness 적용 결과를 Git 이력에 보존하면서 target을 다시 미설치 상태로 만들어, 이후 최신 skill을 같은 Project에 처음부터 재적용할 수 있게 한다. 사용자는 `git reset`으로 이력을 지우지 말고 적용과 제거 흔적을 commit으로 남기라고 지시했다.

## Commit 분리

대상은 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`, branch는 `feat/payment-recovery-mvp`다.

- `527af89 feat: refine payment recovery checkout experience`: 적용 전에 존재한 사용자 제품 변경 `App.tsx`, `styles.css`만 별도로 보존
- `eaacec7 chore: snapshot context harness application`: Harness용 `.gitignore`, `AGENTS.md`, `context/` 42개 파일의 적용 상태와 receipt를 snapshot으로 보존
- `9519a43 Revert "chore: snapshot context harness application"`: `git reset` 없이 적용 commit을 되돌려 Harness를 제거

적용 전 untracked였던 `context/code-map.md`는 적용 도중 사용자가 직접 삭제한 상태를 유지했다. Harness rollback이 해당 파일을 복원하거나 Harness 손실로 기록하지 않았다.

## 최종 상태 검증

- target `git status --short`: 출력 없음
- `git diff --exit-code 527af89 HEAD`: exit `0`
- `AGENTS.md`, `context/`: 존재하지 않음
- 기존 `.gitignore`: Harness용 Python ignore 항목 없이 복원됨
- 최초 기준 `76d8e2f`와 현재 HEAD의 tree 차이: `apps/checkout-web/src/App.tsx`, `apps/checkout-web/src/styles.css` 두 제품 파일뿐

Rollback 상태에서 과거 Harness 고정 argv와 같은 다음 명령을 직접 실행했다.

```bash
pnpm exec turbo run typecheck test build --force
```

결과는 cache 없이 `11 successful, 11 total`, `0 cached`였다. 5개 test file의 31개 test, typecheck와 Checkout production build가 통과했다. 첫 sandbox 실행은 Turbo log 파일 쓰기 권한 때문에 내부 오류로 끝났고, 동일 명령을 target 쓰기가 허용된 환경에서 다시 실행해 위 최종 결과를 확인했다.

## 현재 의미와 상한

- 첫 적용의 코드·계약·receipt는 `eaacec7`에서 다시 볼 수 있지만 현재 target에 설치되어 있지는 않다.
- 제품 코드는 `527af89`에 보존됐고 rollback 뒤에도 같은 tree다.
- Rollback 후 제품 검증은 이 작업에서 관찰한 terminal 결과를 요약한 것이며 별도 append-only verification receipt를 만들지는 않았다.
- 최신 reference와 skill에 추가된 Workspace source/output/minimum-memory 계약은 아직 target에 재적용하지 않았다.
- 브라우저 acceptance, 실제 PG·WebView·운영 효과와 다른 Project portability는 이번 rollback으로 검증하지 않았다.
- 이후 재테스트는 현재 clean HEAD `9519a43`에서 새 preflight와 새 receipt로 시작해야 한다.
