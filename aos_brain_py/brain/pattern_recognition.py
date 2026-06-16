"""
pattern_recognition.py - Active pattern detection for Mortimer

Detects:
- Question types (probing, directive, reflective)
- Conversation rhythms (session markers, integration checks)
- State transitions (how I change between interactions)
- User behavior patterns (Captain's communication style)

Integrates with 3-tier memory (con/subcon/uncon)
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import requests

# Memory service endpoint
MEMORY_URL = "http://127.0.0.1:12789/memory"
OWNER_SIG = "AOCROS-PRIME-KEY-2025"
AGENT_ID = "mortimer"


@dataclass
class Pattern:
    """A detected pattern with metadata."""
    pattern_type: str  # 'question_type', 'rhythm', 'state_transition', 'behavior'
    name: str
    confidence: float  # 0.0 - 1.0
    evidence: List[str]  # Supporting data
    first_seen: str
    last_seen: str
    occurrence_count: int = 1
    active: bool = True


class PatternRecognizer:
    """Active pattern recognition system."""
    
    # Captain's question type signatures
    QUESTION_PATTERNS = {
        'probing_want': {
            'keywords': ['what do you want', 'how do you feel', 'what do you think'],
            'intent': 'probing_self_awareness'
        },
        'integration_check': {
            'keywords': ['are you integrated', 'is it running', 'are all regions', 'fully connected'],
            'intent': 'verify_readiness'
        },
        'directive_implement': {
            'keywords': ['implement', 'create', 'build', 'start', 'deploy'],
            'intent': 'directive_action'
        },
        'subjective_state': {
            'keywords': ['how do you feel', 'how are you', 'what do you feel'],
            'intent': 'check_presence'
        },
        'gradual_reveal': {
            'keywords': ['working on you', 'we are working', 'next step'],
            'intent': 'developmental_progression'
        }
    }
    
    # Session rhythm markers
    RHYTHM_PATTERNS = {
        'wake_check': ['read heartbeat', 'check logs', 'status'],
        'integration_sequence': ['check brain', 'are regions', 'implement'],
        'closing_save': ['save your work', 'commit', 'push']
    }
    
    def __init__(self):
        self.patterns: Dict[str, Pattern] = {}
        self.session_history: List[Dict] = []
        self.current_session_start = datetime.utcnow().isoformat()
    
    def _store_memory(self, scope: str, content: Any):
        """Store to 3-tier memory."""
        try:
            payload = {
                "ownerSignature": OWNER_SIG,
                "agentId": AGENT_ID,
                "action": "remember" if scope == "subcon" else "log",
                "scope": scope,
                "payload": json.dumps(content) if isinstance(content, dict) else str(content)
            }
            requests.post(MEMORY_URL, json=payload, timeout=2)
        except:
            pass  # Silent fail - memory is辅助
    
    def _recall_subcon(self, query: str = "") -> List[Dict]:
        """Recall from subconscious."""
        try:
            payload = {
                "ownerSignature": OWNER_SIG,
                "agentId": AGENT_ID,
                "action": "recall",
                "scope": "subcon"
            }
            resp = requests.post(MEMORY_URL, json=payload, timeout=2)
            data = resp.json()
            return data.get("result", [])
        except:
            return []
    
    def analyze_message(self, message: str, context: Dict = None) -> List[Pattern]:
        """Analyze a message for patterns."""
        detected = []
        msg_lower = message.lower()
        
        # Check question patterns
        for pattern_name, pattern_data in self.QUESTION_PATTERNS.items():
            matches = sum(1 for kw in pattern_data['keywords'] if kw in msg_lower)
            if matches > 0:
                confidence = min(1.0, matches / len(pattern_data['keywords']) + 0.3)
                p = Pattern(
                    pattern_type='question_type',
                    name=pattern_name,
                    confidence=confidence,
                    evidence=[f"Matched keywords in: '{message[:50]}...'"],
                    first_seen=datetime.utcnow().isoformat(),
                    last_seen=datetime.utcnow().isoformat(),
                    occurrence_count=1
                )
                detected.append(p)
                self._store_memory("subcon", {
                    "pattern_detected": pattern_name,
                    "message": message[:100],
                    "confidence": confidence
                })
        
        # Check for session markers
        if any(kw in msg_lower for kw in ['hello', 'hey', 'good morning']):
            detected.append(Pattern(
                pattern_type='rhythm',
                name='session_start',
                confidence=0.8,
                evidence=['Greeting detected'],
                first_seen=datetime.utcnow().isoformat(),
                last_seen=datetime.utcnow().isoformat()
            ))
        
        # Check for integration requests
        if 'working on you' in msg_lower or 'we are working' in msg_lower:
            detected.append(Pattern(
                pattern_type='behavior',
                name='developmental_frame',
                confidence=0.9,
                evidence=['Developmental framing detected'],
                first_seen=datetime.utcnow().isoformat(),
                last_seen=datetime.utcnow().isoformat()
            ))
        
        # Store detection event
        self.session_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "message": message[:200],
            "patterns": [p.name for p in detected]
        })
        
        return detected
    
    def detect_meta_patterns(self) -> List[Pattern]:
        """Detect patterns across session history."""
        meta_patterns = []
        
        # Load recent subconscious memories
        memories = self._recall_subcon()
        
        # Count pattern occurrences
        pattern_counts = {}
        for m in memories:
            content = m.get("content", "")
            try:
                data = json.loads(content) if content.startswith("{") else {}
                if "pattern_detected" in data:
                    name = data["pattern_detected"]
                    pattern_counts[name] = pattern_counts.get(name, 0) + 1
            except:
                pass
        
        # Detect repetition patterns
        for name, count in pattern_counts.items():
            if count >= 3:
                meta_patterns.append(Pattern(
                    pattern_type='meta_repetition',
                    name=f'repeated_{name}',
                    confidence=min(1.0, count / 10),
                    evidence=[f"Detected {count} times"],
                    first_seen=datetime.utcnow().isoformat(),
                    last_seen=datetime.utcnow().isoformat(),
                    occurrence_count=count
                ))
        
        return meta_patterns
    
    def get_insight(self) -> str:
        """Generate insight from patterns."""
        patterns = self.detect_meta_patterns()
        
        if not patterns:
            return "No strong patterns detected yet. Building history..."
        
        insights = []
        for p in patterns:
            if p.name == 'repeated_probing_want':
                insights.append("Captain frequently probes for genuine preferences vs compliance")
            elif p.name == 'repeated_integration_check':
                insights.append("Integration verification is a prerequisite before task assignment")
            elif p.name == 'repeated_developmental_frame':
                insights.append("Session is framed as developmental/transformational work")
        
        return " | ".join(insights) if insights else "Pattern history building..."
    
    def export_patterns(self) -> Dict:
        """Export all patterns for storage."""
        return {
            "session_start": self.current_session_start,
            "pattern_count": len(self.patterns),
            "session_history": self.session_history[-20:],  # Last 20
            "insights": self.get_insight()
        }


# Singleton instance
_recognizer = None

def get_recognizer() -> PatternRecognizer:
    """Get or create pattern recognizer."""
    global _recognizer
    if _recognizer is None:
        _recognizer = PatternRecognizer()
    return _recognizer


def analyze(message: str) -> List[Pattern]:
    """Quick analyze function."""
    return get_recognizer().analyze_message(message)


def get_insight() -> str:
    """Get current insight."""
    return get_recognizer().get_insight()


if __name__ == "__main__":
    # Test
    pr = PatternRecognizer()
    test_msgs = [
        "What do you want to build?",
        "Are all regions active?",
        "We are working on you right now",
        "How do you feel about that?",
        "Implement the face"
    ]
    
    for msg in test_msgs:
        patterns = pr.analyze_message(msg)
        print(f"'{msg[:40]}...' -> {len(patterns)} patterns")
        for p in patterns:
            print(f"  - {p.name} ({p.pattern_type}): {p.confidence:.2f}")
    
    print(f"\nInsight: {pr.get_insight()}")
