'use strict';
const $ = id => document.getElementById(id);
const state = {items: [], nav: {groups:[]}, aliases: {}, current: null, searching: false, editing: null, sectionPicker: null};
let editorAssetsPromise;
const LARGE_DOCUMENT_CHARS = 80_000;
const TARGET_SECTION_CHARS = 32_000;

function editorAssets() {
  if (editorAssetsPromise) return editorAssetsPromise;
  for (const file of ['toastui-editor.css', 'toastui-editor-dark.css']) {
    const link = document.createElement('link');
    link.rel = 'stylesheet'; link.href = '/vendor/toastui/' + file;
    if (file.includes('dark')) link.id = 'editor-dark-css';
    document.head.append(link);
  }
  const loadScript = src => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src; script.onload = resolve; script.onerror = reject;
    document.head.append(script);
  });
  editorAssetsPromise = loadScript('/vendor/toastui/editor-bundle.js')
    .then(() => loadScript('/vendor/toastui/zh-cn.js'))
    .catch(error => { editorAssetsPromise = undefined; throw error; });
  return editorAssetsPromise;
}

function preloadEditorAssets() {
  const prepare = () => editorAssets().catch(() => {});
  if ('requestIdleCallback' in window) requestIdleCallback(prepare, {timeout: 2500});
  else setTimeout(prepare, 1200);
}

