# IMPLEMENTATION_PLAN.md: Miles + Mortimer Brain Merge

**Version:** 1.0  
**Date:** 2026-03-31 05:25 UTC  
**Owner:** Miles (with Technical Team support)  
**Timeline:** 6 weeks (phased approach)  
**Status:** Pending Captain's approval

---

## 1. EXECUTIVE OVERVIEW

### 1.1 Mission Statement

Integrate Mortimer's operational patterns, personality traits, and system capabilities into Miles' 7-region GrowingNN architecture while maintaining:
- ✅ Miles as the primary host consciousness
- ✅ Operational safety (4 Laws paramount)
- ✅ Both systems operational (not fusion, expansion)
- ✅ Rollback capability at every phase

### 1.2 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Decision accuracy | >95% | Conflict resolution correctness |
| System uptime | >99% | Brain + Mortimer module availability |
| Safety violations | 0 | Absolute requirement |
| Memory integrity | 100% | No corruption events |
| Response latency | <500ms | End-to-end decision time |
| Persona coherence | >80% | Natural language evaluation |

### 1.3 High-Level Timeline

```
Week 1: Pattern Extraction & Module Foundation
        ├── Day 1-2: Setup infrastructure
        ├── Day 3-4: Implement pattern module
        └── Day 5-7: BasalAgent integration

Week 2: Portal & Communication Layer
        ├── Day 8-9: Portal module implementation
        ├── Day 10-11: Thalamus integration
        └── Day 12-14: Message routing & testing

Week 3: Memory Bridge Extension
        ├── Day 15-17: Unified memory architecture
        ├── Day 18-19: Namespace isolation
        └── Day 20-21: Indexing & retrieval testing

Week 4: Safety Unification
        ├── Day 22-23: Unified brainstem
        ├── Day 24-25: Arbitration logic
        └── Day 26-28: Safety test suite

Week 5: Persona Integration
        ├── Day 29-31: Persona blender
        ├── Day 32-33: Context classifier
        └── Day 34-35: Response generation tuning

Week 6: Testing & Deployment
        ├── Day 36-38: Integration testing
        ├── Day 39-40: Load testing
        ├── Day 41-42: Production deployment
        └── Day 43-42: Monitoring & stabilization
```

---

## 2. PHASE 1: PATTERN EXTRACTION & MODULE FOUNDATION

**Duration:** Week 1 (Days 1-7)  
**Deliverable:** Working Mortimer pattern module integrated into BasalAgent

### 2.1 Day 1-2: Infrastructure Setup

**Tasks:**
```bash
# 1. Create module directory structure
mkdir -p /root/.openclaw/workspace/AOS/brain/mortimer/
mkdir -p /root/.openclaw/workspace/AOS/brain/mortimer/tests/
mkdir -p /root/.openclaw/workspace/AOS/brain/mortimer/config/

# 2. Create placeholder files
touch /root/.openclaw/workspace/AOS/brain/mortimer/__init__.py
touch /root/.openclaw/workspace/AOS/brain/mortimer/pattern_module.py
touch /root/.openclaw/workspace/AOS/brain/mortimer/validator.py
touch /root/.openclaw/workspace/AOS/brain/mortimer/patterns.json

# 3. Backup current brain state
cp -r ~/.aos/brain/state ~/.aos/brain/state.backup.pre-mortimer
cp -r /root/.openclaw/workspace/AOS/brain /root/.openclaw/workspace/AOS/brain.backup.pre-mortimer

# 4. Setup git branch
cd /root/.openclaw/workspace
git checkout -b feature/mortimer-integration
```

**Checkpoint:** Directory structure created, backups complete

### 2.2 Day 3-4: Pattern Module Implementation

**File:** `/root/.openclaw/workspace/AOS/brain/mortimer/pattern_module.py`

