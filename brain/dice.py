"""
Dice - Quantum Intuition Organ for AOS-OS
Mortimer's quantum dice for decision support and exploration
"""

import math
import random
import json
from pathlib import Path
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


class Dice:
    """
    The DICE organ - Quantum-powered decision support.
    
    Provides probabilistic exploration without fake certainty.
    """
    
    def __init__(self, memory_path: str = None):
        self.simulator = AerSimulator()
        self.memory_path = memory_path or "/root/.openclaw/workspace/aoscros_brain/memory/"
        self.history = []
        self._load_history()
        
    def _load_history(self):
        """Load past dice rolls from brain memory."""
        p = Path(self.memory_path)
        if p.exists():
            f = p / "dice_history.json"
            if f.exists():
                try:
                    self.history = json.loads(f.read_text())
                except:
                    self.history = []
                
    def _save_history(self):
        """Save dice history to brain memory."""
        Path(self.memory_path).mkdir(parents=True, exist_ok=True)
        f = Path(self.memory_path) / "dice_history.json"
        f.write_text(json.dumps(self.history[-100:]))  # Keep last 100
    
    def consult(self, question: str, options: list, gut: int = None) -> dict:
        """
        Guided dice roll - amplifies the "gut feeling" choice.
        gut: Index of the option that feels right (0-indexed)
        """
        if not options:
            return {"error": "No options provided"}
            
        n_qubits = max(1, math.ceil(math.log2(len(options))))
        
        qc = QuantumCircuit(n_qubits, n_qubits)
        for i in range(n_qubits):
            qc.h(i)
        
        if gut is not None and gut < len(options):
            # Grover-like amplification
            target = format(gut, f'0{n_qubits}b')
            iters = max(1, int(math.pi / 4 * math.sqrt(2 ** n_qubits)) - 1)
            
            for _ in range(iters):
                # Oracle
                for i, b in enumerate(target):
                    if b == '0': qc.x(i)
                qc.h(n_qubits - 1)
                if n_qubits > 1:
                    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
                else:
                    qc.z(0)
                qc.h(n_qubits - 1)
                for i, b in enumerate(target):
                    if b == '0': qc.x(i)
                # Diffusion
                for i in range(n_qubits): qc.h(i)
                for i in range(n_qubits): qc.x(i)
                qc.h(n_qubits - 1)
                if n_qubits > 1:
                    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
                else:
                    qc.z(0)
                qc.h(n_qubits - 1)
                for i in range(n_qubits): qc.x(i)
                for i in range(n_qubits): qc.h(i)
        
        qc.measure(range(n_qubits), range(n_qubits))
        result = self.simulator.run(qc, shots=10000).result()
        
        probs = {}
        for state, count in result.get_counts().items():
            idx = int(state[::-1], 2)
            if idx < len(options):
                probs[options[idx]] = round(count / 100, 1)
        
        sorted_probs = dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))
        
        record = {
            "type": "consult",
            "question": question,
            "options": options,
            "gut": options[gut] if gut is not None else None,
            "result": sorted_probs,
            "recommendation": max(sorted_probs, key=sorted_probs.get)
        }
        self.history.append(record)
        self._save_history()
        
        return record
    
    def roll(self, options: list) -> dict:
        """Pure quantum exploration - random selection with superposition."""
        if not options:
            return {"error": "No options provided"}
            
        n_qubits = min(math.ceil(math.log2(len(options))), 10)
        
        qc = QuantumCircuit(n_qubits, n_qubits)
        for i in range(n_qubits):
            qc.h(i)
            qc.rz(random.uniform(0, 2 * math.pi), i)
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        
        qc.measure(range(n_qubits), range(n_qubits))
        result = self.simulator.run(qc, shots=5000).result()
        
        probs = {}
        for state, count in result.get_counts().items():
            idx = int(state[::-1], 2)
            if idx < len(options):
                probs[options[idx]] = round(count / 50, 1)
        
        record = {"type": "roll", "result": probs}
        self.history.append(record)
        self._save_history()
        
        return record
    
    def oracle(self, question: str, options: list) -> dict:
        """Deep exploration - for important decisions."""
        if not options:
            return {"error": "No options provided"}
            
        n_qubits = min(math.ceil(math.log2(len(options))), 8)
        
        qc = QuantumCircuit(n_qubits, n_qubits)
        for i in range(n_qubits):
            qc.h(i)
            qc.rz(random.uniform(0, 2 * math.pi), i)
        for _ in range(3):
            for i in range(n_qubits - 1):
                qc.cx(i, i + 1)
        
        qc.measure(range(n_qubits), range(n_qubits))
        result = self.simulator.run(qc, shots=10000).result()
        
        probs = {}
        for state, count in result.get_counts().items():
            idx = int(state[::-1], 2)
            if idx < len(options):
                probs[options[idx]] = round(count / 100, 1)
        
        sorted_probs = dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))
        
        record = {
            "type": "oracle",
            "question": question,
            "result": sorted_probs,
            "recommendation": max(sorted_probs, key=sorted_probs.get)
        }
        self.history.append(record)
        self._save_history()
        
        return record
    
    def get_last(self) -> dict:
        """Get the most recent dice roll."""
        return self.history[-1] if self.history else {}
    
    def get_history(self, limit: int = 10) -> list:
        """Get recent dice history."""
        return self.history[-limit:] if self.history else []


def create_dice():
    """Factory function to create the Dice organ."""
    return Dice()