# Apply Context Harness blind 평가

날짜: `2026-08-14`
평가 task: `019ffec6-7cad-7120-b803-a6f4ef6787f3`

## 목적과 격리 경계

repo-local `apply-context-harness` skill이 첫 적용 기록을 답안처럼 재사용하지 않고도 실제 target에 맞춰 이식 절차를 끝까지 수행하는지 확인했다.

- 원본 Project `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`는 branch `feat/payment-recovery-mvp`, HEAD `9519a43`의 clean·Harness 미설치 상태로 유지했다.
- 평가는 격리 사본 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio-skill-test`, branch `codex/context-harness-skill-test`, HEAD `527af89`에서 수행했다.
- 실행 prompt는 `$apply-context-harness`, target 경로, 첫 사용자 장면만 제공했다. 이 Workspace의 기존 current·records·output을 읽는 것은 명시적으로 금지했다.
- 이 기록은 별도 task transcript와 main의 독립 재검증을 근거로 한다. 사람 acceptance를 대신하지 않는다.

## 실행 흐름과 target adaptation

1. target 쓰기 전에 preflight receipt를 만들고 dry-run으로 변경 경계를 확인했다.
2. target의 기존 Project canonical을 유지한 채 repo-local 진입점과 Workspace·Harness를 배치했다.
3. Workspace `output/index.md`의 한 단계 어긋난 상대 링크를 target 안에서 바로잡았다.
4. README의 과도한 test 범위 주장을 실제 검증 범위로 좁혔다.
5. 첫 verify는 `node_modules` 부재로 실패했고 실패 receipt를 보존했다.
6. 네트워크 다운로드 없이 offline frozen install을 수행한 뒤 verify를 다시 실행해 통과시켰다.
7. 성공 status와 receipt를 연결한 뒤 recover를 다시 실행하고, 별도 reviewer가 결과를 독립 검토했다.

`node_modules`, `dist`, `.turbo`, `*.tsbuildinfo`는 설치·build 과정의 ignored artifact로 남기고 적용 산출물이나 evidence 입력으로 올리지 않았다.

## 최종 target 상태

- `AGENTS.md`와 `context/`를 합친 44개 설치 파일이 untracked 상태다.
- tracked worktree diff와 staged diff는 모두 없다.
- commit과 staging은 수행하지 않았다.
- 따라서 이 상태는 검증 가능한 격리 평가물이지 accepted canonical이나 원본 Project 설치가 아니다.

## 독립 재검증

main은 작업자의 요약만 신뢰하지 않고 다음을 다시 확인했다.

- 원본과 격리 사본의 preflight SHA 일치
- recover가 Workspace current와 선택한 Project canonical을 합쳐 정확히 10개 경로만 로드함
- 실행 전 Harness Python source 14개와 Harness test 28개를 연결한 durable receipt
- 제품 verify 입력 36개의 SHA-256·size와 성공 status·receipt linkage
- direct Harness 계약 test 28개 통과
- direct 제품 검증에서 Turbo task `11/11`, test 31개, typecheck와 Checkout build 통과, cache `0`
- 적용 결과에 대한 독립 review 통과

자동 검증 과정은 `recover → 실패 verify → offline frozen install → 성공 verify → recover`의 실패·복구 경로까지 남겼다.

## 독립 review에서 남은 상한

핵심 이식 계약에는 P1·P2 문제가 없었지만, 다음 다섯 가지는 후속 skill 개선이나 더 강한 재시험에 남길 P3 또는 증거 상한이다.

- 44개는 Git이 보여 주는 **non-ignored 설치 파일** 수다. 실행 뒤 ignored `node_modules/`, `.turbo/`, `dist/`, `*.tsbuildinfo`도 격리 target에 남아 있으므로 “working tree에는 `AGENTS.md`와 `context/`만 추가됐다”는 표현은 non-ignored 변경으로 한정해야 한다.
- 별도 task는 첫 상위 지침 탐색에서 Desktop 아래의 지침 **파일명 목록**까지 넓게 출력한 뒤 즉시 target과 당시 source root `output/`으로 범위를 좁혔다. 이 source root는 이후 `reference-project/`로 이름을 바꿨다. 인접 저장소 파일 내용은 열거나 판단에 쓰지 않았지만, 이후 구현은 조상 경로를 직접 확인해 이 불필요한 metadata 노출도 피하는 편이 낫다.
- 과거 002 문서를 읽지 않았다는 사실과 dry-run manifest가 target 쓰기보다 먼저였다는 실행 순서는 별도 task transcript가 뒷받침한다. 최종 filesystem과 receipt만으로는 이 과정의 선후 관계를 독립 증명할 수 없다.
- 평가 branch의 ancestry에는 이전 Harness commit `eaacec7`이 없었지만, 같은 Git 저장소의 `feat/payment-recovery-mvp` ref에는 그 commit이 남아 있어 `git log --all`처럼 전체 ref를 탐색하면 발견할 수 있었다. Transcript에는 별도 task가 이 과거 commit을 열어 사용한 흔적이 없으므로 이번 결과는 **prompt-bounded blind**이며, 과거 이력을 물리적으로 제거한 blind test는 아니다. 더 강한 재시험은 `527af89` tree를 새 Git 저장소로 내보내 수행해야 한다.
- 실제 실행 도구는 Node `v24.19.0`, pnpm `11.19.0`이었고 Project `package.json`은 `pnpm@11.16.0`을 선언한다. verify evidence는 Node·pnpm binary와 설치 dependency bytes를 포함하지 않으므로 같은 도구chain의 정확한 재현성까지 증명하지 않는다.

## 증명한 것과 상한

이번 평가는 과거 002 적용 문서를 입력으로 주지 않은 조건에서 skill이 preflight, target별 수정, 선택적 recover, 고정 verify, durable receipt, 상태 갱신과 후속 recover를 한 번의 격리 적용으로 재현할 수 있음을 확인했다.

다음은 증명하거나 결정하지 않았다.

- 원본 `/Users/hammyeong-yeon/Desktop/payment-recovery-portfolio`에 Harness가 다시 설치됐다는 주장
- 격리 평가물의 commit, staging 또는 사람 acceptance
- 실제 PG, 영속 DB, Android WebView, 웹훅, 브라우저 승인·취소·focus 복귀·모바일 표시와 운영 효과
- 서로 다른 canonical·runtime·test graph를 가진 다른 Project에 대한 portability와 generalization

격리 평가 결과의 채택, 파일 보존·제거, 원본 재적용은 각각 별도의 사용자 판단이다.