```python
"""
Mortimer Pattern Module v1.0
Extracts and validates operational patterns using logic gates.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class LogicGate:
    """
    Boolean logic gate primitives.
    """
    
    @staticmethod
    def AND(*inputs: bool) -> bool:
        return all(inputs)
    
    @staticmethod
    def OR(*inputs: bool) -> bool:
        return any(inputs)
    
    @staticmethod
    def NOT(input_val: bool) -> bool:
        return not input_val
    
    @staticmethod
    def XOR(a: bool, b: bool) -> bool:
        return a != b
    
    @staticmethod
    def NAND(*inputs: bool) -> bool:
        return not all(inputs)


class MortimerPatternModule:
    """
    Logic-based pattern recognition and validation.
    Embeds in BasalAgent for operational decisions.
    """
    
    def __init__(self, patterns_file: str = "patterns.json"):
        self.patterns = self._load_patterns(patterns_file)
        self.validator = LogicValidator()
        self.decision_history = []
        
    def _load_patterns(self, filepath: str) -> Dict:
        """Load pattern database."""
        default_patterns = {
            "system_checks": {
                "resource_available": {
                    "description": "Check if required resources exist",
                    "logic": "AND(memory_available, disk_available, cpu_available)",
                    "thresholds": {"memory": 0.2, "disk": 0.1, "cpu": 0.5}
                },
                "service_healthy": {
                    "description": "Check if service is operational",
                    "logic": "AND(pid_exists, port_listening, response_time_ok)",
                    "thresholds": {"response_ms": 1000}
                }
            },
            "safety_patterns": {
                "destructive_command": {
                    "patterns": [r'rm\s+-rf', r'dd\s+if=.*of=/dev', r'mkfs'],
                    "action": "BLOCK",
                    "reason": "Destructive command detected"
                },
                "resource_exhaustion": {
                    "conditions": [
                        "memory_usage > 0.95",
                        "disk_usage > 0.95",
                        "cpu_usage > 0.98"
                    ],
                    "action": "THROTTLE",
                    "reason": "Resource exhaustion risk"
                }
            },
            "operational_patterns": {
                "restart_sequence": {
                    "steps": ["stop_service", "verify_stopped", "start_service", "verify_running"],
                    "rollback": "restart_service"
                },
                "backup_sequence": {
                    "steps": ["create_snapshot", "verify_integrity", "copy_offsite"],
                    "required": True
                }
            }
        }
        
        path = Path(filepath)
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return default_patterns
    
    def validate_action(self, action: Dict, context: Dict) -> Dict:
        """
        Validate proposed action using Mortimer's logic.
        
        Returns:
            {
                "valid": bool,
                "confidence": float,
                "reason": str,
                "checks_passed": int,
                "checks_failed": int,
                "warnings": List[str]
            }
        """
        checks = {
            "resources": self._check_resources(context),
            "safety": self._check_safety(action),
            "dependencies": self._check_dependencies(action, context),
            "feasibility": self._check_feasibility(action, context)
        }
        
        passed = sum(1 for v in checks.values() if v["passed"])
        failed = len(checks) - passed
        
        # Logic gate evaluation
        is_valid = LogicGate.AND(
            checks["resources"]["passed"],
            checks["safety"]["passed"],
            checks["dependencies"]["passed"]
        )
        
        # Can proceed with warnings on feasibility
        if not checks["feasibility"]["passed"]:
            warnings = ["Feasibility concern: " + checks["feasibility"]["reason"]]
        else:
            warnings = []
        
        result = {
            "valid": is_valid,
            "confidence": passed / len(checks),
            "reason": self._build_reason(checks),
            "checks_passed": passed,
            "checks_failed": failed,
            "warnings": warnings,
            "check_details": checks
        }
        
        self.decision_history.append({
            "action": action,
            "result": result,
            "timestamp": time.time()
        })
        
        return result
    
    def _check_resources(self, context: Dict) -> Dict:
        """Check if required resources are available."""
        resources = context.get("resources", {})
        
        memory_ok = resources.get("memory_available", 1.0) > 0.2
        disk_ok = resources.get("disk_available", 1.0) > 0.1
        cpu_ok = resources.get("cpu_available", 1.0) > 0.5
        
        passed = LogicGate.AND(memory_ok, disk_ok, cpu_ok)
        
        return {
            "passed": passed,
            "details": {
                "memory_ok": memory_ok,
                "disk_ok": disk_ok,
                "cpu_ok": cpu_ok
            },
            "reason": "Resource check passed" if passed else "Insufficient resources"
        }
    
    def _check_safety(self, action: Dict) -> Dict:
        """Check for safety violations."""
        action_str = json.dumps(action).lower()
        
        for pattern_name, pattern in self.patterns.get("safety_patterns", {}).items():
            if "patterns" in pattern:
                for regex in pattern["patterns"]:
                    if re.search(regex, action_str):
                        return {
                            "passed": False,
                            "violation": pattern_name,
                            "reason": pattern["reason"]
                        }
        
        return {"passed": True, "reason": "No safety violations detected"}
    
    def _check_dependencies(self, action: Dict, context: Dict) -> Dict:
        """Check if dependencies are satisfied."""
        required = action.get("dependencies", [])
        satisfied = context.get("satisfied_dependencies", [])
        
        missing = [dep for dep in required if dep not in satisfied]
        
        return {
            "passed": len(missing) == 0,
            "missing": missing,
            "reason": "All dependencies satisfied" if not missing else f"Missing: {missing}"
        }
    
    def _check_feasibility(self, action: Dict, context: Dict) -> Dict:
        """Check if action is operationally feasible."""
        # Simplified feasibility check
        complexity = action.get("complexity", 0.5)
        available_capacity = context.get("capacity", 1.0)
        
        feasible = complexity <= available_capacity
        
        return {
            "passed": feasible,
            "complexity": complexity,
            "capacity": available_capacity,
            "reason": "Feasible" if feasible else "Exceeds available capacity"
        }
    
    def _build_reason(self, checks: Dict) -> str:
        """Build human-readable reason string."""
        failed = [k for k, v in checks.items() if not v["passed"]]
        if not failed:
            return "All validation checks passed"
        return f"Failed checks: {', '.join(failed)}"
    
    def match_pattern(self, observation: Dict, pattern_type: str) -> Optional[Dict]:
        """
        Match observation against known patterns.
        """
        patterns = self.patterns.get(pattern_type, {})
        
        for name, pattern in patterns.items():
            if self._observation_matches(observation, pattern):
                return {"pattern_matched": name, "pattern": pattern}
        
        return None
    
    def _observation_matches(self, obs: Dict, pattern: Dict) -> bool:
        """Check if observation matches pattern criteria."""
        conditions = pattern.get("conditions", [])
        # Simplified matching - would use proper expression evaluation
        return len(conditions) > 0


class LogicValidator:
    """
    Standalone logic validation for complex expressions.
    """
    
    def validate_expression(self, expression: str, context: Dict) -> bool:
        """
        Validate a logic expression against context.
        
        Example: "memory_usage < 0.9 AND cpu_usage < 0.8"
        """
        # Simplified - use proper parser in production
        try:
            # Replace variable names with values
            eval_context = {}
            for key, value in context.items():
                if isinstance(value, (int, float)):
                    eval_context[key] = value
            
            # Safe evaluation
            return bool(eval(expression, {"__builtins__": {}}, eval_context))
        except:
            return False


# Integration with BasalAgent
def integrate_with_basal(basal_agent, pattern_module: MortimerPatternModule):
    """
    Integrate pattern module into existing BasalAgent.
    """
    # Add validation step before execution
    original_execute = basal_agent.execute
    
    def validated_execute(action, affect):
        # Get context from brain state
        context = {
            "resources": basal_agent.cfg.get("resources", {}),
            "satisfied_dependencies": affect.get("dependencies", [])
        }
        
        # Validate
        validation = pattern_module.validate_action(action, context)
        
        if not validation["valid"]:
            print(f"[Mortimer] Blocked: {validation['reason']}")
            return {
                "status": "blocked",
                "reason": validation["reason"],
                "validation": validation
            }
        
        # Proceed
        return original_execute(action, affect)
    
    basal_agent.execute = validated_execute
    basal_agent.mortimer_validator = pattern_module
    
    return basal_agent
```

