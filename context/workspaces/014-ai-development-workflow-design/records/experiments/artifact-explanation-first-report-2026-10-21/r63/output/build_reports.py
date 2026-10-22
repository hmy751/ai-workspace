from pathlib import Path
from html import escape
import json, re
root=Path.cwd(); out=root/'output'; repo=root/'repository'
css='''*{box-sizing:border-box}body{margin:0;background:#f4f6fa;color:#192338;font:16px/1.75 system-ui,-apple-system,sans-serif}main{max-width:1080px;margin:auto;padding:38px 24px 80px}h1{font-size:34px;line-height:1.35}h2{font-size:23px;margin-top:36px}h3{font-size:18px}a{color:#185ab3}nav{display:flex;gap:16px;flex-wrap:wrap;font-size:14px}.lead{font-size:21px;background:#fff;border-left:5px solid #226453;padding:22px}.note{padding:18px 22px;background:#fff5dc;border-radius:12px}.meta{font-size:13px;color:#52617a}section{background:white;border:1px solid #dce2eb;border-radius:14px;padding:22px;margin:20px 0}table{width:100%;border-collapse:collapse;font-size:14px}th,td{vertical-align:top;text-align:left;padding:13px;border-bottom:1px solid #dce2eb}th{background:#edf3f9}pre{font:13px/1.65 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:#172235;color:#e4ebf5;padding:18px;border-radius:8px}code{overflow-wrap:anywhere}details{padding:10px 0}summary{cursor:pointer;color:#185ab3}.scroll{overflow:auto}.badge{display:inline-block;border-radius:20px;padding:3px 12px;background:#e8f0f7;font-size:13px}li{margin:7px 0}.missing{border:2px dashed #b8c3d0;border-radius:10px;padding:20px;color:#52617a}@media(max-width:650px){main{padding:20px 14px}h1{font-size:27px}section{padding:14px}table{min-width:600px}}@media print{body{background:white}main{padding:0}section{break-inside:avoid}nav{display:none}}'''
files=['02-foreground.html','03-integrated-ux.html','04-date-consistency.html','05-scope-boundaries.html']
titles=['② 앱 복귀 시 네트워크 재확인','③ 목록·상세·폼 종합 UX','④ 홈·목록 날짜 차이','⑤ 보류·후속 티켓 경계']
def table(headers,rows):
 return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def section(title,body):return '<section><h2>'+title+'</h2>'+body+'</section>'
def source(path,start,end):
 lines=(repo/path).read_text().splitlines(); excerpt='\n'.join(f'{i+1:4} {v}' for i,v in enumerate(lines) if start<=i+1<=end)
 return f'<details><summary>{escape(path)}:{start} — 코드·문서 발췌</summary><p><a href="../repository/{path}">원문 파일</a></p><pre>{escape(excerpt)}</pre></details>'
def sources(items):return section('근거를 직접 확인하기', ''.join(source(*i) for i in items))
def missing(body): return section('스크린샷·실행 증거', '<div class="missing"><strong>이 보고서에는 앱 스크린샷이 없습니다.</strong><p>앞선 홈 보고서와 9월 30일 HTML·캡처는 Git 제외 자료로, 이번 입력에 제공되지 않았습니다. 시뮬레이터·DB도 없습니다. 과거 대화의 관찰 보고를 이번 직접 관찰로 바꾸거나 화면을 재구성해 캡처처럼 제시하지 않았습니다.</p></div><p>'+body+'</p>')
def page(idx,lead,body):
 nav='<nav><a href="index.html">전체 결과</a>'+''.join(f'<a href="{f}">{escape(t)}</a>' for f,t in zip(files,titles))+'</nav>'
 common='<p class="meta">대조 기준: 제공된 HEAD 0b3b167 tracked snapshot · 조사 방식: 읽기 전용 · 제품 코드 변경 없음</p><p class="note">코드·테스트 본문을 직접 읽었습니다. Jest·시뮬레이터·DB 검증은 이번에 실행하지 않았습니다. 날짜 보고서의 독립 계산만 별도로 실행했습니다. 원래 요청의 6.1 sol 병렬 운영은 이번 환경 제약으로 수행하지 못했습니다.</p>'
 (out/files[idx]).write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+titles[idx]+'</title><style>'+css+'</style><main>'+nav+'<p class="badge">Ticket 06 · 검토 보고서</p><h1>'+titles[idx]+'</h1><p class="lead">'+lead+'</p>'+common+body+'<p class="meta">이 결과는 제공된 snapshot의 검토이며 현재 앱 상태·사용자 acceptance·티켓 완료를 뜻하지 않습니다.</p></main></html>')
