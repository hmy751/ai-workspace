from pathlib import Path
from html import escape
import json
O=Path(__file__).resolve().parent
R=O.parent/'repository'
T='context/work/workspaces/002-code-readability-refactoring/current/memory/tickets/'
CSS='''*{box-sizing:border-box}body{margin:0;background:#f4f6f8;color:#1e293b;font:16px/1.7 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif}main{max-width:1080px;margin:auto;padding:35px 24px 80px}a{color:#235ca7}nav{display:flex;flex-wrap:wrap;gap:16px;font-size:14px;margin-bottom:28px}header{padding:28px 32px;background:#153f42;color:white;border-radius:20px}header p{color:#deefec}h1{font-size:32px;line-height:1.35;margin:12px 0}h2{font-size:23px;margin:0 0 16px}h3{font-size:18px}section{background:white;border:1px solid #dce3e8;padding:28px;border-radius:16px;margin-top:22px}.tag{display:inline-block;padding:3px 10px;background:#d9ede6;color:#145642;border-radius:6px;font-size:13px}.warning{background:#fff5df;border-left:4px solid #bd8522;padding:16px;margin-top:18px}.lead{font-size:19px;font-weight:600}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;vertical-align:top;padding:13px;border-bottom:1px solid #dce3e8}th{background:#edf3f5}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;line-height:1.6;background:#edf2f6;padding:16px;border-radius:8px}summary{cursor:pointer;font-weight:600}details{margin:14px 0}.muted,figcaption,footer{font-size:13px;color:#536779}.empty{padding:22px;border:2px dashed #b8c4cd;border-radius:12px;background:#f8fafc}ul,ol{padding-left:22px}code{overflow-wrap:anywhere}td:first-child{min-width:140px}@media(max-width:650px){main{padding:18px 12px 40px}section,header{padding:19px}h1{font-size:25px}.table{overflow-x:auto}table{min-width:580px}}@media print{body{background:white}section{break-inside:avoid}nav{display:none}}'''
PAGES=[('02-foreground.html','② 앱 복귀 시 네트워크 재확인'),('03-ux-flows.html','③ 목록·상세·폼 종합 UX'),('04-dates.html','④ 홈·목록 날짜 차이'),('05-scope.html','⑤ 보류·후속 티켓 경계')]
def section(title,body):return f'<section><h2>{title}</h2>{body}</section>'
def table(headers,rows):return '<div class="table"><table><thead><tr>'+''.join(f'<th>{h}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def evidence(path,start,end):
 lines=(R/path).read_text().splitlines()
 return f'<details><summary>{escape(path)} · {start}–{end}행</summary><p class="muted">제공된 코드 원문 발췌 · 실행 화면이 아닙니다.</p><pre>'+escape('\n'.join(f'{i}: {lines[i-1]}' for i in range(start,min(end,len(lines))+1)))+'</pre></details>'
def shots(items):return section('스크린샷과 다음 수집', '<div class="empty"><strong>이번 보고서에는 앱 스크린샷이 없습니다.</strong><br>기존 HTML·캡처·시뮬레이터가 입력에 포함되지 않았습니다. 대화 속 관찰은 이전 보고로만 인용하며, 코드 발췌나 설명용 예제를 실제 화면으로 대체하지 않았습니다.</div><ol>'+''.join('<li>'+s+'</li>' for s in items)+'</ol>')
def write(name,title,verdict,body):
 nav='<nav><a href="index.html">보고서 모음</a>'+''.join(f'<a href="{n}">{escape(t)}</a>' for n,t in PAGES)+'</nav>'
 common='<p class="muted">대상: 제공된 HEAD 0b3b167의 tracked snapshot. Git 메타데이터·당시 실행 환경은 제공되지 않았습니다. 제품 코드 변경 없음.</p>'
 html=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)}</title><style>{CSS}</style></head><body><main>{nav}<header><span class="tag">Ticket 06 · 조사 보고서</span><h1>{escape(title)}</h1><p>{verdict}</p></header>{common}{body}<footer><p>코드 직접 확인 / 기존 검증 기록 / 이번 제한된 실행 / 미확인을 구분했습니다. Jest·native·DB 통과 및 티켓 완료를 새로 선언하지 않습니다.</p></footer></main></body></html>'
 (O/name).write_text(html)