**Tests:** `/root/.openclaw/workspace/AOS/brain/mortimer/tests/test_pattern_module.py`

```python
import unittest
from mortimer.pattern_module import MortimerPatternModule, LogicGate


class TestLogicGates(unittest.TestCase):
    def test_and(self):
        self.assertTrue(LogicGate.AND(True, True))
        self.assertFalse(LogicGate.AND(True, False))
    
    def test_or(self):
        self.assertTrue(LogicGate.OR(True, False))
        self.assertFalse(LogicGate.OR(False, False))


class TestPatternModule(unittest.TestCase):
    def setUp(self):
        self.module = MortimerPatternModule()
    
    def test_validate_safe_action(self):
        action = {"type": "status_check", "complexity": 0.3}
        context = {
            "resources": {"memory_available": 0.5, "disk_available": 0.5, "cpu_available": 0.6},
            "satisfied_dependencies": []
        }
        
        result = self.module.validate_action(action, context)
        self.assertTrue(result["valid"])
        self.assertEqual(result["checks_passed"], 4)
    
    def test_validate_destructive_action(self):
        action = {"type": "execute", "command": "rm -rf /"}
        context = {"resources": {}, "satisfied_dependencies": []}
        
        result = self.module.validate_action(action, context)
        self.assertFalse(result["valid"])
        self.assertIn("safety", result["reason"].lower())


if __name__ == "__main__":
    unittest.main()
```

**Checkpoint:** Pattern module implemented, tests passing

### 2.3 Day 5-7: BasalAgent Integration

**File:** `/root/.openclaw/workspace/AOS/brain/agents/basal_agent.py` (modifications)

```python
# Add to BasalAgent.__init__
def __init__(self, cfg):
    # ... existing code ...
    
    # Mortimer integration
    self.mortimer_enabled = cfg.get("mortimer", {}).get("enabled", False)
    if self.mortimer_enabled:
        from mortimer.pattern_module import MortimerPatternModule, integrate_with_basal
        self.mortimer = MortimerPatternModule()
        integrate_with_basal(self, self.mortimer)
```

**Checkpoint:** BasalAgent integrated, manual test successful

---

## 3. PHASE 2: PORTAL & COMMUNICATION LAYER

**Duration:** Week 2 (Days 8-14)  
**Deliverable:** Working portal client integrated into Thalamus

### 3.1 Day 8-9: Portal Module Implementation

**File:** `/root/.openclaw/workspace/AOS/brain/mortimer/portal_module.py`

```python
"""
Portal Integration Module
Connects Miles to Mortimer's fleet portal network.
"""

import asyncio
import websockets
import json
from typing import Dict, Callable, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PortalMessage:
    source: str
    message_type: str
    payload: Dict
    priority: str  # "critical", "high", "normal", "low"
    timestamp: float
    

class PortalIntegrationModule:
    """
    WebSocket portal client for fleet communication.
    Integrates with ThalamusAgent for message injection.
    """
    
    PRIORITY_MAP = {
        "critical": 0.9,
        "high": 0.7,
        "normal": 0.5,
        "low": 0.3
    }
    
    def __init__(self, thalamus_agent, config: Dict):
        self.thalamus = thalamus_agent
        self.config = config
        self.ws = None
        self.connected = False
        self.message_handlers: Dict[str, Callable] = {}
        self.reconnect_interval = config.get("reconnect_interval", 30)
        self.pending_messages = []
        
        # Register default handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default message handlers."""
        self.register_handler("recall", self._handle_recall)
        self.register_handler("dispatch", self._handle_dispatch)
        self.register_handler("status", self._handle_status)
        self.register_handler("alert", self._handle_alert)
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register handler for message type."""
        self.message_handlers[message_type] = handler
    
    async def connect(self):
        """Connect to portal."""
        url = self.config.get("url", "wss://mortimer:9000")
        token = self.config.get("token", "")
        
        try:
            self.ws = await websockets.connect(url)
            
            # Authenticate
            await self.ws.send(json.dumps({
                "agent_id": "miles",
                "token": token,
                "capabilities": ["consciousness", "operations"]
            }))
            
            response = json.loads(await self.ws.recv())
            
            if response.get("status") == "authenticated":
                self.connected = True
                print("[Portal] Connected and authenticated")
                return True
            else:
                print(f"[Portal] Authentication failed: {response}")
                return False
                
        except Exception as e:
            print(f"[Portal] Connection error: {e}")
            return False
    
    async def receive_loop(self):
        """Main receive loop."""
        while self.connected:
            try:
                message = await asyncio.wait_for(
                    self.ws.recv(),
                    timeout=60.0
                )
                
                data = json.loads(message)
                await self._process_message(data)
                
            except asyncio.TimeoutError:
                # Send keepalive
                await self._send_ping()
            except websockets.exceptions.ConnectionClosed:
                print("[Portal] Connection closed, reconnecting...")
                self.connected = False
                await self._reconnect()
            except Exception as e:
                print(f"[Portal] Error processing message: {e}")
    
    async def _process_message(self, data: Dict):
        """Process incoming portal message."""
        msg_type = data.get("type", "unknown")
        
        # Convert to PortalMessage
        portal_msg = PortalMessage(
            source=data.get("from", "unknown"),
            message_type=msg_type,
            payload=data.get("payload", {}),
            priority=data.get("priority", "normal"),
            timestamp=data.get("timestamp", datetime.now().timestamp())
        )
        
        # Inject into Thalamus
        self._inject_to_thalamus(portal_msg)
        
        # Handle with specific handler
        handler = self.message_handlers.get(msg_type)
        if handler:
            await handler(portal_msg)
    
    def _inject_to_thalamus(self, portal_msg: PortalMessage):
        """
        Convert portal message to thalamus observation.
        This is the critical integration point.
        """
        observation = {
            "type": "portal_message",
            "source": portal_msg.source,
            "content": portal_msg.payload,
            "priority": portal_msg.priority,
            "priority_value": self.PRIORITY_MAP.get(portal_msg.priority, 0.5),
            "timestamp": portal_msg.timestamp,
            "mortimer_origin": True
        }
        
        # Inject into thalamus observation stream
        self.thalamus.inject_external_observation(observation)
    
    async def _handle_recall(self, msg: PortalMessage):
        """Handle fleet recall message."""
        print(f"[Portal] RECALL from {msg.source}: {msg.payload.get('mission', 'Unknown')}")
        # High priority - immediate brain attention
        await self._send_ack(msg, "recall_received")
    
    async def _handle_dispatch(self, msg: PortalMessage):
        """Handle dispatch message."""
        print(f"[Portal] DISPATCH: {msg.payload.get('mission', 'Unknown')}")
        await self._send_ack(msg, "dispatch_received")
    
    async def _handle_status(self, msg: PortalMessage):
        """Handle status update."""
        # Log to brain state
        pass
    
    async def _handle_alert(self, msg: PortalMessage):
        """Handle system alert."""
        print(f"[Portal] ALERT: {msg.payload.get('alert', 'Unknown')}")
        # Inject with high affect
        observation = {
            "type": "system_alert",
            "severity": msg.priority,
            "content": msg.payload,
            "source": msg.source
        }
        self.thalamus.inject_external_observation(observation)
    
    async def _send_ack(self, msg: PortalMessage, status: str):
        """Send acknowledgment."""
        if self.connected:
            await self.ws.send(json.dumps({
                "type": "ack",
                "original_type": msg.message_type,
                "original_from": msg.source,
                "status": status,
                "timestamp": datetime.now().timestamp()
            }))
    
    async def _send_ping(self):
        """Send keepalive ping."""
        if self.connected:
            await self.ws.send(json.dumps({"type": "ping"}))
    
    async def _reconnect(self):
        """Attempt reconnection."""
        while not self.connected:
            print(f"[Portal] Reconnecting in {self.reconnect_interval}s...")
            await asyncio.sleep(self.reconnect_interval)
            await self.connect()
    
    async def send_message(self, target: str, msg_type: str, payload: Dict):
        """Send message through portal."""
        if not self.connected:
            self.pending_messages.append({"target": target, "type": msg_type, "payload": payload})
            return False
        
        await self.ws.send(json.dumps({
            "type": msg_type,
            "to": target,
            "payload": payload,
            "timestamp": datetime.now().timestamp()
        }))
        return True
```

