# PM01 AOS Bridge

**Secure gRPC bridge for AOS Brain ↔ EngineAI PM01 Humanoid Robot**

Security Level: **P0 Hardened** (per Jordan requirements)

---

## Architecture

```
AOS Brain (Unix Socket /tmp/aos_brain.sock)
    ↓ Intent Commands
AOS Client (Python)
    ↓ mTLS
PM01 Bridge (gRPC Server)
    ↓ Action Validation
LearningBasedController (C++)
    ↓ Joint Commands
PM01 Hardware
```

---

## Security Features

- ✅ **Mutual TLS 1.3** - Both client and server authenticate
- ✅ **Short-lived Certificates** - 24h server, 30d client validity
- ✅ **Action Validation** - Rate limiting and safety bounds
- ✅ **Rate Limiting** - 100Hz max action rate
- ✅ **Certificate Pinning** - CA-based trust chain

---

## Quick Start

### 1. Setup Environment

```bash
cd pm01_aos_bridge
source venv/bin/activate
```

### 2. Start Bridge Server

```bash
cd src/bridge
python secure_bridge.py
```

Generates certificates automatically, starts gRPC server on port 50051.

### 3. Generate Client Certificates

```bash
cd src/security
python generate_client_certs.py aos_brain_client
```

### 4. Connect AOS Client

```bash
cd src/bridge
python aos_client.py
```

Requires AOS Brain socket at `/tmp/aos_brain.sock`.

---

## Protocol Buffer API

### Services

- `SendCommand(IntentCommand)` → CommandAck
- `StreamState(StateRequest)` → stream RobotState  
- `AgentLoop(stream IntentCommand)` → stream RLAction

### Message Types

- **IntentCommand** - High-level intent ("navigate to reception")
- **RLAction** - Low-level joint commands
- **RobotState** - Telemetry stream

See `proto/aos_pm01.proto` for full schema.

---

## Agent Personalities

| Agent | Role | File |
|-------|------|------|
| Miles | Sales Consultant | `src/agents/miles.py` |
| Patricia | Operations | `src/agents/patricia.py` |
| Jordan | Security | `src/agents/jordan.py` |
| Pulp | Sales Specialist | `src/agents/pulp.py` |

---

## Configuration

Edit `secure_bridge.py` BridgeConfig:

```python
config = BridgeConfig(
    listen_port=50051,
    cert_validity_hours=24,  # Short-lived per Jordan
    require_client_cert=True,
    max_action_rate=100,     # Hz
    action_timeout_ms=50     # Validation timeout
)
```

---

## Testing

```bash
# Unit tests
python -m pytest tests/

# Integration test (requires running bridge)
python tests/test_bridge_integration.py
```

---

## Security Checklist

- [ ] mTLS enabled with client cert verification
- [ ] Certificates regenerated every 24h (automated)
- [ ] Action validation with rate limiting
- [ ] Joint velocity limits enforced
- [ ] No debug ports accessible
- [ ] Logs sanitized (no PII)

---

## Deployment

See `../docs/PM01_Integration_Assessment.md` for full roadmap.

---

**Maintainer:** Performance Supply Depot LLC  
**License:** MIT (with security notice)
