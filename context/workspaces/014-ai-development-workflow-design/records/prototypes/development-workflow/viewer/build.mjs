import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath, pathToFileURL} from 'node:url';

const viewerDirectory = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(viewerDirectory);

async function loadMarked() {
  const configuredModule = process.env.MARKED_MODULE;
  if (configuredModule) {
    const moduleUrl = configuredModule.startsWith('file:')
      ? configuredModule
      : pathToFileURL(path.resolve(configuredModule)).href;
    return import(moduleUrl);
  }
  try { return await import('marked'); }
  catch (error) {
    throw new Error('설치된 marked를 찾지 못했습니다. MARKED_MODULE에 로컬 marked 모듈 파일 경로를 지정해 다시 실행하세요.', {cause: error});
  }
}

const {Marked} = await loadMarked();
const personalRoot = 'noline-demo/context/personal/';
const namingRoot = personalRoot + 'development/naming-and-completion/';
const personal = namingRoot + 'index.md';
const personalCases = namingRoot + 'index.cases.md';
const personalCommon = personalRoot + 'development/index.md';
const workflow = 'noline-demo/context/work/DEVELOPMENT.md';
const project = 'noline-demo/context/project/';
const work = 'noline-demo/context/work/workspaces/001-login-completion-names/';
const namingComparison = work + 'records/2026-10-19-06-naming-alternatives.md';
const escapeHtml = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const slug = text => text.toLowerCase().replace(/[^\p{L}\p{N}_\s-]/gu, '').trim().replace(/\s+/g, '-');

function sourceFiles(directory) {
  return fs.readdirSync(directory, {withFileTypes: true}).flatMap(entry => {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      return fullPath === viewerDirectory ? [] : sourceFiles(fullPath);
    }
    if (!entry.isFile()) { return []; }
    const relativePath = path.relative(root, fullPath).split(path.sep).join('/');
    const isDocument = entry.name.endsWith('.md');
    const isDemoCode = /^noline-demo\/examples\/authentication\/(?:src|tests)\/.+\.mjs$/.test(relativePath);
    return isDocument || isDemoCode ? [fullPath] : [];
  });
}

function renderMarkdown(content) {
  const headingCounts = new Map();
  const renderer = {
    html({text}) { return escapeHtml(text); },
    heading({tokens, depth, text}) {
      const base = slug(text);
      const count = headingCounts.get(base) || 0;
      headingCounts.set(base, count + 1);
      const id = count ? `${base}-${count}` : base;
      return `<h${depth} id="${escapeHtml(id)}">${this.parser.parseInline(tokens)}</h${depth}>\n`;
    },
    image({text, href}) {
      return `<span title="${escapeHtml(href)}">${escapeHtml(text || '이미지 참조')}</span>`;
    },
  };
  return new Marked({renderer, gfm: true, breaks: false}).parse(content);
}

const labels = {
  'README.md': '개발 판단 · 읽기와 실행 시작점',
  'noline-demo/context/README.md': 'Context · Personal·Project·Work',
  [personalRoot + 'README.md']: 'Personal 입구 · 적용할 기준 선택',
  [personalRoot + 'development/README.md']: '개발 기준 입구 · 주제 선택과 관리',
  [personalCommon]: '짧은 개발 공통 · 조건별 적용',
  [namingRoot + 'README.md']: '이름 기준 묶음 · 구성과 읽기 안내',
  [personal]: '일반 기준 · 이름·책임·완료',
  [namingRoot + 'background/README.md']: '형성 자료 입구 · 질문별 읽기 안내',
  [namingRoot + 'background/context.md']: '형성 맥락 · 목적과 선택 이유',
  [namingRoot + 'background/evidence.md']: '근거 발췌 · 당시 발화와 확인 범위',
  [personalCases]: '상세 사례 · 같은 코드의 선택 비교',
  [workflow]: 'Workflow · 입력 선택과 전달·갱신',
  [project + 'README.md']: 'Project 입구 · 담당 본문 선택',
  [project + 'current/authentication-flow.md']: '작업 후 · 인증 흐름 현황',
  [work + 'records/2026-10-19-01-input-selection.md']: '이번 Work에서 실제 선택한 입력',
  [work + 'records/2026-10-19-03-execution.md']: '로컬 실행 결과와 확인 범위',
  [work + 'records/2026-10-19-04-review.md']: '실물 검토 결과와 미확인',
  [work + 'source/scenario-input.md']: '작업 전 · 코드와 사용처',
  [namingComparison]: '같은 코드 · 이름 유지와 개명 비교',
  'walkthrough.md': '적용 해설 · 초기 조건 재구성과 현재 결과',
};

