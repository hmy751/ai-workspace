function range(startISO,endISO) {
  const current = new Date(startISO);
  const end = new Date(endISO);

  if (!Number.isFinite(current.getTime()) || !Number.isFinite(end.getTime())) return [];

  current.setUTCHours(0, 0, 0, 0);
  end.setUTCHours(0, 0, 0, 0);

  const dates = [];

  while (current <= end) {
    dates.push(current.toISOString().split('T')[0]);
    current.setUTCDate(current.getUTCDate() + 1);
  }

  return dates;}
const inputs=[['offset','2026-09-30T00:00:00+09:00','2026-10-02T00:00:00+09:00'],['utc','2026-09-30T00:00:00Z','2026-10-02T00:00:00Z']]; const results=[]; for(const zone of ['Asia/Seoul','UTC','America/Los_Angeles']) {process.env.TZ=zone;for(const [name,start,end] of inputs){const local=x=>{const d=new Date(x);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')};const dates=range(start,end), schedule=local('2026-10-02T09:00:00+09:00');results.push({zone,name,home:[local(start),local(end)],dates,schedule,inRange:dates.includes(schedule)});}} console.log(JSON.stringify(results,null,2));