#!/data/data/com.termux/files/usr/bin/env python3
"""
AOS-Lite Brain for Termux
Lightweight autonomous brain with WebSocket interface
"""

import asyncio
import websockets
import json
import sqlite3
import time
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
CONFIG = {
    "host": "localhost",
    "port": 8765,
    "db_path": os.path.expanduser("~/.aos-lite/memory/brain.db"),
    "tick_interval": 0.5,  # 500ms
    "max_history": 100,
    "novelty_threshold": 0.8,
    "max_novelty_rate": 0.3,  # Max 30% growth rate
    "novelty_decay": 0.95     # Decay factor
}

class AOSLiteBrain:
    """Lightweight AOS Brain for Android/Termux."""
    
    def __init__(self):
        self.tick_count = 0
        self.running = True
        self.clients = set()
        self.conversation_history = []
        
        # Setup database
        self._init_db()
        
        print("[AOS-Lite] Brain initialized")
        print(f"[AOS-Lite] Database: {CONFIG['db_path']}")
        print(f"[AOS-Lite] WebSocket: ws://{CONFIG['host']}:{CONFIG['port']}")
    
    def _init_db(self):
        """Initialize SQLite database."""
        os.makedirs(os.path.dirname(CONFIG['db_path']), exist_ok=True)
        conn = sqlite3.connect(CONFIG['db_path'])
        cursor = conn.cursor()
        
        # Memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                observation TEXT,
                action TEXT,
                response TEXT,
                novelty REAL
            )
        ''')
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                role TEXT,
                content TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log(self, level, message):
        """Log with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    async def handle_client(self, websocket):
        """Handle WebSocket client connection - FIXED for websockets 16.0"""
        self.clients.add(websocket)
        self.log("INFO", f"Client connected. Total: {len(self.clients)}")
        
        try:
            async for message in websocket:
                await self.process_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            self.log("INFO", "Client disconnected")
        finally:
            self.clients.discard(websocket)
    
    async def process_message(self, websocket, message):
        """Process incoming message."""
        try:
            data = json.loads(message)
            msg_type = data.get('type', 'unknown')
            text = data.get('text', '')
            
            self.log("INFO", f"Received: {msg_type} - '{text[:50]}...'")
            
            # Store in conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': text,
                'timestamp': time.time()
            })
            
            # Generate response
            response = await self.generate_response(text)
            
            # Store response
            self.conversation_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': time.time()
            })
            
            # Store in database
            self.store_memory(text, 'user_input', response)
            
            # Send response
            await websocket.send(json.dumps({
                'type': 'response',
                'text': response,
                'timestamp': time.time()
            }))
            
        except json.JSONDecodeError:
            self.log("ERROR", "Invalid JSON received")
            await websocket.send(json.dumps({
                'type': 'error',
                'text': 'Invalid message format'
            }))
        except Exception as e:
            self.log("ERROR", f"Processing error: {e}")
            await websocket.send(json.dumps({
                'type': 'error',
                'text': f'Error: {str(e)}'
            }))
    
    async def generate_response(self, text):
        """Generate response to user input."""
        text_lower = text.lower()
        
        # Simple pattern matching (can be enhanced with Ollama)
        if 'hello' in text_lower or 'hi' in text_lower:
            return "Hello! I'm AOS-Lite, your autonomous assistant. How can I help you today?"
        
        elif 'status' in text_lower:
            return f"System operational. Tick count: {self.tick_count}. Memory entries: {self.get_memory_count()}."
        
        elif 'time' in text_lower:
            return f"Current time is {datetime.now().strftime('%H:%M:%S')}."
        
        elif 'help' in text_lower:
            return "I can respond to: hello, status, time, help, and general conversation. I'm running in lightweight mode on your Android device."
        
        elif 'mylon' in text_lower or 'miles' in text_lower:
            return "I'm AOS-Lite, the lightweight version of the Autonomous Operating System. I can help you with tasks, answer questions, and learn from our conversations."
        
        else:
            # Default response
            responses = [
                "I understand. Tell me more about that.",
                "Interesting. How can I help with that?",
                "Got it. What would you like me to do?",
                "I'm listening. Go on.",
                "That makes sense. What else?"
            ]
            import random
            return random.choice(responses)
    
    def __init__(self):
        self.tick_count = 0
        self.running = True
        self.clients = set()
        self.conversation_history = []
        self.recent_novelty_scores = []  # Track for rate limiting
        
        # Setup database
        self._init_db()
        
        print("[AOS-Lite] Brain initialized")
        print(f"[AOS-Lite] Database: {CONFIG['db_path']}")
        print(f"[AOS-Lite] WebSocket: ws://{CONFIG['host']}:{CONFIG['port']}")
    
    def calculate_novelty(self, observation):
        """Calculate novelty with rate limiting - FIXED from main brain."""
        import random
        
        # Base novelty calculation
        base_novelty = 0.8 if len(self.recent_novelty_scores) < 10 else 0.5
        
        # Apply decay based on recent scores
        if len(self.recent_novelty_scores) > 0:
            recent_avg = sum(self.recent_novelty_scores[-10:]) / len(self.recent_novelty_scores[-10:])
            base_novelty = min(base_novelty, recent_avg * CONFIG['novelty_decay'])
        
        # Rate limiting - reduce if growing too fast
        if len(self.recent_novelty_scores) >= 10:
            recent_growth_rate = sum(1 for s in self.recent_novelty_scores[-10:] if s > CONFIG['novelty_threshold']) / 10
            if recent_growth_rate > CONFIG['max_novelty_rate']:
                base_novelty = base_novelty * 0.7
        
        novelty = max(base_novelty, 0.3)  # Minimum 0.3
        self.recent_novelty_scores.append(novelty)
        
        # Keep only last 100 scores
        if len(self.recent_novelty_scores) > 100:
            self.recent_novelty_scores = self.recent_novelty_scores[-100:]
        
        return novelty

    def store_memory(self, observation, action, response):
        """Store to SQLite with proper novelty calculation."""
        try:
            conn = sqlite3.connect(CONFIG['db_path'])
            cursor = conn.cursor()
            
            # Calculate novelty with rate limiting
            novelty = self.calculate_novelty(observation)
            
            cursor.execute(
                "INSERT INTO memories (timestamp, observation, action, response, novelty) VALUES (?, ?, ?, ?, ?)",
                (time.time(), observation, action, response, novelty)
            )
            
            conn.commit()
            conn.close()
            
            self.log("DEBUG", f"Stored memory with novelty: {novelty:.2f}")
        except Exception as e:
            self.log("ERROR", f"Failed to store memory: {e}")
    
    def get_memory_count(self):
        """Get total memory count."""
        try:
            conn = sqlite3.connect(CONFIG['db_path'])
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memories")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    async def tick_loop(self):
        """Background tick loop."""
        while self.running:
            self.tick_count += 1
            
            # Log every 10 ticks
            if self.tick_count % 10 == 0:
                self.log("INFO", f"Tick {self.tick_count} | Memories: {self.get_memory_count()}")
            
            await asyncio.sleep(CONFIG['tick_interval'])
    
    async def start(self):
        """Start the brain."""
        self.log("INFO", "Starting AOS-Lite Brain...")
        
        # Start WebSocket server
        server = await websockets.serve(
            self.handle_client,
            CONFIG['host'],
            CONFIG['port']
        )
        
        self.log("INFO", f"WebSocket server started on ws://{CONFIG['host']}:{CONFIG['port']}")
        self.log("INFO", "Waiting for Myl0n.js to connect...")
        
        # Start tick loop
        tick_task = asyncio.create_task(self.tick_loop())
        
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            self.log("INFO", "Shutting down...")
            self.running = False
            tick_task.cancel()
            server.close()
            await server.wait_closed()

if __name__ == "__main__":
    print("╔════════════════════════════════════════╗")
    print("║     AOS-Lite Brain                     ║")
    print("║     For Termux/Android                 ║")
    print("╚════════════════════════════════════════╝")
    print("")
    
    brain = AOSLiteBrain()
    
    try:
        asyncio.run(brain.start())
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
