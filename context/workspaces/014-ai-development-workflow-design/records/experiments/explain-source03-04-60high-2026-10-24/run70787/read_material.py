from pathlib import Path
import sys,json,hashlib,datetime
r=Path(__file__).resolve().parent
inv=json.loads((r/'inventory.json').read_text())
log=r/'output/read-events.jsonl'
if len(sys.argv)==1:
 print('\n'.join(f"{p} | {v['chunks']} chunks" for p,v in inv.items()));sys.exit()
if sys.argv[1]=='--check':
 events=[json.loads(x) for x in log.read_text().splitlines()] if log.exists() else []
 seen={(x['path'],x['chunk']) for x in events}
 chosen={x['path'] for x in events}|set(json.loads((r/'required.json').read_text()))
 missing=[(p,n) for p in sorted(chosen) for n in range(1,inv[p]['chunks']+1) if (p,n) not in seen]
 result={'complete':not missing,'files':len(chosen),'missing':missing}
 (r/'output/read-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False));sys.exit(1 if missing else 0)
p=sys.argv[1]
if p not in inv:raise SystemExit('Allowed input file required')
n=int(sys.argv[2]) if len(sys.argv)>2 else 1
if n<1 or n>inv[p]['chunks']:raise SystemExit('Chunk outside bounds')
t=(r/'input'/p).read_text();chunk=t[(n-1)*3000:n*3000]
event={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'path':p,'chunk':n,'sha256':hashlib.sha256(chunk.encode()).hexdigest()}
with log.open('a') as f:f.write(json.dumps(event)+'\n')
print(f'BEGIN {p} chunk {n}/{inv[p]["chunks"]}')
print(chunk)
print(f'END {p} chunk {n}/{inv[p]["chunks"]}')
