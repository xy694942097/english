'use strict';
const $ = id => document.getElementById(id);
const state = {items: [], nav: {groups:[]}, aliases: {}, current: null, searching: false};

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
    const [path, anchor=''] = href.split('#');
    if (path.toLowerCase().endsWith('.md')) {
      let decoded = anchor; try { decoded = decodeURIComponent(anchor); } catch {}
      a.href = docHash(resolve(path), decoded);
    }
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
    html += `<details class="reference-answers"><summary>查看参考答案</summary><h2>参考答案</h2>${answerEl.innerHTML}</details>`;
  }
  return html;
}

function headingSlug(text) {
  return text.toLowerCase().trim().replace(/[^\p{L}\p{N}\p{M}\s_-]/gu, '').replace(/\s/g, '-');
}

function docHash(id, anchor='') {
  return '#' + encodeURIComponent(id) + (anchor ? '::' + encodeURIComponent(anchor) : '');
}

function addDocumentContents(item) {
  const article = $('article');
  const counts = new Map();
  const headings = [...article.querySelectorAll('h1,h2,h3,h4,h5,h6')];
  const used = new Set(headings.filter(h => h.id).map(h => h.id));
  headings.forEach(h => {
    if (h.id) return;
    const slug = headingSlug(h.textContent) || 'section';
    let count = counts.get(slug) || 0;
    while (used.has(count ? `${slug}-${count}` : slug)) count++;
    counts.set(slug, count + 1);
    h.id = count ? `${slug}-${count}` : slug;
    used.add(h.id);
  });
  const entries = headings.filter(h => /^H[23]$/.test(h.tagName));
  if (!entries.length) return;
  const toc = document.createElement('details');
  toc.className = 'document-toc';
  toc.open = entries.length <= 20;
  const summary = document.createElement('summary');
  summary.textContent = '本文目录';
  toc.append(summary);
  const list = document.createElement('ul');
  entries.forEach(h => {
    const li = document.createElement('li');
    li.className = h.tagName === 'H3' ? 'toc-subsection' : '';
    const link = document.createElement('a');
    link.textContent = h.textContent;
    link.href = docHash(item.id, h.id);
    li.append(link); list.append(li);
  });
  toc.append(list);
  const title = article.querySelector('h1');
  if (title) title.after(toc); else article.prepend(toc);
  article.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href');
    if (href?.startsWith('#') && !href.includes('::')) {
      let anchor; try { anchor = decodeURIComponent(href.slice(1)); } catch { return; }
      if ([...article.querySelectorAll('[id]')].some(el => el.id === anchor)) a.href = docHash(item.id, anchor);
    }
  });
}

function scrollToSection(anchor) {
  if (!anchor) { window.scrollTo(0, 0); return; }
  const target = [...$('article').querySelectorAll('[id]')].find(el => el.id === anchor);
  if (!target) return;
  for (let p=target.parentElement; p && p!==$('article'); p=p.parentElement) {
    if (p.tagName === 'DETAILS') p.open = true;
  }
  target.scrollIntoView({block:'start'});
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
  for(const group of (state.nav.maintenance||[])) {
    const entries=group.items.flatMap(it=>typeof it==='string'?[it]:it.items);
    html+=`<details class="nav-maintenance" ${entries.includes(cur)?'open':''}><summary>${group.title}</summary>${entries.map(itemHTML).join('')}</details>`;
  }
  $('nav').innerHTML=html;
}

function route() {
  $('search').value = '';
  const [rawId, rawAnchor=''] = location.hash.slice(1).split('::');
  let id, anchor; try { id=decodeURIComponent(rawId); anchor=decodeURIComponent(rawAnchor); } catch { id=''; anchor=''; }
  if (state.aliases[id] && state.items.some(x => x.id === state.aliases[id])) {
    id = state.aliases[id];
    history.replaceState(null, '', docHash(id, anchor));
  }
  const item = state.items.find(x=>x.id===id) || state.items[0];
  if (item && state.current?.id === item.id && !state.searching) {
    scrollToSection(anchor); return;
  }
  state.current = item;
  state.searching = false;
  if (!state.current) return;
  $('article').innerHTML = renderDoc(item);
  addDocumentContents(item);
  $('breadcrumb').textContent = item.group + ' / ' + item.title;
  $('source').textContent = 'english/' + item.id;
  nav();
  scrollToSection(anchor);
}

async function loadBook() {
  const response = await fetch('/api/catalog');
  if (!response.ok) throw new Error('目录加载失败，请刷新重试。');
  const data = await response.json();
  state.items = data.items; state.nav = data.nav || {groups:[]}; state.aliases = data.aliases || {};
  route();
}

$('search').oninput=()=>{
  const query=$('search').value.trim().toLowerCase(); if(!query)return route();
  state.searching = true;
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