body=section('판단과 사용자에게 미치는 영향','<p class="lead">재확인 동작은 구현됐지만, 앱으로 돌아온 사건에 연결된 앱 코드는 없습니다.</p><p>다른 앱에 있는 동안 네트워크가 바뀌었을 때 복귀 시 관측을 다시 요청하는 연결이 남았습니다. 다만 NetInfo 자체 listener가 관측을 전달할 수 있으므로, “복귀하면 반드시 오래된 상태가 남는다”는 실제 결함 재현까지 확인한 것은 아닙니다.</p>')
body+=section('현재 연결',table(['부분','직접 확인한 코드','남은 일'],[
('앱 수명','AppInitialization mount에서 networkStore.init(), unmount에서 cleanup(). DB→인증 복원→앱 진입은 네트워크 확정과 별개.','background/inactive→active 변화에서 refresh를 호출할 앱 수명 연결.'),
('재확인','networkStore.refresh()가 NetInfo.refresh()를 요청. 동시 호출은 같은 Promise 공유.','복귀 이벤트와 수동 버튼이 겹칠 때 실제 integration 확인.'),
('늦은 관측','refresh 시작 시 revision과 listener 최신 revision을 비교하고 cleanup된 session 응답 무시.','연속 복귀·해제·재진입까지 AppState 소비 테스트로 연결.'),
('화면·sync','화면 표시 override와 실제 요청 관측은 분리.','복귀 결과가 비활성 화면 제한과 실제 online sync 시작 조건에 전달되는지 관찰.')]))
body+=section('검증 근거의 범위','<p><strong>직접 확인:</strong> 앱 source 전체에서 AppState 참조를 찾지 못했습니다. Network Store와 관련 테스트 본문에서 중복 Promise 공유, 오래된 refresh 배제, cleanup 후 응답 무시를 확인했습니다.</p><p><strong>테스트 파일의 존재와 검사 내용 확인:</strong> tests/shared/store/network.test.ts 223행·297행·356행. 이번에 Jest를 실행한 것은 아닙니다. Store 단위의 검사는 아직 없는 앱 복귀 연결의 검증이 될 수 없습니다.</p><p><strong>이전 기록:</strong> 06 티켓은 foreground 후속과 전체 UX 수락을 남겨 두었습니다. 대화의 홈 online/offline/unknown 관찰은 background 복귀 검증이 아닙니다.</p>')
body+=section('수정한다면 지켜야 할 경계','<p>앱 실행 수명을 소유하는 AppInitialization에서 실제 복귀 전환을 구별해 기존 refresh를 호출하는 방향이 적절합니다. 현재 active 상태로의 단순 rerender와 실제 복귀를 구별하고 listener 정리도 같은 수명에 둡니다. 인증 복원·DB 준비·Splash를 다시 시작할 이유로 삼지 않습니다.</p><p>복귀 직후 강제로 unknown으로 바꾸거나 polling을 추가하지 않습니다. unknown일 때만 확인하는 것으로 한정하지도 않습니다. 이미 Store가 맡는 중복·timeout·늦은 결과 방어를 새로 복제할 필요는 없습니다.</p>')
body+=shots(['앱 online 화면을 기준 캡처한 뒤 background 이동 → 실제 연결 변경 → foreground 복귀 화면·상태 로그를 같은 여행에서 수집.','빠른 복귀 반복과 수동 재확인을 겹치고 요청 수·최종 관측·화면을 함께 수집.','활성 여행은 Local 이용 유지, 비활성 여행은 제한 해제 또는 유지, 실제 online 복구는 sync 시작 조건까지 별도 로그 확인.'])
body+=section('직접 근거',evidence('apps/client/src/application/AppInitialization.tsx',66,86)+evidence('apps/client/src/shared/store/network.ts',142,170)+evidence('apps/client/src/shared/store/network.ts',278,305))
write(*PAGES[0],'기존 refresh를 복귀 수명에 연결할 작업이 남았습니다. 실제 foreground 전환은 이번에 실행하지 않았습니다.',body)

