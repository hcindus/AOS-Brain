#!/usr/bin/env python3
"""
Twilio Voice Integration for AI Qualifier
SOP-044: AI Qualifying - Phase 2

Handles voice calls, TTS, transcription, and call flow
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Optional, List, Callable
from functools import wraps

from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TwilioVoice")


class TwilioVoiceIntegration:
    """
    Twilio Voice Integration for AI Sales Calls
    
    Features:
    - Outbound call initiation
    - Real-time TTS (ElevenLabs/Mort_II)
    - Speech-to-text transcription
    - Conversation state management
    - Call recording and logging
    """
    
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_FROM_NUMBER")
        
        self.webhook_url = "https://sales-automation.psdepot.com/voice"
        self.active_calls = {}
        
        # Voice configuration (Adam from TOOLS.md)
        self.voice_config = {
            "provider": "elevenlabs",
            "voice_id": "adam",  # Deep, energetic, professional
            "model": "eleven_multilingual_v2",
            "stability": 0.5,
            "similarity_boost": 0.75
        }
        
    def initiate_call(self, to_number: str, lead_id: str, 
                       context: Optional[Dict] = None) -> Dict:
        """
        Initiate outbound call to prospect
        
        Returns call SID for tracking
        """
        logger.info(f"Initiating call to {to_number} for lead {lead_id}")
        
        # Would use Twilio REST API
        # from twilio.rest import Client
        # client = Client(self.account_sid, self.auth_token)
        # call = client.calls.create(
        #     to=to_number,
        #     from_=self.from_number,
        #     url=f"{self.webhook_url}/incoming",
        #     status_callback=f"{self.webhook_url}/status",
        #     record=True
        # )
        
        # Mock for now
        call_sid = f"CA{hash(to_number) % 10000000000:010d}"
        
        self.active_calls[call_sid] = {
            "lead_id": lead_id,
            "to_number": to_number,
            "started_at": datetime.now().isoformat(),
            "status": "initiated",
            "context": context or {},
            "transcript": [],
            "bant": {}
        }
        
        return {
            "call_sid": call_sid,
            "status": "initiated",
            "to": to_number
        }
    
    def generate_twiml(self, message: str, gather: bool = True) -> str:
        """
        Generate TwiML for call response
        
        Uses Stream for real-time audio or Say for pre-recorded
        """
        if gather:
            # Gather speech input after speaking
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{message}</Say>
    <Gather input="speech" action="/voice/process-speech" timeout="5" speechTimeout="auto">
        <Say>I'm listening...</Say>
    </Gather>
</Response>"""
        else:
            # Just speak, no input
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{message}</Say>
    <Hangup/>
</Response>"""
    
    def handle_incoming_call(self, request: web.Request) -> web.Response:
        """
        Handle incoming webhook from Twilio
        
        Triggered when call connects
        """
        data = request.post()
        call_sid = data.get("CallSid")
        
        logger.info(f"Call connected: {call_sid}")
        
        # Get call context
        call_data = self.active_calls.get(call_sid, {})
        lead_id = call_data.get("lead_id")
        
        # Opening script from SOP-044
        opening = """Hi, this is Miles from Performance Supply Depot. 
