// Toasts, bottom sheets and confirm dialogs. No framework, just DOM.

import { esc } from './util.js';

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

let toastTimer = null;

export function toast(message, { tone = 'default' } = {}) {
  const host = $('#toast');
  host.textContent = message;
  host.className = `toast show tone-${tone}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { host.className = 'toast'; }, 2600);
}

/* ---------- bottom sheet ---------- */

// Sheets stack: a picker can open on top of an editor and dismiss back to it.
const sheetStack = [];

export function closeSheet() {
  const top = sheetStack.pop();
  if (!top) return;
  const { root, onClose } = top;
  root.classList.remove('open');
  setTimeout(() => root.remove(), 180);
  if (!sheetStack.length) document.body.classList.remove('sheet-open');
  onClose?.();
}

export function closeAllSheets() {
  while (sheetStack.length) closeSheet();
}

/**
 * @param {object} opts
 * @param {string} opts.title
 * @param {string} opts.body     HTML for the sheet contents
 * @param {(root: HTMLElement) => void} [opts.mount]  wire up listeners after render
 */
export function openSheet({ title, body, mount, onClose }) {
  const root = document.createElement('div');
  root.className = 'sheet-backdrop';
  root.style.zIndex = String(60 + sheetStack.length * 2);
  root.innerHTML = `
    <section class="sheet" role="dialog" aria-modal="true" aria-label="${esc(title)}">
      <header class="sheet-head">
        <h2>${esc(title)}</h2>
        <button class="icon-btn" data-sheet-close aria-label="Close">✕</button>
      </header>
      <div class="sheet-body">${body}</div>
    </section>`;
  document.body.appendChild(root);
  document.body.classList.add('sheet-open');
  sheetStack.push({ root, onClose });

  root.addEventListener('click', (e) => {
    // Only the topmost sheet responds to a backdrop tap.
    if (sheetStack[sheetStack.length - 1]?.root !== root) return;
    if (e.target === root || e.target.closest('[data-sheet-close]')) closeSheet();
  });
  requestAnimationFrame(() => root.classList.add('open'));
  mount?.(root);
  return root;
}

export function confirmDialog(message, { confirmLabel = 'Confirm', danger = false } = {}) {
  return new Promise((resolve) => {
    let settled = false;
    const finish = (value) => {
      if (settled) return;
      settled = true;
      resolve(value);
    };
    openSheet({
      title: 'Are you sure?',
      body: `
        <p class="sheet-text">${esc(message)}</p>
        <div class="sheet-actions">
          <button class="btn ghost" data-choice="cancel">Cancel</button>
          <button class="btn ${danger ? 'danger' : 'primary'}" data-choice="ok">${esc(confirmLabel)}</button>
        </div>`,
      mount(root) {
        root.addEventListener('click', (e) => {
          const choice = e.target.closest('[data-choice]')?.dataset.choice;
          if (!choice) return;
          finish(choice === 'ok');
          closeSheet();
        });
      },
      onClose: () => finish(false),
    });
  });
}

export function statusChip(status) {
  const label = { yes: 'In', no: 'Out', pending: 'Waiting' }[status] || status;
  return `<span class="chip chip-${status}">${label}</span>`;
}

export function emptyState(icon, title, hint, actionHTML = '') {
  return `
    <div class="empty">
      <div class="empty-icon" aria-hidden="true">${icon}</div>
      <h3>${esc(title)}</h3>
      <p>${esc(hint)}</p>
      ${actionHTML}
    </div>`;
}

// Keeps the caret in place when a keystroke triggers a re-render of a list.
export function preserveFocus(render) {
  const active = document.activeElement;
  const id = active?.id;
  const start = active?.selectionStart;
  const end = active?.selectionEnd;
  render();
  if (!id) return;
  const next = document.getElementById(id);
  if (!next) return;
  next.focus();
  if (start != null && next.setSelectionRange) {
    try { next.setSelectionRange(start, end); } catch { /* not a text input */ }
  }
}
