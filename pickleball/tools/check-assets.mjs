// Pre-deploy sanity check. Run from the repo root:  node pickleball/tools/check-assets.mjs
//
// The service worker precaches a hardcoded list of files. If that list drifts
// from what's actually on disk — a renamed module, a new view — the install
// step rejects and the app silently loses offline mode. Nothing in the browser
// tells you; it just stops working on a train. So check it here instead.

import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const appDir = join(dirname(fileURLToPath(import.meta.url)), '..');
const problems = [];
const note = (msg) => problems.push(msg);

/* --- the service worker's precache list must match the files on disk --- */

const sw = readFileSync(join(appDir, 'sw.js'), 'utf8');
const listed = [...sw.matchAll(/^\s*'(\.\/[^']*)',?\s*$/gm)]
  .map((m) => m[1])
  .filter((p) => p !== './');

if (!listed.length) note('sw.js: could not find the ASSETS list — did its formatting change?');

for (const asset of listed) {
  if (!existsSync(join(appDir, asset))) note(`sw.js precaches ${asset}, which does not exist`);
}

// Every shipped file should be precached, so the app works fully offline.
const SKIP_DIRS = new Set(['tools', 'node_modules', '.git']);
const SKIP_FILES = new Set(['README.md', '_headers', 'sw.js']);

const walk = (dir) => readdirSync(dir).flatMap((entry) => {
  const full = join(dir, entry);
  if (statSync(full).isDirectory()) return SKIP_DIRS.has(entry) ? [] : walk(full);
  return [`./${relative(appDir, full).split('\\').join('/')}`];
});

const onDisk = walk(appDir).filter((p) => !SKIP_FILES.has(p.slice(2)));
const listedSet = new Set(listed);
for (const file of onDisk) {
  if (!listedSet.has(file)) note(`${file} ships but is not in the sw.js ASSETS list (won't work offline)`);
}

/* --- the manifest has to parse, and its icons have to exist --- */

let manifest;
try {
  manifest = JSON.parse(readFileSync(join(appDir, 'manifest.webmanifest'), 'utf8'));
} catch (err) {
  note(`manifest.webmanifest does not parse: ${err.message}`);
}

if (manifest) {
  for (const key of ['name', 'start_url', 'icons']) {
    if (!manifest[key]) note(`manifest.webmanifest is missing "${key}"`);
  }
  for (const icon of manifest.icons ?? []) {
    if (!existsSync(join(appDir, icon.src))) note(`manifest icon ${icon.src} does not exist`);
  }
  if (!(manifest.icons ?? []).some((i) => i.purpose === 'maskable')) {
    note('manifest.webmanifest has no maskable icon — Android will letterbox the home-screen icon');
  }
}

/* --- index.html must reference files that exist --- */

const html = readFileSync(join(appDir, 'index.html'), 'utf8');
for (const [, ref] of html.matchAll(/(?:href|src)="(\.\/[^"]+)"/g)) {
  if (!existsSync(join(appDir, ref))) note(`index.html references ${ref}, which does not exist`);
}

/* --- report --- */

if (problems.length) {
  console.error(`✗ ${problems.length} problem(s):`);
  for (const p of problems) console.error(`  - ${p}`);
  process.exit(1);
}
console.log(`✓ ${listed.length} precached assets, manifest and index.html all check out`);
