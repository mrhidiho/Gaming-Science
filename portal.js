(() => {
  'use strict';

  const catalog = window.COURSE_INDEX;
  if (!catalog || !Array.isArray(catalog.volumes)) return;

  const STORAGE_KEY = 'game-engineering-course-map-v1';
  const volumeByNumber = new Map(catalog.volumes.map(volume => [volume.number, volume]));
  const lessonById = new Map();
  const lessons = [];
  for (const volume of catalog.volumes) {
    for (const module of volume.modules) {
      for (const lesson of module.lessons) {
        lesson.volumeNumber = volume.number;
        lesson.moduleNumber = module.number;
        lesson.moduleTitle = module.title;
        lesson.reader = volume.reader;
        lessonById.set(lesson.id, lesson);
        lessons.push(lesson);
      }
    }
  }

  const elements = {
    sidebar: document.getElementById('sidebar'),
    scrim: document.getElementById('mobile-scrim'),
    tree: document.getElementById('course-tree'),
    search: document.getElementById('course-search'),
    searchHelp: document.getElementById('search-help'),
    home: document.getElementById('home-view'),
    readerView: document.getElementById('reader-view'),
    savedView: document.getElementById('saved-view'),
    volumeGrid: document.getElementById('volume-grid'),
    checkpointTrack: document.getElementById('checkpoint-track'),
    savedList: document.getElementById('saved-list'),
    continueButton: document.getElementById('continue-button'),
    resumeLine: document.getElementById('resume-line'),
    bookmarkCount: document.getElementById('bookmark-count'),
    storageNote: document.getElementById('storage-note'),
    storageIndicator: document.getElementById('storage-indicator'),
    reader: document.getElementById('course-reader'),
    readerTitle: document.getElementById('reader-title'),
    readerId: document.getElementById('reader-lesson-id'),
    readerOutcome: document.getElementById('reader-outcome'),
    readerBreadcrumb: document.getElementById('reader-breadcrumb'),
    readerLink: document.getElementById('open-reader-link'),
    saveLesson: document.getElementById('save-lesson-button'),
    context: document.getElementById('topbar-context'),
    previous: document.getElementById('previous-lesson'),
    next: document.getElementById('next-lesson'),
    menuButton: document.getElementById('menu-button'),
  };

  const initialState = () => ({ version: 1, lastLesson: null, recent: [], bookmarks: [] });
  let state = initialState();
  let storageAvailable = true;
  let activeFilter = 'all';
  let currentLessonId = null;
  let searchTerm = '';

  function validIds(list) {
    if (!Array.isArray(list)) return [];
    return [...new Set(list.filter(id => typeof id === 'string' && lessonById.has(id)))];
  }

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const data = JSON.parse(raw);
      if (!data || data.version !== 1) throw new Error('Unrecognized course-map data.');
      state = {
        version: 1,
        lastLesson: typeof data.lastLesson === 'string' && lessonById.has(data.lastLesson) ? data.lastLesson : null,
        recent: validIds(data.recent).slice(0, 10),
        bookmarks: validIds(data.bookmarks),
      };
    } catch (_) {
      state = initialState();
      storageAvailable = false;
    }
    updateStorageNote();
  }

  function saveState() {
    if (!storageAvailable) return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (_) {
      storageAvailable = false;
      updateStorageNote();
    }
  }

  function updateStorageNote() {
    elements.storageNote.textContent = storageAvailable
      ? 'Resume and saved lessons stay in this browser.'
      : 'Browser storage is unavailable; navigation lasts for this session only.';
    elements.storageIndicator.classList.toggle('is-unavailable', !storageAvailable);
  }

  function escapeHTML(value) {
    return String(value ?? '').replace(/[&<>"']/g, char => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[char]));
  }

  function formatHours(hours) {
    if (!hours) return '';
    return `${Number(hours.minimum).toLocaleString()}–${Number(hours.maximum).toLocaleString()} HRS`;
  }

  function lessonUrl(lesson) {
    return `${lesson.reader}#${lesson.anchor}`;
  }

  function buildVolumeCards() {
    elements.volumeGrid.innerHTML = catalog.volumes.map(volume => {
      const modules = volume.modules.map(module => `<span class="module-tag" title="Module ${module.number}: ${escapeHTML(module.title)}">${escapeHTML(module.title)}</span>`).join('');
      const regular = volume.resources.filter(resource => !resource.answers);
      const answer = volume.resources.find(resource => resource.answers);
      const resourceLinks = regular.map(resource => `<a href="${escapeHTML(resource.path)}" target="_blank" rel="noreferrer">${escapeHTML(resource.label)} ↗</a>`).join('');
      const answerLink = answer ? `<details class="answer-resources"><summary>After attempting the quiz: answer key</summary><div class="resource-links"><a href="${escapeHTML(answer.path)}" target="_blank" rel="noreferrer">${escapeHTML(answer.label)} ↗</a></div></details>` : '';
      const firstLesson = volume.modules[0]?.lessons[0];
      const description = volume.purpose || volume.level;
      return `<article class="volume-card">
        <div class="volume-card-head"><span class="volume-number"><b>${String(volume.number).padStart(2, '0')}</b> VOLUME ${volume.number}</span><span class="volume-hours">${escapeHTML(formatHours(volume.hours))}</span></div>
        <h3>${escapeHTML(volume.title)}</h3>
        <p class="volume-purpose">${escapeHTML(description)}</p>
        <div class="module-tags" aria-label="Modules">${modules}</div>
        <div class="volume-card-footer"><span class="volume-checkpoint">CHECKPOINT ${escapeHTML(volume.checkpoint?.id || '—')} · 20 LESSONS</span><button type="button" class="volume-open" data-open-lesson="${escapeHTML(firstLesson?.id || '')}">Open volume <span aria-hidden="true">→</span></button></div>
        <details class="volume-resources"><summary>Volume materials</summary><div class="resource-links">${resourceLinks}</div>${answerLink}</details>
      </article>`;
    }).join('');
  }

  function buildCheckpointTrack() {
    elements.checkpointTrack.innerHTML = catalog.volumes.map(volume => `<div class="checkpoint-item"><span class="checkpoint-gate">GATE ${escapeHTML(volume.checkpoint?.id || '—')}</span><strong>${escapeHTML(volume.checkpoint?.title || volume.title)}</strong><span class="checkpoint-volume">After Volume ${volume.number}</span></div>`).join('');
  }

  function matchesSearch(lesson, module, volume) {
    if (!searchTerm) return true;
    const haystack = [
      lesson.id, lesson.title, lesson.outcome, lesson.practical, lesson.reading,
      module.title, module.prerequisites, module.project,
      volume.title, volume.purpose, volume.level,
    ].join(' ').toLocaleLowerCase();
    return haystack.includes(searchTerm);
  }

  function allowedByFilter(id) {
    if (activeFilter === 'saved') return state.bookmarks.includes(id);
    if (activeFilter === 'recent') return state.recent.includes(id);
    return true;
  }

  function renderTree() {
    const priorScroll = elements.tree.scrollTop;
    const filtered = new Map();
    let count = 0;
    for (const volume of catalog.volumes) {
      const modules = [];
      for (const module of volume.modules) {
        const matches = module.lessons.filter(lesson => allowedByFilter(lesson.id) && matchesSearch(lesson, module, volume));
        if (matches.length) {
          modules.push({ module, lessons: matches });
          count += matches.length;
        }
      }
      if (modules.length) filtered.set(volume.number, modules);
    }

    if (searchTerm) {
      elements.searchHelp.textContent = count ? `${count} matching lesson${count === 1 ? '' : 's'} across the series.` : 'No lessons match those terms.';
    } else if (activeFilter === 'saved') {
      elements.searchHelp.textContent = `${count} saved lesson${count === 1 ? '' : 's'}.`;
    } else if (activeFilter === 'recent') {
      elements.searchHelp.textContent = `${count} recently opened lesson${count === 1 ? '' : 's'}.`;
    } else {
      elements.searchHelp.textContent = 'Search across 200 lessons, outcomes, and assignments.';
    }

    const html = catalog.volumes.map(volume => {
      const moduleMatches = filtered.get(volume.number);
      if (!moduleMatches) return '';
      const open = Boolean(searchTerm) || (state.lastLesson && lessonById.get(state.lastLesson)?.volumeNumber === volume.number) || (!state.lastLesson && volume.number === 1);
      const modules = moduleMatches.map(({ module, lessons: moduleLessons }) => `<section class="tree-module">
        <h3 class="tree-module-title">MODULE ${String(module.number).padStart(2, '0')} · ${escapeHTML(module.title)}</h3>
        <details class="tree-module-brief"><summary>Prerequisite and project</summary><p><strong>Before:</strong> ${escapeHTML(module.prerequisites || 'No prerequisite is listed.')}<br><strong>Project:</strong> ${escapeHTML(module.project || 'See the volume reader for this module’s work.')}</p></details>
        <div class="tree-lessons">${moduleLessons.map(lesson => {
          const isSaved = state.bookmarks.includes(lesson.id);
          const current = lesson.id === currentLessonId;
          return `<div class="tree-lesson-row"><button type="button" class="tree-lesson${current ? ' is-current' : ''}" data-open-lesson="${escapeHTML(lesson.id)}" aria-label="Open lesson ${escapeHTML(lesson.id)}: ${escapeHTML(lesson.title)}" ${current ? 'aria-current="page"' : ''}><span class="tree-lesson-id">${escapeHTML(lesson.id)}</span><span class="tree-lesson-title">${escapeHTML(lesson.title)}</span></button><button type="button" class="bookmark-mini${isSaved ? ' is-saved' : ''}" data-bookmark="${escapeHTML(lesson.id)}" aria-label="${isSaved ? 'Remove' : 'Save'} lesson ${escapeHTML(lesson.id)}" aria-pressed="${isSaved}">${isSaved ? '★' : '☆'}</button></div>`;
        }).join('')}</div>
      </section>`).join('');
      return `<details class="volume-tree" data-volume="${volume.number}" ${open ? 'open' : ''}><summary class="volume-summary"><span class="volume-index">${String(volume.number).padStart(2, '0')}</span><span class="volume-name">${escapeHTML(volume.title)}</span></summary>${modules}</details>`;
    }).join('');

    elements.tree.innerHTML = html || `<p class="tree-empty">${searchTerm ? 'No matches. Try another topic or clear the search.' : activeFilter === 'saved' ? 'No saved lessons yet. Select ☆ beside any lesson to save it.' : 'No recently opened lessons yet.'}</p>`;
    elements.tree.scrollTop = priorScroll;
    elements.bookmarkCount.textContent = String(state.bookmarks.length);
  }

  function updateResume() {
    const last = state.lastLesson ? lessonById.get(state.lastLesson) : null;
    if (!last) {
      elements.continueButton.innerHTML = 'Start with lesson 01.1 <span aria-hidden="true">→</span>';
      elements.resumeLine.textContent = storageAvailable ? 'No recent lesson yet. Begin with the foundations or choose a volume below.' : 'Browser storage is unavailable here. Your course map still works while this page stays open.';
      return;
    }
    elements.continueButton.innerHTML = `Continue ${escapeHTML(last.id)} <span aria-hidden="true">→</span>`;
    elements.resumeLine.textContent = `Last opened: ${last.id} · ${last.title}`;
  }

  function toggleBookmark(id) {
    if (!lessonById.has(id)) return;
    const current = new Set(state.bookmarks);
    if (current.has(id)) current.delete(id); else current.add(id);
    state.bookmarks = [...current];
    saveState();
    renderTree();
    renderSaved();
    syncCurrentBookmark();
  }

  function syncCurrentBookmark() {
    if (!currentLessonId) return;
    const saved = state.bookmarks.includes(currentLessonId);
    elements.saveLesson.classList.toggle('is-saved', saved);
    elements.saveLesson.setAttribute('aria-pressed', String(saved));
    elements.saveLesson.innerHTML = `${saved ? '★' : '☆'} <span>${saved ? 'Saved' : 'Save lesson'}</span>`;
  }

  function switchView(view) {
    elements.home.hidden = view !== 'home';
    elements.readerView.hidden = view !== 'reader';
    elements.savedView.hidden = view !== 'saved';
    elements.context.textContent = view === 'reader' ? 'LESSON READER' : view === 'saved' ? 'SAVED LESSONS' : 'COURSE HOME';
    document.querySelectorAll('.side-link').forEach(button => {
      const active = (view === 'home' && button.dataset.action === 'home') || (view === 'saved' && button.dataset.action === 'bookmarks');
      button.classList.toggle('is-active', active);
    });
  }

  function openLesson(id) {
    const lesson = lessonById.get(id);
    if (!lesson) return;
    const volume = volumeByNumber.get(lesson.volumeNumber);
    currentLessonId = id;
    state.lastLesson = id;
    state.recent = [id, ...state.recent.filter(previous => previous !== id)].slice(0, 10);
    saveState();

    elements.readerTitle.textContent = lesson.title;
    elements.readerId.textContent = `LESSON ${lesson.id}`;
    elements.readerOutcome.textContent = lesson.outcome;
    elements.readerBreadcrumb.textContent = `VOLUME ${volume.number} · MODULE ${lesson.moduleNumber} · ${lesson.moduleTitle}`;
    const href = lessonUrl(lesson);
    elements.reader.src = href;
    elements.reader.title = `${lesson.id}: ${lesson.title} — ${volume.title}`;
    elements.readerLink.href = href;
    document.title = `${lesson.id} ${lesson.title} · Game Engineering`;

    const position = lessons.findIndex(entry => entry.id === id);
    elements.previous.disabled = position <= 0;
    elements.next.disabled = position < 0 || position >= lessons.length - 1;
    renderTree();
    renderSaved();
    syncCurrentBookmark();
    updateResume();
    switchView('reader');
    closeMobileMenu();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function renderSaved() {
    const savedLessons = state.bookmarks.map(id => lessonById.get(id)).filter(Boolean).sort((a, b) => a.volumeNumber - b.volumeNumber || a.id.localeCompare(b.id));
    if (!savedLessons.length) {
      elements.savedList.innerHTML = '<div class="saved-empty">No saved lessons yet. Use the ☆ beside any lesson in the course path.</div>';
      return;
    }
    elements.savedList.innerHTML = savedLessons.map(lesson => `<article class="saved-card"><div class="saved-card-top"><span>VOLUME ${lesson.volumeNumber} · MODULE ${lesson.moduleNumber}</span><span>${escapeHTML(lesson.id)}</span></div><h2>${escapeHTML(lesson.title)}</h2><div class="saved-card-actions"><button type="button" data-open-lesson="${escapeHTML(lesson.id)}">Open lesson →</button><button type="button" data-bookmark="${escapeHTML(lesson.id)}">Remove from saved</button></div></article>`).join('');
  }

  function showHome() {
    switchView('home');
    closeMobileMenu();
    document.title = 'Game Engineering · Student Course Map';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function showSaved() {
    renderSaved();
    switchView('saved');
    closeMobileMenu();
    document.title = 'Saved Lessons · Game Engineering';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function closeMobileMenu() {
    elements.sidebar.classList.remove('is-open');
    elements.scrim.hidden = true;
    elements.menuButton.setAttribute('aria-expanded', 'false');
    elements.menuButton.setAttribute('aria-label', 'Open course navigation');
  }

  function toggleMobileMenu() {
    const open = !elements.sidebar.classList.contains('is-open');
    elements.sidebar.classList.toggle('is-open', open);
    elements.scrim.hidden = !open;
    elements.menuButton.setAttribute('aria-expanded', String(open));
    elements.menuButton.setAttribute('aria-label', open ? 'Close course navigation' : 'Open course navigation');
  }

  function setFilter(filter) {
    activeFilter = filter;
    document.querySelectorAll('.filter-chip').forEach(button => button.classList.toggle('is-selected', button.dataset.filter === filter));
    renderTree();
  }

  function stepLesson(direction) {
    const position = lessons.findIndex(lesson => lesson.id === currentLessonId);
    const next = lessons[position + direction];
    if (next) openLesson(next.id);
  }

  elements.tree.addEventListener('click', event => {
    const bookmark = event.target.closest('[data-bookmark]');
    if (bookmark) {
      event.preventDefault();
      toggleBookmark(bookmark.dataset.bookmark);
      return;
    }
    const lesson = event.target.closest('[data-open-lesson]');
    if (lesson) openLesson(lesson.dataset.openLesson);
  });

  document.addEventListener('click', event => {
    const bookmark = event.target.closest('[data-bookmark]');
    if (bookmark && !elements.tree.contains(bookmark)) {
      toggleBookmark(bookmark.dataset.bookmark);
      return;
    }
    const lesson = event.target.closest('[data-open-lesson]');
    if (lesson && !elements.tree.contains(lesson)) {
      openLesson(lesson.dataset.openLesson);
      return;
    }
    const action = event.target.closest('[data-action]')?.dataset.action;
    if (action === 'home') showHome();
    if (action === 'bookmarks') showSaved();
  });

  elements.search.addEventListener('input', event => {
    searchTerm = event.target.value.trim().toLocaleLowerCase();
    if (searchTerm && activeFilter !== 'all') setFilter('all'); else renderTree();
  });
  elements.search.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      elements.search.value = '';
      searchTerm = '';
      renderTree();
    }
  });
  document.querySelectorAll('.filter-chip').forEach(button => button.addEventListener('click', () => setFilter(button.dataset.filter)));
  elements.continueButton.addEventListener('click', () => openLesson(state.lastLesson || '01.1'));
  document.getElementById('browse-button').addEventListener('click', () => document.getElementById('volume-section').scrollIntoView({ behavior: 'smooth' }));
  document.getElementById('sidebar-browse-link').addEventListener('click', () => {
    if (window.matchMedia('(max-width: 850px)').matches && !elements.sidebar.classList.contains('is-open')) toggleMobileMenu();
    elements.search.focus();
  });
  document.getElementById('back-button').addEventListener('click', showHome);
  document.getElementById('save-lesson-button').addEventListener('click', () => currentLessonId && toggleBookmark(currentLessonId));
  elements.previous.addEventListener('click', () => stepLesson(-1));
  elements.next.addEventListener('click', () => stepLesson(1));
  elements.menuButton.addEventListener('click', toggleMobileMenu);
  elements.scrim.addEventListener('click', closeMobileMenu);
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !event.metaKey && !event.ctrlKey && !event.altKey && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
      event.preventDefault();
      elements.search.focus();
    }
    if (event.key === 'Escape' && elements.sidebar.classList.contains('is-open')) closeMobileMenu();
  });

  loadState();
  buildVolumeCards();
  buildCheckpointTrack();
  renderTree();
  renderSaved();
  updateResume();
})();
