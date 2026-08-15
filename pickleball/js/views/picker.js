// Reusable "who?" sheet — tap whole groups or individual people, they merge into one list.

import * as store from '../store.js';
import { esc, formatPhone, pluralize } from '../util.js';
import { openSheet, closeSheet, $, $$, emptyState } from '../ui.js';

/**
 * @param {object} opts
 * @param {string} opts.title
 * @param {string[]} opts.selected            person ids already chosen
 * @param {boolean} [opts.showGroups=true]    offer group shortcuts
 * @param {(ids: string[]) => void} opts.onSave
 */
export function openPicker({ title, selected = [], showGroups = true, onSave, confirmLabel = 'Done' }) {
  const chosen = new Set(selected);
  let query = '';

  const allPeople = store.people();
  const allGroups = store.groups();

  function groupState(g) {
    const members = g.memberIds.filter((id) => store.person(id));
    if (!members.length) return 'empty';
    return members.every((id) => chosen.has(id)) ? 'all' : members.some((id) => chosen.has(id)) ? 'some' : 'none';
  }

  function listHTML() {
    const q = query.trim().toLowerCase();
    const matches = allPeople.filter((p) => !q || p.name.toLowerCase().includes(q) || p.phone.includes(q));
    if (!allPeople.length) {
      return emptyState('👥', 'No contacts yet', 'Add people first, then you can pick them here.');
    }
    if (!matches.length) return `<p class="hint">No one matches "${esc(query)}".</p>`;
    return `<ul class="pick-list">${matches.map((p) => `
      <li>
        <label class="pick-row">
          <input type="checkbox" data-person="${esc(p.id)}" ${chosen.has(p.id) ? 'checked' : ''}>
          <span class="pick-who">
            <strong>${esc(p.name)}</strong>
            <span>${esc(formatPhone(p.phone))}</span>
          </span>
        </label>
      </li>`).join('')}</ul>`;
  }

  function groupsHTML() {
    if (!showGroups || !allGroups.length) return '';
    return `
      <div class="pick-groups">
        <p class="label-sm">Groups — tap to add everyone in it</p>
        <div class="chip-row">
          ${allGroups.map((g) => {
            const st = groupState(g);
            return `<button class="chip-btn ${st}" data-group="${esc(g.id)}">
                ${esc(g.name)} <span>${g.memberIds.length}</span>
              </button>`;
          }).join('')}
        </div>
      </div>`;
  }

  function countHTML() {
    return `${pluralize(chosen.size, 'person', 'people')} selected`;
  }

  openSheet({
    title,
    body: `
      ${groupsHTML()}
      <div class="pick-tools">
        <input id="pick-search" class="input" type="search" placeholder="Search contacts" autocomplete="off">
        <button class="btn small ghost" data-act="all">All</button>
        <button class="btn small ghost" data-act="none">None</button>
      </div>
      <div class="pick-body">${listHTML()}</div>
      <div class="sheet-actions sticky">
        <span class="count" data-count>${countHTML()}</span>
        <button class="btn primary" data-act="picker-done">${esc(confirmLabel)}</button>
      </div>`,
    mount(root) {
      const body = $('.pick-body', root);
      const search = $('#pick-search', root);

      const refreshChips = () => {
        $$('[data-group]', root).forEach((btn) => {
          const g = store.group(btn.dataset.group);
          btn.className = `chip-btn ${g ? groupState(g) : 'none'}`;
        });
        $('[data-count]', root).textContent = countHTML();
      };

      search?.addEventListener('input', () => {
        query = search.value;
        body.innerHTML = listHTML();
      });

      root.addEventListener('change', (e) => {
        const box = e.target.closest('[data-person]');
        if (!box) return;
        if (box.checked) chosen.add(box.dataset.person);
        else chosen.delete(box.dataset.person);
        refreshChips();
      });

      root.addEventListener('click', (e) => {
        const groupBtn = e.target.closest('[data-group]');
        if (groupBtn) {
          const g = store.group(groupBtn.dataset.group);
          const members = g.memberIds.filter((id) => store.person(id));
          const addAll = groupState(g) !== 'all';
          members.forEach((id) => (addAll ? chosen.add(id) : chosen.delete(id)));
          body.innerHTML = listHTML();
          refreshChips();
          return;
        }
        // Scoped to this sheet: an editor sheet may be sitting underneath with its own buttons.
        const act = e.target.closest('[data-act]')?.dataset.act;
        if (act === 'all') {
          allPeople.forEach((p) => chosen.add(p.id));
          body.innerHTML = listHTML();
          refreshChips();
        } else if (act === 'none') {
          chosen.clear();
          body.innerHTML = listHTML();
          refreshChips();
        } else if (act === 'picker-done') {
          onSave([...chosen]);
          closeSheet();
        }
      });
    },
  });
}
