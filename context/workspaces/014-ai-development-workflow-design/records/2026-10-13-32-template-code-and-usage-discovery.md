# 더 풍부한 template 저장소의 코드와 사용 예시 확인

2026-10-13. 사용자 지정 경로 `/Users/hammyeong-yeon/Desktop/20_lab/template`를 읽기 전용으로 조사했다. 현재 코드 기준을 채택하거나 이 저장소를 수정한 기록은 아니다.

## 사용자 요청과 조사 범위

> /Users/hammyeong-yeon/Desktop/20_lab/template 여기 확인하자 여기가 더 풍부하다 내가 이걸 생각했엇는데  code-template 보다 뭐 남은게 있다면 code-template 마저 봐도 되고

앞선 `30_study/code-template`는 짧은 메모였고, 이번 저장소에는 실제 컴포넌트·Hook·store·Storybook 예시가 있다. 현재 질문과 직접 이어지는 Dialog, Field와 폼 조합, 무한 스크롤을 골라 읽었다. 전체 저장소의 품질이나 사용자 선호를 확정하는 조사는 아니다. 앞 자료를 반드시 모두 소진한 뒤 넘어갈 필요는 없으며, 고유하게 남은 질문이 있을 때 다시 참고한다.

확인 시 HEAD는 `8a200e0` (`docs: 프로로젝트 정책 recipe 반영`)였다. 기존 미추적 파일은 `doc/FORM_IMPLEMENTATION_GUIDE.md`와 `doc/react-query/`였다. 이를 정리하거나 변경하지 않았다. `CLAUDE.md`는 과제 대비용 코드·패턴 모음과 문서 관리 방식을 설명한다. README와 package.json도 확인했다. React Query·React Hook Form·Zustand는 의존성으로 선언되어 있지만 설치 버전이나 실행 상태를 검증한 것은 아니다.

## 현재 질문에 연결되는 실제 코드

| 위치 (template 기준) | 확인한 내용 | 논의할 책임 |
| --- | --- | --- |
| `src/component/Dialog/index.tsx`, `index.stories.tsx` | Radix를 import하지 않고 React Context·state·createPortal로 구현한다. 내부 상태 방식과 open/onOpenChange 외부 제어를 지원하며 실제 Storybook 사용 예시가 있다. | 프로젝트 공통 API와 내부 구현 수단을 구별한 사용자 설명에 대입할 실제 사례. 라이브러리판과 동작이 동등하다고 확인한 것은 아니다. |
| `src/store/useConfirmDialogStore.ts`와 Dialog story | store가 제목·설명·열림·확인 callback을 보관하고, story가 Dialog props와 부품을 연결한다. | 공통 Dialog 동작과 화면 밖에서 호출하는 확인 흐름의 경계. |
| `src/component/FormSection/Field/index.tsx`, `FormSection/index.stories.tsx` | Field는 제목·입력 배치·설명·메시지를 제공한다. Story에는 useForm의 register·errors·handleSubmit 및 Controller로 입력 컴포넌트를 연결하는 예가 있다. | UI 구성과 폼 도구의 상태·검증을 실제로 어떻게 연결했는지 비교할 수 있다. |
| `src/component/InfiniteScrollContainer/index.tsx`, `index.stories.tsx`, `src/hooks/useInfiniteScrollObserver.ts` | story가 useInfiniteQuery를 호출한다. 컨테이너는 데이터·요청 상태·fetchNextPage를 받고, 관찰 Hook은 IntersectionObserver와 다음 페이지 호출 조건을 맡는다. 항목 UI는 children 함수로 받는다. | 기존 요청 도구·재사용 Hook·표시 컴포넌트의 책임 배치와 호출부의 선택권. |

Dialog의 Confirm은 callback을 호출한 뒤 setOpen(false)를 실행한다. 비동기 완료를 기다리는 코드는 없다. 이 동작이 의도한 공통 정책인지 예제의 편의인지는 사용자에게 확인할 대상으로 남긴다. 코드 스타일이나 자동 수정 대상으로 전환하지 않는다.

## 자료 해석의 한계와 다음 후보

- Storybook 코드는 실제 저장된 사용 예시이지만 런타임 검증이나 제품 적용 실적을 뜻하지 않는다. 이번에는 실행·설치·테스트를 하지 않았다.
- 코드 작성자와 AI 기여, 지금도 유지하고 싶은 설계는 아직 확인하지 않았다. 반복 패턴을 곧바로 사용자 원칙으로 추출하지 않는다.
- 미추적 `FORM_IMPLEMENTATION_GUIDE.md`는 React Native용 문서이며 Controller 의무 등의 문장이 있다. 웹 Story는 register와 Controller를 모두 사용한다. 이 문서의 강한 표현을 웹 코드나 현재 사용자의 보편적 원칙으로 적용하지 않는다.
- 문서의 구조 안내와 실제 파일 배치는 동일하다고 가정하지 않는다. React Query 문서는 실제로 `doc/react-query/`에 있으며 이번에는 목차·검색 범위에서만 확인했다.
- 바로 이어갈 후보는 Dialog 실제 구현과 WithFooter·외부 제어 story의 책임 비교다. 그 뒤 Field와 React Hook Form, 무한 스크롤을 통해 기존 도구에 맡긴 책임을 비교할 수 있다. 이 순서는 Main의 제안이며 고정된 커리큘럼은 아니다.

