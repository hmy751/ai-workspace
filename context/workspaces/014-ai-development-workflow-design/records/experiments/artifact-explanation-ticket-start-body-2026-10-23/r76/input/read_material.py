from pathlib import Path
import sys,json,hashlib,datetime
root=Path(__file__).resolve().parent
cmd=sys.argv[1]
p=(root/sys.argv[2]).resolve()
if not p.is_relative_to(root):raise SystemExit('Outside scope')
s=p.read_text();n=(len(s)+3999)//4000
if cmd=='info':print(json.dumps({'file':sys.argv[2],'characters':len(s),'chunks':n},ensure_ascii=False))
elif cmd=='read':
 i=int(sys.argv[3]);part=s[(i-1)*4000:i*4000]
 if i<1 or i>n:raise SystemExit('Invalid chunk')
 e={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file':str(p.relative_to(root)),'chunk':i,'total_chunks':n,'sha256':hashlib.sha256(part.encode()).hexdigest()}
 with (root/'read-events.jsonl').open('a') as f:f.write(json.dumps(e,ensure_ascii=False)+'\n')
 print(json.dumps(e,ensure_ascii=False));print(part);print('END OF CHUNK '+str(i)+'/'+str(n))
else:raise SystemExit('Use info or read')
