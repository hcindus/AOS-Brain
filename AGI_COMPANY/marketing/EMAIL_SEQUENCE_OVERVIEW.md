# Performance Supply Depot - Marketing Integration Guide
## 20-Email Campaigns + Weekly Newsletter Alignment

---

## Campaign Structure Overview

**6 Active State Campaigns:**
- CA_campaign_20260428.json (California)
- NV_campaign_20260428.json (Nevada - Las Vegas focus)
- NM_campaign_20260428.json (New Mexico)
- OR_campaign_20260428.json (Oregon)
- TX_campaign_20260428.json (Texas)
- WA_campaign_20260428.json (Washington)

**Each Campaign:** 70 leads × 20 emails = 1,400 touchpoints

---

## 20-Email Sequence Breakdown

| Email # | Name | Purpose | Newsletter Alignment |
|---------|------|---------|---------------------|
| 1 | Initial Outreach | First contact, establish presence | **Week 5** (New Business Setup) |
| 2 | Value Proposition | Highlight services | **Week 1** (Cost Management) |
| 3 | Social Proof | Share success stories | **Week 4** (Operational Efficiency) |
| 4 | Special Offer | Promotional discount | **Week 3** (POS Technology) |
| 5 | Case Study | Detailed savings example | **Week 1** (Cost Management) |
| 6 | Direct Ask | Request decision | **Week 2** (Printer Maintenance) |
| 7 | Final Attempt - Soft | Permission to close | - |
| 8 | Breakup - Last | Final outreach | - |
| 9 | Re-engagement | Check in after break | **Week 4** (Efficiency) |
| 10 | New Products | Feature updates | **Week 3** (POS Technology) |
| 11 | Seasonal | Holiday prep | **Week 5** (New Business) |
| 12 | Referral Ask | Request introductions | - |
| 13 | Win Back | Return offer | **Week 6** (Seasonal) |
| 14 | Industry Update | Market insights | **Week 8** (Trends) |
| 15 | Testimonial | Customer quote | **Week 4** (Social Proof) |
| 16 | Event Invitation | Local meetup | **Week 8** (Trends) |
| 17 | Survey | Feedback request | **Week 8** (Insights) |
| 18 | Competitive | Compare options | **Week 3** (POS Technology) |
| 19 | Urgency | Price increase warning | **Week 6** (Seasonal) |
| 20 | Final Final | Last chance | - |

---

## 8-Week Newsletter Cycle

Each newsletter **expounds on the topic** from the email sequence, providing deeper value.

### Week 1: Supply Chain & Cost Management
**Aligns with:** Emails #2 (Value Proposition), #5 (Case Study)
**Content:** 15-20% cost increases, locking in pricing, 2-week buffer strategy
**Key Stats:** 2024-2025 supply chain data
**CTA:** Get a quote, lock in pricing

### Week 2: Printer Maintenance & Repair
**Aligns with:** Emails #6 (Direct Ask), #2 (Value Proposition)
**Content:** 5-minute monthly cleaning routine, when to call a tech
**Key Stats:** $847 vs $15/month prevention
**CTA:** Book diagnostic, printer swaps

### Week 3: POS Technology & Upgrades
**Aligns with:** Emails #4 (Special Offer), #10 (New Products), #18 (Competitive)
**Content:** Samsung vs Sam4s, cloud vs local, professional setup ROI
**Key Stats:** $500-1,200 hardware, $1,500-3,500 with setup
**CTA:** Consultation, quote

### Week 4: Operational Efficiency
**Aligns with:** Emails #3 (Social Proof), #9 (Re-engagement), #15 (Testimonial)
**Content:** 2-week buffer rule, supply management systems
**Key Stats:** Most restaurants keep 3-5 days (should be 14)
**CTA:** Calculate your buffer

### Week 5: New Business Setup
**Aligns with:** Emails #1 (Initial Outreach), #11 (Seasonal)
**Content:** End-to-end POS setup, common mistakes
**Key Stats:** 800+ setups, 15 years experience
**CTA:** Setup consultation