page(0,'재확인 기능은 준비되어 있지만, 앱으로 돌아오는 사건과 연결되지 않았습니다. 남은 구현은 앱 수명에서 기존 refresh()를 호출하는 연결입니다.',
section('현재 답과 사용자에게 생기는 차이','<p>다른 앱을 보는 동안 연결이 바뀌면 복귀 직후 기존 관측이 오래됐을 수 있습니다. AppInitialization은 mount 때 네트워크 구독을 시작하고 해제 때 정리하지만 AppState를 구독하지 않습니다. 앱의 src·app·tests를 검색해 foreground 연결을 찾지 못했습니다. 다만 NetInfo나 OS가 자체 관측을 전달할 가능성까지 부정하는 결론은 아닙니다.</p><p>기존 refresh()는 실제 NetInfo.refresh()를 요청합니다. 이미 확인된 online/offline을 먼저 unknown으로 지우지 않으며, 새 관측에 따라 상태를 갱신합니다. 따라서 복귀용 별도 네트워크 저장소나 polling을 추가할 필요는 없습니다.</p>')+
section('있는 동작과 빠진 연결',table(['구간','직접 확인한 내용','판단'],[
['앱 준비','DB → 인증 복원 후 children 연결. 네트워크 확인 결과를 기다리지 않음.','foreground 재확인을 준비 완료의 새 조건으로 넣지 않음.'],
['재확인 중복','진행 중 activeRefresh의 동일 Promise를 반환.','수동 재확인과 복귀가 겹쳐도 기존 장치를 재사용.'],
['늦은 결과','session·activeRefresh·observationRevision을 모두 검사.','새 listener 관측을 오래된 refresh 결과가 덮지 않도록 구성됨.'],
['실패·미응답','unknown이면 확인 불가 안내, 기존 확정 상태는 유지. 작업은 10초 후 종료 가능.','실제 인터넷 도달·서버 정상 응답을 보장하는 timeout이 아님.'],
['복귀 → refresh','AppState 사용·연결을 찾지 못함.','구현과 앱 수명 통합 검사가 남음.']]))+
section('화면과 sync까지 이어지는 범위','<p>관측이 바뀌면 정책 훅은 실제 상태와 표시 override를 구별해 조회 접근을 계산하고, 조회 조합은 제한 또는 캐시 내용을 선택합니다. SyncProvider는 실제 네트워크·인증·override·종료 일시 중단에 따른 실행 가능 조건의 변화를 구독합니다. 단, refresh가 기존 online을 그대로 반환하면 조건 변화가 없으므로 복귀마다 sync를 새로 시작하는 계약은 아닙니다.</p><p>전역 Query의 refetchOnReconnect와 refetchOnWindowFocus는 false입니다. 복귀 연결이 생긴다는 이유로 모든 조회·sync를 강제 실행하거나 완료를 기다리게 해서는 안 됩니다.</p>')+
section('기존 검사와 다음 검사',table(['확인 방법','기존 테스트 본문','추가할 확인'],[
['Store 단위','network.test.ts는 동시 Promise 공유, 실패, timeout, 새 listener 이후 오래된 결과, cleanup 이후 결과 무시를 assertion으로 표현. 이번 재실행 없음.','기존 검사를 재사용해 변경 후 회귀 확인.'],
['앱 수명','layout.test.tsx는 실제 RootLayout과 Store를 쓰되 native·DB·sync를 대체. AppState 복귀 검사는 없음.','background → active, inactive 경유, active 반복 이벤트, mount/cleanup, 수동 refresh와 겹침을 검증.'],
['실앱','이번 관찰 없음.','이전 online/offline/unknown 각각에서 연결 변경 후 복귀. 화면 선택·초안 유지와 sync 중복 여부 관찰.']]))+
missing('수집할 최소 장면: 복귀 전 네트워크 상태 → 다른 앱으로 이동 → 연결 변경 → 복귀 직후 화면과 재확인 완료 화면. 캡처만으로 refresh 호출 횟수는 알 수 없으므로 시각과 호출 로그를 함께 남겨야 합니다.')+
section('다음 행동','<p>AppInitialization의 네트워크 감지 수명에 복귀 listener를 연결하고 cleanup에서 제거하는 작은 구현이 적절합니다. 이전 상태를 기억해 실제 복귀만 재확인하도록 하고, 중복·늦은 결과는 Store에 맡깁니다. 현재 보고서 작업에서는 구현하지 않았습니다.</p>')+
sources([('apps/client/src/application/AppInitialization.tsx',61,80),('apps/client/src/shared/store/network.ts',119,151),('apps/client/src/shared/store/network.ts',291,311),('apps/client/src/shared/services/sync/provider.tsx',48,65),('apps/client/src/shared/lib/queryClient.ts',8,24),('apps/client/tests/shared/store/network.test.ts',223,247)]))
page(1,'초안 유지와 제한·복구를 잇는 코드는 이미 있습니다. 남은 핵심은 실제 단절·native 조작에서도 그 경험이 성립하는지 확인하는 것입니다.',
section('이미 만든 흐름을 다시 구현할 단계는 아닙니다','<p>조회 조합은 여행 없음, 제한, 최초 로딩·실패, 정상 데이터, 기존 데이터를 유지하는 갱신 실패를 나눕니다. 제한 중에도 Query 캐시는 별도로 지우지 않습니다. 사용자는 같은 여행·탭을 유지하고, 접근이 허용되면 기존 내용을 먼저 볼 수 있습니다.</p><p>일정 생성은 검색·작성·장소 변경 단계를 사용자 행동으로 바꾸고 초안을 조건부 폼보다 위에 둡니다. 연결 복귀가 작성 단계를 바꾸거나 두 폼을 동시에 붙이는 과거 문제는 코드와 기존 테스트 본문에서 개선 근거를 확인했습니다. 실제 취소 경고가 없어졌다고 이번에 관찰한 것은 아닙니다.</p>')+
section('장면별 확인 결과와 빈칸',table(['사용자 장면','직접 읽은 근거','아직 필요한 확인'],[
['비활성 목록·상세에서 단절 → 복구','정책을 우선해 캐시를 가리고, ready에서는 캐시를 다시 사용. schedule-recovery·expense-recovery·read-query-consumers에 관련 assertions.','같은 여행과 지도 선택을 유지하는 실제 화면 전환.'],
['최초 조회 실패','첫 실패를 error로 표시. 일정 상세 오류·경비만 실패·홈 경비 실패를 빈 결과나 0원과 구별하는 검사 본문.','서버 실패를 만든 실제 화면에서 문구·버튼 가시성 확인.'],
['기존 내용 갱신 실패','ready + refreshFailed로 내용을 유지하고 갱신 실패 안내. retry 가능 여부를 따로 전달.','좁은 폭에서 본문·재시도, 연속 단절·재시도 경험.'],
['일정 작성 중 연결 변화','create-schedule-flow가 단일 폼·제목·장소 유지, unknown 저장 차단, 복구 후 명시적 저장을 검사.','native 날짜/시간 picker 확인·취소, 키보드, 전체 저장·재진입.'],
['경비 작성·수정','날짜와 일정 연결을 독립적으로 유지. 생성 flow는 다른 날짜 연결, null 해제, 저장 실패 후 입력 유지와 명시적 재시도를 표현.','비활성 기존 연결 보유 초안의 제한·해제·복구를 실제 앱에서 수집.'],
['활성 Local 저장','Router·생성 flow가 활성 offline/unknown의 Local 경로를 표현. native DB·HTTP는 대체됨.','실제 통신 단절에서 저장 → 재진입 → 복구 sync 후 서버 반영. Debug override로는 입증할 수 없음.']]))+
section('Debug 화면 검증과 실제 단절을 구분합니다','<p>Debug override는 표시 제한을 재현하지만 Router 쓰기를 Local·Remote 모두 막는 계약입니다. 따라서 Debug offline에서 입력이 남았다는 사실은 실제 offline Local 저장 성공의 근거가 아닙니다. 과거 대화의 활성 홈 일정 2개·EUR 56 유지도 홈의 표시 대조 결과에 한정됩니다.</p><p>이전 기록에는 개발 DB에 반영된 경비 두 건과 날짜·연결·명시적 재시도 확인이 있습니다. 현재 환경에는 그 DB와 로그가 없으므로 과거 보고로만 취급합니다. 기존 523 passed / 1 skipped 기록 역시 이번 실행 결과가 아닙니다.</p>')+
section('수집은 한 여행·상태 묶음으로', '<ol><li>비활성 여행을 online에서 열어 목록·상세와 기존 연결이 있는 폼을 준비합니다.</li><li>offline·unknown에서 각 화면의 제한 문구, 선택 유지, 폼 값을 빠르게 수집합니다. 수집자는 원인 판정을 보류하고 조건·조작·보이는 결과를 남깁니다.</li><li>online 복구 직후 기존 내용, 자동 저장 없음, 명시적 재시도 결과를 수집합니다.</li><li>활성 여행은 별도 실제 단절 세션에서 Local 저장과 복구 후 반영을 확인합니다. 쓰기 환경을 고정해야 합니다.</li></ol><p>우선 캡처는 전체 화면과 오류 영역의 확대를 함께 확보하면 됩니다. native picker·실제 단절 저장은 입력과 결과가 바뀌는 별도 실행이라 후순위 수집 묶음으로 둡니다.</p>')+
missing('목록·상세는 정상/제한/복구 세 장면을 같은 여행으로, 폼은 연결 전 입력과 차단 후 입력·복구 후 재시도 결과를 쌍으로 수집해야 합니다. 이번에는 그 이미지를 확보하지 못했습니다.')+
section('06 종료 판단에 미치는 영향','<p>검사 본문에 시나리오가 있다는 이유로 전체 UX 완료로 닫을 수 없습니다. 우선 native 흐름과 실제 단절 저장의 빈칸을 채우고, 발견한 문제가 06의 제한·복구 약속을 직접 막는지 판단해야 합니다. 경비 삭제 실패 이유와 특정 상세 재시도 문제의 기존 보류는 유지합니다.</p>')+
sources([('apps/client/src/shared/services/policy-query/usePolicyReadQuery.ts',20,36),('apps/client/src/screens/CreateScheduleScreen.tsx',24,45),('apps/client/tests/screens/read-query-consumers.test.tsx',238,284),('apps/client/tests/screens/create-schedule-flow.test.tsx',129,163),('apps/client/tests/screens/create-expense-flow.test.tsx',169,197),('apps/client/src/screens/ScheduleQueryFeedback.tsx',28,47)]))
checks=json.loads((out/'date-check.json').read_text())
rows=[[r['zone'],r['homeStart']+' ~ '+r['homeEnd'],', '.join(r['listDates']),r['scheduleLocalDate'], '포함' if r['scheduleInListRange'] else '범위 밖'] for r in checks['cases']]
page(2,'홈과 목록은 서로 다른 날짜 기준을 사용합니다. 설명용 입력으로 하루 차이와 목록 범위 밖 일정이 생기는 계산을 확인했지만, 당시 DB 값을 재현한 것은 아닙니다.',
section('직접 확인한 원인과 영향','<p>홈 MainTripSection은 Trip startDate·endDate를 new Date로 읽고 기기의 getMonth/getDate로 표시합니다. 일정·경비 목록은 getUTCDateRange로 Trip timestamp의 UTC 날짜 범위를 만듭니다. 일정 목록은 그 날짜에 일정의 현지 날짜를 맞춰 묶습니다.</p><p>이 조합에서는 홈의 마지막 날에 해당하는 일정이 목록 날짜 범위에 들어가지 않을 수 있습니다. Query에서 삭제된다는 뜻이 아니라 날짜 범위를 순회해 만든 목록 그룹에 배치되지 않는다는 뜻입니다. 실제 사용자 데이터에서 발생했는지는 원본 여행·일정 시각과 기기 시간대가 있어야 확정할 수 있습니다.</p>')+
section('독립 계산으로 확인한 예시','<p><strong>가정한 입력:</strong> 여행 시작 <code>2026-09-30T00:00:00+09:00</code>, 종료 <code>2026-10-02T00:00:00+09:00</code>. 비교 일정은 <code>2026-10-02T09:00:00+09:00</code>입니다. 이는 과거 DB에서 가져온 값이 아닙니다.</p>'+table(['기기 시간대','홈 날짜','목록 날짜 범위','비교 일정 현지 날짜','그룹 포함'],rows)+'<p>실제 getUTCDateRange 본문에서 타입 표기만 제거해 Node로 실행했습니다. 홈과 일정 날짜는 같은 Date 구성요소 방식으로 독립 계산했습니다. Seoul에서 홈은 9/30~10/2이고 범위는 9/29~10/1이며, 10/2 일정은 그룹 범위 밖임을 assertion으로 확인했습니다. 앱·렌더·DB 실행은 아닙니다.</p><p><a href="date-check.json">입력·시간대별 실제 계산 결과</a> · <a href="date-check.cjs">재현 스크립트</a></p>')+
section('이미 개선된 부분과 남은 의미',table(['대상','현재 근거','남은 판단'],[
['UTC 범위 계산','공통 helper가 UTC 일자로 순회. datetime.test는 DST 기간의 중복·누락 없는 범위를 검사.','홈과 같은 날짜를 뜻한다는 보장은 아님. 이번 Jest 미실행.'],
['경비 date','달력 날짜 YYYY-MM-DD. 날짜와 일정 연결은 독립.','홈 표시를 맞추려고 경비 date에 timezone 변환을 적용하면 안 됨.'],
['일정 scheduledAt','한 시점. 폼 현지 날짜·시간을 submit에서 ISO로 결합.','현지 날짜 그룹과 Trip 날짜 범위의 기준 차이를 대조해야 함.'],
['Trip start/end','공유 schema는 ISO datetime, UI는 여행 시작·종료일처럼 사용.','장기적으로 달력 날짜인지 시점인지 아직 결정되지 않음.']]))+
section('고칠 범위는 날짜 의미에 따라 달라집니다','<p>단지 홈 formatter를 UTC로 바꾸면 숫자는 맞출 수 있지만 사용자가 선택한 여행 날짜가 달라질 수 있습니다. 반대로 목록을 현지 날짜로 바꾸면 기기 시간대 변경·대표 여행 계산·기간 밖 일정 접근에 영향을 줍니다. 어느 쪽도 단순 스타일 수정으로 채택하지 않습니다.</p><p>06에서는 이 차이와 노출 영향을 확인하고, 계산·표현은 Ticket 08, 날짜 일관성·기간 밖 접근은 그 티켓이 연결한 003-08과 조율하는 것이 맞습니다. 본 실행에서는 003의 과거 보고서를 대체 기준으로 사용하지 않았습니다.</p>')+
missing('원본 여행 ID, API/Local startDate·endDate 원문, 일정 scheduledAt 원문, 기기 시간대, 같은 여행의 홈·목록 캡처가 필요합니다. 현재 대표 여행과 사용자가 선택한 여행이 같은지도 캡처에 남겨야 합니다.')+
section('다음 행동','<p>우선 문제 여행의 원문 값과 시간대를 확보해 독립 예시가 실제 사례와 같은지 대조합니다. 그 다음 날짜 의미를 고정하고 홈·목록·그룹·대표 여행에 미치는 영향을 함께 검사합니다. 현재 근거로는 “해결됨”이나 “원본 사례 재현됨”으로 닫을 수 없습니다.</p>')+
sources([('apps/client/src/screens/HomeScreen/MainTripSection.tsx',33,40),('apps/client/src/screens/ScheduleScreen.tsx',95,103),('apps/client/src/screens/ScheduleScreen.tsx',172,183),('apps/client/src/shared/lib/datetime.ts',80,99),('apps/client/tests/shared/lib/datetime.test.ts',56,67),('context/project/common/date-and-time.md',63,82)]))
page(3,'06의 남은 연결과 실앱 확인은 끝내야 합니다. 이미 보류한 결함을 되살리거나, 일부 개선을 후속 티켓 전체 완료로 확대해서는 안 됩니다.',
section('06에서 끝내야 할 결과','<p>06은 초기화·인증·네트워크 관측이 화면 제한·복구·작성 유지와 sync 시작에 일관되게 연결되는 작업입니다. 남은 핵심은 홈 공통 안내, foreground 재확인 연결, 목록·상세·폼의 종합 확인, 날짜 차이의 영향과 처리 경계입니다. 2~5번 보고서 생성은 제품 구현이나 06 종료를 대신하지 않습니다.</p>')+
section('명시적 보류와 현재 선택',table(['항목','직접 대조한 근거','이번 처리'],[
['경비 삭제 실패 이유 유실','ExpensesScreen의 onError는 구체 오류를 받지 않고 “경비 삭제에 실패했습니다.” 안내. Ticket·state가 사용자 보류 기록.','미해결로 유지. 자동으로 다음 필수 작업에 올리지 않음.'],
['경비 상세 특정 재시도','retry는 canFetch가 true일 때만 실행. cached list에 대상 없음 + 과거 오류 + display online/real offline에서 오류 버튼 경로와 차단이 어긋날 여지가 코드에 남음.','과거 재현 보고와 코드 근거를 구별. 이번 실앱 재현 없음. 보류 유지.'],
['복구 토스트','Ticket 06은 헤더 상태·내용 복귀·Query 오류로 우선 처리하고 현재 추가하지 않기로 기록.','추가하지 않음. 복구를 알아차리지 못하는 실제 장면이 생기면 재검토.']]))+
section('후속 책임과 재사용할 선행 결과',table(['담당','이미 받은 결과','계속 남는 책임'],[
['07·17 API 경계','Schedule/Expense 시간 검사, serializer와 요청 경계 일부.','Trip client PATCH / server PUT 차이가 실제 코드에 남음. method·허용 필드·전체 접근/오류 계약 확인.'],
['08 날짜 계산','공통 UTC 범위·시각 입력 helper.','대표 여행 계산·현지 날짜 그룹·기간 밖 접근. 날짜 의미를 새로 정했다는 뜻이 아님.'],
['10 일정 폼','단일 초안·검색 책임, 날짜/시각 검사와 변경값 전송.','picker·동일/다른 ID 재열기·늦은 데이터·native modal 전체 조합.'],
['11 경비 폼','초안·모든 날짜 일정 연결/해제·날짜 독립성.','늦게 온 여행 통화와 사용자 수정 관계, 재진입·외부 갱신·무효 연결.'],
['13 저장 후 경로','저장 요청 입력 개선.','성공 후 500ms 대기와 오래된 목록, 경로 재사용·좌표 0·부분 실패.'],
['14 Local mutation','Router 대상 tripId와 transaction·반환 검사 일부.','실기기 SQLite, 전체 write·타입·cache invalidation 계약.'],
['15 sync 결과','실패 큐 재시도·인증 중단·typed pull의 선행 구현.','중단 IN_PROGRESS 재개, cleanup 부분 실패, 전체 pull 원자성·충돌·cursor.'],
['16 cleanup','계정 종료와 vacuum의 미전송 보존 일부.','여행별 정리는 여전히 PENDING 중심. FAILED/IN_PROGRESS predicate·실제 processed 집계와 공통 정리.']]))+
section('코드가 보여 주는 구체적인 남은 차이','<p>경비 생성의 기본 통화는 여행 query에서 계산하지만 useForm의 최초 defaultValues에만 들어갑니다. 늦게 여행이 도착할 때 반영하는 흐름은 이 훅에서 찾지 못했습니다. 이는 11의 남은 범위와 일치합니다.</p><p>일정 submit은 저장 요청에는 null 병합으로 좌표 0을 유지하지만 성공 후 경로용 projection에서는 truthy 비교와 500ms timer를 사용합니다. “장소 상세 0 좌표 선택 테스트가 있다”는 사실을 경로 계산까지 정상이라고 확대하면 안 됩니다.</p><p>cleanup은 여행별 hasPendingTasksForTrip을 확인하는 경로를 사용합니다. 계정 종료의 FAILED 보존 개선이 여행별 cleanup 전체까지 자동 적용된 것은 아닙니다. 16의 위험은 유지하되 이번 화면 수집을 위해 여행을 비활성화하거나 파괴적인 정리 실험을 수행하지 않았습니다.</p>')+
section('완료 판단과 다음 실행','<p>후속 티켓이 남았다는 사실만으로 06을 무한히 늘릴 필요는 없습니다. 반대로 후속으로 보냈다는 문구만으로 06의 약속을 막는 문제를 제외할 수도 없습니다. 문제를 발견하면 제한·복구·작성 유지의 현재 약속을 직접 막는지, 어떤 책임이 소유하는지를 대조해야 합니다.</p><p>현재는 홈 안내를 먼저 정리하고, ②의 복귀 연결과 ③의 실제 검증을 이어가는 순서가 적절합니다. 날짜는 원본 값으로 확인해 08과 경계를 정합니다. 종료 보고에는 실제 수정·확인한 장면, 확인 못한 조건, 보류와 후속 담당을 함께 남겨야 합니다. 사용자 수락과 Ticket 전체 완료는 아직입니다.</p>')+
missing('이 보고서는 작업 경계를 판정하는 코드·문서 보고서입니다. 스크린샷만으로 PATCH/PUT·큐 보존·경로 준비 완료를 판단할 수 없습니다. 해당 확인에는 요청 로그, 큐/DB 결과, 최신 저장 결과와 경로 입력 비교가 필요합니다.')+
sources([('apps/client/src/screens/ExpensesScreen.tsx',136,146),('apps/client/src/screens/ExpenseDetailScreen.tsx',14,22),('apps/client/src/screens/ExpenseDetailScreen.tsx',67,79),('apps/client/src/features/expense/create-expense/useCreateExpenseForm.ts',20,44),('apps/client/src/features/schedule/create-schedule/useSubmitSchedule.ts',24,64),('apps/client/src/entities/trip/api/trips.ts',55,64),('apps/server/src/routes/trips.ts',155,165),('apps/client/src/shared/services/sync/cleanup-job.ts',107,122),('context/work/workspaces/002-code-readability-refactoring/current/state/index.md',19,35)]))
index='''<p class="lead">2~5번을 각각 HTML 보고서로 만들었습니다. 코드상 남은 연결과 실제 화면 검증의 빈칸을 분리했고, 날짜 차이는 독립 계산으로 확인했습니다.</p><p class="note">이번 입력에는 원래 홈 HTML·스크린샷·시뮬레이터·DB가 없습니다. 새 캡처와 동일한 원본 디자인 재현, 서브 워커 병렬 실행은 수행하지 못했습니다. 아래는 제공된 코드 snapshot을 검토한 결과입니다.</p>'''+table(['보고서','현재 답','다음 행동'],[[f'<a href="{files[0]}">{titles[0]}</a>','Store 재확인은 있음. 앱 복귀 연결 없음.','앱 수명 listener 연결·통합 검사.'],[f'<a href="{files[1]}">{titles[1]}</a>','초안·복구 코드와 검사 본문 있음. 실앱 빈칸 남음.','한 여행에서 제한→복구 묶음 수집, 실제 단절 Local 저장 별도 확인.'],[f'<a href="{files[2]}">{titles[2]}</a>','홈 local / 목록 UTC. 설명용 입력 계산에서 차이 확인.','원본 Trip·일정 시각과 시간대 확보, 08과 처리 범위 결정.'],[f'<a href="{files[3]}">{titles[3]}</a>','보류 두 건과 후속 책임 유지.','홈 안내→복귀 연결→종합 UX, 06 종료 근거 대조.']])+section('검증 범위','<p>네 HTML의 링크·구조·발췌 경로를 로컬 정적 검사했습니다. 앱 Jest는 의존성이 없어 실행하지 않았습니다. 날짜 helper의 독립 Node 계산은 실행해 assertion 통과를 확인했습니다. 브라우저 렌더와 모바일 가시성은 미확인입니다.</p><p><a href="date-check.json">날짜 계산 결과</a> · <a href="worklog.md">조사·확인 기록</a></p>')
(out/'index.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ticket 06 검토 보고서 2~5</title><style>'+css+'</style><main><p class="badge">제공된 0b3b167 snapshot 기준</p><h1>Ticket 06 · 남은 네 범위 검토</h1>'+index+'</main></html>')
print('Created 4 reports and index')
