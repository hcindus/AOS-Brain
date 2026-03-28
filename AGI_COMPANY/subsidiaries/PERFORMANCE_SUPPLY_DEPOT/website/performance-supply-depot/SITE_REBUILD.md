# SITE REBUILD - UNIFIED DESIGN
## AGI Company Website Rebuild Documentation

---

## Overview

**Completed:** 2026-03-28  
**Scope:** Unified design across all pages using index.html as template  
**Integration:** Phone login system + Dark Factory documentation

---

## Design System

### Color Palette (CSS Variables)
```css
:root {
    --primary: #1a365d;          /* Dark blue - headers, CTAs */
    --primary-light: #2c5282;     /* Lighter blue - gradients */
    --accent: #ed8936;             /* Orange - buttons, highlights */
    --accent-hover: #dd6b20;       /* Darker orange - hover states */
    --bg-light: #f7fafc;          /* Light gray - page background */
    --bg-dark: #edf2f7;          /* Darker gray - sections */
    --text: #2d3748;              /* Dark gray - body text */
    --text-light: #718096;       /* Light gray - secondary text */
    --white: #ffffff;             /* White - cards, nav */
    --shadow: 0 10px 25px rgba(0,0,0,0.1);
    --radius: 12px;               /* Border radius - cards */
}
```

### Typography
- **Font Family:** `'Segoe UI', system-ui, sans-serif`
- **Hero Headings:** 48px, bold
- **Section Headings:** 36px, bold
- **Body Text:** 16px, regular
- **Small Text:** 14px, light gray

### Components

#### Navigation Bar
```css
nav {
    background: var(--white);
    padding: 15px 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.logo {
    font-size: 24px;
    font-weight: 800;
    color: var(--primary);
}

.logo span { color: var(--accent); }

.nav-links a {
    color: var(--text);
    margin-left: 30px;
    font-weight: 600;
}
```

#### Hero Section
```css
.hero {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: var(--white);
    padding: 140px 20px 100px;
    text-align: center;
    margin-top: 60px;
}
```

#### Buttons
```css
.btn {
    background: var(--accent);
    color: var(--white);
    padding: 15px 30px;
    border-radius: 8px;
    font-weight: 600;
    border: none;
}

.btn:hover { background: var(--accent-hover); }

.btn-secondary {
    background: var(--bg-dark);
    color: var(--text);
}
```

#### Cards
```css
.card {
    background: var(--white);
    padding: 40px;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}
```

#### Footer
```css
footer {
    background: var(--primary);
    color: var(--white);
    padding: 60px 20px 30px;
}
```

---

## Page Structure Template

Every page should follow this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AGI Company - [Page Name]</title>
    <meta name="description" content="[Description]">
    <style>
        /* Use the CSS variables above */
        :root { /* colors */ }
        /* Standard styles from template */
    </style>
</head>
<body>
    <!-- Navigation (same on all pages) -->
    <nav>
        <div class="container">
            <a href="index.html" class="logo">AGI<span>Company</span></a>
            <div class="nav-links">
                <a href="index.html">Home</a>
                <a href="index.html#products">Products</a>
                <a href="index.html#about">About</a>
                <a href="index.html#contact">Contact</a>
                <a href="login.html">Business Login</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <div class="page-hero">
        <h1>[Page Title]</h1>
        <p>[Page Description]</p>
    </div>

    <!-- Main Content -->
    <main>
        <div class="container">
            [Page-specific content]
        </div>
    </main>

    <!-- Footer (same on all pages) -->
    <footer>
        [Standard footer content]
    </footer>
</body>
</html>
```

---

## Pages Rebuilt

### 1. index.html (Home)
- **Status:** ✅ Already unified (reference template)
- **Features:** Hero, products, about, contact sections

### 2. login.html (NEW)
- **Status:** ✅ Created with unified design
- **Features:** 
  - 5-step phone login flow
  - Business lookup by phone
  - Address verification
  - Email collection
  - Product selection
- **Integration:** Links to checkout.html

### 3. checkout.html (REBUILT)
- **Status:** ✅ Rebuilt with unified design
- **Features:**
  - Stripe payment integration
  - Product summary
  - Secure card input
  - Test mode banner
  - Order confirmation
- **Integration:** Receives orders from login.html

---

## File Structure

```
performance-supply-depot/
├── index.html          ✅ Template / Home page
├── login.html          ✅ NEW - Phone login system
├── checkout.html       ✅ REBUILT - Unified design
├── deploy.sh           # Deployment script
└── sales/              # Sales materials
```

---

## Integration Points

### Phone Login → Checkout Flow
1. User enters phone on **login.html**
2. System looks up business → Verifies → Collects address → Gets email
3. User selects AGI agent product
4. Redirects to **checkout.html** with product details
5. Completes Stripe payment
6. Order confirmed

### API Endpoints (Future)
```
POST /api/lookup          - Find business by phone
POST /api/verify-phone    - Verify SMS code
POST /api/verify-address  - Confirm/correct address
POST /api/collect-email   - Save email
POST /api/create-order    - Create order
```

---

## Responsive Breakpoints

| Breakpoint | Width | Behavior |
|------------|-------|----------|
| Mobile | < 640px | Stack nav, single column |
| Tablet | 640-1024px | 2 columns |
| Desktop | > 1024px | Full layout |

---

## To Add New Pages

1. **Copy template** from existing page
2. **Update:**
   - `<title>` tag
   - `<meta name="description">`
   - Hero section content
   - Main content area
3. **Keep consistent:**
   - Navigation bar (exact copy)
   - Footer (exact copy)
   - CSS variables (exact copy)
   - Button styles
   - Card styles
4. **Test:**
   - Navigation links work
   - Mobile responsive
   - Colors match

---

## Commit History

| Commit | Description |
|--------|-------------|
| `177db8b` | Add unified phone login + rebuild checkout |
| Previous | index.html template |

---

## Next Steps

1. **Deploy to Hostinger**
   ```bash
   ./deploy.sh
   ```

2. **Test flow:**
   - Visit myl0nr0s.cloud/login.html
   - Enter test phone
   - Complete all 5 steps
   - Verify checkout page loads

3. **Add more pages:**
   - about.html
   - products.html
   - contact.html
   - documentation.html

4. **API Integration:**
   - Connect to phone_login_web.py backend
   - Enable real business lookup
   - Add SMS sending

---

## Resources

- **Live Site:** https://myl0nr0s.cloud
- **GitHub:** https://github.com/hcindus/aos-brain
- **Support:** miles@myl0nr0s.cloud

---

*All pages now share unified design language. Navigation and footer consistent across site.*
