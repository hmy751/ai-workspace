const fs = require('fs');
const cp = require('child_process');
const path = require('path');
if (!process.env.PROBE_TZ) {
  const results = ['UTC','Asia/Seoul','America/Los_Angeles'].map(tz => JSON.parse(cp.execFileSync(process.execPath,[__filename],{env:{...process.env,TZ:tz,PROBE_TZ:tz},encoding:'utf8'})));
  const out = {kind:'extracted-pure-function-probe', scope:'제품 UI·DB·Jest 실행 아님. 예시 입력으로 추출한 UTC 날짜 함수와 홈 포맷의 차이를 확인.',results};
  fs.writeFileSync(path.join(__dirname,'date-probe.json'),JSON.stringify(out,null,2));
  console.log(JSON.stringify(out,null,2));
} else {
  const root = path.resolve(__dirname,'../repository');
  const source = fs.readFileSync(path.join(root,'apps/client/src/shared/lib/datetime.ts'),'utf8');
  const match = source.match(/export function getUTCDateRange\(startISO: string, endISO: string\): string\[\] \{([\s\S]*?)\n\}/);
  if (!match) throw Error('Cannot extract range function');
  const range = new Function('startISO','endISO',match[1].replace('const dates: string[]','const dates'));
  const homeSource = fs.readFileSync(path.join(root,'apps/client/src/screens/HomeScreen/MainTripSection.tsx'),'utf8');
  const formatMatch = homeSource.match(/const formatDate = \(dateString: string \| null\) => \{([\s\S]*?)\n  \};/);
  if (!formatMatch) throw Error('Cannot extract home format');
  const home = new Function('dateString',formatMatch[1]);
  const cases = [
    ['offset-example','2026-09-30T00:00:00+09:00','2026-10-02T00:00:00+09:00'],
    ['UTC-midnight','2026-09-30T00:00:00Z','2026-10-02T00:00:00Z'],
    ['DST-boundary','2026-11-01T00:00:00Z','2026-11-03T00:00:00Z'],
  ].map(([name,start,end])=>({name,start,end,home:[home(start),home(end)],list:range(start,end)}));
  console.log(JSON.stringify({timezone:process.env.TZ,cases}));
}
