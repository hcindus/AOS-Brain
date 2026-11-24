// Frontline SOA — dashboard client
const $ = (s) => document.querySelector(s);

async function jget(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(url + " -> " + r.status);
  return r.json();
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function timeAgo(ts) {
  if (!ts) return "—";
  const d = new Date(ts);
  const diff = (Date.now() - d.getTime()) / 1000;
  if (diff < 60) return "just now";
  if (diff < 3600) return Math.floor(diff / 60) + "m ago";
  if (diff < 86400) return Math.floor(diff / 3600) + "h ago";
  return d.toLocaleDateString();
}

const INTENTS = ["sales", "support", "hr", "legal", "security", "logistics", "other"];
const QUALIFIED = ["lead", "support", "spam", "unknown"];

let activeFilter = null;

function renderKpis(stats) {
  $("#kpi-total").textContent = stats.total;
  $("#kpi-leads").textContent = (stats.by_qualified["lead"] || 0);
  $("#kpi-today").textContent = stats.today;
  $("#kpi-agents").textContent = Object.keys(stats.agents || {}).length;
}

function renderBars(stats) {
  const wrap = $("#intent-bars");
  const total = stats.total || 1;
  const by = stats.by_intent || {};
  wrap.innerHTML = INTENTS.filter((i) => by[i]).map((i) => {
    const pct = Math.round((by[i] / total) * 100);
    return `<div class="bar-row">
      <span class="bar-label">${esc(i)}</span>
      <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
      <span class="bar-count">${by[i]}</span>
    </div>`;
  }).join("") || `<div class="empty">No data yet</div>`;
}

function renderSuites(data) {
  const suites = data.suites || {};
  const routing = data.routing || {};
  const wrap = $("#suites");
  let html = "";
  for (const [name, agents] of Object.entries(suites)) {
    const price = { front_office: "$149", growth: "$349", full_office: "$749", security: "$99" }[name] || "";
    html += `<div class="suite">
      <div><div class="suite-name">${esc(name).replace(/_/g, " ")}</div>
      <div class="suite-agents">${agents.map(esc).join(" · ")}</div></div>
      <span class="suite-price">${price ? price + "/mo" : ""}</span>
    </div>`;
  }
  html += `<div style="margin-top:6px"><div class="meta" style="font-weight:700;color:var(--muted);text-transform:uppercase;font-size:10.5px;letter-spacing:.06em">Routing</div></div>`;
  for (const [intent, agents] of Object.entries(routing)) {
    html += `<div class="route-row"><span class="route-intent">${esc(intent)}</span> <span class="route-agents">→ ${agents.map(esc).join(", ")}</span></div>`;
  }
  wrap.innerHTML = html;
}

function renderFeed(items) {
  const body = $("#feed-body");
  const empty = $("#feed-empty");
  empty.style.display = items.length ? "none" : "block";
  body.innerHTML = items.map((r) => {
    const agents = (r.agents || []).map((a) => `<span>${esc(a)}</span>`).join("");
    return `<tr>
      <td class="time-cell">${timeAgo(r.ts)}</td>
      <td><span class="b-channel">${esc(r.channel)}</span></td>
      <td><span class="badge b-intent-${esc(r.intent)}">${esc(r.intent)}</span></td>
      <td><span class="badge b-q-${esc(r.qualified)}">${esc(r.qualified)}</span></td>
      <td><span class="b-agents">${agents || "—"}</span></td>
      <td class="summary-cell">${esc(r.summary)}</td>
    </tr>`;
  }).join("");
}

function renderFilters() {
  const wrap = $("#filters");
  wrap.innerHTML = `<span class="f-chip ${!activeFilter ? "active" : ""}" data-f="">All</span>` +
    INTENTS.map((i) => `<span class="f-chip ${activeFilter === i ? "active" : ""}" data-f="${i}">${i}</span>`).join("");
  wrap.querySelectorAll(".f-chip").forEach((c) => {
    c.onclick = () => { activeFilter = c.dataset.f || null; renderFilters(); load(); };
  });
}

function renderSim(result) {
  const el = $("#sim-result");
  el.classList.remove("hidden");
  const entity = result.entity || {};
  const ent = Object.entries(entity).filter(([, v]) => v).map(([k, v]) => `${esc(k)}=${esc(v)}`).join(", ");
  el.innerHTML = `
    <div class="r-title">Route resolved</div>
    <div class="r-grid">
      <span><span class="badge b-intent-${esc(result.intent)}">${esc(result.intent)}</span></span>
      <span><span class="badge b-q-${esc(result.qualified)}">${esc(result.qualified)}</span></span>
      <span><strong>urgency:</strong> ${esc(result.urgency)}</span>
      <span><strong>agents:</strong> ${esc((result.agents || []).join(", ") || "—")}</span>
      ${ent ? `<span><strong>entity:</strong> ${ent}</span>` : ""}
    </div>
    <div style="margin-top:8px;color:var(--muted)">${esc(result.summary)}</div>`;
}

async function load() {
  try {
    const [stats, suites, inbound] = await Promise.all([
      jget("api/stats"),
      jget("api/suites"),
      jget("api/inbound?limit=100"),
    ]);
    renderKpis(stats);
    renderBars(stats);
    renderSuites(suites);
    let items = inbound.items || [];
    if (activeFilter) items = items.filter((i) => i.intent === activeFilter);
    renderFeed(items);
  } catch (e) {
    console.error(e);
  }
}

async function initHealth() {
  try {
    const h = await jget("health");
    $("#status-pill").innerHTML = `<span class="dot"></span> Live`;
    $("#model-meta").textContent = "model " + h.model;
    $("#uptime-meta").textContent = "up " + Math.round(h.uptime_seconds / 60) + "m";
    $("#version").textContent = h.version;
  } catch (e) {
    $("#status-pill").innerHTML = `<span class="dot" style="background:#ef4444"></span> Offline`;
  }
}

$("#sim-go").onclick = async () => {
  const body = $("#sim-body").value.trim();
  if (!body) return;
  try {
    const r = await fetch("api/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ channel: $("#sim-channel").value, from_: "simulator", body }),
    });
    renderSim(await r.json());
  } catch (e) {
    $("#sim-result").innerHTML = `<div class="r-title">Error</div><div>${esc(e)}</div>`;
    $("#sim-result").classList.remove("hidden");
  }
};
$("#sim-body").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#sim-go").click(); });

renderFilters();
initHealth();
load();
setInterval(load, 15000);
