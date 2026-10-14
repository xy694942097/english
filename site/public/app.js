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
    img.src = './files/' + resolve(src);
  });
  contentEl.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (/^(https?:|data:|\/\/|#|mailto:)/i.test(href)) return;
    const [path, anchor=''] = href.split('#');
    if (path.toLowerCase().endsWith('.md')) {
      let decoded = anchor; try { decoded = decodeURIComponent(anchor); } catch {}
      const resolved = resolve(path);
      const id = state.aliases[resolved] || resolved;
      if (!state.items.some(item => item.id === id)) {
        a.removeAttribute('href');
        a.title = '这份资料未在当前站点展示';
        return;
      }
      a.href = docHash(id, decoded);
    }
  });
}

function renderMarkdownPart(source) {
  const contentEl = document.createElement('div');
  contentEl.innerHTML = marked.parse(source, {gfm: true});
  return contentEl;
}

function renderDoc(item) {
  const answer = /^## (参考答案|参考 Chunk)\s*$/m.exec(item.body);
  const contentEl = renderMarkdownPart(answer ? item.body.slice(0, answer.index) : item.body, 0);
  if (window.hljs) contentEl.querySelectorAll('pre code').forEach(el => hljs.highlightElement(el));
  fixAssets(contentEl, item.id);
  let html = contentEl.innerHTML;
  if (answer) {
    const answerStart = answer.index + answer[0].length;
    const answerEl = renderMarkdownPart(item.body.slice(answerStart), answerStart);
    fixAssets(answerEl, item.id);
    const label = answer[1];
    html += `<details class="reference-answers"><summary>查看${label}</summary><h2>${label}</h2>${answerEl.innerHTML}</details>`;
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
  const list = document.createElement('ul');
  entries.forEach(h => {
    const li = document.createElement('li');
    li.className = h.tagName === 'H3' ? 'toc-subsection' : '';
    const link = document.createElement('a');
    link.textContent = h.textContent;
    link.href = docHash(item.id, h.id);
    li.append(link); list.append(li);
  });
  $('outline-links').replaceChildren(list);
  $('right-toggle').hidden = entries.length === 0;
  if (!entries.length) closeOutline();
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

function foldDocumentSections() {
  const article = $('article');
  const nodes = [...article.childNodes];
  const stack = [];
  let count = 0;
  nodes.forEach(node => {
    const heading = node.nodeType === Node.ELEMENT_NODE && /^H[2-6]$/.test(node.tagName);
    if (heading) {
      const level = Number(node.tagName.slice(1));
      while (stack.length && stack.at(-1).level >= level) stack.pop();
      const section = document.createElement('details');
      section.className = 'section-fold';
      section.open = true;
      const summary = document.createElement('summary');
      summary.append(node);
      section.append(summary);
      const content = document.createElement('div');
      content.className = 'section-content';
      section.append(content);
      (stack.length ? stack.at(-1).content : article).append(section);
      stack.push({level, content});
      count++;
    } else if (stack.length && !(node.nodeType === Node.ELEMENT_NODE && node.classList.contains('reference-answers'))) {
      stack.at(-1).content.append(node);
    } else {
      stack.length = 0;
      article.append(node);
    }
  });
  if (!count) return;
  const controls = document.createElement('div');
  controls.className = 'section-controls';
  for (const [label, open] of [['展开正文', true], ['收起正文', false]]) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.onclick = () => article.querySelectorAll('.section-fold').forEach(section => {section.open = open;});
    controls.append(button);
  }
  article.querySelector('h1')?.after(controls);
}

function closeOutline() {
  $('outline').hidden = true;
  document.body.classList.add('right-collapsed');
  const toggle = $('right-toggle');
  toggle.textContent = '☷';
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-label', '展开目录');
  toggle.dataset.tip = '展开目录';
}

function toggleOutline() {
  if ($('outline').hidden) {
    $('outline').hidden = false;
    document.body.classList.remove('right-collapsed');
    const toggle = $('right-toggle');
    toggle.textContent = '›';
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', '收起目录');
    toggle.dataset.tip = '收起目录';
  } else closeOutline();
}

function setLeftSidebarOpen(open) {
  document.body.classList.toggle('left-collapsed', !open);
  const toggle = $('left-toggle');
  toggle.textContent = open ? '‹' : '›';
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? '收起左侧导航' : '展开左侧导航');
  toggle.dataset.tip = open ? '收起左侧导航' : '展开左侧导航';
  $('mobile-nav').setAttribute('aria-expanded', String(open));
  $('nav-backdrop').hidden = !open || !matchMedia('(max-width: 760px)').matches;
  if (!matchMedia('(max-width: 760px)').matches)
    localStorage.setItem('english-left-sidebar', open ? 'open' : 'closed');
}

