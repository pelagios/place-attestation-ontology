#!/usr/bin/env node
// The README's three badges (DOI, status, version), as static SVG files in badges/, made from
// CITATION.cff: its `version`, and the concept DOI under `identifiers`. No badge service is used,
// since a service-rendered badge can break; these are files in the repository. Run at each release,
// after CITATION.cff is updated (see the Releases section of CLAUDE.md):
//
//   node scripts/badges.mjs           write badges/*.svg
//   node scripts/badges.mjs --check   exit 1, naming each badge, if a committed one is out of date
//
// No dependencies. Text widths come from DejaVu Sans's advance widths at 11px (close to Verdana's),
// and each text is also given that width as its textLength, so that it fits its box in any font.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const STATUS = 'experimental';

// Advance widths of printable ASCII (space to ~), in tenths of a pixel at 11px; other characters
// are taken as 7px.
const W = [35, 44, 51, 92, 70, 105, 86, 30, 43, 43, 55, 92, 35, 40, 35, 37, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 37, 37,
  92, 92, 92, 58, 110, 75, 75, 77, 85, 70, 63, 85, 83, 32, 32, 72, 61, 95, 82, 87, 66, 87, 76, 70, 67, 81, 75, 109, 75, 67,
  75, 43, 37, 43, 92, 55, 55, 67, 70, 60, 70, 68, 39, 70, 70, 31, 31, 64, 31, 107, 70, 67, 70, 70, 45, 57, 43, 70, 65, 90,
  65, 65, 58, 70, 37, 70, 92];
export const textWidth = (s) => Math.ceil([...s].reduce((n, c) => n + (W[c.codePointAt(0) - 32] ?? 70), 0) / 10);

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const PAD = 6, LABEL = '#555', DARK = '#101a3a';

// One flat badge: a grey label and a coloured value, white text with a faint shadow, or dark text
// (no shadow) on a light colour.
export function badge(label, value, colour, { dark = false } = {}) {
  const lt = textWidth(label), vt = textWidth(value), lw = lt + 2 * PAD, vw = vt + 2 * PAD, w = lw + vw;
  const text = (s, x, len, fill, shadow) => (shadow ? `<text x="${x}" y="15" fill="#010101" fill-opacity=".3" textLength="${len}" lengthAdjust="spacing">${esc(s)}</text>` : '')
    + `<text x="${x}" y="14" fill="${fill}" textLength="${len}" lengthAdjust="spacing">${esc(s)}</text>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="20" role="img" aria-label="${esc(label)}: ${esc(value)}">`
    + `<title>${esc(label)}: ${esc(value)}</title>`
    + '<linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient>'
    + `<clipPath id="r"><rect width="${w}" height="20" rx="3" fill="#fff"/></clipPath>`
    + `<g clip-path="url(#r)"><rect width="${lw}" height="20" fill="${LABEL}"/><rect x="${lw}" width="${vw}" height="20" fill="${colour}"/><rect width="${w}" height="20" fill="url(#s)"/></g>`
    + '<g text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">'
    + text(label, lw / 2, lt, '#fff', true) + text(value, lw + vw / 2, vt, dark ? DARK : '#fff', !dark)
    + '</g></svg>\n';
}

// The version, and the concept DOI (the first `type: doi` under `identifiers`), from CITATION.cff.
export function citation(cff) {
  const version = cff.match(/^version:[ \t]*["']?([^"'\s]+)/m)?.[1];
  const ids = cff.match(/^identifiers:[ \t]*\n((?:[ \t].*\n?)*)/m)?.[1] ?? '';
  const doi = ids.match(/type:[ \t]*doi[ \t]*\n[ \t]*value:[ \t]*["']?([^"'\s]+)/)?.[1];
  if (!version) throw new Error('CITATION.cff has no version');
  if (!doi) throw new Error('CITATION.cff has no DOI under identifiers');
  return { version, doi };
}

export function badges(cff) {
  const { version, doi } = citation(cff);
  return {
    'doi.svg': badge('DOI', doi, '#1f45b8'),
    'status.svg': badge('status', STATUS, '#f0b429', { dark: true }),
    'version.svg': badge('version', version, '#1f45b8'),
  };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const root = fileURLToPath(new URL('..', import.meta.url)), dir = join(root, 'badges');
  const made = badges(readFileSync(join(root, 'CITATION.cff'), 'utf8'));
  if (process.argv.includes('--check')) {
    const stale = Object.entries(made).filter(([f, svg]) => { try { return readFileSync(join(dir, f), 'utf8') !== svg; } catch { return true; } }).map(([f]) => f);
    if (stale.length) { console.error(`badges out of date (run node scripts/badges.mjs): ${stale.join(', ')}`); process.exit(1); }
    console.log('badges up to date');
  } else {
    mkdirSync(dir, { recursive: true });
    for (const [f, svg] of Object.entries(made)) writeFileSync(join(dir, f), svg);
    console.log(`wrote ${Object.keys(made).map((f) => 'badges/' + f).join(', ')}`);
  }
}
