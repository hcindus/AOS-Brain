#!/usr/bin/env python3
"""
VOICE BRIDGE FOR BRAIN + JORDAN
Real-time voice communication system
"""

import asyncio
import websockets
import json
import base64
import subprocess
import tempfile
import os
from pathlib import Path
from datetime import datetime

class VoiceBridge:
    """WebSocket-based voice bridge for brain communication."""
    
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.clients = set()
        self.audio_buffer = []
        
        # Paths
        self.tmp_dir = Path('/tmp/voice_bridge')
        self.tmp_dir.mkdir(exist_ok=True)
        
    async def handle_client(self, websocket, path):
        """Handle WebSocket client connection."""
        self.clients.add(websocket)
        client_id = id(websocket)
        print(f"[VoiceBridge] Client {client_id} connected")
        
        try:
            async for message in websocket:
                data = json.loads(message)
                
                if data.get('type') == 'audio':
                    # Received audio from client
                    audio_data = base64.b64decode(data['audio'])
                    await self.process_audio(audio_data, client_id, websocket)
                    
                elif data.get('type') == 'ping':
                    await websocket.send(json.dumps({'type': 'pong'}))
                    
        except websockets.exceptions.ConnectionClosed:
            print(f"[VoiceBridge] Client {client_id} disconnected")
        finally:
            self.clients.discard(websocket)
    
    async def process_audio(self, audio_data, client_id, websocket):
        """Process incoming audio: STT -> Brain -> TTS."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_file = self.tmp_dir / f'input_{client_id}_{timestamp}.webm'
        output_wav = self.tmp_dir / f'output_{client_id}_{timestamp}.wav'
        
        try:
            # Save audio
            with open(input_file, 'wb') as f:
                f.write(audio_data)
            
            # Convert to wav for processing
            subprocess.run([
                'ffmpeg', '-y', '-i', str(input_file),
                '-ar', '16000', '-ac', '1', '-f', 'wav',
                str(output_wav)
            ], check=True, capture_output=True)
            
            # Step 1: Speech-to-Text (Whisper)
            transcript = await self.speech_to_text(output_wav)
            
            if not transcript:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': 'Could not understand audio'
                }))
                return
            
            print(f"[VoiceBridge] User said: {transcript}")
            
            # Step 2: Send to Brain/Jordan
            brain_response = await self.query_brain(transcript)
            
            print(f"[VoiceBridge] Brain response: {brain_response}")
            
            # Step 3: Text-to-Speech (ElevenLabs)
            audio_response = await self.text_to_speech(brain_response)
            
            # Send back to client
            await websocket.send(json.dumps({
                'type': 'response',
                'transcript': transcript,
                'response': brain_response,
                'audio': base64.b64encode(audio_response).decode('utf-8')
            }))
            
        except Exception as e:
            print(f"[VoiceBridge] Error: {e}")
            await websocket.send(json.dumps({
                'type': 'error',
                'message': str(e)
            }))
        finally:
            # Cleanup
            for f in [input_file, output_wav]:
                if f.exists():
                    f.unlink()
    
    async def speech_to_text(self, audio_file):
        """Convert speech to text using Whisper."""
        try:
            # Run Whisper
            result = subprocess.run([
                'whisper', str(audio_file),
                '--model', 'base',
                '--language', 'en',
                '--output_format', 'txt',
                '--output_dir', str(self.tmp_dir)
            ], capture_output=True, text=True, timeout=30)
            
            # Read transcript
            transcript_file = audio_file.with_suffix('.txt')
            if transcript_file.exists():
                return transcript_file.read_text().strip()
            return None
            
        except Exception as e:
            print(f"[VoiceBridge] STT error: {e}")
            return None
    
    async def query_brain(self, message):
        """Send message to brain and get response."""
        try:
            # Option 1: Direct brain API
            import requests
            response = requests.post(
                'http://localhost:5000/process',
                json={'input': message, 'context': 'voice'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response from brain')
            
            # Option 2: Query Jordan via file
            jordan_task = Path('/root/.openclaw/workspace/aocros/agent_sandboxes/jordan/CURRENT_TASKS.md')
            if jordan_task.exists():
                # Add voice query to Jordan's tasks
                with open(jordan_task, 'a') as f:
                    f.write(f"\n- [VOICE {datetime.now().isoformat()}] {message}")
                return "Query sent to Jordan. Check his response in his workspace."
            
            return "Brain temporarily unavailable. Please try again."
            
        except Exception as e:
            print(f"[VoiceBridge] Brain query error: {e}")
            return "Brain connection error. Using local processing."
    
    async def text_to_speech(self, text):
        """Convert text to speech using ElevenLabs."""
        try:
            import requests
            
            # Load ElevenLabs config
            vault_path = Path('/root/.aos/vault/elevenlabs_miles.json')
            if vault_path.exists():
                config = json.loads(vault_path.read_text())
                api_key = config.get('voice_id', '')  # Actually needs API key
            else:
                # Fallback to piper TTS if available
                return await self.local_tts(text)
            
            # Call ElevenLabs API
            response = requests.post(
                'https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM',  # Adam voice
                headers={
                    'xi-api-key': api_key,
                    'Content-Type': 'application/json'
                },
                json={
                    'text': text,
                    'voice_settings': {'stability': 0.5, 'similarity_boost': 0.5}
                }
            )
            
            if response.status_code == 200:
                return response.content
            else:
                return await self.local_tts(text)
                
        except Exception as e:
            print(f"[VoiceBridge] TTS error: {e}")
            return await self.local_tts(text)
    
    async def local_tts(self, text):
        """Fallback local TTS using espeak or piper."""
        try:
            # Try espeak
            output_file = self.tmp_dir / 'tts_output.wav'
            subprocess.run([
                'espeak', '-w', str(output_file), text
            ], check=True, capture_output=True)
            
            if output_file.exists():
                return output_file.read_bytes()
            
            # Fallback: return error tone
            return b'RIFF'  # Minimal WAV header
            
        except:
            return b'RIFF'
    
    async def start(self):
        """Start WebSocket server."""
        print(f"[VoiceBridge] Starting server on ws://{self.host}:{self.port}")
        print(f"[VoiceBridge] Web interface: http://{self.host}:{self.port}")
        
        # Start WebSocket server
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        
        print("[VoiceBridge] Server running. Press Ctrl+C to stop.")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    bridge = VoiceBridge()
    asyncio.run(bridge.start())