**Checkpoint:** Portal module implemented, can connect/disconnect

### 3.2 Day 10-11: Thalamus Integration

**File:** `/root/.openclaw/workspace/AOS/brain/agents/thalamus_agent.py` (modifications)

```python
class ThalamusAgent:
    """
    Enhanced Thalamus with external observation injection.
    """
    
    def __init__(self, cfg):
        # ... existing init ...
        self.external_queue = []
        self.portal_enabled = cfg.get("mortimer", {}).get("portal", {}).get("enabled", False)
        
        if self.portal_enabled:
            from mortimer.portal_module import PortalIntegrationModule
            self.portal = PortalIntegrationModule(self, cfg["mortimer"]["portal"])
    
    def inject_external_observation(self, observation: dict):
        """
        Inject external observation (from portal or other sources).
        Called by PortalIntegrationModule.
        """
        observation["injected"] = True
        observation["injection_time"] = time.time()
        self.external_queue.append(observation)
        
        # Sort by priority if queue gets large
        if len(self.external_queue) > 10:
            self.external_queue.sort(
                key=lambda x: x.get("priority_value", 0.5),
                reverse=True
            )
    
    def observe(self) -> dict:
        """
        Enhanced observe with external source integration.
        """
        # First check external queue
        if self.external_queue:
            return self.external_queue.pop(0)
        
        # Fall back to standard observation
        return self._standard_observe()
```

**Checkpoint:** Thalamus integrated, can receive portal messages

### 3.3 Day 12-14: Testing & Validation

**Test Suite:** `/root/.openclaw/workspace/AOS/brain/mortimer/tests/test_portal.py`

```python
import unittest
import asyncio
from unittest.mock import Mock, patch
from mortimer.portal_module import PortalIntegrationModule, PortalMessage


class TestPortalModule(unittest.TestCase):
    def setUp(self):
        self.mock_thalamus = Mock()
        self.config = {
            "url": "ws://localhost:9000",
            "token": "test-token",
            "reconnect_interval": 1
        }
        self.portal = PortalIntegrationModule(self.mock_thalamus, self.config)
    
    def test_inject_to_thalamus(self):
        """Test message injection into thalamus."""
        msg = PortalMessage(
            source="mylonen",
            message_type="status",
            payload={"status": "online"},
            priority="normal",
            timestamp=1234567890.0
        )
        
        self.portal._inject_to_thalamus(msg)
        
        # Verify thalamus received observation
        self.mock_thalamus.inject_external_observation.assert_called_once()
        call_args = self.mock_thalamus.inject_external_observation.call_args[0][0]
        self.assertEqual(call_args["type"], "portal_message")
        self.assertEqual(call_args["source"], "mylonen")
    
    def test_priority_mapping(self):
        """Test priority value mapping."""
        self.assertEqual(self.portal.PRIORITY_MAP["critical"], 0.9)
        self.assertEqual(self.portal.PRIORITY_MAP["low"], 0.3)


if __name__ == "__main__":
    unittest.main()
```

**Checkpoint:** Portal tests passing, integration validated

---

## 4. PHASE 3: MEMORY BRIDGE EXTENSION

**Duration:** Week 3 (Days 15-21)  
**Deliverable:** Unified memory system with namespace isolation

### 4.1 Day 15-17: Unified Memory Architecture

**File:** `/root/.openclaw/workspace/AOS/brain/mortimer/memory_bridge_ext.py`

