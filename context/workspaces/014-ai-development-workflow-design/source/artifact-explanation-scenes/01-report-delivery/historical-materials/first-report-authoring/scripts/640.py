from pathlib import Path
import html, json, base64, re
ROOT=Path('/Users/hammyeong-yeon/Desktop/10_work/noline')
DEST=ROOT/'artifacts/ticket-06-simulator/remaining-review-20261004'
DEST.mkdir(parents=True,exist_ok=True)
BASE=ROOT/'artifacts/ticket-06-simulator/home-review-20261004/report.html'
CSS=re.search(r'<style>(.*?)</style>',BASE.read_text(),re.S).group(1)
CSS+='''\n.gallery{grid-template-columns:repeat(2,minmax(0,1fr))}.gallery.single{grid-template-columns:minmax(0,760px);justify-content:center}.status{display:inline-block;padding:5px 10px;border-radius:6px;background:#e8f1e9;font-size:13px;font-weight:700}.warn{background:#fff0d9;color:#805219}.flow{display:flex;gap:12px;align-items:stretch;flex-wrap:wrap;margin:20px 0}.flow div{flex:1;min-width:180px;background:white;border:1px solid var(--line);border-radius:12px;padding:18px}.flow b{display:block;color:var(--green);margin-bottom:8px}.report-links{display:flex;flex-wrap:wrap;gap:10px}.report-links a{border:1px solid var(--line);padding:8px 13px;border-radius:8px;background:white;text-decoration:none}.source-path{font-size:12px;color:var(--muted);overflow-wrap:anywhere}blockquote{margin:16px 0;border-left:3px solid #b4cbb8;padding:8px 18px;background:white}.gallery .shot-heading{min-height:145px}.thumb{width:100%;height:250px;object-fit:cover;object-position:top;border-radius:8px;margin:10px 0}.panel a.title{display:block;text-decoration:none;font-size:21px;font-weight:750;margin:10px 0}.tagline{font-size:13px;color:var(--muted)}@media(max-width:600px){.gallery{grid-template-columns:1fr}.gallery .shot-heading{min-height:0}}'''
FILES=[('02-foreground.html','② foreground 복귀'),('03-journey-ux.html','③ 목록·상세·폼 UX'),('04-date-consistency.html','④ 날짜 표시 차이'),('05-deferred-scope.html','⑤ 보류·후속 범위')]
def E(v):return html.escape(str(v))
def image_uri(path):
 p=ROOT/path
 return 'data:image/'+('png' if p.suffix=='.png' else 'jpeg')+';base64,'+base64.b64encode(p.read_bytes()).decode()
def shot(s):
 return f'''<article class="shot"><div class="shot-heading"><span class="tag {'old' if s.get('old') else ''}">{E(s['badge'])}</span><h3>{E(s['title'])}</h3><p class="state">{E(s['state'])}</p></div><button class="image-button" data-zoom aria-label="{E(s['title'])} 이미지 확대"><img loading="lazy" src="{image_uri(s['path'])}" alt="{E(s['observation'])}"></button><div class="caption"><p>{E(s['observation'])}</p><p class="limit">{E(s['limit'])}</p><span class="filename">{E(Path(s['path']).name)}</span></div></article>'''
def paragraphs(items):return ''.join('<p>'+E(x)+'</p>' for x in items)
def bullets(items,ordered=False):
 t='ol' if ordered else 'ul'
 return '<'+t+'>'+''.join('<li>'+E(x)+'</li>' for x in items)+'</'+t+'>'
