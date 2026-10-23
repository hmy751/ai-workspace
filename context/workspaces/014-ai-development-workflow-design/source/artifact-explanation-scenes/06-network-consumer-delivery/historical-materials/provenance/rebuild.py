import ast,builtins,collections,hashlib,json,re,shlex,subprocess
from pathlib import Path
B=Path('/private/tmp/0402-network-timing-20261023');R=B/'reconstructed-v3';R.mkdir(exist_ok=True)
N='/Users/hammyeong-yeon/Desktop/10_work/noline';HEAD='7cfa7db7f4a56f05f618163b80c77848032e28a3'
CS=json.loads((B/'commands.json').read_text());SS=json.loads((B/'snapshots.json').read_text());PS=json.loads((B/'filechanges.json').read_text())
trace=collections.defaultdict(list);issues=[];observations=[];current={}
def path(p):
 s=str(p)
 if s.startswith(N+'/'):s=s[len(N)+1:]
 elif s.startswith(str(R)+'/'):s=s[len(str(R))+1:]
 if s.startswith('/') or '..' in Path(s).parts:raise ValueError('outside reconstruction '+s)
 if not s.startswith(('apps/','context/','.claude/')) and s not in ['.prettierrc','prettier.config.js','.prettierrc.json']:raise ValueError('unsupported path '+s)
 return R/s
def ensure(p):
 p=path(p)
 if not p.exists():
  rel=str(p.relative_to(R));g=subprocess.run(['git','-C',N,'show',f'{HEAD}:{rel}'],capture_output=True)
  if g.returncode:raise FileNotFoundError(rel)
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(g.stdout);trace[rel].append({'kind':'git', 'commit':HEAD})
 return p
def save(p,data,kind):
 p=path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data if isinstance(data,bytes) else data.encode());trace[str(p.relative_to(R))].append({**current,'kind':kind})
class P:
 def __init__(self,p):self.s=str(p)
 def __truediv__(self,p):return P(self.s+'/'+str(p))
 def __str__(self):return self.s
 def read_text(self):return ensure(self.s).read_text()
 def write_text(self,s):save(self.s,s,'recorded-python-transform');return len(s)
 def read_bytes(self):return ensure(self.s).read_bytes()
 def write_bytes(self,s):save(self.s,s,'recorded-python-transform');return len(s)
def op(p,mode='r',*args,**kwargs):
 dest=path(p)
 if any(x in mode for x in 'wa'):
  dest.parent.mkdir(parents=True,exist_ok=True);trace[str(dest.relative_to(R))].append({**current,'kind':'recorded-python-transform'})
 else:dest=ensure(p)
 return builtins.open(dest,mode,*args,**kwargs)
def run_python(s):
 t=ast.parse(s);im=[n for n in ast.walk(t) if isinstance(n,(ast.Import,ast.ImportFrom))]
 for n in im:
  if isinstance(n,ast.ImportFrom) and n.module=='pathlib' and [a.name for a in n.names]==['Path']:continue
  if isinstance(n,ast.Import) and [a.name for a in n.names]==['re']:continue
  raise ValueError('unsupported import '+ast.unparse(n))
 allowed={'Path','open','str','len','print','range','enumerate','zip','list','tuple','set','sorted','bool'}
 methods={'read_text','write_text','read_bytes','write_bytes','read','write','replace','index','find','split','splitlines','join','startswith','endswith','strip','removeprefix','capitalize','group','sub','append'}
 for n in ast.walk(t):
  if isinstance(n,ast.Call):
   if isinstance(n.func,ast.Name) and n.func.id not in allowed:raise ValueError('unsupported call '+n.func.id)
   if isinstance(n.func,ast.Attribute) and n.func.attr not in methods:raise ValueError('unsupported method '+n.func.attr)
  if isinstance(n,ast.Attribute) and n.attr.startswith('_'):raise ValueError('private attribute')
 class StripImports(ast.NodeTransformer):
  def visit_Import(self,n):return None
  def visit_ImportFrom(self,n):return None
 t=StripImports().visit(t)
 env={'__builtins__':{k:getattr(builtins,k) for k in allowed if hasattr(builtins,k)},'Path':P,'open':op,'re':re}
 exec(compile(t,'<recorded-data-transform>','exec'),env)
def format_files(paths):
 valid=[]
 for p in paths:
  if p.startswith('src/') or p.startswith('tests/') or p.startswith('app/'):p='apps/client/'+p
  if not p.startswith('apps/'):continue
  if any(c in p for c in '*?['):
   valid.extend(str(q) for q in R.glob(p) if q.is_file());continue
  try:valid.append(str(ensure(p)))
  except FileNotFoundError:continue
 if not valid:return
 result=subprocess.run(['node',N+'/node_modules/prettier/bin/prettier.cjs','--config',str(B/'prettier.json'),'--write',*valid],capture_output=True)
 if result.returncode:issues.append({**current,'kind':'format-error','detail':result.stderr.decode()[:300]})
 for p in valid:trace[str(Path(p).relative_to(R))].append({**current,'kind':'prettier-3.6.2'})
