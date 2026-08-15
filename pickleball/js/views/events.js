// Events: the list of play dates, the roster/response screen, and the create form.

import * as store from '../store.js';
import {
  esc, shortDate, dayName, monthDay, formatTime, formatPhone, relativeDay,
  isPast, nextWeekday, toISO, today, pluralize, firstName,
} from '../util.js';
import { toast, emptyState, confirmDialog, openSheet, closeSheet, $, $$ } from '../ui.js';
import { go, back } from '../router.js';
import { openPicker } from './picker.js';
import { openSendSheet } from './send.js';
import { smsHref } from '../sms.js';

/* ================= list ================= */

export function renderEventList() {
  const list = store.events();
  if (!list.length) {
    return {
      title: 'Pickleball',
      html: emptyState(
        '🎾',
        'No play dates yet',
        'Create one for Wednesday, Friday or Saturday, then ask your people who is in.',
        '<button class="btn primary" data-act="new-event">Create a play date</button>',
      ),
    };
  }

  const upcoming = list.filter((e) => !isPast(e.date));
  const past = list.filter((e) => isPast(e.date));

  const card = (evt) => {
    const t = store.tally(evt);
    const pct = evt.target ? Math.min(100, (t.yes / evt.target) * 100) : 0;
    const rel = relativeDay(evt.date);
    return `
      <li class="card event-card ${isPast(evt.date) ? 'past' : ''}" data-open-event="${esc(evt.id)}">
        <div class="event-when">
          <span class="dow">${esc(dayName(evt.date).slice(0, 3))}</span>
          <span class="dom">${esc(monthDay(evt.date))}</span>
        </div>
        <div class="event-main">
          <h3>${esc(formatTime(evt.time))} · ${esc(evt.place)}</h3>
          <p class="counts">
            <span class="chip chip-yes">${t.yes} in</span>
            <span class="chip chip-pending">${t.pending} waiting</span>
            <span class="chip chip-no">${t.no} out</span>
          </p>
          ${evt.target ? `
            <div class="progress-bar slim ${t.yes >= evt.target ? 'full' : ''}">
              <span style="width:${pct}%"></span>
            </div>
            <p class="need">${t.yes >= evt.target
              ? `Full — ${t.yes} of ${evt.target}`
              : `Need ${pluralize(t.short, 'more player')} (${t.yes}/${evt.target})`}</p>` : ''}
        </div>
        ${rel ? `<span class="rel">${esc(rel)}</span>` : ''}
      </li>`;
  };

  return {
    title: 'Pickleball',
    html: `
      ${upcoming.length ? `<ul class="list">${upcoming.map(card).join('')}</ul>`
        : '<p class="hint">Nothing coming up. Create the next play date below.</p>'}
      <button class="btn primary block" data-act="new-event">+ New play date</button>
      ${past.length ? `
        <h2 class="section-head">Past</h2>
        <ul class="list">${past.slice(0, 12).map(card).join('')}</ul>` : ''}`,
  };
}

/* ================= detail ================= */

