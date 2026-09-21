const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto('http://127.0.0.1:4175/', { waitUntil: 'networkidle' });
  const home = await page.evaluate(() => ({
    folds: document.querySelectorAll('#nav > details').length,
    nested: document.querySelectorAll('#nav details details').length,
    docnav: !!document.getElementById('docnav'),
    titles: [...document.querySelectorAll('#nav > details .nav-fold-title')].map(e => e.textContent),
    openAtHome: document.querySelectorAll('#nav > details[open]').length,
  }));
  // 当前页所在组自动展开 + 高亮
  await page.goto('http://127.0.0.1:4175/#LEARNER.md', { waitUntil: 'networkidle' });
  await page.waitForTimeout(300);
  const learner = await page.evaluate(() => ({
    openGroups: [...document.querySelectorAll('#nav > details[open] .nav-fold-title')].map(e => e.textContent),
    active: document.querySelector('#nav a.active')?.textContent,
    activeInOpenGroup: !!document.querySelector('#nav > details[open] a.active'),
  }));
  // nav.json 组里的章节
  await page.goto('http://127.0.0.1:4175/#progress/CURRENT.md', { waitUntil: 'networkidle' });
  await page.waitForTimeout(300);
  const current = await page.evaluate(() => ({
    openGroups: [...document.querySelectorAll('#nav > details[open] .nav-fold-title')].map(e => e.textContent),
    active: document.querySelector('#nav a.active')?.textContent,
  }));
  // 专题章自动展开
  const chapter = await page.evaluate(() => document.querySelector('#nav a.nav-link')?.getAttribute('href'));
  await page.goto('http://127.0.0.1:4175/' + chapter, { waitUntil: 'networkidle' });
  await page.waitForTimeout(300);
  const lesson = await page.evaluate(() => ({
    openGroups: [...document.querySelectorAll('#nav > details[open] .nav-fold-title')].map(e => e.textContent),
    active: document.querySelector('#nav a.active')?.textContent,
  }));
  // 移动端
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('http://127.0.0.1:4175/', { waitUntil: 'networkidle' });
  const mobile = await page.evaluate(() => {
    const s = document.querySelector('.sidebar');
    return { visible: !!s.offsetParent, scrollable: s.scrollHeight >= s.clientHeight, folds: document.querySelectorAll('#nav > details').length };
  });
  // 点击组内链接后组保持展开
  await page.goto('http://127.0.0.1:4175/#LEARNER.md', { waitUntil: 'networkidle' });
  await page.waitForTimeout(300);
  await page.click('#nav a.active');
  await page.waitForTimeout(300);
  const afterClick = await page.evaluate(() => [...document.querySelectorAll('#nav > details[open] .nav-fold-title')].map(e => e.textContent));
  console.log(JSON.stringify({ home, learner, current, lesson, mobile, afterClick }, null, 1));
  await browser.close();
})();
