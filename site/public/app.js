'use strict';
const $ = id => document.getElementById(id);
const state = {items: [], nav: {groups:[]}, current: null};

function fixAssets(contentEl, docPath) {
  // markdown 里的相对路径：图片改走 /files/，文档链接改成 hash 深链
  const dir = docPath.includes('/') ? docPath.slice(0, docPath.lastIndexOf('/')) : '';
  const resolve = rel => {
    try { return decodeURIComponent(new URL(rel, 'https://book.local/' + (dir ? dir + '/' : '')).pathname.slice(1)); }
    catch { return ''; }
  };
  contentEl.querySelectorAll('img').forEach(img => {
    const src = img.getAttribute('src') || '';
    if (/^(https?:|data:|\/\/|#)/i.test(src)) return;
    img.src = '/files/' + resolve(src);
  });
  contentEl.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (/^(https?:|data:|\/\/|#|mailto:)/i.test(href)) return;
    if (href.toLowerCase().endsWith('.md')) a.href = '#' + encodeURIComponent(resolve(href));
  });
}

function renderDoc(item) {
  const parts = item.body.split(/^## 参考答案\s*$/m);
  const contentEl = document.createElement('div');
  contentEl.innerHTML = marked.parse(parts[0], {gfm: true});
  if (window.hljs) contentEl.querySelectorAll('pre code').forEach(el => hljs.highlightElement(el));
  fixAssets(contentEl, item.id);
  let html = contentEl.innerHTML;
  if (parts.length > 1) {
    const answerEl = document.createElement('div');
    answerEl.innerHTML = marked.parse(parts.slice(1).join('\n'), {gfm: true});
    fixAssets(answerEl, item.id);
    html += `<details><summary>查看参考答案</summary>${answerEl.innerHTML}</details>`;
  }
  return html;
}

function nav() {
  const link=(id,title)=>`<a class="nav-link ${id===state.current?.id?'active':''}" href="#${encodeURIComponent(id)}">${title}</a>`;
  const fold=(open,title,count,inner)=>`<details class="nav-fold" ${open?'open':''}><summary><span class="nav-fold-title">${title}</span><span class="nav-fold-count">${count}</span></summary>${inner}</details>`;
  const byId={}; state.items.forEach(x=>byId[x.id]=x);
  const cur=state.current?.id;
  const itemHTML=(id)=>{const x=byId[id];return x?link(x.id,x.title):''};
  let html='';
  for(const group of (state.nav.groups||[])) {
    const renderItems=(items)=>items.map(it=>typeof it==='string'?itemHTML(it):`<div class="nav-sub">${it.sub}</div>`+it.items.map(itemHTML).join('')).join('');
    const entries=group.items.flatMap(it=>typeof it==='string'?[it]:it.items);
    html+=fold(entries.some(id=>id===cur),group.title,entries.length,renderItems(group.items));
  }
  $('nav').innerHTML=html;
}

function route() {
  $('search').value = '';
  let id; try { id=decodeURIComponent(location.hash.slice(1)); } catch { id=''; }
  state.current = state.items.find(x=>x.id===id) || state.items[0];
  if (!state.current) return;
  const item = state.current;
  $('article').innerHTML = renderDoc(item);
  $('breadcrumb').textContent = item.group + ' / ' + item.title;
  $('source').textContent = 'english/' + item.id;
  nav();
}

async function loadBook() {
  const response = await fetch('/api/catalog');
  if (!response.ok) throw new Error('目录加载失败，请刷新重试。');
  const data = await response.json();
  state.items = data.items; state.nav = data.nav || {groups:[]};
  route();
}

$('search').oninput=()=>{
  const query=$('search').value.trim().toLowerCase(); if(!query)return route();
  const results=state.items.filter(x=>(x.title+'\n'+x.body).toLowerCase().includes(query));
  $('article').innerHTML=`<h1>搜索知识书</h1><p>${results.length} 个结果</p>`+results.map(x=>{const at=x.body.toLowerCase().indexOf(query);return `<a class="search-result" href="#${encodeURIComponent(x.id)}"><strong>${x.title}</strong><small>${x.body.slice(Math.max(0,at-30),Math.max(0,at-30)+150)}</small></a>`;}).join('');
  $('breadcrumb').textContent='全文搜索';$('source').textContent='';
};
$('article').addEventListener('click',e=>{if(e.target.closest('a')?.hash===location.hash)route();});
$('nav').addEventListener('click',e=>{if(e.target.closest('a')?.hash===location.hash)route();if(e.target.closest('a'))e.target.closest('details')?.setAttribute('open','');});
$('theme').onclick=()=>{const current=document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');const next=current==='dark'?'light':'dark';document.documentElement.dataset.theme=next;localStorage.setItem('english-theme',next);};
if(localStorage.getItem('english-theme'))document.documentElement.dataset.theme=localStorage.getItem('english-theme');
addEventListener('hashchange',route);
(async()=>{try{await loadBook();}catch(e){$('article').textContent=e.message;}})();