export function renderEventDetail(id) {
  const evt = store.event(id);
  if (!evt) return { title: 'Not found', html: '<p class="hint">That play date is gone.</p>' };

  const t = store.tally(evt);
  const groups = {
    yes: store.rosterByStatus(evt, 'yes'),
    pending: store.rosterByStatus(evt, 'pending'),
    no: store.rosterByStatus(evt, 'no'),
  };

  const row = (entry) => {
    const p = entry.person;
    return `
      <li class="roster-row">
        <div class="roster-who">
          <strong>${esc(p.name)}</strong>
          <span>${esc(formatPhone(p.phone))}${entry.askedAt ? ' · asked' : ''}${entry.remindedAt ? ' · reminded' : ''}</span>
        </div>
        <div class="roster-actions">
          <button class="pill yes ${entry.status === 'yes' ? 'on' : ''}"
                  data-respond="yes" data-person="${esc(p.id)}" aria-label="${esc(p.name)} said yes">Yes</button>
          <button class="pill no ${entry.status === 'no' ? 'on' : ''}"
                  data-respond="no" data-person="${esc(p.id)}" aria-label="${esc(p.name)} said no">No</button>
        </div>
      </li>`;
  };

  const section = (key, label, hint) => (groups[key].length ? `
    <section class="roster-section ${key}">
      <h3>${label} <span class="n">${groups[key].length}</span></h3>
      ${hint ? `<p class="hint tight">${esc(hint)}</p>` : ''}
      <ul class="list flush">${groups[key].map(row).join('')}</ul>
    </section>` : '');

  const noRoster = !evt.roster.length;

  return {
    title: dayName(evt.date),
    back: '/events',
    html: `
      <div class="event-head">
        <h2>${esc(shortDate(evt.date))}</h2>
        <p>${esc(formatTime(evt.time))} · ${esc(evt.place)}</p>
        <div class="head-actions">
          <button class="btn small ghost" data-act="edit-event">Edit details</button>
          <button class="btn small ghost" data-act="edit-invitees">Who's invited</button>
        </div>
      </div>

      <div class="tally">
        <div class="tally-cell yes"><b>${t.yes}</b><span>in</span></div>
        <div class="tally-cell pending"><b>${t.pending}</b><span>waiting</span></div>
        <div class="tally-cell no"><b>${t.no}</b><span>out</span></div>
      </div>
      ${evt.target ? `<p class="need big">${t.yes >= evt.target
        ? `✓ You have enough — ${t.yes} of ${evt.target}`
        : `Need ${pluralize(t.short, 'more player')} to hit ${evt.target}`}</p>` : ''}

      ${noRoster
        ? emptyState('👥', 'Nobody invited yet', 'Pick people or a whole group to ask.',
            '<button class="btn primary" data-act="edit-invitees">Choose who to ask</button>')
        : `
        <div class="action-stack">
          ${t.pending ? `
            <button class="btn primary block" data-act="ask">
              ${t.pending === t.total ? `Ask all ${t.total}` : `Ask the ${pluralize(t.pending, 'person', 'people')} still waiting`}
            </button>` : ''}
          <button class="btn ${t.pending ? 'outline' : 'primary'} block" data-act="remind" ${t.yes ? '' : 'disabled'}>
            Remind the ${t.yes} playing
          </button>
          <div class="mini-row">
            ${t.pending !== t.total ? '<button class="link-btn" data-act="ask-all">Re-ask everyone</button>' : ''}
            ${t.yes ? `
              <a class="link-btn" href="${esc(smsHref(groups.yes.map((r) => r.person.phone), ''))}">Group thread</a>
              <button class="link-btn" data-act="save-group">Save yes list as a group</button>` : ''}
          </div>
        </div>

        ${section('pending', 'Waiting on', 'Tap Yes or No as each reply comes in.')}
        ${section('yes', 'Playing')}
        ${section('no', "Can't make it")}`}

      <button class="btn danger-ghost block spaced" data-act="delete-event">Delete this play date</button>`,
  };
}

/* ================= create / edit form ================= */

const QUICK_DAYS = [['Wed', 3], ['Fri', 5], ['Sat', 6]];

// Draft lives outside render so picking invitees does not lose typed values.
let draft = null;

export function renderEventForm(id = null) {
  const existing = id ? store.event(id) : null;
  const s = store.settings();

  if (!draft || draft.id !== (id || 'new')) {
    draft = existing
      ? { id, date: existing.date, time: existing.time, place: existing.place, target: existing.target,
          invitees: existing.roster.map((r) => r.personId) }
      : { id: 'new', date: nextWeekday(3), time: s.defaultTime, place: s.defaultPlace,
          target: s.defaultTarget, invitees: [] };
  }

  return {
    title: existing ? 'Edit play date' : 'New play date',
    back: existing ? `/event/${id}` : '/events',
    html: `
      <div class="chip-row day-quick">
        ${QUICK_DAYS.map(([label, idx]) => {
          const iso = nextWeekday(idx);
          return `<button class="chip-btn ${draft.date === iso ? 'all' : 'none'}" data-quick-day="${esc(iso)}">
            ${label} <span>${esc(monthDay(iso))}</span>
          </button>`;
        }).join('')}
      </div>

      <label class="field"><span>Date</span>
        <input class="input" type="date" id="f-date" value="${esc(draft.date)}" min="${esc(toISO(today()))}">
      </label>
      <label class="field"><span>Start time</span>
        <input class="input" type="time" id="f-time" value="${esc(draft.time)}">
      </label>
      <label class="field"><span>Where</span>
        <input class="input" type="text" id="f-place" value="${esc(draft.place)}" placeholder="the pickleball facility">
      </label>
      <label class="field"><span>Players needed</span>
        <input class="input" type="number" id="f-target" value="${esc(draft.target)}" min="0" max="64" inputmode="numeric">
        <small>Used for the "need 3 more" counter. 8 fills two doubles courts.</small>
      </label>

      <button class="btn outline block" data-act="pick-invitees">
        ${draft.invitees.length ? `Inviting ${pluralize(draft.invitees.length, 'person', 'people')} — change` : 'Choose who to ask'}
      </button>
      ${draft.invitees.length ? `<p class="hint tight">${esc(
        draft.invitees.map((pid) => store.person(pid)?.name).filter(Boolean).join(', '),
      )}</p>` : ''}

      <button class="btn primary block spaced" data-act="save-event">
        ${existing ? 'Save changes' : 'Create play date'}
      </button>`,
  };
}

/* ================= interactions ================= */

