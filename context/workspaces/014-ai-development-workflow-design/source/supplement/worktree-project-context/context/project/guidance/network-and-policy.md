# 연결 관측과 화면 접근을 변경할 때

Network Store, 화면 정책, 제한 안내와 폼의 온라인 기능을 추가·수정할 때 읽는다. 이 본문은 기존 Policy Architecture의 현재 개발 계약을 소유한다. 여행의 선택·활성화와 연결을 잃었을 때의 제품 경험은 [여행 이용](../common/travel-access.md), 실제 화면별 적용과 남은 연결은 [네트워크와 화면 접근의 현재 범위](../current/network-and-screen-access.md)가 설명한다.

## 실제 관측과 화면 실험의 상태를 구별한다

Network Store의 관측은 `online/offline/unknown`이다. 연결되었다는 신호와 인터넷 도달 신호가 모두 확인되면 online, 둘 중 하나가 명시적으로 끊겼으면 offline, 확정할 수 없으면 unknown이다. unknown은 앱 시작 때만 생기는 상태가 아니며 사용 중에도 돌아올 수 있다. online도 특정 서버 요청의 성공을 보장하지 않는다.

화면은 `useDisplayNetworkStatus()`로 Debug override를 포함한 상태를 사용할 수 있다. Router와 sync의 실행 가능 판단은 실제 관측을 사용한다. Debug override를 online으로 바꿔도 실제 연결이 없으면 Remote 요청을 허용하지 않는다. Override 중에는 시험 조작으로 실제 데이터를 바꾸지 않도록 Local 저장·queue 추가를 포함한 쓰기와 sync를 차단한다.

상태를 React에서 표시할 때에는 구독하는 hook을 사용한다. 비React 코드의 getter를 렌더 중 읽는 것만으로 상태 변화가 화면에 반영된다고 간주하지 않는다. 실제 관측과 표시 상태를 모두 `status`라고 숨겨 소비자가 추측하게 만들지 않는다.

## 한 관측 수명 안에서 늦은 결과를 거절한다

네트워크 감지는 `init`부터 `cleanup`까지 하나의 구독 수명으로 다룬다. 같은 수명의 구독을 중복 등록하지 않고, 종료할 때 listener·안내 timer·진행 중 refresh 대기를 정리한다. 종료된 구독의 callback이 새 수명의 상태를 바꾸지 못하게 한다.

Refresh를 바꿀 때에는 다음 관계를 함께 보존한다.

- 동시 refresh는 진행 중 Promise를 공유한다.
- 요청 시작 이후 listener의 새 관측이 들어왔다면 늦은 refresh 결과가 이를 덮지 않는다.
- timeout이나 cleanup으로 끝난 refresh가 새 요청의 대기 표시나 Promise를 종료하지 않는다.
- 전송 실패를 처리하는 `catch`와 관측 결과를 적용하는 코드는 실패를 분류하려는 경계에 맞춰 배치한다.

Unknown 안내의 10초는 `checking`에서 확인 불가 안내로 바꾸는 시간이다. 실제 상태를 offline으로 바꾸는 시간이 아니다. 같은 unknown의 반복 관측은 timer를 다시 시작하지 않고, 사용자의 명시적 재확인은 안내 시간을 다시 시작한다. 확정된 online/offline에서 refresh를 시작하거나 실패했다고 바로 unknown으로 되돌리지 않는다.

Refresh의 앱 대기 종료 시간은 별도 책임이다. 응답이 오지 않는 요청이 재확인을 계속 점유하지 않게 하며, native 요청 자체가 취소됐다는 뜻은 아니다. 이후 실제 관측은 listener로 받을 수 있다. 두 시간이 현재 같아도 변경 이유가 다르므로 하나의 timeout 의미로 합치지 않는다.

## Policy, Router, UI, Service는 연결된 다른 책임이다

