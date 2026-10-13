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

    // 无文档深链时打开首页，显式点击后才进入文章。
    await page.goto(base);
    await page.getByRole('heading', {name:'读懂整句，也把意思说出来。',exact:true}).waitFor();
    assert.equal(await page.locator('#right-toggle').isVisible(), false);
    await page.locator('#article a').filter({hasText:'阅读精选 Chunks'}).click();
    await page.getByRole('heading', {name:'精选 Chunks',exact:true}).waitFor();
    await page.locator('.brand').click();
    await page.getByRole('heading', {name:'读懂整句，也把意思说出来。',exact:true}).waitFor();
    await page.reload();
    await page.getByRole('heading', {name:'读懂整句，也把意思说出来。',exact:true}).waitFor();
    await page.locator('#article a').filter({hasText:'生词与熟词新义'}).click();
    await page.getByRole('heading', {name: '生词与熟词新义', exact: true}).waitFor();
    assert.ok((await page.locator('#article h2').count()) > 0, 'marked 渲染出章节小节');
    assert.equal(await page.locator('#nav .nav-fold').count(), 5, '五个学习导航分组');
    const registeredCount = (await (await page.request.get(base + 'api/catalog')).json()).items.length;
    assert.equal(await page.locator('#nav a.nav-link').count(), registeredCount, '登记文档均有导航入口');
    const navText = await page.locator('#nav').innerText();
    assert.ok(navText.includes('表达练习') && navText.includes('原文与参考资料'), '练习与查阅分区可见');
    assert.ok(!navText.includes('英语固定短语完全指南') && !navText.includes('雅思级别英语1000句 v2'), '隔离文档不在导航');
    // 当前文档所在分组展开并高亮
    assert.ok(await page.locator('#nav > details[open] a.active').count() > 0, '当前文档分组展开且高亮');

    assert.equal(await page.locator('[contenteditable=true], #edit-document, #save-edit').count(), 0, '纯只读界面');

    // 两侧边栏可独立收起并恢复，左侧状态可在刷新后保持。
    await page.getByRole('button', {name:'收起左侧导航',exact:true}).click();
    assert.equal(await page.locator('.sidebar').isVisible(), false);
    assert.equal(await page.getByRole('button', {name:'展开左侧导航',exact:true}).getAttribute('aria-expanded'), 'false');
    await page.getByRole('button', {name:'展开左侧导航',exact:true}).click();
    assert.equal(await page.locator('.sidebar').isVisible(), true);

    // 新表达章可由深链打开，且练习答案仍保持折叠
    await page.goto(base + '#' + encodeURIComponent('course/表达练习/Better Call Saul S01 中译英练习.md'));
    await page.getByRole('heading', {name: 'Better Call Saul S01 中译英练习', exact: true}).waitFor();
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
    await contents.filter({hasText: '参考 Chunk'}).click();
    assert.equal(await page.locator('#outline').isVisible(), false, '点击目录后抽屉关闭');
    await page.waitForFunction(() => location.hash.includes('::'));
    await page.waitForFunction(() => document.querySelector('.reference-answers')?.open === true);
    await page.reload();
    await page.getByRole('heading', {name: '参考 Chunk', exact: true}).waitFor();
    assert.notEqual(await page.locator('.reference-answers').getAttribute('open'), null);
    assert.equal(await page.locator('#article h1').innerText(), 'Better Call Saul S01 中译英练习');

    // 项目内 Skill 和学习计划在只读站点中可读
    await page.goto(base + '#' + encodeURIComponent('course/编纂与维护/Skills/中文到英文表达训练计划.md'));
    await page.getByRole('heading', {name: '中译英训练与编题', exact: true}).waitFor();

    await page.goto(base + '#' + encodeURIComponent('course/表达练习/每日逐句精读与迁移.md'));
    await page.getByRole('heading', {name: '每日逐句精读与迁移', exact: true}).waitFor();

    await page.goto(base + '#' + encodeURIComponent('course/Chunks 收集/Chunks 收集箱.md'));
    await page.getByRole('heading', {name: 'Chunks 收集箱', exact: true}).waitFor();
    assert.equal(await page.locator('#article table').count(), 0, '收集箱不使用长表格');
    assert.equal(await page.locator('#article h3').count(), 63, '收集箱63个候选均保留为纵向条目');

    await page.goto(base + '#' + encodeURIComponent('course/Chunks 收集/总统演讲 Chunks：坚持原则、澄清判断与回应挫折.md'));
    await page.getByRole('heading', {name: '总统演讲 Chunks：坚持原则、澄清判断与回应挫折', exact: true}).waitFor();
    assert.equal(await page.locator('#article h3').count(), 20, '总统演讲精选二十个纵向 chunks');
    await page.goto(base + '#' + encodeURIComponent('course/原文与参考资料/原文、教材与影视/总统演讲原文合集：GovInfo.md'));
    await page.getByRole('heading', {name: '总统演讲原文合集：GovInfo', exact: true}).waitFor();

    await page.goto(base + '#' + encodeURIComponent('course/学习章节/口语表达/脱口秀口语 Chunks：把观察、反问和不确定说出来.md'));
    await page.getByRole('heading', {name: '精选 Chunks', exact: true}).waitFor();
    await page.getByRole('heading', {name: /Did you ever notice \(that\/how\) \.\.\.\?/ }).waitFor();
    await page.getByRole('heading', {name: /One of these days, \.\.\./ }).waitFor();

    // 中译英题目先独立呈现，目标 Chunk 仅在主动查看提示后显示
    await page.goto(base + '#' + encodeURIComponent('course/表达练习/Better Call Saul S01 中译英练习.md'));
    await page.getByRole('heading', {name: 'Better Call Saul S01 中译英练习', exact: true}).waitFor();
    assert.equal(await page.locator('#article h3').count(), 31, 'S01E01 试跑31题');
    const chunkReference = page.locator('#article .reference-answers');
    assert.equal(await chunkReference.getAttribute('open'), null, '参考 Chunk 默认关闭');
    assert.equal(await chunkReference.locator('li').first().isVisible(), false, '题目页不显示英文提示');
    assert.ok(!(await page.locator('#article').innerText()).includes('bully sb. into doing sth.'));
    assert.ok(!(await page.locator('#outline-links').innerText()).includes('bully sb. into doing sth.'), '目录不泄露目标词块');
    await chunkReference.locator('summary').click();
    assert.equal(await chunkReference.locator('li').first().isVisible(), true, '主动查看后显示关联词块');

    await page.goto(base + '#' + encodeURIComponent('course/编纂与维护/资料来源.md'));
    await page.getByRole('heading', {name: '资料来源', exact: true}).waitFor();
    assert.ok((await page.locator('#article').innerText()).includes('English → Download'), '字幕来源操作说明可读');

    // 精选 Chunks 已合并原有短专题；练习页仍保留答案折叠
    await page.goto(base + '#' + encodeURIComponent('course/Chunks 收集/精选 Chunks.md'));
    await page.getByRole('heading', {name: '精选 Chunks', exact: true}).waitFor();
    await page.getByRole('heading', {name: /^\d+\. nothing but$/}).waitFor();
    await page.goto(base + '#' + encodeURIComponent('course/表达练习/Better Call Saul S01 中译英练习.md'));
    await page.getByRole('heading', {name: 'Better Call Saul S01 中译英练习', exact: true}).waitFor();
    assert.equal(await page.locator('#article .reference-answers').getAttribute('open'), null, '参考答案默认折叠');
    await page.locator('#article .reference-answers summary').click();
    assert.notEqual(await page.locator('#article .reference-answers').getAttribute('open'), null);

    // 文内相对 .md 链接改写为 hash 深链
    await page.goto(base + '#' + encodeURIComponent('course/Chunks 收集/Chunks 收集箱.md'));
    await page.getByRole('heading', {name: 'Chunks 收集箱', exact: true}).waitFor();
    const relLink = await page.locator('#article a[href^="#"]').evaluateAll(links => links.some(a => decodeURIComponent(a.hash.slice(1)).startsWith('course/编纂与维护/') && !a.hash.includes('::')));
    assert.ok(relLink, '文档间相对链接改写为新目录深链');
    await page.goto(base + '#' + encodeURIComponent('book/01-reading/02-resigned.md'));
    await page.getByRole('heading', {name:'生词与熟词新义',exact:true}).waitFor();
    assert.ok(decodeURIComponent(await page.evaluate(()=>location.hash)).startsWith('#course/词汇/生词与熟词新义.md'), '旧生词书签转向词汇页');
    await page.goto(base + '#' + encodeURIComponent('学习章节/句式与结构/nothing but：几个小词，意思为什么差这么多.md') + '::' + encodeURIComponent('参考答案'));
    await page.getByRole('heading', {name:'精选 Chunks',exact:true}).waitFor();
    assert.ok(decodeURIComponent(await page.evaluate(()=>location.hash)).startsWith('#course/Chunks 收集/精选 Chunks.md'), '旧 chunk 书签转到精选页');

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
    await page.goto(base + '#' + encodeURIComponent('course/Chunks 收集/Better Call Saul：Chunks 积累.md'));
    await page.getByRole('heading', {name:'Better Call Saul：Chunks 积累',exact:true}).waitFor();
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
    // 自定义 Markdown 目录、重复标题与历史定位；搜索无结果后能回到原文。
    const catalogue = await (await page.request.get(base + 'api/catalog')).json();
    catalogue.items.push({id:'toc-fixture.md', title:'目录测试', group:'测试', body:'# 目录测试\n\n[跳到第二节](#重复-1)\n\n## 重复\n第一节\n\n## 重复\n第二节\n\n## 重复-1\n第三节'});
    await page.route('**/catalog.json', route => route.fulfill({json:catalogue}));
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
    await page.unroute('**/catalog.json');

    await page.goto(base + '#missing-document.md');
    await page.getByRole('heading', {name:'未找到这篇文章',exact:true}).waitFor();
    await page.getByRole('link', {name:'返回首页',exact:true}).click();
    await page.getByRole('heading', {name:'读懂整句，也把意思说出来。',exact:true}).waitFor();

    assert.deepEqual(errors, []);
    console.log('PASS: read-only viewer, reader, nav, TOC, links, search, theme, /files/, mobile width; no page errors.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