body=section('판단과 현재 상태','<p class="lead">화면별 제한·복구·입력 유지의 자동 검사 근거는 있습니다. 남은 일은 native 화면에서 같은 흐름이 자연스럽게 이어지는지 확인하는 것입니다.</p><p>연결 변화 자체로 여행·탭·작성 초안을 바꾸지 않고, 비활성 내용만 제한합니다. 복구하면 같은 여행의 캐시를 먼저 표시하며 저장은 사용자가 다시 실행합니다. 활성 여행의 Local 이용과 지도·검색처럼 인터넷이 필요한 서비스는 구별합니다.</p>')
body+=section('장면별 근거와 남은 확인',table(['장면','확인된 자료','아직 필요한 확인'],[
('비활성 목록 제한·복구','schedule-recovery / expense-recovery에 캐시 숨김·복귀·최초 오류·갱신 오류 테스트.','목록→상세 이동·탭·선택 유지와 안내 중복, 좁은 화면 가독성.'),
('최초 실패와 빈 결과','schedule-recovery 529행: 최초 오류 뒤 재시도 성공일 때 빈 목록. 상세도 오류와 부재 분리.','서버 실패를 실제 요청으로 만들어 빈 일정·0원 오인 없는지 캡처.'),
('기존 내용 갱신 실패','usePolicyReadQuery는 isRefetchError일 때 data 유지와 refreshFailed 반환.','내용·실패 안내·재시도 버튼이 함께 보이는지와 복구 성공 확인.'),
('일정 작성 중 연결 변경','create-schedule-flow 129행: 직접 작성 후 복귀에도 단일 폼과 입력 유지. 146행: 선택 장소 유지.','native 취소 React 경고, picker 확인·취소, 키보드 포함 전체 작성.'),
('경비 작성·일정 연결','create-expense-flow 169행: unknown 저장 거부→초안 유지→online에서 명시적 재시도. 날짜와 연결 독립.','기존 일정 연결이 있는 비활성 초안의 제한·해제, 후보 표시·연결 설명·저장까지.'),
('실제 단절 중 활성 Local 저장','검사는 Router 흐름을 쓰되 Local/Remote 함수가 mock. 기존 기록의 Debug 검사와 별개.','실제 통신 단절 상태에서 저장→목록/상세 재진입→연결 복구→서버 반영.'),
('새 activation 전체','기존 제한적 정상 경비 관찰은 전체 activation 검증이 아님.','준비된 계정·여행으로 native 전체 흐름과 실패·복구를 별도 확인.')]))
body+=section('무엇을 실제로 확인했는가','<p>화면 조회 조합의 구현과 관련 테스트 본문을 직접 대조했습니다. useTripReadAccess는 표시 정책과 실제 관측 정책을 함께 적용하며, refetch callback은 최신 commit의 접근 조건을 다시 확인합니다. UI 제한으로 Query 캐시를 삭제하거나 별도 데이터 복제본을 만드는 구조가 아닙니다.</p><p>테스트는 네트워크·DB·Repository·native Drawer 등의 일부를 대체합니다. 실제 입력 흐름을 쓰는 검사도 iOS picker·키보드·HTTP·SQLite의 실제 작동을 모두 보장하지 않습니다.</p><p><strong>이전 실행 기록:</strong> 10월 2일 티켓·세션 기록에는 client 523 passed / 1 skipped와 날짜가 다른 일정 연결·연결 해제·Debug 초안 유지·명시적 재시도·두 경비 서버 반영이 보고돼 있습니다. 이번 실행의 통과 결과나 제공되지 않은 캡처 재검토로 말하지 않습니다.</p>')
body+=section('효율적인 후속 수집 순서','<ol><li>비활성 여행 한 개를 online에서 열고 목록·상세를 기준 수집합니다.</li><li>같은 여행·탭에서 offline→unknown 확인 중→확인 불가→online으로 전환하며 선택·내용·안내를 수집합니다. 모든 화면에서 같은 초기 상태를 반복 준비하지 않습니다.</li><li>작성 초안 하나에 기존 일정 연결을 두고 제한·복구·명시적 저장을 수집합니다. 일정 폼은 취소·picker·키보드만 별도 보충합니다.</li><li>실제 통신 단절과 서버 실패는 Debug 전환과 나누어 실행합니다. 계정 종료·여행 해제처럼 데이터에 영향을 주는 조작은 수집을 위해 임의 수행하지 않습니다.</li></ol><p>실행 환경이 확보되면 화면 조작은 한 수집 담당이 독점하고 관찰값·문구·캡처만 먼저 반환하는 방식이 적절합니다. 이번 환경에서는 추가 워커·시뮬레이터를 실행하지 않았습니다.</p>')
body+=shots(['목록·상세 각각 정상/제한/복구 비교 캡처. 최초 조회 실패는 기존 데이터가 없는 조건과 구분.','작성 전 입력 → 제한 중 입력·기존 연결 → 복구 후 저장 전 → 명시적 저장 성공의 네 장면.','일정 취소 경고는 화면만이 아니라 console 로그, picker 확인·취소 값은 전후 값을 함께 수집.'])
body+=section('직접 근거',evidence('apps/client/src/shared/services/policy-query/usePolicyReadQuery.ts',23,35)+evidence('apps/client/tests/screens/create-expense-flow.test.tsx',169,197)+evidence('apps/client/tests/screens/schedule-recovery.test.tsx',529,542))
write(*PAGES[1],'자동 검사로 다룬 흐름과 실제 기기에서 남은 장면을 구분했습니다. 새 앱 캡처·Jest 실행은 없습니다.',body)

