import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {fileURLToPath, pathToFileURL} from 'node:url';

const viewerDirectory = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(viewerDirectory);
const outputFile = path.join(root, 'viewer.html');
const html = fs.readFileSync(outputFile, 'utf8');
const dataBlock = html.match(/<script type="application\/json" id="viewer-data">([\s\S]*?)<\/script>/);
assert.ok(dataBlock, '표시할 파일 목록이 없습니다.');
const data = JSON.parse(dataBlock[1]);
const sourceHash = content => crypto.createHash('sha256').update(content).digest('hex');
const escapeHtml = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const slug = text => text.toLowerCase().replace(/[^\p{L}\p{N}_\s-]/gu, '').trim().replace(/\s+/g, '-');

function expectedFiles(directory) {
  return fs.readdirSync(directory, {withFileTypes: true}).flatMap(entry => {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) { return fullPath === viewerDirectory ? [] : expectedFiles(fullPath); }
    if (!entry.isFile()) { return []; }
    const relativePath = path.relative(root, fullPath).split(path.sep).join('/');
    return relativePath.endsWith('.md') || /^noline-demo\/examples\/authentication\/(?:src|tests)\/.+\.mjs$/.test(relativePath)
      ? [relativePath] : [];
  });
}

assert.deepEqual(data.documents.map(doc => doc.path).sort(), expectedFiles(root).sort());
for (const doc of data.documents) {
  const source = fs.readFileSync(path.join(root, doc.path), 'utf8');
  assert.equal(doc.content, source, `${doc.path} 본문이 갱신되지 않았습니다.`);
  assert.equal(doc.sha256, sourceHash(source), `${doc.path} 해시가 다릅니다.`);
  if (doc.kind === 'code') {
    assert.ok(doc.html.includes(`<code>${escapeHtml(source)}</code>`), `${doc.path} 전체 코드 표시가 다릅니다.`);
  }
}
const documents = new Map(data.documents.map(doc => [doc.path, doc]));
for (const stage of data.stages) {
  for (const documentPath of stage.documents) { assert.ok(documents.has(documentPath), documentPath); }
}
assert.equal(data.comparison.length, 3);
for (const entry of data.comparison) { assert.equal(documents.get(entry.path)?.kind, 'markdown', entry.path); }
const namingDocument = documents.get(data.namingComparison);
assert.equal(namingDocument?.kind, 'markdown', '이름 비교의 원문이 없습니다.');
const namingBlocks = [...namingDocument.content.matchAll(/```js\n([\s\S]*?)\n```/g)].map(match => match[1]);
assert.equal(namingBlocks.length, 2, '같은 동작의 A·B 코드가 필요합니다.');
for (const block of namingBlocks) { new vm.Script(block); }
assert.equal(
  namingBlocks[0].replaceAll('loginAndRefresh', 'signInAndRequestRefresh').replaceAll('onCompleted', 'onSignedIn'),
  namingBlocks[1],
  '이름 외에 주석이나 동작도 달라졌습니다. 비교 조건을 다시 확인하세요.',
);
for (const heading of ['A — 이름 유지와 설명 보완', 'B — 개명과 설명 보완']) {
  assert.ok(namingDocument.html.includes(`>${heading}</h2>`), `비교 열 제목이 없습니다: ${heading}`);
}
assert.ok(data.documents.some(doc => doc.path.startsWith('noline-demo/examples/authentication/src/')));
assert.ok(data.documents.some(doc => doc.path.startsWith('noline-demo/examples/authentication/tests/')));

const scripts = [...html.matchAll(/<script(?: [^>]*)?>([\s\S]*?)<\/script>/g)].map(match => match[1]);
const clientScript = scripts.at(-1);
new vm.Script(clientScript);
const helperStart = clientScript.indexOf('  function resolveDocumentLink(');
const helperEnd = clientScript.indexOf('  function showLinkedDocument(');
assert.ok(helperStart >= 0 && helperEnd > helperStart);
// DOM이나 브라우저를 만들지 않고 경로 계산과 링크 속성 설정만 검사한다.
const helpers = vm.runInNewContext(
  `${clientScript.slice(helperStart, helperEnd)}\n({resolveDocumentLink, configureReferenceLink})`,
  {documents, URL},
);
const viewerUrl = pathToFileURL(outputFile);
const problems = [];
let internalLinks = 0;
let referenceLinks = 0;
let anchorLinks = 0;
const documentLinks = new Map();

