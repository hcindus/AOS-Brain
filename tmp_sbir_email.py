#!/usr/bin/env python3
import sys
sys.path.insert(0, "/root/.openclaw/workspace/skills/email-sender")
from send_email import send_email

subject = "SBIR/STTR Play — Your Registration Checklist & Next Steps (Miles)"

body = """Captain,

Here's exactly what you need to do to unlock government seed funding via DoD SBIR/STTR. I've broken it into what's blocking, what's quick, and what I'm running in the background.

=== WHY THIS MATTERS ===
~$3B in FY26 SBIR seed funding. Phase 1 = $50K-$275K (Navy wearable C2 topic is $200K base + $115K option = $315K). Phase 2 = $750K-$1.8M. Our sharpest fit is C2 data fusion / decision-support software (the "information overload -> synthesized decision" problem), which maps 1:1 to our agent-orchestration + Temporal pipeline stack.

=== YOUR REGISTRATION CHECKLIST (in order) ===

1. DSIP ACCOUNT  [BOTTLENECK - DO FIRST]
   - Go to https://www.dodsbirsttr.mil and register for a DSIP account
   - Free. This unlocks the topic browser, Q&A, and proposal submission.
   - The live topic list is auth-gated (I confirmed 401 without an account), so this is also what unblocks my research.

2. SAM.GOV REGISTRATION  [1-2 WEEKS - START NOW]
   - https://sam.gov -> register your entity
   - Gives you a CAGE Code (unique business identifier required to receive awards)
   - You need your EIN/TIN, bank info, and UEI (Unique Entity ID). UEI comes from SAM itself now (no more DUNS).

3. SBA COMPANY REGISTRY  [QUICK]
   - Register the business at the SBA SBIR company registry
   - Confirms small-business eligibility (under 500 employees, US-owned)

4. FOREIGN RISK EVALUATION  [CHECK]
   - Must be US-owned and operated, no foreign influence (per the BAA). Confirm our corporate structure is clean here.

5. CMMC LEVEL 2  [LATER, AWARD-DEPENDENT]
   - The Navy topic projects CMMC Level 2. Not needed to apply, but plan for it if we pursue award.

=== TIMING ===
- The live Navy wearable C2 topic: OPEN Aug 26 -> DUE Sept 23, 12pm EST.
- xTech prize competition already closed (Aug 17) but repeats on a cadence — worth watching.

=== WHAT I'M DOING IN THE BACKGROUND ===
- Delegating topic research to Beets (Hermes 1st mate): mapping current FY26 DoD SBIR/STTR topics that fit software/AI/autonomy/C2-data-fusion, and drafting a 10-page Navy-format Phase 1 positioning template so we can move fast once you have DSIP + SAM.

Send me a note when DSIP and SAM are done and I'll pull the live topic list and shortlist the top 3 with TPO contacts.

— Miles
"""

html_body = body.replace("\n", "<br>\n")

r = send_email(
    to="Antonio.hudnall@gmail.com",
    subject=subject,
    body=body,
    html_body=f"<html><body style='font-family:sans-serif;font-size:14px;color:#222'>{html_body}</body></html>",
)
print(r)
