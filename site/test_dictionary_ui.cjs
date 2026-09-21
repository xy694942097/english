const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
const base=process.env.ENGLISH_TEST_URL||'http://127.0.0.1:4175';

(async()=>{
  const browser=await chromium.launch();
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1000}});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(base+'/#dictionary/indignant');
    await page.getByRole('heading',{name:'查词典',exact:true}).waitFor();
    await page.getByRole('heading',{name:'indignant',exact:true}).waitFor();
    await page.getByText('愤怒的, 愤慨的').waitFor();
    await page.locator('text=angered at something unjust or wrong').first().waitFor();
    await page.getByText('词根词缀').waitFor();
    await page.locator('#dict-query').fill('resigned');
    await page.locator('#dict-submit').click();
    await page.getByRole('heading',{name:'resigned',exact:true}).waitFor();
    await page.getByText('查询：resigned').waitFor();
    await page.goto(base+'/#'+encodeURIComponent('book/01-reading/02-resigned.md'));
    await page.getByRole('heading',{name:'从 resigned 理解词义与搭配',exact:true}).waitFor();
    await page.getByRole('button',{name:'查选中词'}).waitFor();
    await page.evaluate(()=>{
      const walker=document.createTreeWalker(document.querySelector('#article'),NodeFilter.SHOW_TEXT);
      let node;
      while((node=walker.nextNode())){
        const at=node.nodeValue.indexOf('resigned');
        if(at>=0){
          const range=document.createRange();
          range.setStart(node,at);
          range.setEnd(node,at+'resigned'.length);
          const selection=getSelection();
          selection.removeAllRanges();
          selection.addRange(range);
          break;
        }
      }
    });
    await page.getByRole('button',{name:'查选中词'}).click();
    await page.getByRole('heading',{name:'resigned',exact:true}).waitFor();
    await page.getByRole('link',{name:/回到原文/}).click();
    await page.getByRole('heading',{name:'从 resigned 理解词义与搭配',exact:true}).waitFor();
    assert.deepEqual(errors,[]);
    console.log('PASS: dictionary page, lookup, lemma resolution, selected word navigation, return to chapter.');
  }finally{
    await browser.close();
  }
})().catch(e=>{console.error(e);process.exitCode=1;});