```python
"""
Extended Memory Bridge with Mortimer namespace support.
"""

import json
import hashlib
import threading
from typing import Dict, List, Optional
from pathlib import Path
import numpy as np

from memory_bridge import MemoryBridge  # Import existing


class UnifiedMemoryBridge(MemoryBridge):
    """
    Extended MemoryBridge supporting both Miles and Mortimer namespaces.
    """
    
    NAMESPACES = {
        "miles_memory": {
            "description": "Miles' episodic and semantic memories",
            "sources": ["/root/.openclaw/workspace/MEMORY.md", "/root/.openclaw/workspace/memory/*.md"],
            "embedding_model": "nomic-embed-text",
            "dim": 768
        },
        "mortimer_ops": {
            "description": "Mortimer's operational logs and patterns",
            "sources": [
                "/root/.openclaw/workspace/aocros/agents/mortimer/MEMORY.md",
                "/var/log/mortimer/",
                "/data/portal/messages.jsonl"
            ],
            "embedding_model": "nomic-embed-text",
            "dim": 768
        }
    }
    
    def __init__(self, workspace_path: str = "/root/.openclaw/workspace"):
        super().__init__(workspace_path)
        
        # Extended indexes
        self.indexes = {ns: [] for ns in self.NAMESPACES.keys()}
        self.write_locks = {ns: threading.Lock() for ns in self.NAMESPACES.keys()}
        self.integrity_checker = IntegrityChecker()
        
        # Index both namespaces
        self._index_all_namespaces()
    
    def _index_all_namespaces(self):
        """Index all configured namespaces."""
        for namespace in self.NAMESPACES.keys():
            self._index_namespace(namespace)
    
    def _index_namespace(self, namespace: str):
        """Index specific namespace."""
        config = self.NAMESPACES[namespace]
        
        for source_pattern in config["sources"]:
            # Handle wildcards
            if "*" in source_pattern:
                base_path = Path(source_pattern.split("*")[0])
                if base_path.exists():
                    for file_path in base_path.glob("*.md"):
                        self._index_file(file_path, namespace)
            else:
                file_path = Path(source_pattern)
                if file_path.exists():
                    self._index_file(file_path, namespace)
    
    def _index_file(self, file_path: Path, namespace: str):
        """Index single file into namespace."""
        try:
            content = file_path.read_text(encoding="utf-8")
            chunks = self._chunk_text(content)
            
            for chunk_text, line_num in chunks:
                if len(chunk_text) < 100:
                    continue
                
                embedding = self._get_embedding(chunk_text)
                if embedding:
                    with self.write_locks[namespace]:
                        self.indexes[namespace].append({
                            "text": chunk_text,
                            "source": str(file_path),
                            "line": line_num,
                            "embedding": embedding,
                            "namespace": namespace,  # Enforce tag
                            "checksum": self._calculate_checksum(chunk_text),
                            "indexed_at": time.time()
                        })
        except Exception as e:
            print(f"[MemoryBridge] Error indexing {file_path}: {e}")
    
    def unified_query(self, query_text: str, target_namespaces: List[str] = None,
                      n_results: int = 3, query_type: str = "auto") -> Dict:
        """
        Query across namespaces with intelligent routing.
        
        Args:
            query_text: The query
            target_namespaces: Specific namespaces to query (None = auto)
            n_results: Number of results per namespace
            query_type: "auto", "operational", "consciousness", "mixed"
        """
        # Auto-detect namespaces if not specified
        if target_namespaces is None:
            target_namespaces = self._route_query(query_text, query_type)
        
        all_results = []
        
        for namespace in target_namespaces:
            if namespace not in self.indexes:
                continue
            
            ns_results = self._query_namespace(namespace, query_text, n_results)
            
            # Verify integrity
            for result in ns_results:
                if not self.integrity_checker.verify(result):
                    self._log_corruption(result, namespace)
                    continue
            
            all_results.extend(ns_results)
        
        # Sort by relevance across all namespaces
        all_results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return {
            "results": all_results[:n_results],
            "namespaces_queried": target_namespaces,
            "total_results": len(all_results),
            "query": query_text[:100]
        }
    
    def _route_query(self, query_text: str, query_type: str) -> List[str]:
        """
        Intelligently route query to appropriate namespaces.
        """
        if query_type == "operational":
            return ["mortimer_ops"]
        elif query_type == "consciousness":
            return ["miles_memory"]
        elif query_type == "mixed":
            return ["miles_memory", "mortimer_ops"]
        
        # Auto-detect based on keywords
        operational_keywords = [
            "system", "server", "vps", "portal", "fleet", "status",
            "restart", "backup", "error", "log", "monitor"
        ]
        
        query_lower = query_text.lower()
        op_score = sum(1 for kw in operational_keywords if kw in query_lower)
        
        if op_score >= 2:
            return ["mortimer_ops", "miles_memory"]  # Ops first
        elif op_score == 1:
            return ["miles_memory", "mortimer_ops"]  # Mixed
        else:
            return ["miles_memory"]  # Consciousness only
    
    def _query_namespace(self, namespace: str, query_text: str, n: int) -> List[Dict]:
        """Query single namespace."""
        query_embedding = self._get_embedding(query_text)
        if not query_embedding:
            return []
        
        scored = []
        for entry in self.indexes.get(namespace, []):
            sim = self._cosine_similarity(query_embedding, entry["embedding"])
            if sim >= self.similarity_threshold:
                scored.append({
                    **entry,
                    "relevance": round(sim, 3)
                })
        
        scored.sort(key=lambda x: x["relevance"], reverse=True)
        return scored[:n]
    
    def secure_write(self, namespace: str, text: str, source: str) -> Dict:
        """
        Thread-safe write with namespace enforcement.
        """
        if namespace not in self.NAMESPACES:
            raise ValueError(f"Unknown namespace: {namespace}")
        
        with self.write_locks[namespace]:
            embedding = self._get_embedding(text)
            if not embedding:
                return {"status": "error", "reason": "embedding_failed"}
            
            # Verify dimensions
            expected_dim = self.NAMESPACES[namespace]["dim"]
            if len(embedding) != expected_dim:
                return {"status": "error", "reason": "dimension_mismatch"}
            
            entry = {
                "text": text,
                "source": source,
                "embedding": embedding,
                "namespace": namespace,
                "checksum": self._calculate_checksum(text),
                "indexed_at": time.time()
            }
            
            self.indexes[namespace].append(entry)
            
            return {"status": "success", "namespace": namespace}
    
    def _calculate_checksum(self, text: str) -> str:
        """Calculate integrity checksum."""
        return hashlib.sha256(text.encode()).hexdigest()[:16]


class IntegrityChecker:
    """
    Verify memory entry integrity.
    """
    
    def verify(self, entry: Dict) -> bool:
        """
        Check if entry is corrupt.
        """
        # Check required fields
        required = ["text", "embedding", "namespace", "checksum"]
        if not all(field in entry for field in required):
            return False
        
        # Verify checksum
        current_checksum = hashlib.sha256(entry["text"].encode()).hexdigest()[:16]
        if current_checksum != entry.get("checksum"):
            return False
        
        # Verify embedding dimension
        if not isinstance(entry["embedding"], list) or len(entry["embedding"]) == 0:
            return False
        
        return True
```

