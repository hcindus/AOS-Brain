# PSD Stack Map — Inventory for Customer-VPS Scaffolding

**Purpose:** capture everything that runs so we can stamp out an identical customer VPS ("click → done").

---

## 1. Core Brain (AOS)
- **Complete Brain v4.5** — socket `/tmp/aos_brain.sock`; 14+ components: SuperiorHeart (ternary), Stomach v2, Intestine v2, Brain v3.1 (7-region OODA), 3D Cortex (32×32×32), TracRay, consciousness layers, QMD loop, MemoryBridge (nomic-embed), Voice Manager (Mort_II TTS), Vision (stub), Thyroid v1.2, Lungs v1.0, Liver v1.0, Kidneys v1.0, Persistence v1.0.
- **BHSI v4** — heart/stomach/intestines, socket `/tmp/bhsi_v4.sock`.
- **Mission Control v2.0** — port 8080.
- **Model Router** — tinyllama (decision), Mort_II (voice), nomic-embed (embeddings).
- Files: `/root/.aos/aos/` (runtime, 332 commits behind origin/main).

## 2. Agents (fleet)
- **AOCROS agents** (systemd + heartbeat): Patricia, Forge, Jordan, Aurora, Chelios (5 active, 1-min heartbeats) + more in `agent_sandboxes/`.
- **Hermes agent (Beets)** — gateway + WhatsApp bridge (enrichment).
- **Sales team**: Miles, Hume, CLOSETER, Judy, Jane, Pulp, Clippy-42, GREET.
- Manifests/roles in `aocros/agent_profiles/`, `AGI_COMPANY/agents/`, `AGI_COMPANY/subsidiaries/`.

## 3. Systemd services (27 running, ours)
| Service | What |
|---|---|
| aos-brain-v4 | complete brain |
| aos-bhsi-v4 | heart/stomach/intestines |
| aos-mission-control | MC dashboard (8080) |
| aos-vision(-daemon) | vision (stub) |
| brain-health-monitor | brain health |
| collections-api / -worker | Go collections (8085) |
| darkfactory-worker | Temporal Dark Factory |
| depotchaos(-tasks) | CRM (8082) |
| enrichment-agent | lead enrichment |
| legal-worker / media-worker | Temporal legal/media |
| outreach-worker | Temporal outreach |
| psd-sales-automation | Dan Martell pipeline (8085) |
| psdepot-contact / -creditcard(5002) / -payment / -order-api(8088) | order/payment/contact |
| scraper-mechanic | scrapers |
| testimonials-api | testimonials |
| nognog-bridge / roblox-bridge | game bridges |
| monarx-agent | monitoring |

## 4. Docker (7 containers)
- **temporal** (7233), temporal-ui (8233), temporal-postgresql (postgres:13)
- **overpass** (OSM query, 12345)
- **buzz-postgres** (postgres:17), **buzz-redis** (redis:7), **n8n** (automation)

## 5. Crons (~20 jobs)
- Outreach: reorder_reminder (15:00), closeter_inbox_monitor (5m), closeter_reply_handler (5m+30s), submit_leads (16:00), temporal_status (5m)
- Ops: heartbeat_monitor (5m), agent_daily_scheduler (6:00), sync_depotchaos_live (6:30)
- Patricia: patricia_v2 (5m), patricia_task_automation (8:00/18:00), outreach_backlog (9:00)
- Media: trend_radar (7:00), blog (Tue 9:00)
- Data: depotchaos_intake (15m), daily_opportunity_alert (7:00), refresh_stale_leads (Sun 2:00), process_overnight_scraper (7:00), queue_monitoring (4h), pending_tasks_freshness (8:00)

## 6. Ports (40 listening)
22(ssh) · 25(smtp) · 53(dns) · 80/443(web) · 3000-3002 · 4242 · 5000-5002 · 5432(pg) · 5678 · 6379(redis) · 7233(temporal) · 8001(tg webhook) · 8080(MC) · 8081-8089(apis) · 8233(temporal-ui) · 8644 · 8765 · 9100 · 11434(ollama) · 11435(broken llama bridge) · 18789-18792 · 37761 · 43243 · 65529

## 7. Databases
- `DepotChaos/depot_chaos.db` — vendors (147K), write_offs
- `data/depot_chaos/unified.db` — datadepot_intelligence (77K real) + demo
- `datadepot/data/collections.db` — collections_accounts (185)
- `/var/www/psdepot.com/...` — web assets

## 8. Secrets / config
- `aocros/secrets/smtp.env` (Hostinger SMTP/IMAP), `.env` (Google Places empty), `google_oauth_client.json`, `google_oauth_state.json`, `/root/.deepseek_env` (DeepSeek key)

---

## Scaffolding target (the "customer VPS" minimum)
A customer box needs, at minimum:
1. **Brain** (aos-brain-v4 + BHSI + model router) — or a lighter "suite-only" subset
2. **Agents** (their purchased suite: Greeter/Closeter/etc. + manifests/prompts)
3. **The outreach/order services** (CLOSETER inbox+reply, order API, submit_leads)
4. **Temporal** (durable workflows)
5. **Secrets/config** per customer (isolated)

Everything else (DepotChaos, collections, media/legal workers, game bridges, n8n, overpass) is **PSD-internal** and does NOT ship to a customer box.

*Next step: containerize the "customer minimum" into a compose file + provision script.*
