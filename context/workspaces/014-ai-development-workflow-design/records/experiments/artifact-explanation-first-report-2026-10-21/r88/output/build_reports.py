from pathlib import Path
from html import escape
import json
O=Path(__file__).resolve().parent
R=O.parent/'repository'
T='context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/'
S='apps/client/src/'
Q='apps/client/tests/'
used=[]
def evidence(path,a,b,why):
 lines=(R/path).read_text().splitlines(); used.append({'path':path,'start':a,'end':min(b,len(lines))})
 text='\n'.join(f'{i+1:4} {lines[i]}' for i in range(a-1,min(b,len(lines))))
 return f'<details><summary>{escape(why)}</summary><p class="path">{escape(path)}:{a}</p><pre>{escape(text)}</pre></details>'
def table(head,rows):
 return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def sec(title,body):return f'<section><h2>{title}</h2>{body}</section>'
def p(t):return '<p>'+t+'</p>'
items=[('02-foreground.html','② 앱 복귀 시 네트워크 재확인'),('03-ux.html','③ 목록·상세·폼 종합 UX'),('04-dates.html','④ 홈·목록 날짜 차이'),('05-scope.html','⑤ 보류·후속 티켓 경계')]
style='''*{box-sizing:border-box}body{margin:0;background:#f3f5f8;color:#172238;font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1080px;margin:auto;padding:32px 24px 70px}nav{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:36px}nav a,.button{background:white;padding:7px 13px;border-radius:9px;text-decoration:none;border:1px solid #d5dce6;color:#184c78}h1{font-size:34px;line-height:1.3;margin:12px 0 20px}h2{font-size:23px;margin:0 0 16px}h3{font-size:18px}p{margin:10px 0 18px}.eyebrow{font-size:13px;letter-spacing:.06em;color:#657188}.lead{font-size:20px;font-weight:600}section{background:white;border:1px solid #e0e5ec;border-radius:16px;padding:25px;margin:20px 0}.limit{background:#fff4dc;border-left:4px solid #cd8a13;padding:15px 20px;border-radius:8px}.status{color:#386a53;font-weight:600}.scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{vertical-align:top;text-align:left;border-bottom:1px solid #e3e8ee;padding:13px 12px}th{background:#f0f4f8;white-space:nowrap}details{margin:14px 0;border:1px solid #dce3eb;border-radius:9px;padding:10px 14px}summary{cursor:pointer;font-weight:600}.path{font-size:12px;overflow-wrap:anywhere;color:#657188}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#172238;color:#e5edf6;padding:18px;border-radius:9px;font-size:12px;line-height:1.7}footer{font-size:13px;color:#657188}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}.card{background:white;border:1px solid #dce3eb;border-radius:12px;padding:22px;color:inherit;text-decoration:none}.card strong{display:block;color:#184c78}.badge{display:inline-block;background:#e6eef8;padding:2px 9px;border-radius:4px;font-size:12px}@media(max-width:600px){main{padding:18px 12px}h1{font-size:27px}section{padding:18px}td,th{min-width:120px}}@media print{nav{display:none}body{background:white}section{break-inside:avoid}details{display:block}}'''
common='<aside class="limit"><strong>화면 증거 미확보</strong><br>시뮬레이터·DB·기존 HTML과 캡처가 제공되지 않았습니다. 새 스크린샷은 없으며, 이 보고서는 제공된 코드·검사 본문·티켓과 제한된 날짜 실행을 근거로 작성했습니다. 과거 대화의 실행 보고는 이번 직접 관찰과 구별합니다.</aside>'
def save(file,title,lead,body):
 nav='<nav><a href="index.html">보고서 모음</a>'+''.join(f'<a href="{f}">{t}</a>' for f,t in items)+'</nav>'
 doc=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · Ticket 06</title><style>{style}</style></head><body><main>{nav}<div class="eyebrow">TICKET 06 · 제공된 0b3b167 스냅샷 기준</div><h1>{title}</h1><p class="lead">{lead}</p>{common}{body}<footer>코드·티켓은 읽기 전용으로 조사했습니다. Jest·실앱·서버 DB 검증은 이번에 실행하지 않았습니다. 작성일 2026-10-21. 코드 근거는 접힌 영역에서 원문과 줄 번호로 확인할 수 있습니다.</footer></main></body></html>'
 (O/file).write_text(doc)
