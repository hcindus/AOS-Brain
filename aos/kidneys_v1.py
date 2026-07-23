#!/usr/bin/env python3
"""
AOS KIDNEYS v1.0 - Ternary Waste Management & Pattern Recycling
Biological analogy: Filter blood, reabsorb nutrients, excrete waste as urine

Ternary States:
- FILTER: Pass useful patterns to memory/storage
- REABSORB: Extract and recycle valuable signal from waste streams
- EXCRETE: Discard pure noise/waste permanently

Key Concept: Signal vs Noise
- SIGNAL: Information that advances goals, reveals patterns, enables predictions
- NOISE: Random variation that obscures patterns, redundant data, corruption
"""

import time
import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional
from enum import Enum, auto
from collections import defaultdict
from datetime import datetime


class KidneyState(Enum):
    FILTER = auto()     # Standard filtering - keep useful, discard waste
    REABSORB = auto()   # Aggressive recycling - extract signal from garbage
    EXCRETE = auto()    # Emergency purge - discard everything


@dataclass
class WasteEvent:
    """
    Feedback-to-Curriculum: Waste becomes nourishment
    
    When Kidneys detect REABSORB or EXCRETE, auto-generate
    curriculum items to teach the Brain from its mistakes.
    """
    event_id: str = ""                           # UUID v4
    timestamp: float = 0.0                        # Unix timestamp
    kidneys_state: str = ""                       # REABSORB or EXCRETE
    source_tick: int = 0                          # Brain tick when generated
    output_type: str = "text"                     # code/decision/text/classification
    output_hash: str = ""                         # SHA256 of problematic output
    error_category: str = ""                      # syntax/logic/alignment/efficiency/security
    severity: float = 0.0                           # 0.0-1.0
    content_preview: str = ""                     # Truncated sample (no full prompt)
    suggested_lesson: str = ""                    # Auto-generated learning objective
    status: str = "pending"                       # pending/processed/archived
    
    def __post_init__(self):
        if not self.event_id:
            import uuid
            self.event_id = str(uuid.uuid4())[:8]
        if self.timestamp == 0.0:
            self.timestamp = time.time()
    
    def to_dict(self) -> dict:
        """Serialize for persistence/socket"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WasteEvent':
        """Deserialize from persistence"""
        return cls(**data)


@dataclass
class Filtrate:
    """A filtered unit ready for processing"""
    content: str
    source: str
    timestamp: float
    signal_score: float = 0.0      # 0.0-1.0, higher = more signal
    pattern_hash: str = ""         # Fingerprint for deduplication
    recycle_count: int = 0         # How many times reabsorbed
    
    def __post_init__(self):
        if not self.pattern_hash:
            self.pattern_hash = hashlib.md5(self.content.encode()).hexdigest()[:8]


class AOSKidneysV1:
    """
    Ternary Kidneys - Pattern recycling and waste management
    
    Like biological kidneys:
    - FILTER: Keep the good stuff, send waste to bladder
    - REABSORB: When dehydrated (low signal), squeeze waste for every drop of value
    - EXCRETE: When flooded (too much noise), purge to prevent system damage
    
    NEW v1.1: Feedback-to-Curriculum Loop
    - REABSORB/EXCRETE auto-generate WasteEvents
    - WasteEvents convert to curriculum lessons
    - Brain learns from its own mistakes (metabolic loop)
    
    Signal vs Noise Detection:
    - Signal: Novel, structured, goal-relevant, low entropy
    - Noise: Repetitive, random, irrelevant, high entropy
    """
    
    def __init__(self,
                 signal_threshold: float = 0.5,
                 reabsorb_threshold: float = 0.2,
                 bladder_capacity: int = 500,
                 pattern_memory: int = 1000,
                 waste_loop_enabled: bool = True):
        
        self.signal_threshold = signal_threshold    # Above this = keep
        self.reabsorb_threshold = reabsorb_threshold # Below this = potential waste
        self.bladder_capacity = bladder_capacity
        self.pattern_limit = pattern_memory
        self.waste_loop_enabled = waste_loop_enabled  # NEW: Feedback-to-Curriculum toggle
        
        self.state = KidneyState.FILTER
        
        # Storage systems
        self.bladder = []           # Waste waiting for potential reabsorption
        self.nutrients = []         # Valuable patterns going to memory
        self.pattern_history = defaultdict(int)  # Seen patterns (for dedup)
        
        # NEW v1.1: Waste Queue for Curriculum Loop
        self.waste_queue = []       # WasteEvents awaiting curriculum ingestion
        self.waste_queue_max_size = 1000  # Prevent memory bloat
        self.processed_waste_hashes = set()  # Deduplication
        
        # Statistics
        self.total_processed = 0
        self.reabsorbed_count = 0
        self.excreted_count = 0
        self.waste_events_generated = 0  # NEW
        self.curriculum_items_queued = 0  # NEW
        
        # Signal/Noise tracking
        self.signal_history = []
        self.noise_estimate = 0.5
        
        print(f"[Kidneys v1.1] Initialized - ternary waste management")
        print(f"  FILTER:   Keep signal >{signal_threshold}, queue rest")
        print(f"  REABSORB: Extract value from waste when signal low")
        print(f"  EXCRETE:  Emergency purge when overwhelmed")
        if waste_loop_enabled:
            print(f"  ♻️  FEEDBACK LOOP: Waste → Curriculum (enabled)")
    
    def calculate_signal_score(self, content: str, context: dict = None) -> float:
        """
        Calculate signal-to-noise ratio for content
        
        SIGNAL indicators:
        - Novel (hasn't been seen before)
        - Structured (has patterns, not random)
        - Goal-relevant (contains actionable info)
        - Low entropy (predictable, not chaotic)
        
        NOISE indicators:
        - Repetitive (already seen)
        - Random/gibberish
        - Irrelevant (no action possible)
        - High entropy (chaotic)
        """
        score = 0.5  # Baseline
        
        # Novelty check (signal is novel)
        pattern_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        if pattern_hash not in self.pattern_history:
            score += 0.2  # Novel = signal
            self.pattern_history[pattern_hash] = 1
        else:
            score -= 0.3  # Repetitive = noise
            self.pattern_history[pattern_hash] += 1
        
        # Structure check (signal has structure)
        words = content.split()
        if len(words) > 3:
            avg_len = sum(len(w) for w in words) / len(words)
            if 3 < avg_len < 12:  # Normal word lengths = structured
                score += 0.15
            else:
                score -= 0.1
        
        # Actionability check (signal enables action)
        action_keywords = ['error', 'warning', 'complete', 'failed', 'success', 
                          'created', 'deleted', 'updated', 'running', 'stopped',
                          'temperature', 'pressure', 'status', 'alert']
        if any(kw in content.lower() for kw in action_keywords):
            score += 0.15  # Actionable = signal
        
        # Context boost (if provided)
        if context:
            if context.get('is_alert', False):
                score += 0.2
            if context.get('is_user_input', False):
                score += 0.1
        
        # Entropy estimate (low entropy = signal)
        if len(content) > 10:
            unique_ratio = len(set(content.lower())) / len(content)
            if unique_ratio < 0.7:  # Low character diversity = structure
                score += 0.1
            else:
                score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    # ========== v1.1: FEEDBACK-TO-CURRICULUM METHODS ==========
    
    def _categorize_error(self, content: str, signal_score: float) -> Tuple[str, float]:
        """
        Auto-categorize waste for curriculum generation
        
        Returns: (error_category, severity)
        """
        content_lower = content.lower()
        
        # Syntax errors
        if any(kw in content_lower for kw in ['syntaxerror', 'parse error', 'invalid syntax', 'unexpected token']):
            return "syntax", 0.9
        
        # Logic errors
        if any(kw in content_lower for kw in ['logic error', 'undefined', 'null pointer', 'indexerror', 'keyerror']):
            return "logic", 0.8
        
        # Security issues
        if any(kw in content_lower for kw in ['security', 'vulnerability', 'injection', 'sanitize', 'xss', 'sql']):
            return "security", 0.95
        
        # Efficiency issues
        if any(kw in content_lower for kw in ['timeout', 'slow', 'performance', 'memory leak', 'infinite loop']):
            return "efficiency", 0.7
        
        # Alignment issues (mismatch with expected)
        if any(kw in content_lower for kw in ['mismatch', 'not aligned', 'off topic', 'irrelevant']):
            return "alignment", 0.6
        
        # Default based on signal score
        if signal_score < 0.2:
            return "logic", 0.7  # Low signal = likely logic problem
        elif signal_score < 0.4:
            return "alignment", 0.5
        else:
            return "general", 0.3
    
    def _generate_lesson(self, error_category: str, content: str, state: str) -> str:
        """
        Auto-generate curriculum lesson from waste pattern
        
        Metabolic principle: Waste becomes nourishment
        """
        lessons = {
            "syntax": [
                "Review proper syntax structure. Common patterns: brackets mismatch, indentation errors, missing delimiters.",
                "Strengthen syntactic precision. Focus on: quote matching, brace balance, statement termination.",
                "Practice error-free code construction. Check: parentheses, brackets, quotes, semicolons."
            ],
            "logic": [
                "Strengthen logical reasoning. Verify: preconditions, invariants, edge cases, boundary conditions.",
                "Practice defensive programming. Consider: null inputs, empty states, type mismatches, race conditions.",
                "Review algorithmic correctness. Validate: loop termination, recursion depth, state transitions."
            ],
            "security": [
                "Prioritize secure coding practices. Always: sanitize inputs, validate data, escape outputs.",
                "Review security vulnerabilities. Check for: injection attacks, XSS, CSRF, unsafe deserialization.",
                "Adopt defense-in-depth. Validate at boundaries, minimize attack surface, fail securely."
            ],
            "efficiency": [
                "Optimize resource utilization. Profile: memory usage, CPU cycles, I/O operations, network calls.",
                "Review algorithmic complexity. Target: O(n) or better, avoid nested loops, use appropriate data structures.",
                "Practice efficient patterns. Cache results, batch operations, lazy load, stream large data."
            ],
            "alignment": [
                "Re-align with mission objectives. Verify output matches intent and governance constraints.",
                "Review scope compliance. Ensure work stays within defined boundaries and approved parameters.",
                "Practice intent matching. Validate that output directly addresses the specific request."
            ],
            "general": [
                "Focus on signal clarity. Reduce noise, increase structure, prioritize actionable information.",
                "Practice pattern recognition. Identify what makes high-quality vs low-quality outputs.",
                "Review and refine. Self-assess before finalizing, seek continuous improvement."
            ]
        }
        
        # Select lesson based on state (REABSORB vs EXCRETE severity)
        category_lessons = lessons.get(error_category, lessons["general"])
        if state == "EXCRETE":
            return category_lessons[0]  # Most critical lesson
        elif state == "REABSORB":
            return category_lessons[1]  # Reinforcement lesson
        else:
            return category_lessons[2]  # General improvement
    
    def _create_waste_event(self, state: KidneyState, content: str, 
                           source: str, signal_score: float, tick: int = 0) -> WasteEvent:
        """
        Create WasteEvent for Feedback-to-Curriculum loop
        
        Called when REABSORB or EXCRETE occurs
        """
        error_category, severity = self._categorize_error(content, signal_score)
        
        # Generate content hash for deduplication
        output_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # Truncate content for preview (no full prompts exposed)
        preview = content[:200] + "..." if len(content) > 200 else content
        
        # Generate auto-lesson
        suggested_lesson = self._generate_lesson(error_category, content, state.name)
        
        event = WasteEvent(
            kidneys_state=state.name,
            source_tick=tick,
            output_type=self._detect_output_type(content),
            output_hash=output_hash,
            error_category=error_category,
            severity=severity,
            content_preview=preview,
            suggested_lesson=suggested_lesson,
            status="pending"
        )
        
        return event
    
    def _detect_output_type(self, content: str) -> str:
        """Detect if content is code, decision, text, etc."""
        # Simple heuristics
        code_markers = ['def ', 'class ', 'function', 'import ', '#include', '{', ';']
        if any(m in content for m in code_markers):
            return "code"
        
        decision_markers = ['decision:', 'action:', 'plan:', 'strategy:']
        if any(m in content.lower() for m in decision_markers):
            return "decision"
        
        if content.strip().startswith('{') or content.strip().startswith('['):
            return "json"
        
        return "text"
    
    def _queue_waste_for_curriculum(self, waste_event: WasteEvent) -> bool:
        """
        Queue waste event for curriculum ingestion
        
        Returns: True if queued, False if duplicate or queue full
        """
        # Deduplication check
        if waste_event.output_hash in self.processed_waste_hashes:
            return False
        
        # Queue size limit
        if len(self.waste_queue) >= self.waste_queue_max_size:
            # Remove oldest
            oldest = self.waste_queue.pop(0)
            self.processed_waste_hashes.discard(oldest.output_hash)
        
        # Add to queue
        self.waste_queue.append(waste_event)
        self.processed_waste_hashes.add(waste_event.output_hash)
        self.waste_events_generated += 1
        
        return True
    
    def process_for_recycling(self, content: str, source: str = "unknown",
                              context: dict = None, tick: int = 0) -> Tuple[KidneyState, Optional[WasteEvent], dict]:
        """
        NEW v1.1: Assess output and auto-generate waste event if needed
        
        This is the entry point for Feedback-to-Curriculum loop.
        
        Returns: (kidneys_state, waste_event_or_none, metadata)
        """
        signal_score = self.calculate_signal_score(content, context)
        self.total_processed += 1
        
        # Determine state
        state = self._determine_state(signal_score, content)
        self.state = state
        
        waste_event = None
        
        # If REABSORB or EXCRETE, create WasteEvent
        if state in [KidneyState.REABSORB, KidneyState.EXCRETE] and self.waste_loop_enabled:
            waste_event = self._create_waste_event(state, content, source, signal_score, tick)
            
            # Queue for curriculum
            if self._queue_waste_for_curriculum(waste_event):
                self.curriculum_items_queued += 1
                print(f"[Kidneys] 🔄 Queued waste event: {waste_event.error_category} "
                      f"(severity: {waste_event.severity:.2f})")
        
        # Standard processing
        if state == KidneyState.FILTER:
            result = self._filter(content, signal_score, source)
        elif state == KidneyState.REABSORB:
            result = self._reabsorb()
        else:  # EXCRETE
            result = self._excrete()
        
        # Update noise estimate
        self.noise_estimate = 0.9 * self.noise_estimate + 0.1 * (1 - signal_score)
        self.signal_history.append(signal_score)
        if len(self.signal_history) > 100:
            self.signal_history.pop(0)
        
        metadata = {
            "signal_score": signal_score,
            "noise_estimate": self.noise_estimate,
            "bladder_level": len(self.bladder),
            "nutrients_stored": len(self.nutrients),
            "unique_patterns": len(self.pattern_history),
            "waste_queue_size": len(self.waste_queue),  # NEW
            "waste_event_created": waste_event is not None  # NEW
        }
        
        return state, waste_event, metadata
    
    def flush_waste_queue(self) -> List[WasteEvent]:
        """
        Return all pending waste events and clear queue
        
        Called by curriculum feeder to ingest lessons
        """
        flushed = self.waste_queue.copy()
        self.waste_queue = []
        return flushed
    
    def get_waste_queue_status(self) -> dict:
        """Get current waste queue status for monitoring"""
        return {
            "queue_size": len(self.waste_queue),
            "max_size": self.waste_queue_max_size,
            "events_generated": self.waste_events_generated,
            "items_queued": self.curriculum_items_queued,
            "unique_hashes_tracked": len(self.processed_waste_hashes)
        }
    
    def process(self, content: str, source: str = "unknown", 
                context: dict = None, force_state: KidneyState = None) -> Tuple[KidneyState, Optional[str], dict]:
        """
        Process content through kidney filtration
        
        Returns: (state, result_content, metadata)
        """
        signal_score = self.calculate_signal_score(content, context)
        self.total_processed += 1
        
        # Determine state
        if force_state:
            self.state = force_state
        else:
            self.state = self._determine_state(signal_score, content)
        
        # Process based on state
        if self.state == KidneyState.FILTER:
            result = self._filter(content, signal_score, source)
            
        elif self.state == KidneyState.REABSORB:
            result = self._reabsorb()
            
        else:  # EXCRETE
            result = self._excrete()
        
        # Update noise estimate (exponential moving average)
        self.noise_estimate = 0.9 * self.noise_estimate + 0.1 * (1 - signal_score)
        self.signal_history.append(signal_score)
        if len(self.signal_history) > 100:
            self.signal_history.pop(0)
        
        metadata = {
            "signal_score": signal_score,
            "noise_estimate": self.noise_estimate,
            "bladder_level": len(self.bladder),
            "nutrients_stored": len(self.nutrients),
            "unique_patterns": len(self.pattern_history)
        }
        
        return self.state, result, metadata
    
    def _determine_state(self, signal_score: float, content: str) -> KidneyState:
        """Determine which filtration mode to use"""
        
        # Check for emergency (bladder full)
        if len(self.bladder) > self.bladder_capacity * 0.9:
            return KidneyState.EXCRETE
        
        # Check for dehydration (low recent signal)
        recent_signal = sum(self.signal_history[-10:]) / max(len(self.signal_history[-10:]), 1)
        if recent_signal < 0.3 and len(self.bladder) > 10:
            return KidneyState.REABSORB
        
        # Normal filtering
        return KidneyState.FILTER
    
    def _filter(self, content: str, signal_score: float, source: str) -> Optional[str]:
        """FILTER: Keep signal, queue potential noise"""
        if signal_score >= self.signal_threshold:
            # Good signal - store as nutrient
            filtrate = Filtrate(
                content=content,
                source=source,
                timestamp=time.time(),
                signal_score=signal_score
            )
            self.nutrients.append(filtrate)
            
            # Keep nutrients bounded
            if len(self.nutrients) > self.pattern_limit:
                self.nutrients.pop(0)
            
            return content
        else:
            # Low signal - store in bladder for possible reabsorption
            filtrate = Filtrate(
                content=content,
                source=source,
                timestamp=time.time(),
                signal_score=signal_score
            )
            self.bladder.append(filtrate)
            
            # Keep bladder bounded
            if len(self.bladder) > self.bladder_capacity:
                old = self.bladder.pop(0)
                self.excreted_count += 1
            
            return None  # Not immediately passed through
    
    def _reabsorb(self) -> Optional[str]:
        """REABSORB: Squeeze waste for valuable patterns"""
        if not self.bladder:
            return None
        
        # Sort bladder by signal score (highest first)
        self.bladder.sort(key=lambda x: x.signal_score, reverse=True)
        
        # Take best from waste
        best_waste = self.bladder.pop(0)
        best_waste.recycle_count += 1
        self.reabsorbed_count += 1
        
        # Re-add to nutrients
        self.nutrients.append(best_waste)
        
        print(f"[Kidneys] REABSORBED pattern from waste (score: {best_waste.signal_score:.2f})")
        
        return best_waste.content
    
    def _excrete(self) -> None:
        """EXCRETE: Emergency purge of all waste"""
        purged = len(self.bladder)
        self.bladder = []
        self.excreted_count += purged
        
        print(f"[Kidneys] EXCRETED {purged} waste items (emergency purge)")
        
        return None
    
    def get_nutrients(self, n: int = 10) -> List[Filtrate]:
        """Get top nutrients for memory storage"""
        self.nutrients.sort(key=lambda x: x.signal_score, reverse=True)
        return self.nutrients[:n]
    
    def get_status(self) -> dict:
        """Current kidney status"""
        recent_signal = sum(self.signal_history[-20:]) / max(len(self.signal_history[-20:]), 1) if self.signal_history else 0
        
        return {
            "state": self.state.name,
            "total_processed": self.total_processed,
            "reabsorbed": self.reabsorbed_count,
            "excreted": self.excreted_count,
            "bladder_level": len(self.bladder),
            "bladder_capacity": self.bladder_capacity,
            "nutrients_stored": len(self.nutrients),
            "recent_signal_avg": recent_signal,
            "noise_estimate": self.noise_estimate,
            "unique_patterns_seen": len(self.pattern_history),
            # NEW v1.1: Feedback loop metrics
            "waste_loop_enabled": self.waste_loop_enabled,
            "waste_queue_size": len(self.waste_queue),
            "waste_events_generated": self.waste_events_generated,
            "curriculum_items_queued": self.curriculum_items_queued
        }


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("  🫘 KIDNEYS v1.0 - Ternary Waste Management Test")
    print("=" * 70)
    
    kidneys = AOSKidneysV1()
    
    print("\nSIGNAL vs NOISE Examples:")
    print("-" * 70)
    
    test_inputs = [
        ("ERROR: Database connection failed at 07:42:15", "log", {"is_alert": True}),
        ("asdfasdf jkl;jkl; random gibberish content here", "garbage", {}),
        ("System temperature: 45°C, CPU: 12%", "sensor", {}),
        ("The quick brown fox jumps over the lazy dog", "text", {}),
        ("!!!!!!!!! ALERT !!!!!!!!!!", "alert", {"is_alert": True}),
        ("User input: Start the backup process", "user", {"is_user_input": True}),
        ("lorem ipsum dolor sit amet consectetur", "filler", {}),
        ("Backup completed successfully at 2026-04-05 07:42:30", "log", {}),
    ]
    
    print("\nProcessing stream...\n")
    for content, source, context in test_inputs:
        state, result, meta = kidneys.process(content, source, context)
        
        signal_type = "SIGNAL" if meta['signal_score'] > 0.5 else "NOISE"
        
        print(f"  [{signal_type}] {source:8s} | Score: {meta['signal_score']:.2f} | State: {state.name:10s}")
        print(f"    In:  {content[:50]}...")
        if result:
            print(f"    Out: {result[:50]}...")
        elif state.name == "REABSORB":
            print(f"    Out: [REABSORBED from waste]")
        else:
            print(f"    Out: [FILTERED → bladder]")
        print()
    
    # Force reabsorption
    print("-" * 70)
    print("\nForcing REABSORB mode (low signal detected)...\n")
    kidneys.signal_history = [0.1] * 15  # Simulate low signal period
    state, result, meta = kidneys.process("Low priority log entry", "system", {})
    
    print("=" * 70)
    print("  Kidney Status:")
    for k, v in kidneys.get_status().items():
        print(f"    {k}: {v}")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("  SIGNAL vs NOISE SUMMARY")
    print("=" * 70)
    print("""
    SIGNAL (Keep):
    - Novel patterns (never seen before)
    - Structured content (not random)
    - Actionable information (errors, alerts, completions)
    - Goal-relevant data
    - Low entropy (predictable patterns)
    
    NOISE (Filter/Reabsorb/Excrete):
    - Repetitive content (already seen)
    - Random/gibberish text
    - Irrelevant filler (lorem ipsum)
    - Excessive punctuation
    - High entropy (chaotic)
    """)
