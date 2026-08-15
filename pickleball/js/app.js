// App shell: routing, header, bottom nav. Views return { title, html } and the
// shell paints it into #view.

import { $, preserveFocus } from './ui.js';
import { currentPath, segments, onRoute, go, back } from './router.js';
import { renderEventList, renderEventDetail, renderEventForm, wireEvents, resetDraft } from './views/events.js';
import { renderPeople, wirePeople } from './views/people.js';
import { renderGroups, wireGroups } from './views/groups.js';
import { renderSettings, wireSettings } from './views/settings.js';

const view = $('#view');
const titleEl = $('#app-title');
const backBtn = $('#back-btn');

const NAV = [
  ['/events', 'Play dates', '🎾'],
  ['/people', 'People', '📇'],
  ['/groups', 'Groups', '👥'],
  ['/settings', 'Settings', '⚙️'],
];

function resolve(path) {
  const [head, id, action] = segments(path);
  switch (head) {
    case 'event':
      if (id === 'new') return renderEventForm(null);
      if (action === 'edit') return renderEventForm(id);
      return renderEventDetail(id);
    case 'people':
      return renderPeople();
    case 'groups':
      return renderGroups();
    case 'settings':
      return renderSettings();
    case 'events':
    default:
      return renderEventList();
  }
}

let lastPath = null;

function paint() {
  const path = currentPath();
  const result = resolve(path);
  const isNavigation = path !== lastPath;
  // Swapping the markup resets the scroller. Landing at the top is right when you
  // navigate, and wrong when you just tapped Yes halfway down the roster.
  const keepAt = view.scrollTop;

  titleEl.textContent = result.title;
  view.innerHTML = result.html;

  if (isNavigation) {
    view.scrollTop = 0;
    lastPath = path;
  } else {
    view.scrollTop = keepAt;
  }

  backBtn.hidden = !result.back;
  backBtn.dataset.to = result.back || '';

  const root = `/${segments(path)[0] || 'events'}`;
  const navRoot = root === '/event' ? '/events' : root;
  $('#nav').querySelectorAll('a').forEach((a) => {
    a.classList.toggle('on', a.getAttribute('href') === `#${navRoot}`);
    a.setAttribute('aria-current', a.getAttribute('href') === `#${navRoot}` ? 'page' : 'false');
  });
}

export function rerender({ keepFocus = false } = {}) {
  if (keepFocus) preserveFocus(paint);
  else paint();
}

function boot() {
  $('#nav').innerHTML = NAV.map(([href, label, icon]) => `
    <a href="#${href}">
      <span class="nav-icon" aria-hidden="true">${icon}</span>
      <span class="nav-label">${label}</span>
    </a>`).join('');

  backBtn.addEventListener('click', () => {
    resetDraft();
    const to = backBtn.dataset.to;
    if (to) go(to);
    else back();
  });

  // Delegated once — sheets live outside #view, so their clicks never reach these.
  wireEvents(view, rerender);
  wirePeople(view, rerender);
  wireGroups(view, rerender);
  wireSettings(view, rerender);

  onRoute(paint);
  paint();

  if (!location.hash) location.hash = '/events';
}

boot();

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch((err) => {
      console.warn('Offline support unavailable:', err);
    });
  });
}
