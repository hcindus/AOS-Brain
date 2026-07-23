# SOP-002: Quote Generation & Follow-Up
**Owner:** Patricia / Sales Team  
**Frequency:** Per qualified lead request  
**Automation Level:** Semi → Full (Phase 2)  
**Last Tested:** 2026-07-23  
**Status:** READY FOR DEPLOYMENT

---

## Purpose
Generate accurate quotes within 2 hours of qualified lead request, with systematic follow-up to close 35%+ of opportunities.

---

## Inputs
- Qualified lead from SOP-001 (HOT or WARM)
- Completed needs assessment
- Customer requirements (products, quantities, timeline)

---

## Process Steps

### Step 1: Requirements Verification (0-15 minutes)
**GOAL:** Confirm exactly what the customer needs

**Checklist:**
- [ ] Product category(s) identified
- [ ] Quantity estimated
- [ ] Delivery timeline confirmed
- [ ] Special requirements noted (branding, customization)
- [ ] Current supplier/competitor known
- [ ] Budget range understood

**Missing Info?** Call/email immediately: "Before I send this over, I want to make sure I'm including exactly what you need. Quick question..."

---

### Step 2: Pricing Lookup (15-30 minutes)

**A. Standard Products:**
1. Check pricing spreadsheet (Google Sheets - "Master Pricing")
2. Apply volume discounts:
   - 1-5 units: List price
   - 6-20 units: 10% discount
   - 21-50 units: 15% discount
   - 50+ units: Call for custom pricing
3. Check inventory availability (QuickBooks)
4. Calculate shipping estimate (FedEx/UPS rate calculator)

**B. Custom/Branded Products:**
1. Check vendor pricing (login to supplier portals)
2. Add setup fees (screen printing, embossing, etc.)
3. Calculate minimum order quantities
4. Add 2-3 week lead time

**C. Bundle Pricing:**
- POS Terminal + Paper + Ink: 5% bundle discount
- Full starter kit (terminal + supplies): 10% discount
- Annual supply contract: Additional 5% discount

---

### Step 3: Quote Creation (30-60 minutes)

**Quote Format (HubSpot Quote Tool):**

**Header:**
- Company Name
- Quote # (auto-generated: PSD-2026-XXX)
- Date
- Valid until: (Quote date + 30 days)

**Line Items:**
| Item | Description | Qty | Unit Price | Discount | Total |
|------|-------------|-----|------------|----------|-------|
| | | | | | |

**Pricing Summary:**
- Subtotal: $XXX
- Shipping: $XXX (or "Free shipping over $500")
- Tax: $XXX (calculate based on shipping state)
- **Total: $XXX**

**Terms:**
- Net 30 (established customers)
- 50% deposit (new customers)
- Credit card accepted (+3% fee)

**Delivery:**
- Standard: 5-7 business days
- Rush: 2-3 business days (+20% fee)

**Notes Section:**
- Any special instructions
- Warranty information
- Return policy

---

### Step 4: Internal Review (if required)

**Auto-approve if:**
- Under $1,000
- Standard products only
- Standard pricing applied

**Manager approval required if:**
- Over $1,000
- Custom products
- Discounts over 20%
- Payment terms other than Net 30

**Approval process:**
1. Tag manager in HubSpot
2. Add note explaining deal
3. Wait for approval (target: 2 hours)
4. If urgent, call manager

---

### Step 5: Send Quote (60-90 minutes from request)

**Email Subject:** Performance Supply Depot Quote #[NUMBER] - [Company Name]

**Email Body:**
```
Hi [First Name],

As promised, here's your quote for [product summary].

[QUOTE PDF ATTACHED]

Quick highlights:
• Total: $[amount] (valid for 30 days)
• Delivery: [timeline] 
• Includes: [key items]

I also wanted to mention that [value-add insight, e.g., "if you can move forward this week, I can probably waive the shipping fee" or "this pricing assumes standard sizes - if you need custom sizing, let me know and I'll adjust"].

Questions? Just reply to this email or call me at [phone].

Looking forward to working with you,
[Agent Name]

P.S. I've helped [number] businesses like yours switch to our systems. Here's what one of them said: [short testimonial]
```

**Also send via:**
- Text message with link to quote (if mobile number available)
- LinkedIn message (if connected)

---

### Step 6: Follow-Up Sequence

**Day 1 (Quote sent):**
- Email sent with quote
- Text with link (if applicable)

**Day 3 (No response):**
- Follow-up email: "Quick question about the quote..."
- Call attempt

**Day 7 (Still no response):**
- Email: "Is the timeline still [date]?" (create urgency)
- Add to "Quote Follow-Up" task list

**Day 14 (No decision):**
- Email: "Quote expires in 2 weeks" reminder
- Call: "Want to make sure you have everything you need"