function refreshEditorTheme() {
  const dark = (document.documentElement.dataset.theme ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')) === 'dark';
  $('edit-panel').classList.toggle('toastui-editor-dark', dark);
  $('markdown-editor').querySelector('.toastui-editor-defaultUI')?.classList.toggle('toastui-editor-dark', dark);
}

function updateEditDirty() {
  const editing = state.editing;
  if (!editing) return;
  editing.dirty = editing.editor.getMarkdown() !== editing.baseline;
  $('save-edit').disabled = !editing.dirty || editing.saving;
  $('edit-status').textContent = editing.dirty ? '有未保存的修改' : '尚无修改';
}

function markdownHeadings(body) {
  const headings = [];
  let offset = 0, fenceChar = '', fenceLength = 0;
  for (const line of body.match(/[^\n]*\n|[^\n]+$/g) || []) {
    const trimmed = line.trimEnd();
    const fence = /^ {0,3}(`{3,}|~{3,})(.*)$/.exec(trimmed);
    if (fence) {
      const marker = fence[1];
      if (!fenceChar) { fenceChar = marker[0]; fenceLength = marker.length; }
      else if (marker[0] === fenceChar && marker.length >= fenceLength && !fence[2].trim()) fenceChar = '';
    } else if (!fenceChar) {
      const heading = /^ {0,3}(#{1,6})[ \t]+(.+?)(?:[ \t]+#+)?$/.exec(trimmed);
      if (heading) headings.push({level: heading[1].length, title: heading[2].trim(), start: offset});
    }
    offset += line.length;
  }
  return headings;
}

function editableSections(body) {
  const headings = markdownHeadings(body);
  const byLevel = new Map();
  for (let i = 0; i < headings.length; i++) {
    const heading = headings[i];
    if (heading.level < 2) continue;
    let end = body.length;
    for (let j = i + 1; j < headings.length; j++) {
      if (headings[j].level <= heading.level) { end = headings[j].start; break; }
    }
    const sections = byLevel.get(heading.level) || [];
    sections.push({start: heading.start, end, title: heading.title});
    byLevel.set(heading.level, sections);
  }
  const candidates = [...byLevel].filter(([, sections]) => sections.length > 1)
    .sort(([a], [b]) => a - b);
  if (!candidates.length) return null;
  const choice = candidates.find(([, sections]) =>
    Math.max(...sections.map(section => section.end - section.start)) <= TARGET_SECTION_CHARS)
    || candidates.at(-1);
  return {level: choice[0], sections: choice[1]};
}

function exitSectionPicker() {
  state.sectionPicker?.headings.forEach(heading => heading.classList.remove('editable-heading'));
  state.sectionPicker = null;
  $('section-edit-tip').hidden = true;
  $('article').classList.remove('section-picking', 'pick-h2', 'pick-h3', 'pick-h4', 'pick-h5', 'pick-h6');
  $('edit-document').textContent = '编辑本文';
}

function enterSectionPicker(item) {
  const choice = editableSections(item.body);
  if (!choice) return false;
  const visible = [...$('article').querySelectorAll('.section-fold > summary > h' + choice.level)];
  const headingSections = new Map(), headings = [];
  const clean = text => text.replace(/\s+/g, ' ').trim();
  let cursor = 0;
  choice.sections.forEach(section => {
    const title = clean(section.title);
    let index = -1;
    for (let at = cursor; at < visible.length; at++) {
      if (clean(visible[at].textContent) === title) { index = at; break; }
    }
    if (index >= 0) {
      headingSections.set(visible[index], section);
      headings.push(visible[index]);
      cursor = index + 1;
    }
  });
  if (headings.length < 2) return false;
  headings.forEach(heading => heading.classList.add('editable-heading'));
  state.sectionPicker = {item, ...choice, headings, headingSections};
  $('section-edit-tip').hidden = false;
  $('article').classList.add('section-picking', 'pick-h' + choice.level);
  $('edit-document').textContent = '退出选节';
  editorAssets().catch(() => {});
  return true;
}

function restoreEditorPlacement() {
  $('edit-panel').classList.remove('section-edit');
  $('article').after($('edit-panel'));
}

async function beginEdit(section = null) {
  if (!state.current || state.editing) return;
  const item = state.current;
  if (!section && item.body.length >= LARGE_DOCUMENT_CHARS && enterSectionPicker(item)) return;
  $('edit-document').disabled = true;
  $('edit-document').textContent = '准备编辑…';
  let editor;
  try {
    await editorAssets();
    if (state.current !== item || state.searching) return;
    // Keep the reader in place while the editor parses larger Markdown files.
    if (section) {
      section.element.after($('edit-panel'));
      $('edit-panel').classList.add('section-edit');
    }
    $('edit-panel').hidden = false;
    editor = new toastui.Editor({
      el: $('markdown-editor'), height: 'calc(100vh - 175px)', minHeight: '520px',
      initialEditType: 'wysiwyg', previewStyle: 'tab', language: 'zh-CN',
      initialValue: section ? item.body.slice(section.start, section.end) : item.body,
      usageStatistics: false,
      toolbarItems: [
        ['heading', 'bold', 'italic', 'strike'], ['hr', 'quote'],
        ['ul', 'ol', 'task', 'indent', 'outdent'], ['table', 'image', 'link'],
        ['code', 'codeblock'],
      ],
      hooks: {addImageBlobHook: () => {
        alert('请先把图片存入项目，再用图片网址或相对路径插入。');
        return false;
      }},
    });
    if (state.current !== item || state.searching) {
      editor.destroy(); $('markdown-editor').replaceChildren(); $('edit-panel').hidden = true;
      restoreEditorPlacement();
      return;
    }
    if (section) {
      section.element.hidden = true;
      $('section-edit-tip').hidden = true;
      $('article').classList.remove('section-picking', 'pick-h' + state.sectionPicker.level);
      $('edit-panel').scrollIntoView({block: 'start'});
    } else {
      $('article').hidden = true;
      $('source').hidden = true;
    }
    $('edit-document').hidden = true;
    $('edit-actions').hidden = false;
    $('search').disabled = true;
    closeOutline();
    $('right-toggle').hidden = true;
    refreshEditorTheme();
    state.editing = {item, editor, section, baseline: editor.getMarkdown(), dirty: false, saving: false};
    editor.on('change', updateEditDirty);
    updateEditDirty();
  } catch (error) {
    editor?.destroy();
    $('markdown-editor').replaceChildren();
    if (section) section.element.hidden = false;
    restoreEditorPlacement();
    $('edit-status').textContent = '';
    $('article').hidden = false; $('source').hidden = false;
    $('edit-panel').hidden = true; $('edit-document').hidden = false;
    $('edit-actions').hidden = true;
    $('search').disabled = false;
    alert('编辑器加载失败：' + error.message);
  } finally {
    $('edit-document').disabled = false;
    $('edit-document').textContent = state.sectionPicker ? '退出选节' : '编辑本文';
  }
}

function endEdit() {
  if (!state.editing) return;
  if (state.editing.section) state.editing.section.element.hidden = false;
  state.editing.editor.destroy();
  state.editing = null;
  $('markdown-editor').replaceChildren();
  $('edit-panel').hidden = true;
  restoreEditorPlacement();
  $('article').hidden = false;
  $('source').hidden = false;
  $('edit-document').hidden = false;
  $('edit-actions').hidden = true;
  $('search').disabled = false;
  $('edit-status').textContent = '';
  exitSectionPicker();
  $('right-toggle').hidden = !$('outline-links').querySelector('a');
}

function cancelEdit() {
  if (!state.editing || state.editing.saving) return;
  if (state.editing.dirty && !confirm('有未保存的修改，确定放弃吗？')) return;
  endEdit();
  route();
}

async function saveEdit() {
  const editing = state.editing;
  if (!editing || !editing.dirty || editing.saving) return;
  editing.saving = true;
  $('save-edit').disabled = true;
  $('edit-status').textContent = '正在保存…';
  try {
    let body = editing.editor.getMarkdown();
    if (editing.section) {
      const {start, end} = editing.section;
      const original = editing.item.body.slice(start, end);
      const trailingNewlines = /\n*$/.exec(original)[0];
      body = editing.item.body.slice(0, start) + body.trimEnd() + trailingNewlines + editing.item.body.slice(end);
    }
    const response = await fetch('/api/document', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({id: editing.item.id, body,
        expectedSha256: editing.item.sha256}),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || '保存失败');
    Object.assign(editing.item, result);
    endEdit();
    route({force: true});
  } catch (error) {
    $('edit-status').textContent = error.message;
    editing.saving = false;
    $('save-edit').disabled = false;
  }
}

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
  localStorage.setItem('english-left-sidebar', open ? 'open' : 'closed');
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

function route({force = false} = {}) {
  const [rawId, rawAnchor=''] = location.hash.slice(1).split('::');
  let id, anchor; try { id=decodeURIComponent(rawId); anchor=decodeURIComponent(rawAnchor); } catch { id=''; anchor=''; }
  if (state.aliases[id] && state.items.some(x => x.id === state.aliases[id])) {
    id = state.aliases[id];
    history.replaceState(null, '', docHash(id, anchor));
  }
  const item = state.items.find(x=>x.id===id) || state.items[0];
  if (state.editing) {
    if (item?.id === state.editing.item.id) return;
    if (state.editing.dirty && !confirm('有未保存的修改，确定离开吗？')) {
      history.replaceState(null, '', docHash(state.editing.item.id));
      return;
    }
    endEdit();
  }
  if (state.sectionPicker && item?.id !== state.sectionPicker.item.id) exitSectionPicker();
  $('search').value = '';
  if (item && state.current?.id === item.id && !state.searching && !force) {
    scrollToSection(anchor); return;
  }
  state.current = item;
  state.searching = false;
  if (!state.current) return;
  $('article').innerHTML = renderDoc(item);
  addDocumentContents(item);
  foldDocumentSections();
  $('breadcrumb').textContent = item.group + ' / ' + item.title;
  $('source').textContent = 'english/' + item.id;
  $('edit-document').hidden = false;
  nav();
  scrollToSection(anchor);
}

async function loadBook() {
  const response = await fetch('/api/catalog');
  if (!response.ok) throw new Error('目录加载失败，请刷新重试。');
  const data = await response.json();
  state.items = data.items; state.nav = data.nav || {groups:[]}; state.aliases = data.aliases || {};
  route();
  preloadEditorAssets();
}

$('search').oninput=()=>{
  const query=$('search').value.trim().toLowerCase(); if(!query)return route();
  if (state.sectionPicker) exitSectionPicker();
  state.searching = true;
  closeOutline();
  $('right-toggle').hidden = true;
  $('edit-document').hidden = true;
  const results=state.items.filter(x=>(x.title+'\n'+x.body).toLowerCase().includes(query));
  $('article').innerHTML=`<h1>搜索知识书</h1><p>${results.length} 个结果</p>`+results.map(x=>{const at=x.body.toLowerCase().indexOf(query);return `<a class="search-result" href="#${encodeURIComponent(x.id)}"><strong>${x.title}</strong><small>${x.body.slice(Math.max(0,at-30),Math.max(0,at-30)+150)}</small></a>`;}).join('');
  $('breadcrumb').textContent='全文搜索';$('source').textContent='';
};
$('article').addEventListener('click',e=>{if(e.target.closest('a')?.hash===location.hash)route();});
$('article').addEventListener('click', e => {
  const picker = state.sectionPicker;
  if (!picker || state.editing) return;
  const heading = e.target.closest('h' + picker.level);
  if (!heading || !$('article').contains(heading)) return;
  const section = picker.headingSections.get(heading);
  const element = heading.closest('.section-fold');
  if (!section || !element) return;
  e.preventDefault();
  e.stopPropagation();
  beginEdit({...section, element});
}, true);
$('nav').addEventListener('click',e=>{if(e.target.closest('a')?.hash===location.hash)route();if(e.target.closest('a'))e.target.closest('details')?.setAttribute('open','');});
$('right-toggle').onclick = toggleOutline;
$('edit-document').onclick = () => {if (state.sectionPicker) exitSectionPicker(); else beginEdit();};
$('cancel-edit').onclick = cancelEdit;
$('save-edit').onclick = saveEdit;
$('left-toggle').onclick = () => setLeftSidebarOpen(document.body.classList.contains('left-collapsed'));
$('outline-links').addEventListener('click', e => { if (e.target.closest('a')) closeOutline(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeOutline(); });
setLeftSidebarOpen(localStorage.getItem('english-left-sidebar') !== 'closed');
closeOutline();
$('theme').onclick=()=>{const current=document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');const next=current==='dark'?'light':'dark';document.documentElement.dataset.theme=next;localStorage.setItem('english-theme',next);refreshEditorTheme();};
if(localStorage.getItem('english-theme'))document.documentElement.dataset.theme=localStorage.getItem('english-theme');
addEventListener('hashchange',route);
addEventListener('beforeunload', e => {if (state.editing?.dirty) {e.preventDefault(); e.returnValue = '';}});
(async()=>{try{await loadBook();}catch(e){$('article').textContent=e.message;}})();
