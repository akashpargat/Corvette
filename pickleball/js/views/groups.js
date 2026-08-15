// Groups: reusable sets of people, so one tap invites the whole crew.

import * as store from '../store.js';
import { esc, pluralize, firstName } from '../util.js';
import { toast, emptyState, confirmDialog, openSheet, closeSheet, $ } from '../ui.js';
import { openPicker } from './picker.js';
import { openBroadcastSheet } from './send.js';

export function renderGroups() {
  const all = store.groups();
  if (!all.length) {
    return {
      title: 'Groups',
      html: emptyState(
        '👥',
        'No groups yet',
        'A group is a shortcut — "Morning regulars", "Weekend crew". Pick the group and everyone in it gets asked.',
        '<button class="btn primary" data-act="add-group">Create a group</button>',
      ),
    };
  }

  return {
    title: 'Groups',
    html: `
      <ul class="list">
        ${all.map((g) => {
          const members = g.memberIds.map((id) => store.person(id)).filter(Boolean);
          return `
            <li class="card group-card" data-edit-group="${esc(g.id)}">
              <div class="person-main">
                <strong>${esc(g.name)}</strong>
                <span>${pluralize(members.length, 'person', 'people')}</span>
                ${members.length ? `<p class="note">${esc(members.map((p) => firstName(p.name)).join(', '))}</p>` : ''}
              </div>
              <span class="chev" aria-hidden="true">›</span>
            </li>`;
        }).join('')}
      </ul>
      <button class="btn primary block" data-act="add-group">+ New group</button>`,
  };
}

function groupSheet(id, rerender) {
  const existing = id ? store.group(id) : null;
  // Working copy — nothing reaches the store until Save.
  let name = existing?.name ?? '';
  let members = existing ? [...existing.memberIds] : [];

  const body = () => `
    <label class="field"><span>Group name</span>
      <input class="input" id="g-name" type="text" value="${esc(name)}" placeholder="Morning regulars">
    </label>
    <button class="btn outline block" data-act="pick">
      ${members.length ? `${pluralize(members.length, 'member')} — change` : 'Add members'}
    </button>
    <p class="hint tight">${esc(
      members.map((pid) => store.person(pid)?.name).filter(Boolean).join(', ') || 'Nobody in this group yet.',
    )}</p>
    <div class="sheet-actions">
      ${existing ? '<button class="btn danger-ghost" data-act="delete">Delete</button>' : ''}
      <button class="btn primary" data-act="save">${existing ? 'Save' : 'Create'}</button>
    </div>
    ${members.length ? '<button class="btn outline block" data-act="text-group">Message these people now</button>' : ''}`;

  openSheet({
    title: existing ? 'Edit group' : 'New group',
    body: body(),
    mount(sheet) {
      const panel = $('.sheet-body', sheet);
      if (!existing) $('#g-name', sheet).focus();

      sheet.addEventListener('input', (e) => {
        if (e.target.id === 'g-name') name = e.target.value;
      });

      sheet.addEventListener('click', async (e) => {
        const act = e.target.closest('[data-act]')?.dataset.act;
        if (!act) return;

        if (act === 'pick') {
          openPicker({
            title: 'Who is in this group?',
            selected: members,
            showGroups: false,
            onSave: (ids) => {
              members = ids;
              panel.innerHTML = body(); // picker closes back to this sheet
            },
          });
        } else if (act === 'save') {
          if (!name.trim()) { toast('Give the group a name'); return; }
          if (existing) store.updateGroup(id, { name, memberIds: members });
          else store.addGroup({ name, memberIds: members });
          closeSheet();
          rerender();
          toast(existing ? 'Saved' : `"${name.trim()}" created`);
        } else if (act === 'delete') {
          if (await confirmDialog(`Delete "${existing.name}"? The contacts themselves stay.`,
            { confirmLabel: 'Delete', danger: true })) {
            store.removeGroup(id);
            closeSheet();
            rerender();
            toast('Group deleted');
          }
        } else if (act === 'text-group') {
          const people = members.map((pid) => store.person(pid)).filter(Boolean);
          openBroadcastSheet({ people, title: name.trim() || 'group' });
        }
      });
    },
  });
}

export function wireGroups(root, rerender) {
  root.addEventListener('click', (e) => {
    const edit = e.target.closest('[data-edit-group]');
    if (edit) { groupSheet(edit.dataset.editGroup, rerender); return; }
    if (e.target.closest('[data-act="add-group"]')) groupSheet(null, rerender);
  });
}