| 책임 | 결정하는 것 | 소비 위치 |
| --- | --- | --- |
| Policy | 작업 허용·UI 모드·이유 | 화면·feature 조합부에서 읽는다. |
| Router | Local/Remote 출처와 실행 시점의 거절 | Repository가 요청한다. 화면 제한 뒤 상태가 바뀌어도 다시 확인한다. |
| UI | 안내·버튼·폼·대안 | Policy와 실행 오류를 사용자 경험으로 연결한다. |
| Service | 지도·검색·경로 등 외부 호출 | 해당 서비스의 실제 연결·인증 조건을 확인한다. |

Data hook은 repository를 호출하며 화면 Policy 검사를 넣지 않는다. Router에도 Alert·toast를 넣지 않는다. 데이터 경로의 기준은 [데이터 가이드](local-data-and-sync.md)가 소유한다.

기본 Policy는 online/offline과 active/inactive의 네 조합을 사용한다. Unknown에서는 offline 권한 모드를 재사용하지만 관측과 안내 이유는 unknown으로 남긴다.

인증은 Local 세션과 대상 활성 여부의 선행 조건으로 적용한다. Local 세션이 없으면 로그인 안내, reauth-required이면 활성 여행 Local CRUD 유지·비활성 여행 보호 요청 제한이다. 인증 만료만으로 네트워크를 offline으로 만들거나 공개 서비스에 보호 API 조건을 일괄 적용하지 않는다.

## 아직 모르는 활성 상태를 비활성으로 표시하지 않는다

대상 여행의 활성 조회가 성공하기 전에는 Schedule·Expense CRUD를 잠시 보류한다. 조회 성공 결과가 없는 `undefined`와, 조회했지만 활성 기록이 없는 `null`은 다른 상태다.

- 첫 조회 진행 중: `allowed: false, pending: true`와 확인 중 이유를 반환한다. `PolicyErrorDisplay`는 중립적인 진행 표시를 사용한다.
- 첫 조회 실패: 확인 실패 이유로 제한한다. 아직 확인하지 못한 여행을 비활성으로 단정하지 않는다.
- 성공 결과가 있음: 재조회 중이거나 재조회에 실패해도 기존 결과로 Policy를 계산한다.
- 로컬 세션 없음: 활성 조회 상태보다 로그인 안내를 우선한다.

재인증 중이어도 활성 여부가 확인된 뒤 활성 여행의 작업을 허용한다. 네트워크 unknown과 활성 조회 미확정은 서로 다른 입력이며 같은 오류 이유로 합치지 않는다.

## 필요한 작업 구조와 실제 소비를 함께 유지한다

`OperationPolicy`는 한 작업의 `allowed`, 선택적 `pending/mode/reason`을 나타낸다. `EntityPolicy`는 선택된 Schedule·Expense의 `create/read/update/delete`를, `EntityPolicyTable`은 상태별 원본 표를 나타낸다. 지도·검색은 `ServicePolicy`와 `SERVICE_POLICIES`를 사용한다.

온라인에는 활성·비활성 모두 Schedule·Expense CRUD를 제공한다. 오프라인 활성 여행은 읽기·삭제를 계속하고 생성·수정은 `manual-only`로 외부 검색·새 연결 기능을 제한한다. 오프라인 비활성 여행은 내용을 제한한다. 서비스 표에서는 online에 Google 지도·API 검색, offline 활성에 Mapbox 지도와 검색 제한, offline 비활성에 지도·검색 제한을 표현한다. 지도 다운로드 유무 등 서비스의 실제 이용 조건은 해당 Service가 추가로 확인한다.

새 Entity나 Service 정책을 추가할 때에는 `types.ts`, `constants.ts`, `useAppPolicy.ts`, export와 실제 consumer를 함께 맞춘다. 실제로 사용하지 않는 `validation`, `fieldRules`, `syncStrategy`, `uiMode` 같은 선언을 구현된 보장처럼 쌓지 않는다. 반대로 핵심 Entity의 CRUD 구조는 지금 consumer가 적다는 이유만으로 지우지 않는다.

