#!/usr/bin/env python3
"""
Ternary Lungs v1.0 - Organ G
AOS Complete Brain v4.5 Component

Role:
- Inhale ambient computational atmosphere (events, deltas, signals)
- Perform ternary gas exchange (+1 / 0 / -1)
- Regulate internal "pressure" and breath rhythm
- Exhale spent cognitive gas for kidneys/intestine

Part of the Signal/Noise Pipeline:
Ambient Input → LUNGS (INHALE/GAS_EXHANGE/EXHALE) → LIVER → Brain → KIDNEYS → Output
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Optional
import time
import math
import json


@dataclass
class BreathMetrics:
    """Respiratory cycle metrics for telemetry"""
    timestamp: float
    inhale_count: int
    exhale_count: int
    pressure: float
    breath_rate: float
    oxygen_saturation: float  # Ratio of useful signal to total intake


@dataclass
class TernaryOxygenPacket:
    """
    Perceived 'gas' for the rest of the body.
    Analogous to oxygen, CO2, and nitrogen in biological systems.
    """
    positives: List[Any] = field(default_factory=list)  # +1 - opportunities, fuel
    neutrals: List[Any] = field(default_factory=list)   # 0 - background, ignorable
    negatives: List[Any] = field(default_factory=list)  # -1 - threats, caution gas

    def total(self) -> int:
        return len(self.positives) + len(self.neutrals) + len(self.negatives)

    def saturation(self) -> float:
        """Calculate oxygen saturation (useful signal ratio)"""
        total = self.total()
        if total == 0:
            return 0.0
        return len(self.positives) / total

    def to_dict(self) -> Dict:
        return {
            "positives": len(self.positives),
            "neutrals": len(self.neutrals),
            "negatives": len(self.negatives),
            "total": self.total(),
            "saturation": self.saturation()
        }


@dataclass
class ExhaledWaste:
    """CO2-equivalent waste gas for kidneys/intestine processing"""
    waste_volume: int
    neutrals: List[Any] = field(default_factory=list)
    negatives: List[Any] = field(default_factory=list)
    pressure: float = 1.0
    breath_rate: float = 1.0
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict:
        return {
            "waste_volume": self.waste_volume,
            "neutrals_count": len(self.neutrals),
            "negatives_count": len(self.negatives),
            "pressure": self.pressure,
            "breath_rate": self.breath_rate,
            "timestamp": self.timestamp
        }


class TernaryLungs:
    """
    Organ G: Ternary Lungs

    The respiratory system for the AOS organism. Handles:
    - Ambient intake from environment (events, telemetry, signals)
    - Ternary classification (opportunity/threat/neutral)
    - Pressure regulation (prevents cognitive suffocation/hyperventilation)
    - Rhythmic breathing synchronized with heart and brainstem
    - Waste gas routing to kidneys

    Integrates with:
    - Heart: valence modulates breath rate and depth
    - Stomach: receives oxygenated data for digestion
    - Intestine: filters oxygenated signals
    - Liver: transforms oxygen into metabolic substrates
    - Kidneys: handles CO2-equivalent waste
    - Brain: 7-region OODA consumes oxygenated inputs
    """

    def __init__(
        self,
        base_breath_rate: float = 1.0,  # breaths per second (logical)
        base_pressure: float = 1.0,     # normalized internal pressure
        classification_threshold: float = 0.2,  # ternary classification threshold
    ):
        self.base_breath_rate = base_breath_rate
        self.base_pressure = base_pressure
        self.classification_threshold = classification_threshold

        # Dynamic state
        self.current_breath_rate = base_breath_rate
        self.current_pressure = base_pressure
        self.oxygen_saturation = 1.0

        # Cycle tracking
        self.last_breath_ts: float = time.time()
        self.inhale_count: int = 0
        self.exhale_count: int = 0

        # Phase tracking (for breath-phase hooks)
        self.phase = "REST"  # INHALE, EXHALE, REST
        self.phase_progress = 0.0  # 0.0 to 1.0

        # History for trend analysis
        self.metrics_history: List[BreathMetrics] = []
        self.max_history = 100

    # =================================================================
    # PUBLIC API
    # =================================================================

    def step(
        self,
        ambient_stream: List[Any],
        heart_valence: float = 0.0,
        metabolic_demand: float = 1.0,
    ) -> Tuple[TernaryOxygenPacket, ExhaledWaste]:
        """
        One respiratory step in the agent loop.

        Args:
            ambient_stream: Raw events / world deltas / signals
            heart_valence: [-1, 1] emotional/drive tone from heart
            metabolic_demand: [0, inf) demand from brain/body

        Returns:
            oxygen_packet: Ternary-classified "gas" for other organs
            exhaled: Waste gas for kidneys/intestine
        """
        # Update respiratory rhythm based on physiological state
        self._update_rhythm(heart_valence, metabolic_demand)

        # Inhale and classify ambient atmosphere
        oxygen_packet = self._inhale(ambient_stream)

        # Exhale waste gas
        exhaled = self._exhale(oxygen_packet)

        # Update phase tracking
        self._update_phase()

        return oxygen_packet, exhaled

    def inhale_external(self, raw_input: Any, context: Optional[Dict] = None) -> int:
        """
        Direct external inhalation - classify a single item.
        Returns ternary classification (-1, 0, +1).
        """
        return self._classify_item(raw_input, context)

    def get_metrics(self) -> BreathMetrics:
        """Get current respiratory metrics"""
        return BreathMetrics(
            timestamp=time.time(),
            inhale_count=self.inhale_count,
            exhale_count=self.exhale_count,
            pressure=self.current_pressure,
            breath_rate=self.current_breath_rate,
            oxygen_saturation=self.oxygen_saturation
        )

    def get_status(self) -> Dict:
        """Get full status for diagnostic API"""
        return {
            "organ": "TernaryLungs",
            "version": "1.0",
            "phase": self.phase,
            "phase_progress": round(self.phase_progress, 3),
            "breath_rate": round(self.current_breath_rate, 3),
            "pressure": round(self.current_pressure, 3),
            "oxygen_saturation": round(self.oxygen_saturation, 3),
            "cycles": {
                "inhale": self.inhale_count,
                "exhale": self.exhale_count
            },
            "base": {
                "breath_rate": self.base_breath_rate,
                "pressure": self.base_pressure
            }
        }

    def hold_breath(self) -> None:
        """
        Hold breath primitive for suspense, focus, or danger states.
        Suspends normal respiratory rhythm.
        """
        self.phase = "HOLD"
        self.current_breath_rate = 0.0

    def release_breath(self) -> None:
        """Release breath hold and resume normal rhythm"""
        self.phase = "REST"
        self.current_breath_rate = self.base_breath_rate

    def set_breath_rate(self, rate: float) -> None:
        """Manually set breath rate (for override/debug)"""
        self.base_breath_rate = max(0.1, rate)
        self.current_breath_rate = self.base_breath_rate

    # =================================================================
    # INTERNAL MECHANICS
    # =================================================================

    def _inhale(self, ambient_stream: List[Any]) -> TernaryOxygenPacket:
        """Inhale ambient atmosphere and perform gas exchange"""
        self.inhale_count += 1
        self.phase = "INHALE"
        return self._gas_exchange(ambient_stream)

    def _exhale(self, oxygen_packet: TernaryOxygenPacket) -> ExhaledWaste:
        """Exhale waste gas (CO2 equivalent)"""
        self.exhale_count += 1
        self.phase = "EXHALE"

        # Calculate oxygen saturation
        total = oxygen_packet.total()
        if total > 0:
            self.oxygen_saturation = len(oxygen_packet.positives) / total
        else:
            self.oxygen_saturation = 0.0

        # Build waste packet
        waste = ExhaledWaste(
            waste_volume=len(oxygen_packet.neutrals) + len(oxygen_packet.negatives),
            neutrals=oxygen_packet.neutrals,
            negatives=oxygen_packet.negatives,
            pressure=self.current_pressure,
            breath_rate=self.current_breath_rate
        )

        # Store metrics
        self._record_metrics()

        return waste

    def _gas_exchange(self, ambient_stream: List[Any]) -> TernaryOxygenPacket:
        """
        Convert ambient items into ternary oxygen.
        This is the core "gas exchange" function.
        """
        packet = TernaryOxygenPacket()

        for item in ambient_stream:
            label = self._classify_item(item)

            if label > 0:
                packet.positives.append(item)
            elif label < 0:
                packet.negatives.append(item)
            else:
                packet.neutrals.append(item)

        return packet

    def _classify_item(self, item: Any, context: Optional[Dict] = None) -> int:
        """
        Ternary classifier for ambient items.

        Returns:
            +1: Opportunity, fuel, energizing
             0: Neutral, background, ignorable
            -1: Threat, caution, draining

        This is the primary classification logic - can be overridden
        or extended for domain-specific classification.
        """
        # Handle different input types
        if isinstance(item, dict):
            return self._classify_dict(item, context)
        elif isinstance(item, str):
            return self._classify_string(item, context)
        elif hasattr(item, 'valence'):
            # Object with valence attribute
            val = float(getattr(item, 'valence', 0.0))
            return self._valence_to_ternary(val)
        elif hasattr(item, 'get'):
            # Dict-like object
            val = item.get('valence', item.get('urgency', item.get('priority', 0.0)))
            return self._valence_to_ternary(float(val))
        else:
            # Default: neutral
            return 0

    def _classify_dict(self, item: Dict, context: Optional[Dict] = None) -> int:
        """Classify a dictionary item"""
        # Check for explicit markers
        if 'type' in item:
            if item['type'] in ['error', 'exception', 'failure', 'threat']:
                return -1
            elif item['type'] in ['opportunity', 'success', 'fuel', 'growth']:
                return +1

        # Check numeric valence
        for key in ['valence', 'urgency', 'priority', 'importance', 'score']:
            if key in item:
                return self._valence_to_ternary(float(item[key]))

        # Check sentiment
        if 'sentiment' in item:
            sent = str(item['sentiment']).lower()
            if sent in ['positive', 'good', 'opportunity']:
                return +1
            elif sent in ['negative', 'bad', 'threat']:
                return -1

        return 0

    def _classify_string(self, item: str, context: Optional[Dict] = None) -> int:
        """Classify a string item (basic keyword heuristics)"""
        item_lower = item.lower()

        positive_keywords = ['success', 'complete', 'opportunity', 'growth',
                           'win', 'achieve', 'learn', 'improve', 'positive']
        negative_keywords = ['error', 'fail', 'exception', 'threat', 'danger',
                           'critical', 'warning', 'negative', 'break']

        if any(kw in item_lower for kw in negative_keywords):
            return -1
        elif any(kw in item_lower for kw in positive_keywords):
            return +1

        return 0

    def _valence_to_ternary(self, val: float) -> int:
        """Convert continuous valence to ternary"""
        if val > self.classification_threshold:
            return +1
        elif val < -self.classification_threshold:
            return -1
        return 0

    def _update_rhythm(self, heart_valence: float, metabolic_demand: float) -> None:
        """
        Adjust breath rate and pressure based on:
        - heart_valence: negative → shallow, guarded; positive → deeper, open
        - metabolic_demand: higher → faster breathing
        """
        # Clamp inputs
        heart_valence = max(-1.0, min(1.0, heart_valence))
        metabolic_demand = max(0.0, metabolic_demand)

        # Breath rate: base + demand + small valence modulation
        target_rate = self.base_breath_rate * (1.0 + 0.5 * metabolic_demand)
        target_rate *= (1.0 + 0.2 * heart_valence)

        # Smooth transition
        self.current_breath_rate = 0.7 * self.current_breath_rate + 0.3 * target_rate

        # Pressure: higher with demand, slightly reduced by negative valence
        target_pressure = self.base_pressure * (1.0 + 0.3 * metabolic_demand)
        target_pressure *= (1.0 - 0.2 * max(0.0, -heart_valence))

        self.current_pressure = 0.7 * self.current_pressure + 0.3 * target_pressure

        self.last_breath_ts = time.time()

    def _update_phase(self) -> None:
        """Update breath phase tracking"""
        if self.phase == "HOLD":
            self.phase_progress = 1.0
            return

        # Simple phase cycling
        elapsed = time.time() - self.last_breath_ts
        cycle_duration = 1.0 / max(self.current_breath_rate, 0.1)

        self.phase_progress = (elapsed % cycle_duration) / cycle_duration

        # Phase transitions
        if self.phase_progress < 0.4:
            self.phase = "INHALE"
        elif self.phase_progress < 0.7:
            self.phase = "REST"
        else:
            self.phase = "EXHALE"

    def _record_metrics(self) -> None:
        """Record metrics for trend analysis"""
        metrics = self.get_metrics()
        self.metrics_history.append(metrics)

        if len(self.metrics_history) > self.max_history:
            self.metrics_history.pop(0)


# =================================================================
# SOCKET API INTEGRATION
# =================================================================

def handle_lungs_command(params: Dict) -> Dict:
    """
    Handle socket commands for lungs.
    To be wired into brain socket server.
    """
    global _lungs_instance

    if '_lungs_instance' not in globals():
        _lungs_instance = TernaryLungs()

    cmd = params.get('cmd', 'status')

    if cmd == 'status':
        return _lungs_instance.get_status()

    elif cmd == 'inhale':
        ambient = params.get('ambient', [])
        valence = params.get('valence', 0.0)
        demand = params.get('demand', 1.0)
        o2, waste = _lungs_instance.step(ambient, valence, demand)
        return {
            "oxygen": o2.to_dict(),
            "waste": waste.to_dict()
        }

    elif cmd == 'hold':
        _lungs_instance.hold_breath()
        return {"status": "breath_held"}

    elif cmd == 'release':
        _lungs_instance.release_breath()
        return {"status": "breath_released"}

    elif cmd == 'metrics':
        m = _lungs_instance.get_metrics()
        return {
            "inhale_count": m.inhale_count,
            "exhale_count": m.exhale_count,
            "pressure": m.pressure,
            "breath_rate": m.breath_rate,
            "oxygen_saturation": m.oxygen_saturation
        }

    else:
        return {"error": f"Unknown lungs command: {cmd}"}


# =================================================================
# DIAGNOSTIC
# =================================================================

if __name__ == "__main__":
    print("🫁 Ternary Lungs v1.0 Diagnostic")
    print("=" * 50)

    # Create lungs
    lungs = TernaryLungs(base_breath_rate=1.0, base_pressure=1.0)

    # Test ambient stream
    test_ambient = [
        {"type": "opportunity", "valence": 0.8, "content": "New learning signal"},
        {"type": "background", "valence": 0.0, "content": "Telemetry tick"},
        {"type": "error", "valence": -0.9, "content": "Connection timeout"},
        {"valence": 0.5, "content": "Positive feedback"},
        {"valence": -0.3, "content": "Minor delay"},
        "This is a neutral string",
        "Critical failure detected!"
    ]

    print(f"\nTest ambient stream: {len(test_ambient)} items")

    # Simulate breathing cycles
    for cycle in range(3):
        print(f"\n--- Cycle {cycle + 1} ---")

        # Vary heart valence
        heart_valence = [0.5, -0.3, 0.8][cycle]
        metabolic_demand = [1.0, 2.0, 0.5][cycle]

        print(f"Heart valence: {heart_valence}, Metabolic demand: {metabolic_demand}")

        oxygen, waste = lungs.step(test_ambient, heart_valence, metabolic_demand)

        print(f"Oxygen packet: +{len(oxygen.positives)} / {len(oxygen.neutrals)} / -{len(oxygen.negatives)}")
        print(f"Saturation: {oxygen.saturation():.2%}")
        print(f"Waste volume: {waste.waste_volume}")
        print(f"Breath rate: {lungs.current_breath_rate:.2f}, Pressure: {lungs.current_pressure:.2f}")

    print("\n" + "=" * 50)
    print("Final status:")
    print(json.dumps(lungs.get_status(), indent=2))
