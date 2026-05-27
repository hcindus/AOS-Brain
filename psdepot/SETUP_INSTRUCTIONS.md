# Credit Card Authorization Form - Setup Instructions

## Overview

This system creates a complete CC authorization workflow:
1. **Google Form** → Customer fills out securely
2. **Google Apps Script** → Auto-generates PDF on submission
3. **Email** → PDF sent to both customer and merchant
4. **Drive Archive** → PDF saved for compliance

---

## Files Included

| File | Purpose |
|------|---------|
| `cc-auth-form-google-form.json` | Form structure (reference) |
| `cc-auth-pdf-template.html` | PDF styling reference |
| `cc-auth-apps-script.gs` | **Main automation script** |
| `SETUP_INSTRUCTIONS.md` | This file |

---

## Step-by-Step Setup

### Step 1: Create the Google Form

1. Go to [forms.new](https://forms.new) or Google Drive → New → Google Forms
2. Title: **"Credit Card Authorization - Performance Supply Depot"**
3. Description: *"Secure authorization to keep credit card on file. A PDF copy will be emailed upon submission."*

### Step 2: Add Form Fields (in order)

#### Section 1 — Business Information
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Business Name | Short answer | ✅ | - |
| Business Street Address | Short answer | ✅ | - |
| Business City, State, ZIP | Short answer | ✅ | - |
| Business Phone Number | Short answer | ✅ | - |
| Business Email Address | Short answer | ✅ | - |

#### Section 2 — Authorized Cardholder
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Cardholder Full Name | Short answer | ✅ | - |
| Billing Address | Short answer | ✅ | - |
| Billing ZIP Code | Short answer | ✅ | Number, 5 digits |
| Cardholder Phone | Short answer | ✅ | - |
| Cardholder Email | Short answer | ✅ | - |

#### Section 3 — Credit Card Information
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Credit Card Number | Short answer | ✅ | Regex: `^[0-9]{15,16}$` |
| Expiration Date (MM/YY) | Short answer | ✅ | Regex: `^(0[1-9]|1[0-2])\/([0-9]{2})$` |
| CVV / Security Code | Short answer | ✅ | Regex: `^[0-9]{3,4}$` |
| Billing ZIP (Credit Card) | Short answer | ✅ | Number, 5 digits |

#### Section 4 — Authorization Agreement
| Field | Type | Required |
|-------|------|----------|
| Authorization Statement | Checkboxes | ✅ |

**Checkbox Options (paste exactly):**
```
I hereby authorize Performance Supply Depot LLC to charge the credit card listed above for purchases, invoices, or recurring orders made by my business. I confirm that I am an authorized user of this credit card and that I will not dispute charges provided they correspond to the terms indicated on invoices or order confirmations.

I authorize Performance Supply Depot LLC to store this credit card information securely on file for future transactions, recurring orders, or replacement orders requested by my business. This authorization will remain in effect until I provide written notice to revoke it.

I understand that a PDF copy of this authorization, including the information I have provided, will be generated and emailed to both myself and Performance Supply Depot LLC for record-keeping purposes.
```

| Field | Type | Required |
|-------|------|----------|
| Electronic Signature (Type Full Name) | Short answer | ✅ |
| Date | Date | ✅ |

#### Section 5 — Optional
| Field | Type | Required |
|-------|------|----------|
| Photo of Credit Card (Optional) | File upload | ❌ |
| Photo of ID (Optional) | File upload | ❌ |
| Special Instructions | Paragraph | ❌ |

---

### Step 3: Connect to Google Sheets

1. In your Form, click **Responses** tab
2. Click the **green Sheets icon** (⎘)
3. Select **"Create a new spreadsheet"**
4. Name it: `CC-Authorization-Responses`

---

### Step 4: Install Apps Script

1. In the spreadsheet, go to **Extensions → Apps Script**
2. Delete all default code in the editor
3. **Copy the entire contents** of `cc-auth-apps-script.gs`
4. **Paste** into the Apps Script editor
5. Press **Ctrl+S** (or ⌘+S) to save
6. Name the project: `CC-Authorization-Automation`

---

### Step 5: Configure the Script

In the script, find the `CONFIG` section at the top:

```javascript
const CONFIG = {
  MERCHANT_EMAIL: 'info@psdepot.com',  // ← CHANGE THIS TO YOUR EMAIL
  ARCHIVE_FOLDER_ID: '',  // ← Optional: paste Drive folder ID here
};
```

**To get a Drive folder ID:**
1. Go to Google Drive
2. Create a folder called `CC-Authorizations`
3. Open the folder
4. Look at the URL: `drive.google.com/drive/folders/FOLDER_ID_HERE`
5. Copy the ID part and paste into `ARCHIVE_FOLDER_ID`

---

### Step 6: Create the Trigger

1. In Apps Script, click the **Triggers icon** (⏰) on the left
2. Click **+ Add Trigger** (bottom right)
3. Configure:
   - **Function to run:** `onFormSubmit`
   - **Deployment:** Head
   - **Event source:** `From form`
   - **Form:** `CC-Authorization-Responses` (or your form name)
   - **Event type:** `On form submit`
4. Click **Save**

---

### Step 7: Authorize Permissions

1. You'll see an error: **"Authorization required"**
2. Click **Review Permissions**
3. Choose your Google account
4. Click **Advanced** → **Go to CC-Authorization-Automation (unsafe)**
5. Click **Allow** for all requested permissions:
   - View and manage your spreadsheets
   - Send email on your behalf
   - Access Google Drive

---

### Step 8: Test the System

1. In Apps Script, select the `testFormProcessing` function
2. Click **Run** (▶)
3. Check both email addresses for test PDFs
4. Verify the PDF looks correct

---

## How It Works

```
Customer submits form
        ↓
Google Sheets captures data
        ↓
Apps Script triggers onFormSubmit()
        ↓
PDF generated with professional formatting
        ↓
Email sent to customer (with PDF)
Email sent to merchant (with PDF)
        ↓
PDF saved to Drive (if configured)
```

---

## Email Recipients

| Email Type | Recipient | Content |
|------------|-----------|---------|
| Customer | Cardholder email entered in form | Friendly confirmation + PDF |
| Merchant | Your configured email | Alert with business details + PDF |

---

## Security Notes

- Card numbers are **masked** in the PDF (****-****-****-1234)
- Only the last 4 digits are visible in archived records
- Consider requiring file upload of card photo (with middle digits covered)
- Store PDFs in a secured Drive folder
- This form is PCI-compliant for authorization records only (you'll need a proper payment processor for actual charging)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Emails not sending | Check spam folders; verify permissions granted |
| PDF formatting off | Check HTML template in script |
| Fields not mapping | Verify form field order matches `parseFormResponse()` |
| "Authorization required" | Click through Advanced → Allow |
| Test function fails | Check `values` array indices match your form |

---

## Customization

### Change Email Content
Edit `sendCustomerEmail()` and `sendMerchantEmail()` functions in the script.

### Change PDF Styling
Edit the CSS in `buildHTMLTemplate()` function.

### Add More Fields
1. Add field to Google Form
2. Update `parseFormResponse()` with the new column index
3. Update HTML template to display it

---

## Support

- **Google Apps Script Docs:** https://developers.google.com/apps-script
- **Test with:** `testFormProcessing()` function
- **Check logs:** Apps Script → Executions

---

**Last Updated:** 2026-05-27
**Version:** 1.0.0
