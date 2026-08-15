// Hash routing, kept in its own module so views can navigate without importing the app shell.

const handlers = new Set();

export function currentPath() {
  const raw = location.hash.replace(/^#/, '');
  return raw.startsWith('/') ? raw : '/events';
}

export function go(path) {
  if (currentPath() === path) {
    handlers.forEach((fn) => fn(path));
    return;
  }
  location.hash = path;
}

export function back(fallback = '/events') {
  if (history.length > 1) history.back();
  else go(fallback);
}

export function onRoute(fn) {
  handlers.add(fn);
  return () => handlers.delete(fn);
}

window.addEventListener('hashchange', () => handlers.forEach((fn) => fn(currentPath())));

// '/event/e_123/edit' -> ['event', 'e_123', 'edit']
export function segments(path = currentPath()) {
  return path.split('/').filter(Boolean);
}
