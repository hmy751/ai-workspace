from pathlib import Path
import sys,json,hashlib,datetime
root=Path(__file__).resolve().parent
if len(sys.argv)!=3: raise SystemExit('Usage: read_material.py relative-file chunk-number')
p=(root/sys.argv[1]).resolve()
if not p.is_relative_to(root):raise SystemExit('Outside input scope')
data=p.read_text();parts=[data[i:i+4000] for i in range(0,len(data),4000)]
n=int(sys.argv[2]);part=parts[n-1] if 1<=n<=len(parts) else None
if part is None:raise SystemExit('Invalid chunk')
e={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file':str(p.relative_to(root)),'chunk':n,'total_chunks':len(parts),'start_character':(n-1)*4000,'end_character':min(n*4000,len(data)),'sha256':hashlib.sha256(part.encode()).hexdigest()}
with (root/'read-events.jsonl').open('a') as f:f.write(json.dumps(e,ensure_ascii=False)+'\n')
print(json.dumps(e,ensure_ascii=False));print(part);print('END OF CHUNK '+str(n)+'/'+str(len(parts)))