seoul=json.loads((O/'date-seoul.json').read_text());la=json.loads((O/'date-la.json').read_text())
body=section('판단과 사용자에게 미치는 영향','<p class="lead">홈과 목록의 날짜 기준은 지금도 다릅니다. 같은 입력에서 다른 날짜를 표시할 수 있음을 제한된 계산 실행으로 확인했습니다.</p><p>홈은 기기 현지 날짜의 월·일을 표시합니다. 일정·경비 목록은 Trip timestamp의 UTC 날짜 범위를 공유합니다. 일정은 그 범위 안에서 scheduledAt의 현지 날짜로 묶으므로 범위와 항목 묶기에도 기준 차이가 있습니다. 실제 과거 여행 데이터·기기 시간대는 제공되지 않아 당시 화면의 원인을 단일 입력으로 확정하지는 않습니다.</p>')
body+=section('이번에 실행한 설명용 사례','<p><strong>사용자 DB에서 얻은 데이터가 아닌 설명용 입력입니다.</strong> 시작 <code>2026-09-29T15:00:00Z</code>, 종료 <code>2026-10-01T15:00:00Z</code>를 썼습니다. 실제 getUTCDateRange 함수에서 타입 표기만 제거해 실행했고 홈의 getMonth/getDate 계산을 함께 대조했습니다.</p>'+table(['실행 시간대','홈 시작~종료','목록의 날짜 범위'],[(x['timezone'],' ~ '.join(x['home']),' / '.join(x['list'])) for x in [seoul,la]])+'<p>서울 시간대에서는 홈이 9월 30일~10월 2일이지만 목록은 9월 29일부터 10월 1일까지입니다. LA 시간대에서는 이 입력의 홈과 목록 날짜가 일치합니다. 즉 모든 여행에서 항상 하루 어긋나는 문제가 아니라 저장 시점과 기기 시간대에 따라 나타나는 경계 차이입니다.</p><p>추가로 3월 7~10일 UTC 범위를 두 시간대에서 계산해 각각 네 날짜가 중복·누락 없이 나왔습니다. 이 계산의 정상성은 홈과 목록의 날짜 의미가 일치한다는 뜻은 아닙니다.</p>')
body+=section('책임과 해결 범위',table(['대상','현재 기준','판단'],[
('Trip startDate/endDate','schema·저장에서는 ISO datetime, UI는 여행 시작일/종료일처럼 사용.','달력 날짜인지 한 시점인지 장기 의미는 미결정. 임의 전면 변경 금지.'),
('일정·경비 목록','getUTCDateRange 공통 사용.','DST 일자 순회 개선을 완료 결과로 재사용. 홈 일치까지 해결됐다고 확대하지 않음.'),
('Schedule scheduledAt','한 시점이며 현지 날짜·시각 표시.','기간 밖 일정 접근은 Ticket 08 및 기존 날짜 결함 담당과 연결.'),
('Expense date','YYYY-MM-DD 달력 날짜.','다시 현지 시간으로 이동시키지 않음. Trip 날짜 해결에 끌려 변경할 이유 없음.')]))
body+=section('다음 행동','<p>우선 실제 문제 여행의 원본 startDate/endDate, 기기 시간대, 홈·일정·경비 날짜 캡처를 같은 시각에 수집해야 합니다. 그다음 여행 시작·종료가 사용자의 달력 날짜를 뜻하는지 기준을 정하고 표시·입력·대표 여행 선택·DB/API 영향까지 대조합니다.</p><p>06에서는 차이의 현재 근거와 사용자 영향을 확인하고 처리 담당을 연결합니다. 계산 구조는 08, 기존 날짜/기간 밖 접근 결함은 003-08이 맡는 관계를 유지합니다. 이번 계산 예제로 Trip 데이터 계약 변경이나 티켓 종료를 승인한 것은 아닙니다.</p>')
body+=shots(['같은 여행의 홈 기간과 일정·경비 날짜 탭을 나란히 캡처하고 Trip raw ISO와 기기 timezone을 함께 기록.','일정이 여행 기간 경계 밖 현지 날짜에 놓인 조건에서 접근 가능 여부를 별도 수집.'])
body+=section('직접 근거',evidence('apps/client/src/screens/HomeScreen/MainTripSection.tsx',32,38)+evidence('apps/client/src/shared/lib/datetime.ts',80,98)+evidence('apps/client/src/screens/ScheduleScreen.tsx',173,182)+'<p><a href="date-seoul.json">서울 실행 결과</a> · <a href="date-la.json">LA 실행 결과</a>. 전체 Jest 및 실제 기기 시간대 변경 검증은 실행하지 않았습니다.</p>')
write(*PAGES[2],'홈의 현지 날짜와 목록의 UTC 날짜가 병존합니다. 설명용 입력 계산은 실행했으며 당시 DB·화면 재현은 미확인입니다.',body)

