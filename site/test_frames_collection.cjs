'use strict';
// 总集文档渲染冒烟测试：node test_frames_collection.cjs
const fs = require('node:fs');
const path = require('node:path');
global.window = { addEventListener() {}, matchMedia: () => ({ matches: false }) };
global.addEventListener = () => {};
const el = () => ({ textContent: '', innerHTML: '', onclick: null, oninput: null, hidden: false,
  addEventListener() {}, appendChild() {}, style: {} });
global.document = { getElementById: el, addEventListener() {}, documentElement: { dataset: {} },
  querySelectorAll: () => [] };
global.localStorage = { getItem: () => null, setItem() {} };
global.location = { hash: '' };
global.getSelection = () => null;
global.fetch = () => Promise.reject(new Error('offline'));

const source = fs.readFileSync(path.join(__dirname, 'public', 'app.js'), 'utf8');
eval(source + ';global.__m = markdown;');
const html = global.__m(
  fs.readFileSync(path.join(__dirname, '..', 'book', '08-frames', '08-frames-collection.md'), 'utf8'),
  'book/08-frames/');

const count = re => (html.match(re) || []).length;
const assert = require('node:assert/strict');
assert.ok(count(/<h1>/g) === 9, '一级标题应为 9（总集+8章）');
assert.ok(count(/<table>/g) >= 10, '表格应≥10');
assert.ok(count(/<blockquote>/g) >= 30, '引用块应≥30');
assert.ok(count(/<pre>/g) >= 10, '代码块应≥10');
assert.ok(count(/<h3>/g) >= 45, '编号框架节应≥45');
assert.equal(count(/<p>\|/g), 0, '不应有裸竖线段落');
assert.equal(count(/<p>&gt; /g), 0, '不应有裸引用符号段落');
console.log('表格', count(/<table>/g), '| 引用块', count(/<blockquote>/g), '| 代码块', count(/<pre>/g),
  '| h1', count(/<h1>/g), '| h2', count(/<h2>/g));
console.log('总集渲染冒烟测试通过');
