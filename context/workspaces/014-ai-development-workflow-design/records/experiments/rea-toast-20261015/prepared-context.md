# Toast 컨텍스트 작성 참고 예시

**참고 조사용 예시.** 2026-10-16 사용자 요청에 따라 공식 Project 컨텍스트·개발 가이드·변경 지시로 사용하지 않는다. 아래는 당시 입력 사본에서 얻은 설명과 검토 질문이다. [보존 지위와 마무리](../../2026-10-16-46-rea-reference-research-close.md).

2026-10-15 사본 기준. 014의 컨텍스트 구성 비교를 위한 예시이며 template의 공식 개발 가이드로 채택하지 않았다.

Toast는 **알림 데이터는 공유 store가 보관하고, 표시된 항목의 자동 삭제는 ToastItem의 effect가 맡는 구조**다. 호출자는 `useToastStore`의 `addToast`에 title·description·duration을 전달한다. 표시와 자동 삭제가 필요하면 `<Toast />`도 마운트해야 한다.

| 바꾸려는 것 | 읽을 위치 |
| --- | --- |
| 데이터·추가·삭제 액션 | [useToastStore.ts](input/src/store/useToastStore.ts) |
| portal 표시·항목별 삭제 타이머 | [Toast/index.tsx](input/src/component/Toast/index.tsx) |
| 버튼에서 호출하는 예시 | [Toast story](input/src/component/Toast/index.stories.tsx) |

duration 기본값은 5000ms이며 story는 3000ms를 명시한다. **알림 추가 시각부터의 절대 만료를 보장하지 않는다.** 표시부를 없애면 타이머는 정리되지만 store 데이터는 남는다. 다시 마운트하면 남은 알림을 표시하고 전체 duration을 새로 센다. 표시부가 없는 동안 추가한 알림도 마운트 전까지 자동 만료되지 않는다.

이 동작은 React 19.1.0·Zustand 5.0.5와 JSDOM·가상 시간으로 정상 만료·기본값·재마운트·표시부 없는 추가의 4개 시나리오에서 확인했다. 시각적 레이아웃이나 실제 브라우저의 시간 지연을 검증한 것은 아니다. [검사 근거](../../receipts/rea-toast-20261015/runtime-results.json)

실험에서 남긴 검토 질문은 **‘보여준 뒤 일정 시간 유지’가 목적일지, ‘추가 후 일정 시간에 만료’가 목적일지**다. 후자가 필요하면 표시부와 별개의 수명 관리나 만료 시각 저장을 검토해야 한다. 현재 동작을 결함으로 확정하거나 특정 대안으로 바꾸기로 한 것은 아니다. 앱 전체의 Toast 배치와 화면 이동 중 알림 정책은 아직 확인하지 않았다.