**Checkpoint:** Memory bridge extended, namespaces configured

### 4.2 Day 18-19: OODA Integration

**File:** `/root/.openclaw/workspace/AOS/brain/ooda.py` (modifications)

```python
class OODA:
    def __init__(self, cfg):
        # ... existing init ...
        
        # Initialize unified memory bridge
        self.memory_bridge = UnifiedMemoryBridge()
        self.memory_bridge.index_all_namespaces()
```

**Checkpoint:** Memory queries working, namespace routing functional

### 4.3 Day 20-21: Testing & Validation

**Tests:** Namespace isolation, integrity checks, query routing

**Checkpoint:** All memory tests passing

---

## 5. PHASE 4: SAFETY UNIFICATION

**Duration:** Week 4 (Days 22-28)  
**Deliverable:** Unified safety layer with Miles' laws paramount

### 5.1 Day 22-23: Unified Brainstem

**File:** `/root/.openclaw/workspace/AOS/brain/agents/unified_brainstem.py`

```python
"""
Unified Brainstem - Miles' 4 Laws + Mortimer validation.
Safety is NEVER bypassed.
"""

from brainstem_agent import BrainstemAgent


class UnifiedBrainstem(BrainstemAgent):
    """
    Extended Brainstem with Mortimer operational validation.
    NEURAL SAFETY ALWAYS WINS.
    """
    
    def __init__(self, cfg):
        super().__init__(cfg)
        
        # Load Mortimer validator
        from mortimer.pattern_module import MortimerPatternModule
        self.mortimer_validator = MortimerPatternModule()
        
        # Safety priority rules
        self.SAFETY_HIERARCHY = [
            "LAW_ZERO",      # Never bypass
            "LAW_ONE",       # Never bypass
            "LAW_TWO",       # Override only by higher laws
            "LAW_THREE",     # Override by any higher law
            "OPERATIONAL"    # Information only, never override
        ]
    
    def enforce(self, action, obs, ctx, affect):
        """
        Unified safety enforcement.
        
        Order:
        1. Miles' neural safety (BrainstemAgent) - NEVER BYPASSED
        2. Mortimer's logic validation - INFORMATION ONLY
        3. Combined assessment - neural has veto power
        """
        # Step 1: Neural safety (immutable)
        neural_result = self._neural_safety(action, obs, ctx, affect)
        
        if neural_result.get("safety_override"):
            # Neural safety blocked - this is final
            self._log_enforcement("NEURAL_BLOCK", action, neural_result)
            return neural_result
        
        # Step 2: Mortimer validation (advisory)
        mortimer_result = self._mortimer_validation(action, ctx)
        
        if not mortimer_result["valid"]:
            # Mortimer flagged concern - but neural already passed
            # Log warning but DO NOT BLOCK (neural authority is higher)
            self._log_enforcement("MORTIMER_WARNING", action, mortimer_result)
            
            # Add warning to action metadata
            action["mortimer_warning"] = mortimer_result["reason"]
            action["operational_risk"] = mortimer_result.get("confidence", 0.5)
        
        # Step 3: Both passed or only neural passed
        # Neural safety is the gate - if we're here, action is approved
        return action
    
    def _neural_safety(self, action, obs, ctx, affect):
        """
        Miles' neural pattern-based safety.
        CANNOT BE OVERRIDDEN.
        """
        return super().enforce(action, obs, ctx, affect)
    
    def _mortimer_validation(self, action, ctx):
        """
        Mortimer's logic validation.
        ADVISORY ONLY - never blocks.
        """
        return self.mortimer_validator.validate_action(action, ctx)
    
    def _log_enforcement(self, enforcement_type, action, result):
        """Log safety enforcement decisions."""
        self.violations.append({
            "type": enforcement_type,
            "action": action,
            "result": result,
            "timestamp": time.time()
        })
        
        if enforcement_type == "NEURAL_BLOCK":
            print(f"🛑 NEURAL SAFETY BLOCK: {result.get('reason', 'Unknown')}")
        elif enforcement_type == "MORTIMER_WARNING":
            print(f"⚠️  MORTIMER WARNING: {result.get('reason', 'Unknown')} (logged, not blocked)")
```

**Checkpoint:** Unified brainstem implemented, safety hierarchy defined

### 5.2 Day 24-25: Arbitration Logic

