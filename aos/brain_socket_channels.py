#!/usr/bin/env python3
"""
Brain Socket Channel Commands v1.0
Channel-based collaboration for AOS

Extends socket interface with Buzz-inspired channel commands:
- channel_create
- channel_join
- channel_post
- channel_history
- channel_members
"""

import time
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib


@dataclass
class ChannelMessage:
    """Message in a channel"""
    message_id: str
    channel_id: str
    sender: str  # Agent ID or "user"
    content: str
    timestamp: float
    mentions: List[str] = field(default_factory=list)  # @mentioned agents
    reply_to: Optional[str] = None  # Thread support


@dataclass
class Channel:
    """A channel for collaboration"""
    channel_id: str
    name: str
    description: str
    members: List[str] = field(default_factory=list)  # Agent IDs + "user"
    messages: List[ChannelMessage] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    is_private: bool = False


class BrainSocketChannels:
    """
    Channel-based collaboration system for AOS
    
    Similar to Buzz's channel concept but simplified for our use case.
    Agents can be @mentioned to trigger responses.
    """
    
    def __init__(self, max_history: int = 1000):
        self.channels: Dict[str, Channel] = {}
        self.max_history = max_history
        
        # Create default channels
        self._create_default_channels()
        
        print(f"[Brain Channels] 📢 Initialized")
        print(f"  Channels: {len(self.channels)}")
        print(f"  Max history per channel: {max_history}")
    
    def _create_default_channels(self):
        """Create default system channels"""
        defaults = [
            ("general", "General Discussion", "General team chat"),
            ("crew-updates", "Crew Updates", "Automated crew status updates"),
            ("operations", "Operations", "Task coordination and assignments"),
            ("intelligence", "Intelligence", "Curriculum and learning discussions"),
        ]
        
        for channel_id, name, desc in defaults:
            self.channels[channel_id] = Channel(
                channel_id=channel_id,
                name=name,
                description=desc,
                members=["user"]  # Captain is default member
            )
    
    def handle_command(self, cmd: str, params: Dict) -> Dict:
        """Handle socket commands for channels"""
        
        handlers = {
            "channel_create": self._cmd_create,
            "channel_join": self._cmd_join,
            "channel_leave": self._cmd_leave,
            "channel_post": self._cmd_post,
            "channel_history": self._cmd_history,
            "channel_members": self._cmd_members,
            "channel_list": self._cmd_list,
        }
        
        if cmd in handlers:
            return handlers[cmd](params)
        else:
            return {"error": f"Unknown channel command: {cmd}"}
    
    def _cmd_create(self, params: Dict) -> Dict:
        """Create new channel"""
        channel_id = params.get("channel_id")
        name = params.get("name", channel_id)
        description = params.get("description", "")
        is_private = params.get("is_private", False)
        created_by = params.get("created_by", "user")
        
        if not channel_id:
            return {"error": "channel_id required"}
        
        if channel_id in self.channels:
            return {"error": f"Channel {channel_id} already exists"}
        
        self.channels[channel_id] = Channel(
            channel_id=channel_id,
            name=name,
            description=description,
            members=[created_by],
            is_private=is_private
        )
        
        return {
            "success": True,
            "channel_id": channel_id,
            "name": name,
            "members": [created_by]
        }
    
    def _cmd_join(self, params: Dict) -> Dict:
        """Join a channel"""
        channel_id = params.get("channel_id")
        agent_id = params.get("agent_id", "user")
        
        if not channel_id:
            return {"error": "channel_id required"}
        
        if channel_id not in self.channels:
            return {"error": f"Channel {channel_id} not found"}
        
        channel = self.channels[channel_id]
        
        if agent_id in channel.members:
            return {"success": True, "message": f"Already in {channel_id}"}
        
        channel.members.append(agent_id)
        
        # Post join message
        self._post_system_message(channel_id, f"{agent_id} joined the channel")
        
        return {
            "success": True,
            "channel_id": channel_id,
            "members": channel.members
        }
    
    def _cmd_leave(self, params: Dict) -> Dict:
        """Leave a channel"""
        channel_id = params.get("channel_id")
        agent_id = params.get("agent_id", "user")
        
        if channel_id not in self.channels:
            return {"error": f"Channel {channel_id} not found"}
        
        channel = self.channels[channel_id]
        
        if agent_id in channel.members:
            channel.members.remove(agent_id)
            self._post_system_message(channel_id, f"{agent_id} left the channel")
        
        return {
            "success": True,
            "channel_id": channel_id,
            "members": channel.members
        }
    
    def _cmd_post(self, params: Dict) -> Dict:
        """Post message to channel"""
        channel_id = params.get("channel_id")
        sender = params.get("sender", "user")
        content = params.get("content", "")
        reply_to = params.get("reply_to")
        
        if not channel_id or not content:
            return {"error": "channel_id and content required"}
        
        if channel_id not in self.channels:
            return {"error": f"Channel {channel_id} not found"}
        
        channel = self.channels[channel_id]
        
        # Check if sender is member
        if sender not in channel.members:
            return {"error": f"Not a member of {channel_id}"}
        
        # Parse mentions (@agent_name)
        mentions = self._parse_mentions(content)
        
        # Create message
        msg = ChannelMessage(
            message_id=hashlib.sha256(f"{sender}{content}{time.time()}".encode()).hexdigest()[:16],
            channel_id=channel_id,
            sender=sender,
            content=content,
            timestamp=time.time(),
            mentions=mentions,
            reply_to=reply_to
        )
        
        channel.messages.append(msg)
        
        # Prune history if needed
        if len(channel.messages) > self.max_history:
            channel.messages = channel.messages[-self.max_history:]
        
        return {
            "success": True,
            "message_id": msg.message_id,
            "channel_id": channel_id,
            "mentions": mentions,
            "timestamp": msg.timestamp
        }
    
    def _parse_mentions(self, content: str) -> List[str]:
        """Parse @mentions from content"""
        mentions = []
        words = content.split()
        for word in words:
            if word.startswith("@"):
                mentions.append(word[1:])  # Remove @
        return mentions
    
    def _cmd_history(self, params: Dict) -> Dict:
        """Get channel message history"""
        channel_id = params.get("channel_id")
        limit = params.get("limit", 50)
        before_message = params.get("before_message")  # For pagination
        
        if channel_id not in self.channels:
            return {"error": f"Channel {channel_id} not found"}
        
        channel = self.channels[channel_id]
        messages = channel.messages
        
        # Filter by pagination
        if before_message:
            for i, msg in enumerate(messages):
                if msg.message_id == before_message:
                    messages = messages[:i]
                    break
        
        # Limit results
        messages = messages[-limit:]
        
        return {
            "channel_id": channel_id,
            "messages": [
                {
                    "message_id": m.message_id,
                    "sender": m.sender,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "mentions": m.mentions,
                    "reply_to": m.reply_to
                }
                for m in messages
            ],
            "has_more": len(channel.messages) > limit
        }
    
    def _cmd_members(self, params: Dict) -> Dict:
        """Get channel members"""
        channel_id = params.get("channel_id")
        
        if channel_id not in self.channels:
            return {"error": f"Channel {channel_id} not found"}
        
        return {
            "channel_id": channel_id,
            "members": self.channels[channel_id].members
        }
    
    def _cmd_list(self, params: Dict) -> Dict:
        """List all channels"""
        return {
            "channels": [
                {
                    "channel_id": c.channel_id,
                    "name": c.name,
                    "description": c.description,
                    "member_count": len(c.members),
                    "message_count": len(c.messages),
                    "is_private": c.is_private
                }
                for c in self.channels.values()
            ]
        }
    
    def _post_system_message(self, channel_id: str, content: str):
        """Post system message to channel"""
        msg = ChannelMessage(
            message_id=hashlib.sha256(f"system{content}{time.time()}".encode()).hexdigest()[:16],
            channel_id=channel_id,
            sender="system",
            content=content,
            timestamp=time.time()
        )
        self.channels[channel_id].messages.append(msg)
    
    def get_mentions_for_agent(self, agent_id: str, since: float = 0) -> List[ChannelMessage]:
        """Get all @mentions for an agent"""
        mentions = []
        for channel in self.channels.values():
            for msg in channel.messages:
                if agent_id in msg.mentions and msg.timestamp > since:
                    mentions.append(msg)
        return mentions
    
    def agent_respond_to_mention(self, agent_id: str, message_id: str, 
                                  response: str, channel_id: str) -> Optional[str]:
        """Agent responds to a mention"""
        if channel_id not in self.channels:
            return None
        
        # Post response
        result = self._cmd_post({
            "channel_id": channel_id,
            "sender": agent_id,
            "content": response,
            "reply_to": message_id
        })
        
        return result.get("message_id") if result.get("success") else None


