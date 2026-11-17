#!/usr/bin/env python3
"""
Twilio voice endpoint — serves TwiML for outbound/inbound calls.

Endpoints:
  POST /twiml/outbound  → 60-second consultative pitch
  POST /twiml/inbound   → 8-minute courtesy call-back

Voice: Polly.Matthew (deep, male — closest to our "Adam" brand voice).
Run: uvicorn twilio_voice:app --host 127.0.0.1 --port 8099
"""
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse

app = FastAPI(title="PSD Twilio Voice")

VOICE = "Polly.Matthew"


def say(text):
    return f"<Say voice='{VOICE}'>{text}</Say>"


@app.post("/twiml/outbound")
async def outbound(request: Request):
    """60-second consultative outbound pitch."""
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  {say("Hi, this is Miles from Performance Supply Depot. Did I catch you at a bad time?")}
  <Pause length="1"/>
  {say("Could I grab just a minute of your time?")}
  <Pause length="1"/>
  {say("Great. We supply restaurants with thermal receipt paper and printer ribbons, and we've just added a full line of toner and ink.")}
  <Pause length="1"/>
  {say("Would it be okay if I email you our prices, so you can consider us in the future?")}
  <Pause length="1"/>
  {say("Thank you so much for your time. I hope we can earn your business in the future.")}
</Response>"""
    return PlainTextResponse(xml, media_type="application/xml")


@app.post("/twiml/inbound")
async def inbound(request: Request):
    """8-minute courtesy call-back (we saw a missed call from this number)."""
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  {say("Hi, this is Performance Supply Depot. We saw a missed call from this number.")}
  <Pause length="1"/>
  {say("Is there anything we can do for you, or would you like to order supplies?")}
  <Pause length="1"/>
  {say("We carry thermal paper, printer ribbons, and a full line of toner and ink for restaurants.")}
  <Pause length="1"/>
  {say("Thank you for calling. We'll make sure someone follows up with you.")}
</Response>"""
    return PlainTextResponse(xml, media_type="application/xml")


@app.get("/twiml/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8099)
