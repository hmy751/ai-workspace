import json
from pathlib import Path
p=Path('/tmp/noline_remaining_reports_content.json')
d=json.loads(p.read_text())
P='artifacts/ticket-06-simulator/remaining-review-20261004/'
foreground=dict(path=P+'01-foreground-home.jpg',title='홈 버튼에서 나갔다가 앱 아이콘으로 복귀',state='활성 파리 여행 · online · override 없음',observation='시뮬레이터 Home 버튼으로 나간 뒤 SpringBoard의 Noline(Dev) 아이콘을 눌렀습니다. 복귀한 홈에 온라인·준비 완료·9월 30일~10월 2일·일정 2개·EUR 56.00이 보입니다.',limit='화면 복귀를 확인한 캡처입니다. refresh 호출·실제 연결 변화·sync 실행은 이 화면만으로 확인할 수 없습니다.',badge='현재 수집 · 10월 4일',old=False)
d[0]['thumbnail']=foreground['path']
d[0]['thumbnailAlt']='Home 버튼 이후 앱 아이콘으로 복귀한 온라인 홈'
s=d[0]['sections'][2]
s['paragraphs']=['Home 버튼으로 앱을 떠났다가 앱 아이콘을 직접 눌러 돌아온 화면을 수집했습니다. 앞선 앱 실행 도구 시도는 PID 변화와 Metro 로딩이 있어 foreground 근거에서 제외했고, 아래는 아이콘 복귀로 다시 수집한 최종 화면입니다.']
s['shots']=[foreground]
for report in d:
 for section in report['sections']:
  for shot in section.get('shots',[]):
   if shot['path'].endswith('08-expense-create-form.jpg'):shot['path']=P+'08-expense-create-unsaved.jpg'
d[2]['sections'][0]['shots'][0]=dict(foreground,title='홈의 여행 기간',observation='같은 활성 파리 여행의 홈은 9월 30일~10월 2일, 일정 2개·경비 EUR 56.00으로 표시합니다.',limit='이번 추가 수집의 최종 홈 캡처입니다. 원본 startDate/endDate 값은 이 화면만으로 확인할 수 없습니다.')
d[2]['sections'][0]['note']='이번 추가 수집에서 같은 활성 파리 여행의 홈과 목록을 비교했습니다. 여행 기간·활성 상태·기기 날짜를 바꾸지 않았습니다.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
obs=Path(P+'observations.md')
t=obs.read_text().replace('06·07 실제 캡처 헤더에는 온라인 라벨이 보이지 않는다. AX에 남은 온라인 text를 시각적으로 보이는 상태로 확대하지 않는다. 08 헤더에는 온라인 라벨이 보인다.','Main 이미지 재검토: 06·07·08 캡처 모두 헤더 오른쪽에 초록색 온라인 라벨이 보인다. 앞선 수집자의 06·07 라벨 미표시 기록은 이미지와 달라 정정했다. 화면의 온라인 표시는 실제 통신 성공이나 refresh 실행을 보장하지 않는다.')
obs.write_text(t)
