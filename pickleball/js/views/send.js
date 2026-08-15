// The send sheet: preview the text, then hand each draft to the messaging app.
//
// A web page cannot send an SMS silently — it can only open a prefilled draft
// that you tap send on. Everything here stops at that line.

import * as store from '../store.js';
import { esc, firstName, formatPhone } from '../util.js';
import { openSheet, toast, $, $$ } from '../ui.js';
import { renderMessage, smsHref, copyText, canShare, shareText, PLACEHOLDERS } from '../sms.js';

/**
 * Shared engine for both flavours of sending.
 * @param {object} opts
 * @param {string} opts.title
 * @param {object[]} opts.people        recipients
 * @param {string} opts.template        starting message text
 * @param {(template: string, person: object|null) => string} opts.fill
 * @param {string[]} [opts.tokens]      placeholders offered as insert buttons
 * @param {Set<string>} [opts.alreadySent]
 * @param {(personId: string) => void} [opts.onSent]
 * @param {(template: string) => void} [opts.onSaveTemplate]
 * @param {() => void} [opts.onDone]
 */
function sendSheet({
  title, people, template, fill, tokens = PLACEHOLDERS.map(([t]) => t),
  alreadySent = new Set(), onSent, onSaveTemplate, onDone,
}) {
  let mode = store.settings().sendMode;
  const sent = new Set(alreadySent);

  const textFor = (person) => fill(template, person);

  function markSent(personId) {
    sent.add(personId);
    onSent?.(personId);
  }

  function queueHTML() {
    const next = people.find((p) => !sent.has(p.id));
    return `
      <p class="hint">
        Everyone gets their own text with their own name in it. Tap a name, your messaging app opens
        with the draft ready — send it there, then come back for the next one.
      </p>
      <div class="progress-row">
        <div class="progress-bar"><span style="width:${(sent.size / people.length) * 100}%"></span></div>
        <strong>${sent.size}/${people.length}</strong>
      </div>
      ${next
        ? `<a class="btn primary block" href="${esc(smsHref(next.phone, textFor(next)))}" data-send="${esc(next.id)}">
             Text ${esc(firstName(next.name))} →
           </a>`
        : `<p class="all-done">✓ All ${people.length} drafts opened.</p>`}
      <ul class="send-list">
        ${people.map((p) => `
          <li class="${sent.has(p.id) ? 'sent' : ''}">
            <div class="send-who">
              <strong>${esc(p.name)}</strong>
              <span>${esc(formatPhone(p.phone))}</span>
            </div>
            <div class="send-act">
              ${sent.has(p.id) ? '<span class="tick" title="Draft opened">✓</span>' : ''}
              <a class="btn small ${sent.has(p.id) ? 'ghost' : 'outline'}"
                 href="${esc(smsHref(p.phone, textFor(p)))}" data-send="${esc(p.id)}">
                ${sent.has(p.id) ? 'Again' : 'Text'}
              </a>
            </div>
          </li>`).join('')}
      </ul>
      ${sent.size ? '<button class="btn ghost block" data-act="reset-queue">Reset progress</button>' : ''}`;
  }

  function groupHTML() {
    const groupText = textFor(null);
    return `
      <p class="hint">
        One thread with everyone in it. Names can't be personalised here — <code>{first}</code> becomes
        "everyone", and replies all land in the same thread where everyone sees them.
      </p>
      <div class="preview-box">${esc(groupText)}</div>
      <a class="btn primary block" href="${esc(smsHref(people.map((p) => p.phone), groupText))}" data-act="group-sent">
        Open group text · ${people.length} ${people.length === 1 ? 'person' : 'people'}
      </a>
      <button class="btn outline block" data-act="copy-numbers">Copy all numbers</button>`;
  }

  openSheet({
    title,
    onClose: onDone,
    body: `
      <div class="seg" role="tablist">
        <button class="${mode === 'individual' ? 'on' : ''}" data-mode="individual" role="tab">One by one</button>
        <button class="${mode === 'group' ? 'on' : ''}" data-mode="group" role="tab">Group text</button>
      </div>

      <label class="field"><span>Message</span>
        <textarea id="send-template" rows="4">${esc(template)}</textarea>
      </label>
      <p class="tokens">${tokens.map((t) => `<button class="token" data-token="${esc(t)}">${esc(t)}</button>`).join('')}</p>
      <div class="preview-box preview-live">${esc(textFor(people[0]))}</div>

      <div class="send-panel">${mode === 'individual' ? queueHTML() : groupHTML()}</div>

      <div class="sheet-actions">
        <button class="btn ghost" data-act="copy">Copy text</button>
        ${canShare() ? '<button class="btn ghost" data-act="share">Share</button>' : ''}
        ${onSaveTemplate ? '<button class="btn outline" data-act="save-template">Save as default</button>' : ''}
      </div>`,
    mount(root) {
      const area = $('#send-template', root);
      const repaint = () => {
        $('.send-panel', root).innerHTML = mode === 'individual' ? queueHTML() : groupHTML();
        $('.preview-live', root).textContent = textFor(people[0]);
        $$('.seg button', root).forEach((b) => b.classList.toggle('on', b.dataset.mode === mode));
      };

      area.addEventListener('input', () => {
        template = area.value;
        repaint();
      });

      root.addEventListener('click', async (e) => {
        const token = e.target.closest('[data-token]');
        if (token) {
          const start = area.selectionStart ?? area.value.length;
          const end = area.selectionEnd ?? start;
          area.value = area.value.slice(0, start) + token.dataset.token + area.value.slice(end);
          template = area.value;
          const caret = start + token.dataset.token.length;
          area.focus();
          area.setSelectionRange(caret, caret);
          repaint();
          return;
        }

        // The anchor itself opens the SMS draft; we only record that it happened.
        const sendLink = e.target.closest('[data-send]');
        if (sendLink) {
          markSent(sendLink.dataset.send);
          setTimeout(repaint, 400);
          return;
        }

        const modeBtn = e.target.closest('[data-mode]');
        if (modeBtn) {
          mode = modeBtn.dataset.mode;
          store.updateSettings({ sendMode: mode });
          repaint();
          return;
        }

        const act = e.target.closest('[data-act]')?.dataset.act;
        if (!act) return;

        if (act === 'group-sent') {
          people.forEach((p) => markSent(p.id));
          setTimeout(repaint, 400);
        } else if (act === 'copy') {
          toast(await copyText(textFor(people[0])) ? 'Message copied' : 'Could not copy');
        } else if (act === 'copy-numbers') {
          toast(await copyText(people.map((p) => p.phone).join(', ')) ? 'Numbers copied' : 'Could not copy');
        } else if (act === 'share') {
          await shareText(textFor(people[0]));
        } else if (act === 'save-template') {
          onSaveTemplate(template);
          toast('Saved as your default');
        } else if (act === 'reset-queue') {
          sent.clear();
          repaint();
        }
      });
    },
  });
}

