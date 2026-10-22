from pathlib import Path
import html,json
R=Path(__file__).resolve().parent.parent/'repository'
O=Path(__file__).resolve().parent
S='apps/client/src/'
T='apps/client/tests/'
W='context/work/workspaces/002-code-readability-refactoring/'
K=W+'current/memory/tickets/'
css='''*{box-sizing:border-box}body{margin:0;background:#f4f6f8;color:#192a35;font:16px/1.75 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif}main{max-width:1080px;margin:auto;padding:40px 24px 80px}nav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 25px}nav a{padding:6px 12px;background:#fff;border:1px solid #d7dfe5;border-radius:8px}a{color:#175fa2;text-underline-offset:3px}h1{font-size:34px;line-height:1.35;letter-spacing:-1px}h2{font-size:23px;margin-top:0}h3{font-size:18px}section,.hero{background:white;border:1px solid #dce4ea;border-radius:15px;padding:26px;margin:20px 0}.hero{border-top:5px solid #166863}.lead{font-size:20px;font-weight:650}.meta{color:#526572;font-size:14px}.badge{display:inline-block;background:#e2eeeb;color:#1d5b4b;padding:3px 10px;border-radius:6px;font-size:13px;font-weight:650}.warn{background:#fff5df;border-left:4px solid #b28123;padding:17px 20px;margin:18px 0}.table{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:15px}th,td{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #e1e6eb}th{background:#edf3f6}code{background:#f1f4f7;padding:2px 5px;border-radius:3px;font-size:13px;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f5f7;padding:15px;font-size:12px;line-height:1.65}summary{cursor:pointer;color:#175fa2;overflow-wrap:anywhere}details{margin:15px 0;border-top:1px solid #e4e9ed;padding-top:12px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}.card{padding:20px;background:#fff;border:1px solid #dce4ea;border-radius:12px}.flow{display:flex;gap:12px;flex-wrap:wrap}.flow div{flex:1;min-width:170px;background:#edf4f3;padding:16px;border-radius:8px}footer{color:#526572;font-size:14px}@media(max-width:600px){main{padding:24px 14px}h1{font-size:27px}section,.hero{padding:19px}th,td{padding:9px}}@media print{body{background:white}nav{display:none}main{max-width:none;padding:0}section{break-inside:avoid}details{display:block}}'''
nav='<nav aria-label="보고서 이동"><a href="index.html">전체 보기</a><a href="02-foreground.html">② 앱 복귀</a><a href="03-ux.html">③ 종합 UX</a><a href="04-dates.html">④ 날짜 차이</a><a href="05-scope.html">⑤ 보류·후속</a></nav>'
def table(head,rows):
 return '<div class="table"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def sec(title,body):return '<section><h2>'+title+'</h2>'+body+'</section>'
def p(x):return '<p>'+x+'</p>'
def evidence(id,path,start,end):
 lines=(R/path).read_text().splitlines()
 assert 1<=start<=end<=len(lines),(path,start,end,len(lines))
 text='\n'.join(f'{i:4d}  {lines[i-1]}' for i in range(start,end+1))
 return f'<details id="{id}"><summary>{html.escape(path)} · {start}–{end}행</summary><pre>{html.escape(text)}</pre></details>'
def ref(id,label):return f'<a href="#{id}">{label}</a>'
def report(file,n,title,lead,body,ev):
 common='<p class="meta">코드 기준: 제공된 HEAD 0b3b167 스냅샷 · 검토 작성: 2026-10-21 · 이어받은 대화 시점: 2026-10-04</p>'
 intro='<div class="hero"><span class="badge">Ticket 06 · '+n+'</span><h1>'+title+'</h1><p class="lead">'+lead+'</p>'+common+'</div>'
 scope='<div class="warn"><strong>근거 범위</strong> — 이번에 코드·테스트 본문을 직접 대조했습니다. 앱·시뮬레이터·DB·전체 Jest는 실행하지 않았습니다. 대화와 저장 기록의 과거 통과·관찰은 새 실행 결과와 구별합니다. Git 메타데이터가 없어 branch·working tree는 재확인하지 못했습니다.</div>'
 page='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+' | Ticket 06</title><style>'+css+'</style></head><body><main>'+nav+intro+scope+body+sec('직접 확인한 원자료 발췌',ev)+'<footer>제품 코드와 Ticket 상태는 변경하지 않았습니다. 이 보고서는 Ticket 완료·사용자 수락을 선언하지 않습니다.</footer></main></body></html>'
 (O/file).write_text(page)