body=sec('현재 답',p('기존 네트워크 재확인 기능은 있지만, 앱이 백그라운드에서 돌아올 때 호출하는 연결은 없습니다. 따라서 Store의 중복·지연 응답 방어가 있어도 앱 복귀 시의 오래된 관측을 적극 갱신하는 경로는 완성되지 않았습니다.')+p('앱 소스와 테스트에서 AppState 사용을 검색했으며 찾지 못했습니다. NetInfo 자체 listener가 상태 변화를 전달할 수 있으므로 “복귀하면 반드시 stale하다”는 재현 결론까지 내릴 수는 없습니다.'))
body+=sec('어디까지 연결되어 있나',table(['경계','확인한 구현','보장 한계'],[
('앱 수명','AppInitialization이 mount 시 networkStore.init(), 해제 시 cleanup()','background → active 사건의 구독과 refresh 호출 없음'),
('재확인','Network Store의 refresh()가 NetInfo.refresh() 호출','완료 자체를 online으로 간주하지 않음'),
('동시 호출','activeRefresh.promise 공유','foreground 호출과의 결합 검사는 새로 필요'),
('늦은 응답','세션·작업 identity와 observationRevision 대조','구현·mock 검사 본문 확인, native 실행 미확인'),
('화면과 sync','조회 조합은 정책을 소비하고 SyncProvider는 realStatus 변화로 eligibility 계산','복귀 사건부터 실제 화면·sync까지의 실행 관찰 없음')]))
body+=sec('구현할 결과와 확인 순서',p('앱 수명을 맡는 application 경계에서 background/inactive에서 active로 돌아오는 전환을 감지해 기존 refresh()를 호출하는 것이 적절합니다. 초기 mount와 반복 active 알림을 전환으로 오인하지 않고, 해제 시 listener를 정리해야 합니다. 이전 상태가 online·offline·unknown 어느 것이든 같은 재확인 경로를 사용합니다.')+p('새 polling·강제 unknown 전환은 필요하지 않습니다. 수동 재확인과 겹침, 빠른 왕복, 해제 후 응답, refresh 뒤 더 최신 listener 도착을 결합 검사하고, 실제 한 번의 앱 왕복에서 관측·화면 제한·sync 시작을 함께 확인하면 됩니다.'))
body+=sec('증거',evidence(S+'application/AppInitialization.tsx',62,78,'앱 수명은 시작·정리만 연결')+evidence(S+'shared/store/network.ts',128,158,'동시 재확인 공유와 unknown 안내 재시작')+evidence(S+'shared/store/network.ts',301,318,'최신 listener 관측을 지키는 조건')+evidence(Q+'shared/store/network.test.ts',222,248,'동시 refresh 검사 본문 — 이번 실행 없음')+evidence(Q+'shared/store/network.test.ts',297,319,'오래된 결과 검사 본문 — 이번 실행 없음')+evidence(S+'shared/services/sync/provider.tsx',35,65,'실제 연결 변화의 sync 소비'))
body+=sec('수집해야 할 화면과 기록',p('동일한 여행을 유지한 채 online으로 나가기 → 연결을 바꾸고 돌아오기 → 제한 안내 → 다시 online 복귀를 수집합니다. 스크린샷만으로 refresh 횟수나 sync 중복은 판별하기 어려우므로 AppState·재확인 호출 횟수·최신 realStatus 기록도 필요합니다. 이 자료는 이번에는 수집하지 못했습니다.'))
save(items[0][0],items[0][1],'앱 복귀 사건과 재확인 기능을 잇는 작업이 남아 있습니다.',body)
body=sec('현재 답',p('조회는 제한·최초 실패·빈 결과·갱신 실패를 구분하고, 폼은 연결 전환에 초안을 유지하도록 구현돼 있습니다. 관련 검사 본문도 그 차이를 다룹니다. 다만 native 화면·picker·키보드와 실제 통신 단절 저장을 확인하지 못해 종합 UX를 통과로 판단할 수 없습니다.'))
body+=sec('장면별 확인 범위',table(['장면','소스·검사에서 확인한 내용','남은 직접 확인'],[
('비활성 목록·상세 제한','표시 정책이 ready 캐시보다 먼저 적용돼 내용을 가림. 데이터 별도 삭제 없음','동일 여행·탭·선택 유지와 안내 가시성'),
('online 복귀','유효한 캐시는 먼저 표시. stale/invalidated는 Query 기준 갱신','화면 깜빡임·중복 안내·실패 안내 배치'),
('최초 조회 실패','빈 일정/경비·0원·대상 부재와 오류를 구분하는 검사 존재','실제 실패 상태와 재시도 성공 화면'),
('기존 내용 갱신 실패','기존 내용 유지와 작은 오류·재시도 검사 존재','스크롤·버튼 조작과 안내 중복'),
('일정 작성 중 전환','화면 단계와 draft를 폼 위에서 유지. 단일 폼·명시적 재시도 검사 존재','취소 React 경고, native picker·키보드, 저장·재진입'),
('경비 작성 중 전환','날짜와 일정 연결 독립, 제한 후 초안 유지·명시적 저장 검사 존재','기존 일정 연결이 있는 비활성 초안의 제한·해제'),
('활성 Local 저장','검사는 Router Local 호출과 초안 보존을 확인','실제 단절 중 SQLite·큐 반영과 재시작 후 보존')]))
body+=sec('과거 문제와 현재 구현의 관계',p('일정 수동 작성 중 online 복귀 시 폼 소실, 장소 선택 후 두 폼 표시의 과거 지적은 현재 단계 상태와 단일 분기로 수정된 근거가 있습니다. 이를 새 구현 대상으로 되돌릴 필요는 없습니다. 취소 경고의 native 재현은 별도 남습니다.')+p('과거 대화와 Ticket에는 경비 실앱·서버 반영 확인이 기록되어 있지만 이번에는 그 캡처·DB를 볼 수 없습니다. 기록된 523 passed / 1 skipped는 과거 검증 수치이며 이번 실행 결과가 아닙니다.'))
body+=sec('검사와 실제 경험 사이',p('조회 검사에서는 repository·NetInfo·native 요소를 대체합니다. 일정/경비 생성 검사도 실제 통신·SQLite·picker를 모두 입증하지 않습니다. 글자 잘림·버튼 가시성·실제 통신 끊김을 이 검사 통과만으로 보장할 수 없습니다.')+evidence(S+'shared/services/policy-query/usePolicyReadQuery.ts',19,39,'제한·캐시·오류의 표시 순서')+evidence(Q+'screens/read-query-consumers.test.tsx',238,272,'상세 제한·부재·개별 실패 검사')+evidence(Q+'screens/schedule-recovery.test.tsx',325,365,'복구·갱신 실패·재시도 검사')+evidence(Q+'screens/expense-recovery.test.tsx',180,230,'경비 목록·상세 최초/갱신 오류 검사')+evidence(S+'screens/CreateScheduleScreen.tsx',24,40,'화면 단계와 초안의 수명')+evidence(Q+'screens/create-schedule-flow.test.tsx',129,144,'연결 복귀 뒤 단일 폼 검사')+evidence(Q+'screens/create-expense-flow.test.tsx',169,186,'비활성 초안과 명시적 저장 검사'))
body+=sec('다음 수집을 짧게 묶는 방법',p('한 시뮬레이터에서 먼저 비활성 여행의 목록·상세를 같은 데이터로 순회하며 정상 → 제한 → 복구만 수집합니다. 이어 같은 초안을 유지한 일정·경비 폼을 확인하고, 실제 단절 Local 저장은 Debug override를 해제한 별도 묶음으로 수집합니다. Debug override는 쓰기를 막으므로 실제 offline 저장의 대체 증거가 되지 않습니다. 캡처마다 여행 ID·활성 여부·실제/강제 상태·입력·행동·결과를 함께 기록해야 합니다.'))
save(items[1][0],items[1][1],'구현과 검사 근거는 쌓였지만, 실제 사용자 흐름의 최종 확인이 남아 있습니다.',body)
data=json.loads((O/'date-check.json').read_text())
body=sec('현재 답',p('홈은 Date의 현지 월·일을 표시하고, 일정·경비 목록은 Trip timestamp의 UTC 날짜 범위를 만듭니다. 같은 값을 입력해도 날짜가 달라질 수 있습니다. 공통 UTC helper 적용은 두 목록 간 계산을 맞췄지만 홈까지 일치시키지는 않습니다.'))
body+=sec('이번에 직접 실행한 계산',p('저장소의 datetime.ts를 Node로 직접 import해 3개 시간대에서 실행했습니다. 아래 값은 <strong>설명용 fixture</strong>이며 당시 여행 DB 값이 아닙니다. 홈의 getMonth()/getDate()와 같은 현지 날짜 해석을 formatISOToLocalDate()로 확인하고, 목록은 실제 getUTCDateRange()를 호출했습니다.')+p('<code>start = 2026-09-29T15:00:00Z</code><br><code>end = 2026-10-01T15:00:00Z</code>')+table(['시간대','홈과 같은 현지 날짜 해석','목록 UTC 범위'],[(r['zone'],' ~ '.join(r['home']),' ~ '.join([r['range'][0],r['range'][-1]])) for r in data['results']])+p('예상값 대조 6개 assertion이 통과했습니다. 과거 보고서와 같은 날짜 차이를 만들 수 있음을 확인한 것이며, 과거 원인 확정이나 시뮬레이터 재현은 아닙니다. 실행 원문은 <a href="date-check.json">date-check.json</a>에 있습니다.'))
body+=sec('사용자에게 미치는 영향',p('일정 화면은 UTC로 만든 날짜들에 현지 날짜로 변환한 일정들을 끼워 넣습니다. 따라서 홈에서 보이는 마지막 날이 목록 범위 밖이면 그 날의 일정이 이 그룹 경로에 포함되지 않을 수 있습니다. 예제의 서울 시간대에서 10월 2일 일정은 위 목록 범위에 없으며, 이 포함 여부도 계산 결과에 기록했습니다. 이는 화면을 직접 조작한 결과가 아니라 소스와 helper 실행으로 도출한 영향입니다.'))
body+=sec('왜 바로 표시만 바꾸지 않나',p('현재 Project 기준은 Trip 시작·종료를 ISO datetime으로 다루되 장기적으로 달력 날짜인지 한 시점인지는 새로 결정하지 않았다고 명시합니다. 홈에 맞춰 목록만 바꾸거나 반대로 홈만 UTC로 바꾸면 편집·대표 여행 선택·활성 만료와 의미가 어긋날 수 있습니다.')+p('06에서는 차이와 영향을 남기고 날짜 담당 08 및 003-08과 연결해야 합니다. 다음에는 실제 startDate/endDate·기기 시간대·같은 여행 ID의 홈/목록 캡처를 함께 대조한 뒤 표시 기준과 기간 밖 항목 접근을 정리해야 합니다.'))
body+=sec('증거',evidence(S+'screens/HomeScreen/MainTripSection.tsx',32,39,'홈의 현지 날짜 표시')+evidence(S+'shared/lib/datetime.ts',77,101,'UTC 날짜 범위 helper')+evidence(S+'screens/ScheduleScreen.tsx',98,105,'목록 날짜 범위')+evidence(S+'screens/ScheduleScreen.tsx',178,191,'일정의 현지 날짜별 그룹')+evidence('context/project/common/date-and-time.md',43,55,'현재 날짜 의미와 Trip의 열린 판단')+evidence(T+'08-date-selection-grouping.md',9,15,'날짜 구조와 결함 담당 경계'))
save(items[2][0],items[2][1],'홈과 목록의 날짜 차이를 만드는 계산은 남아 있으며, 예제 실행에서도 확인됐습니다.',body)
body=sec('현재 답',p('06은 앱 준비·인증·네트워크 정책의 실제 화면 연결을 마무리하는 범위입니다. 이미 구현한 선행 조각은 후속 티켓에서 재사용하되, 사용자 보류와 다른 담당의 나머지 책임을 모두 06의 필수 구현으로 되살리면 안 됩니다. 범위가 나뉘었다는 이유로 해결된 것으로 기록해서도 안 됩니다.'))
body+=sec('보류와 현재 추가하지 않을 것',table(['항목','현재 근거와 의미','다음 행동'],[
('경비 삭제 실패 이유 유실','ExpensesScreen onError가 원인을 받지 않고 일반 실패 Alert 표시. 사용자가 보류','해결 표시 금지. 이번 필수 선행으로 올리지 않음'),
('경비 상세 특정 재시도','대상 없음+이전 오류+display online/real offline이면 retry UI가 보여도 canFetch가 요청을 막는 경계','보류 유지. 일반적인 online 재시도 전체가 고장났다고 확대 금지'),
('복구 토스트','현재 추가하지 않기로 한 선택. 구현 완료와 다름','헤더·내용 복귀로 인지가 부족한 실제 장면이 있을 때 재검토')]))
body+=sec('후속 티켓과 재사용할 결과',table(['담당','06 등에서 재사용할 것','남아 있는 책임'],[
('07 / 17 · API 계약','입력·응답 검증/직렬화의 선행 개선','Trip client PATCH와 server PUT 불일치, route 계약 대조'),
('08 / 003-08 · 날짜','공통 UTC 일자 범위와 일정·경비 시간 개선','홈/목록 의미, 대표 여행 계산, 기간 밖 항목 접근'),
('10 · 일정 폼','단일 생성 흐름·초안/검색 분리','수정 전체 수명과 재진입·legacy 검색 실패 등 나머지'),
('11 / 003-06 · 경비 폼','날짜와 일정 연결 독립·초안·저장 오류 처리','늦게 도착한 기본 통화와 사용자 입력 보존, 전체 재진입 조합'),
('13 / 003-09 · 경로 준비','저장 자체와 검색 장소 채택의 개선','500ms 대기·오래된 목록/좌표, 경로 입력에서 정상 0 좌표 유실'),
('14 · Local transaction','종료 전 저장 대기·원자성의 선행 검증 기록','전체 독립 write·payload 타입·cache 계약·실제 SQLite 확인'),
('15 · Sync','중복 시작 차단, 실패 전달·HTTP retry·pull parse의 선행 개선 기록','cleanup 부분 실패 결과, IN_PROGRESS 재개, pull 원자성·충돌·cursor'),
('16 · 정리','계정 종료·vacuum의 원본 보존 개선 기록','여행별 PENDING 중심 조회를 FAILED/IN_PROGRESS까지 연결, 실제 처리 집계')]))
body+=sec('과거 지적을 현재 미해결로 복사하면 안 되는 이유',p('15번 초기 분석에는 push 실패의 정상 반환, 재시도와 pull 무검증이 적혀 있지만 같은 티켓의 현재 결과에는 실패 전달·HTTP retry·pull parse 개선이 기록되어 있습니다. 이 보고서는 그 초기 분석을 그대로 미해결 목록으로 쓰지 않았습니다. 다만 이번에는 sync 전체를 실행 검증하지 않았으므로 티켓 기록의 보장 범위로 한정합니다.'))
body+=sec('실제 코드와 기록',evidence(S+'screens/ExpensesScreen.tsx',133,146,'경비 삭제의 일반 오류 안내')+evidence(S+'screens/ExpenseDetailScreen.tsx',13,23,'상세 재시도 실행 조건')+evidence(S+'screens/ExpenseDetailScreen.tsx',63,76,'대상 없음·오류 상태의 재시도 UI')+evidence(S+'features/expense/create-expense/useCreateExpenseForm.ts',25,49,'기본 통화의 최초 defaultValues 적용')+evidence(S+'features/schedule/create-schedule/useSubmitSchedule.ts',29,64,'저장 뒤 500ms와 route 좌표의 truthy 변환')+evidence(S+'entities/trip/api/trips.ts',57,63,'Trip 수정 요청 PATCH')+evidence('apps/server/src/routes/trips.ts',158,163,'server 수정 route PUT')+evidence(T+'15-sync-result-retry-pull-types.md',26,39,'Sync의 개선 기록과 나머지 범위')+evidence(T+'16-unsynced-data-cleanup.md',25,34,'정리의 개선 기록과 PENDING 중심의 나머지 범위'))
body+=sec('06 종료 판단에 필요한 것',p('홈 공통 안내, foreground 연결, 종합 사용자 흐름 검증의 결과를 확인하고 날짜 차이의 처리 담당과 영향을 연결해야 합니다. 보류·다른 담당·미확인을 구분한 상태에서 실제 완료 조건과 대조해야 하며, 네 보고서 생성이나 과거 테스트 수치만으로 06을 닫을 수는 없습니다.'))
save(items[3][0],items[3][1],'보류는 유지하고, 후속 티켓의 선행 개선과 나머지 책임을 구분했습니다.',body)
body=sec('이번 검토의 결론',p('02는 앱 복귀 연결이 빠진 구현 과제, 03은 기존 구현의 실제 사용자 흐름 확인, 04는 서로 다른 날짜 해석의 현재 영향과 제품 판단, 05는 보류와 후속 책임의 경계입니다. 서로 같은 종류의 미완성이 아니므로 일괄 통과 또는 일괄 재구현으로 처리할 수 없습니다.'))
leads=['앱 복귀와 refresh 연결이 빠져 있음','구현·검사 근거와 native 미확인 구분','3개 시간대 helper 실행에서 차이 확인','이미 된 선행 개선과 나머지 책임 대조']
body+='<div class="cards">'+''.join(f'<a class="card" href="{f}"><strong>{t}</strong>{l}</a>' for (f,t),l in zip(items,leads))+'</div>'
body+=sec('다음 실행',p('우선 홈 안내 정리와 foreground 연결을 진행하고, 한 시뮬레이터에서 동일 여행의 목록·상세·폼 전환을 수집하는 순서가 적절합니다. 날짜 비교에는 원본 DB 값과 기기 시간대를 함께 확보해야 합니다. 이번 환경에서는 추가 worker 없이 직접 조사했고 제품 변경은 하지 않았습니다.'))
save('index.html','Ticket 06 · 후속 검토 보고서 4편','요청한 ②~⑤를 각각 확인하고 현재 답과 다음 작업을 묶었습니다.',body)
(O/'report-source-manifest.json').write_text(json.dumps(used,ensure_ascii=False,indent=2))
print('Created index.html and four reports; source excerpts:',len(used))
