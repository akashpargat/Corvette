// End-to-end walk through the whole app in a phone-sized browser.
//
//   npm i playwright && npx playwright install chromium
//   python3 -m http.server 8777          # from the repo root
//   node pickleball/tools/smoke-test.mjs
//
// Screenshots land in ./shots. Override the URL with BASE_URL, and point
// PW_CHROMIUM at a browser binary if you have one installed already.

import { chromium, devices } from 'playwright';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL || 'http://localhost:8777/pickleball/index.html';
const shots = 'shots';
mkdirSync(shots, { recursive: true });

const browser = await chromium.launch(
  process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {},
);
const ctx = await browser.newContext({ ...devices['Pixel 7'] });
const page = await ctx.newPage();

const errors = [];
page.on('pageerror', (e) => errors.push('PAGEERROR: ' + e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });

const step = async (name, fn) => {
  try { await fn(); console.log('✓', name); }
  catch (e) { console.log('✗', name, '—', e.message.split('\n')[0]); }
  await page.screenshot({ path: `${shots}/${name}.png` });
};

await page.goto(BASE);
await page.waitForTimeout(400);

await step('01-empty', async () => {
  if (!(await page.getByText('No play dates yet').isVisible())) throw new Error('empty state missing');
});

// Load sample data via settings
await step('02-settings', async () => {
  await page.click('a[href="#/settings"]');
  await page.waitForTimeout(200);
  await page.click('[data-act="sample"]');
  await page.waitForTimeout(400);
});

await step('03-event-detail', async () => {
  const t = await page.textContent('#app-title');
  if (!/day/i.test(t)) throw new Error('not on event detail, title=' + t);
  const yes = await page.textContent('.tally-cell.yes b');
  if (yes !== '4') throw new Error('expected 4 yes, got ' + yes);
});

await step('04-respond-toggle', async () => {
  const before = await page.textContent('.tally-cell.yes b');
  await page.click('.roster-section.pending .pill.yes');
  await page.waitForTimeout(200);
  const after = await page.textContent('.tally-cell.yes b');
  if (Number(after) !== Number(before) + 1) throw new Error(`yes ${before} -> ${after}`);
});

await step('05-send-sheet', async () => {
  await page.click('[data-act="ask"]');
  await page.waitForTimeout(300);
  if (!(await page.locator('.sheet').isVisible())) throw new Error('sheet did not open');
  const preview = await page.textContent('.preview-live');
  if (!/Pickleball on/.test(preview)) throw new Error('bad preview: ' + preview);
  const href = await page.getAttribute('[data-send]', 'href');
  if (!href.startsWith('sms:')) throw new Error('bad sms href: ' + href);
  console.log('   sms href:', href.slice(0, 90));
});

await step('06-send-group-mode', async () => {
  await page.click('[data-mode="group"]');
  await page.waitForTimeout(200);
  const href = await page.getAttribute('[data-act="group-sent"]', 'href');
  if ((href.match(/,/g) || []).length < 3) throw new Error('group href missing recipients');
  await page.click('[data-sheet-close]');
  await page.waitForTimeout(300);
});

await step('07-save-group', async () => {
  await page.click('[data-act="save-group"]');
  await page.waitForTimeout(300);
  await page.click('[data-save-group]');
  await page.waitForTimeout(300);
  await page.click('a[href="#/groups"]');
  await page.waitForTimeout(300);
  const n = await page.locator('.group-card').count();
  if (n !== 3) throw new Error('expected 3 groups, got ' + n);
});

await step('08-group-edit-picker-stack', async () => {
  await page.click('.group-card');
  await page.waitForTimeout(300);
  await page.fill('#g-name', 'Renamed crew');
  await page.click('[data-act="pick"]');
  await page.waitForTimeout(300);
  await page.click('.pick-row');           // toggle a member
  await page.click('[data-act="picker-done"]');
  await page.waitForTimeout(300);
  const name = await page.inputValue('#g-name');
  if (name !== 'Renamed crew') throw new Error('name lost across picker: ' + name);
  await page.click('.sheet [data-act="save"]');
  await page.waitForTimeout(300);
  if (!(await page.getByText('Renamed crew').first().isVisible())) throw new Error('rename not saved');
});

await step('09-people', async () => {
  await page.click('a[href="#/people"]');
  await page.waitForTimeout(300);
  await page.fill('#people-search', 'ravi');
  await page.waitForTimeout(300);
  const n = await page.locator('.person-card').count();
  if (n !== 1) throw new Error('search returned ' + n);
  const focused = await page.evaluate(() => document.activeElement?.id);
  if (focused !== 'people-search') throw new Error('search lost focus: ' + focused);
});

await step('10-add-person', async () => {
  await page.fill('#people-search', '');
  await page.waitForTimeout(200);
  await page.click('[data-act="add-person"]');
  await page.waitForTimeout(300);
  await page.fill('#p-name', 'Test Player');
  await page.fill('#p-phone', '555 987 6543');
  await page.click('.sheet [data-act="save"]');
  await page.waitForTimeout(300);
  if (!(await page.getByText('Test Player').isVisible())) throw new Error('person not added');
});

await step('11-new-event', async () => {
  await page.click('a[href="#/events"]');
  await page.waitForTimeout(200);
  await page.click('[data-act="new-event"]');
  await page.waitForTimeout(300);
  await page.click('[data-quick-day]:nth-child(3)');   // Saturday
  await page.waitForTimeout(200);
  await page.fill('#f-place', 'Riverside courts');
  await page.click('[data-act="pick-invitees"]');
  await page.waitForTimeout(300);
  await page.click('[data-group]');                     // whole group
  await page.click('[data-act="picker-done"]');
  await page.waitForTimeout(300);
  const place = await page.inputValue('#f-place');
  if (place !== 'Riverside courts') throw new Error('place lost across picker: ' + place);
  await page.click('[data-act="save-event"]');
  await page.waitForTimeout(400);
  const title = await page.textContent('#app-title');
  if (title !== 'Saturday') throw new Error('expected Saturday, got ' + title);
});

await step('12-reminder-flow', async () => {
  await page.click('.roster-section.pending .pill.yes');
  await page.waitForTimeout(200);
  await page.click('[data-act="remind"]');
  await page.waitForTimeout(300);
  const preview = await page.textContent('.preview-live');
  if (!/Don't forget/.test(preview)) throw new Error('bad reminder: ' + preview);
  console.log('   reminder:', preview.trim());
  await page.click('[data-sheet-close]');
  await page.waitForTimeout(300);
});

await step('13-persistence', async () => {
  await page.reload();
  await page.waitForTimeout(500);
  await page.click('a[href="#/events"]');
  await page.waitForTimeout(400);
  const n = await page.locator('.event-card').count();
  if (n < 2) throw new Error('events lost on reload: ' + n);
});

await step('14-events-list', async () => {
  await page.click('a[href="#/events"]');
  await page.waitForTimeout(300);
});

console.log('\n--- console/page errors ---');
console.log(errors.length ? errors.join('\n') : '(none)');

await browser.close();