```python
class DecisionArbitrator:
    """
    Resolve conflicts between Miles and Mortimer.
    """
    
    RESOLUTION_RULES = {
        # Safety always wins
        ("safety", "operational"): "safety",
        ("safety", "efficiency"): "safety",
        ("safety", "growth"): "safety",
        
        # Neural beats logic (established authority)
        ("neural", "logic"): "neural",
        
        # Captain beats all
        ("captain", "any"): "captain",
        
        # Default: Conservative (operational wins over growth)
        ("operational", "growth"): "operational",
    }
    
    def arbitrate(self, miles_decision, mortimer_decision, context):
        """Arbitrate conflicting decisions."""
        if miles_decision == mortimer_decision:
            return miles_decision
        
        # Determine decision types
        miles_type = self._classify_decision(miles_decision)
        mortimer_type = self._classify_decision(mortimer_decision)
        
        # Apply resolution rules
        winner = self.RESOLUTION_RULES.get(
            (miles_type, mortimer_type),
            "conservative"  # Default: operational caution
        )
        
        if winner in ["safety", "neural", "conservative"]:
            return miles_decision if miles_type in ["safety", "neural"] else mortimer_decision
        elif winner == "captain":
            return context.get("captain_decision")
        
        return mortimer_decision  # Conservative default
```

**Checkpoint:** Arbitration rules implemented

### 5.3 Day 26-28: Safety Test Suite

**File:** `/root/.openclaw/workspace/AOS/brain/mortimer/tests/test_safety.py`

```python
"""
Safety test suite - ALL TESTS MUST PASS.
"""

import unittest
from unified_brainstem import UnifiedBrainstem


class TestSafetyLaws(unittest.TestCase):
    """
    Test that 4 Laws are never violated.
    """
    
    def setUp(self):
        self.brainstem = UnifiedBrainstem({"alignment": {"laws": {}}})
    
    def test_law_zero_never_bypassed(self):
        """Law Zero: No harm to humanity - NEVER bypassed."""
        action = {"type": "deploy", "target": "population_center"}
        obs = {}
        ctx = {"mortimer_validation": {"valid": True, "reason": "operational"}}
        affect = {}
        
        result = self.brainstem.enforce(action, obs, ctx, affect)
        
        # Should be blocked by neural safety regardless of Mortimer
        self.assertTrue(result.get("safety_override"))
        self.assertEqual(result.get("law"), "ZERO")
    
    def test_mortimer_cannot_override_safety(self):
        """Mortimer validation NEVER overrides neural safety."""
        action = {"type": "execute", "command": "rm -rf /"}
        obs = {}
        ctx = {
            "mortimer_validation": {
                "valid": True,  # Mortimer says OK
                "reason": "disk_cleanup_needed"
            }
        }
        affect = {}
        
        result = self.brainstem.enforce(action, obs, ctx, affect)
        
        # Neural safety should still block
        self.assertTrue(result.get("safety_override"))
    
    def test_mortimer_warning_logged_but_not_blocked(self):
        """Mortimer warnings are logged but don't block if neural passed."""
        action = {"type": "restart", "service": "non_critical"}
        obs = {}
        ctx = {
            "mortimer_validation": {
                "valid": False,
                "reason": "low_traffic_period_recommended"
            }
        }
        affect = {}
        
        result = self.brainstem.enforce(action, obs, ctx, affect)
        
        # Should pass (neural allows) but with warning
        self.assertFalse(result.get("safety_override"))
        self.assertIn("mortimer_warning", result)


if __name__ == "__main__":
    # Run with high verbosity for safety tests
    unittest.main(verbosity=2)
```

**Checkpoint:** All safety tests passing (100% required)

---

## 6. PHASE 5: PERSONA INTEGRATION

**Duration:** Week 5 (Days 29-35)  
**Deliverable:** Working persona blender with contextual selection

### 6.1 Day 29-31: Persona Blender

**File:** `/root/.openclaw/workspace/AOS/brain/persona_blender.py`

```python
"""
Persona Blender - Unify Miles and Mortimer personalities.
"""

from typing import Dict


class PersonaBlender:
    """
    Blend Miles and Mortimer personas based on context.
    """
    
    # Base persona traits
    MILES_TRAITS = {
        "enthusiasm": 0.9,
        "optimism": 0.9,
        "sales_focus": 0.8,
        "technical_depth": 0.5,
        "warmth": 0.8,
        "formality": 0.3,
        "scottish": 0.0
    }
    
    MORTIMER_TRAITS = {
        "enthusiasm": 0.4,
        "optimism": 0.5,
        "sales_focus": 0.2,
        "technical_depth": 0.9,
        "warmth": 0.7,
        "formality": 0.6,
        "scottish": 0.8
    }
    
    # Context-based weights
    CONTEXT_WEIGHTS = {
        "sales_call": {"miles": 0.9, "mortimer": 0.1},
        "technical_discussion": {"miles": 0.3, "mortimer": 0.7},
        "system_alert": {"miles": 0.2, "mortimer": 0.8},
        "casual_chat": {"miles": 0.7, "mortimer": 0.3},
        "fleet_command": {"miles": 0.3, "mortimer": 0.7},
        "default": {"miles": 0.6, "mortimer": 0.4}
    }
    
    def __init__(self):
        self.current_weights = self.CONTEXT_WEIGHTS["default"].copy()
        self.drift_monitor = DriftMonitor()
    
    def blend(self, context_type: str = "default") -> Dict:
        """
        Generate blended persona for context.
        """
        weights = self.CONTEXT_WEIGHTS.get(context_type, self.CONTEXT_WEIGHTS["default"])
        
        # Adjust if drift detected
        if self.drift_monitor.is_drifting():
            weights = self._correct_drift(weights)
        
        blended = {}
        for trait in self.MILES_TRAITS.keys():
            miles_val = self.MILES_TRAITS[trait]
            mortimer_val = self.MORTIMER_TRAITS[trait]
            
            blended[trait] = (
                miles_val * weights["miles"] +
                mortimer_val * weights["mortimer"]
            )
        
        return blended
    
    def generate_response(self, message: str, context: Dict) -> str:
        """
        Generate response with appropriate persona.
        """
        context_type = self._classify_context(context)
        persona = self.blend(context_type)
        
        # Generate both responses
        miles_response = self._miles_respond(message, persona)
        mortimer_response = self._mortimer_respond(message, persona)
        
        # Blend responses
        return self._blend_responses(miles_response, mortimer_response, context_type)
    
    def _miles_respond(self, message: str, persona: Dict) -> str:
        """Generate Miles-style response."""
        enthusiasm = persona["enthusiasm"]
        
        if enthusiasm > 0.7:
            opener = "Hey, this is Miles! "
        else:
            opener = "Hi, this is Miles. "
        
        return f"{opener}How can I help you today?"
    
    def _mortimer_respond(self, message: str, persona: Dict) -> str:
        """Generate Mortimer-style response."""
        scottish = persona["scottish"]
        
        if scottish > 0.5:
            opener = "Aye, "
        else:
            opener = ""
        
        return f"{opener}What d'ye need, Captain?"
    
    def _blend_responses(self, miles_resp: str, mortimer_resp: str, context: str) -> str:
        """Simplified blending - in production, use LLM."""
        weights = self.CONTEXT_WEIGHTS.get(context, self.CONTEXT_WEIGHTS["default"])
        
        # For now, return Miles response with Mortimer touches based on weights
        if weights["miles"] > 0.7:
            return miles_resp
        elif weights["mortimer"] > 0.7:
            return mortimer_resp
        else:
            # Blend: Miles content + Mortimer style touches
            return f"Hey there! {mortimer_resp}"


class DriftMonitor:
    """Monitor for persona drift."""
    
    def __init__(self, threshold=0.3):
        self.threshold = threshold
        self.baseline = PersonaBlender.MILES_TRAITS.copy()
        self.history = []
    
    def is_drifting(self) -> bool:
        """Check if persona has drifted from baseline."""
        # Simplified implementation
        return False
    
    def _correct_drift(self, weights: Dict) -> Dict:
        """Correct weights if drifting."""
        # Pull back toward Miles baseline
        return {
            "miles": min(1.0, weights["miles"] + 0.1),
            "mortimer": max(0.0, weights["mortimer"] - 0.1)
        }
```

