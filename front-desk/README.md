# Frontline SOA

**Performance Supply Depot — Service Oriented Assistant.**

A single intake surface for every inbound channel — voice, email, text, web, DM —
that classifies intent, routes to the right fleet agent, persists a contact history,
and alerts the team. Packaged as a live FastAPI service with a clean operations dashboard.

---

## What it does

```
InboundEvent ──▶ engine.classify() ──▶ Route ──▶ store.log()   (SQLite contact history)
   (channel, from, body)      │  intent/urgency/entity       └─▶ alert.dispatch()  (Telegram)
                              └─▶ router.route(intent) ──▶ fleet agents
```

| Layer | File | Role |
|-------|------|------|
| Engine | `engine.py` | LLM intent classifier (`InboundEvent` → `Route`) |
| Router | `router.py` | intent → fleet-agent destination |
| Agents | `agents.py` | closeter · concierge · lead_qualifier · content_generator · followup_writer |
| Store | `store.py` | SQLite inbound log + repeat-contact history |
| Alert | `alert.py` | Telegram dispatch to the routed agent(s) |
| Server | `server.py` | FastAPI REST API + dashboard |
| UI | `static/` | operations dashboard |

## Sellable suites

| Suite | Agents | Price |
|-------|--------|-------|
| Front office | greeter · missed-call · review · ping | $149/mo |
| Growth | closeter · concierge | $349/mo |
| Full office | clerk · ea · miles | $749/mo |
| Security | chelios | $99/mo add-on |

## Routing

| Intent | Agents |
|--------|--------|
| sales | closeter · miles |
| support | concierge · clerk |
| legal | redactor |
| security | chelios |
| hr | feelix |
| logistics | concierge |
| catch-all | greeter |

---

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | dashboard UI |
| `GET` | `/health` | liveness + model + uptime |
| `POST` | `/api/inbound` | full intake (classify → store → alert) |
| `POST` | `/api/classify` | dry-run classify (no persistence) |
| `GET` | `/api/inbound` | recent feed (`?limit=`, `?intent=`, `?qualified=`) |
| `GET` | `/api/stats` | totals, intent/qualified/channel mix, agent counts |
| `GET` | `/api/suites` | suites + routing + model |

**Intake payload:**
```json
{ "channel": "voice", "from": "+14155550123", "body": "I need a quote for thermal paper." }
```

---

## Setup

```bash
# 1. configure (LLM base_url / model / telegram) in config.yaml
# 2. install + start as a service
sudo bash setup/install.sh

# or run it directly
python3 server.py            # -> http://127.0.0.1:8120
```

Expose publicly via nginx (see `setup/nginx.conf`) → `https://psdepot.com/frontline/`.

---

## Configuration

`config.yaml` — LLM (OpenAI-compatible, defaults to Ollama + Mort_II), suites, routing,
alert (Telegram), and store path. Every value supports `${VAR:-default}` env expansion;
secrets live in `aocros/secrets/`.

## Client provisioning

Onboarding a new client is driven by two files:

- **`client_questionnaire.md`** — the client-facing setup form (company info, tone of
  greeting, tone of receptionist, emergency contact, emails, cadence, suite).
- **`client_config.example.yaml`** — the provisioning config the answers map to; copy to
  a per-client `client_config.yaml` when booting that client's SOA.

---

## Self-test

```bash
python3 validate.py     # runs 5 sample inbound messages, prints classified routes
```
