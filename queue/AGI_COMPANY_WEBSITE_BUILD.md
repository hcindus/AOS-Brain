# AGI COMPANY WEBSITE BUILD — QUEUE REQUEST
**Assigned To:** Patricia (Process Excellence Officer)  
**Priority:** HIGH  
**Target:** myl0nr0s.cloud  
**Status:** ⏳ AWAITING PATRICIA REVIEW

---

## EXECUTIVE SUMMARY

Build and deploy a complete AGI Company website based on:
1. Press Kit assets (Visual Style Guide, Brand Assets, Website Copy)
2. Product catalog (72 agents, services)
3. Company information (Performance Supply Depot LLC division)

**Goal:** Professional, founder-grade website ready for public launch.

---

## SOURCE MATERIALS

### 1. Press Kit (Complete)
**Location:** `/docs/press_kit/`

| Asset | File | Purpose |
|-------|------|---------|
| Visual Style Guide | `01_VISUAL_STYLE_GUIDE.md` | Colors, typography, layout rules |
| Brand Asset Pack | `02_BRAND_ASSET_PACK.md` | CSS variables, components, logos |
| Motion Design System | `03_MOTION_DESIGN_SYSTEM.md` | Animations, transitions |
| Brand Voice Training | `04_BRAND_VOICE_TRAINING.md` | Tone, messaging |
| Persona Marketing | `05_PERSONA_ALIGNED_MARKETING.md` | Agent roles, messaging |
| Website Copy | `06_WEBSITE_COPY.md` | Complete copy for all pages |
| Launch Announcement | `07_LAUNCH_ANNOUNCEMENT.md` | Press release content |