# Read the committed formatter options as data, never load repository scripts.
config={'arrowParens':'always','singleQuote':True,'jsxSingleQuote':True,'tabWidth':2,'semi':True,'trailingComma':'all','printWidth':120,'endOfLine':'auto'};(B/'prettier.json').write_text(json.dumps(config))
# Initial untracked tests: independently repeated cat output agrees byte-for-byte.
s=CS[25]['stdout'];cut=s.index('\nimport ',s.index('describe('))+1
policy,router=s[:cut],s[cut:];alltests=CS[103]['stdout'];assert alltests.endswith(router+policy);provider=alltests[:-len(router+policy)]
assert provider in CS[11]['stdout'];assert CS[26]['stdout']==CS[102]['stdout']==CS[110]['stdout']
current={'source':'main+independent_code_quality_review','source_lines':[54,134,141,34,35,63]}
for p,s in [('policy/useAppPolicy-network.test.ts',policy),('services/offline-prep/router-network.test.ts',router),('services/sync/provider-network.test.tsx',provider),('store/network.test.ts',CS[26]['stdout'])]:save('apps/client/tests/shared/'+p,s,'repeated-initial-cat')
# Store copy at worker dispatch, before the first mutation.
base=B/'before';base.mkdir(exist_ok=True)
events=[]
for i,c in enumerate(CS):events.append((c['timestamp'],0,'cmd',i,c))
for p in PS:events.append((p['timestamp'],1,'patch',None,p))
for s in SS:events.append((s['timestamp'],2,'observation',None,s))
base_done=False
for when,_,kind,idx,e in sorted(events,key=lambda x:(x[0],x[1])):
 current={'source':e['source'],'source_line':e.get('line',e.get('source_line')),'timestamp':when}
 if not base_done and when>='2026-09-17T02:55:08.836Z':
  for p in R.rglob('*'):
   if p.is_file():d=base/p.relative_to(R);d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(p.read_bytes())
  base_done=True
 if kind=='observation':
  p=e['path'];data=(B/e['snapshot']).read_bytes()
  if path(p).exists():observations.append({**current,'path':p,'matches_replay':path(p).read_bytes()==data})
  save(p,data,'git-diff-hash-verified-observation');continue
 if kind=='patch':
  for p,ch in e['item']['changes'].items():
   if not str(p).startswith(N+'/apps/'):continue
   if ch['type']=='add':save(p,ch['content'],'recorded-file-add');continue
   if ch['type']=='update':
    try:
     dest=ensure(p);before=dest.read_bytes();rel=str(dest.relative_to(R));patch='--- a/'+rel+'\n+++ b/'+rel+'\n'+ch['unified_diff']
     proc=subprocess.run(['patch','--silent','--forward','-p1','-d',str(R)],input=patch.encode(),capture_output=True)
     if proc.returncode:dest.write_bytes(before);raise ValueError(proc.stdout.decode()+proc.stderr.decode())
     trace[rel].append({**current,'kind':'recorded-file-update'})
    except Exception as ex:issues.append({**current,'path':p,'kind':'patch-error','detail':str(ex)[:200]})
  continue
 if e['source']=='/root/independent_code_quality_review':continue
 cmd=e['command'][-1]
 if e['source']=='main' and not any(t in cmd for t in ['apps/','apply_patch']):continue
 # Only extract literal heredoc files and constrained Python text transformations.
 matches=[]
 for m in re.finditer(r"cat\s*(>>?)\s*(\S+)\s*<<['\"]?(\w+)['\"]?\n([\s\S]*?)\n\3(?:\n|$)",cmd):matches.append((m.start(),'cat',m))
 for m in re.finditer(r"python3?[^\n]*<<['\"]?(\w+)['\"]?\n([\s\S]*?)\n\1(?:\n|$)",cmd):matches.append((m.start(),'python',m))
 for _,typ,m in sorted(matches):
  try:
   if typ=='cat':
    if m[2]=='/tmp/noline-policy-ui-edit.py' and 'python3 /tmp/noline-policy-ui-edit.py' in cmd:
     run_python(m[4])
    elif m[2].startswith('apps/'):
     data=m[4]+'\n'
     if m[1]=='>>':data=ensure(m[2]).read_text()+data
     save(m[2],data,'recorded-heredoc')
   elif 'write' in m[2] and 'apps/' in m[2] and 'subprocess' not in m[2]:
    if idx==215:
     run_python(m[2][m[2].index("p=Path('apps/client/tests/entities/repository-routing.test.ts')"):])
    else:run_python(m[2])
  except Exception as ex:issues.append({**current,'command_index':idx,'kind':'transform-error','detail':str(ex)[:200]})
 for line in cmd.splitlines():
  if re.match(r'^(?:node |\.\./|node_modules)',line) and 'prettier' in line and '--write' in line:
   tokens=shlex.split(line);format_files(tokens[tokens.index('--write')+1:])
# discard patch backup/reject artifacts; they are not reconstructed sources
for p in R.rglob('*'):
 if p.suffix in ('.orig','.rej'):p.unlink()
(B/'replay-trace.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n');(B/'replay-issues.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2)+'\n');(B/'observation-checks.json').write_text(json.dumps(observations,ensure_ascii=False,indent=2)+'\n')
print('reconstructed',sum(p.is_file() for p in R.rglob('*')),'issues',len(issues),'observations',len(observations),'matches',sum(x['matches_replay'] for x in observations))
for x in issues:print(x)
