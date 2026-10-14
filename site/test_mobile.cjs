const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
(async () => {
 const browser = await chromium.launch();
 try {
  for (const width of [360,390,430,844]) {
   const page = await browser.newPage({viewport:{width,height:844},isMobile:width<760,hasTouch:true});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(process.env.ENGLISH_TEST_URL || 'http://127.0.0.1:4174/');
   await page.locator('#article h1').waitFor();
   await page.locator('#nav a.nav-link').first().waitFor({state:'attached'});
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
   if(width<760){
    assert.equal(await page.locator('.sidebar').isVisible(),false);
    await page.locator('#nav a.nav-link').first().waitFor({state:'attached'});
    await page.locator('#mobile-nav').click();
    assert.equal(await page.locator('.sidebar').isVisible(),true);
    await page.locator('#nav-backdrop').click({position:{x:width-10,y:10}});
    await page.locator('#mobile-nav').click();
    const firstGroup = page.locator('#nav .nav-fold').first();
    // 目录只在侧栏中显示。
    if (await firstGroup.getAttribute('open') === null) await firstGroup.locator('summary').click();
    assert.notEqual(await firstGroup.getAttribute('open'), null, '选择文章前分组已展开');
    await page.locator('#nav a.nav-link').first().click();
    await page.waitForFunction(()=>location.hash.length>1);
    assert.equal(await page.locator('.sidebar').isVisible(),false);
    await page.locator('#right-toggle').click();
    await page.locator('#outline-links a').first().click();
    await page.waitForFunction(()=>location.hash.includes('::'));
    assert.equal(await page.locator('#outline').isVisible(),false);
   }
   await page.locator('#search').fill('resigned');
   await page.locator('.search-result').first().click();
   await page.locator('#article h1').waitFor();
   assert.deepEqual(errors,[]);
   console.log('PASS touch navigation/search width',width);
   await page.close();
  }
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