const documents = sourceFiles(root).map(fullPath => {
  const relativePath = path.relative(root, fullPath).split(path.sep).join('/');
  const content = fs.readFileSync(fullPath, 'utf8');
  const kind = relativePath.endsWith('.md') ? 'markdown' : 'code';
  const isTest = relativePath.startsWith('noline-demo/examples/authentication/tests/');
  const title = kind === 'markdown'
    ? content.match(/^#\s+(.+)$/m)?.[1] || path.basename(fullPath)
    : `${isTest ? '검사 코드' : '데모 소스'} · ${path.basename(fullPath)}`;
  const group = kind === 'code' ? isTest ? '로컬 데모 · 검사 코드' : '로컬 데모 · 구현 코드'
    : relativePath.startsWith(personalRoot) ? 'Personal · 개인의 기준'
    : relativePath.includes('/context/work/') ? '이번 Work · 요구와 근거'
    : relativePath.startsWith('noline-demo/') ? 'Project · 제품의 계약'
    : '전체 안내와 적용 장면';
  const rendered = kind === 'markdown'
    ? renderMarkdown(content)
    : `<p class="code-notice">실제 파일의 전체 코드입니다. 이 화면에서는 읽기만 하며 실행 방법과 확인 범위는 prototype README 및 Work 기록에서 찾습니다.</p><pre><code>${escapeHtml(content)}</code></pre>`;
  return {
    path: relativePath, title, label: labels[relativePath], group, kind,
    content, html: rendered, sha256: crypto.createHash('sha256').update(content).digest('hex'),
  };
});
const documentPaths = new Set(documents.map(doc => doc.path));
const demoSources = documents.filter(doc => doc.path.startsWith('noline-demo/examples/authentication/src/')).map(doc => doc.path);
const demoTests = documents.filter(doc => doc.path.startsWith('noline-demo/examples/authentication/tests/')).map(doc => doc.path);

const stages = [
  {label: 'Context와 작업', title: '1. 한 프로젝트 안의 Context와 Work', description: '같은 context 안에 Personal·Project·Work를 두고, 이번 작업의 Spec·Ticket·현재 상태를 찾습니다.', documents: ['noline-demo/context/README.md', work + 'README.md', work + 'current/memory/index.md', work + 'current/memory/spec/01-problem-goal-scope.md', work + 'current/memory/tickets/01-authentication-completion.md', work + 'source/scenario-input.md', 'README.md']},
  {label: '필요 본문 선택', title: '2. Work에서 Personal과 Project를 선택', description: '일반 기준을 읽고 판단 차이가 필요할 때 상세 사례를 고릅니다. 현재 읽기 경로이며 최초 전달 판본의 복원본은 아닙니다.', documents: [workflow, work + 'current/memory/personal-context.md', work + 'current/memory/project-context.md', personalRoot + 'README.md', personalCommon, personal, personalCases, project + 'README.md', project + 'guidance/code-readability.md']},
  {label: '대안·계약 판단', title: '3. 초기 판단 조건과 대안을 재구성해 읽음', description: '보존된 시작 입력으로 판단 조건을 풀고 현재 기준과 대조한 해설입니다. 새 작업자가 독립적으로 적용한 실험은 아닙니다.', documents: ['walkthrough.md', work + 'source/scenario-input.md', personal, personalCases, project + 'guidance/authentication-and-session.md']},
  {label: '구현과 결과', title: '4. Output에서 실제 구현을 찾음', description: '선택 후 이름·코드는 결과로 읽습니다. 당시 작성 기록과 현재 보완된 선택 이유를 구별합니다.', documents: [work + 'output/index.md', work + 'current/memory/spec/05-constraints-design-assumptions.md', project + 'current/authentication-flow.md', work + 'records/2026-10-19-02-implementation.md', ...demoSources]},
  {label: '검토와 검사', title: '5. 실제 수행과 한계를 구별', description: '현재 실행 방법과 당시 검사·검토 결과에서 확인한 경계와 남은 조건을 구별합니다.', documents: ['noline-demo/README.md', work + 'current/memory/spec/04-quality-and-completion.md', work + 'records/2026-10-19-03-execution.md', work + 'records/2026-10-19-04-review.md', ...demoTests]},
  {label: '현재와 다음', title: '6. 같은 구조에서 다음 변경을 이어감', description: '현재 상태와 결과 위치를 확인하고, 개인 기준·제품 계약·작업 상태 중 달라진 Owner를 갱신합니다.', documents: [work + 'current/state/index.md', work + 'output/index.md', project + 'current/authentication-flow.md', project + 'MAINTENANCE.md', personalRoot + 'README.md', workflow]},
];
const comparison = [
  {label: 'Personal 기준', path: personal},
  {label: 'Project 가이드', path: project + 'guidance/code-readability.md'},
  {label: 'Workflow 연결', path: workflow},
];
for (const stage of stages) {
  for (const relativePath of stage.documents) {
    if (!documentPaths.has(relativePath)) { throw new Error(`아직 없는 단계 본문: ${relativePath}`); }
  }
}
for (const document of comparison) {
  if (!documentPaths.has(document.path)) { throw new Error(`아직 없는 비교 본문: ${document.path}`); }
}
if (!demoSources.length || !demoTests.length) { throw new Error('표시할 데모 소스와 검사 코드가 모두 필요합니다.'); }

if (!documentPaths.has(namingComparison)) { throw new Error('이름 대안 비교 본문이 없습니다.'); }
const payload = JSON.stringify({documents, stages, comparison, namingComparison}).replaceAll('<', '\\u003c').replaceAll('\u2028', '\\u2028').replaceAll('\u2029', '\\u2029');
const shell = fs.readFileSync(path.join(viewerDirectory, 'shell.html'), 'utf8');
const html = shell.replace('__DATA__', payload);
fs.writeFileSync(path.join(root, 'viewer.html'), html);
console.log(JSON.stringify({file: path.join(root, 'viewer.html'), documents: documents.filter(doc => doc.kind === 'markdown').length, codeFiles: documents.filter(doc => doc.kind === 'code').length, bytes: Buffer.byteLength(html)}, null, 2));
