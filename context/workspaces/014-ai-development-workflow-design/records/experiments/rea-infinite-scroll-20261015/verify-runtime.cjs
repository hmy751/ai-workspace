// 원본 사본을 실제 React/React Query로 실행한다. 서버·교차 감지만 통제한다.
// node verify-runtime.cjs /tmp/rea-infinite-runtime
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const assert = require('node:assert/strict');
const dep = Module.createRequire(path.join(process.argv[2] || '/tmp/rea-infinite-runtime', 'package.json'));
const ts = dep('typescript');
for (const ext of ['.ts', '.tsx']) {
  require.extensions[ext] = (module, filename) => {
    const compiled = ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
      fileName: filename,
      compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, esModuleInterop: true },
    });
    const local = module.require.bind(module);
    module.require = name => name.startsWith('.') || path.isAbsolute(name) ? local(name) : dep(name);
    module._compile(compiled.outputText, filename);
  };
}
require.extensions['.css'] = module => { module.exports = new Proxy({}, { get: (_, k) => k === '__esModule' ? false : String(k) }); };
const dom = new (dep('jsdom').JSDOM)('<!doctype html><html><body></body></html>', { url: 'http://localhost' });
global.window = dom.window; global.document = dom.window.document;
global.HTMLElement = dom.window.HTMLElement; global.IS_REACT_ACT_ENVIRONMENT = true;
const observers = [];
global.IntersectionObserver = class {
  constructor(callback, options) { this.callback = callback; this.options = options; this.targets = new Set(); observers.push(this); }
  observe(target) { this.targets.add(target); }
  unobserve(target) { this.targets.delete(target); }
  disconnect() { this.targets.clear(); }
  fire() { if (this.targets.size) this.callback([...this.targets].map(target => ({ target, isIntersecting: true }))); }
};
const React = dep('react'); const { act } = React;
const { createRoot } = dep('react-dom/client');
const { QueryClient, QueryClientProvider } = dep('@tanstack/react-query');
const Story = require('./input/src/component/InfiniteScrollContainer/index.stories.tsx').InfiniteScroll.render;
const clock = dep('@sinonjs/fake-timers').install({ toFake: ['setTimeout', 'clearTimeout'] });
let requests, root, host, client, failNextPages, checkpoints;
const results = [];
const originalFetch = global.fetch;
global.fetch = (url, options) => new Promise(resolve => {
  const item = { url, signal: options.signal, resolve, settled: false };
  requests.push(item);
  if (failNextPages && new URL(url).searchParams.get('skip') !== '0') respond(item, [], 500);
});
function respond(item, products, status = 200) {
  item.settled = true;
  item.resolve(new Response(JSON.stringify(status === 200 ? { products } : { message: 'test failure', code: 'TEST_ERROR' }), {
    status, headers: { 'Content-Type': 'application/json' },
  }));
}
const products = (start, count) => Array.from({ length: count }, (_, i) => ({ id: start + i, title: `Product ${start + i}`, thumbnail: 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==' }));
async function flush(ms = 5) { await act(async () => { await clock.tickAsync(ms); }); }
function active() { return observers.findLast(o => o.targets.size); }
function observe(label) {
  const q = client.getQueryState(['products']);
  const item = { label, time_ms: clock.now, requests: requests.map(r => ({ url: r.url, aborted: r.signal.aborted, settled: r.settled })),
    displayed_products: host.querySelectorAll('h3').length, text: host.textContent,
    query_status: q?.status, fetch_status: q?.fetchStatus,
    cached_products: q?.data?.pages.flat().length ?? 0, active_observers: observers.filter(o => o.targets.size).length };
  checkpoints.push(item); return item;
}
async function mount() {
  client = new QueryClient(); // preview.tsx와 동일: 재시도 옵션을 덮어쓰지 않는다.
  host = document.createElement('div'); document.body.append(host); root = createRoot(host);
  await act(async () => root.render(React.createElement(QueryClientProvider, { client }, React.createElement(Story))));
}
async function cleanup() {
  if (root) { await act(async () => root.unmount()); root = null; host.remove(); client.clear(); }
  observers.length = 0; clock.reset();
}
async function firstPage() { await mount(); await act(async () => respond(requests[0], products(1, 20))); await flush(); }
async function scenario(name, fn) {
  await cleanup(); requests = []; failNextPages = false; checkpoints = [];
  try { await fn(); results.push({ name, passed: true, checkpoints }); }
  catch (error) { results.push({ name, passed: false, error: error.message, checkpoints }); throw error; }
}
(async () => {
 try {
  await scenario('first-next-short-page-and-pending-guard', async () => {
    await mount(); assert.equal(requests.length, 1); assert.match(observe('initial pending').text, /Loading products/);
    await act(async () => respond(requests[0], products(1, 20))); await flush();
    assert.equal(observe('first page').displayed_products, 20);
    await act(async () => active().fire()); await flush();
    assert.equal(requests.length, 2); assert.match(requests[1].url, /skip=20&limit=20/);
    await act(async () => active().fire()); await flush();
    assert.equal(requests.length, 2); observe('repeat after pending render is suppressed');
    await act(async () => respond(requests[1], products(21, 5))); await flush();
    const end = observe('short page ends'); assert.equal(end.displayed_products, 25); assert.match(end.text, /모든 상품/); assert.equal(end.active_observers, 0);
  });
  await scenario('next-page-error-after-default-retries', async () => {
    await firstPage(); failNextPages = true;
    await act(async () => active().fire()); await flush(); observe('next page failure starts retry');
    await flush(7100); await flush();
    const failed = observe('retries exhausted'); assert.equal(requests.length, 5); assert.equal(failed.query_status, 'error');
    assert.equal(failed.cached_products, 20); assert.equal(failed.displayed_products, 0); assert.match(failed.text, /An error occurred/); assert.equal(failed.active_observers, 0);
  });
  await scenario('two-observer-callbacks-before-react-rerender', async () => {
    await firstPage(); const observer = active();
    await act(async () => { observer.fire(); observer.fire(); }); await flush();
    const pending = observe('two callbacks in same act');
    assert.equal(requests.length, 3); assert.equal(requests[1].url, requests[2].url);
    assert.equal(pending.requests[1].aborted, false);
    await act(async () => { respond(requests[1], products(21, 5)); respond(requests[2], products(21, 5)); }); await flush();
    assert.equal(observe('latest result shown without duplicate items').displayed_products, 25);
  });
  await scenario('exact-page-size-needs-empty-followup', async () => {
    await firstPage(); assert.ok(active());
    await act(async () => active().fire()); await flush();
    await act(async () => respond(requests[1], [])); await flush();
    const end = observe('empty followup ends after full first page'); assert.equal(requests.length, 2); assert.equal(end.displayed_products, 20); assert.match(end.text, /모든 상품/);
  });
 } finally {
  await cleanup(); clock.uninstall(); global.fetch = originalFetch; dom.window.close();
  const result = { recorded_at: new Date().toISOString(), node: process.version,
    versions: Object.fromEntries(['react','react-dom','@tanstack/react-query','typescript','jsdom','@sinonjs/fake-timers'].map(n => [n, dep(n+'/package.json').version])),
    scope: 'Original TS/TSX snapshot transpiled in memory; actual React/React Query; default QueryClient; mocked fetch and IntersectionObserver; JSDOM, fake timers, CSS stub. No real browser geometry, backend, visual acceptance or production build.',
    passed: results.length === 4 && results.every(r => r.passed), scenarios: results };
  fs.writeFileSync(path.resolve(__dirname, '../../receipts/rea-infinite-scroll-20261015/runtime-results.json'), JSON.stringify(result, null, 2)+'\n');
  console.log(JSON.stringify({ passed: result.passed, scenarios: results.map(r => ({ name:r.name, passed:r.passed, error:r.error, checkpoints:r.checkpoints.map(c => ({ label:c.label, requests:c.requests.length, displayed:c.displayed_products, cached:c.cached_products, status:c.query_status })) })) }, null, 2));
 }
})().catch(error => { console.error(error); process.exitCode = 1; });
