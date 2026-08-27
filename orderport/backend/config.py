"""OrderPort configuration — env-driven with sane defaults."""
import os

# ---- Core ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("ORDERPORT_DB", os.path.join(BASE_DIR, "orderport.db"))
PORT = int(os.environ.get("ORDERPORT_PORT", "8088"))

# ---- Domain / URL ----
PUBLIC_BASE_URL = os.environ.get("ORDERPORT_BASE_URL", "https://psdepot.com")

# ---- Revenue split (basis points) ----
COMPANY_SHARE_BPS = int(os.environ.get("COMPANY_SHARE_BPS", "1000"))  # 10%
REP_SHARE_BPS = int(os.environ.get("REP_SHARE_BPS", "500"))           # 5%
# remaining = business (85%)

# ---- Stripe ----
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

# ---- Email (Hostinger SMTP) ----
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.hostinger.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "miles@myl0nr0s.cloud")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", "Performance Supply Depot <miles@myl0nr0s.cloud>")

# ---- Twilio (SMS) ----
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM = os.environ.get("TWILIO_FROM", "")

# ---- Auth ----
SECRET_KEY = os.environ.get("ORDERPORT_SECRET", "change-me-in-production")
TOKEN_TTL_HOURS = int(os.environ.get("ORDERPORT_TOKEN_TTL_HOURS", "72"))
