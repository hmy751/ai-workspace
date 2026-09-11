# Noline Maintainer 문서 통합 편집 기준 적용

Reference source `def91c24e9e87344080517c163c734530472bbe5`의 사람용 Workspace 문서 작성 기준과 Maintainer 적용·prompt 연결을 Noline 설치본에 적응했다. Target 기준점은 branch `refactor/codebase`의 `a51b7592eb71576dc617a01a79e3b9f6cb3e390a`였고, 적용 결과는 Noline commit `37c1fc5`다.

Target의 Workspace collection·Spec/Ticket 계약, Maintain README·Noline agent 정의·자동 prompt·관련 테스트를 좁게 수정했다. Noline용 agent 이름과 설명, root instruction routing, skill·hook·session binding 설정은 유지했다. Application Workspace 001의 state에는 기존 Maintainer 설명과 관계를 통합하고, output·records에서 새 기준과 적용 근거를 찾게 했다. 제품 코드, Product Verify와 machine status는 변경하지 않았다.

Preflight가 고정한 기존 dirty 파일은 `geonames.api.ts`와 Workspace 002의 Ticket 본문·Ticket 색인·state·output 다섯 개다. 적용 뒤 각각의 SHA-256이 preflight와 같음을 다시 확인했으며 이번 커밋에는 포함하지 않았다. Preflight 원본과 전체 Harness 결과는 Noline Application Workspace 001의 `records/receipts/`에 보존했다.

Noline Maintainer 단위 테스트 70개, TOML parse, `node scripts/check-harness.mjs`, `git diff --check`, explicit Workspace 001 Recover와 active/default Recover가 통과했다. `pnpm harness:check`는 검사 본체 전에 pnpm의 `node_modules` 재설치 요구로 중단되어 동일 script 본체를 직접 실행했다. 전체 Harness는 122개 중 121개가 통과했고 Reference에서도 같은 결과였던 Verify descendant timeout 타이밍 시험 1개가 실패했으나, 해당 시험만 분리 재실행하면 통과했다. Semantic 재생, actual-host trust·activation·runtime event와 기존 문서의 실제 가독성 개선 효과는 아직 확인하지 않았다.
