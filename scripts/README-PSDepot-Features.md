# PSDepot AI Features - Setup Guide

Three new features to match 11 Labs capabilities on psdepot.com.

## Quick Overview

| Feature | Files | URL |
|---------|-------|-----|
| **Cal.com Booking** | `/var/www/psdepot.com/booking.html`, API in `depotchaos_fastapi.py` | https://psdepot.com/booking.html |
| **Chat Widget** | `/var/www/psdepot.com/widget/chat-widget.js` | Add to any page |
| **Auto-Crawl RAG** | `/root/.openclaw/workspace/scripts/auto_crawl_rag.py` | https://psdepot.com/kb-admin.html |

---

## 1. Cal.com Booking Integration

### Setup

1. **Create Cal.com Account**
   - Go to https://cal.com
   - Sign up with info@psdepot.com
   - Create an event type "consultation" (30 min)

2. **Get API Key** (Optional - for full API integration)
   - Settings → API Keys → Generate
   - Add to environment: `export CALCOM_API_KEY=your_key_here`
   - Or add to systemd service: `systemctl edit depotchaos`

3. **Configure Webhook** (Optional)
   - In Cal.com: Settings → Webhooks
   - Add webhook URL: `https://psdepot.com/api/cal/webhook`
   - Select events: booking_created, booking_cancelled, booking_rescheduled

### Embed Mode (No API Key)

The booking page works without an API key using Cal.com's embed script. The widget displays your Cal.com calendar inline.

### API Endpoints (with API key)

```bash
# Check Cal.com status
GET /api/cal/health

# Create booking
POST /api/cal/book
{
  "eventTypeId": 12345,
  "start": "2025-07-25T14:00:00Z",
  "end": "2025-07-25T14:30:00Z",
  "name": "John Doe",
  "email": "john@example.com",
  "notes": "Need POS system advice"
}

# Get availability
POST /api/cal/availability
{
  "eventTypeId": 12345,
  "dateFrom": "2025-07-25",
  "dateTo": "2025-07-30"
}

# List bookings
GET /api/cal/bookings?status=upcoming&limit=20

# Webhook receiver
POST /api/cal/webhook
```

---

## 2. Chat Widget

### Installation

Add to any HTML page:

```html
<!-- At the bottom of your page, before </body> -->
<script src="https://psdepot.com/widget/chat-widget.js"></script>
<script>
    PSDepotChat.init({
        apiUrl: 'http://localhost:8080',
        position: 'bottom-right',
        voiceEnabled: true
    });
</script>
```

### Configuration Options

```javascript
PSDepotChat.init({
    apiUrl: 'http://localhost:8080',     // Mission Control URL
    position: 'bottom-right',            // Position: bottom-right, bottom-left, etc.
    title: 'Chat with Miles',            // Widget title
    subtitle: 'AI Sales Assistant',      // Subtitle text
    placeholder: 'Ask about products...', // Input placeholder
    voiceEnabled: true                   // Enable voice input
});
```

### Demo Page

Visit https://psdepot.com/chat-demo.html to see it in action.

---

## 3. Auto-Crawl RAG System

### Initial Setup

1. **Initialize the knowledge base:**
   ```bash
   python3 /root/.openclaw/workspace/scripts/auto_crawl_rag.py crawl
   ```

2. **Check the admin panel:**
   Visit https://psdepot.com/kb-admin.html

3. **Test search:**
   ```bash
   python3 /root/.openclaw/workspace/scripts/auto_crawl_rag.py search "thermal paper"
   ```

### API Endpoints

```bash
# Check KB status
GET /api/kb/health

# Search knowledge base
POST /api/kb/search
{
  "query": "thermal paper prices",
  "limit": 5
}

# Refresh knowledge base (async)
POST /api/kb/refresh

# List documents
GET /api/kb/documents?limit=50
```

### Automated Weekly Crawl

Add to crontab:

```bash
# Edit crontab
sudo crontab -e

# Add this line for weekly Sunday 2am crawl
0 2 * * 0 /usr/bin/python3 /root/.openclaw/workspace/scripts/auto_crawl_rag.py crawl >> /var/log/psdepot_crawl.log 2>&1

# Or use the setup script
sudo bash /root/.openclaw/workspace/scripts/setup_crawl_cron.sh
```

### CLI Usage

```bash
# Crawl all pages
python3 auto_crawl_rag.py crawl

# Search
python3 auto_crawl_rag.py search "thermal paper"

# Show stats
python3 auto_crawl_rag.py stats
```

---

## Restart Services

After making changes:

```bash
# Restart DepotChaos API (loads new endpoints)
sudo systemctl restart depotchaos

# Check status
sudo systemctl status depotchaos

# View logs
sudo journalctl -u depotchaos -f
```

---

## File Locations

```
/var/www/psdepot.com/
├── booking.html                    # Cal.com booking page
├── chat-demo.html                  # Chat widget demo
├── kb-admin.html                   # Knowledge base admin
└── widget/
    └── chat-widget.js              # Embeddable chat widget

/root/.openclaw/workspace/
├── scripts/
│   ├── auto_crawl_rag.py          # Crawler script
│   └── README-PSDepot-Features.md   # This file
└── data/
    └── psdepot_kb.db                # Knowledge base SQLite

/root/.openclaw/workspace/datadepot/web/
└── depotchaos_fastapi.py           # FastAPI with new endpoints
```

---

## Troubleshooting

### Chat widget shows "API Error"
- Check Mission Control is running: `curl http://localhost:8080/api/health`
- Check browser console for CORS errors
- Ensure `apiUrl` points to correct Mission Control URL

### Cal.com shows "Not configured"
- This is normal for embed mode - it uses Cal.com's hosted widget
- For API integration, add CALCOM_API_KEY environment variable

### Knowledge base shows "Not initialized"
- Run initial crawl: `python3 auto_crawl_rag.py crawl`
- Check permissions on `/root/.openclaw/workspace/data/`

### Booking page not loading calendar
- Verify Cal.com account exists at cal.com/psdepot
- Check browser console for embed script errors
- Try Cal.com's embed test page first

---

## Next Steps

1. **Set up Cal.com account** and configure the consultation event type
2. **Add CALCOM_API_KEY** if you want full API integration
3. **Run initial crawl** to populate the knowledge base
4. **Add chat widget** to psdepot.com index.html
5. **Set up weekly cron** for automatic knowledge base refresh
6. **Configure WhatsApp Business API** when ready (separate from these features)

---

## Links

- **Booking Page:** https://psdepot.com/booking.html
- **Chat Demo:** https://psdepot.com/chat-demo.html
- **KB Admin:** https://psdepot.com/kb-admin.html
- **Mission Control:** http://localhost:8080
- **API Base:** https://psdepot.com/api/