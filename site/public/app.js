'use strict';
const $ = id => document.getElementById(id);
const state = {items: [], nav: {groups:[]}, aliases: {}, current: null, searching: false, editing: null, quickEditing: null};
let editorAssetsPromise;

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

function updateQuickDirty(block) {
  const editing = state.quickEditing;
  if (!editing) return;
  if (block && editing.baseline.has(block)) {
    if (block.innerHTML === editing.baseline.get(block)) editing.changed.delete(block);
    else editing.changed.add(block);
  }
  $('save-edit').disabled = !editing.changed.size || editing.saving;
  $('edit-status').textContent = editing.changed.size ? `已修改 ${editing.changed.size} 块` : '点击正文直接编辑';
}

function startQuickEdit() {
  if (!state.current || state.quickEditing || state.editing) return;
  const blocks = [...$('article').querySelectorAll('[data-md-start]')];
  const covered = blocks.reduce((count, block) => count +
    Number(block.dataset.mdEnd) - Number(block.dataset.mdStart), 0);
  if (!blocks.length || covered < state.current.body.length * .8) return beginEdit();
  const baseline = new Map(blocks.map(block => [block, block.innerHTML]));
  blocks.forEach(block => { block.contentEditable = 'true'; });
  state.quickEditing = {item: state.current, blocks, baseline, changed: new Set(), saving: false};
  $('article').classList.add('quick-editing');
  document.body.classList.add('quick-editing-mode');
  $('edit-document').hidden = true;
  $('edit-actions').hidden = false;
  $('quick-format').hidden = false;
  $('advanced-edit').hidden = false;
  $('search').disabled = true;
  closeOutline();
  $('right-toggle').hidden = true;
  updateQuickDirty();
}

function endQuickEdit() {
  const editing = state.quickEditing;
  if (!editing) return;
  editing.blocks.forEach(block => block.removeAttribute('contenteditable'));
  state.quickEditing = null;
  $('article').classList.remove('quick-editing');
  document.body.classList.remove('quick-editing-mode');
  $('edit-document').hidden = false;
  $('edit-actions').hidden = true;
  $('quick-format').hidden = true;
  $('advanced-edit').hidden = true;
  $('search').disabled = false;
  $('edit-status').textContent = '';
  $('right-toggle').hidden = !$('outline-links').querySelector('a');
}

function cancelQuickEdit() {
  if (!state.quickEditing || state.quickEditing.saving) return;
  const dirty = state.quickEditing.changed.size > 0;
  if (dirty && !confirm('有未保存的修改，确定放弃吗？')) return;
  endQuickEdit();
  if (dirty) route({force: true, preserveScroll: true});
}