## Confirm의 초기 의도 확인

Main은 현재 Confirm이 callback 호출 후 즉시 닫히므로 비동기 완료를 기다리지 않는다는 점을 실제 저장 장면으로 설명했다. 사용자는 다음과 같이 답했다.

> 아 나는 비동기 같은 상황은 생각 못했고 확인 누르면 원하는 콜백이 있는경우 하고 그 다음 닫겠지 하고 생각했지 음 고민되네 여기서 버튼 저렇게 두면 쓰는 쪽에서 구분할지 컨펌은 그냥 이런 용도다 하고

사용자는 비동기 상황을 처음부터 고려하지 않았다고 밝혔다. 따라서 현재 Confirm을 의도적으로 동기 확인 전용으로 제한한 설계라고 해석하지 않는다. 콜백이 있으면 실행하고 다음에 닫는 흐름을 생각했으며, 비동기 저장 때 일반 Button과 Confirm을 사용처가 구별해야 하는 구성이 적절한지 현재 고민 중이다. 자동 닫기 정책·비동기 지원·오류 및 진행 상태의 책임은 아직 선택하지 않았다.

당시 Main이 제시한 비교는 즉시 닫는 Confirm과 사용처가 닫기를 제어하는 Button을 구별하는 안, Confirm이 동기·비동기 확인 작업의 정상 완료 후 닫는 안이었다. 후자는 기다리는 동안의 중복 실행과 실패 처리를 어디에 둘지도 정해야 한다. 어느 안도 구현하거나 채택하지 않았다.

## Confirm의 본래 역할에 대한 정정과 비동기 예시 요청

사용자는 첫 번째 안이 Confirm을 단순히 즉시 닫는 버튼으로 재정의하면서 본래 확인 역할과 Cancel과의 관계를 놓친다고 지적했다.

> 용도가 확인이란걸 담당한다는 의미에서 COnfirm이 나온건데 그 본래 목적을 잊고 하는 대안이니까
> 일단 두번째 방향으로 한다면 콛가 구체적으로 어떻게 해서 대처해야할지 예시를 보여줘

Main의 ‘즉시 닫는 Confirm / 비동기에는 일반 Button’ 비교는 현재 유효한 추천에서 제외한다. Confirm을 유지할 이유를 기계적인 닫기 시점만으로 설명하지 않고, 확인 동작을 수행하는 공통 부품의 역할에서 대안을 판단한다. 사용자는 두 번째 방향의 구체 코드를 요청했으며 최종 API나 모든 닫기 정책을 채택한 것은 아니다.

기존 `Button` 구현에 isLoading과 disabled 처리가 있음을 확인했다. 새 예시는 요청 Hook의 진행·오류 상태와 기존 Button을 활용하고, Confirm이 callback의 Promise 완료 후 닫으며 실패 시 창을 유지하는 구성을 제시한다. 사용자 저장소에 실제 기능 Hook이 있다고 확인한 것은 아니며 프로필 저장 Hook은 설명용 가정이다. 콜백이 완료 Promise를 반환해야 한다는 계약, 실패를 정상 반환으로 바꾸면 성공으로 오인할 수 있다는 조건도 함께 설명한다. 실제 Dialog·Button 코드는 변경하지 않았다.

## 컴포넌트를 넘어선 설계 판단의 정정

사용자는 본래 목적을 놓친 대안 제시를 컴포넌트에 한정하지 않는 판단 태도의 문제로 기록해 달라고 요청했다. 이후 지적한 정확한 장면을 구별했다.

> 그러니까 의도가 있고 이해해서 없애는건 좋은데 아까는 COnfirm을 그냥 닫게 하고 뭐 이런거있었잖아? 본래 목적도 고려안하고 그걸 말한 거야

대상은 Main이 Confirm을 즉시 닫는 용도로 남기고, 비동기 저장 화면에서는 일반 Button과 외부 open 제어로 따로 처리하자고 제시했던 첫 번째 안이다. 다음 사용 코드 자체가 나쁘다는 뜻은 아니다.

```tsx
<Dialog open={open} onOpenChange={setOpen}>
  <Dialog.Content>
    {/* 프로필 입력 폼 */}
    <Dialog.Footer>
      <Button onClick={handleSave}>저장</Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog>
```

문제는 Confirm이 확인 동작을 맡기 위해 존재한다는 목적과 Cancel을 포함한 주변 역할 관계를 검토하지 않고, 비동기 문제를 피하기 위해 기존 동작에 맞춰 Confirm의 용도를 ‘바로 닫기’로 축소한 판단이다. 그 결과 확인 역할은 애매하게 남고 예외 상황은 사용처가 우회하게 됐다.

앞으로의 설계 판단에서는 대상이 왜 존재하고 어떤 역할을 맡는지 이해한 뒤, 그 목적에 비추어 유지·변경·통합·제거를 판단한다. 목적과 책임을 검토한 결과 Confirm을 없애거나 일반 Button으로 조합하는 선택도 가능하다. 기존 추상화를 반드시 유지하라는 뜻이나, 사용처의 직접 제어를 금지하는 규칙으로 바꾸지 않는다. 이 기록은 문제를 피하는 대안이 본래 목적을 무심코 바꾸고 있지 않은지 살피기 위한 실제 사례다.
