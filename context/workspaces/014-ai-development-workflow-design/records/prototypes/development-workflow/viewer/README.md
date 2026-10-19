# Prototype 열람 화면을 다시 만들고 확인하기

이 디렉터리는 [development-workflow](../README.md)의 문서·소스·테스트를 한 화면에서 읽게 하는 표시 도구를 소유한다. 기준과 작업 결과의 정본은 각각의 원본 파일이다. [viewer.html](../viewer.html)은 그 내용을 담은 표시 사본이며, 여기에서 데모 코드를 실행하지 않는다.

## 본문을 고친 뒤 다시 생성한다

명령은 `development-workflow/`에서 실행한다. 먼저 담당 Markdown 또는 데모 코드를 고친 뒤 화면을 다시 만든다.

```sh
node viewer/build.mjs
node viewer/check.mjs
```

생성 도구는 로컬에 설치된 `marked`를 사용한다. 기본 모듈 탐색으로 찾지 못하면 이미 설치된 모듈 파일의 경로를 `MARKED_MODULE`에 지정한다. 아래 경로는 예시이며 실제 로컬 경로로 바꾼다. 이 도구는 패키지를 설치하거나 내려받지 않는다.

```sh
MARKED_MODULE="/path/to/marked/lib/marked.esm.js" node viewer/build.mjs
node viewer/check.mjs
```

출력 파일은 항상 이 prototype의 `viewer.html`이다. 새 날짜별 복사본을 만들지 않는다. 이미 열어 둔 화면은 파일 재생성 뒤 사용자가 새로고침해 갱신한다.

## 표시하거나 연결하는 파일

prototype 아래 Markdown과 `noline-demo/examples/authentication/src/`, `noline-demo/examples/authentication/tests/`의 `.mjs` 파일을 전체 내용으로 담는다. 소스와 테스트는 코드를 실행하지 않고 읽기 전용으로 표시한다. 이 `viewer/`의 도구 파일은 본문 목록에서 제외하며 이 안내에서 직접 찾을 수 있다.

첫 화면은 실제 폴더 경로를 따라 탐색하는 모드다. 폴더를 열어 본문을 고르며, 단계별 적용과 세 본문 비교로 전환할 수 있다.

화면에 포함된 파일 링크는 해당 전체 본문으로 전환한다. 포함되지 않은 원기록은 원래 Markdown 위치를 기준으로 경로를 보정한 새 탭 링크로 남긴다. Personal과 Project의 본문을 합치거나 원기록을 표시 파일로 이동하지 않는다.

| 바꿀 내용 | 담당 파일 |
| --- | --- |
| 읽기 순서, 파일 분류, 비교할 세 본문, 표시할 파일 종류 | [build.mjs](build.mjs) |
| 화면 배치, 파일 선택·원문 보기, 내부 전환·원기록 링크 | [shell.html](shell.html) |
| 원본·SHA·경로·앵커·링크 속성의 정적 확인 | [check.mjs](check.mjs) |

## 확인 범위

`check.mjs`는 포함된 파일 목록과 현재 원문·SHA를 대조하고, 소스 전체가 실행 가능한 HTML로 삽입되지 않도록 escape됐는지 확인한다. 읽기 단계·비교 문서, 파일·앵커 경로와 링크 구성, 화면 스크립트 문법도 확인한다. DOM이나 브라우저를 실행하지 않으며 화면 배치·클릭 동작을 실측한 결과는 아니다.

인증 데모의 동작 검사는 별도다. 실행법과 확인한 제품 경계는 [prototype README](../README.md), 실제 수행 결과와 한계는 [Work 상태](../noline-demo/context/work/workspaces/001-login-completion-names/current/state/index.md)에서 확인한다. 표시 도구의 검사를 제품 코드의 검사 결과로 기록하지 않는다.
