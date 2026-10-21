from pathlib import Path
import sys,json,datetime
root=Path(__file__).resolve().parent
if sys.argv[1:]==['--list']:
 print('\n'.join(str(p.relative_to(root/'input')) for p in sorted((root/'input').rglob('*')) if p.is_file()))
 raise SystemExit
for name in sys.argv[1:]:
 p=(root/'input'/name).resolve()
 p.relative_to((root/'input').resolve())
 content=p.read_text()
 with (root/'reads.jsonl').open('a') as f:f.write(json.dumps({'path':str(p.relative_to(root/'input')),'at':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
 print('FILE '+str(p.relative_to(root/'input'))+'\n'+content)
