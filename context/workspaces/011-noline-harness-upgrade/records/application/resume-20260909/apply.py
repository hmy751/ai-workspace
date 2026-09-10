from pathlib import Path
import json,os,hashlib,subprocess
H=Path(__file__).resolve().parent;P=H/'payload';T=Path('/Users/hammyeong-yeon/Desktop/10_work/noline')
data=json.loads((H/'paths.json').read_text());removed=json.loads((H/'removed.json').read_text());links=json.loads((H/'symlinks.json').read_text())
def stamp(p):
 if p.is_symlink():return {'kind':'symlink','target':os.readlink(p)}
 if p.is_file():return {'kind':'file','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size}
 if p.is_dir():return {'kind':'directory'}
 return {'kind':'absent'}
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=T,text=True).strip()=='b4ed41f6e4bbae26fd45827b3b9063097a2c1ea4'
assert subprocess.check_output(['git','branch','--show-current'],cwd=T,text=True).strip()=='feat/noline-context-harness'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=T).strip()
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=T).strip()
for x in data['items']:
 assert stamp(T/x['path'])==x['before'],('preimage changed',x['path'])
for x in data['protected']:
 current=stamp(T/x['path'])
 assert current['sha256']==x['sha256'],('protected changed',x['path'])
for f in P.rglob('*'):
 if not f.is_file():continue
 dst=T/f.relative_to(P)
 for a in dst.parents:
  if a==T:break
  assert not a.is_symlink(),('symlink ancestor',a)
 assert not dst.is_symlink(),('symlink destination',dst)
 dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(f.read_bytes())
for name,dest in links.items():
 p=T/name;assert not p.exists() and not p.is_symlink();p.symlink_to(dest)
for name in removed:
 original=T/name
 backup=T/'context/work/workspaces/001-noline-context-harness-application/source/prior-memory'/(original.name+'.txt')
 assert original.read_bytes()==backup.read_bytes()
 original.unlink()
for x in data['protected']:assert stamp(T/x['path'])['sha256']==x['sha256']
print(json.dumps({'written_files':sum(f.is_file() for f in P.rglob('*')),'new_symlinks':len(links),'prior_memory_preserved':len(removed),'protected_unchanged':len(data['protected'])}))
