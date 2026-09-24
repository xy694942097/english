// Run with PLAYWRIGHT_MODULE set to a local Playwright installation if needed.
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const base = (process.env.ENGLISH_TEST_URL || 'http://127.0.0.1:4174') + '/';

    // 打开即第一份文档（nav.json 第一项），marked 渲染出标题
    await page.goto(base);
    await page.getByRole('heading', {name: '从 resigned 理解词义与搭配', exact: true}).waitFor();
    assert.ok((await page.locator('#article h2').count()) > 0, 'marked 渲染出章节小节');
    assert.equal(await page.locator('#nav details').count(), 8, '八个导航分组');
    assert.equal(await page.locator('#nav a.nav-link').count(), 57, '57 个登记文档');
    // 当前文档所在分组展开并高亮
    assert.ok(await page.locator('#nav > details[open] a.active').count() > 0, '当前文档分组展开且高亮');

    // 深链 + 参考答案折叠
    await page.goto(base + '#' + encodeURIComponent('book/05-patterns/01-nothing-but.md'));
    await page.getByRole('heading', {name: 'nothing but：几个小词，意思为什么差这么多', exact: true}).waitFor();
    assert.equal(await page.locator('#article details').getAttribute('open'), null, '参考答案默认折叠');
    await page.locator('#article summary').click();
    assert.notEqual(await page.locator('#article details').getAttribute('open'), null);

    // 文内相对 .md 链接改写为 hash 深链（句式骨架总集含 ../05-patterns/ 链接）
    await page.goto(base + '#' + encodeURIComponent('book/08-frames/08-frames-collection.md'));
    await page.getByRole('heading', {name: '句式骨架总集：六大家族与教材回收', exact: true}).waitFor();
    const relLink = await page.locator('#article a[href^="#book%2F"]').count();
    assert.ok(relLink > 0, '文档间相对链接改写为站内深链');

    // 搜索
    await page.locator('#search').fill('qualified support');
    const hit = page.locator('.search-result').first();
    await hit.waitFor();
    assert.ok((await page.locator('.search-result').count()) > 0, '关键词搜索出结果');
    await hit.click();
    await page.locator('#article h1').first().waitFor();

    // 主题切换
    const before = await page.evaluate(() => document.documentElement.dataset.theme || '');
    await page.locator('#theme').click();
    const after = await page.evaluate(() => document.documentElement.dataset.theme || '');
    assert.notEqual(before, after, '主题切换生效');
    await page.evaluate(() => localStorage.removeItem('english-theme'));

    // /files/ 路由：仓库内文件可取，路径穿越被拒
    const ok = await page.evaluate(() => fetch('/files/nav.json').then(r => r.status));
    const blocked = await page.evaluate(() => fetch('/files/%2e%2e/%2e%2e/etc/passwd').then(r => r.status).catch(() => 0));
    assert.equal(ok, 200, '/files/ 提供仓库内文件');
    assert.equal(blocked, 404, '/files/ 路径穿越被拒');

    // 移动端无横向溢出
    await page.setViewportSize({width: 390, height: 844});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);

    assert.deepEqual(errors, []);
    console.log('PASS: first doc, marked render, nav groups/folds, answer fold, md links, search, theme, /files/, mobile width; no page errors.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
