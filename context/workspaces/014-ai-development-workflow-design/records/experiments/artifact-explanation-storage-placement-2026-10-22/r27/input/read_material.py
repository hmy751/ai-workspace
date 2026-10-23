from pathlib import Path
import sys,json,hashlib,datetime
root=Path(__file__).resolve().parent
for name in sys.argv[1:]:
 p=(root/name).resolve()
 if not p.is_relative_to(root):raise SystemExit("Outside input scope")
 data=p.read_bytes()
 with (root/'read-events.jsonl').open('a') as log:
  log.write(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file':str(p.relative_to(root)),'sha256':hashlib.sha256(data).hexdigest()},ensure_ascii=False)+'\n')
 print('\nFILE: '+str(p.relative_to(root))+'\n'+data.decode())