# 02
body=sec('앱으로 돌아왔을 때 지금 연결을 다시 확인하는가',p('앱 시작 시 네트워크 감지는 구독하지만, background 또는 inactive에서 active로 돌아온 사건을 받아 재확인하는 코드 연결은 없습니다. '+ref('startup','AppInitialization')+'은 mount에서 init, unmount에서 cleanup을 호출합니다. client src·app을 검색한 범위에서 AppState 사용은 발견되지 않았습니다. NetInfo 자체가 플랫폼에서 이벤트를 주는 가능성과 앱이 복귀 때 한 번 확인하는 보장은 구별해야 합니다.'))
body+=sec('있는 기능과 빠진 연결',table(['단계','직접 확인','의미'],[
['관측 수명','init() 중복 방지·listener·cleanup 구현','네트워크가 늦어도 DB→인증→화면 준비를 진행합니다.'],
['현재 연결 재확인','refresh()가 NetInfo.refresh() 실행','기존 online/offline을 먼저 unknown으로 바꾸지 않습니다.'],
['겹치는 요청','진행 중 Promise 공유','수동 재확인과 복귀 확인이 겹쳐도 Store의 한 작업을 사용할 수 있습니다.'],
['늦은 결과','session·activeRefresh·observationRevision 비교','이전 구독/작업 결과가 최신 listener 관측을 덮는 것을 막습니다.'],
['앱 복귀 사건','AppState 연결 없음','Store 기능이 있어도 복귀 사건에서 호출되지 않습니다.']
])+p('구현 근거: '+ref('refresh','refresh 진입')+' · '+ref('operation','늦은 결과 방어')+' · '+ref('provider','SyncProvider 실제 소비')))
body+=sec('화면과 sync에 이어지는 영향',p('관측이 바뀌면 조회 정책과 SyncProvider가 실제 상태를 소비합니다. 비활성 여행은 실제 online을 확인해야 Remote 요청이 열립니다. sync는 인증·DB·override·진행 중 실행 조건도 맞아야 시작합니다. 앱 복귀 때 상태가 계속 online이면 복귀 자체가 새 sync 이유가 되지는 않습니다. 이번 연결을 “돌아올 때마다 강제 sync·전체 refetch”로 확대하면 기존 책임이 달라집니다.')+'<div class="flow" aria-label="현재 코드와 제안 연결"><div><strong>빠진 연결</strong><br>background/inactive에서 active</div><div><strong>재사용 대상</strong><br>networkStore.refresh()</div><div><strong>현재 소비</strong><br>실제 관측에 따른 조회 정책·sync eligibility</div></div>'+p('위 구조에서 첫 연결은 제안이고, 나머지는 코드로 확인한 흐름입니다. 실제 복귀 trace는 아닙니다.'))
body+=sec('작게 마무리할 수정과 검사',p('앱 전체 관측 수명을 가진 AppInitialization 근처에서 이전 AppState를 추적하고, 비활성 상태에서 active로 전환할 때 기존 refresh()를 호출하는 것이 적절합니다. initial active와 active 반복은 복귀로 세지 않고 listener는 unmount에서 정리합니다. 별도 polling·강제 unknown·unknown에서만 재확인은 추가하지 않는 기존 결정을 유지합니다.')+table(['확인 장면','기대 결과','현재 근거'],[
['background→active / inactive→active','각 복귀에서 재확인 호출','새 수명 연결의 회귀 검사 필요'],
['이전 online / offline / unknown','모든 이전 상태에서 확인 가능','Store refresh는 상태별 분기 지원'],
['빠른 복귀와 수동 재확인 겹침','진행 중 한 Promise 공유','기존 Store 테스트 본문 존재·이번 미실행'],
['새 listener 관측 후 오래된 응답','새 관측 유지','기존 Store 테스트 본문 존재·이번 미실행'],
['unmount·재mount·확인 timeout','이전 작업 무시·구독 정리','Store 검사와 앱 수명 통합 검사를 구별'],
['복귀 후 제한 해제와 sync','선택·탭 유지, 실행 가능 변화에서 중복 시작 없음','native UI·요청 trace 수집 필요']
]))
body+=sec('스크린샷·실행 증거',p('이번 제공 자료에 스크린샷은 없습니다. 복귀 확인은 정지 화면 한 장으로 요청 실행 여부까지 판단할 수 없으므로 상태 전환 로그와 함께 수집해야 합니다.')+p('다음 수집 묶음: 비활성 여행·override 해제 상태의 복귀 직전 → 외부에서 연결 변경 → 복귀 직후 → 관측 완료. 동일 tripId, 이전/다음 AppState, realStatus, refresh 시작·종료, 실제 요청 횟수를 함께 보존합니다. 활성 여행을 대조군으로 한 번 확인합니다. 이 자료를 얻기 전에는 복귀 동작 통과로 표시하지 않습니다.'))
ev=evidence('startup',S+'application/AppInitialization.tsx',61,84)+evidence('refresh',S+'shared/store/network.ts',130,169)+evidence('operation',S+'shared/store/network.ts',300,388)+evidence('provider',S+'shared/services/sync/provider.tsx',44,59)+evidence('networktests',T+'shared/store/network.test.ts',222,248)
report('02-foreground.html','02','foreground 네트워크 재확인','재확인 기능은 준비돼 있습니다. 앱 복귀 사건을 연결하고 화면·sync까지 확인하는 일이 남았습니다.',body,ev)
# 03
body=sec('개선된 작성 흐름을 다시 만들 필요는 없습니다',p('일정 생성은 연결 상태가 아니라 사용자 행동으로 search/form/change-place 단계를 바꿉니다. 초안 훅은 분기 UI보다 위에서 유지되고 ScheduleForm은 한 분기에서만 장착됩니다. '+ref('create','현재 생성 화면')+'과 '+ref('flowtests','회귀 테스트 본문')+'이 과거 폼 숨김·동시 표시 문제에 대응합니다. 다만 native picker·취소 경고 소멸은 이번 정적 확인만으로 확정할 수 없습니다.'))
body+=sec('목록·상세·폼을 연결해서 확인한 결과',table(['장면','코드·테스트가 다루는 결과','이번 판정'],[
['비활성 여행 단절','display policy 차단을 data보다 우선해 캐시 숨김; 캐시 별도 삭제 없음','구현 확인. 실제 화면 전환 미확인'],
['접근 복구','성공 또는 갱신 실패 데이터는 ready로 반환','기존 내용 우선 표시 구조 확인'],
['처음 조회 실패','error와 빈 성공 결과 분리','일정 상세/홈의 관련 테스트 본문 확인'],
['기존 내용 갱신 실패','내용 유지 + refreshFailed 안내','일정 복구 테스트 본문 확인'],
['한쪽 데이터만 실패','일정과 경비의 별도 조회·안내','경비 실패를 0원으로 표시하지 않는 검사 존재'],
['작성 중 제한·실패','폼 편집·기존 일정 연결 보존, 저장 순간 Router 차단','일정·경비 생성 검사 본문 확인'],
['복구 후 저장','사용자 명시적 재시도 후 성공 처리','관련 mock 검사 존재. 실제 통신 단절 저장 미확인']
])+p('조회 근거: '+ref('query','공통 조회 표시·실행 조합')+' · '+ref('consumer','상세·홈 회귀 검사')+'. “검사 존재”는 이번 통과를 뜻하지 않습니다.'))
body+=sec('자동 검사에서 실제로 대체하는 것',p('create-schedule-flow는 DatePicker·TimePicker를 null로 대체하고 Local/Remote 저장을 mock으로 연결합니다. create-expense-flow도 picker 선택을 시험용 버튼으로 대체합니다. 따라서 초안과 정책 연결을 확인하는 검사와 실제 native 조작·SQLite·통신을 확인하는 검사는 범위가 다릅니다.')+p('저장된 current/state에는 client 48 suites / 523 passed / 1 skipped와 제한적인 경비 실앱 확인이 기록돼 있습니다. 이는 10월 2일의 과거 기록이며 이번에는 재실행하지 않았습니다. 전체 테스트 숫자가 아래 미확인을 해소하지는 않습니다.'))
body+=sec('화면 수집이 필요한 남은 묶음',table(['순서·준비','빠르게 수집할 것','판단 기준'],[
['1 · 비활성 여행 / 캐시 있는 목록·상세','online→offline→unknown 확인 중→확인 불가→online, 선택·탭·표시 문구','내용 제한, 선택 유지, 복구 뒤 기존 내용 우선'],
['2 · 최초 실패 / 갱신 실패 각각','빈 화면·실패 화면·재시도 중·성공 후; 일정/경비 한쪽 실패','없음·0원과 실패 구별, 정상인 영역 유지'],
['3 · 일정 생성','직접 작성→연결 복구; 장소 선택→단절; picker 취소·확인; 키보드 표시·저장','단일 폼·초안 유지, 취소 시 경고·값 변화 확인'],
['4 · 경비 생성·수정','기존 일정 연결을 가진 비활성 초안의 제한·해제; 날짜 변경·연결 해제','입력·연결 유지, 자동 저장 없음, 재시도 1회'],
['5 · 활성 여행 / 실제 통신 단절 / override 해제','Local 저장 직전·완료·목록 재진입·연결 복구 뒤 sync와 DB','Debug 차단과 구별, 행·큐·서버 반영을 각각 확인']
])+p('새 activation 전체와 지도 준비 완료는 이번 목록·폼 관찰만으로 완료하지 않습니다. 계정·tripId·활성 상태·override·realStatus를 각 묶음에 남겨야 결과를 해석할 수 있습니다.'))
body+=sec('스크린샷과 판단의 현재 한계',p('화면 원본이 제공되지 않아 이번 보고서에 새 캡처는 없습니다. 대화에 기록된 10월 4일 활성 홈의 2개·EUR 56.00 유지는 홈 관찰의 과거 보고이며 나머지 목록·상세·폼 확인으로 확대하지 않습니다. 각 묶음의 스크린샷과 짧은 조작 순서가 확보되면 동일 보고서의 근거로 연결할 수 있습니다.')+p('추천은 홈 안내·foreground 연결의 작은 수정 후 위 묶음을 한 시뮬레이터에서 이어 확인하는 것입니다. 수집자는 화면·문구·입력값·요청 결과만 반환하고, 원인·수정 범위는 그 근거를 모아 판단하면 됩니다.'))
ev=evidence('create',S+'screens/CreateScheduleScreen.tsx',24,45)+evidence('createform',S+'screens/CreateScheduleScreen.tsx',77,111)+evidence('query',S+'shared/services/policy-query/usePolicyReadQuery.ts',14,36)+evidence('consumer',T+'screens/read-query-consumers.test.tsx',238,284)+evidence('flowtests',T+'screens/create-schedule-flow.test.tsx',20,36)+evidence('expensetests',T+'screens/create-expense-flow.test.tsx',141,197)+evidence('connection',S+'features/expense/expense-form/ExpenseScheduleField.tsx',39,64)
report('03-ux.html','03','목록·상세·폼 종합 UX','초안 보존과 조회 복구는 구현됐지만, native 조작과 실제 단절 저장을 포함한 종합 확인은 남아 있습니다.',body,ev)
# 04
probe=json.loads((O/'date-probe.json').read_text())
rows=[]
for result in probe['results']:
 for case in result['cases'][:2]:rows.append([result['timezone'],case['name'],' ~ '.join(case['home']),' ~ '.join([case['list'][0],case['list'][-1]])])