function nav() {
  const link=(id,title)=>`<a class="nav-link ${id===state.current?.id?'active':''}" href="#${encodeURIComponent(id)}">${title}</a>`;
  const fold=(open,title,count,inner)=>`<details class="nav-fold" ${open?'open':''}><summary><span class="nav-fold-title">${title}</span><span class="nav-fold-count">${count}</span></summary>${inner}</details>`;
  const byId={}; state.items.forEach(x=>byId[x.id]=x);
  const cur=state.current?.id;
  const itemHTML=(id)=>{const x=byId[id];return x?link(x.id,x.title):''};
  const renderItems=(items)=>items.map(it=>typeof it==='string'?itemHTML(it):`<div class="nav-sub">${it.sub}</div>`+it.items.map(itemHTML).join('')).join('');
  let html=`<a class="nav-home ${!state.current && !state.searching ? 'active' : ''}" href="#">首页</a>`;
  for(const group of (state.nav.groups||[])) {
    const entries=group.items.flatMap(it=>typeof it==='string'?[it]:it.items);
    html+=fold(entries.some(id=>id===cur),group.title,entries.length,renderItems(group.items));
  }
  for(const group of (state.nav.maintenance||[])) {
    const entries=group.items.flatMap(it=>typeof it==='string'?[it]:it.items);
    html+=`<details class="nav-maintenance" ${entries.includes(cur)?'open':''}><summary>${group.title}</summary>${renderItems(group.items)}</details>`;
  }
  $('nav').innerHTML=html;
}

function showHome() {
  state.current = null;
  state.searching = false;
  $('search').value = '';
  closeOutline();
  $('right-toggle').hidden = true;
  $('outline-links').replaceChildren();
  $('breadcrumb').textContent = '首页';
  $('source').textContent = '';
  const article = $('article');
  article.classList.add('home-page');
  article.replaceChildren();
  const element = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const byId = new Map(state.items.map(item => [item.id, item]));
  const link = (item, className) => {
    const anchor = element('a', item.title, className);
    anchor.href = docHash(item.id);
    return anchor;
  };
  const lead = element('header', '', 'home-lead');
  lead.append(element('p', 'ENGLISH BOOK', 'home-label'),
    element('h1', '读懂整句，也把意思说出来。'),
    element('p', '积累 Chunks 和词汇，在外部视频中做 Shadowing，记录练习并逐渐用熟。', 'home-intro'));
  const actions = element('div', '', 'home-actions');
  for (const [id, label, className] of [
    ['course/Chunks 收集/精选 Chunks.md', '阅读精选 Chunks', 'home-primary'],
    ['course/Shadowing/Shadowing 记录.md', '记录 Shadowing', 'home-secondary'],
  ]) {
    const item = byId.get(id);
    if (!item) continue;
    const anchor = link(item, className); anchor.textContent = label; actions.append(anchor);
  }
  lead.append(actions); article.append(lead);
  article.append(element('h2', '选择想看的内容', 'home-directory-title'));
  const descriptions = {
    '词汇': '熟词的新意思、生词和常用接法，放回句子中理解。',
    'Chunks 收集': '精选表达与作品中的词块积累，从整块意思进入。',
    'Shadowing': '在 YouTube 等外部播放器跟读，这里记录真实练习。',
    '原文与参考资料': '影视、演讲、教材和语法资料，按阅读需要查阅。',
    '我的学习': '学习背景、方法与当前记录。',
    '编纂与维护': '资料来源、编纂规则，以及教学和出题 Skills。',
  };
  const grid = element('div', '', 'home-grid');
  for (const group of [...state.nav.groups, ...(state.nav.maintenance || [])]) {
    const ids = group.items.flatMap(entry => typeof entry === 'string' ? [entry] : entry.items);
    const items = ids.map(id => byId.get(id)).filter(Boolean);
    if (!items.length) continue;
    const section = element('section', '', 'home-section');
    const heading = element('div', '', 'home-section-heading');
    heading.append(element('h3', group.title), element('span', `${items.length} 篇`, 'home-count'));
    section.append(heading, element('p', descriptions[group.title] || '浏览这个分区的阅读文档。'));
    const list = element('ul');
    const previews = items.slice(0, 3);
    if (group.title === '编纂与维护') {
      const skill = items.find(item => item.id.includes('/Skills/'));
      if (skill && !previews.includes(skill)) previews[previews.length - 1] = skill;
    }
    for (const item of previews) { const row = element('li'); row.append(link(item)); list.append(row); }
    section.append(list);
    if (items.length > previews.length) {
      const more = element('button', '查看全部', 'home-more'); more.type = 'button';
      more.onclick = () => {
        const entry = [...$('nav').querySelectorAll('details')].find(node =>
          node.querySelector('summary')?.textContent.trim().startsWith(group.title));
        if (entry) { entry.open = true; setLeftSidebarOpen(true); entry.scrollIntoView({block: 'nearest'}); }
      };
      section.append(more);
    }
    grid.append(section);
  }
  article.append(grid, element('p', '可以直接阅读，也可以用顶部搜索查找词汇、Chunks 或材料。', 'home-note'));
  nav();
  window.scrollTo(0, 0);
}

