'use strict';
const kindNames={word:'单词／义项',phrase:'词组搭配',sentence:'句子',grammar:'语法结构',expression:'情境表达'};
const modeNames={understand:'理解',express:'表达'};
let viewVersion=0, importRows=[], currentEntry=null, noticeTimer=null;
const esc=escapeHTML;
function notice(text){$('notice').textContent=text;$('notice').hidden=false;clearTimeout(noticeTimer);noticeTimer=setTimeout(()=>$('notice').hidden=true,6500);}
async function change(path,body){return api('/api/learning/'+path,{method:'POST',headers:{'Content-Type':'application/json','X-English-Token':state.token},body:JSON.stringify(body)});}
function options(map,value){return Object.entries(map).map(([k,v])=>`<option value="${k}" ${k===value?'selected':''}>${v}</option>`).join('');}
function when(value){return new Date(value).toLocaleString('zh-CN',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'});}
async function updateStats(){const s=await api('/api/learning/stats');$('due-count').textContent=s.due||'';return s;}
window.learningRoute=function(id){
  const v=++viewVersion;
  if(!['library','reviews','import'].includes(id)&&!id.startsWith('library/')&&!id.startsWith('learn/')&&!id.startsWith('review/'))return false;
  $('article').innerHTML='<p>正在读取学习记录…</p>';$('source').textContent='';
  $('breadcrumb').textContent='英语学习工作台';state.current=null;
  nav();
  (async()=>{
    if(id==='library'||id.startsWith('library/'))await libraryView(v,id.split('/')[1]||'');
    else if(id==='reviews')await reviewQueue(v);
    else if(id==='import')await importView(v);
    else {const parts=id.split('/');await detailView(parts[1],parts[0]==='review'?parts[2]:null,v);}
    await updateStats();
  })().catch(e=>{if(v===viewVersion)$('article').textContent=e.message;});
  return true;
};
window.attachLearning=async function(chapter){
  const v=viewVersion;
  try{
    const items=await api('/api/learning/items?chapter='+encodeURIComponent(chapter));
    if(v!==viewVersion||state.current?.id!==chapter)return;
    for(const h of $('article').querySelectorAll('h2')){
      const name=h.textContent.replace(/^\d+\.\s*/,'').split(/[：·]/)[0].trim();
      const item=items.find(x=>x.title===name);
      if(item){const link=document.createElement('a');link.className='entry-link';link.href='#learn/'+item.id;link.textContent=item.learned_modes?'查看学习记录':'记录学习';h.append(link);}
    }
    $('chapter-learning').innerHTML=`<a href="#library">本章关联 ${items.length} 个知识点 · 打开知识库</a><button id="capture-selection">将选中文字录入</button>`;
    $('capture-selection').onclick=()=>{const selection=window.getSelection();const text=selection.toString().trim();if(!text)return notice('请先在正文中选中一个词、短语或句子。');sessionStorage.setItem('english-import-text',text.slice(0,8000));sessionStorage.setItem('english-import-source','摘自 '+chapter);location.hash='import';};
    await updateStats();
  }catch(e){notice(e.message);}
};
function rowsHTML(items){return items.map(x=>`<a class="knowledge-row" href="#learn/${x.id}"><span><strong>${esc(x.title)}</strong><small>${esc(x.meaning||'尚未补充释义')}</small></span><span class="badge">${kindNames[x.kind]}${x.learned_modes?' · 已学习':''}</span></a>`).join('');}
async function libraryView(v,collection=''){
  const [collections,s]=await Promise.all([api('/api/learning/collections'),updateStats()]);if(v!==viewVersion)return;
  $('article').innerHTML=`<h1 class="learning-title">我的知识库</h1><p class="learn-help">词汇与词组可属于多个词表。学习记录不重复计算；资料收录不代表已经审校或掌握。</p><div class="learning-stats"><span><strong>${s.items}</strong>知识点</span><span><strong>${s.studied}</strong>有学习记录</span><span><strong>${s.due}</strong>到期任务</span><span><strong>${s.minutes}</strong>分钟手动记录</span></div><div class="learn-toolbar"><select id="knowledge-collection" aria-label="词表分类"><option value="">全部词表与自建内容</option>${collections.map(c=>`<option value="${esc(c.id)}" ${c.id===collection?'selected':''}>${esc(c.title)}（${c.count}）</option>`).join('')}</select></div><p id="collection-description" class="learn-help"></p><div class="learn-toolbar"><input id="knowledge-search" placeholder="搜索英文、中文含义…" aria-label="搜索知识点"><select id="knowledge-kind" aria-label="知识类型"><option value="">全部类型</option>${options(kindNames,'')}</select><select id="knowledge-state" aria-label="学习状态"><option value="">全部状态</option><option value="new">未学习</option><option value="studied">有记录</option></select></div><p id="knowledge-count" class="learn-help"></p><div id="knowledge-list" class="knowledge-list"></div><button id="show-more" hidden>再显示100条</button><div class="learn-actions"><a href="#import">录入新知识</a><button id="export-data">导出数据</button><button id="backup-data">备份数据库</button></div>`;
  let shown=0, sequence=0;
  async function render(append=false){
    const seq=++sequence;if(!append){shown=0;$('knowledge-list').innerHTML='';}
    $('knowledge-count').textContent='正在查询…';$('show-more').disabled=true;
    const selected=$('knowledge-collection').value,meta=collections.find(c=>c.id===selected);
    $('collection-description').textContent=meta?JSON.parse(meta.metadata).description||'':'';
    const query=new URLSearchParams({q:$('knowledge-search').value.trim(),kind:$('knowledge-kind').value,state:$('knowledge-state').value,collection:selected,offset:String(shown),limit:'100'});
    try{const found=await api('/api/learning/browse?'+query);if(v!==viewVersion||seq!==sequence)return;
      shown+=found.items.length;$('knowledge-count').textContent=`找到 ${found.total} 项，显示 ${shown} 项。`;
      const html=rowsHTML(found.items);if(append)$('knowledge-list').insertAdjacentHTML('beforeend',html);else $('knowledge-list').innerHTML=html||'<p class="learn-empty">没有匹配的知识点，可以从录入开始。</p>';
      $('show-more').hidden=shown>=found.total;$('show-more').disabled=false;
    }catch(e){if(v===viewVersion&&seq===sequence){$('knowledge-count').textContent=e.message;$('show-more').disabled=false;}}
  }
  $('knowledge-search').oninput=()=>render();$('knowledge-kind').onchange=()=>render();$('knowledge-state').onchange=()=>render();$('knowledge-collection').onchange=()=>{history.replaceState(null,'','#library'+($('knowledge-collection').value?'/'+$('knowledge-collection').value:''));render();};$('show-more').onclick=()=>render(true);await render();
  $('export-data').onclick=async()=>{try{const data=await api('/api/learning/export');const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='english-learning-'+new Date().toISOString().slice(0,10)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}catch(e){notice(e.message);}};
  $('backup-data').onclick=async()=>{try{const result=await change('backup',{});notice('备份已保存：'+result.path);}catch(e){notice(e.message);}};
}
async function reviewQueue(v){
  const rows=await api('/api/learning/due');if(v!==viewVersion)return;
  $('article').innerHTML=`<h1>今日复习</h1><p class="learn-help">先尝试回忆，再查看解释。这里按到期时间排列，理解和表达是两个任务。</p>${rows.length?`<p>${rows.length} 项待复习</p><div class="knowledge-list">${rows.map(x=>`<a class="knowledge-row" href="#review/${x.id}/${x.mode}"><span><strong>${esc(x.title)}</strong><small>到期：${when(x.due)}</small></span><span class="badge">${modeNames[x.mode]}</span></a>`).join('')}</div>`:'<div class="learn-empty">目前没有到期任务。完成首次学习后，会自动安排次日复习。<br>你也可以从知识点详情提前练习。</div>'}<div class="learn-actions"><a href="#library">去知识库</a></div><p class="learn-help">忘了：10分钟后；费力：较短间隔；顺利：逐步延长至3、7、14、30、60天。采用可解释的初版规则，不承诺最优记忆效果。网页关闭不会影响到期日期；当前不发送系统通知。</p>`;
}
function answerInputs(){return `<label for="learning-answer">你的回答／本次学习笔记</label><textarea id="learning-answer" placeholder="先写下理解，或用英文表达。原答会保留，也可留空自行回忆。"></textarea><div class="learn-inputs"><div><label for="assistance">这次如何完成</label><select id="assistance">${options({independent:'独立尝试',hint:'有提示',lookup:'查阅资料'},'independent')}</select></div><div><label for="study-minutes">用时（分钟）</label><input id="study-minutes" type="number" min="0" max="240" value="0"></div></div>`;}
async function detailView(id,reviewMode,v){
  const item=await api('/api/learning/item?id='+encodeURIComponent(id));if(v!==viewVersion)return;
  currentEntry=item;state.knowledgeId=item.id;state.current={id:'knowledge:'+item.id,title:item.title,body:item.body};
  const mode=reviewMode||'understand';if(!modeNames[mode])throw Error('无效的复习方向');
  const prompt=mode==='express'?(item.meaning||'请在一个新情境中用英文表达这个知识点。'):item.title;
  const explanation=`<p><strong>${esc(item.meaning||'尚未补充释义')}</strong></p>${markdown(item.body||'可以请老师补充用法，也可以录入带释义的新条目。',item.chapters[0]||'book/README.md')}`;
  const status=item.progress.map(p=>`<span>${modeNames[p.mode]}：下次 ${when(p.due)}</span>`).join(' · ')||'尚无学习记录';
  $('article').innerHTML=`<a href="#${reviewMode?'reviews':'library'}">← ${reviewMode?'复习队列':'知识库'}</a><p class="learn-meta">${kindNames[item.kind]} · ${esc(item.source)}</p><h1 class="learning-title">${reviewMode?modeNames[mode]+'复习':esc(item.title)}</h1>${reviewMode?`<div class="review-title">${esc(prompt)}</div><p class="learn-help">${mode==='express'?'根据意图尝试英文表达，不要求与参考答案逐字一致。':'先解释含义，并尝试给一个新语境。'}</p>`:explanation}<div class="learn-box"><h2>${reviewMode?'先回忆，再对照':'记录本次学习'}</h2><p class="learn-help">${status}</p>${reviewMode?'':`<label for="learning-mode">学习方向</label><select id="learning-mode">${options(modeNames,'understand')}</select>`}${answerInputs()}<div class="learn-actions">${reviewMode?'<button id="reveal-answer" class="primary">查看解释与参考</button>':'<button id="mark-learned" class="primary">完成本次学习</button><button id="practice-now">提前复习</button>'}</div>${reviewMode?`<section class="review-answer" id="review-answer" hidden>${explanation}<p class="learn-help">对照后给这次表现一个自评。评分是你的报告，不是永久掌握证明。</p><div class="learn-actions"><button data-rating="forgot">忘了 · 10分钟后</button><button data-rating="hard">费力 · 缩短间隔</button><button data-rating="good" class="primary">顺利 · 延长间隔</button></div></section>`:''}</div><div class="learn-meta">${item.chapters.map(c=>`<a href="#${encodeURIComponent(c)}">回到原章节</a>`).join(' · ')}</div><section class="events"><h2>学习历史</h2>${item.events.length?item.events.map(e=>`<div class="event-row"><strong>${modeNames[e.mode]} · ${e.action==='learn'?'首次学习':({forgot:'复习：忘了',hard:'复习：费力',good:'复习：顺利'}[e.rating])}</strong> · ${when(e.at)} ${e.undone?'<span class="undo-label">已撤销</span>':`<button data-undo="${esc(e.id)}">撤销</button>`}<p>${esc(e.answer||'未填写文字回答')} · ${{independent:'独立',hint:'有提示',lookup:'查阅'}[e.assistance]} · ${e.minutes}分钟</p></div>`).join(''):'<p class="learn-help">这里保留实际回答、提示程度、日期和自评。</p>'}</section>`;
  const selectedMode=()=>reviewMode||$('learning-mode').value;
  async function record(action,rating=''){
    const buttons=[...$('article').querySelectorAll('button')];buttons.forEach(b=>b.disabled=true);
    try{await change('record',{id:item.id,mode:selectedMode(),action,rating,answer:$('learning-answer').value,assistance:$('assistance').value,minutes:Number($('study-minutes').value),request_id:crypto.randomUUID()});await updateStats();notice(action==='learn'?'已记录本次学习，次日复习。':'已保存原答与自评，复习时间已更新。');if(reviewMode)location.hash='reviews';else route();}
    catch(e){notice(e.message);buttons.forEach(b=>b.disabled=false);}
  }
  if(reviewMode){$('reveal-answer').onclick=()=>{$('review-answer').hidden=false;$('reveal-answer').hidden=true;};$('article').querySelectorAll('[data-rating]').forEach(b=>b.onclick=()=>record('review',b.dataset.rating));}
  else{$('mark-learned').onclick=()=>record('learn');$('practice-now').onclick=()=>{if(!item.progress.some(p=>p.mode===selectedMode()))return notice('这个方向尚未学习，请先完成首次学习。');location.hash=`review/${item.id}/${selectedMode()}`;};const update=()=>{$('mark-learned').disabled=item.progress.some(p=>p.mode===selectedMode());};$('learning-mode').onchange=update;update();}
  $('article').querySelectorAll('[data-undo]').forEach(b=>b.onclick=async()=>{b.disabled=true;try{await change('undo',{event_id:b.dataset.undo});notice('已撤销，恢复之前的复习安排。');route();}catch(e){notice(e.message);b.disabled=false;}});
  if(item.collections?.length){
    const section=document.createElement('section');section.className='collection-sources';
    section.innerHTML='<h2>所属词表与补充资料</h2><p class="learn-help">下列是额外来源，原有学习记录不代表这些新增解释都已掌握。</p>'+item.collections.map(c=>`<details><summary>${esc(c.title)}</summary><p><a href="#library/${esc(c.id)}">浏览此词表</a></p>${markdown(c.body||'',item.chapters[0]||'book/README.md')}</details>`).join('');
    $('article').append(section);
  }
}
async function importView(v){
  importRows=[];
  $('article').innerHTML=`<h1>录入知识</h1><p class="learn-help">输入一个词、短语、句子或多行材料。每行一个条目，可用 Tab、＝ 或「 — 」分隔释义。先预览，核对后入库；同类型、同内容、同义项不会重复保存。</p><div class="learn-box"><label for="import-kind">默认类型</label><select id="import-kind">${options(kindNames,'phrase')}</select><label for="import-text">待整理的内容</label><textarea id="import-text" rows="7" placeholder="take issue with — 对……提出异议&#10;be resigned to — 无奈接受"></textarea><label for="import-source">来源／出处（可选）</label><input id="import-source" placeholder="例如书名、章节、文章链接"><div class="learn-actions"><button class="primary" id="preview-import">整理为候选</button><button id="generate-import">请老师补充释义与例句</button></div><p class="learn-help">直接整理每次最多100行；AI补充每次最多20行，使用当前Codex账户。生成内容待你核对，不冒充词典原文。</p><p id="import-status" class="import-status" role="status"></p></div><div id="import-candidates"></div><div class="learn-actions"><button id="confirm-import" class="primary" hidden>确认选中项入库</button></div>`;
  $('import-text').value=sessionStorage.getItem('english-import-text')||'';$('import-source').value=sessionStorage.getItem('english-import-source')||'';
  sessionStorage.removeItem('english-import-text');sessionStorage.removeItem('english-import-source');
  function show(rows){if(v!==viewVersion)return;importRows=rows;$('import-candidates').innerHTML=rows.map((r,i)=>`<section class="import-candidate" data-index="${i}"><div class="candidate-head"><input type="checkbox" aria-label="选择候选${i+1}" ${r.exists?'':'checked'}><strong>候选 ${i+1}</strong><span class="badge">${r.exists?'已存在':r.related?.length?'已有同名条目，请核对义项':'待核对'}</span></div><select aria-label="候选类型">${options(kindNames,r.kind)}</select><input class="title-edit" aria-label="候选内容" value="${esc(r.title)}"><textarea class="meaning-edit" aria-label="候选释义" placeholder="中文含义，可选">${esc(r.meaning)}</textarea><textarea class="body-edit" aria-label="候选讲解" placeholder="用法、例句、语法或表达分析，可选">${esc(r.body)}</textarea><p class="learn-help">${esc(r.source)}${r.related?.length?' · 已有：'+r.related.map(x=>esc(x.meaning||'无释义')).join(' / '):''}</p></section>`).join('');$('confirm-import').hidden=!rows.length;$('import-status').textContent=`已整理 ${rows.length} 个候选，可编辑后确认。`;}
  $('preview-import').onclick=async()=>{try{show(await change('preview',{text:$('import-text').value,kind:$('import-kind').value}));}catch(e){notice(e.message);}};
  async function watch(job){if(v!==viewVersion)return;try{const r=await api('/api/learning/draft?id='+job);if(v!==viewVersion)return;if(r.status==='running'){setTimeout(()=>watch(job),2000);return;}localStorage.removeItem('english-draft');$('generate-import').disabled=false;if(r.status==='error')throw Error(r.error);show(r.items);}catch(e){if(v===viewVersion){$('import-status').textContent=e.message;$('generate-import').disabled=false;}}}
  $('generate-import').onclick=async()=>{try{$('generate-import').disabled=true;const r=await change('generate',{text:$('import-text').value,kind:$('import-kind').value});localStorage.setItem('english-draft',r.id);$('import-status').textContent='老师正在整理候选，完成后请核对。可以离开后回来继续查看。';watch(r.id);}catch(e){notice(e.message);$('generate-import').disabled=false;}};
  const pending=localStorage.getItem('english-draft');if(pending){$('generate-import').disabled=true;$('import-status').textContent='正在恢复上次候选生成…';watch(pending);}
  $('confirm-import').onclick=async()=>{const rows=[...$('import-candidates').querySelectorAll('.import-candidate')].filter(el=>el.querySelector('input[type=checkbox]').checked).map(el=>{const original=importRows[Number(el.dataset.index)];return {kind:el.querySelector('select').value,title:el.querySelector('.title-edit').value,meaning:el.querySelector('.meaning-edit').value,body:el.querySelector('.body-edit').value,source:original.source+($('import-source').value?'；出处：'+$('import-source').value:'')};});if(!rows.length)return notice('请至少选择一个候选。');$('confirm-import').disabled=true;try{const result=await change('import',{items:rows});notice(`已新增 ${result.added} 项，匹配已有 ${result.existing} 项。`);location.hash=result.ids.length===1?'learn/'+result.ids[0]:'library';}catch(e){notice(e.message);$('confirm-import').disabled=false;}};
}
