// Defaults, message templates, and backup/restore.

import * as store from '../store.js';
import { esc } from '../util.js';
import { toast, confirmDialog, openSheet, closeSheet, $ } from '../ui.js';
import { PLACEHOLDERS } from '../sms.js';
import { go } from '../router.js';

export function renderSettings() {
  const s = store.settings();
  const state = store.getState();

  return {
    title: 'Settings',
    html: `
      <section class="panel">
        <h3>Defaults for a new play date</h3>
        <label class="field"><span>Start time</span>
          <input class="input" type="time" id="s-time" value="${esc(s.defaultTime)}">
        </label>
        <label class="field"><span>Where you play</span>
          <input class="input" type="text" id="s-place" value="${esc(s.defaultPlace)}">
        </label>
        <label class="field"><span>Players needed</span>
          <input class="input" type="number" id="s-target" value="${esc(s.defaultTarget)}" min="0" max="64" inputmode="numeric">
        </label>
      </section>

      <section class="panel">
        <h3>Message templates</h3>
        <label class="field"><span>Asking who is in</span>
          <textarea id="s-ask" rows="3">${esc(s.askTemplate)}</textarea>
        </label>
        <label class="field"><span>Reminder</span>
          <textarea id="s-remind" rows="3">${esc(s.reminderTemplate)}</textarea>
        </label>
        <p class="hint tight">${PLACEHOLDERS.map(([t, d]) => `<code>${esc(t)}</code> ${esc(d)}`).join(' · ')}</p>
      </section>

      <button class="btn primary block" data-act="save-settings">Save settings</button>

      <section class="panel">
        <h3>Your data</h3>
        <p class="hint tight">
          ${state.people.length} contacts · ${state.groups.length} groups · ${state.events.length} play dates.
          Everything is stored on this phone only — nothing is uploaded anywhere. Clearing your browser
          data would wipe it, so keep a backup.
        </p>
        <div class="row-2">
          <button class="btn outline" data-act="export">Download backup</button>
          <button class="btn outline" data-act="import">Restore backup</button>
        </div>
        <button class="btn ghost block" data-act="sample">Load sample data</button>
        <button class="btn danger-ghost block" data-act="wipe">Erase everything</button>
      </section>

      <section class="panel">
        <h3>How the replies work</h3>
        <p class="hint tight">
          A web app can't read your incoming texts — no browser allows it, on any phone. So when
          someone replies YES or NO, open the play date and tap their Yes or No button. That one tap
          keeps the count, the playing list and the reminder list correct.
        </p>
      </section>

      <p class="version">Pickleball Manager · offline-ready</p>`,
  };
}

function importSheet(rerender) {
  openSheet({
    title: 'Restore a backup',
    body: `
      <p class="hint">Pick a backup file, or paste its contents below.</p>
      <input class="input" type="file" id="imp-file" accept="application/json,.json">
      <label class="field"><span>Or paste JSON</span>
        <textarea id="imp-text" rows="6" placeholder='{"people": [...]}'></textarea>
      </label>
      <label class="check">
        <input type="checkbox" id="imp-merge">
        <span>Merge into what I already have (instead of replacing it)</span>
      </label>
      <div class="sheet-actions">
        <button class="btn ghost" data-sheet-close>Cancel</button>
        <button class="btn primary" data-act="do-import">Restore</button>
      </div>`,
    mount(sheet) {
      const file = $('#imp-file', sheet);
      const text = $('#imp-text', sheet);
      file.addEventListener('change', async () => {
        const f = file.files?.[0];
        if (f) text.value = await f.text();
      });
      $('[data-act="do-import"]', sheet).addEventListener('click', () => {
        const raw = text.value.trim();
        if (!raw) { toast('Nothing to restore'); return; }
        try {
          store.importJSON(raw, { replace: !$('#imp-merge', sheet).checked });
          closeSheet();
          rerender();
          toast('Backup restored');
        } catch (err) {
          toast(`Could not read that: ${err.message}`);
        }
      });
    },
  });
}

function download(filename, contents) {
  const blob = new Blob([contents], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function wireSettings(root, rerender) {
  root.addEventListener('click', async (e) => {
    const act = e.target.closest('[data-act]')?.dataset.act;
    if (!act) return;

    if (act === 'save-settings') {
      store.updateSettings({
        defaultTime: $('#s-time', root).value || '06:00',
        defaultPlace: $('#s-place', root).value.trim(),
        defaultTarget: Number($('#s-target', root).value) || 0,
        askTemplate: $('#s-ask', root).value,
        reminderTemplate: $('#s-remind', root).value,
      });
      toast('Settings saved');
    } else if (act === 'export') {
      const stamp = new Date().toISOString().slice(0, 10);
      download(`pickleball-backup-${stamp}.json`, store.exportJSON());
      toast('Backup downloaded');
    } else if (act === 'import') {
      importSheet(rerender);
    } else if (act === 'sample') {
      const eventId = store.loadSample();
      toast('Sample data loaded');
      go(`/event/${eventId}`);
    } else if (act === 'wipe') {
      if (await confirmDialog('Erase all contacts, groups and play dates on this phone?',
        { confirmLabel: 'Erase everything', danger: true })) {
        store.clearAll();
        rerender();
        toast('Everything erased');
      }
    }
  });
}
