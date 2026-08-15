// All app state lives in one localStorage blob. Small data, single user, no server.

import { uid, normalizePhone, sortByName, isPast, parseDate } from './util.js';

const KEY = 'pickleball-manager.v1';

export const DEFAULT_SETTINGS = {
  defaultTime: '06:00',
  defaultPlace: 'the pickleball facility',
  defaultTarget: 8,
  askTemplate:
    'Hi {first}! Pickleball on {day} {date} at {time}, {place}. Are you in? Reply YES or NO 🎾',
  reminderTemplate:
    "Don't forget {first} — pickleball {day} {date} at {time}, {place}. See you on the court! 🎾",
  sendMode: 'individual', // 'individual' | 'group'
};

const EMPTY = { people: [], groups: [], events: [], settings: { ...DEFAULT_SETTINGS } };

let state = load();
const listeners = new Set();

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return structuredClone(EMPTY);
    const parsed = JSON.parse(raw);
    return {
      people: Array.isArray(parsed.people) ? parsed.people : [],
      groups: Array.isArray(parsed.groups) ? parsed.groups : [],
      events: Array.isArray(parsed.events) ? parsed.events : [],
      settings: { ...DEFAULT_SETTINGS, ...(parsed.settings || {}) },
    };
  } catch (err) {
    console.error('Could not read saved data, starting empty.', err);
    return structuredClone(EMPTY);
  }
}

function persist() {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch (err) {
    console.error('Could not save data.', err);
    alert('Ran out of storage space — export a backup from Settings.');
  }
}

function commit() {
  persist();
  listeners.forEach((fn) => fn(state));
}

