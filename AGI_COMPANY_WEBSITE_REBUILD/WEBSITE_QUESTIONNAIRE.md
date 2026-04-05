# AGI Company Website Rebuild - Design Questionnaire

**Date:** 2026-04-05
**Status:** Pre-Build Planning Phase
**Goal:** Complete site rebuild with unified design

---

## SECTION 1: BRAND IDENTITY (From Press Kit)

### 1.1 Visual Style Guide
| Element | Specification |
|---------|--------------|
| **Primary Background** | Deep Tech Blue `#0A1A2F` |
| **Accent Color** | Electric Cyan `#00E0FF` |
| **CTA Color** | Performance Orange `#FF7A00` |
| **Text Primary** | Cloud White `#F8F9FA` |
| **Text Secondary** | Titanium Gray `#C7CCD1` |

### 1.2 Typography
| Use | Font | Weight |
|-----|------|--------|
| **Headlines** | Inter Tight | 800 (H1), 700 (H2), 600 (H3) |
| **Body Text** | Inter | 400 (normal), 600 (bold) |
| **Code/Technical** | JetBrains Mono | 400, 500 |

### 1.3 Layout Standards
| Element | Measurement |
|---------|-------------|
| **Header Height** | 70px |
| **Sidebar Width** | 260px |
| **Navigation Gap** | 30px |
| **Footer Height** | 60px |
| **Page Padding** | 40px |
| **Card Border Radius** | 12px-16px |
| **Spacing Scale** | 4px, 8px, 16px, 24px, 32px, 48px, 64px |

---

## SECTION 2: SITE ARCHITECTURE

### 2.1 Core Pages (Required)

