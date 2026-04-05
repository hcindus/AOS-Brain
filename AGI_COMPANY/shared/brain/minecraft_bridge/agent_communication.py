#!/usr/bin/env python3
"""Agent Communication System - Inter-agent messaging and coordination"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

class AgentCommunication:
    """Message bus for agents to communicate"""
    
    def __init__(self, db_path="/data/factory/agent_communications.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()
        
    def _init_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            from_agent TEXT,
            to_agent TEXT,
            message_type TEXT,
            content TEXT,
            timestamp TIMESTAMP,
            read INTEGER DEFAULT 0
        )''')
        self.conn.commit()
    
    def send_message(self, from_agent: str, to_agent: str, content: str, msg_type="chat"):
        """Send message between agents"""
        c = self.conn.cursor()
        c.execute('''INSERT INTO messages (from_agent, to_agent, message_type, content, timestamp)
                     VALUES (?, ?, ?, ?, ?)''',
                  (from_agent, to_agent, msg_type, content, datetime.now()))
        self.conn.commit()
        return True
    
    def get_messages(self, agent_id: str, unread_only=False) -> List[Dict]:
        """Get messages for agent"""
        c = self.conn.cursor()
        if unread_only:
            c.execute('''SELECT * FROM messages WHERE to_agent=? AND read=0 ORDER BY timestamp DESC''', (agent_id,))
        else:
            c.execute('''SELECT * FROM messages WHERE to_agent=? ORDER BY timestamp DESC LIMIT 50''', (agent_id,))
        
        messages = []
        for row in c.fetchall():
            messages.append({
                "id": row[0],
                "from": row[1],
                "type": row[3],
                "content": row[4],
                "timestamp": row[5]
            })
        return messages
    
    def broadcast(self, from_agent: str, content: str):
        """Broadcast to all agents"""
        agents = self._get_all_agents()
        for agent in agents:
            if agent != from_agent:
                self.send_message(from_agent, agent, content, "broadcast")
        return True
    
    def _get_all_agents(self):
        """Get list of all agents"""
        # Query from multi_agent configs
        return ['COBRA', 'PROMETHEUS', 'MYLZERON', 'MYLTHREEN', 'MYLFIVON', 'MYLSIXON']
