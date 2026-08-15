// Building the text itself, and handing it off to the phone's messaging app.
//
// A web page can open a prefilled SMS draft, but it can never send silently and
// it can never read the replies back. Everything here stops at "draft is open".

import { dayName, monthDay, formatTime, firstName, normalizePhone } from './util.js';

export const PLACEHOLDERS = [
  ['{first}', "the person's first name"],
  ['{name}', 'their full name'],
  ['{day}', 'Wednesday'],
  ['{date}', 'Aug 19'],
  ['{time}', '6:00 AM'],
  ['{place}', 'where you play'],
  ['{count}', 'how many said yes'],
];

export function isIOS() {
  const ua = navigator.userAgent || '';
  // iPadOS 13+ reports itself as a Mac, so check for touch too.
  return /iPad|iPhone|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
}

// Fills a template. `person` is optional — for a group text there is no single name.
export function renderMessage(template, { evt, person = null, yesCount = 0 }) {
  const values = {
    '{first}': person ? firstName(person.name) : 'everyone',
    '{name}': person ? person.name : 'everyone',
    '{day}': dayName(evt.date),
    '{date}': monthDay(evt.date),
    '{time}': formatTime(evt.time),
    '{place}': evt.place,
    '{count}': String(yesCount),
  };
  return Object.entries(values).reduce(
    (text, [token, value]) => text.split(token).join(value),
    String(template ?? ''),
  );
}

// iOS wants `&body=`, everyone else wants `?body=`. Both accept comma-joined numbers.
export function smsHref(phones, body) {
  const list = (Array.isArray(phones) ? phones : [phones]).map(normalizePhone).filter(Boolean);
  const separator = isIOS() ? '&' : '?';
  return `sms:${list.join(',')}${separator}body=${encodeURIComponent(body)}`;
}

export function openSMS(phones, body) {
  window.location.href = smsHref(phones, body);
}

export async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Clipboard API needs a secure context; fall back to the old selection trick.
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch { ok = false; }
    ta.remove();
    return ok;
  }
}

export function canShare() {
  return typeof navigator.share === 'function';
}

export async function shareText(text) {
  try {
    await navigator.share({ text });
    return true;
  } catch {
    return false;
  }
}
