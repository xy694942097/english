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
    assert.equal(await page.locator('#nav details').count(), 13, '按教学角色整理的十三个导航分组');
    assert.equal(await page.locator('#nav a.nav-link').count(), 62, '62 个登记文档');
    const navText = await page.locator('#nav').innerText();
    assert.ok(navText.includes('表达练习') && navText.includes('查阅资料（待审校）'), '练习与查阅分区可见');
    assert.ok(!navText.includes('英语固定短语完全指南') && !navText.includes('雅思级别英语1000句 v2'), '隔离文档不在导航');
    // 当前文档所在分组展开并高亮
    assert.ok(await page.locator('#nav > details[open] a.active').count() > 0, '当前文档分组展开且高亮');

    // 新表达章可由深链打开，且练习答案仍保持折叠
    await page.goto(base + '#' + encodeURIComponent('book/10-expression/01-relationship-options.md'));
    await page.getByRole('heading', {name: '中文到英文表达：关系还有没有挽回余地', exact: true}).waitFor();
    assert.equal(await page.locator('#article details').getAttribute('open'), null, '表达章答案默认折叠');

    // 项目内 Skill 和学习计划在只读站点中可读
    await page.goto(base + '#' + encodeURIComponent('engineering/skills/translation-coach/PLAN.md'));
    await page.getByRole('heading', {name: '中文到英文表达训练计划', exact: true}).waitFor();

    await page.goto(base + '#' + encodeURIComponent('references/translation-training/pilot-001-prompts.md'));
    await page.getByRole('heading', {name: '中译英校准素材 P001：中文情境任务', exact: true}).waitFor();

    await page.goto(base + '#' + encodeURIComponent('references/chunks/INBOX.md'));
    await page.getByRole('heading', {name: 'Chunks 收集箱', exact: true}).waitFor();
    assert.equal(await page.locator('#article table').count(), 6, '六个分类各有一张收集表');
    assert.equal(await page.locator('#article table').first().locator('th').count(), 3, '收集表固定三列');

    await page.goto(base + '#' + encodeURIComponent('book/11-spoken-chunks/01-standup-conversation-moves.md'));
    await page.getByRole('heading', {name: '脱口秀口语 Chunks：把观察、反问和不确定说出来', exact: true}).waitFor();
    assert.equal(await page.locator('#article h2').filter({hasText: /^\d+\. /}).count(), 8, '脱口秀章展示八个知识点');
    assert.equal(await page.locator('#article details').getAttribute('open'), null, '脱口秀章答案默认折叠');

    // 深链 + 参考答案折叠
    await page.goto(base + '#' + encodeURIComponent('book/05-patterns/01-nothing-but.md'));
    await page.getByRole('heading', {name: 'nothing but：几个小词，意思为什么差这么多', exact: true}).waitFor();
    assert.equal(await page.locator('#article details').getAttribute('open'), null, '参考答案默认折叠');
    await page.locator('#article summary').click();
    assert.notEqual(await page.locator('#article details').getAttribute('open'), null);

    // 文内相对 .md 链接改写为 hash 深链（句式骨架导览含家族章链接）
    await page.goto(base + '#' + encodeURIComponent('book/08-frames/00-guide.md'));
    await page.getByRole('heading', {name: '句式骨架（Frames）：比语法分析高一层的学习单位', exact: true}).waitFor();
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