function route({force = false, preserveScroll = false, fromHash = false} = {}) {
  const previousScroll = window.scrollY;
  const [rawId, rawAnchor=''] = location.hash.slice(1).split('::');
  let id, anchor; try { id=decodeURIComponent(rawId); anchor=decodeURIComponent(rawAnchor); } catch { id=''; anchor=''; }
  if (state.aliases[id] && state.items.some(x => x.id === state.aliases[id])) {
    id = state.aliases[id];
    history.replaceState(null, '', docHash(id, anchor));
  }
  if (!id || id === 'home') { showHome(); return; }
  const item = state.items.find(x=>x.id===id);
  // A delayed anchor event must not erase text entered into search meanwhile.
  if (fromHash && state.searching && rawAnchor && item?.id === state.current?.id) return;
  $('search').value = '';
  if (item && state.current?.id === item.id && !state.searching && !force) {
    scrollToSection(anchor); return;
  }
  state.current = item;
  state.searching = false;
  $('article').classList.remove('home-page');
  if (!state.current) {
    $('article').replaceChildren();
    const title = document.createElement('h1'); title.textContent = '未找到这篇文章';
    const back = document.createElement('a'); back.href = '#'; back.textContent = '返回首页';
    $('article').append(title, back); closeOutline(); $('right-toggle').hidden = true;
    $('breadcrumb').textContent = '文章未找到'; $('source').textContent = ''; nav(); return;
  }
  $('article').innerHTML = renderDoc(item);
  addDocumentContents(item);
  foldDocumentSections();
  $('breadcrumb').textContent = item.group + ' / ' + item.title;
  $('source').textContent = 'english/' + item.id;
  nav();
  if (preserveScroll) window.scrollTo(0, previousScroll);
  else scrollToSection(anchor);
}

async function loadBook() {
  const response = await fetch('./catalog.json');
  if (!response.ok) throw new Error('目录加载失败，请刷新重试。');
  const data = await response.json();
  state.items = data.items; state.nav = data.nav || {groups:[]}; state.aliases = data.aliases || {};
  route();
}

$('search').oninput=()=>{
  const query=$('search').value.trim().toLowerCase(); if(!query)return route();
  state.searching = true;
  $('article').classList.remove('home-page');
  closeOutline();
  $('right-toggle').hidden = true;
  const results=state.items.filter(x=>(x.title+'\n'+x.body).toLowerCase().includes(query));
  $('article').innerHTML=`<h1>搜索知识书</h1><p>${results.length} 个结果</p>`+results.map(x=>{const at=x.body.toLowerCase().indexOf(query);return `<a class="search-result" href="#${encodeURIComponent(x.id)}"><strong>${x.title}</strong><small>${x.body.slice(Math.max(0,at-30),Math.max(0,at-30)+150)}</small></a>`;}).join('');
  $('breadcrumb').textContent='全文搜索';$('source').textContent='';
};
document.querySelector('.brand').addEventListener('click', () => {if (!location.hash || location.hash === '#') showHome();});
$('article').addEventListener('click', e => {
  if (e.target.closest('a')?.hash === location.hash) route();
});
$('nav').addEventListener('click',e=>{if(e.target.closest('a')?.hash===location.hash)route();if(e.target.closest('a')){e.target.closest('details')?.setAttribute('open','');if(matchMedia('(max-width:760px)').matches)setLeftSidebarOpen(false);}});
$('right-toggle').onclick = toggleOutline;
$('left-toggle').onclick = () => setLeftSidebarOpen(document.body.classList.contains('left-collapsed'));
$('mobile-nav').onclick = $('left-toggle').onclick;
$('nav-backdrop').onclick = () => setLeftSidebarOpen(false);
$('outline-links').addEventListener('click', e => { if (e.target.closest('a')) closeOutline(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') {closeOutline();if(matchMedia('(max-width:760px)').matches)setLeftSidebarOpen(false);} });
const mobileViewport = matchMedia('(max-width:760px)');
setLeftSidebarOpen(!mobileViewport.matches && localStorage.getItem('english-left-sidebar') !== 'closed');
mobileViewport.addEventListener('change', () => setLeftSidebarOpen(!mobileViewport.matches && localStorage.getItem('english-left-sidebar') !== 'closed'));
new ResizeObserver(() => document.documentElement.style.setProperty('--topbar-height', document.querySelector('.topbar').offsetHeight + 'px')).observe(document.querySelector('.topbar'));
closeOutline();
$('theme').onclick=()=>{const current=document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');const next=current==='dark'?'light':'dark';document.documentElement.dataset.theme=next;localStorage.setItem('english-theme',next);};
if(localStorage.getItem('english-theme'))document.documentElement.dataset.theme=localStorage.getItem('english-theme');
addEventListener('hashchange', () => route({fromHash: true}));
(async()=>{try{await loadBook();}catch(e){$('article').textContent=e.message;}})();
