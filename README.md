# AOS – Autonomous Operating System

AOS is a neural OODA-based Autonomous Operating System with:

- GrowingNN policy and memory cores
- Immutable safety laws (Law Zero + Three Laws)
- Override modes (strict, adaptive, sandbox)
- Local-first model support (GGUF, Ollama, cloud fallback)
- Full test suite and brain visualizer

## Install on VPS

```bash
cd ~/AOS
chmod +x install_aos_vps.sh
./install_aos_vps.sh
python3 ~/.aos/brain/brain.py
```

## Install on Android / Termux (AOS-Lite)
```bash
cd ~/AOS
chmod +x install_aos_android.sh
./install_aos_android.sh
python3 ~/.aos/brain/brain.py
```

## Visualizer
```bash
python3 ~/.aos/visualizer/brain_visualizer.py
```

## Tests
```bash
pytest ~/.aos/test -q
```