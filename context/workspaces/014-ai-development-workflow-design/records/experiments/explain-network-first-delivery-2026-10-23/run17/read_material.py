from pathlib import Path
import sys,json,hashlib,datetime
root=Path(__file__).resolve().parent
base=root/'input'
inv=json.loads((root/'inventory.json').read_text())
if len(sys.argv)==1:
 print(json.dumps(inv,ensure_ascii=False,indent=2));sys.exit()
name=sys.argv[1]
if name not in inv: raise SystemExit('Allowed input file required')
p=base/name
lines=p.read_text().splitlines(keepends=True)
start=int(sys.argv[2]) if len(sys.argv)>2 else 1
end=min(start+119,len(lines))
chunk=''.join(lines[start-1:end])
event={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'path':name,'start':start,'end':end,'sha256':hashlib.sha256(chunk.encode()).hexdigest()}
with (root/'output/read-events.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
print(f'{name} lines {start}-{end} / {len(lines)}')
print(chunk,end='')
