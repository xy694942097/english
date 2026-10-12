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
    assert.equal(await page.locator('#nav .nav-fold').count(), 5, '五个学习导航分组');
    const registeredCount = (await (await page.request.get(base + 'api/catalog')).json()).items.length;
    assert.equal(await page.locator('#nav a.nav-link').count(), registeredCount, '登记文档均有导航入口');
    const navText = await page.locator('#nav').innerText();
    assert.ok(navText.includes('表达练习') && navText.includes('原文与参考资料'), '练习与查阅分区可见');
    assert.ok(!navText.includes('英语固定短语完全指南') && !navText.includes('雅思级别英语1000句 v2'), '隔离文档不在导航');
    // 当前文档所在分组展开并高亮
    assert.ok(await page.locator('#nav > details[open] a.active').count() > 0, '当前文档分组展开且高亮');

    // 点击编辑直接让现有正文块可改，取消后恢复原文。
    page.on('dialog', dialog => dialog.accept());
    await page.getByRole('button', {name:'编辑本文', exact:true}).click();
    assert.equal(await page.locator('#article').isVisible(), true);
    assert.ok(await page.locator('#article [contenteditable=true]').count() > 0, '正文直接可编辑');
    assert.equal(await page.locator('.sidebar').isVisible(), true, '编辑时保留导航');
    const originalText = await page.locator('#article p[data-md-start]').first().innerText();
    await page.locator('#article p[data-md-start]').first().click();
    await page.keyboard.type('测试取消');
    assert.equal(await page.getByRole('button', {name:'保存修改'}).isEnabled(), true);
    await page.getByRole('button', {name:'取消', exact:true}).click();
    assert.equal(await page.locator('#article').isVisible(), true, '取消后回到原阅读页');
    assert.equal(await page.locator('#article p[data-md-start]').first().innerText(), originalText);

    // 两侧边栏可独立收起并恢复，左侧状态可在刷新后保持。
    await page.getByRole('button', {name:'收起左侧导航',exact:true}).click();
    assert.equal(await page.locator('.sidebar').isVisible(), false);
    assert.equal(await page.getByRole('button', {name:'展开左侧导航',exact:true}).getAttribute('aria-expanded'), 'false');
    await page.getByRole('button', {name:'展开左侧导航',exact:true}).click();
    assert.equal(await page.locator('.sidebar').isVisible(), true);

    // 新表达章可由深链打开，且练习答案仍保持折叠
    await page.goto(base + '#' + encodeURIComponent('表达练习/中文到英文表达：关系还有没有挽回余地.md'));
    await page.getByRole('heading', {name: '中文到英文表达：关系还有没有挽回余地', exact: true}).waitFor();
    assert.equal(await page.locator('#article .reference-answers').getAttribute('open'), null, '表达章答案默认折叠');

    // 自动目录锚点不会被当成文档路由；跳到折叠答案时自动打开。
    assert.equal(await page.locator('#article .document-toc').count(), 0, '正文没有自动目录');
    assert.equal(await page.locator('#article .document-toc').count(), 0);
    const rightToggle = page.getByRole('button', {name:'展开目录',exact:true});
    const position = await rightToggle.boundingBox();
    assert.ok(position && Math.abs(position.y + position.height / 2 - 500) < 5, '目录入口位于屏幕右侧中间');
    await rightToggle.click();
    assert.equal(await page.locator('#outline').isVisible(), true);
    const closeToggle = page.getByRole('button', {name:'收起目录',exact:true});
    await closeToggle.hover();
    assert.equal(await closeToggle.getAttribute('data-tip'), '收起目录');
    const contents = page.locator('#outline-links a');
    assert.ok(await contents.count() >= 8);
    await contents.filter({hasText: '参考答案'}).click();
    assert.equal(await page.locator('#outline').isVisible(), false, '点击目录后抽屉关闭');
    await page.waitForFunction(() => location.hash.includes('::'));
    await page.waitForFunction(() => document.querySelector('.reference-answers')?.open === true);
    await page.reload();
    await page.getByRole('heading', {name: '参考答案', exact: true}).waitFor();
    assert.notEqual(await page.locator('.reference-answers').getAttribute('open'), null);
    assert.equal(await page.locator('#article h1').innerText(), '中文到英文表达：关系还有没有挽回余地');

    // 项目内 Skill 和学习计划在只读站点中可读
    await page.goto(base + '#' + encodeURIComponent('编纂与维护/中文到英文表达训练计划.md'));
    await page.getByRole('heading', {name: '中文到英文表达训练计划', exact: true}).waitFor();

    await page.goto(base + '#' + encodeURIComponent('表达练习/中译英校准素材 P001：中文情境任务.md'));
    await page.getByRole('heading', {name: '中译英校准素材 P001：中文情境任务', exact: true}).waitFor();

    await page.goto(base + '#' + encodeURIComponent('Chunks 收集/Chunks 收集箱.md'));
    await page.getByRole('heading', {name: 'Chunks 收集箱', exact: true}).waitFor();
    assert.equal(await page.locator('#article table').count(), 6, '六个分类各有一张收集表');
    assert.equal(await page.locator('#article table').first().locator('th').count(), 3, '收集表固定三列');

    await page.goto(base + '#' + encodeURIComponent('Chunks 收集/总统演讲 Chunks：坚持原则、澄清判断与回应挫折.md'));
    await page.getByRole('heading', {name: '总统演讲 Chunks：坚持原则、澄清判断与回应挫折', exact: true}).waitFor();
    assert.equal(await page.locator('#article tbody tr').count(), 20, '总统演讲精选二十个 chunks');
    await page.goto(base + '#' + encodeURIComponent('原文与参考资料/原文、教材与影视/总统演讲原文合集：GovInfo.md'));
    await page.getByRole('heading', {name: '总统演讲原文合集：GovInfo', exact: true}).waitFor();

    await page.goto(base + '#' + encodeURIComponent('学习章节/口语表达/脱口秀口语 Chunks：把观察、反问和不确定说出来.md'));
    await page.getByRole('heading', {name: '脱口秀口语 Chunks：把观察、反问和不确定说出来', exact: true}).waitFor();
    assert.equal(await page.locator('#article h2').filter({hasText: /^\d+\. /}).count(), 8, '脱口秀章展示八个知识点');
    assert.equal(await page.locator('#article .reference-answers').getAttribute('open'), null, '脱口秀章答案默认折叠');

    await page.goto(base + '#' + encodeURIComponent('编纂与维护/资料来源.md'));
    await page.getByRole('heading', {name: '资料来源', exact: true}).waitFor();
    assert.ok((await page.locator('#article').innerText()).includes('English → Download'), '字幕来源操作说明可读');

    // 深链 + 参考答案折叠
    await page.goto(base + '#' + encodeURIComponent('学习章节/句式与结构/nothing but：几个小词，意思为什么差这么多.md'));
    await page.getByRole('heading', {name: 'nothing but：几个小词，意思为什么差这么多', exact: true}).waitFor();
    assert.equal(await page.locator('#article .reference-answers').getAttribute('open'), null, '参考答案默认折叠');
    await page.locator('#article .reference-answers summary').click();
    assert.notEqual(await page.locator('#article .reference-answers').getAttribute('open'), null);

    // 文内相对 .md 链接改写为 hash 深链（句式骨架导览含家族章链接）
    await page.goto(base + '#' + encodeURIComponent('学习章节/句式与结构/句式骨架（Frames）：比语法分析高一层的学习单位.md'));
    await page.getByRole('heading', {name: '句式骨架（Frames）：比语法分析高一层的学习单位', exact: true}).waitFor();
    const relLink = await page.locator('#article a[href^="#"]').evaluateAll(links => links.some(a => decodeURIComponent(a.hash.slice(1)).startsWith('学习章节/') && !a.hash.includes('::')));
    assert.ok(relLink, '文档间相对链接改写为新目录深链');
    await page.goto(base + '#' + encodeURIComponent('book/01-reading/02-resigned.md'));
    await page.getByRole('heading', {name:'从 resigned 理解词义与搭配',exact:true}).waitFor();
    assert.ok(decodeURIComponent(await page.evaluate(()=>location.hash)).startsWith('#学习章节/'), '旧文档书签自动转向新路径');

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

    // 第一季词块页使用可流式阅读的纵向条目，不再出现整集长表格。
    await page.goto(base + '#' + encodeURIComponent('Chunks 收集/Better Call Saul：Chunks 积累.md'));
    await page.getByRole('heading', {name:'Better Call Saul：Chunks 积累',exact:true}).waitFor();
    await page.getByRole('button', {name:'编辑本文', exact:true}).click();
    assert.equal(await page.locator('#article').isVisible(), true, '长文原页面直接可编辑');
    assert.ok(await page.locator('#article [contenteditable=true]').count() > 8000);
    await page.getByRole('button', {name:'取消', exact:true}).click();
    assert.equal(await page.locator('#article [contenteditable=true]').count(), 0);
    assert.equal(await page.locator('#article table').count(), 0);
    assert.ok(await page.locator('#article h3').count() >= 1065, '第一季全部条目已展示');
    assert.equal(await page.locator('#nav').getByText('Better Call Saul：第一集纵向条目试读', {exact:true}).count(), 0);
    await page.getByRole('button', {name:'收起正文',exact:true}).click();
    assert.ok(await page.locator('.section-fold').evaluateAll(sections=>sections.every(s=>!s.open)), '正文全部收起');
    assert.equal(await page.locator('#article blockquote').first().isVisible(), false);
    await page.locator('#s01e01').click();
    const firstChunk = page.locator('#article .section-fold .section-fold').first();
    await firstChunk.locator('summary').first().click();
    assert.equal(await page.locator('#article blockquote').first().isVisible(), true, '单独展开一个词块');
    await page.getByRole('button', {name:'收起正文',exact:true}).click();
    await page.getByRole('button', {name:'展开目录', exact:true}).click();
    await page.locator('#outline-links a').filter({hasText:/^1\. /}).last().click();
    await page.waitForFunction(()=>location.hash.includes('::'));
    const targetId = decodeURIComponent((await page.evaluate(()=>location.hash)).split('::')[1]);
    assert.equal(await page.locator('#article').locator('[id]').filter({hasText:''}).evaluateAll((nodes,id)=>nodes.find(n=>n.id===id)?.closest('.section-fold')?.open,targetId), true, '目录展开目标词块');
    await page.reload();
    await page.getByRole('heading', {name:'Better Call Saul：Chunks 积累',exact:true}).waitFor();
    assert.ok(await page.locator('#article .section-fold').evaluateAll(sections=>sections.every(s=>s.open)), '刷新后默认展开正文');
    await page.getByRole('button', {name:'展开正文',exact:true}).click();
    await page.getByRole('button', {name:'展开目录',exact:true}).click();
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#outline').isVisible(), false, 'Escape 关闭右侧目录');


    // 移动端无横向溢出
    await page.setViewportSize({width: 390, height: 844});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.getByRole('button', {name:'编辑本文', exact:true}).click();
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, '移动端编辑工具栏不横向溢出');
    await page.getByRole('button', {name:'取消', exact:true}).click();

    // 自定义 Markdown 目录、重复标题与历史定位；搜索无结果后能回到原文。
    const catalogue = await (await page.request.get(base + 'api/catalog')).json();
    catalogue.items.push({id:'toc-fixture.md', title:'目录测试', group:'测试', body:'# 目录测试\n\n[跳到第二节](#重复-1)\n\n## 重复\n第一节\n\n## 重复\n第二节\n\n## 重复-1\n第三节'});
    await page.route('**/api/catalog', route => route.fulfill({json:catalogue}));
    await page.goto(base + '?toc-test#toc-fixture.md');
    await page.getByRole('heading', {name:'目录测试',exact:true}).waitFor();
    const ids = await page.locator('#article h2').evaluateAll(nodes => nodes.map(n=>n.id));
    assert.equal(new Set(ids).size, 3, '重复标题及已有后缀不会产生重复 ID');
    await page.getByRole('link', {name:'跳到第二节',exact:true}).click();
    await page.waitForFunction(() => decodeURIComponent(location.hash).endsWith('::重复-1'));
    await page.goBack();
    await page.waitForFunction(() => !location.hash.includes('::'));
    await page.goForward();
    await page.waitForFunction(() => decodeURIComponent(location.hash).endsWith('::重复-1'));
    await page.locator('#search').fill('no-results-928743');
    await page.locator('#search').fill('');
    await page.getByRole('heading', {name:'目录测试',exact:true}).waitFor();
    await page.unroute('**/api/catalog');

    assert.deepEqual(errors, []);
    console.log('PASS: direct block editing, reader, nav, TOC, links, search, theme, /files/, mobile width; no page errors.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
