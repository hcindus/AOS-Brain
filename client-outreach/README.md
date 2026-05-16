# Client Outreach App

A mobile-first PWA for client outreach and email scheduling.

## Features

- **Client Management**: Full CRUD for client records
- **Email Scheduling**: Queue emails with timestamps
- **Mobile-First**: Designed for on-the-go sales teams
- **PWA**: Installable on Android/iOS
- **FastAPI Backend**: Modern Python API

## Quick Start

```bash
# Run the app
./run.sh
```

Access at: `http://localhost:8083`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| GET | /api/clients | List clients |
| POST | /api/clients | Create client |
| GET | /api/clients/{id} | Get client |
| PUT | /api/clients/{id} | Update client |
| DELETE | /api/clients/{id} | Delete client |
| GET | /api/clients/need-contact/today | Today's follow-ups |
| POST | /api/clients/{id}/activities | Add activity |
| GET | /api/clients/{id}/activities | Get activities |
| POST | /api/email-queue | Schedule email |
| GET | /api/email-queue/pending | Get pending emails |
| GET | /api/email-queue/stats | Queue statistics |

## Demo Data

5 demo clients pre-populated:

| Name | Company | Tier | Status |
|------|---------|------|--------|
| Sarah Chen | Golden Dragon Restaurant | Prime | Active |
| Mike Torres | Barrio Tacos | PPCL | Prospect |
| Lisa Park | Seoul Kitchen | Stone | Inactive |
| Dave Kumar | Spice Route | PPCL | Follow-up |
| Emma Wilson | Coastal Grill | Prime | New |

## Building the APK (TWA)

```bash
# Generate APK from PWA using Bubblewrap
npx @bubblewrap/cli build
```

## File Structure

```
client-outreach/
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic models
│   └── crud.py          # Database operations
├── database/
│   ├── schema.sql       # Database schema + demo data
│   └── outreach.db      # SQLite database
├── static/
│   ├── css/style.css    # Mobile-first styles
│   ├── js/
│   │   ├── app.js       # Main JavaScript
│   │   └── sw.js        # Service worker
│   └── manifest.json    # PWA manifest
├── templates/
│   ├── index.html       # Dashboard
│   ├── clients.html     # Client list
│   ├── client_detail.html
│   └── scheduler.html
└── run.sh               # Startup script
```

## Port

- **Dev:** 8083
- **Production:** Via nginx reverse proxy
