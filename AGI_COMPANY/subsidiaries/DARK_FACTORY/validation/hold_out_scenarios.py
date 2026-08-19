#!/usr/bin/env python3
"""
HOLD-OUT SCENARIOS — Blind Validation for the Dark Factory
Based on the RiP GoR Council directive (2026-08-18) + Hold Out Kidneys v1.0.

CORE PRINCIPLE:
    "What does success look like?" is written BEFORE the build,
    in a file the BUILDER never sees. A SEPARATE validator session
    (blind to the implementation plan) runs these scenarios against
    the finished output. No bias, no self-grading, no gaming the tests.

Schema (hold_out_scenarios.json):
    {
      "product": "cobra_v1",
      "authored_at": "2026-08-18T00:00:00Z",
      "scenarios": [
        {
          "id": "SC-001",
          "name": "Human-readable success criterion (no implementation detail)",
          "check": "file_exists | file_nonempty | dir_contains | artifact_present | log_contains",
          "target": "path/glob/string to check",
          "weight": 1.0,
          "min_matches": 1
        }
      ]
    }

The builder agent never reads this file. The validator reads ONLY this file
+ the built output. The two never share a session.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class HoldOutValidator:
    """Runs hold-out scenarios against built output, blind to the plan."""

    def __init__(self, scenarios_dir: str):
        self.scenarios_dir = Path(scenarios_dir)
        # The validator intentionally does NOT know the build plan / logs.

    def load_scenarios(self, product: str) -> Dict[str, Any]:
        """Load the hold-out scenarios authored for a product BEFORE the build."""
        path = self.scenarios_dir / f"{product}.json"
        if not path.exists():
            # Fall back to a single shared catalog
            shared = self.scenarios_dir / "hold_out_scenarios.json"
            if not shared.exists():
                return {"product": product, "scenarios": []}
            data = json.loads(shared.read_text())
            # filter to this product if catalog is keyed by product
            return self._select_product(data, product)

        return json.loads(path.read_text())

    @staticmethod
    def _select_product(catalog: Dict, product: str) -> Dict:
        """If the catalog is a map of product -> scenarios, pick the right one."""
        if "scenarios" in catalog:
            return catalog
        # catalog might be {"products": {...}}
        products = catalog.get("products", catalog)
        return products.get(product, {"product": product, "scenarios": []})

    def validate(self, product: str, output_path: str, size_bytes: int = 0) -> Dict[str, Any]:
        """Run every hold-out scenario for `product` against `output_path`."""
        spec = self.load_scenarios(product)
        scenarios = spec.get("scenarios", [])

        if not scenarios:
            # No hold-out scenarios authored = cannot certify. Treat as fail-open
            # with a warning (config gap), NOT silent pass.
            return {
                "product": product,
                "passed": False,
                "reason": "NO_HOLD_OUT_SCENARIOS_DEFINED",
                "results": [],
                "score": 0.0,
            }

        results = []
        passed_count = 0
        total_weight = 0.0
        earned_weight = 0.0

        for sc in scenarios:
            ok = self._run_check(sc, output_path, size_bytes)
            w = float(sc.get("weight", 1.0))
            total_weight += w
            if ok:
                passed_count += 1
                earned_weight += w
            results.append({
                "id": sc.get("id", "?"),
                "name": sc.get("name", ""),
                "passed": ok,
                "weight": w,
            })

        score = (earned_weight / total_weight) if total_weight > 0 else 0.0
        return {
            "product": product,
            "passed": score >= 0.8,  # 80% threshold = certifiable
            "score": round(score, 3),
            "results": results,
            "passed_count": passed_count,
            "total_count": len(scenarios),
            "reason": None if score >= 0.8 else "HOLDOUT_THRESHOLD_NOT_MET",
        }

    def _run_check(self, scenario: Dict, output_path: str, size_bytes: int) -> bool:
        check = scenario.get("check", "file_exists")
        target = scenario.get("target", "")
        min_matches = int(scenario.get("min_matches", 1))

        if check == "file_exists":
            return Path(target).exists()

        if check == "file_nonempty":
            p = Path(target)
            return p.exists() and p.is_file() and p.stat().st_size > 0

        if check == "dir_contains":
            p = Path(target)
            if not p.exists() or not p.is_dir():
                return False
            files = [f for f in p.rglob("*") if f.is_file()]
            return len(files) >= min_matches

        if check == "artifact_present":
            # target is a glob pattern, e.g. "*.apk" within output_path
            base = Path(output_path) if output_path else Path(".")
            # If output is a single file (e.g. a built .apk), search its parent dir
            if base.is_file():
                base = base.parent
            matches = list(base.rglob(target)) if target else []
            return len(matches) >= min_matches

        if check == "log_contains":
            # search the built output's logs for a marker string
            marker = scenario.get("marker", target)
            base = Path(output_path) if output_path else Path(".")
            for f in base.rglob("*"):
                if f.is_file() and f.suffix in (".log", ".txt", ".md"):
                    try:
                        if marker in f.read_text(errors="ignore"):
                            return True
                    except Exception:
                        continue
            return False

        # Unknown check type → fail loudly (don't silently pass)
        return False


def validate_hold_out(product: str, output_path: str, size_bytes: int = 0,
                      scenarios_dir: str = None) -> Dict[str, Any]:
    """
    Standalone entry point. Runs blind hold-out validation.
    The builder NEVER calls this. Only the separate validator does.
    """
    if scenarios_dir is None:
        scenarios_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "validation",
        )
    validator = HoldOutValidator(scenarios_dir)
    return validator.validate(product, output_path, size_bytes)


if __name__ == "__main__":
    import sys
    product = sys.argv[1] if len(sys.argv) > 1 else "cobra_v1"
    output = sys.argv[2] if len(sys.argv) > 2 else ""
    result = validate_hold_out(product, output)
    print(json.dumps(result, indent=2))