/** Ask-who's-in, or remind-the-players, for a specific play date. */
export function openSendSheet({ evt, people, kind, onDone }) {
  if (!people.length) {
    toast('Nobody to text yet.');
    return;
  }
  const s = store.settings();
  const yesCount = store.tally(evt).yes;
  const stampField = kind === 'ask' ? 'askedAt' : 'remindedAt';

  sendSheet({
    title: `${kind === 'ask' ? 'Ask who is in' : 'Send reminder'} · ${people.length}`,
    people,
    template: kind === 'ask' ? s.askTemplate : s.reminderTemplate,
    fill: (tpl, person) => renderMessage(tpl, { evt, person, yesCount }),
    alreadySent: new Set(
      evt.roster.filter((r) => r[stampField] && people.some((p) => p.id === r.personId)).map((r) => r.personId),
    ),
    onSent: (personId) => {
      if (kind === 'ask') store.markAsked(evt.id, [personId]);
      else store.markReminded(evt.id, [personId]);
    },
    onSaveTemplate: (tpl) => store.updateSettings(kind === 'ask' ? { askTemplate: tpl } : { reminderTemplate: tpl }),
    onDone,
  });
}

/** Free-form blast to any set of people, with no play date attached. */
export function openBroadcastSheet({ people, title = null }) {
  if (!people.length) {
    toast('Nobody to text.');
    return;
  }
  sendSheet({
    title: title ? `Message ${title}` : `Message ${people.length}`,
    people,
    template: 'Hi {first}! ',
    tokens: ['{first}', '{name}'],
    fill: (tpl, person) => tpl
      .split('{first}').join(person ? firstName(person.name) : 'everyone')
      .split('{name}').join(person ? person.name : 'everyone'),
  });
}