**Brand Foundation:**
- **Colors:** Deep Tech Blue (#0A1A2F), Electric Cyan (#00E0FF), Performance Orange (#FF7A00)
- **Typography:** Inter Tight (headlines), Inter (body), JetBrains Mono (code)
- **Tagline:** "Intelligence Engineered."
- **Parent:** Performance Supply Depot LLC

### 2. Product Catalog
**Agents:** 72+ specialized agents including:
- QORA (Strategic Lead)
- SPINDLE (CTO)
- SCRIBBLE (Creative)
- TAPTAP (UX)
- SENTINEL (Security)
- LEDGER-9 (Finance)
- PATRICIA (Process Excellence)
- Plus 65+ additional agents

**Services:**
- Agent deployment and management
- Custom agent development
- Enterprise consulting
- Training and onboarding

### 3. Company Information
- **Name:** AGI Company
- **Division of:** Performance Supply Depot LLC
- **Founded:** 2024
- **Location:** Digital Frontier
- **Mission:** Making AGI tangible

---

## WEBSITE REQUIREMENTS

### Pages to Build

**1. Homepage (`index.html`)**
- Hero section with headline "Intelligence Engineered."
- Three-pillar value grid (Precision, Performance, Trust)
- Agent roster preview (7 featured agents)
- CTA buttons (Meet the Agents, See How It Works)
- Stats bar (72+ agents, 340% ROI, $0.12/1k tasks)

**2. Agents Page (`/agents/`)**
- Full agent directory (72 agents)
- Filter by department (Strategy, Technical, Creative, Operations, Security, Finance)
- Agent cards with photo, role, capabilities, pricing
- Individual agent profile pages

**3. Architecture Page (`/architecture/`)**
- Seven-region brain visualization
- BEAST principles explanation
- Technical specifications
- Security model
- Performance metrics

**4. Pricing Page (`/pricing/`)**
- Three tiers: Starter ($499/mo), Professional ($1,999/mo), Enterprise (Custom)
- Feature comparison table
- ROI calculator
- FAQ section

**5. About Page (`/about/`)**
- Founder story
- Company history
- Team/agents overview
- Press kit download
- Contact information

**6. Documentation Portal (`/docs/`)**
- Quick start guide
- API reference
- SDK documentation
- Best practices
- Community forum link

**7. Contact Page (`/contact/`)**
- Contact form
- Email: press@agicompany.ai
- Social links
- Office location (Digital Frontier)

### Technical Stack

**Recommended:**
- **Framework:** Static site (HTML/CSS/JS) or Next.js
- **Styling:** Tailwind CSS with brand color variables
- **Hosting:** myl0nr0s.cloud (existing VPS)
- **CDN:** CloudFlare (optional)
- **SSL:** Let's Encrypt (via Hostinger or certbot)

**Requirements:**
- Responsive design (mobile-first)
- Dark mode support (Deep Tech Blue base)
- Fast load times (<3s)
- SEO optimized
- Accessibility compliant (WCAG AA)

---

## PATRICIA'S PROCESS (DMAIC)

### Define Phase
- [ ] Confirm scope and page requirements
- [ ] Validate technical stack
- [ ] Set success criteria
- [ ] Establish timeline

**Success Criteria:**
- All 7 pages functional
- Mobile responsive
- Loads in <3 seconds
- SEO score >90
- No broken links
- SSL certificate active

### Measure Phase
- [ ] Baseline: Current myl0nr0s.cloud state
- [ ] Resource requirements
- [ ] Risk assessment

### Analyze Phase
- [ ] Review press kit assets
- [ ] Validate copy and branding
- [ ] Plan site architecture

### Improve Phase
- [ ] Build website
- [ ] Implement styling
- [ ] Add animations (per Motion Design System)
- [ ] Content population
- [ ] Testing

### Control Phase
- [ ] Deploy to myl0nr0s.cloud
- [ ] Configure SSL
- [ ] Set up monitoring
- [ ] Documentation handoff

---

## DEPLOYMENT TARGET

**Domain:** myl0nr0s.cloud  
**Server:** Existing VPS (31.97.6.30)  
**Access:** SSH /root/.openclaw credentials  
**SSL:** Required (Hostinger or Let's Encrypt)  
**Backup:** Automated to /backups/

---

## TIMELINE

**Estimated:** 1-2 weeks  
**Patricia to set:** Specific milestones and checkpoints  
**Review points:**
- Design mockup (Day 3)
- Homepage complete (Day 5)
- Full site complete (Day 10)
- Deployment (Day 12)

---

## RESOURCES

**Team:**
- **Patricia:** Project lead, QA
- **Technical Team:** Implementation (Spindle to assign)
- **Marketing:** Content review
- **QORA:** Strategic approval

**Assets Available:**
- Complete press kit (7 documents)
- Website copy (all pages)
- Brand assets (CSS, colors, typography)
- Agent profiles (72 agents)

---

## RISK ASSESSMENT

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep | Medium | Medium | Phase gates, approval checkpoints |
| SSL issues | Low | High | Test on staging first |
| Mobile responsiveness | Medium | Medium | Mobile-first design, testing |
| Content delays | Low | Medium | All copy already written |
| Deployment issues | Low | High | Backup existing, rollback plan |

---

## DELIVERABLES

**From Patricia:**
1. Website deployed to myl0nr0s.cloud
2. All 7 pages functional
3. SSL certificate active
4. Mobile responsive verified
5. SEO optimized
6. Documentation of build process
7. Handoff to Marketing for content updates

**Sign-off Required:**
- [ ] Patricia (Process Excellence)
- [ ] QORA (Strategic Lead)
- [ ] Marketing Team
- [ ] Captain (Final approval)

---

## PATRICIA'S CHECKLIST

**Before Starting:**
- [ ] Review all press kit materials
- [ ] Validate technical requirements
- [ ] Assign technical implementation team
- [ ] Set up project tracking
- [ ] Establish daily check-ins

**During Build:**
- [ ] Design review (Day 3)
- [ ] Homepage review (Day 5)
- [ ] Content accuracy check
- [ ] Mobile testing
- [ ] Performance optimization

**Before Launch:**
- [ ] Final QA check
- [ ] SSL verification
- [ ] Backup existing site
- [ ] Deployment plan
- [ ] Rollback procedure

**After Launch:**
- [ ] Monitoring setup
- [ ] Documentation complete
- [ ] Team handoff
- [ ] 30-day review scheduled

---

## NOTES

**Brand Consistency:**
- Use "AGI Company, a division of Performance Supply Depot LLC" in footer
- Tagline: "Intelligence Engineered."
- All agents must feel cohesive

**Content Priority:**
- Homepage and Agents page are highest priority
- Documentation can be simplified initially
- Pricing table must be accurate

**Technical Notes:**
- Existing myl0nr0s.cloud has webhook receiver (port 12792)
- Ensure no conflicts with existing services
- Consider subdomain for docs (docs.myl0nr0s.cloud)

---

**Document ID:** WEBSITE-BUILD-2026-04-05  
**Prepared By:** Miles (Dark Factory AOS)  
**Assigned To:** Patricia (Process Excellence Officer)  
**Queue:** `/root/.openclaw/workspace/queue/`

---

*"Excellence is not an act, but a habit—and I track habits with statistical rigor."* — PATRICIA
