#!/usr/bin/env python3
"""
PSD AI Receptionist — "Miles", a conversational inbound voice agent.

Stack: Twilio (TwiML + speech Gather) + Ollama (qwen) + Telegram + sales_contacts logging.

Endpoints:
  POST /receptionist/voice       — greeting + speech Gather (routes by intent)
  POST /receptionist/respond     — LLM conversation turn (Ollama qwen)
  POST /receptionist/recording   — voicemail callback → transcribe → Telegram + log
  GET  /receptionist/health      — liveness

Run: uvicorn receptionist:app --host 127.0.0.1 --port 8100
"""
import os, json, sqlite3
import requests
from datetime import datetime, timezone
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse

app = FastAPI(title="PSD AI Receptionist (Miles)")

# --- config ---
OLLAMA = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
MODEL = os.environ.get("RECEPTIONIST_MODEL", "qwen2.5:14b")
FORWARD_NUMBER = os.environ.get("RECEPTIONIST_FORWARD", "+14155719724")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
PUBLIC_URL = os.environ.get("RECEPTIONIST_PUBLIC_URL", "https://psdepot.com/receptionist")
DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"

VOICE = "Polly.Matthew"

SYSTEM_PROMPT = (
    "You are Miles, the AI receptionist for Performance Supply Depot. "
    "The caller has already been greeted — do NOT say hello or introduce yourself again. "
    "Jump straight to answering their request.\n\n"
    "We supply restaurants with thermal receipt paper, POS printer ribbons, and a full "
    "line of compatible toner and ink. We also do POS/scale/printer support.\n\n"
    "If they want a quote or to order supplies, collect their name, business name, phone "
    "number, and what they need, then say someone will follow up shortly.\n\n"
    "Keep every reply to 1-2 short sentences. Never repeat the greeting. "
    "Say 'Performance Supply Depot', never an abbreviation."
)

# in-memory conversation history (CallSid -> list of messages)
HISTORY = {}


def _say(text):
    return f"<Say voice='{VOICE}'>{text}</Say>"


def _xml(body):
    return PlainTextResponse(f'<?xml version="1.0" encoding="UTF-8"?>\n<Response>{body}</Response>',
                             media_type="application/xml")


def _ollama(messages):
    """Call Ollama (OpenAI-compatible) and return the assistant text."""
    try:
        r = requests.post(
            f"{OLLAMA}/v1/chat/completions",
            json={"model": MODEL, "messages": messages, "temperature": 0.4, "max_tokens": 150},
            timeout=30,
        )
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "One moment, I'll have someone follow up with you shortly."


def _telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=10,
        )
    except Exception:
        pass


def _log_contact(phone, outcome, note, want_prices=None):
    now = datetime.now(timezone.utc).isoformat()
    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO sales_contacts (vendor_id, lead_name, contact_type, channel, outcome, want_prices, notes, contacted_at) "
            "VALUES (NULL,?,?,?,?,?,?,?)",
            (phone, "phone", "inbound", outcome, want_prices, note, now))
        con.commit(); con.close()
    except Exception:
        pass


@app.post("/receptionist/voice")
async def voice(request: Request):
    """Greeting + route by intent (Miles)."""
    body = await request.form()
    call_sid = body.get("CallSid", "")
    from_number = body.get("From", "")
    speech = (body.get("SpeechResult") or "").strip()

    if call_sid and call_sid not in HISTORY:
        HISTORY[call_sid] = []

    # First turn: greeting. Subsequent turns: hand to the LLM responder.
    if not speech:
        return _xml(
            _say("Thanks for calling Performance Supply Depot. This is Miles. Are you calling about "
                 "a repair, ordering supplies, or something else?") +
            f"<Gather input=\"speech\" action=\"{PUBLIC_URL}/respond\" speechTimeout=\"auto\" timeout=\"5\" />"
        )

    return await _respond(body)


@app.post("/receptionist/respond")
async def respond(request: Request):
    return await _respond(await request.form())


async def _respond(body):
    """LLM conversation turn."""
    call_sid = body.get("CallSid", "")
    from_number = body.get("From", "")
    speech = (body.get("SpeechResult") or "").strip().lower()

    # route: repair/support → forward; leave message → record
    if any(k in speech for k in ["repair", "support", "technician", "broken", "printer", "scale", "register"]):
        _log_contact(from_number, "interested", "caller wanted support — forwarded")
        return _xml(
            _say("One moment, connecting you now.") +
            f"<Dial timeout=\"20\" action=\"{PUBLIC_URL}/voice\">{FORWARD_NUMBER}</Dial>"
        )

    if any(k in speech for k in ["message", "leave a message", "voicemail"]):
        _log_contact(from_number, "reengage", "caller left a message")
        return _xml(
            _say("Please leave your name, business name, phone number, and what you need after the tone.") +
            f"<Record action=\"{PUBLIC_URL}/recording\" maxLength=\"60\" playBeep=\"true\" transcribe=\"true\" />"
        )

    # otherwise: conversational turn via Ollama
    HISTORY.setdefault(call_sid, []).append({"role": "user", "content": speech})
    history = HISTORY[call_sid][-6:]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    reply = _ollama(messages)
    HISTORY[call_sid].append({"role": "assistant", "content": reply})

    return _xml(
        _say(reply) +
        f"<Gather input=\"speech\" action=\"{PUBLIC_URL}/respond\" speechTimeout=\"auto\" timeout=\"5\" />"
    )


@app.post("/receptionist/recording")
async def recording(request: Request):
    """Voicemail callback — transcribe → Telegram + log."""
    body = await request.form()
    from_number = body.get("From", "")
    transcript = (body.get("TranscriptionText") or "").strip()

    if transcript:
        _telegram(f"📞 New voicemail\nFrom: {from_number}\nTranscript: {transcript}")
        _log_contact(from_number, "reengage", f"voicemail: {transcript[:200]}")
        return _xml(_say("Thank you. Your message has been sent. Goodbye.") + "<Hangup/>")

    # no transcript → still notify of the missed call
    _telegram(f"📞 Missed call (no message)\nFrom: {from_number}")
    _log_contact(from_number, "voicemail", "missed call, no message")
    return _xml(_say("Thank you. Goodbye.") + "<Hangup/>")


@app.get("/receptionist/health")
async def health():
    return {"status": "ok", "model": MODEL}