I hope I'm not catching you at a bad time?"""
        
        twiml = self.generate_twiml(opening, gather=True)
        
        return web.Response(text=twiml, content_type="text/xml")
    
    def handle_speech_input(self, request: web.Request) -> web.Response:
        """
        Process speech input from prospect
        
        Triggered after Gather completes
        """
        data = request.post()
        call_sid = data.get("CallSid")
        speech_result = data.get("SpeechResult", "")
        confidence = data.get("Confidence", 0)
        
        logger.info(f"Speech input: {speech_result[:50]}...")
        
        # Get call state
        call_data = self.active_calls.get(call_sid, {})
        
        # Add to transcript
        call_data["transcript"].append({
            "speaker": "prospect",
            "text": speech_result,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })
        
        # Determine next step in conversation flow
        next_response = self._determine_response(call_sid, speech_result)
        
        twiml = self.generate_twiml(next_response, gather=True)
        
        return web.Response(text=twiml, content_type="text/xml")
    
    def _determine_response(self, call_sid: str, prospect_input: str) -> str:
        """
        Determine AI response based on conversation state
        
        This integrates with the Qualifier Agent from SOP-044
        """
        call_data = self.active_calls.get(call_sid, {})
        transcript = call_data.get("transcript", [])
        
        # Simple state machine
        if len(transcript) == 1:
            # First response - permission check
            return """Great! You just popped up on my calendar. 
Do you have 2 minutes for a quick conversation about your supply needs?"""
            
        elif len(transcript) == 2:
            # Discovery - business type
            return "What type of business are you running?"
            
        elif len(transcript) == 3:
            # Discovery - locations/budget
            return "How many locations? And what's your monthly spend on supplies?"
            
        elif len(transcript) == 4:
            # Authority check
            return "Are you the person who handles purchasing, or should I talk to someone else?"
            
        elif len(transcript) == 5:
            # Timeline
            return "When do you typically need to restock? Any urgency here?"
            
        elif len(transcript) == 6:
            # Qualification complete - attempt booking
            return """Perfect! Based on what you told me, I think we can definitely help. 
Let me get you scheduled with our team. When's a good time this week?"""
            
        else:
            # Continue conversation or wrap up
            return "I understand. Let me send you some information via email. What's the best email for you?"
    
    def handle_call_status(self, request: web.Request) -> web.Response:
        """
        Handle call status callbacks
        
        Triggered on call end, recording available, etc.
        """
        data = request.post()
        call_sid = data.get("CallSid")
        status = data.get("CallStatus")
        recording_url = data.get("RecordingUrl")
        
        logger.info(f"Call status: {call_sid} = {status}")
        
        if status == "completed":
            call_data = self.active_calls.get(call_sid, {})
            
            # Save final transcript
            self._save_transcript(call_sid, call_data)
            
            # Trigger follow-up if needed
            if recording_url:
                self._process_recording(call_sid, recording_url)
        
        return web.Response(text="OK")
    
    def _save_transcript(self, call_sid: str, call_data: Dict):
        """Save call transcript to disk"""
        output_path = f"/root/.openclaw/workspace/psd/sales-automation/call_logs/{call_sid}.json"
        
        with open(output_path, 'w') as f:
            json.dump(call_data, f, indent=2)
            
        logger.info(f"Saved transcript: {output_path}")
    
    def _process_recording(self, call_sid: str, recording_url: str):
        """Process call recording"""
        logger.info(f"Processing recording: {recording_url}")
        
        # Would download and transcribe with Whisper
        # For detailed analysis
    
    def get_call_quality_metrics(self, call_sid: str) -> Dict:
        """
        Get quality metrics for a call
        """
        call_data = self.active_calls.get(call_sid, {})
        transcript = call_data.get("transcript", [])
        
        if not transcript:
            return {}
        
        avg_confidence = sum(t.get("confidence", 0) for t in transcript) / len(transcript)
        
        return {
            "call_sid": call_sid,
            "duration_seconds": None,  # Would calculate from timestamps
            "turns": len(transcript),
            "avg_confidence": avg_confidence,
            "completed": len(transcript) >= 6
        }


class VoiceWebhookServer:
    """
    HTTP server for Twilio webhooks
    """
    
    def __init__(self, port=8086):
        self.port = port
        self.voice = TwilioVoiceIntegration()
        self.app = web.Application()
        self._setup_routes()
    
    def _setup_routes(self):
        self.app.router.add_post('/voice/incoming', self.voice.handle_incoming_call)
        self.app.router.add_post('/voice/process-speech', self.voice.handle_speech_input)
        self.app.router.add_post('/voice/status', self.voice.handle_call_status)
    
    def run(self):
        logger.info(f"Voice webhook server on port {self.port}")
        web.run_app(self.app, port=self.port)


def main():
    """CLI entry point"""
    # Start webhook server
    server = VoiceWebhookServer()
    server.run()


if __name__ == "__main__":
    main()