function serializeCodeBlock(block, original) {
  const opening = /^(`{3,}|~{3,})[^\n]*\n/.exec(original);
  if (!opening) return null;
  const trailing = /\n*$/.exec(original)[0];
  const code = (block.querySelector('code') || block).textContent.replace(/\n+$/, '');
  return opening[0] + code + '\n' + opening[1] + trailing;
}

function sourceHTML(block) {
  const clone = block.cloneNode(true);
  clone.removeAttribute('contenteditable');
  for (const node of clone.querySelectorAll('[data-original-href], [data-original-src]')) {
    if (node.dataset.originalHref && node.getAttribute('href') === node.dataset.viewerHref)
      node.setAttribute('href', node.dataset.originalHref);
    if (node.dataset.originalSrc && node.getAttribute('src') === node.dataset.viewerSrc)
      node.setAttribute('src', node.dataset.originalSrc);
    delete node.dataset.originalHref; delete node.dataset.viewerHref;
    delete node.dataset.originalSrc; delete node.dataset.viewerSrc;
  }
  return clone.outerHTML;
}

async function saveQuickEdit() {
  const editing = state.quickEditing;
  if (!editing || !editing.changed.size || editing.saving) return;
  editing.saving = true;
  $('save-edit').disabled = true;
  $('edit-status').textContent = '正在保存…';
  let converter, container;
  try {
    await editorAssets();
    container = document.createElement('div');
    container.hidden = true;
    document.body.append(container);
    converter = new toastui.Editor({el: container, height: '200px', initialEditType: 'wysiwyg',
      initialValue: '', usageStatistics: false});
    const replacements = [];
    for (const block of editing.changed) {
      if (!block.isConnected) throw new Error('正文结构已改变，请复制修改内容后刷新页面');
      const start = Number(block.dataset.mdStart), end = Number(block.dataset.mdEnd);
      const original = editing.item.body.slice(start, end);
      let replacement;
      if (block.dataset.mdType === 'code') replacement = serializeCodeBlock(block, original);
      if (replacement == null) {
        converter.setHTML(sourceHTML(block));
        replacement = converter.getMarkdown().trimEnd() + /\n*$/.exec(original)[0];
      }
      replacements.push({start, end, replacement});
    }
    replacements.sort((a, b) => b.start - a.start);
    let body = editing.item.body;
    for (const {start, end, replacement} of replacements) {
      body = body.slice(0, start) + replacement + body.slice(end);
    }
    const response = await fetch('/api/document', {method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({id: editing.item.id, body, expectedSha256: editing.item.sha256})});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || '保存失败');
    Object.assign(editing.item, result);
    endQuickEdit();
    route({force: true, preserveScroll: true});
  } catch (error) {
    $('edit-status').textContent = error.message;
    editing.saving = false;
    $('save-edit').disabled = false;
  } finally {
    converter?.destroy();
    container?.remove();
  }
}

function restoreEditorPlacement() {
  $('article').after($('edit-panel'));
}

async function beginEdit() {
  if (!state.current || state.editing) return;
  const item = state.current;
  $('edit-document').disabled = true;
  $('edit-document').textContent = '准备编辑…';
  let editor;
  try {
    await editorAssets();
    if (state.current !== item || state.searching) return;
    // Keep the reader in place while the editor parses larger Markdown files.
    $('edit-panel').hidden = false;
    editor = new toastui.Editor({
      el: $('markdown-editor'), height: 'calc(100vh - 175px)', minHeight: '520px',
      initialEditType: 'wysiwyg', previewStyle: 'tab', language: 'zh-CN',
      initialValue: item.body,
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
    $('article').hidden = true;
    $('source').hidden = true;
    $('edit-document').hidden = true;
    $('edit-actions').hidden = false;
    $('search').disabled = true;
    closeOutline();
    $('right-toggle').hidden = true;
    refreshEditorTheme();
    state.editing = {item, editor, baseline: editor.getMarkdown(), dirty: false, saving: false};
    editor.on('change', updateEditDirty);
    updateEditDirty();
  } catch (error) {
    editor?.destroy();
    $('markdown-editor').replaceChildren();
    restoreEditorPlacement();
    $('edit-status').textContent = '';
    $('article').hidden = false; $('source').hidden = false;
    $('edit-panel').hidden = true; $('edit-document').hidden = false;
    $('edit-actions').hidden = true;
    $('search').disabled = false;
    alert('编辑器加载失败：' + error.message);
  } finally {
    $('edit-document').disabled = false;
    $('edit-document').textContent = '编辑本文';
  }
}

function endEdit() {
  if (!state.editing) return;
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
    const body = editing.editor.getMarkdown();
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
    img.dataset.originalSrc = src;
    img.src = '/files/' + resolve(src);
    img.dataset.viewerSrc = img.getAttribute('src');
  });
  contentEl.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (/^(https?:|data:|\/\/|#|mailto:)/i.test(href)) return;
    const [path, anchor=''] = href.split('#');
    if (path.toLowerCase().endsWith('.md')) {
      let decoded = anchor; try { decoded = decodeURIComponent(anchor); } catch {}
      a.dataset.originalHref = href;
      a.href = docHash(resolve(path), decoded);
      a.dataset.viewerHref = a.getAttribute('href');
    }
  });
}

function renderMarkdownPart(source, offset) {
  const tokens = marked.lexer(source, {gfm: true});
  const contentEl = document.createElement('div');
  contentEl.innerHTML = marked.parser(tokens, {gfm: true});
  const visibleTokens = tokens.filter(token => !['space', 'def'].includes(token.type));
  if (visibleTokens.length === contentEl.children.length) {
    let position = 0, elementIndex = 0;
    for (const token of tokens) {
      const raw = token.raw || '';
      const start = source.startsWith(raw, position) ? position : source.indexOf(raw, position);
      if (start < 0) break;
      position = start + raw.length;
      if (['space', 'def'].includes(token.type)) continue;
      const element = contentEl.children[elementIndex++];
      if (['heading', 'paragraph', 'blockquote', 'list', 'table', 'code'].includes(token.type)) {
        element.dataset.mdStart = String(offset + start);
        element.dataset.mdEnd = String(offset + position);
        element.dataset.mdType = token.type;
      }
    }
  }
  return contentEl;
}

function renderDoc(item) {
  const answer = /^## 参考答案\s*$/m.exec(item.body);
  const contentEl = renderMarkdownPart(answer ? item.body.slice(0, answer.index) : item.body, 0);
  if (window.hljs) contentEl.querySelectorAll('pre code').forEach(el => hljs.highlightElement(el));
  fixAssets(contentEl, item.id);
  let html = contentEl.innerHTML;
  if (answer) {
    const answerStart = answer.index + answer[0].length;
    const answerEl = renderMarkdownPart(item.body.slice(answerStart), answerStart);
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

function route({force = false, preserveScroll = false} = {}) {
  const previousScroll = window.scrollY;
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
  if (state.quickEditing) {
    if (item?.id === state.quickEditing.item.id) return;
    if (state.quickEditing.changed.size && !confirm('有未保存的修改，确定离开吗？')) {
      history.replaceState(null, '', docHash(state.quickEditing.item.id));
      return;
    }
    endQuickEdit();
  }
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
  if (preserveScroll) window.scrollTo(0, previousScroll);
  else scrollToSection(anchor);
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
  closeOutline();
  $('right-toggle').hidden = true;
  $('edit-document').hidden = true;
  const results=state.items.filter(x=>(x.title+'\n'+x.body).toLowerCase().includes(query));
  $('article').innerHTML=`<h1>搜索知识书</h1><p>${results.length} 个结果</p>`+results.map(x=>{const at=x.body.toLowerCase().indexOf(query);return `<a class="search-result" href="#${encodeURIComponent(x.id)}"><strong>${x.title}</strong><small>${x.body.slice(Math.max(0,at-30),Math.max(0,at-30)+150)}</small></a>`;}).join('');
  $('breadcrumb').textContent='全文搜索';$('source').textContent='';
};
$('article').addEventListener('click', e => {
  if (state.quickEditing && e.target.closest('a')) { e.preventDefault(); return; }
  if (e.target.closest('a')?.hash === location.hash) route();
});
$('article').addEventListener('input', e => {
  if (!state.quickEditing) return;
  updateQuickDirty(e.target.closest('[data-md-start]'));
});
$('nav').addEventListener('click',e=>{if(e.target.closest('a')?.hash===location.hash)route();if(e.target.closest('a'))e.target.closest('details')?.setAttribute('open','');});
$('right-toggle').onclick = toggleOutline;
$('edit-document').onclick = () => startQuickEdit();
$('advanced-edit').onclick = () => {
  if (!state.quickEditing) return;
  const dirty = state.quickEditing.changed.size > 0;
  if (dirty && !confirm('切换高级格式会放弃本轮未保存的修改，确定吗？')) return;
  endQuickEdit();
  if (dirty) route({force: true});
  beginEdit();
};
$('cancel-edit').onclick = () => {if (state.quickEditing) cancelQuickEdit(); else cancelEdit();};
$('save-edit').onclick = () => {if (state.quickEditing) saveQuickEdit(); else saveEdit();};
$('quick-format').addEventListener('mousedown', e => {if (e.target.closest('button')) e.preventDefault();});
$('quick-format').addEventListener('click', e => {
  const button = e.target.closest('button[data-format]');
  if (!button || !state.quickEditing) return;
  let command = button.dataset.format, argument;
  if (command === 'link') {
    argument = prompt('链接地址');
    if (!argument) return;
    command = 'createLink';
  }
  document.execCommand(command, false, argument);
  const focus = document.getSelection()?.anchorNode;
  updateQuickDirty((focus?.nodeType === Node.ELEMENT_NODE ? focus : focus?.parentElement)?.closest('[data-md-start]'));
});
$('left-toggle').onclick = () => setLeftSidebarOpen(document.body.classList.contains('left-collapsed'));
$('outline-links').addEventListener('click', e => { if (e.target.closest('a')) closeOutline(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeOutline(); });
setLeftSidebarOpen(localStorage.getItem('english-left-sidebar') !== 'closed');
closeOutline();
$('theme').onclick=()=>{const current=document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');const next=current==='dark'?'light':'dark';document.documentElement.dataset.theme=next;localStorage.setItem('english-theme',next);refreshEditorTheme();};
if(localStorage.getItem('english-theme'))document.documentElement.dataset.theme=localStorage.getItem('english-theme');
addEventListener('hashchange',route);
addEventListener('beforeunload', e => {if (state.editing?.dirty || state.quickEditing?.changed.size) {e.preventDefault(); e.returnValue = '';}});
(async()=>{try{await loadBook();}catch(e){$('article').textContent=e.message;}})();