export function subscribe(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

export function getState() {
  return state;
}

/* ---------- people ---------- */

export function people() {
  return [...state.people].sort(sortByName);
}

export function person(id) {
  return state.people.find((p) => p.id === id) || null;
}

export function addPerson({ name, phone, note = '' }) {
  const entry = { id: uid('p'), name: name.trim(), phone: normalizePhone(phone), note: note.trim() };
  state.people.push(entry);
  commit();
  return entry;
}

export function updatePerson(id, patch) {
  const p = person(id);
  if (!p) return;
  if (patch.name !== undefined) p.name = patch.name.trim();
  if (patch.phone !== undefined) p.phone = normalizePhone(patch.phone);
  if (patch.note !== undefined) p.note = patch.note.trim();
  commit();
}

// Removing a person also pulls them out of every group and roster.
export function removePerson(id) {
  state.people = state.people.filter((p) => p.id !== id);
  state.groups.forEach((g) => {
    g.memberIds = g.memberIds.filter((m) => m !== id);
  });
  state.events.forEach((e) => {
    e.roster = e.roster.filter((r) => r.personId !== id);
  });
  commit();
}

// Returns the existing person when the number is already known, so bulk import is re-runnable.
export function findByPhone(phone) {
  const target = normalizePhone(phone);
  if (!target) return null;
  return state.people.find((p) => p.phone === target) || null;
}

/* ---------- groups ---------- */

export function groups() {
  return [...state.groups].sort(sortByName);
}

export function group(id) {
  return state.groups.find((g) => g.id === id) || null;
}

export function addGroup({ name, memberIds = [] }) {
  const entry = { id: uid('g'), name: name.trim(), memberIds: [...new Set(memberIds)] };
  state.groups.push(entry);
  commit();
  return entry;
}

export function updateGroup(id, patch) {
  const g = group(id);
  if (!g) return;
  if (patch.name !== undefined) g.name = patch.name.trim();
  if (patch.memberIds !== undefined) g.memberIds = [...new Set(patch.memberIds)];
  commit();
}

export function removeGroup(id) {
  state.groups = state.groups.filter((g) => g.id !== id);
  commit();
}

export function groupsForPerson(personId) {
  return groups().filter((g) => g.memberIds.includes(personId));
}

/* ---------- events ---------- */

export function events() {
  // Upcoming first (soonest at top), then past (most recent first).
  const upcoming = state.events.filter((e) => !isPast(e.date)).sort((a, b) => a.date.localeCompare(b.date));
  const past = state.events.filter((e) => isPast(e.date)).sort((a, b) => b.date.localeCompare(a.date));
  return [...upcoming, ...past];
}

export function event(id) {
  return state.events.find((e) => e.id === id) || null;
}

export function addEvent({ date, time, place, target, inviteeIds = [] }) {
  const entry = {
    id: uid('e'),
    date,
    time,
    place: place.trim(),
    target: Number(target) || 0,
    createdAt: new Date().toISOString(),
    askSentAt: null,
    reminderSentAt: null,
    roster: [...new Set(inviteeIds)].map((personId) => ({
      personId,
      status: 'pending', // 'pending' | 'yes' | 'no'
      askedAt: null,
      remindedAt: null,
      respondedAt: null,
    })),
  };
  state.events.push(entry);
  commit();
  return entry;
}

export function updateEvent(id, patch) {
  const e = event(id);
  if (!e) return;
  Object.assign(e, patch);
  commit();
}

export function removeEvent(id) {
  state.events = state.events.filter((e) => e.id !== id);
  commit();
}

export function setInvitees(eventId, personIds) {
  const e = event(eventId);
  if (!e) return;
  const wanted = [...new Set(personIds)];
  const kept = e.roster.filter((r) => wanted.includes(r.personId));
  const existing = new Set(kept.map((r) => r.personId));
  const added = wanted
    .filter((id) => !existing.has(id))
    .map((personId) => ({ personId, status: 'pending', askedAt: null, remindedAt: null, respondedAt: null }));
  e.roster = [...kept, ...added];
  commit();
}

// Tapping the status a person already has clears them back to pending.
export function setResponse(eventId, personId, status) {
  const e = event(eventId);
  const row = e?.roster.find((r) => r.personId === personId);
  if (!row) return;
  const next = row.status === status ? 'pending' : status;
  row.status = next;
  row.respondedAt = next === 'pending' ? null : new Date().toISOString();
  commit();
}

export function markAsked(eventId, personIds) {
  const e = event(eventId);
  if (!e) return;
  const stamp = new Date().toISOString();
  const ids = new Set(personIds);
  e.roster.forEach((r) => {
    if (ids.has(r.personId)) r.askedAt = stamp;
  });
  e.askSentAt = stamp;
  commit();
}

export function markReminded(eventId, personIds) {
  const e = event(eventId);
  if (!e) return;
  const stamp = new Date().toISOString();
  const ids = new Set(personIds);
  e.roster.forEach((r) => {
    if (ids.has(r.personId)) r.remindedAt = stamp;
  });
  e.reminderSentAt = stamp;
  commit();
}

/* ---------- derived ---------- */

export function tally(evt) {
  const counts = { yes: 0, no: 0, pending: 0, total: evt.roster.length };
  evt.roster.forEach((r) => { counts[r.status] += 1; });
  counts.short = Math.max(0, (evt.target || 0) - counts.yes);
  return counts;
}

export function rosterByStatus(evt, status) {
  return evt.roster
    .filter((r) => r.status === status)
    .map((r) => ({ ...r, person: person(r.personId) }))
    .filter((r) => r.person)
    .sort((a, b) => sortByName(a.person, b.person));
}

// Expands a mixed selection of person ids and group ids into a deduped person list.
export function resolveRecipients({ personIds = [], groupIds = [] }) {
  const ids = new Set(personIds);
  groupIds.forEach((gid) => group(gid)?.memberIds.forEach((id) => ids.add(id)));
  return [...ids].map((id) => person(id)).filter(Boolean).sort(sortByName);
}

export function settings() {
  return state.settings;
}

export function updateSettings(patch) {
  Object.assign(state.settings, patch);
  commit();
}

/* ---------- backup ---------- */

export function exportJSON() {
  return JSON.stringify({ ...state, exportedAt: new Date().toISOString(), version: 1 }, null, 2);
}

export function importJSON(text, { replace = true } = {}) {
  const parsed = JSON.parse(text);
  if (!parsed || typeof parsed !== 'object') throw new Error('That file is not app data.');
  const incoming = {
    people: Array.isArray(parsed.people) ? parsed.people : [],
    groups: Array.isArray(parsed.groups) ? parsed.groups : [],
    events: Array.isArray(parsed.events) ? parsed.events : [],
    settings: { ...DEFAULT_SETTINGS, ...(parsed.settings || {}) },
  };
  if (replace) {
    state = incoming;
  } else {
    const known = new Set(state.people.map((p) => p.phone));
    state.people.push(...incoming.people.filter((p) => !known.has(p.phone)));
    const ids = new Set(state.groups.map((g) => g.id));
    state.groups.push(...incoming.groups.filter((g) => !ids.has(g.id)));
    const eventIds = new Set(state.events.map((e) => e.id));
    state.events.push(...incoming.events.filter((e) => !eventIds.has(e.id)));
  }
  commit();
  return incoming;
}

export function clearAll() {
  state = structuredClone(EMPTY);
  commit();
}

/* ---------- seed ---------- */

// One tap in Settings to see how the app behaves with data in it.
export function loadSample() {
  const names = [
    ['Ravi Menon', '+15551230001'], ['Dana Whitfield', '+15551230002'],
    ['Marcus Lee', '+15551230003'], ['Priya Shah', '+15551230004'],
    ['Tom Okafor', '+15551230005'], ['Elena Vasquez', '+15551230006'],
    ['Chris Bell', '+15551230007'], ['Nina Park', '+15551230008'],
    ['Sam Reyes', '+15551230009'], ['Joy Adeyemi', '+15551230010'],
  ];
  const added = names.map(([name, phone]) => findByPhone(phone) || addPerson({ name, phone }));
  addGroup({ name: 'Morning regulars', memberIds: added.slice(0, 6).map((p) => p.id) });
  addGroup({ name: 'Weekend crew', memberIds: added.slice(4).map((p) => p.id) });
  const nextWed = (() => {
    const d = new Date();
    d.setDate(d.getDate() + ((3 - d.getDay() + 7) % 7 || 7));
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  })();
  const evt = addEvent({
    date: nextWed,
    time: state.settings.defaultTime,
    place: state.settings.defaultPlace,
    target: state.settings.defaultTarget,
    inviteeIds: added.map((p) => p.id),
  });
  ['yes', 'yes', 'yes', 'no', 'yes'].forEach((status, i) => setResponse(evt.id, added[i].id, status));
  return evt.id;
}

/* ---------- misc ---------- */

export function eventTitle(evt) {
  const d = parseDate(evt.date);
  return d.toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' });
}
