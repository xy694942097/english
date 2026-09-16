'use strict';
const $ = id => document.getElementById(id);
const state = {items: [], course: {topics:[]}, current: null, token: '', session: '', timer: null, sending: false};
const escapeHTML = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const dictWord = text => (String(text||'').match(/[A-Za-z][A-Za-z'-]{1,}/)?.[0]||'').replace(/^'+|'+$/g,'').toLowerCase();
function inline(text, base) {
  return escapeHTML(text).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/\*([^*]+)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (all, label, raw) => {
      if (/^https?:\/\//.test(raw)) return `<a href="${raw}" target="_blank" rel="noopener noreferrer">${label}</a>`;
      if (!raw.endsWith('.md') || raw.includes(':')) return label;
      const path = decodeURIComponent(new URL(raw, 'https://book.local/' + base).pathname.slice(1));
      return `<a href="#${encodeURIComponent(path)}">${label}</a>`;
    });
}
function markdown(text, base) {
  const lines = text.split('\n'); let html = '', list = '', code = false, buffer = [];
  let quote = null, table = null;
  const splitRow = line => { let s = line.trim(); if (s.startsWith('|')) s = s.slice(1); if (s.endsWith('|')) s = s.slice(0, -1); return s.split('|').map(c => c.trim()); };
  const isSeparator = cells => cells.length > 0 && cells.every(c => /^:?-{2,}:?$/.test(c));
  function closeList() { if (list) { html += `</${list}>`; list = ''; } }
  function closeQuote() { if (quote) { html += `<blockquote>${quote.map(l => `<p>${inline(l,base)}</p>`).join('')}</blockquote>`; quote = null; } }
  function closeTable() {
    if (!table) return;
    const rows = table.map(splitRow);
    const header = rows[0] || [];
    const body = rows.slice(1).filter(r => !isSeparator(r));
    html += `<table><thead><tr>${header.map(c => `<th>${inline(c,base)}</th>`).join('')}</tr></thead><tbody>${body.map(r => `<tr>${r.map(c => `<td>${inline(c,base)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
    table = null;
  }
  function closeAll() { closeList(); closeQuote(); closeTable(); }
  for (const line of lines) {
    if (line.startsWith('```')) { closeAll(); if (code) { html += `<pre><code>${escapeHTML(buffer.join('\n'))}</code></pre>`; buffer = []; } code = !code; continue; }
    if (code) { buffer.push(line); continue; }
    const trimmed = line.trim();
    if (!trimmed) { closeAll(); continue; }
    let m;
    if ((m = line.match(/^(#{1,4}) (.*)/))) { closeAll(); const n = m[1].length; html += `<h${n}>${inline(m[2],base)}</h${n}>`; }
    else if (line.startsWith('>')) { closeList(); closeTable(); const content = line.replace(/^>\s?/, '').trim(); if (content) quote = quote ? quote.concat(content) : [content]; }
    else if (trimmed.startsWith('|') && trimmed.indexOf('|', 1) !== -1) { closeList(); closeQuote(); (table = table || []).push(trimmed); }
    else if ((m = line.match(/^[-*] (.*)/))) { closeQuote(); closeTable(); if (list !== 'ul') { closeList(); list='ul'; html+='<ul>'; } html += `<li>${inline(m[1],base)}</li>`; }
    else if ((m = line.match(/^\d+\. (.*)/))) { closeQuote(); closeTable(); if (list !== 'ol') { closeList(); list='ol'; html+='<ol>'; } html += `<li>${inline(m[1],base)}</li>`; }
    else { closeAll(); html += `<p>${inline(line,base)}</p>`; }
  }
  closeAll(); if (code) html += `<pre><code>${escapeHTML(buffer.join('\n'))}</code></pre>`;
  return html;
}
async function api(path, options) {
  const response = await fetch(path, options); const data = await response.json();
  if (!response.ok) throw new Error(data.error || '连接失败，请刷新页面重试。'); return data;
}
function dictionaryHash(word, from=state.current?.id || '', y=scrollY) {
  const base = '#dictionary' + (word ? '/' + encodeURIComponent(word) : '');
  const params = new URLSearchParams();
  if (from) params.set('from', from);
  if (Number.isFinite(y)) params.set('y', String(Math.round(y)));
  const suffix = params.toString();
  return base + (suffix ? '?' + suffix : '');
}
function selectedDictionaryWord() {
  const selection = getSelection()?.toString() || '';
  return dictWord(selection);
}
function goDictionary(word) {
  word = dictWord(word);
  if (!word) { if (window.notice) notice('请先选中一个英文单词。'); return; }
  location.hash = dictionaryHash(word);
}
function dictionarySection(title, rows, render) {
  if (!rows?.length) return '';
  return `<section class="dict-section"><h2>${escapeHTML(title)}</h2>${render(rows)}</section>`;
}
function dictionaryResult(data) {
  if (!data.found) return `<div class="dict-empty">没有查到 <strong>${escapeHTML(data.query)}</strong>。可以换成原形或更短的词头再试。</div>`;
  const entry = data.entry || {};
  const title = escapeHTML(data.resolved_word || data.query);
  const meta = data.query !== data.resolved_word ? `查询：${escapeHTML(data.query)} → ${title}` : `查询：${title}`;
  const tags = [entry.phonetic && `/${escapeHTML(entry.phonetic)}/`, entry.tag && escapeHTML(entry.tag), entry.bnc && `BNC ${entry.bnc}`, entry.frq && `FRQ ${entry.frq}`].filter(Boolean).join(' · ');
  return `<article class="dict-card">
    <p class="dict-meta">${meta}</p>
    <h1>${title}</h1>
    ${tags?`<p class="dict-tags">${tags}</p>`:''}
    ${entry.translation?`<section class="dict-section"><h2>中文解释</h2><p>${escapeHTML(entry.translation).replace(/\n/g,'<br>')}</p></section>`:''}
    ${entry.definition?`<section class="dict-section"><h2>英英解释</h2><p>${escapeHTML(entry.definition)}</p></section>`:''}
    ${dictionarySection('词根词缀', data.roots, rows=>`<ul>${rows.map(r=>`<li><strong>${escapeHTML(r.root)}</strong>${r.root_class?` <span class="dict-muted">${escapeHTML(r.root_class)}</span>`:''}：${escapeHTML(r.meaning||'')}</li>`).join('')}</ul>`)}
    ${dictionarySection('英英义项', data.senses, rows=>rows.map(s=>`<div class="dict-sense"><p><strong>${escapeHTML(s.pos)}</strong> ${escapeHTML(s.gloss)}</p>${s.synonyms?.length?`<p class="dict-muted">同义：${s.synonyms.map(escapeHTML).join(', ')}</p>`:''}${s.examples?.length?`<ul>${s.examples.map(e=>`<li>${escapeHTML(e)}</li>`).join('')}</ul>`:''}</div>`).join(''))}
    ${dictionarySection('词组搭配', data.phrases, rows=>`<ul>${rows.map(p=>`<li><strong>${escapeHTML(p.phrase)}</strong>：${escapeHTML(p.meaning)}${p.source_collections?.length?` <span class="dict-muted">${p.source_collections.map(escapeHTML).join(' / ')}</span>`:''}</li>`).join('')}</ul>`)}
    ${dictionarySection('例句', data.examples, rows=>`<ul>${rows.map(e=>`<li><p>${escapeHTML(e.english)}</p>${e.chinese?`<p class="dict-muted">${escapeHTML(e.chinese)}</p>`:''}</li>`).join('')}</ul>`)}
    ${dictionarySection('同义、反义与派生', data.relations, rows=>`<div class="dict-relations">${rows.map(r=>`<a href="${dictionaryHash(r.related_word)}"><span>${escapeHTML(r.relation)}</span>${escapeHTML(r.related_word)}</a>`).join('')}</div>`)}
    ${dictionarySection('联想辨析', data.resemble_notes, rows=>`<ul>${rows.map(r=>`<li><strong>${escapeHTML(r.group_key)}</strong>：${escapeHTML(r.note)}</li>`).join('')}</ul>`)}
  </article>`;
}
async function dictionaryView(raw) {
  state.current = null; state.knowledgeId = null; $('teach').hidden = true; $('dict-selection').hidden = true; $('source').textContent = '';
  const [path, queryString=''] = raw.split('?');
  const params = new URLSearchParams(queryString);
  const word = dictWord(path.split('/').slice(1).join(' '));
  const from = params.get('from') || '';
  const y = Number(params.get('y') || 0);
  $('breadcrumb').textContent = '查词典';
  $('chat-context').textContent = word ? `可以围绕 ${word} 问老师：词义差别、搭配、例句或翻译。` : '查一个词，再让老师按你的阅读问题讲。';
  $('article').innerHTML = `<section class="dict-page"><h1>查词典</h1><form id="dict-form" class="dict-form"><label class="sr-only" for="dict-query">输入单词</label><input id="dict-query" value="${escapeHTML(word)}" placeholder="输入单词，如 indignant / resigned"><button id="dict-submit" type="submit">查询</button></form>${from?`<p><a id="dict-back" href="#${encodeURIComponent(from)}">← 回到原文</a></p>`:''}<div id="dict-result">${word?'正在查询…':'输入一个词开始查询。'}</div></section>`;
  if (from) $('dict-back').onclick=()=>{sessionStorage.setItem('english-dictionary-return-y', JSON.stringify({id:from,y}));};
  async function lookup(nextWord) {
    nextWord = dictWord(nextWord);
    if (!nextWord) return;
    $('dict-result').innerHTML = '正在查询…';
    const data = await api('/api/dictionary/lookup?word='+encodeURIComponent(nextWord)+'&examples=8&phrases=20&relations=60&senses=20&notes=20');
    $('dict-result').innerHTML = dictionaryResult(data);
    $('dict-query').value = nextWord;
  }
  $('dict-form').onsubmit=e=>{e.preventDefault();const next=dictWord($('dict-query').value);if(next)location.hash=dictionaryHash(next,from,y);};
  if (word) {
    try { await lookup(word); }
    catch (err) { $('dict-result').innerHTML = `<div class="dict-empty">${escapeHTML(err.message)}</div>`; }
  }
}
function nav() {
  const course=state.course.topics||[], chosen=new Set(course.flatMap(t=>t.lessons.map(l=>l.path)));
  const link=(id,title)=>`<a class="nav-link ${id===state.current?.id?'active':''}" href="#${encodeURIComponent(id)}">${escapeHTML(title)}</a>`;
  const cur=state.current?.id, topicMatch=(location.hash.match(/^#topics\/([^/]+)/)||[])[1]||'';
  const fold=(open,title,count,inner)=>`<details class="nav-fold" ${open?'open':''}><summary><span class="nav-fold-title">${escapeHTML(title)}</span><span class="nav-fold-count">${count}</span></summary>${inner}</details>`;
  const rest=state.items.filter(x=>!chosen.has(x.id)&&!x.hidden);
  const sec=s=>rest.filter(x=>x.section===s);
  const subgroup=xs=>{const m=new Map();xs.forEach(x=>{if(!m.has(x.group))m.set(x.group,[]);m.get(x.group).push(x)});return [...m].map(([g,ys])=>fold(ys.some(y=>y.id===cur),g,ys.length,ys.map(y=>link(y.id,y.title)).join(''))).join('')};
  let html=course.map(t=>fold(t.id===topicMatch||t.lessons.some(l=>l.path===cur),t.title,t.lessons.length+'章',t.lessons.map(l=>link(l.path,l.title)).join(''))).join('');
  $('nav').innerHTML=html;
  let doc='';
  for(const [s,title,nested] of [['archive','学习档案'],['engineering','工程文档',true],['progress','进度与诊断'],['reference','参考资料',true],['history','历史课堂'],['book-extra','Book 其他章节',true]]) {
    const xs=sec(s); if(!xs.length) continue;
    doc+=fold(xs.some(x=>x.id===cur),title,xs.length,nested?subgroup(xs):xs.map(x=>link(x.id,x.title)).join(''));
  }
  $('docnav').innerHTML=doc;
}
function topicHome(selected=''){
  state.current=null;state.knowledgeId=null;$('teach').hidden=true;$('source').textContent='';
  $('breadcrumb').textContent='主页';$('chat-context').textContent='选择一章开始。老师会结合当前专题和你的背景讲解。';
  const topics=state.course.topics||[],all=topics.flatMap(t=>t.lessons),first=all.find(l=>l.path===state.course.start),last=all.find(l=>l.path===localStorage.getItem('english-last-lesson'));
  const shown=selected?topics.filter(t=>t.id===selected):topics;
  const feature=state.course.featured||{};
  const start=first?`<section class="topic-start"><div class="eyebrow">${escapeHTML(feature.label||'建议从这里开始')}</div><h2>${escapeHTML(first.title)}</h2>${feature.sample?`<p class="topic-example">${escapeHTML(feature.sample)}</p>`:''}<p>${escapeHTML(feature.question||first.focus)}</p><a class="start-lesson" href="#${encodeURIComponent(first.path)}">开始这一章 →</a>${last?`<a class="resume-lesson" href="#${encodeURIComponent(last.path)}">继续上次阅读：${escapeHTML(last.title)}</a>`:''}</section>`:'';
  $('article').innerHTML=`<div class="topic-intro"><h1>按专题读懂英语</h1><p>从一句卡住你的英文出发，弄清词义、组合和结构，再到新语境中使用。</p></div>${selected?'':start}<div class="topic-tabs"><a href="#topics">全部专题</a>${topics.map(t=>`<a href="#topics/${t.id}" ${selected===t.id?'aria-current="page"':''}>${escapeHTML(t.title)}</a>`).join('')}</div><div class="topic-sections">${shown.map(t=>`<section class="topic-section"><div class="topic-section-head"><h2>${escapeHTML(t.title)}</h2><span>${t.lessons.length}章</span></div><p class="topic-question">${escapeHTML(t.question)}</p>${t.lessons.map(l=>`<a class="topic-lesson" href="#${encodeURIComponent(l.path)}"><div><strong>${escapeHTML(l.title)}</strong><p>${escapeHTML(l.focus)}</p></div><span>${escapeHTML(l.level)} →</span></a>`).join('')}</section>`).join('')||'<p>专题不存在，请返回全部专题。</p>'}</div><p class="topic-footnote">按需要选章即可。“回顾／深化／进阶”描述内容定位，不是对你的能力评分。<a href="#book/README.md">关于本书 →</a></p>`;
  nav();
}
function route() {
  $('search').value = '';
  let id; try { id=decodeURIComponent(location.hash.slice(1)); } catch { id=''; }
  state.knowledgeId = null;
  $('chapter-learning').innerHTML = '';
  if (window.learningRoute && window.learningRoute(id)) return;
  if(id==='dictionary'||id.startsWith('dictionary/')){dictionaryView(id);return;}
  if(!id||id==='topics'||id.startsWith('topics/')){topicHome(id.split('/')[1]||'');return;}
  state.current = state.items.find(x=>x.id===id) || state.items.find(x=>x.id==='book/01-reading/01-context.md') || state.items[0];
  if (!state.current) return;
  const item = state.current, parts = item.body.split(/^## 参考答案\s*$/m);
  $('article').innerHTML = markdown(parts[0],item.id) + (parts.length>1 ? `<details><summary>查看参考答案</summary>${markdown(parts.slice(1).join('\n'),item.id)}</details>` : '');
  $('breadcrumb').textContent = item.group + ' / ' + item.title;
  $('chat-context').textContent = '本次提问将附上：' + item.title;
  $('source').textContent = '教材来源 · english/' + item.id + ' · 阅读不自动计为掌握';
  $('teach').hidden = false; nav();
  $('dict-selection').hidden = false;
  if(item.lesson){localStorage.setItem('english-last-lesson',item.id);$('breadcrumb').textContent=item.lesson.topic+' / '+item.lesson.title;}
  if(window.attachLearning) window.attachLearning(item.id);
  try {
    const back = JSON.parse(sessionStorage.getItem('english-dictionary-return-y')||'null');
    if (back?.id === item.id) { sessionStorage.removeItem('english-dictionary-return-y'); setTimeout(()=>scrollTo(0, Number(back.y)||0), 0); }
  } catch { sessionStorage.removeItem('english-dictionary-return-y'); }
}
async function loadBook() {
  const data = await api('/api/catalog'); state.items=data.items; state.course=data.course||{topics:[]}; state.token=data.token;
  $('connection').textContent = data.codex ? '通过本机 Codex 回复 · 使用当前登录账户 · 对话保存在本地' : '未找到 Codex CLI，请在本机安装并登录。'; route();
}
async function histories() {
  const list = await api('/api/sessions');
  $('history').innerHTML = '<option value="">本次新对话</option>' + list.map(s=>`<option value="${s.id}">${escapeHTML(s.title || '未命名对话')}</option>`).join('');
  $('history').value = state.session;
}
function renderChat(session) {
  $('messages').innerHTML = session.messages.length ? session.messages.map(m=>`<div class="message ${m.role==='user'?'user':'assistant'}"><div class="role">${m.role==='user'?'你':'老师'}</div><div class="body">${m.role==='user'?escapeHTML(m.content):markdown(m.content,state.current?.id || 'book/README.md')}</div></div>`).join('') : '<div class="empty"><strong>从你卡住的地方开始。</strong>可以问：“be resigned to 和 accept 有什么区别？”或提交本章练习答案。</div>';
  $('messages').scrollTop = $('messages').scrollHeight;
  const busy = session.status === 'running';
  $('send').disabled = busy; $('send').textContent = busy ? '思考中…' : '发送';
  $('chat-status').textContent = busy ? '老师正在结合你的背景与问题组织回复，可继续阅读。' : (session.error || '');
  $('retry').hidden = session.status !== 'error';
}
function stopPoll() { if (state.timer) clearTimeout(state.timer); state.timer=null; }
async function poll(sid) {
  if (state.session!==sid) return;
  try {
    const session = await api('/api/session?id='+sid); if (state.session!==sid) return;
    renderChat(session);
    if (session.status==='running') state.timer=setTimeout(()=>poll(sid),1800); else await histories();
  } catch (err) { $('chat-status').textContent=err.message; $('send').disabled=false; }
}
async function send(retry=false) {
  if (state.sending) return;
  const message=$('question').value.trim(); if (!retry && !message) return;
  state.sending=true; $('send').disabled=true; $('new-chat').disabled=true; $('history').disabled=true;
  try {
    const session=await api('/api/chat',{method:'POST',headers:{'Content-Type':'application/json','X-English-Token':state.token},body:JSON.stringify({message,session:state.session,chapter:state.current?.id,knowledge_id:state.knowledgeId,retry})});
    state.session=session.id; localStorage.setItem('english-session',session.id);
    if (!retry) $('question').value=''; renderChat(session); stopPoll();
    state.timer=setTimeout(()=>poll(session.id),1000); await histories();
  } catch (err) { $('chat-status').textContent=err.message; $('send').disabled=false; }
  finally {state.sending=false; $('new-chat').disabled=false; $('history').disabled=false;}
}
$('chat-form').addEventListener('submit',e=>{e.preventDefault();send();});
$('question').addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key==='Enter'){e.preventDefault();if(!$('send').disabled)send();}});
$('retry').onclick=()=>send(true);
$('new-chat').onclick=()=>{stopPoll();state.session='';localStorage.removeItem('english-session');$('history').value='';renderChat({messages:[],status:'ready'});};
$('history').onchange=()=>{stopPoll();state.session=$('history').value;localStorage.setItem('english-session',state.session);state.session?poll(state.session):renderChat({messages:[],status:'ready'});};
$('teach').onclick=()=>{$('question').value='请按我的背景带我学习这一章。先选一个有上下文的例子，聚焦一个关键表达；不要把已经讲过的内容当作新诊断。';$('question').focus();$('question').scrollIntoView({block:'nearest'});};
$('dict-selection').onclick=()=>goDictionary(selectedDictionaryWord());
$('search').oninput=()=>{
  const query=$('search').value.trim().toLowerCase(); if(!query)return route();
  const results=state.items.filter(x=>(x.title+'\n'+x.body).toLowerCase().includes(query));
  $('article').innerHTML=`<h1>搜索知识书</h1><p>${results.length} 个结果</p>`+results.map(x=>{const at=x.body.toLowerCase().indexOf(query);return `<a class="search-result" href="#${encodeURIComponent(x.id)}"><strong>${escapeHTML(x.title)}</strong><small>${escapeHTML(x.body.slice(Math.max(0,at-30),Math.max(0,at-30)+150))}</small></a>`;}).join('');
  $('breadcrumb').textContent='全文搜索';$('source').textContent='';$('teach').hidden=true;
};
$('article').addEventListener('click',e=>{if(e.target.closest('a')?.hash===location.hash)route();});
$('article').addEventListener('dblclick',()=>setTimeout(()=>{const word=selectedDictionaryWord();if(word&&state.current)goDictionary(word);},0));
$('nav').addEventListener('click',e=>{if(e.target.closest('a')?.hash===location.hash)route();});
$('refresh').onclick=()=>loadBook().catch(e=>$('chat-status').textContent=e.message);
$('theme').onclick=()=>{const current=document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');const next=current==='dark'?'light':'dark';document.documentElement.dataset.theme=next;localStorage.setItem('english-theme',next);};
if(localStorage.getItem('english-theme'))document.documentElement.dataset.theme=localStorage.getItem('english-theme');
addEventListener('hashchange',route);
(async()=>{try{await loadBook();state.session=localStorage.getItem('english-session')||'';await histories();if(state.session)await poll(state.session);else renderChat({messages:[],status:'ready'});}catch(e){$('article').textContent=e.message;}})();
