// 실제 사본의 React 컴포넌트·Zustand store를 JSDOM과 가상 시간으로 확인한다.
// 실행: node verify-runtime.cjs <임시 의존성 설치 폴더>
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const assert = require('node:assert/strict');

const dependencies = process.argv[2] || '/tmp/rea-toast-runtime';
const dependencyRequire = Module.createRequire(path.join(dependencies, 'package.json'));
const ts = dependencyRequire('typescript');
const { JSDOM } = dependencyRequire('jsdom');
const FakeTimers = dependencyRequire('@sinonjs/fake-timers');
const input = path.join(__dirname, 'input');
const receipt = path.resolve(__dirname, '../../receipts/rea-toast-20261015/runtime-results.json');

// 입력 파일은 수정하지 않고 메모리에서 변환한다. 외부 패키지만 고정된 임시 설치로 연결한다.
for (const extension of ['.ts', '.tsx']) {
  require.extensions[extension] = (module, filename) => {
    const source = fs.readFileSync(filename, 'utf8');
    const compiled = ts.transpileModule(source, {
      fileName: filename,
      compilerOptions: {
        target: ts.ScriptTarget.ES2022,
        module: ts.ModuleKind.CommonJS,
        jsx: ts.JsxEmit.ReactJSX,
        esModuleInterop: true,
      },
    });
    const localRequire = module.require.bind(module);
    module.require = (request) => request.startsWith('.') || path.isAbsolute(request)
      ? localRequire(request)
      : dependencyRequire(request);
    module._compile(compiled.outputText, filename);
  };
}
// CSS는 레이아웃 검증 범위 밖이다. class 이름만 보존한다.
require.extensions['.css'] = (module) => {
  module.exports = new Proxy({}, { get: (_, name) => name === '__esModule' ? false : String(name) });
};

const dom = new JSDOM('<!doctype html><html><body></body></html>', { url: 'http://localhost' });
global.window = dom.window;
global.document = dom.window.document;
global.HTMLElement = dom.window.HTMLElement;
global.IS_REACT_ACT_ENVIRONMENT = true;
const React = dependencyRequire('react');
const { createRoot } = dependencyRequire('react-dom/client');
const { act } = React;
const Toast = require(path.join(input, 'src/component/Toast/index.tsx')).default;
const story = require(path.join(input, 'src/component/Toast/index.stories.tsx'));
const store = require(path.join(input, 'src/store/useToastStore.ts')).default;
const clock = FakeTimers.install({ toFake: ['setTimeout', 'clearTimeout'] });
const results = [];
let root;
let host;
let checkpoints;

async function mount(element = React.createElement(Toast)) {
  host = document.createElement('div');
  document.body.appendChild(host);
  root = createRoot(host);
  await act(async () => root.render(element));
}
async function unmount() {
  if (root) {
    await act(async () => root.unmount());
    root = null;
    host.remove();
  }
}
async function tick(ms) { await act(async () => clock.tick(ms)); }
async function add(data) { await act(async () => store.getState().addToast(data)); }
function observe(label, expectedCount, expectedText) {
  const observation = {
    label, virtual_time_ms: clock.now,
    store_count: store.getState().toasts.length,
    body_text: document.body.textContent,
  };
  assert.equal(observation.store_count, expectedCount, label);
  if (expectedText !== undefined) assert.equal(observation.body_text.includes('Toast Title'), expectedText, label);
  checkpoints.push(observation);
}
async function scenario(name, fn) {
  await unmount();
  store.setState({ toasts: [] });
  clock.reset();
  checkpoints = [];
  try {
    await fn();
    results.push({ name, passed: true, checkpoints });
  } catch (error) {
    results.push({ name, passed: false, message: error.message, checkpoints });
    throw error;
  }
}

(async () => {
  try {
    await scenario('story-button-expiry-3000ms', async () => {
      await mount(story.Primary.render());
      await act(async () => document.querySelector('button').dispatchEvent(new window.MouseEvent('click', { bubbles: true })));
      observe('click adds and displays', 1, true);
      await tick(2999); observe('before duration', 1, true);
      await tick(1); observe('at duration', 0, false);
    });
    await scenario('default-duration-5000ms', async () => {
      await mount(); await add({ title: 'Toast Title' });
      await tick(4999); observe('before default duration', 1, true);
      await tick(1); observe('at default duration', 0, false);
    });
    await scenario('unmount-preserves-state-remount-restarts-full-duration', async () => {
      await mount(); await add({ title: 'Toast Title', duration: 3000 });
      await tick(1000); await unmount(); observe('unmounted after 1000ms', 1, false);
      await tick(10000); observe('unmounted beyond original deadline', 1, false);
      await mount(); observe('remounted', 1, true);
      await tick(2999); observe('2999ms after remount', 1, true);
      await tick(1); observe('3000ms after remount', 0, false);
    });
    await scenario('add-without-presenter-does-not-expire-until-mounted', async () => {
      await add({ title: 'Toast Title', duration: 3000 });
      await tick(10000); observe('10000ms without presenter', 1, false);
      await mount(); observe('presenter mounted', 1, true);
      await tick(3000); observe('3000ms after presenter mounted', 0, false);
    });
  } finally {
    await unmount();
    clock.uninstall();
    dom.window.close();
    const versions = Object.fromEntries(['react', 'react-dom', 'zustand', 'typescript', 'jsdom', '@sinonjs/fake-timers'].map((name) => [name, dependencyRequire(name + '/package.json').version]));
    const result = {
      recorded_at: new Date().toISOString(), node: process.version, versions,
      scope: 'Original source snapshots, real React/Zustand, JSDOM DOM, fake timers, CSS stub; no browser visual acceptance.',
      passed: results.length === 4 && results.every((entry) => entry.passed), scenarios: results,
    };
    fs.writeFileSync(receipt, JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify(result, null, 2));
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
