'use strict';
// markdown 渲染器回归测试（纯 Node，无需浏览器/服务器）
// 运行：node test_markdown.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

// 最小 DOM/浏览器 stub，让 app.js 能在 Node 中加载
const el = () => ({ textContent: '', innerHTML: '', onclick: null, oninput: null, hidden: false,
  addEventListener() {}, appendChild() {}, style: {} });
global.window = { addEventListener() {}, matchMedia: () => ({ matches: false }) };
global.addEventListener = () => {};
global.document = { getElementById: el, addEventListener() {}, documentElement: { dataset: {} },
  querySelectorAll: () => [] };
global.localStorage = { getItem: () => null, setItem() {} };
global.location = { hash: '' };
global.getSelection = () => null;
global.fetch = () => Promise.reject(new Error('offline'));

const source = fs.readFileSync(path.join(__dirname, 'public', 'app.js'), 'utf8');
eval(source + ';global.__exports = { markdown, inline };');
const { markdown } = global.__exports;

let passed = 0;
function t(name, fn) { fn(); passed++; console.log('ok  ' + name); }

t('标题与段落', () => {
  const html = markdown('# Title\n\nparagraph **bold**', 'book/08-frames/');
  assert.ok(html.includes('<h1>Title</h1>'));
  assert.ok(html.includes('<p>paragraph <strong>bold</strong></p>'));
});

t('单行引用', () => {
  const html = markdown('> Ron sighed as though resigned to the worst.', '');
  assert.equal(html, '<blockquote><p>Ron sighed as though resigned to the worst.</p></blockquote>');
});

t('连续多行引用合并为一个 blockquote', () => {
  const html = markdown('> first line\n> second line\n\nnext paragraph', '');
  assert.equal((html.match(/<blockquote>/g) || []).length, 1);
  assert.ok(html.includes('<p>first line</p>'));
  assert.ok(html.includes('<p>second line</p>'));
  assert.ok(html.endsWith('<p>next paragraph</p>'));
});

t('空行分隔的两个引用块', () => {
  const html = markdown('> a\n\n> b', '');
  assert.equal((html.match(/<blockquote>/g) || []).length, 2);
});

t('GFM 表格渲染', () => {
  const md = '| 框架 | 语义 |\n|---|---|\n| let alone | 更不用说 |\n| if anything | 甚至可以说 |';
  const html = markdown(md, '');
  assert.ok(html.includes('<table><thead>'));
  assert.ok(html.includes('<th>框架</th>'));
  assert.ok(html.includes('<td>let alone</td>'));
  assert.equal((html.match(/<tbody>/g) || []).length, 1);
  assert.ok(!html.includes('---')); // 分隔行被吃掉
});

t('表格单元格支持行内格式与相对链接', () => {
  const md = '| A | B |\n|---|---|\n| **bold** | [guide](00-guide.md) |';
  const html = markdown(md, 'book/08-frames/');
  assert.ok(html.includes('<td><strong>bold</strong></td>'));
  assert.ok(html.includes(`<a href="#${encodeURIComponent('学习章节/句式与结构/句式骨架（Frames）：比语法分析高一层的学习单位.md')}">guide</a>`));
});

t('表格与前后段落边界', () => {
  const html = markdown('intro\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\noutro', '');
  assert.ok(html.startsWith('<p>intro</p>'));
  assert.ok(html.endsWith('<p>outro</p>'));
  assert.ok(html.includes('<td>1</td>'));
});

t('列表在表格前后正确闭合', () => {
  const html = markdown('- item\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n- item2', '');
  assert.ok(html.includes('<ul><li>item</li></ul>'));
  assert.equal((html.match(/<ul>/g) || []).length, 2);
});

t('代码块内容不转义解析', () => {
  const html = markdown('```\n> not a quote\n| not | table |\n```', '');
  assert.ok(html.includes('<pre><code>&gt; not a quote\n| not | table |</code></pre>'));
  assert.ok(!html.includes('<blockquote>'));
});

t('引用内链接不破坏结构', () => {
  const html = markdown('> see [guide](00-guide.md) here', 'book/08-frames/');
  assert.ok(html.includes('<blockquote><p>see <a href="#'));
});

console.log(`\n${passed} 项全部通过`);
