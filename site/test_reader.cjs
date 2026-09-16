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
    await page.goto(base + '#' + encodeURIComponent('book/03-四六级词汇/00-guide.md'));
    await page.getByRole('heading', {name: '四六级词汇：学习路线与词汇索引', exact: true}).waitFor();
    await page.getByRole('link', {name: '熟悉动词，陌生宾语', exact: true}).click();
    await page.getByRole('heading', {name: '01 熟悉动词，陌生宾语', exact: true}).waitFor();
    assert.equal(await page.locator('#article details').getAttribute('open'), null);
    await page.locator('#article summary').click();
    assert.notEqual(await page.locator('#article details').getAttribute('open'), null);
    await page.locator('#search').fill('qualified support');
    const abstractLink = page.locator('.search-result').filter({has: page.locator('strong', {hasText: '08 六级深化'})});
    await abstractLink.click();
    await page.getByRole('heading', {name: '08 六级深化：抽象语境中的熟词', exact: true}).waitFor();
    assert.equal(await page.locator('#article h2').filter({hasText: /^\d+\./}).count(), 6);
    await page.setViewportSize({width: 390, height: 844});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    assert.deepEqual(errors, []);
    console.log('PASS: Unicode links, search, six entries, folded answers, mobile width; no page errors.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
