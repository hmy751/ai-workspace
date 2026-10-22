from pathlib import Path
from html.parser import HTMLParser
import json
base=Path.cwd()/'output'
class Parser(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True); self.links=[]; self.images=[]; self.headings=[]; self.language=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a': self.links.append(a.get('href',''))
  if tag=='img': self.images.append(a.get('src',''))
  if tag=='h1': self.headings.append(tag)
  if tag=='html': self.language=a.get('lang')
results=[]
for path in sorted(base.glob('*.html')):
 p=Parser(); p.feed(path.read_text()); missing=[]
 for link in p.links:
  if link.startswith(('https:','http:','data:','#')): continue
  if not (path.parent/link.split('#')[0]).exists(): missing.append(link)
 assert not missing, (path.name,missing)
 assert len(p.headings)==1 and p.language=='ko'
 assert not p.images, 'No supplied screenshots; image evidence must not be fabricated'
 results.append({'file':path.name,'links_checked':len(p.links),'missing_links':missing,'one_h1':True,'language':'ko','images':0})
assert len(results)==5
print(json.dumps({'method':'HTMLParser and local link existence; browser render not performed','reports':results},ensure_ascii=False,indent=2))
