// Builds dist/github-jet.svg: an animated "jet" colour-map heatmap of the
// last year of GitHub contributions. Run by .github/workflows/jet-heatmap.yml
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const USER = process.env.GH_USERNAME || "shahzad006";
const TOKEN = process.env.GH_TOKEN;
const OUT = process.env.OUTPUT_PATH || "dist/github-jet.svg";

async function fetchDays() {
  if (TOKEN) {
    try {
      const query = `query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount weekday}}}}}}`;
      const r = await fetch("https://api.github.com/graphql", {
        method: "POST",
        headers: { Authorization: `bearer ${TOKEN}`, "Content-Type": "application/json" },
        body: JSON.stringify({ query, variables: { login: USER } }),
      });
      const j = await r.json();
      const cal = j?.data?.user?.contributionsCollection?.contributionCalendar;
      if (cal) {
        return cal.weeks.flatMap((w, wi) =>
          w.contributionDays.map((d) => ({ date: d.date, count: d.contributionCount, week: wi, day: d.weekday })));
      }
      console.warn("GraphQL returned no calendar, falling back:", JSON.stringify(j).slice(0, 300));
    } catch (e) {
      console.warn("GraphQL failed, falling back:", e.message);
    }
  }
  // Fallback: public contributions page
  const html = await (await fetch(`https://github.com/users/${USER}/contributions`)).text();
  const days = [];
  const re = /data-date="(\d{4}-\d{2}-\d{2})"[^>]*id="contribution-day-component-(\d)-(\d+)"/g;
  const tips = {};
  for (const m of html.matchAll(/<tool-tip[^>]*for="contribution-day-component-(\d)-(\d+)"[^>]*>([^<]*)</g)) {
    const n = /^(\d+)/.exec(m[3].trim());
    tips[`${m[1]}-${m[2]}`] = n ? +n[1] : 0;
  }
  for (const m of html.matchAll(re)) {
    days.push({ date: m[1], day: +m[2], week: +m[3], count: tips[`${m[2]}-${m[3]}`] ?? 0 });
  }
  return days;
}

// Professional green scale (GitHub-style), t in [0,1]
function jet(t) {
  const stops = [[14, 68, 41], [0, 109, 50], [38, 166, 65], [57, 211, 83], [134, 239, 172]];
  const x = Math.max(0, Math.min(1, t)) * (stops.length - 1);
  const i = Math.min(stops.length - 2, Math.floor(x)), f = x - i;
  const h = (v) => Math.round(v).toString(16).padStart(2, "0");
  return "#" + [0, 1, 2].map((k) => h(stops[i][k] + (stops[i + 1][k] - stops[i][k]) * f)).join("");
}

function render(days) {
  const CELL = 15, GAP = 3, PADX = 40, PADY = 34;
  const weeks = Math.max(...days.map((d) => d.week)) + 1;
  const W = PADX * 2 + weeks * (CELL + GAP);
  const H = PADY + 7 * (CELL + GAP) + 44;
  const max = Math.max(1, ...days.map((d) => d.count));
  const total = days.reduce((s, d) => s + d.count, 0);
  const top = [...days].filter((d) => d.count > 0).sort((a, b) => b.count - a.count).slice(0, 6);

  const o = [];
  o.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">`);
  o.push(`<style>
.c{opacity:0;animation:in .5s ease forwards}
@keyframes in{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}
.ring{fill:none;stroke-width:2;animation:ring 2.4s ease-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes ring{0%{opacity:.9;transform:scale(.8)}100%{opacity:0;transform:scale(2.4)}}
.t{fill:#64748b;font-size:11px}
</style>`);
  o.push(`<text class="t" x="${PADX}" y="20">${total} contributions in the last year · @${USER}</text>`);
  ["Mon", "Wed", "Fri"].forEach((l, i) => o.push(`<text class="t" x="6" y="${PADY + (i * 2 + 1) * (CELL + GAP) + 11}">${l}</text>`));
  for (const d of days) {
    const x = PADX + d.week * (CELL + GAP), y = PADY + d.day * (CELL + GAP);
    const fill = d.count === 0 ? "#94a3b8" : jet(0.15 + 0.85 * Math.sqrt(d.count / max));
    const op = d.count === 0 ? 0.18 : 1;
    const delay = (d.week * 0.03 + d.day * 0.02).toFixed(2);
    o.push(`<rect class="c" style="animation-delay:${delay}s;transform-box:fill-box;transform-origin:center" x="${x}" y="${y}" width="${CELL}" height="${CELL}" rx="3" fill="${fill}" fill-opacity="${op}"><title>${d.date}: ${d.count}</title></rect>`);
  }
  top.forEach((d, i) => {
    const x = PADX + d.week * (CELL + GAP), y = PADY + d.day * (CELL + GAP);
    o.push(`<rect class="ring" style="animation-delay:${(i * 0.4).toFixed(1)}s" x="${x}" y="${y}" width="${CELL}" height="${CELL}" rx="4" stroke="#3fb950"/>`);
  });
  // legend
  const ly = H - 16;
  o.push(`<text class="t" x="${W - PADX - 190}" y="${ly + 10}">less</text>`);
  for (let i = 0; i < 10; i++) o.push(`<rect x="${W - PADX - 155 + i * 13}" y="${ly}" width="11" height="11" rx="2" fill="${jet(0.15 + 0.85 * (i / 9))}"/>`);
  o.push(`<text class="t" x="${W - PADX - 20}" y="${ly + 10}">more</text>`);
  o.push(`</svg>`);
  return o.join("\n");
}

const days = process.env.FAKE
  ? Array.from({ length: 371 }, (_, i) => ({ date: `d${i}`, week: Math.floor(i / 7), day: i % 7, count: Math.random() < 0.4 ? 0 : Math.floor(Math.random() ** 2 * 12) }))
  : await fetchDays();
if (!days.length) throw new Error("No contribution data found for " + USER);
mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, render(days));
console.log(`Wrote ${OUT} (${days.length} days)`);