### Week 6: Seasonal Preparation
**Aligns with:** Emails #11 (Seasonal), #13 (Win Back), #19 (Urgency)
**Content:** Holiday prep checklist, December survival guide
**Key Stats:** 40% of annual revenue in 6 weeks
**CTA:** Pre-season tune-up

### Week 7: Staff Training & Support
**Aligns with:** Email #6 (Direct Ask - mentions 24/7 support)
**Content:** Why training fails, scenario-based approach
**Key Stats:** 70% forgotten within a week
**CTA:** Refresher training

### Week 8: Industry Trends & Insights
**Aligns with:** Emails #14 (Industry Update), #16 (Event), #17 (Survey)
**Content:** Cloud vs local, trends worth watching vs skipping
**Key Stats:** Monthly fee savings with local systems
**CTA:** Discuss setup

---

## Integration Strategy

### Weekly Workflow (Mondays)

1. **Generate Newsletter** (12 PM UTC)
   ```
   cd /root/.openclaw/workspace/scripts/x_marketing
   python3 newsletter_generator.py current
   ```

2. **Send to Email List** (Email marketing platform)
   - Subject line from newsletter
   - HTML version with CTA buttons
   - Plain text fallback

3. **Update X/TikTok Content** (Aligned with newsletter theme)
   ```
   python3 x_content.py [relevant_topic]
   python3 tiktok_content.py daily
   ```

4. **Schedule Social Posts** (Same theme, shorter format)
   - X: 3 posts (EN/ES/ZH)
   - TikTok: 1 video script

### Monthly Review

**First Monday of Month:**
- Review newsletter performance (opens, clicks)
- Adjust content based on engagement
- Check email campaign metrics
- Update templates with seasonal adjustments

---

## Content Repository

**Scripts Location:** `/root/.openclaw/workspace/scripts/x_marketing/`

| File | Purpose |
|------|---------|
| `x_content.py` | X (Twitter) posts in 3 languages |
| `tiktok_content.py` | TikTok video scripts |
| `newsletter_generator.py` | Weekly newsletter content |
| `review_content.py` | Ethics/content review tool |

**Campaign Data:** `/root/.openclaw/workspace/AGI_COMPANY/data/campaigns/`

**Output Logs:**
- `/var/log/x_marketing.log` - X/TikTok content
- `/var/log/newsletter_content.log` - Newsletter content

---

## Contact Information (Consistent Across All Channels)

**Phone:** 888-881-6834
**Website:** https://psdepot.com
**Email:** info@psdepot.com
**Alt Phone:** 415-571-9724

---

## Key Messaging Principles

1. **Educational First** - Teach before selling
2. **Factual Claims** - No exaggerated savings
3. **Local Vegas Focus** - 10,000+ restaurants served
4. **Same-Day Service** - When it matters most
5. **Professional Setup** - Not just products, solutions

---

## Quick Commands

```bash
# Generate today's X content
python3 /root/.openclaw/workspace/scripts/x_marketing/x_content.py daily

# Generate TikTok script
python3 /root/.openclaw/workspace/scripts/x_marketing/tiktok_content.py daily

# Generate this week's newsletter
python3 /root/.openclaw/workspace/scripts/x_marketing/newsletter_generator.py current

# Generate HTML version
python3 /root/.openclaw/workspace/scripts/x_marketing/newsletter_generator.py html

# List all newsletter themes
python3 /root/.openclaw/workspace/scripts/x_marketing/newsletter_generator.py list
```

---

## Next Steps

1. ✅ Review this overview
2. ✅ Set up email marketing platform integration (Mailchimp/SendGrid)
3. ✅ Import newsletter content into email templates
4. ✅ Schedule first newsletter send (Week 1)
5. ✅ Align X/TikTok posts with weekly theme
6. ✅ Monitor engagement and adjust

---

*Last Updated: 2026-04-28*
*Campaign Status: 6 states active, 420 total leads, 8,400 scheduled emails*