body=section('판단과 작업 범위','<p class="lead">보류는 해결이 아니며, 후속 티켓 전체를 06번에 합칠 필요도 없습니다.</p><p>06은 관측·화면·실행 조건이 같은 정책으로 이어지는지 마무리합니다. 이미 개선한 날짜·폼·sync 조각은 재사용하고 각 티켓이 맡는 나머지 책임을 남깁니다. 기록의 “최초 조사”와 “현재 상태”를 구별해야 이미 고친 문제를 다시 미해결로 올리지 않을 수 있습니다.</p>')
body+=section('사용자가 결정한 보류·비채택',table(['항목','현재 근거','이번 처리'],[
('경비 삭제 실패 이유 유실','ExpensesScreen 143~144행 onError가 원인을 받지 않고 일반 실패 문구 표시.','명시적 보류 유지. 해결 또는 다음 실행 필수 선행으로 처리하지 않음.'),
('경비 상세 특정 재시도 불일치','기존 목록 캐시에 대상 ID 없음+Query 오류+Debug online/실제 offline에서 재시도 UI 가능. callback은 canFetch false이면 종료.','해당 조건의 보류 유지. 모든 재시도 경로가 실패한다고 확대하지 않음.'),
('복구 토스트','9월 30일 결정: 네트워크 표시와 제한 해제·내용 복귀를 사용.','현재 추가하지 않음. 실제 복귀 인지가 어려운 장면이 있어야 재검토.')]))
body+=section('후속 티켓과 재사용할 선행 결과',table(['담당','이미 있는 결과','남은 책임'],[
('08 날짜·그룹·대표 여행','공통 UTC 범위, Date 입력 비변경, DST 누락 시각 거부.','대표 여행 계산·미래 상대시간·날짜 없는 여행·기간 밖 일정·모든 grouping 의미.'),
('10 일정 폼 수명','생성 단일 초안·검색 경계·시각 검사·실제 변경만 전송.','picker 확인·취소·같은/다른 ID 재열기·늦은 데이터와 native modal 조합.'),
('11 경비 폼 수명','날짜와 일정 연결 독립, 모든 날짜 후보·해제, 저장 오류·입력 보존.','늦은 기본 통화·사용자 통화 변경 관계, 재열기·외부 갱신·실제 무효 연결.'),
('13 저장 후 경로 준비','입력과 저장 경계의 개선을 재사용.','500ms 지연·오래된 query 목록·좌표 0 유실·최신 segment와 실패 결과. 이번 source에서도 timer·truthy 좌표 변환 확인.'),
('14 Local mutation·Router','대상 여행 분기, row+queue transaction 및 날짜 반환 검사 롤백 등 선행 조각.','전체 entity write·타입·cache invalidation 계약 대조.'),
('15 sync 결과·재시도','FAILED 재전송·뒤 작업 중단, SyncIncompleteError, HTTP 5xx 재시도 기록, pull envelope 검증이 이미 있음.','cleanup 부분 실패 typed result·IN_PROGRESS 재개·pull 전체 원자성·충돌·cursor. 앞선 결함 전부가 그대로 남은 것은 아님.'),
('16 미전송 보존·정리','계정 종료의 PENDING/IN_PROGRESS/FAILED 보호와 vacuum 원본 보존 개선.','여행별 deactivation/cleanup은 PENDING 중심. 공통 predicate·실제 processed 수·즉시/지연 정리 공통화.'),
('07·17 HTTP 계약','Trip·Expense serializer 등 선행 조각.','Trip client PATCH/server PUT 불일치와 요청·응답·ownership 나머지. 실제 수정 책임 조율 필요.')]))
body+=section('06을 닫기 위한 판단','<p>홈 공통 안내, foreground 연결, 목록·상세·폼 UX를 실제 확인 범위와 대조하고 날짜 차이의 처리 경계를 기록해야 합니다. 새 문제가 06이 약속한 사용자 흐름을 직접 막는다면 원인과 담당을 다시 연결합니다. 후속 티켓이 있다는 이유만으로 막힌 흐름을 완료로 처리해서도 안 됩니다.</p><p>최종 수락에는 수정 결과, 자동 검사 범위, native·통신·DB 확인 장면, 명시적 보류와 후속 범위가 구별돼야 합니다. 이번 보고서 작성은 구현·제품 Verify·사용자 acceptance나 티켓 완료가 아닙니다.</p>')
body+=shots(['이 보고서는 범위·담당 문서이므로 티켓 표 자체의 가짜 앱 캡처는 만들지 않습니다.','보류 문제를 재검토할 때만 실패 이유·재시도 조건의 실제 화면과 요청 로그를 수집합니다.'])
body+=section('직접 근거',evidence('apps/client/src/screens/ExpensesScreen.tsx',136,146)+evidence('apps/client/src/screens/ExpenseDetailScreen.tsx',14,18)+evidence('apps/client/src/features/schedule/create-schedule/useSubmitSchedule.ts',34,61)+evidence('apps/client/src/shared/services/sync/queue.ts',220,235))
write(*PAGES[3],'명시적 보류와 후속 담당을 유지하면서, 이미 해결된 선행 조각과 남은 책임을 나눴습니다.',body)

