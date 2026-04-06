# Product Pages

This directory contains landing pages for Performance Supply Depot products.

## Pages

### CREAM — Real Estate CRM
- **Landing Page:** `file:///root/.openclaw/workspace/pages/cream/index.html`
- **Leads:** `file:///root/.openclaw/workspace/pages/cream/leads.html`
- **Pipeline:** `file:///root/.openclaw/workspace/pages/cream/pipeline.html`
- **Analytics:** `file:///root/.openclaw/workspace/pages/cream/analytics.html`
- **Description:** AI-powered CRM for real estate professionals
- **Features:** Lead scoring, mobile app, auto-follow-up, deal pipeline
- **Status:** ✅ All pages created

### ReggieStarr — POS System  
- **URL:** `file:///root/.openclaw/workspace/pages/reggiestarr/index.html`
- **Description:** Digital cash register with crypto payments
- **Features:** Multi-currency, KDS, inventory, reports
- **Status:** ✅ Page created

## To View
Open in browser:
```bash
# CREAM CRM Suite
firefox /root/.openclaw/workspace/pages/cream/index.html
firefox /root/.openclaw/workspace/pages/cream/leads.html
firefox /root/.openclaw/workspace/pages/cream/pipeline.html
firefox /root/.openclaw/workspace/pages/cream/analytics.html

# ReggieStarr POS
firefox /root/.openclaw/workspace/pages/reggiestarr/index.html
```

## CREAM CRM Features

### Leads Page
- Lead statistics (New, Hot, Warm, Cold)
- Searchable lead table with AI scores
- Status badges and action buttons
- Pagination support

### Pipeline Page
- Kanban-style deal board
- 5 stages: New Leads → Qualified → Viewing → Offer Made → Closed Won
- Deal cards with values, priorities, and assigned agents
- Drag-and-drop ready UI

### Analytics Page
- KPI cards (Revenue, Deals, Deal Size, Conversion)
- Revenue trend chart
- Lead sources breakdown (pie chart)
- Top performers table
- Conversion funnel visualization

## Hosting Options
- Local: `file:///root/.openclaw/workspace/pages/[product]/`
- Miles.cloud: Can be served via nginx
- GitHub Pages: Push to gh-pages branch

Created: 2026-04-06
