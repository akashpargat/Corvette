// Contacts: add, edit, bulk paste, and see which groups someone belongs to.

import * as store from '../store.js';
import { esc, formatPhone, normalizePhone, isValidPhone, pluralize } from '../util.js';
import { toast, emptyState, confirmDialog, openSheet, closeSheet, $ } from '../ui.js';
import { openBroadcastSheet } from './send.js';

let search = '';

export function renderPeople() {
  const all = store.people();
  const q = search.trim().toLowerCase();
  const shown = all.filter((p) => !q || p.name.toLowerCase().includes(q) || p.phone.includes(q));

  if (!all.length) {
    return {
      title: 'People',
      html: emptyState(
        '📇',
        'No contacts yet',
        'Add the people you play with. Name and mobile number is all it takes.',
        `<button class="btn primary" data-act="add-person">Add someone</button>
         <button class="btn ghost" data-act="bulk-add">Paste a list</button>`,
      ),
    };
  }

  return {
    title: 'People',
    html: `
      <div class="pick-tools">
        <input id="people-search" class="input" type="search" placeholder="Search ${all.length} contacts"
               value="${esc(search)}" autocomplete="off">
        <button class="btn small ghost" data-act="bulk-add">Paste</button>
      </div>
      ${shown.length ? `<ul class="list">${shown.map((p) => {
        const inGroups = store.groupsForPerson(p.id);
        return `
          <li class="card person-card" data-edit-person="${esc(p.id)}">
            <div class="person-main">
              <strong>${esc(p.name)}</strong>
              <span>${esc(formatPhone(p.phone))}</span>
              ${inGroups.length ? `<p class="tags">${inGroups.map((g) => `<span class="tag">${esc(g.name)}</span>`).join('')}</p>` : ''}
              ${p.note ? `<p class="note">${esc(p.note)}</p>` : ''}
            </div>
            <span class="chev" aria-hidden="true">›</span>
          </li>`;
      }).join('')}</ul>` : `<p class="hint">No one matches "${esc(search)}".</p>`}
      <button class="btn primary block" data-act="add-person">+ Add contact</button>`,
  };
}

function personSheet(id = null) {
  const p = id ? store.person(id) : null;
  openSheet({
    title: p ? 'Edit contact' : 'Add contact',
    body: `
      <label class="field"><span>Name</span>
        <input class="input" id="p-name" type="text" value="${esc(p?.name ?? '')}" placeholder="Ravi Menon" autocomplete="name">
      </label>
      <label class="field"><span>Mobile number</span>
        <input class="input" id="p-phone" type="tel" value="${esc(p?.phone ?? '')}" placeholder="+1 555 123 4567" autocomplete="tel">
      </label>
      <label class="field"><span>Note (optional)</span>
        <input class="input" id="p-note" type="text" value="${esc(p?.note ?? '')}" placeholder="3.5 · plays mornings">
      </label>
      <div class="sheet-actions">
        ${p ? '<button class="btn danger-ghost" data-act="delete">Delete</button>' : ''}
        <button class="btn primary" data-act="save">${p ? 'Save' : 'Add'}</button>
      </div>
      ${p ? '<button class="btn outline block" data-act="text-now">Send this person a text</button>' : ''}`,
    mount(sheet) {
      $('#p-name', sheet).focus();
      sheet.addEventListener('click', async (e) => {
        const act = e.target.closest('[data-act]')?.dataset.act;
        if (!act) return;
        if (act === 'save') {
          const name = $('#p-name', sheet).value.trim();
          const phone = $('#p-phone', sheet).value.trim();
          const note = $('#p-note', sheet).value.trim();
          if (!name) { toast('Name is required'); return; }
          if (!isValidPhone(phone)) { toast('That number looks off'); return; }
          const clash = store.findByPhone(phone);
          if (clash && clash.id !== id) { toast(`${clash.name} already has that number`); return; }
          if (p) store.updatePerson(id, { name, phone, note });
          else store.addPerson({ name, phone, note });
          closeSheet();
          toast(p ? 'Saved' : `${name} added`);
        } else if (act === 'delete') {
          if (await confirmDialog(`Remove ${p.name} from your contacts, groups and rosters?`,
            { confirmLabel: 'Remove', danger: true })) {
            store.removePerson(id);
            closeSheet();
            toast('Removed');
          }
        } else if (act === 'text-now') {
          closeSheet();
          openBroadcastSheet({ people: [p] });
        }
      });
    },
  });
}

function bulkSheet() {
  openSheet({
    title: 'Paste a list of people',
    body: `
      <p class="hint">One person per line: <code>Name, number</code>. Numbers already saved are skipped.</p>
      <label class="field"><span>List</span>
        <textarea id="bulk" rows="8" placeholder="Ravi Menon, 555-123-4567&#10;Dana Whitfield, +1 555 123 4568"></textarea>
      </label>
      <div class="sheet-actions">
        <button class="btn ghost" data-sheet-close>Cancel</button>
        <button class="btn primary" data-act="import">Add them</button>
      </div>`,
    mount(sheet) {
      $('#bulk', sheet).focus();
      $('[data-act="import"]', sheet).addEventListener('click', () => {
        const lines = $('#bulk', sheet).value.split('\n').map((l) => l.trim()).filter(Boolean);
        let added = 0;
        let skipped = 0;
        lines.forEach((line) => {
          // Split on the last comma/tab/semicolon so names with commas survive.
          const match = /^(.*)[,;\t]\s*([^,;\t]+)$/.exec(line);
          const name = (match ? match[1] : line.replace(/[\d+()\-.\s]+$/, '')).trim();
          const phone = normalizePhone(match ? match[2] : line);
          if (!name || !isValidPhone(phone) || store.findByPhone(phone)) { skipped += 1; return; }
          store.addPerson({ name, phone });
          added += 1;
        });
        closeSheet();
        toast(added
          ? `Added ${pluralize(added, 'contact')}${skipped ? `, skipped ${skipped}` : ''}`
          : 'Nothing to add — check the format');
      });
    },
  });
}

export function wirePeople(root, rerender) {
  root.addEventListener('input', (e) => {
    if (e.target.id === 'people-search') {
      search = e.target.value;
      rerender({ keepFocus: true });
    }
  });

  root.addEventListener('click', (e) => {
    const edit = e.target.closest('[data-edit-person]');
    if (edit) { personSheet(edit.dataset.editPerson); return; }
    const act = e.target.closest('[data-act]')?.dataset.act;
    if (act === 'add-person') personSheet();
    else if (act === 'bulk-add') bulkSheet();
  });
}