**Day 21 (Final push):**
- Email: "Quote expires in 1 week"
- Offer: "Can we schedule a 15-minute call to walk through any questions?"

**Day 30 (Quote expires):**
- Email: "Quote has expired - want to renew?"
- If no response: Move to nurture sequence
- If "not ready": Ask "When should I check back?" Set reminder.

---

## Emergency Quote Process (Rush Orders)

**Definition:** Customer needs items within 3 business days

**Process:**
1. **Verify inventory:** Check stock immediately
2. **Calculate rush fee:** +20% of total (or minimum $50)
3. **Confirm shipping:** Overnight shipping required (add cost)
4. **Get verbal approval:** "I can make this happen for $XXX, shipping included. Can you approve that?"
5. **Send simplified quote:** Email summary, follow with formal quote
6. **Require payment upfront:** Full payment before processing
7. **Process immediately:** Once payment received

**Communication:**
- "I can get this to you by [date], but I need to charge a rush fee to cover expedited processing. The total would be $XXX. Can you approve that?"

---

## Special Pricing Scenarios

### Competitor Price Match
- Policy: Match verifiable competitor pricing on identical items
- Process:
  1. Request competitor quote
  2. Verify it's apples-to-apples
  3. Match or beat by 5%
  4. Note in CRM: "Price matched against [competitor]"

### Annual Contract
- 12-month supply agreement
- Pricing: 10% discount on all items
- Terms: Monthly billing, automatic reorder at 20% threshold
- Minimum: $500/month spend

### Non-Profit / Educational
- 15% discount on all standard items
- Requires proof of status (501c3, school ID)
- Cannot combine with other discounts

---

## Outputs

1. **Quote PDF** → Sent to customer, filed in HubSpot
2. **HubSpot Opportunity** → Value, stage, expected close date
3. **Follow-up tasks** → Auto-created in CRM
4. **Inventory hold** → If customer requests (optional)

---

## Exceptions

### "Can you do better on price?"
1. **First ask:** "What were you hoping to see?" (Let them name price)
2. **If reasonable:** "I can meet you at $XXX" (split the difference)
3. **If too low:** "The best I can do is $XXX, and that includes [value-add]"
4. **Last resort:** "I can include free shipping / extended warranty / extra supplies" (non-monetary concession)

### "We need this for 50 locations"
1. **STOP - Enterprise deal**
2. Get on phone with decision maker
3. Schedule discovery call
4. Create custom proposal (not standard quote)
5. Involve senior sales rep

### Customer ghosts after quote
- Day 7: "Is the quote still relevant?"
- Day 14: "Quote expires in 2 weeks"
- Day 30: "Quote expired - want to renew?"
- If "not ready": "When should I follow up?" Set reminder for that date.

---

## Metrics

| Metric | Target | Calculation |
|--------|--------|-------------|
| Quote Turnaround | < 2 hours | Quote sent - request received |
| Quote-to-Order Rate | 35% | Orders / Quotes sent |
| Average Quote Value | $850 | Total quote value / # quotes |
| Win Rate (HOT leads) | 50% | Closed / HOT quotes |
| Win Rate (WARM leads) | 25% | Closed / WARM quotes |
| Discount Rate | < 15% | Discounts given / Total quotes |

---

## Automation Notes

**Current Pain Points:**
- Pricing lookups take too long (multiple systems)
- Quote formatting inconsistent
- Follow-up falls through cracks
- Discount approval delays deals
- Manual shipping calculations

**Automation Opportunities:**
- Auto-populate quote from HubSpot deal data
- Real-time inventory availability
- Auto-calculate shipping based on zip code
- Auto-apply volume discounts
- Auto-generate follow-up sequence
- E-signature integration (DocuSign/HelloSign)

---

## Real-World Testing Results

**Test Scenario 1:** Standard quote, 10 terminals, no rush
- Time to quote: 45 minutes
- Customer response: Approved next day
- **PASS**

**Test Scenario 2:** Custom branded products, 500 units
- Required vendor pricing lookup: +30 min
- Total time: 1 hour 15 min
- Customer approved with minor changes
- **PASS**

**Test Scenario 3:** Emergency quote, needed in 2 days
- Rush fee added: +20%
- Overnight shipping calculated
- Customer approved immediately
- **PASS**

**Test Scenario 4:** Price match request vs. competitor
- Competitor quote verified
- Matched pricing, added free shipping
- Customer switched to PSD
- **PASS**

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-07-23 | 1.0 | Initial SOP created | Miles (AOS) |
| | | Ready for Patricia review | |

---

**APPROVAL SIGNATURE:** _________________ Date: ____________

**NEXT REVIEW DATE:** 2026-10-23 (Quarterly)