# Test function
def test_brain_channels():
    """Test channel functionality"""
    print("\n" + "=" * 70)
    print("  📢 BRAIN SOCKET CHANNELS - TEST")
    print("=" * 70)
    
    channels = BrainSocketChannels()
    
    # Test 1: List default channels
    print("\n[TEST 1] List default channels")
    result = channels._cmd_list({})
    print(f"  Channels: {len(result['channels'])}")
    for c in result['channels']:
        print(f"    #{c['channel_id']}: {c['name']}")
    
    # Test 2: Join channel
    print("\n[TEST 2] Join channel")
    result = channels._cmd_join({"channel_id": "general", "agent_id": "vex_001"})
    print(f"  Result: {result['success']}")
    print(f"  Members: {result['members']}")
    
    # Test 3: Post with mention
    print("\n[TEST 3] Post with @mention")
    result = channels._cmd_post({
        "channel_id": "general",
        "sender": "user",
        "content": "@Vex research the latest POS trends for 2026"
    })
    print(f"  Message ID: {result['message_id']}")
    print(f"  Mentions: {result['mentions']}")
    
    # Test 4: Get mentions for agent
    print("\n[TEST 4] Get mentions for Vex")
    mentions = channels.get_mentions_for_agent("Vex")
    print(f"  Mentions found: {len(mentions)}")
    for m in mentions:
        print(f"    From {m.sender}: {m.content[:50]}...")
    
    # Test 5: Agent responds
    print("\n[TEST 5] Agent responds to mention")
    if mentions:
        response_id = channels.agent_respond_to_mention(
            "vex_001",
            mentions[0].message_id,
            "On it! Researching POS trends now...",
            "general"
        )
        print(f"  Response ID: {response_id}")
    
    # Test 6: Get history
    print("\n[TEST 6] Get channel history")
    result = channels._cmd_history({"channel_id": "general", "limit": 10})
    print(f"  Messages: {len(result['messages'])}")
    for m in result['messages']:
        print(f"    {m['sender']}: {m['content'][:40]}...")
    
    # Test 7: Create new channel
    print("\n[TEST 7] Create new channel")
    result = channels._cmd_create({
        "channel_id": "sales-team",
        "name": "Sales Team",
        "description": "Sales coordination",
        "created_by": "user"
    })
    print(f"  Created: {result['success']}")
    print(f"  Channel: {result['channel_id']}")
    
    print("\n" + "=" * 70)
    print("  ✅ BRAIN SOCKET CHANNELS TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    test_brain_channels()