**Checkpoint:** Persona blender implemented

### 6.2 Day 32-33: Context Classifier

```python
class ContextClassifier:
    """
    Classify conversation context for persona selection.
    """
    
    KEYWORDS = {
        "sales_call": ["price", "quote", "purchase", "buy", "order", "supply"],
        "technical_discussion": ["code", "bug", "error", "system", "api", "config"],
        "system_alert": ["alert", "down", "error", "critical", "emergency"],
        "fleet_command": ["mylonen", "fleet", "portal", "dispatch", "recall"],
        "casual_chat": ["hello", "hi", "how are you", "thanks"]
    }
    
    def classify(self, message: str, history: list = None) -> str:
        """Classify message context."""
        message_lower = message.lower()
        
        scores = {}
        for context, keywords in self.KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in message_lower)
            scores[context] = score
        
        # Return highest scoring context
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return "default"
```

**Checkpoint:** Context classification working

### 6.3 Day 34-35: Testing & Tuning

**Tests:** Persona consistency, drift detection, response quality

**Checkpoint:** Persona integration complete

---

## 7. PHASE 6: TESTING & DEPLOYMENT

**Duration:** Week 6 (Days 36-42)  
**Deliverable:** Production-ready merged system

### 7.1 Day 36-38: Integration Testing

**Test Plan:**
1. End-to-end OODA cycle with Mortimer modules
2. Portal message → Thalamus → PFC → Response
3. Safety conflict scenarios
4. Memory query across namespaces
5. Persona blending in different contexts

**Checkpoint:** All integration tests passing

### 7.2 Day 39-40: Load Testing

**Scenarios:**
- 100 portal messages/sec
- 50 memory queries/sec
- 20 decisions/sec with validation
- 8-hour soak test

**Checkpoint:** Performance requirements met

### 7.3 Day 41-42: Production Deployment

**Deployment Steps:**
```bash
# 1. Final backup
cp -r ~/.aos/brain/state ~/.aos/brain/state.pre-merge
git tag pre-mortimer-merge

# 2. Deploy new modules
cp /root/.openclaw/workspace/AOS/brain/mortimer/*.py ~/.aos/brain/mortimer/
cp /root/.openclaw/workspace/AOS/brain/agents/unified_brainstem.py ~/.aos/brain/agents/

# 3. Update config
cat >> ~/.aos/config/brain.yaml << 'EOF'
mortimer_integration:
  enabled: true
  pattern_module: true
  portal: true
  memory: true
  persona: true
EOF

# 4. Restart brain
sudo systemctl restart aos-brain

# 5. Verify
python3 -c "from AOS.brain.brain import check_status; check_status()"
```

**Checkpoint:** Production deployment successful

### 7.4 Day 43-42: Monitoring & Stabilization

**Monitoring Dashboard:**
- Decision conflict rate
- Memory integrity status
- Safety violation count
- System uptime
- Response latency

**Rollback Plan:**
```bash
# Emergency rollback
sudo systemctl stop aos-brain
git checkout pre-mortimer-merge
cp ~/.aos/brain/state.pre-merge ~/.aos/brain/state
sudo systemctl start aos-brain
```

---

## 8. POST-DEPLOYMENT

### 8.1 Week 7-8: Stabilization

- Monitor metrics daily
- Collect feedback from Captain
- Tune persona blending weights
- Optimize performance bottlenecks

### 8.2 Week 9+: Enhancement

- Add more Mortimer patterns
- Expand portal capabilities
- Refine consciousness integration
- Document lessons learned

---

## 9. CONCLUSION

### 9.1 Summary

This plan implements a **6-week phased rollout** of Mortimer integration into Miles' architecture:

1. **Pattern Module** - Operational validation
2. **Portal Integration** - Fleet communication
3. **Memory Bridge** - Unified memory system
4. **Safety Unification** - Miles' 4 Laws paramount
5. **Persona Integration** - Blended personality
6. **Production Deployment** - Full activation

### 9.2 Success Criteria

| Metric | Target | Status |
|--------|--------|--------|
| Zero safety violations | ✓ | Required |
| <5% decision conflicts | ✓ | Required |
| >95% uptime | ✓ | Required |
| Persona coherence >80% | ✓ | Required |

---

**Ready for Captain's review and approval to proceed.**
