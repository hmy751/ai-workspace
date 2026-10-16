# 무한 스크롤 기능의 관계 탐색 비교

2026-10-15. Toast의 작은 입력으로 관계 탐색 도구의 가치를 판단하기 어렵다는 사용자 지적에 따라, template의 무한 스크롤 기능을 저장소 수준 입력에서 비교한다. 앞선 실험 결과는 Toast에서의 관찰로 유지하며 이번 결과를 미리 정하는 근거로 쓰지 않는다.

## 같은 질문

진입점은 `src/component/InfiniteScrollContainer/index.stories.tsx` 하나다. 다음 개발자가 페이지 크기·스크롤 조건·요청 실패 처리를 바꿀 수 있도록 다음을 찾는다.

1. 기능이 연결하는 파일·외부 라이브러리와 각 책임은 무엇인가?
2. 첫 로드, 다음 페이지 요청, 종료·실패 상태는 어떤 코드와 조건으로 이어지는가?
3. 페이지 크기 변경, 중복 요청 억제, 요청 실패의 사용자 표시를 검토한다면 어디를 함께 읽어야 하는가?
4. 코드로 확인한 사실, 분석 도구가 제공한 관계, 프레임워크 계약에 따른 추론, 실행으로 확인해야 할 사항을 구별한다.

## 입력과 순서

원본 `/Users/hammyeong-yeon/Desktop/20_lab/template`의 src 전체와 package.json·tsconfig.json을 동일 사본으로 보존한다. 의존 구현·문서는 아직 골라 주지 않는다. node_modules·별도 doc·번들·빌드 산출물은 제외한다. 파일·hash·원본 Git 상태는 `../../receipts/rea-infinite-scroll-20261015/input-manifest.json`이 소유한다.

먼저 REA 6.5.0으로 전체 입력을 정적 분석하고, 진입점에서 관계를 조회한다. 분석 결과에서 찾은 근거와 부족한 정보를 `rea-discovery.md`에 고정한 뒤 직접 소스를 읽는다. 직접 단계는 같은 진입점의 import·호출부를 검색·확인해 `direct-context.md`를 만든다. 이후 교차 대조와 필요한 좁은 실행 검사를 수행한다. REA 사용의 최종 평가는 기계 결과만의 설명 능력이 아니라 AI가 관계를 찾고 확인하는 데 실제 더해 준 정보로 한다.

## 무엇을 비교하나

핵심 코드의 발견·변경 영향 후보의 정확성, 불필요한 탐색, 상태·정책의 이해, 근거 재조회, 준비 비용을 비교한다. graph에 나온 파일 수를 도움의 크기로 간주하지 않는다. 일반 module 연결과 실제 함수·상태 흐름을 구별한다. 같은 입력의 반대 방향 탐색으로 공통 코드 변경의 다른 사용처도 확인한다.

## 한계

같은 Main·같은 세션이며 이전 Workspace에서 무한 스크롤의 일부 구조를 접한 적이 있다. REA 결과를 본 뒤 직접 분석하므로 독립 A/B도 시간·토큰의 엄밀한 비교도 아니다. 앞선 Toast와 순서·입력 크기를 바꿔 부족했던 관계 탐색을 관찰하는 사례 비교다. REA가 분석하지 못한 부분을 AI가 원문에서 보완하면 그 출처를 구별한다.

실제 template에 존재하는 연결을 사용하며 복잡성을 높이기 위해 코드를 추가하지 않는다. template 자체가 작은 패턴 모음이면 그 상한을 결과에 명시한다. 원본과 기존 변경을 수정하지 않고, 제품 정책이나 REA 채택을 대신 결정하지 않는다.

## 실행 중 추가한 비교 조건

원본의 확장자 없는 상대 import 해석이 연결되지 않아 같은 입력을 TypeScript 5.8.3 transpileModule로 변환했다. emitted는 ES2022·ESNext·react-jsx, commonjs는 ES2022·CommonJS·react-jsx·esModuleInterop이고 둘 다 source map을 보존했다. 변환 명세는 receipts의 transpile.json·commonjs-transpile.json에 있다. 타입 검사·실제 Webpack 빌드·원본과의 실행 동등성 검증이 아니다. ESM에서도 연결이 실패했고 CommonJS에서는 연결됐다. 이 준비 비용을 숨기지 않으며 원본 코드 분석과 변환 사본 분석 결과를 구별한다.

직접 읽기 중 Provider 설정을 확인하기 위해 .storybook/preview.tsx를 추가로 읽어 supplemental에 보존했다. 초기 입력 밖의 자료이므로 REA 누락으로 채점하지 않는다. 런타임 검사는 원본 input의 TS/TSX를 메모리에서 변환해 실행하며, REA 분석용 commonjs 디렉터리를 실행하지 않는다.

## 재실행

REA 설치는 임시 폴더에 npm의 rea-agents@6.5.0을 --ignore-scripts로 설치한다. 전역 setup은 실행하지 않는다. CLI는 설치 폴더의 node_modules/rea-agents/scripts/rea.mjs다. `node <CLI> analyze-javascript-application <input 또는 commonjs 절대경로> --format json`으로 새 분석을 별도 출력에 보존할 수 있다. macOS sandbox에서 ownership helper 컴파일이 막히면 환경 권한을 확인한다.

저장된 Evidence에 같은 질의를 재실행하려면 이 폴더의 `replay-query.py`를 사용한다. 예: `python3 replay-query.py commonjs-entry-outgoing --output /tmp/rea-infinite-replay`. 기본 CLI 설치 위치는 /tmp/rea-toast-tools이며 --cli로 바꿀 수 있다. 다른 질의 이름은 receipts의 query-executions.json에 있다. 분석 원문은 .json.gz로 무손실 보존했고, 실행 당시 명령에 적힌 .json은 압축 전 이름이다.

동작 검사는 receipts의 runtime-package.json·runtime-package-lock.json을 별도 임시 폴더에 package.json·package-lock.json으로 복사하고 `npm ci --ignore-scripts --no-audit --no-fund --prefix <임시 폴더>`로 설치한 뒤 `node verify-runtime.cjs <임시 폴더>`로 실행한다. 이 명령은 runtime-results.json을 현재 실행 결과로 갱신하므로 당시 증거를 유지하려면 실험 디렉터리·receipts를 별도 위치에 함께 복사한다.
