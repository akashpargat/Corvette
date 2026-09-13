/* Artura Hunt dashboard. Reads inlined JSON (single-file build) or ./data/*.json (GitHub Pages). */
(function () {
  "use strict";
  const $ = (s, el) => (el || document).querySelector(s);
  const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));
  const fmt$ = (n) => n == null ? "—" : "$" + Math.round(n).toLocaleString("en-US");
  const fmtK = (n) => n == null ? "—" : n >= 1000 ? (n / 1000).toFixed(n >= 10000 ? 0 : 1) + "K" : String(n);
  const fmtMi = (n) => n == null ? "— mi" : n.toLocaleString("en-US") + " mi";
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const yearVar = (y) => `var(--y${String(y || 2023).slice(2)})`;
  const SOURCE_SHORT = { craigslist: "Craigslist", iseecars: "iSeeCars", usedcars_com: "UsedCars.com", carsforsale: "Carsforsale", carsdirect: "CarsDirect", classiccars_com: "ClassicCars", jamesedition: "JamesEdition", exoticcartrader: "Exotic Car Trader", pcarmarket: "PCARMARKET", collectingcars: "Collecting Cars", mclarenlife: "McLaren Life", autotempest: "AutoTempest", autotrader_ca: "AutoTrader.ca", kijiji: "Kijiji", cargurus_ca: "CarGurus.ca",  mclaren_preowned: "McLaren CPO", dealer_sites: "Dealer site", cars_com: "Cars.com", autotrader: "Autotrader", kbb: "KBB", cargurus: "CarGurus", carfax: "CARFAX", truecar: "TrueCar", edmunds: "Edmunds", autolist: "Autolist", dupont: "duPont", classic_com: "Classic.com", bringatrailer: "BaT", carsandbids: "Cars & Bids", ebay: "eBay", hemmings: "Hemmings", fb_marketplace: "FB Marketplace", seed: "Seed" };

  const state = { years: new Set(), maxPrice: 400000, maxMiles: 40000, title: "notbranded", type: "all", st: "", src: "", q: "", sort: "price", removed: false, onlyWatch: false, view: "table", country: "" };
  let DATA = { summary: {}, changes: {}, listings: [] }, RUNS = [], MARKET = [];
  let watch = new Set();
  try { watch = new Set(JSON.parse(localStorage.getItem("artura.watch") || "[]")); } catch (e) { }
  try { const v = localStorage.getItem("artura.view"); if (v) state.view = v; } catch (e) { }
  const saveWatch = () => { try { localStorage.setItem("artura.watch", JSON.stringify([...watch])); } catch (e) { } };

  async function load() {
    const inline = (id) => { const el = document.getElementById(id); if (!el) return null; try { return JSON.parse(el.textContent); } catch (e) { return null; } };
    DATA = inline("data-listings") || await fetchJSON("data/listings.json") || DATA;
    RUNS = inline("data-runs") || await fetchJSON("data/runs.json") || [];
    MARKET = inline("data-market") || await fetchJSON("data/market.json") || [];
    if (!Array.isArray(DATA.listings)) DATA.listings = [];
  }
  async function fetchJSON(p) { try { const r = await fetch(p, { cache: "no-store" }); return r.ok ? await r.json() : null; } catch (e) { return null; } }

  /* ---------- derived ---------- */
  const active = () => DATA.listings.filter((l) => l.status === "active");
  const cleanPool = () => active().filter((l) => l.candidate && l.title_status !== "branded");
  const heroCar = () => { const p = cleanPool().sort((a, b) => a.price - b.price); return p[0] || null; };
  const daysOn = (l) => { const a = new Date(l.first_seen), b = new Date(l.last_seen || DATA.summary.date); return Math.max(0, Math.round((b - a) / 864e5)); };
  const isNew = (l) => l.first_seen === DATA.summary.date;
  const dropOf = (l) => (l.last_price_change && l.last_price_change.date === DATA.summary.date) ? l.last_price_change.delta : 0;

  function filtered() {
    const q = state.q.trim().toLowerCase();
    let rows = DATA.listings.filter((l) => {
      if (!state.removed && l.status !== "active") return false;
      if (!l.candidate && l.status === "active" && !state.removed && state.title !== "all") return false;
      if (state.years.size && !state.years.has(l.year)) return false;
      if (l.price != null && l.price > state.maxPrice) return false;
      if (l.mileage != null && state.maxMiles < 40000 && l.mileage > state.maxMiles) return false;
      if (state.title === "clean" && l.title_status !== "clean") return false;
      if (state.title === "notbranded" && l.title_status === "branded") return false;
      if (state.type !== "all" && l.listing_type !== state.type) return false;
      if (state.st && l.state !== state.st) return false;
      if (state.country && (l.country || "US") !== state.country) return false;
      if (state.src && !(l.sources || [l.source]).includes(state.src)) return false;
      if (state.onlyWatch && !watch.has(l.key)) return false;
      if (q) { const hay = [l.title, l.vin, l.dealer, l.location, l.color, l.trim, (l.sources || []).join(" ")].join(" ").toLowerCase(); if (!hay.includes(q)) return false; }
      return true;
    });
    const s = state.sort, inf = 1e12;
    const cmp = {
      price: (a, b) => (a.price ?? inf) - (b.price ?? inf),
      deal: (a, b) => (b.deal_pct ?? -inf) - (a.deal_pct ?? -inf),
      mileage: (a, b) => (a.mileage ?? inf) - (b.mileage ?? inf),
      newest: (a, b) => (b.first_seen || "").localeCompare(a.first_seen || "") || (a.price ?? inf) - (b.price ?? inf),
      drop: (a, b) => dropOf(a) - dropOf(b),
      year: (a, b) => (b.year || 0) - (a.year || 0) || (a.price ?? inf) - (b.price ?? inf),
    }[s];
    rows.sort((a, b) => (a.status !== "active") - (b.status !== "active") || cmp(a, b));
    return rows;
  }

  /* ---------- render: masthead + hero + KPIs ---------- */
  function renderTop() {
    const S = DATA.summary || {};
    const lastRun = RUNS[RUNS.length - 1];
    $("#lastScan").textContent = S.generated_at ? new Date(S.generated_at).toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) : "never";
    if (lastRun) { const ok = lastRun.sources.filter((s) => s.status === "ok").length; $("#sourcesUp").textContent = `${ok} / ${lastRun.sources.length}`; }
    const h = heroCar();
    $("#heroEmpty").hidden = !!h; $("#heroBody").hidden = !h;
    if (h) {
      $("#heroPrice").textContent = fmt$(h.price);
      const d = dropOf(h), delta = $("#heroDelta");
      delta.textContent = d ? `${d < 0 ? "▼" : "▲"} ${fmt$(Math.abs(d))} today` : (h.deal_pct != null ? `${Math.abs(h.deal_pct).toFixed(0)}% ${h.deal_pct >= 0 ? "under" : "over"} market model` : "");
      delta.style.color = d < 0 || (h.deal_pct || 0) > 0 ? "var(--good)" : "var(--ink-2)";
      $("#heroTitle").textContent = h.title || `${h.year} McLaren Artura ${h.trim || ""}`;
      $("#heroFacts").innerHTML = [
        `<span><b>${fmtMi(h.mileage)}</b></span>`, h.color ? `<span>${esc(h.color)}</span>` : "",
        `<span>${esc(h.dealer || (h.listing_type === "private" ? "Private seller" : "Seller n/a"))}</span>`,
        h.location ? `<span>${esc(h.location)}</span>` : "", `<span>Title: <b>${titleWord(h)}</b></span>`,
        h.vin ? `<span class="mono">VIN ${esc(h.vin)}</span>` : "", `<span>Listed ${daysOn(h)}d</span>`,
      ].filter(Boolean).join("");
      $("#heroLink").href = h.url;
      $("#heroSources").textContent = "Seen on " + (h.sources || [h.source]).map((s) => SOURCE_SHORT[s] || s).join(", ");
      const w = $("#heroWatch"); w.textContent = watch.has(h.key) ? "★ Watching" : "☆ Watch"; w.onclick = () => { toggleWatch(h.key); renderAll(); };
      sparkline($("#heroSpark"), h.price_history || [], 320, 64, true);
    }
    const pool = cleanPool(), prices = pool.map((l) => l.price).sort((a, b) => a - b);
    const med = prices.length ? prices[Math.floor(prices.length / 2)] : null;
    const low5 = prices.slice(0, 5); const avg5 = low5.length ? low5.reduce((a, b) => a + b, 0) / low5.length : null;
    const fb = active().filter((l) => (l.sources || []).includes("fb_marketplace")).length;
    const tiles = [
      ["Active listings", active().length, `${pool.length} clean-title candidates`],
      ["New today", S.new_today ?? 0, S.removed_today ? `${S.removed_today} sold or removed` : "since yesterday's scan", S.new_today ? "good" : ""],
      ["Price drops today", S.price_drops_today ?? 0, "cars cheaper than yesterday", S.price_drops_today ? "good" : ""],
      ["Median asking", fmt$(med), "clean-title candidates"],
      ["Lowest five avg", fmt$(avg5), "the bottom of the market"],
      ["Facebook finds", fb, fbNote()],
    ];
    $("#kpis").innerHTML = tiles.map(([l, v, d, c]) => `<div class="kpi"><span class="label">${l}</span><span class="value">${v}</span><span class="delta ${c || ""}">${esc(d)}</span></div>`).join("");
  }
  function fbNote() { const r = (RUNS[RUNS.length - 1] || { sources: [] }).sources.find((s) => s.source === "fb_marketplace"); if (!r) return "not scanned yet"; if (r.extra && r.extra.login_walled_hubs && !r.count) return "login wall — add FB cookies"; return `${r.extra ? r.extra.hubs : "?"} metro hubs scanned`; }
  const titleWord = (l) => l.title_status === "clean" ? "verified clean" : l.title_status === "branded" ? "BRANDED" : "unverified";

  /* ---------- render: table + cards ---------- */
  function renderResults() {
    const rows = filtered();
    $("#resultsCount").textContent = `${rows.length} of ${DATA.listings.length}`;
    $("#tableView").hidden = state.view !== "table"; $("#cardsView").hidden = state.view !== "cards";
    const hero = heroCar();
    if (state.view === "table") {
      $("#gridBody").innerHTML = rows.map((l, i) => {
        const d = dropOf(l);
        return `<tr class="${l.status !== "active" ? "removed" : ""} ${hero && l.key === hero.key ? "top" : ""}" data-key="${esc(l.key)}">
          <td class="num">${l.rank_cheapest_clean || ""}</td>
          <td><div class="car"><span class="t">${esc(l.year || "")} Artura ${esc(l.trim || "")} ${isNew(l) ? '<span class="badge new">NEW</span>' : ""} ${l.listing_type === "auction" ? '<span class="badge auction">auction</span>' : ""}</span><span class="s">${esc(l.color || "")}${l.color && l.vin ? " · " : ""}${esc(l.vin || "")}</span></div></td>
          <td class="num"><span class="price">${fmt$(l.price)}</span>${l.price_local ? `<br><span class="s" style="color:var(--muted)">CA$${l.price_local.toLocaleString("en-US")}</span>` : (l.price_high && l.price_high !== l.price ? `<br><span class="s" style="color:var(--muted)">to ${fmt$(l.price_high)}</span>` : "")}</td>
          <td class="num">${d ? `<span class="badge ${d < 0 ? "drop" : "up"}">${d < 0 ? "▼" : "▲"}${fmtK(Math.abs(d))}</span>` : (l.deal_pct != null && l.deal_pct >= 8 ? `<span class="badge deal">${l.deal_pct.toFixed(0)}% under</span>` : "")}</td>
          <td class="num">${l.mileage != null ? l.mileage.toLocaleString("en-US") : "—"}</td>
          <td><span class="badge ${l.title_status}">${titleWord(l)}</span></td>
          <td>${esc(l.dealer || (l.listing_type === "private" ? "Private" : "—"))}</td>
          <td>${(l.country === "CA") ? "🇨🇦 " : ""}${esc(l.location || l.state || "—")}</td>
          <td><div class="srcs">${(l.sources || [l.source]).map((s) => `<span class="src">${esc(SOURCE_SHORT[s] || s)}</span>`).join("")}</div></td>
          <td class="num">${daysOn(l)}</td>
          <td><svg class="spark" viewBox="0 0 96 28" preserveAspectRatio="none">${sparkPath(l.price_history || [], 96, 28)}</svg></td>
          <td><button class="star ${watch.has(l.key) ? "on" : ""}" data-watch="${esc(l.key)}" title="Watch" aria-label="Watch">${watch.has(l.key) ? "★" : "☆"}</button> <a class="rowlink" href="${esc(l.url)}" target="_blank" rel="noopener">Open ↗</a></td>
        </tr>`;
      }).join("") || `<tr><td colspan="12" style="color:var(--muted);padding:24px">Nothing matches these filters.</td></tr>`;
    } else {
      $("#cardsView").innerHTML = rows.map((l) => {
        const d = dropOf(l);
        return `<article class="card">
          ${l.image ? `<img class="img" src="${esc(l.image)}" alt="" loading="lazy" referrerpolicy="no-referrer">` : `<div class="img"></div>`}
          <div class="body">
            <div class="row"><span class="big">${fmt$(l.price)}</span>${d ? `<span class="badge ${d < 0 ? "drop" : "up"}">${d < 0 ? "▼" : "▲"}${fmt$(Math.abs(d))}</span>` : isNew(l) ? '<span class="badge new">NEW</span>' : ""}</div>
            <div><strong>${esc(l.year || "")} McLaren Artura ${esc(l.trim || "")}</strong></div>
            <div class="meta">${fmtMi(l.mileage)}${l.color ? " · " + esc(l.color) : ""}${l.location ? " · " + esc(l.location) : ""}</div>
            <div class="meta">${esc(l.dealer || (l.listing_type === "private" ? "Private seller" : ""))}</div>
            <div class="srcs"><span class="badge ${l.title_status}">${titleWord(l)}</span>${(l.sources || [l.source]).map((s) => `<span class="src">${esc(SOURCE_SHORT[s] || s)}</span>`).join("")}</div>
            <div class="foot"><svg class="spark" viewBox="0 0 96 28" preserveAspectRatio="none">${sparkPath(l.price_history || [], 96, 28)}</svg><span><button class="star ${watch.has(l.key) ? "on" : ""}" data-watch="${esc(l.key)}" aria-label="Watch">${watch.has(l.key) ? "★" : "☆"}</button> <a class="rowlink" href="${esc(l.url)}" target="_blank" rel="noopener">Open ↗</a></span></div>
          </div></article>`;
      }).join("") || `<p style="color:var(--muted)">Nothing matches these filters.</p>`;
    }
    $$("[data-watch]").forEach((b) => b.addEventListener("click", () => { toggleWatch(b.dataset.watch); renderAll(); }));
  }
  function toggleWatch(k) { watch.has(k) ? watch.delete(k) : watch.add(k); saveWatch(); }

  /* ---------- sparklines ---------- */
  function sparkPath(h, w, ht) {
    const pts = (h || []).filter((p) => p && p.p);
    if (pts.length < 2) { return pts.length === 1 ? `<circle cx="${w - 4}" cy="${ht / 2}" r="3" fill="var(--muted)"/>` : ""; }
    const lo = Math.min(...pts.map((p) => p.p)), hi = Math.max(...pts.map((p) => p.p)), span = hi - lo || 1;
    const xs = pts.map((_, i) => 3 + i * (w - 6) / (pts.length - 1)), ys = pts.map((p) => ht - 4 - (p.p - lo) / span * (ht - 8));
    const d = xs.map((x, i) => `${i ? "L" : "M"}${x.toFixed(1)},${ys[i].toFixed(1)}`).join(" ");
    const dir = pts[pts.length - 1].p < pts[0].p ? "var(--good)" : pts[pts.length - 1].p > pts[0].p ? "var(--bad)" : "var(--muted)";
    return `<path d="${d}" fill="none" stroke="${dir}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/><circle cx="${xs[xs.length - 1]}" cy="${ys[ys.length - 1]}" r="3" fill="${dir}"/>`;
  }
  function sparkline(svg, h, w, ht, area) {
    const pts = (h || []).filter((p) => p && p.p);
    if (pts.length < 2) { svg.innerHTML = ""; return; }
    const lo = Math.min(...pts.map((p) => p.p)), hi = Math.max(...pts.map((p) => p.p)), span = hi - lo || 1;
    const xs = pts.map((_, i) => i * w / (pts.length - 1)), ys = pts.map((p) => ht - 6 - (p.p - lo) / span * (ht - 14));
    const line = xs.map((x, i) => `${i ? "L" : "M"}${x.toFixed(1)},${ys[i].toFixed(1)}`).join(" ");
    svg.innerHTML = (area ? `<path d="${line} L${w},${ht} L0,${ht} Z" fill="var(--accent)" opacity=".12"/>` : "") + `<path d="${line}" fill="none" stroke="var(--accent)" stroke-width="2"/>`;
  }

  /* ---------- charts ---------- */
  function renderScatter() {
    const svg = $("#scatter"), W = 640, H = 340, m = { t: 14, r: 18, b: 42, l: 62 };
    const pool = cleanPool().filter((l) => l.mileage != null);
    const years = [...new Set(pool.map((l) => l.year || 2023))].sort();
    $("#scatterLegend").innerHTML = years.map((y) => `<span><i style="background:${yearVar(y)}"></i>${y}</span>`).join("") + (heroCar() ? `<span><i style="background:transparent;box-shadow:inset 0 0 0 3px var(--accent)"></i>cheapest clean</span>` : "");
    if (!pool.length) { svg.innerHTML = `<text x="${W / 2}" y="${H / 2}" text-anchor="middle" fill="var(--muted)" font-size="13">No clean-title candidates with mileage yet.</text>`; return; }
    const xmax = niceMax(Math.max(...pool.map((l) => l.mileage)) || 1000, 5), ymin = niceMin(Math.min(...pool.map((l) => l.price)), 10000), ymax = niceMax(Math.max(...pool.map((l) => l.price)), 10000);
    const X = (v) => m.l + v / xmax * (W - m.l - m.r), Y = (v) => H - m.b - (v - ymin) / (ymax - ymin || 1) * (H - m.t - m.b);
    let out = "";
    const yt = ticks(ymin, ymax, 5), xt = ticks(0, xmax, 5);
    yt.forEach((v) => { out += `<line class="gridline" x1="${m.l}" x2="${W - m.r}" y1="${Y(v)}" y2="${Y(v)}"/><text class="axis-t" x="${m.l - 8}" y="${Y(v) + 3}" text-anchor="end" fill="var(--muted)" font-size="10" font-family="var(--mono)">$${(v / 1000).toFixed(0)}K</text>`; });
    xt.forEach((v) => { out += `<text x="${X(v)}" y="${H - m.b + 16}" text-anchor="middle" fill="var(--muted)" font-size="10" font-family="var(--mono)">${v >= 1000 ? (v / 1000).toFixed(0) + "K" : v}</text>`; });
    out += `<text x="${(m.l + W - m.r) / 2}" y="${H - 6}" text-anchor="middle" fill="var(--muted)" font-size="11">miles</text>`;
    const model = (DATA.summary.market_model || {});
    if (model.intercept != null) { const y0 = model.intercept, y1 = model.intercept + model.per_mile * xmax; out += `<line x1="${X(0)}" y1="${Y(Math.min(Math.max(y0, ymin), ymax))}" x2="${X(xmax)}" y2="${Y(Math.min(Math.max(y1, ymin), ymax))}" stroke="var(--line-2)" stroke-width="1.5" stroke-dasharray="4 4"/>`; }
    const hero = heroCar();
    pool.forEach((l, i) => { out += `<circle class="dot ${hero && l.key === hero.key ? "hero-dot" : ""}" data-i="${i}" cx="${X(l.mileage)}" cy="${Y(l.price)}" r="5.5" fill="${yearVar(l.year)}"/>`; });
    svg.innerHTML = out;
    $$(".dot", svg).forEach((c) => { const l = pool[+c.dataset.i]; c.addEventListener("mousemove", (e) => tip(e, `<b>${fmt$(l.price)} · ${l.year} Artura ${l.trim || ""}</b>${fmtMi(l.mileage)}${l.location ? " · " + esc(l.location) : ""}<br>${esc(l.dealer || "")}<br>${(l.sources || []).map((s) => SOURCE_SHORT[s] || s).join(", ")}`)); c.addEventListener("mouseleave", hideTip); c.addEventListener("click", () => window.open(l.url, "_blank", "noopener")); });
  }
  function renderMarket() {
    const svg = $("#market"), W = 640, H = 340, m = { t: 14, r: 18, b: 42, l: 62 };
    const pts = MARKET.filter((p) => p.cheapest);
    $("#marketLegend").innerHTML = `<span><i class="line" style="background:var(--accent)"></i>cheapest clean</span><span><i class="line" style="background:var(--ink-2)"></i>median</span>`;
    if (pts.length < 2) { svg.innerHTML = `<text x="${W / 2}" y="${H / 2}" text-anchor="middle" fill="var(--muted)" font-size="13">${pts.length ? "One day of data so far; the line starts tomorrow." : "No daily data yet."}</text>` + (pts.length ? `<text x="${W / 2}" y="${H / 2 + 22}" text-anchor="middle" fill="var(--ink)" font-size="13" font-family="var(--mono)">${pts[0].d}: cheapest ${fmt$(pts[0].cheapest)} · median ${fmt$(pts[0].median)}</text>` : ""); return; }
    const all = pts.flatMap((p) => [p.cheapest, p.median].filter(Boolean));
    const ymin = niceMin(Math.min(...all), 10000), ymax = niceMax(Math.max(...all), 10000);
    const X = (i) => m.l + i / (pts.length - 1) * (W - m.l - m.r), Y = (v) => H - m.b - (v - ymin) / (ymax - ymin || 1) * (H - m.t - m.b);
    let out = "";
    ticks(ymin, ymax, 5).forEach((v) => { out += `<line class="gridline" x1="${m.l}" x2="${W - m.r}" y1="${Y(v)}" y2="${Y(v)}"/><text x="${m.l - 8}" y="${Y(v) + 3}" text-anchor="end" fill="var(--muted)" font-size="10" font-family="var(--mono)">$${(v / 1000).toFixed(0)}K</text>`; });
    const step = Math.max(1, Math.ceil(pts.length / 6));
    pts.forEach((p, i) => { if (i % step === 0 || i === pts.length - 1) out += `<text x="${X(i)}" y="${H - m.b + 16}" text-anchor="middle" fill="var(--muted)" font-size="10" font-family="var(--mono)">${p.d.slice(5)}</text>`; });
    const path = (key) => pts.map((p, i) => p[key] ? `${i && pts[i - 1][key] ? "L" : "M"}${X(i).toFixed(1)},${Y(p[key]).toFixed(1)}` : "").join(" ");
    out += `<path d="${path("cheapest")} L${X(pts.length - 1)},${H - m.b} L${X(0)},${H - m.b} Z" fill="var(--accent)" opacity=".1"/>`;
    out += `<path d="${path("median")}" fill="none" stroke="var(--ink-2)" stroke-width="2" stroke-linejoin="round"/>`;
    out += `<path d="${path("cheapest")}" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round"/>`;
    const last = pts[pts.length - 1];
    out += `<circle cx="${X(pts.length - 1)}" cy="${Y(last.cheapest)}" r="4.5" fill="var(--accent)" stroke="var(--surface)" stroke-width="2"/><text x="${X(pts.length - 1) - 6}" y="${Y(last.cheapest) - 8}" text-anchor="end" fill="var(--ink)" font-size="11" font-family="var(--mono)">${fmt$(last.cheapest)}</text>`;
    pts.forEach((p, i) => { out += `<rect x="${X(i) - (W - m.l - m.r) / pts.length / 2}" y="${m.t}" width="${(W - m.l - m.r) / pts.length}" height="${H - m.t - m.b}" fill="transparent" data-i="${i}" class="hit"/>`; });
    svg.innerHTML = out;
    $$(".hit", svg).forEach((r) => { const p = pts[+r.dataset.i]; r.addEventListener("mousemove", (e) => tip(e, `<b>${p.d}</b>cheapest ${fmt$(p.cheapest)}<br>median ${fmt$(p.median)}<br>${p.clean} clean of ${p.active} active`)); r.addEventListener("mouseleave", hideTip); });
  }
  const niceMax = (v, s) => Math.ceil(v / s) * s || s;
  const niceMin = (v, s) => Math.floor(v / s) * s;
  function ticks(a, b, n) { const step = niceStep((b - a) / n); const out = []; for (let v = Math.ceil(a / step) * step; v <= b + 1e-9; v += step) out.push(v); return out; }
  function niceStep(raw) { const p = Math.pow(10, Math.floor(Math.log10(raw || 1))); const r = raw / p; return (r <= 1 ? 1 : r <= 2 ? 2 : r <= 5 ? 5 : 10) * p; }
  function tip(e, html) { const t = $("#tip"); t.innerHTML = html; t.hidden = false; const x = Math.min(e.clientX + 14, window.innerWidth - 280), y = Math.min(e.clientY + 14, window.innerHeight - 90); t.style.left = x + "px"; t.style.top = y + "px"; }
  function hideTip() { $("#tip").hidden = true; }

  /* ---------- changes + sources ---------- */
  function renderChanges() {
    const C = DATA.changes || {}, by = Object.fromEntries(DATA.listings.map((l) => [l.key, l]));
    const item = (k, label, cls) => { const l = by[k]; if (!l) return ""; const d = l.last_price_change; return `<li><span class="badge ${cls}">${label}</span><span>${fmt$(l.price)} · ${esc(l.year || "")} Artura ${esc(l.trim || "")}${l.mileage != null ? " · " + fmtMi(l.mileage) : ""}${l.location ? " · " + esc(l.location) : ""}${cls === "drop" || cls === "up" ? ` <span style="color:var(--muted)">(was ${fmt$(d.from)})</span>` : ""}</span><a class="rowlink" href="${esc(l.url)}" target="_blank" rel="noopener">Open ↗</a></li>`; };
    const html = [...(C.price_drop || []).map((k) => item(k, "▼ drop", "drop")), ...(C.new || []).map((k) => item(k, "new", "new")), ...(C.price_up || []).map((k) => item(k, "▲ up", "up")), ...(C.removed || []).map((k) => item(k, "gone", "removed")), ...(C.returned || []).map((k) => item(k, "back", "unknown"))].join("");
    $("#changes").innerHTML = html || `<li class="empty">Nothing changed in the last scan.</li>`;
  }
  function renderSources() {
    const run = RUNS[RUNS.length - 1];
    if (!run) { $("#sources").innerHTML = `<p style="color:var(--muted)">No run recorded yet.</p>`; return; }
    $("#sources").innerHTML = run.sources.map((s) => { const note = s.error || (s.status !== "ok" ? (s.notes || []).slice(-1)[0] : "") || ""; return `<div class="srow"><span class="dotst ${s.status}"></span><span>${esc(s.label)}</span><span class="n">${s.count} cars · ${s.seconds}s</span><span class="st">${s.status}</span>${note ? `<span class="note">${esc(note).slice(0, 160)}</span>` : ""}</div>`; }).join("");
    $("#footMeta").textContent = `Last run ${run.started_at ? new Date(run.started_at).toLocaleString() : ""} took ${run.seconds}s across ${run.sources.length} sources and ${run.raw_listings} raw listings. ${RUNS.length} runs on record.`;
  }

  /* ---------- filters ---------- */
  function buildFilters() {
    const years = [2020, 2021, 2022, 2023, 2024, 2025, 2026], have = new Set(DATA.listings.map((l) => l.year));
    $("#yearChips").innerHTML = years.map((y) => `<button type="button" class="chip ${state.years.has(y) ? "on" : ""}" data-year="${y}" ${have.has(y) ? "" : 'style="opacity:.45"'}>${y}</button>`).join("");
    $$("#yearChips .chip").forEach((b) => b.addEventListener("click", () => { const y = +b.dataset.year; state.years.has(y) ? state.years.delete(y) : state.years.add(y); b.classList.toggle("on"); renderAll(); }));
    const states = [...new Set(DATA.listings.map((l) => l.state).filter(Boolean))].sort();
    $("#stateFilter").innerHTML = `<option value="">Any</option>` + states.map((s) => `<option>${s}</option>`).join("");
    const srcs = [...new Set(DATA.listings.flatMap((l) => l.sources || [l.source]))].sort();
    $("#sourceFilter").innerHTML = `<option value="">Any</option>` + srcs.map((s) => `<option value="${s}">${SOURCE_SHORT[s] || s}</option>`).join("");
    const bind = (id, key, fn) => $(id).addEventListener("input", (e) => { state[key] = fn ? fn(e.target) : e.target.value; renderAll(); });
    bind("#maxPrice", "maxPrice", (t) => +t.value); bind("#maxMiles", "maxMiles", (t) => +t.value);
    bind("#titleFilter", "title"); bind("#typeFilter", "type"); bind("#countryFilter", "country"); bind("#stateFilter", "st"); bind("#sourceFilter", "src"); bind("#q", "q"); bind("#sort", "sort");
    bind("#showRemoved", "removed", (t) => t.checked); bind("#onlyWatch", "onlyWatch", (t) => t.checked);
    $$(".viewtoggle button").forEach((b) => b.addEventListener("click", () => { state.view = b.dataset.view; try { localStorage.setItem("artura.view", state.view); } catch (e) { } $$(".viewtoggle button").forEach((x) => x.classList.toggle("on", x === b)); renderResults(); }));
    $$(".viewtoggle button").forEach((x) => x.classList.toggle("on", x.dataset.view === state.view));
  }
  function renderAll() {
    $("#maxPriceOut").textContent = state.maxPrice >= 400000 ? "any" : fmt$(state.maxPrice);
    $("#maxMilesOut").textContent = state.maxMiles >= 40000 ? "any" : fmtK(state.maxMiles) + " mi";
    renderTop(); renderResults(); renderScatter(); renderMarket(); renderChanges(); renderSources();
  }
  load().then(() => { buildFilters(); renderAll(); });
})();