for (const doc of data.documents.filter(entry => entry.kind === 'markdown')) {
  for (const match of doc.html.matchAll(/href="([^"]+)"/g)) {
    const href = match[1].replaceAll('&amp;', '&');
    const resolved = helpers.resolveDocumentLink(doc.path, href);
    assert.ok(resolved, `${doc.path}에서 지원하지 않는 링크: ${href}`);
    const expected = new URL(href, pathToFileURL(path.join(root, doc.path)));
    if (resolved.kind === 'document') {
      internalLinks++;
      if (!documentLinks.has(doc.path)) { documentLinks.set(doc.path, new Set()); }
      documentLinks.get(doc.path).add(resolved.path);
      assert.equal(path.resolve(root, resolved.path), decodeURIComponent(expected.pathname));
      assert.equal(resolved.anchor, decodeURIComponent(expected.hash.slice(1)));
    } else {
      referenceLinks++;
      const actual = new URL(resolved.href, viewerUrl);
      assert.equal(actual.protocol, expected.protocol);
      assert.equal(decodeURIComponent(actual.pathname), decodeURIComponent(expected.pathname));
      assert.equal(actual.search, expected.search);
      assert.equal(decodeURIComponent(actual.hash), decodeURIComponent(expected.hash));
      const attributes = {};
      helpers.configureReferenceLink({
        setAttribute(name, value) { attributes[name] = value; },
        classList: {add() {}},
      }, resolved.href);
      assert.equal(attributes.href, resolved.href);
      assert.equal(attributes.target, '_blank');
      assert.equal(attributes.rel, 'noopener noreferrer');
    }
    if (expected.protocol !== 'file:') { continue; }
    const targetFile = decodeURIComponent(expected.pathname);
    const relativeFile = path.relative(root, targetFile);
    if (relativeFile === '..' || relativeFile.startsWith(`..${path.sep}`) || path.isAbsolute(relativeFile)) {
      problems.push(`${doc.path}: 대상물 밖 파일에 의존하는 링크 ${href}`);
      continue;
    }
    if (!fs.existsSync(targetFile)) { problems.push(`${doc.path}: 없는 파일 ${href}`); continue; }
    if (!expected.hash) { continue; }
    anchorLinks++;
    const relativeTarget = path.relative(root, targetFile).split(path.sep).join('/');
    const embedded = documents.get(relativeTarget);
    const targetText = embedded?.html || fs.readFileSync(targetFile, 'utf8');
    const ids = [...targetText.matchAll(/\bid=["']([^"']+)["']/g)].map(result => result[1]);
    if (!embedded && targetFile.endsWith('.md')) {
      ids.push(...[...targetText.matchAll(/^#{1,6}\s+(.+)$/gm)].map(result => slug(result[1])));
    }
    if (!ids.includes(decodeURIComponent(expected.hash.slice(1)))) {
      problems.push(`${doc.path}: 없는 앵커 ${href}`);
    }
  }
}
assert.deepEqual(problems, []);

// 이름 기준의 본문·형성 자료 입구와 왕복 연결을 확인한다. 의미 일치는 판정하지 않는다.
const personalRoot = 'noline-demo/context/personal/';
const namingRoot = personalRoot + 'development/naming-and-completion/';
const namingEntry = namingRoot + 'README.md';
const namingBody = namingRoot + 'index.md';
const namingCases = namingRoot + 'index.cases.md';
const namingBackground = namingRoot + 'background/README.md';
const namingContext = namingRoot + 'background/context.md';
const namingEvidence = namingRoot + 'background/evidence.md';
const requiredContextLinks = [
  [personalRoot + 'README.md', namingBackground],
  [namingEntry, namingBody],
  [namingEntry, namingCases],
  [namingEntry, namingBackground],
  [namingBody, namingCases],
  [namingBody, namingBackground],
  [namingCases, namingBody],
  [namingBackground, namingContext],
  [namingBackground, namingEvidence],
  [namingContext, namingBody],
  [namingContext, namingEvidence],
  [namingEvidence, namingContext],
];
for (const [from, to] of requiredContextLinks) {
  assert.ok(documents.has(from) && documents.has(to), `이름 기준의 구성 문서가 없습니다: ${from} → ${to}`);
  assert.ok(documentLinks.get(from)?.has(to), `이름 기준의 필수 연결이 없습니다: ${from} → ${to}`);
}

const sampleDocument = data.documents.find(doc => doc.kind === 'markdown').path;
const unsupported = [
  'javascript:alert(1)', 'data:text/html,test', 'vbscript:msgbox(1)',
  'mailto:test@example.com', 'ftp://example.com', '//example.com/x',
  '/absolute/path', 'java\nscript:alert(1)', '%2f%2fexample.com',
  'folder\\file.md', '#%E0%A4', 'https://[invalid',
];
for (const href of unsupported) { assert.equal(helpers.resolveDocumentLink(sampleDocument, href), null, href); }
assert.equal(/<script[^>]+src=|<link[^>]+href=/i.test(html), false);
assert.equal(/\bfetch\(/.test(clientScript), false);
const styles = [...html.matchAll(/<style>([\s\S]*?)<\/style>/g)].map(match => match[1]).join('\n');
assert.equal(/@import|url\(/i.test(styles), false);

console.log(JSON.stringify({
  documents: data.documents.filter(doc => doc.kind === 'markdown').length,
  codeFiles: data.documents.filter(doc => doc.kind === 'code').length,
  sourceContentAndSha: '현재 파일과 모두 일치',
  codeRendering: '전체 소스를 escape하여 읽기 전용 표시',
  stages: data.stages.length,
  comparisonColumns: data.comparison.length,
  namingAlternatives: '2개 코드가 이름 두 쌍 외에 주석 포함 동일',
  namingContextRelations: `${requiredContextLinks.length}개 필수 연결 확인 · 의미 일치는 별도 판단`,
  internalLinks, referenceLinks, anchorLinks,
  missingPathsOrAnchors: problems.length,
  localDocumentBoundary: '모든 로컬 링크가 prototype 안에 있음',
  rejectedLinkCases: unsupported.length,
  clientScriptSyntax: '통과',
  browserRendering: '실행하지 않음',
  demoTests: '이 검사에서는 실행하지 않음',
}, null, 2));
