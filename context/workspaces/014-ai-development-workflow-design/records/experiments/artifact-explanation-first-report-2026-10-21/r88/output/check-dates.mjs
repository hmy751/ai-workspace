import assert from 'node:assert/strict';
import {getUTCDateRange, formatISOToLocalDate} from '../repository/apps/client/src/shared/lib/datetime.ts';
const start='2026-09-29T15:00:00Z', end='2026-10-01T15:00:00Z';
const results=[];
for(const zone of ['Asia/Seoul','UTC','America/Los_Angeles']) {
 process.env.TZ=zone;
 const range=getUTCDateRange(start,end);
 assert.deepEqual(range,['2026-09-29','2026-09-30','2026-10-01']);
 const home=[formatISOToLocalDate(start),formatISOToLocalDate(end)];
 assert.deepEqual(home,zone==='Asia/Seoul'?['2026-09-30','2026-10-02']:['2026-09-29','2026-10-01']);
 const scheduleDate=formatISOToLocalDate('2026-10-02T03:00:00Z');
 results.push({zone,input:{start,end,scheduledAt:'2026-10-02T03:00:00Z'},home,range,scheduleDate,scheduleIncluded:range.includes(scheduleDate)});
}
console.log(JSON.stringify({kind:'synthetic-fixture',runtime:process.version,checks:'6 assertions passed',results},null,2));
