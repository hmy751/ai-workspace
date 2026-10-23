import json,re,subprocess,hashlib
from pathlib import Path
B=Path('/private/tmp/0402-network-timing-20261023');REPO='/Users/hammyeong-yeon/Desktop/10_work/noline';HEAD='7cfa7db7f4a56f05f618163b80c77848032e28a3'
CS=json.loads((B/'commands.json').read_text()); OUT=B/'snapshots';OUT.mkdir(exist_ok=True)
def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def diffs(text):
 lines=text.splitlines(keepends=True);i=0
 while i<len(lines):
  m=re.match(r'diff --git a/(\S+) b/(\S+)\n',lines[i])
  if not m:i+=1;continue
  start=i;p=m[2];i+=1;got=False
  while i<len(lines):
   if lines[i].startswith(('index ','--- ','+++ ','new file mode ','deleted file mode ')):i+=1;continue
   h=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',lines[i])
   if not h:break
   old=int(h[2] or 1);new=int(h[4] or 1);i+=1;got=True
   while (old or new) and i<len(lines):
    s=lines[i]
    if s.startswith(' '):old-=1;new-=1
    elif s.startswith('-'):old-=1
    elif s.startswith('+'):new-=1
    elif s.startswith('\\'):i+=1;continue
    else:break
    i+=1
   if old or new:got=False;break
   if i<len(lines) and lines[i].startswith('\\'):i+=1
  if got:yield p,''.join(lines[start:i])
items=[]
for k,c in enumerate(CS):
 for p,diff in diffs(c['stdout']):
  if not p.startswith(('apps/','.claude/','context/')):continue
  got=subprocess.run(['git','-C',REPO,'show',f'{HEAD}:{p}'],capture_output=True)
  if got.returncode:continue
  work=B/'patch-work';dest=work/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(got.stdout)
  applied=subprocess.run(['patch','--silent','--forward','-p1','-d',str(work)],input=diff.encode(),capture_output=True)
  if applied.returncode:continue
  data=dest.read_bytes();h=re.search(r'^index ([0-9a-f]+)\.\.([0-9a-f]+)',diff,re.M)
  exact=bool(h and blob(got.stdout).startswith(h[1]) and blob(data).startswith(h[2]))
  if not exact:continue
  f=OUT/str(k)/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
  pf=OUT/str(k)/(p+'.patch');pf.write_text(diff)
  items.append({'command_index':k,'source':c['source'],'source_line':c['line'],'timestamp':c['timestamp'],'path':p,'snapshot':str(f.relative_to(B)),'diff':str(pf.relative_to(B)),'git_blob':blob(data),'sha256':hashlib.sha256(data).hexdigest()})
(B/'snapshots.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
last={x['path']:x for x in sorted(items,key=lambda x:x['timestamp'])}
status=CS[158]['stdout'];paths=[l[3:] for l in status.splitlines() if l.startswith(' M apps/')]
print('verified observations',len(items),'files',len(last),'final tracked apps',len(paths))
for p in paths:print(('OK' if p in last else 'MISSING'),p, ('cmd'+str(last[p]['command_index']) if p in last else ''))
