# 🧠 AOS Ternary Brain (Python)

A Python implementation of the AOS brain architecture with ternary neurons, 3-tier memory, and OODA cognition cycles.

## Architecture

```
aos_brain_py/
├── brain/
│   ├── brain_server.py         # Flask API + Unix socket server
│   ├── ternary_ooda.py         # 3-tier memory OODA brain
│   ├── cortex.py               # Language/reasoning module
│   └── brain_original.py       # Original Python reference
├── core/
│   ├── cortical_sheet.py       # 3D ternary wave propagation
│   └── tracray_lexicon.py      # Spatial concept mapping
├── substrate/
│   └── graph_store.py          # Semantic graph with growth rules
├── visualizer/
│   └── brain_visualizer.py     # Bob Ross color console viz
├── agents/
│   └── agent_adapter.py        # Miles, Mortimer, Mini adapters
├── config/
│   └── colors.py               # Bob Ross palette
├── scripts/
│   └── start_brain.sh          # Startup script
└── systemd/
    └── aos-brain.service       # Systemd service file
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the brain server
./scripts/start_brain.sh

# Or run directly
python -m brain.brain_server --port 5000
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/status` | GET | Full brain status |
| `/think` | POST | Main cognition endpoint |
| `/memory` | GET | Memory layer stats |
| `/sheet` | GET | Cortical sheet state |

### Think Endpoint

```bash
curl -X POST http://localhost:5000/think \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello brain!", "agent": "miles"}'
```

Response:
```json
{
  "tick": 42,
  "action": "respond",
  "reason": "user_greeting",
  "mode": "Analytical",
  "language": "Hi, this is Miles...",
  "ternary": [0, 1, 1, 0, 0],
  "confidence": 0.8,
  "cortical": {
    "pos_count": 24,
    "neg_count": 8,
    "center": [5.2, 4.1, 2.8]
  },
  "memory": {
    "short_term": 5,
    "mid_term": 23,
    "substrate": {"nodes": 156, "edges": 89}
  }
}
```

## Agent Adapters

```python
from agents.agent_adapter import MilesAdapter, MortimerAdapter

# Create agent
miles = MilesAdapter("http://localhost:5000")

# Process input
response = miles.process("Tell me about voice agents")
print(response)
```

## Features

### Ternary Neurons
- States: `-1` (inhibit), `0` (rest), `+1` (excite)
- Wave propagation through 3D cortical sheet
- Hebbian learning (plasticity)

### 3-Tier Memory
- **Short-term**: Working memory (last 10 inputs)
- **Mid-term**: Episodic buffer (100 traces)
- **Long-term**: Semantic graph (unlimited growth)

### OODA Cycle
- **Observe**: Encode input to cortical pattern
- **Orient**: Query memory, build context
- **Decide**: Apply ternary logic
- **Act**: Generate output
- **Grow**: Consolidate to substrate

### QMD Modes
- Analytical (blue), Creative (green), Cautious (ochre)
- Exploratory (yellow), Reflective (deep blue)
- Directive (crimson), Emotional (red), Minimal (grey)

## Bob Ross Color Palette

All visualizations use the authentic Bob Ross palette:
- Phthalo Green, Prussian Blue, Cadmium Yellow
- Alizarin Crimson, Cadmium Red, Burnt Sienna
- Yellow Ochre, Titanium White, Midnight Black

## Systemd Service

```bash
# Install service (replace %I with your username)
sudo cp systemd/aos-brain.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable aos-brain@root
sudo systemctl start aos-brain@root

# Check status
sudo systemctl status aos-brain@root
```

## Comparison with Original

| Feature | Original (C++ + Ollama) | Ternary Brain |
|---------|------------------------|---------------|
| Model | Mortimer (2GB Ollama) | TinyLlama/Qwen |
| Neurons | Binary (0/1) | Ternary (-1/0/+1) |
| Memory | Single layer | 3-tier (short/mid/long) |
| Cognition | Direct | OODA cycle |
| Modes | None | QMD adaptive |
| Substrate | None | Semantic graph |
| Visualization | JSON | Console + colors |

## License

MIT - Same as original AOS brain