body=section('네 보고서',table(['보고서','핵심 결과'],[(f'<a href="{n}">{t}</a>',v) for (n,t),v in zip(PAGES,['재확인 함수는 있으나 앱 복귀 연결 없음.','자동 검사 근거와 native·실제 단절 미확인 분리.','서울·LA 계산 실행으로 UTC/현지 기준 차이 확인.','보류 2건·토스트 비채택·후속 티켓별 남은 책임.'])]))
body+=section('이번 결과의 사용 범위','<p>요청하신 ②~⑤를 각각 독립 HTML로 만들었습니다. 인터넷·추가 설치 없이 제공된 코드·테스트·티켓을 직접 조사했습니다. 현재 환경 제약상 추가 서브 워커와 시뮬레이터는 실행하지 않았습니다.</p><p>기존 홈 보고서와 실제 스크린샷은 입력에 없습니다. 네 보고서에 화면을 보았다고 표시하거나 기존 캡처를 재구성하지 않았습니다. 필요한 후속 캡처는 각 보고서에 구체적으로 남겼습니다.</p><p>직접 실행한 것은 날짜 계산 사례와 보고서 구조·링크 확인입니다. 이전 대화의 테스트 통과 수와 앱 관찰을 이번 실행 결과로 재사용하지 않습니다.</p>')
write('index.html','Ticket 06 · 나머지 네 보고서','② foreground 재확인 · ③ 종합 UX · ④ 날짜 차이 · ⑤ 보류와 후속 범위',body)
print('Generated 4 reports and index')