function readForm(root) {
  return {
    date: $('#f-date', root)?.value || draft.date,
    time: $('#f-time', root)?.value || draft.time,
    place: $('#f-place', root)?.value ?? draft.place,
    target: Number($('#f-target', root)?.value ?? draft.target),
  };
}

export function wireEvents(root, rerender) {
  root.addEventListener('click', async (e) => {
    const openCard = e.target.closest('[data-open-event]');
    if (openCard) {
      go(`/event/${openCard.dataset.openEvent}`);
      return;
    }

    const quick = e.target.closest('[data-quick-day]');
    if (quick) {
      Object.assign(draft, readForm(root), { date: quick.dataset.quickDay });
      rerender();
      return;
    }

    const respond = e.target.closest('[data-respond]');
    if (respond) {
      const eventId = currentEventId();
      store.setResponse(eventId, respond.dataset.person, respond.dataset.respond);
      rerender();
      return;
    }

    const act = e.target.closest('[data-act]')?.dataset.act;
    if (!act) return;
    const evt = store.event(currentEventId());

    switch (act) {
      case 'new-event':
        draft = null;
        go('/event/new');
        break;

      case 'edit-event':
        draft = null;
        go(`/event/${evt.id}/edit`);
        break;

      case 'pick-invitees':
        Object.assign(draft, readForm(root));
        openPicker({
          title: 'Who should I ask?',
          selected: draft.invitees,
          onSave: (ids) => { draft.invitees = ids; rerender(); },
        });
        break;

      case 'save-event': {
        const values = readForm(root);
        if (!values.date) { toast('Pick a date first'); return; }
        if (!values.place.trim()) { toast('Where are you playing?'); return; }
        if (draft.id === 'new') {
          const created = store.addEvent({ ...values, inviteeIds: draft.invitees });
          draft = null;
          go(`/event/${created.id}`);
          toast('Play date created');
        } else {
          store.updateEvent(draft.id, values);
          store.setInvitees(draft.id, draft.invitees);
          const savedId = draft.id;
          draft = null;
          go(`/event/${savedId}`);
          toast('Saved');
        }
        break;
      }

      case 'edit-invitees':
        openPicker({
          title: 'Who should I ask?',
          selected: evt.roster.map((r) => r.personId),
          onSave: (ids) => {
            store.setInvitees(evt.id, ids);
            rerender();
            toast(`${pluralize(ids.length, 'person', 'people')} invited`);
          },
        });
        break;

      case 'ask': {
        const pending = store.rosterByStatus(evt, 'pending').map((r) => r.person);
        openSendSheet({
          evt,
          people: pending.length ? pending : evt.roster.map((r) => store.person(r.personId)).filter(Boolean),
          kind: 'ask',
          onDone: rerender,
        });
        break;
      }

      case 'ask-all':
        openSendSheet({
          evt,
          people: evt.roster.map((r) => store.person(r.personId)).filter(Boolean),
          kind: 'ask',
          onDone: rerender,
        });
        break;

      case 'remind':
        openSendSheet({
          evt,
          people: store.rosterByStatus(evt, 'yes').map((r) => r.person),
          kind: 'reminder',
          onDone: rerender,
        });
        break;

      case 'save-group': {
        const yesPeople = store.rosterByStatus(evt, 'yes').map((r) => r.person);
        const suggested = `Pickleball ${dayName(evt.date).slice(0, 3)} ${monthDay(evt.date)}`;
        openSheet({
          title: 'Save the players as a group',
          body: `
            <p class="sheet-text">${pluralize(yesPeople.length, 'person', 'people')} said yes: ${esc(
              yesPeople.map((p) => firstName(p.name)).join(', '),
            )}</p>
            <label class="field"><span>Group name</span>
              <input class="input" id="g-name" type="text" value="${esc(suggested)}">
            </label>
            <div class="sheet-actions">
              <button class="btn ghost" data-sheet-close>Cancel</button>
              <button class="btn primary" data-save-group>Save group</button>
            </div>`,
          mount(sheet) {
            $('[data-save-group]', sheet).addEventListener('click', () => {
              const name = $('#g-name', sheet).value.trim();
              if (!name) { toast('Give the group a name'); return; }
              store.addGroup({ name, memberIds: yesPeople.map((p) => p.id) });
              closeSheet();
              toast(`Saved "${name}"`);
            });
          },
        });
        break;
      }

      case 'delete-event':
        if (await confirmDialog('Delete this play date and its responses?', { confirmLabel: 'Delete', danger: true })) {
          store.removeEvent(evt.id);
          toast('Deleted');
          back('/events');
        }
        break;

      default:
        break;
    }
  });
}

function currentEventId() {
  const parts = location.hash.replace(/^#/, '').split('/').filter(Boolean);
  return parts[0] === 'event' ? parts[1] : null;
}

export function resetDraft() {
  draft = null;
}