| Page | Priority | Status |
|------|----------|--------|
| **index.html** | HIGH | Redesign needed |
| **products.html** | HIGH | Complete rebuild |
| **agents.html** | HIGH | Redesign needed |
| **agent-status.html** | HIGH | KEEP AS-IS (Captain's favorite) |
| **brain.html** | MEDIUM | Remove sphere overlay, keep monitor |
| **cart.html** | HIGH | Complete rebuild |
| **checkout.html** | HIGH | Complete rebuild |
| **about.html** | MEDIUM | Create from press kit |
| **contact.html** | MEDIUM | Complete rebuild |
| **login.html** | MEDIUM | Complete rebuild |
| **register.html** | LOW | Create if needed |
| **dashboard.html** | LOW | Complete rebuild |
| **orders.html** | LOW | Complete rebuild |
| **privacy.html** | LOW | Legal page |
| **terms.html** | LOW | Legal page |
| **support.html** | LOW | Support page |

### 2.2 Product Categories (Must Include)

**CATEGORY 1: APEX C-Suite (6 Agents)**
- Miles - CEO / Dark Factory - Enterprise pricing
- Pulp - Head of Sales - $3,999/month
- Jane - Senior Sales Rep - $1,999/month
- Alpha-9 - CFO - $2,499/month
- Sentinel - CSO - $2,299/month
- Chelios - CISO - $2,799/month

**CATEGORY 2: Sales Team (4 Agents)**
- Hume - Regional Manager - $999/month
- Clippy-42 - Sales Assistant - $499/month
- GREET - Receptionist - $299/month
- CLOSETER - Sales Closer - $599/month

**CATEGORY 3: Technical Team (9 Agents)**
- Jordan - Lead Engineer - $1,899/month
- TAPTAP - DevOps - $1,299/month
- PIPELINE - CI/CD - $999/month
- BUGCATCHER - QA - $899/month
- R2-D2 - API Engineer - $1,099/month
- Spindle - Integration Arch - $1,599/month
- Velum - Database - $1,199/month
- Patricia - QA Lead - $1,399/month
- Fiber - Network - $1,249/month

**CATEGORY 4: Secretarial Pool (6 Agents)** ⭐ **MISSING FROM PREVIOUS BUILD**
- Judy - Executive Secretary - $799/month
- Mill - Document Processor - $599/month
- Boxtron - Archivist - $499/month
- REDACTOR - Data Redaction - $699/month
- SCRIBBLE - Note Taker - $399/month
- Velvet - Executive Assistant - $999/month

**CATEGORY 5: Security & Operations (3 Agents)**
- Sentinel Audit - Security Auditor - $1,499/month
- Dusty - Research Analyst - $1,199/month
- Forge - Factory Manager - $1,899/month

**CATEGORY 6: MYL Series (7 Agents)**
- MYLZERON - Memory Keeper - Custom
- MYLONEN - Transformer - Custom
- MYLTWON - Developer - Custom
- MYLTHREESS - Finance - Custom
- MYLFOURS - Security - Custom
- MYLFIVES - Clerk - Custom
- MYLSIXS - Membrane - Custom

**CATEGORY 7: Support Staff (1 Agent)**
- Mortimer - AI Platform - Custom

---

## SECTION 3: PAGE SPECIFICATIONS

### 3.1 HOME PAGE (index.html)
**Sections:**
1. Hero with animated background
2. Stats bar (36+ agents, 340% ROI, $0.12/task, 99.9% uptime)
3. Three-pillar value proposition (Precision, Excellence, Trust)
4. Featured agents preview (6 agents)
5. Brain architecture teaser
6. Use cases grid (4 cases)
7. Social proof/testimonials
8. Founder story
9. CTA section with trust badges
10. Footer

**Products shown:** Featured agents from each category

### 3.2 PRODUCTS PAGE (products.html)
**Structure:**
- Full catalog with all 36 agents
- Filter by: Category, Tier, Price Range
- Grid layout: 3-4 cards per row
- Each card: Avatar, Name, Role, Features, Price, "Add to Cart"
- Secretarial Pool section prominently displayed

### 3.3 AGENTS PAGE (agents.html)
**Structure:**
- Real-time status dashboard
- 6 agents per row (compact tiles)
- Status indicators (pulsing green/yellow/red)
- Team grouping (C-Suite, Sales, Technical, Secretarial, etc.)
- Auto-refresh every 30 seconds

### 3.4 BRAIN PAGE (brain.html)
**Changes Required:**
- ✅ REMOVE sphere overlay (Captain's instruction)
- Keep: Metrics panel, regions grid, Three.js visualization
- Keep: Real-time data from Brain v4
- Simplify visualization

### 3.5 CART PAGE (cart.html)
**Structure:**
- Cart items list
- Quantity controls
- Remove buttons
- Subtotal calculation
- Checkout CTA
- Continue shopping link

### 3.6 CHECKOUT PAGE (checkout.html)
**Structure:**
- Order summary sidebar
- Payment tabs (Credit Card / Crypto)
- Stripe integration
- MetaMask wallet connect
- Billing information form
- Place order button

### 3.7 ABOUT PAGE (about.html) - NEW
**From Press Kit:**
- "From Supply Chain to AGI" story
- Mission statement
- Values (Precision, Excellence, Trust)
- Team overview
- BEAST architecture explanation

### 3.8 CONTACT PAGE (contact.html)
**Structure:**
- Contact form
- Email, phone, address
- Social links
- Map (optional)

---

## SECTION 4: DESIGN DELIVERABLES

### 4.1 Assets Required
- [ ] Unified CSS file (agi-company.css)
- [ ] All 36 agent avatar images (or emojis)
- [ ] Company logo variations
- [ ] Product icons
- [ ] Background patterns

### 4.2 Technical Requirements
- Responsive (mobile, tablet, desktop)
- Dark mode only (no light mode)
- Chat widget on all pages
- Brain integration where applicable
- Stripe payment processing
- MetaMask wallet integration

---

## SECTION 5: BUILD CHECKLIST

### Phase 1: Template Creation
- [ ] Create unified CSS framework
- [ ] Build template.html with all navigation
- [ ] Test responsive breakpoints

### Phase 2: Core Pages
- [ ] index.html (Home)
- [ ] products.html (Full catalog)
- [ ] agents.html (Status)
- [ ] cart.html
- [ ] checkout.html

### Phase 3: Supporting Pages
- [ ] about.html
- [ ] contact.html
- [ ] login.html
- [ ] brain.html (simplified)

### Phase 4: Integration
- [ ] Chat widget on all pages
- [ ] Navigation links verified
- [ ] Footer consistent
- [ ] Meta tags for SEO

### Phase 5: Testing
- [ ] All links work
- [ ] Mobile responsive
- [ ] Forms functional
- [ ] Payment flow tested

### Phase 6: Deployment
- [ ] Backup old site
- [ ] Deploy new site
- [ ] Verify all pages live
- [ ] Test in production

---

## SECTION 6: APPROVAL REQUIRED

Before build starts, Captain must approve:

1. ✅ Page list (15 pages)
2. ✅ Product catalog (36 agents, 7 categories)
3. ✅ Pricing structure (monthly subscriptions)
4. ✅ Design system (fonts, colors, spacing)
5. ✅ Special requests (keep agent-status.html as-is, remove brain sphere)

**REPLY "APPROVED" TO BEGIN BUILD**

---

**Prepared by:** Miles  
**Date:** 2026-04-05  
**Version:** 1.0