```tsx
const policy = useAppPolicy(tripId);

if (!policy.schedule.create.allowed) {
  return <PolicyErrorDisplay policy={policy.schedule.create} variant='block' />;
}

if (policy.schedule.create.mode === 'manual-only') {
  return <ManualScheduleForm tripId={tripId} />;
}

return <ScheduleForm tripId={tripId} />;
```

지도·검색 조합부는 `policy.service.mapProvider`와 `searchMode`를 사용한다. 제한 이유는 사용자에게 가능한 행동을 설명하고 내부 저장소·구현 이름을 노출하지 않는다.

## 제한 안내가 작성 중인 입력을 지우지 않게 한다

| 바꾸는 부분 | 보존할 기준 | 확인할 경계 |
| --- | --- | --- |
| 내용 제한 | Query 캐시를 지워 제한하지 않는다. 성공한 빈 목록·제한·조회 오류를 구별한다. | 화면 Policy의 내용/안내 분기 |
| 열린 Drawer | 내용이 제한돼도 mount와 form state를 유지한다. 저장 거절 뒤 다시 시도할 수 있어야 한다. | 버튼과 열린 폼 모두 현재 작업 Policy 사용 |
| 일정 수정 | 새 장소를 선택하지 않았다면 기존 장소·주소·좌표를 null/default로 덮지 않는다. | 화면 표시와 저장 payload |
| 경비 수정 | 새 연결을 제한해도 기존 `scheduleId`와 연결 표시를 유지한다. | 화면 표시와 저장 payload |
| 여행 선택 | 연결 변화로 여행·탭을 바꾸지 않는다. 제거 판단은 성공·종료한 실제 Remote 목록과 실제 online을 함께 확인한다. | 실제 조회 출처와 선택 consumer |
| 복구 안내 | 여전히 같은 비활성 여행일 때 재조회 성공에 연결한다. | 초기 unknown 해소와 장애 복구 구별 |

신규 입력의 기본값을 기존 데이터 수정에 그대로 사용하지 않는다. **날짜 변경 뒤 기존 일정 연결을 유지·해제·재선택하는 UX는 미정**이다. 전체 폼 계약은 [Form](../../../.claude/context/form.md)·[수동 입력](../../../.claude/context/manual-input.md)을 따른다.

## 변경 범위에 맞춰 확인한다

| 변경 대상 | 필요한 확인 |
| --- | --- |
| Network Store | 종료된 구독의 응답, listener 뒤 늦은 refresh, 미응답·연타, unknown 반복·명시적 재확인 |
| Policy | 네 조합 외에 인증 만료, 활성 조회의 undefined/null/기존 결과, 실제 상태와 override 불일치 |
| 폼·화면 | 제한 전환 뒤 Drawer 유지, 입력·좌표·일정 연결의 payload 보존, 버튼과 열린 폼 안내 일치 |

Policy hook 검사만으로 폼 동작을 입증하지 않는다. Component 검사와 native 화면·키보드·이동·실제 네트워크 경험도 구별한다.

직접 근거는 [Network Store](../../../apps/client/src/shared/store/network.ts), [Policy](../../../apps/client/src/shared/policy/useAppPolicy.ts), [정책 표](../../../apps/client/src/shared/policy/constants.ts), [화면 검사](../../../apps/client/tests/screens/auth-policy.test.tsx)다. 2026-09-25 코드와 기존 Owner·[합의/구성 근거](../../work/workspaces/002-code-readability-refactoring/records/2026-09-23-01-project-context-composition-proposal.md)를 대조했다.

**브랜치 차이:** 이 브랜치 제품 코드는 `759cba3`이다. 활성 여부 최초 확인(1-A)은 별도 제품 워크트리의 당시 변경이며 [분리 시점 기록](../../work/workspaces/002-code-readability-refactoring/records/2026-09-28-01-project-context-branch-separation.md#제품-작업-1-a의-분리-시점-기록)에 보존했다. 후속 브랜치의 현재 진척·실기기 동작 전체는 여기서 확인하지 않았다. 복구 안내 등 합의와 실제 지원의 차이는 [화면 현황](../current/network-and-screen-access.md)에서 확인한다.