def table(headers,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+E(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def navlinks(current=None):
 return '<div class="report-links"><a href="index.html">전체 보고서</a><a href="../home-review-20261004/report.html">① 홈 안내</a>'+''.join(f'<a href="{f}" {"aria-current=page" if f==current else ""}>{E(t)}</a>' for f,t in FILES)+'</div>'
JS='''const viewer=document.getElementById('viewer');document.querySelectorAll('[data-zoom]').forEach(b=>b.addEventListener('click',()=>{const c=b.closest('.shot');document.getElementById('zoomTitle').textContent=c.querySelector('h3').textContent;const i=b.querySelector('img'),z=document.getElementById('zoomImage');z.src=i.src;z.alt=i.alt;document.getElementById('zoomCaption').replaceChildren(c.querySelector('.caption').cloneNode(true));viewer.showModal();}));document.getElementById('close').onclick=()=>viewer.close();viewer.addEventListener('click',e=>{if(e.target===viewer){const r=viewer.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)viewer.close();}});'''
def write_report(d):
 sections=[]
 for s in d['sections']:
  content=paragraphs(s.get('paragraphs',[]))
  if 'items' in s:content+=bullets(s['items'],s.get('ordered',False))
  if 'rows' in s:content+=table(s['headers'],s['rows'])
  if 'flow' in s:content+='<div class="flow">'+''.join('<div><b>'+E(a)+'</b>'+E(b)+'</div>' for a,b in s['flow'])+'</div>'
  if 'shots' in s:content+='<p class="hint">이미지를 누르면 확대됩니다. 촬영 시점과 확인 범위를 각 이미지 아래에 표시했습니다.</p><div class="gallery '+('single' if len(s['shots'])==1 else '')+'">'+''.join(shot(x) for x in s['shots'])+'</div>'
  if 'note' in s:content+='<div class="note">'+E(s['note'])+'</div>'
  sections.append(f'<section id="{s["id"]}"><h2>{E(s["title"])}</h2>{content}</section>')
 source='<details class="sources"><summary>원자료·코드 위치</summary><ul>'+''.join('<li><b>'+E(x['label'])+'</b><br><span class="source-path">'+E(x['path'])+'</span>'+('<p class="small">'+E(x['note'])+'</p>' if x.get('note') else '')+'</li>' for x in d['sources'])+'</ul></details>'
 doc=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(d['title'])} · Ticket 06</title><style>{CSS}</style></head><body><header><div class="eyebrow">NOLINE / TICKET 06 / 2026.10.04</div><h1>{E(d['title'])}</h1><p>{E(d['intro'])}</p><div class="callout"><p><strong>{E(d['conclusion'])}</strong><br>{E(d['limit'])}</p></div></header><nav aria-label="보고서 목차">{''.join('<a href="#'+s['id']+'">'+E(s.get('nav',s['title']))+'</a>' for s in d['sections'])}<a href="index.html">전체 보고서</a></nav><main>{navlinks(d['file'])}{''.join(sections)}{source}<footer>현재 코드·수집·기록을 대조한 보고서입니다. 구현 완료·전체 검증·사용자 수락을 새로 선언하지 않습니다. 이미지는 HTML에 포함했습니다.</footer></main><dialog id="viewer" aria-labelledby="zoomTitle"><div class="modal-head"><h3 id="zoomTitle"></h3><button id="close">닫기 ×</button></div><div class="modal-content"><img id="zoomImage" alt=""><div id="zoomCaption"></div></div></dialog><script>{JS}</script></body></html>'''
 (DEST/d['file']).write_text(doc)
def write_index(reports):
 cards='<article class="panel"><span class="tag">앞서 만든 보고서</span><a class="title" href="../home-review-20261004/report.html">① 홈 안내</a><p>활성 홈의 현재 수집과 비활성 홈의 과거 안내 문제, 공통 안내의 수정 방향.</p></article>'
 for d in reports:
  img=d.get('thumbnail')
  cards+='<article class="panel"><span class="tag">추가 보고서</span><a class="title" href="'+d['file']+'">'+E(d['title'])+'</a>'+('<img class="thumb" src="'+image_uri(img)+'" alt="'+E(d.get('thumbnailAlt','보고서 참고 화면'))+'">' if img else '')+'<p>'+E(d['conclusion'])+'</p><p class="small">'+E(d['limit'])+'</p></article>'
 (DEST/'index.html').write_text(f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ticket 06 · 남은 작업 보고서 모음</title><style>{CSS}</style></head><body><header><div class="eyebrow">NOLINE / TICKET 06 / 2026.10.04</div><h1>남은 작업을 네 갈래로 확인했습니다</h1><p>홈 안내 보고서에 이어 foreground 복귀, 목록·상세·폼 UX, 날짜 표시 차이, 보류·후속 범위를 각각 정리했습니다. 시뮬레이터 한 명은 화면만 수집하고 코드·기존 검증 대조는 병렬로 진행했습니다.</p><div class="callout"><p>관찰된 화면, 코드로 확인한 연결, 과거 기록과 아직 확인하지 않은 범위를 구분합니다. 문제를 새로 구현하거나 보류 항목을 다시 착수한 결과는 아닙니다.</p></div></header><main><div class="grid">{cards}</div><section><h2>읽는 방법</h2><p>각 보고서의 첫 문장에서 핵심 결과를 보고, 이미지 캡션의 날짜·조건·한계를 함께 읽어주세요. 서로 다른 시점과 조건의 화면을 수정 전후로 해석하지 않습니다. 이미지를 누르면 확대됩니다.</p></section><footer>HTML 파일에 스크린샷을 포함했습니다. 현재 보고서 네 편과 앞선 홈 보고서를 함께 연결합니다.</footer></main></body></html>''')
if __name__=='__main__':
 reports=json.loads(Path('/tmp/noline_remaining_reports_content.json').read_text())
 for d in reports:write_report(d)
 write_index(reports)
 for p in DEST.glob('*.html'):print(p.name,p.stat().st_size)
