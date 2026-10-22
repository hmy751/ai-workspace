function getUTCDateRange(startISO, endISO) {
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

  return dates;
}
const input = { start: '2026-09-29T15:00:00Z', end: '2026-10-01T15:00:00Z' };
function home(value) { const date = new Date(value); return `${date.getMonth()+1}월 ${date.getDate()}일`; }
const result = { timezone: process.env.TZ, input, home: [home(input.start), home(input.end)], list: getUTCDateRange(input.start,input.end), dst: getUTCDateRange('2026-03-07T00:00:00Z','2026-03-10T00:00:00Z') };
if(result.list.join(',') !== '2026-09-29,2026-09-30,2026-10-01') throw new Error('range mismatch');
if(result.dst.length !== 4) throw new Error('DST range mismatch');
console.log(JSON.stringify(result));
