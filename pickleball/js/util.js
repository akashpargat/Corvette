// Small shared helpers: ids, escaping, dates, phone numbers.

export function uid(prefix = 'id') {
  return `${prefix}_${Math.random().toString(36).slice(2, 9)}${Date.now().toString(36).slice(-4)}`;
}

export function esc(value) {
  return String(value ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

/* ---------- phone numbers ---------- */

// Keep digits, and a leading +. Everything else is decoration.
export function normalizePhone(raw) {
  const trimmed = String(raw ?? '').trim();
  const plus = trimmed.startsWith('+') ? '+' : '';
  return plus + trimmed.replace(/\D/g, '');
}

export function formatPhone(raw) {
  const n = normalizePhone(raw);
  const m = /^(\+1)?(\d{3})(\d{3})(\d{4})$/.exec(n);
  return m ? `(${m[2]}) ${m[3]}-${m[4]}` : n;
}

export function isValidPhone(raw) {
  const digits = normalizePhone(raw).replace(/\D/g, '');
  return digits.length >= 7 && digits.length <= 15;
}

/* ---------- dates ---------- */

const DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

// Parse 'YYYY-MM-DD' as a local date so the day never slips a timezone.
export function parseDate(iso) {
  const [y, m, d] = String(iso).split('-').map(Number);
  return new Date(y, m - 1, d);
}

export function toISO(date) {
  const p = (n) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${p(date.getMonth() + 1)}-${p(date.getDate())}`;
}

export function today() {
  const d = new Date();
  d.setHours(0, 0, 0, 0);
  return d;
}

export function dayName(iso) {
  return DAY_NAMES[parseDate(iso).getDay()];
}

// 'Wed, Aug 19'
export function shortDate(iso) {
  return parseDate(iso).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' });
}

// 'Aug 19'
export function monthDay(iso) {
  return parseDate(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

// Next occurrence of a weekday index (0=Sun). Today counts as "next" only if allowToday.
export function nextWeekday(weekdayIndex, allowToday = false) {
  const d = today();
  let delta = (weekdayIndex - d.getDay() + 7) % 7;
  if (delta === 0 && !allowToday) delta = 7;
  d.setDate(d.getDate() + delta);
  return toISO(d);
}

export function isPast(iso) {
  return parseDate(iso) < today();
}

export function daysUntil(iso) {
  return Math.round((parseDate(iso) - today()) / 86400000);
}

export function relativeDay(iso) {
  const n = daysUntil(iso);
  if (n === 0) return 'Today';
  if (n === 1) return 'Tomorrow';
  if (n < 0) return `${Math.abs(n)}d ago`;
  if (n < 7) return `in ${n}d`;
  return '';
}

// '18:00' -> '6:00 PM'
export function formatTime(hhmm) {
  const m = /^(\d{1,2}):(\d{2})$/.exec(String(hhmm ?? '').trim());
  if (!m) return String(hhmm ?? '');
  let h = Number(m[1]);
  const suffix = h >= 12 ? 'PM' : 'AM';
  h = h % 12 || 12;
  return `${h}:${m[2]} ${suffix}`;
}

export function sortByName(a, b) {
  return String(a.name).localeCompare(String(b.name), undefined, { sensitivity: 'base' });
}

export function firstName(fullName) {
  return String(fullName ?? '').trim().split(/\s+/)[0] || '';
}

export function pluralize(n, one, many = `${one}s`) {
  return `${n} ${n === 1 ? one : many}`;
}
