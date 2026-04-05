# AGI Company Website Rebuild

**Status:** In Progress - Awaiting Captain Approval  
**Location:** `/root/.openclaw/workspace/AGI_COMPANY_WEBSITE_REBUILD/`  
**Live Site:** https://myl0nr0s.cloud (current version)

## Built Pages ✅

| Page | File | Status | Features |
|------|------|--------|----------|
| **Home** | `index.html` | ✅ Complete | Hero, stats, value prop, agents preview, brain viz, CTA |
| **Agents** | `agents.html` | ✅ Complete | 36-agent roster, 6-per-row grid, real-time status |
| **CSS** | `css/agi-company.css` | ✅ Complete | Full design system based on press kit |

## Features Implemented

### Visual Design (Per Press Kit)
- ✅ Deep Tech Blue (#0A1A2F) + Electric Cyan (#00E0FF) palette
- ✅ Inter Tight / Inter typography
- ✅ "Intelligence Engineered." tagline
- ✅ Performance Orange (#FF7A00) CTAs

### Interactive Elements
- ✅ Chat widget (minimizes to 🤖 circle)
- ✅ Brain visualizer preview (6 nodes)
- ✅ Agent roster with live status indicators
- ✅ Responsive grid layouts

### Content
- ✅ 36 agent catalog structure
- ✅ Seven-region brain architecture
- ✅ Stats bar (340% ROI, $0.12/task, etc.)
- ✅ Professional footer

## Pages Remaining

- [ ] products.html (full catalog with pricing)
- [ ] brain.html (full 3D visualizer)
- [ ] checkout.html (Stripe + MetaMask)
- [ ] phone-lookup.html (working API)
- [ ] about.html (press kit content)
- [ ] contact.html

## Deployment

**DO NOT DEPLOY** until Captain approves the complete build.

When ready:
```bash
rsync -av /root/.openclaw/workspace/AGI_COMPANY_WEBSITE_REBUILD/ /var/www/myl0nr0s.cloud/
```

## Notes

- Agent status page at `/var/www/myl0nr0s.cloud/agent-status.html` is **LIVE** and working well
- Chat widget uses localStorage for messages
- All navigation standardized across pages
- Mobile responsive (breakpoints: 1024px, 768px)
