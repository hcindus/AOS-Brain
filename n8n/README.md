# n8n Installation

**Status:** ✅ Running  
**URL:** http://localhost:5678  
**Version:** Latest (Docker)  
**Data Volume:** `n8n_data` (persistent)

---

## Quick Access

| Endpoint | URL |
|----------|-----|
| **Web UI** | <http://localhost:5678> |
| **REST API** | <http://localhost:5678/api/v1> |
| **Webhook Base** | <http://localhost:5678/webhook/> |

---

## Authentication

| Field | Value |
|-------|-------|
| Username | `captain` |
| Password | `captain2025!` |

---

## Management

```bash
# Start n8n
cd /root/.openclaw/workspace/n8n
docker compose up -d

# Stop n8n
docker compose down

# View logs
docker compose logs -f

# Restart
docker compose restart

# Check status
docker ps | grep n8n
```

---

## For Agents

All agents can access n8n via:
- **Webhooks:** POST to `http://localhost:5678/webhook/<workflow-name>`
- **API:** `curl -u captain:captain2025! http://localhost:5678/api/v1/workflows`
- **Execute Workflow:** Use the n8n API or webhooks to trigger workflows

---

## Docker Compose

See `docker-compose.yml` for configuration.

---

**Installed:** 2026-04-02 by Miles