body=sec('같은 여행을 서로 다른 날짜 기준으로 표시합니다',p('홈 MainTripSection은 new Date 뒤 getMonth/getDate로 기기 현지 날짜를 표시합니다. 일정 목록과 경비 목록은 getUTCDateRange로 Trip timestamp의 UTC 일자를 나열합니다. 일정은 다시 scheduledAt의 현지 날짜로 그룹에 들어갑니다. '+ref('home','홈 표시')+' · '+ref('range','UTC 범위 함수')+' · '+ref('schedule','일정 그룹')+'. 공통 날짜 범위 함수를 도입한 개선과 홈까지 같은 의미로 표시하는 일은 구별해야 합니다.'))
body+=sec('이번에 실행한 작은 확인',p('외부 의존성이 없는 날짜 범위 함수와 홈 포맷 본문을 제공 코드에서 추출해 Node에서 실행했습니다. UTC·서울·로스앤젤레스의 세 시간대에 같은 예시 입력을 넣었습니다. 아래는 실제 probe 결과이며 당시 DB 값이나 앱 캡처가 아닙니다.')+p('<code>offset-example</code>: 시작 2026-09-30T00:00:00+09:00 / 종료 2026-10-02T00:00:00+09:00<br><code>UTC-midnight</code>: 시작 2026-09-30T00:00:00Z / 종료 2026-10-02T00:00:00Z')+table(['실행 시간대','예시 입력','홈 시작·종료','목록 시작·종료'],rows)+p('<a href="date-probe.json">실행 결과 전체 JSON</a> · <a href="date-probe.cjs">추출·실행 방법</a>')+p('서울의 offset 예시는 “홈 9월 30일~10월 2일 / 목록 9월 29일 시작”이라는 과거 보고와 같은 형태의 차이를 만듭니다. 그러나 당시 실제 startDate·endDate와 기기 시간대가 없으므로 과거 원인을 이 예시로 확정하지 않습니다. 추가 DST 예시에서도 UTC 범위는 11월 1·2·3일을 한 번씩 나열했습니다. 이것이 native DST 전체 검증은 아닙니다.'))
body+=sec('숫자 표시만의 문제를 넘어갈 수 있는 이유',p('일정 화면은 Trip에서 만든 dateRange를 순회하며 각 날짜에 현지 날짜가 같은 일정만 배치합니다. 두 기준의 차이로 일정의 현지 날짜가 범위 밖이 되면 목록 그룹에서 보이지 않을 가능성이 있습니다. 이는 확인한 코드에서 도출한 조건부 영향이며 실제 사용자 일정 누락을 이번에 재현한 것은 아닙니다.')+p('Expense date는 이미 달력 날짜(YYYY-MM-DD) 계약이므로 시점처럼 기기 시간대 변환을 추가하면 안 됩니다. Schedule scheduledAt은 시점입니다. Trip 날짜의 장기 의미는 아직 열린 판단으로 명시돼 있습니다. '+ref('contract','제품 날짜 계약')+'.'))
body+=sec('06에서 확인할 것과 다음 담당',table(['이번 06에서 남길 결과','연결할 담당·자료'],[
['동일 tripId의 raw start/end와 홈·목록 표시 비교','실제 기기 시간대·DB/API 값·화면 캡처'],
['일정 현지 날짜가 범위 끝을 벗어나는지 확인','08 날짜 계산·그룹, 필요 시 003-08 기존 재현 근거'],
['작은 표시 수정인지 Trip 의미 변경인지 구별','Project 날짜 canonical, Trip form·선택·만료·DB/API 영향'],
['범위 helper 개선은 재사용','UTC 일자 순회와 memoized 소비를 미구현으로 되돌리지 않음']
])+p('추천은 당시 데이터의 원시 날짜를 먼저 고정하고, Trip 시작·종료를 어떤 달력 기준으로 보여야 하는지 정한 뒤 홈과 목록에 일관되게 적용하는 것입니다. 한쪽을 무조건 UTC 또는 local로 바꾸는 수정은 아직 하지 않았습니다.'))
body+=sec('필요한 스크린샷',p('같은 여행의 홈 전체와 일정·경비 첫날/마지막날, 원시 날짜와 기기 시간대 정보를 한 묶음으로 수집해야 합니다. 서울·로스앤젤레스에서 같은 데이터를 대조하고, 기간 밖 일정·경비의 접근도 따로 확인합니다. 원본 9월 30일 캡처는 이번 입력에 없어 첨부하지 못했습니다.'))
ev=evidence('home',S+'screens/HomeScreen/MainTripSection.tsx',32,38)+evidence('range',S+'shared/lib/datetime.ts',80,101)+evidence('schedule',S+'screens/ScheduleScreen.tsx',171,183)+evidence('expense',S+'screens/ExpensesScreen.tsx',56,64)+evidence('contract','context/project/common/date-and-time.md',45,51)+evidence('ticket8',K+'08-date-selection-grouping.md',5,19)
report('04-dates.html','04','홈·목록 날짜 차이','UTC 목록과 현지 날짜 표시의 차이가 남아 있습니다. 예시 함수 실행으로 차이를 확인했고, 실제 데이터의 재대조가 필요합니다.',body,ev)
#05
body=sec('보류는 해결도 다음 작업의 필수 선행도 아닙니다',p('사용자는 경비 삭제 실패 이유 유실과 경비 상세 특정 재시도 불일치를 이번에는 넘기고 완료 작업을 커밋·기록하기로 했습니다. 저장된 current/state와 Ticket 06에도 같은 경계가 있습니다. '+ref('state','현재 상태 기록')+'. 보고서에 남기되 홈 안내나 foreground 연결에 몰래 포함하지 않는 것이 현재 결정에 맞습니다.'))
body+=sec('명시적 보류 두 건',table(['항목','현재 코드 근거','영향과 한계'],[
['경비 삭제 실패 이유 유실','ExpensesScreen onError가 오류 인자 없이 “경비 삭제에 실패했습니다.” 표시','실행 경계의 구체 제한 이유가 일반 문구에 가려질 수 있음. 이번 실제 삭제 실험 없음. '+ref('delete','코드')],
['경비 상세 특정 재시도 불일치','목록 캐시에 ID 부재 + 이전 오류면 Feedback에 retry 제공. retry는 canFetch false일 때 요청 없음','Debug 표시 online·실제 offline/unknown 등에서 버튼은 보여도 요청하지 않는 조건. 실제 화면 재현 미실행. '+ref('detail','코드')]
]))
body+=sec('선행 조각을 재사용하되 남은 책임을 유지합니다',table(['담당','06에서 이미 만든 관련 조각','담당에 남은 범위'],[
['07·17 API 계약','요청·응답·날짜 입력 경계 일부','Trip client PATCH / server PUT 불일치와 허용 필드·ownership·오류 계약'],
['08 날짜 계산','공통 UTC 범위·날짜 입력 보완','대표 여행 계산·그룹 의미·기간 밖 접근과 날짜 없는 여행'],
['09 activation 준비','입수 envelope·시점 검사','새 activation 전체·지도/경로 준비와 완료 상태 확인'],
['10 일정 form','단일 초안·검색 경계·실제 시각 변경만 전송','picker·같은/다른 ID 재열기·늦은 data·native modal'],
['11 경비 form','날짜/연결 독립성·제한 중 초안·오류/재시도','늦은 기본 통화·사용자 통화 보존·재진입 전체·무효 연결'],
['13 저장 후 경로','현재 저장·이동 흐름 재사용','과거 목록 capture·500ms 지연·최신 경로·부분 실패·정상 0 좌표'],
['14 Local mutation','대상 tripId Router 분기·시간 검사·일부 원자성','전체 타입·cache invalidation·나머지 원자성 계약'],
['15 sync','시작 조건·중복 실행·입수 검사','cleanup 부분 실패 결과·IN_PROGRESS 재개·pull 원자성/충돌/cursor'],
['16 cleanup','계정 종료·vacuum 직접 보호','여행별 PENDING 중심 조회를 FAILED/IN_PROGRESS까지 통일·실제 처리 집계']
])+p('이 표는 후속 전체 재검증 결과가 아니라 관련 Ticket 본문과 state가 정한 책임을 정리한 것입니다. 모든 후속 코드를 이번에 전수 검토한 것은 아닙니다.'))
body+=sec('후속 경계를 코드에서도 대조한 사례',p('경비 생성은 비동기 여행에서 기본 통화를 계산해 useForm의 최초 defaultValues로 넘깁니다. 그 뒤 이 훅에는 여행 통화 도착에 맞춰 baseline을 바꾸는 경로가 없습니다. 늦은 기본 통화는 11의 남은 범위와 일치합니다. '+ref('currency','기본값 코드')+'.')+p('일정 submit은 저장 후 500ms timer에서 capture한 schedules와 새 일정을 조합합니다. 저장 입력은 ?? null로 정상 좌표 0을 유지하지만, 뒤 경로 projection은 숫자 0을 truthy 검사해 undefined로 바꿀 수 있습니다. 따라서 “새 일정 장소 0 허용” 테스트를 경로 준비 끝까지 해결됐다는 근거로 쓰면 안 됩니다. '+ref('route','저장 이후 경로 코드')+'.')+p('Trip client는 PATCH, server route는 PUT으로 선언돼 있습니다. 정적 불일치 확인이며 실제 HTTP 호출 실패는 이번에 재현하지 않았습니다. '+ref('patch','client')+' · '+ref('put','server')+'.'))
body+=sec('현재 추가하지 않는 것과 다시 판단할 때',p('복구 토스트는 현재 추가하지 않는 기존 결정을 유지합니다. 실제 종합 UX에서 헤더 상태와 내용 복귀로 복구를 인지하지 못하는 장면이 관찰되면 재검토합니다. 선제적인 polling·weak/degraded 상태·debounce도 이번 검토에 추가하지 않습니다.')+p('후속 항목이 06의 약속한 Local 이용·비활성 제한·초안 보존·명시적 복구를 직접 막는다면 그 실제 장면을 근거로 처리 담당과 범위를 다시 연결해야 합니다. 다른 티켓이라는 이름만으로 직접 막히는 문제를 숨기거나, 관련이 있다는 이유로 모두 06에 흡수하지 않습니다.'))
body+=sec('06 종료에 필요한 근거',p('홈 공통 제한 안내와 foreground 연결을 마무리하고, ③의 실제 사용자 흐름 및 ④의 날짜 차이 상태를 확인해야 합니다. 수정한 것·자동 검사만 있는 것·native/통신 미확인·보류·후속을 구별해 종료 판단 자료를 남깁니다. 현재는 06을 닫을 근거가 충분하지 않습니다.')+p('이 보고서에는 보류 문제의 화면 원본이 없습니다. 재시도 버튼 문제를 다시 수집한다면 목록 캐시에 대상 ID가 없고 이전 오류가 있는 조건에서 display/real 네트워크 상태·버튼 표시·실제 요청 횟수를 함께 남겨야 합니다. 삭제를 실행해야만 이 보고서의 경계를 정리할 수 있는 것은 아닙니다.'))
ev=evidence('state',W+'current/state/index.md',18,32)+evidence('delete',S+'screens/ExpensesScreen.tsx',136,146)+evidence('detail',S+'screens/ExpenseDetailScreen.tsx',15,31)+evidence('detail2',S+'screens/ExpenseDetailScreen.tsx',77,89)+evidence('currency',S+'features/expense/create-expense/useCreateExpenseForm.ts',24,44)+evidence('route',S+'features/schedule/create-schedule/useSubmitSchedule.ts',28,68)+evidence('patch',S+'entities/trip/api/trips.ts',55,64)+evidence('put','apps/server/src/routes/trips.ts',157,164)+evidence('scope13',K+'13-schedule-route-preparation.md',5,15)+evidence('scope16',K+'16-unsynced-data-cleanup.md',25,33)
report('05-scope.html','05','보류·후속 티켓 경계','명시적 보류 두 건을 유지하고, 선행 개선과 후속 전체 완료를 분리했습니다.',body,ev)
# index
cards=''
for file,n,title,desc in [
('02-foreground.html','②','앱 복귀 네트워크 재확인','Store 재확인 기능은 있음 · AppState 연결 없음'),
('03-ux.html','③','목록·상세·폼 종합 UX','초안·조회 구현과 native·실제 단절 미확인을 분리'),
('04-dates.html','④','홈·목록 날짜 차이','현지 날짜와 UTC 범위 차이 · 함수 실행 결과 포함'),
('05-scope.html','⑤','보류·후속 티켓 경계','보류 두 건 유지 · 담당별 재사용 조각과 남은 책임')]:cards+=f'<article class="card"><span class="badge">{n}</span><h2><a href="{file}">{title}</a></h2><p>{desc}</p></article>'
index='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ticket 06 · 나머지 네 보고서</title><style>'+css+'</style></head><body><main><div class="hero"><span class="badge">Ticket 06 · ②~⑤</span><h1>홈 다음에 확인할 네 가지</h1><p class="lead">코드로 확인한 남은 일과 실행이 필요한 장면을 보고서별로 나눴습니다.</p><p class="meta">제공된 0b3b167 스냅샷 기준 · 작성 2026-10-21</p></div><div class="warn"><strong>이번 자료의 제한</strong><br>시뮬레이터·DB·의존성·Git 제외 HTML/스크린샷·worker 로그가 없어 새 화면 수집·병렬 워커 실행은 하지 않았습니다. HTML 네 편은 작성했으며, 스크린샷을 포함한 완전한 실앱 보고서는 아직 아닙니다.</div><div class="cards">'+cards+'</div>'+sec('이번에 직접 확인한 것',p('앱 시작/네트워크 Store/sync 소비, 조회 조합과 화면·form의 회귀 검사 본문, 날짜 표시·그룹, 보류 문제의 코드와 후속 Ticket을 대조했습니다. 날짜 함수만 예시 입력으로 세 시간대에서 실행해 <a href="date-probe.json">결과</a>를 남겼습니다. Jest·제품 UI·DB 실행 결과와 구별합니다.'))+sec('화면 증거가 오면 이어갈 수집 순서',p('한 시뮬레이터에서 비활성 목록·상세 제한/복구를 먼저 수집하고, 일정·경비의 작성 흐름을 이어서 봅니다. foreground는 상태 전환·요청 로그, 날짜는 raw start/end·시간대, 보류 재시도는 캐시/이전 오류 조건을 함께 남겨야 합니다. 각 보고서에 필요한 장면과 판정 기준이 있습니다.'))+'<footer>각 보고서는 독립 HTML입니다. 코드 근거 발췌는 파일 안에 포함돼 있습니다. 외부 서버·이미지·라이브러리 연결은 필요 없습니다.</footer></main></body></html>'
(O/'index.html').write_text(index)
print('Wrote index and four reports')
