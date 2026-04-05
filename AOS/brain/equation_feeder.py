#!/usr/bin/env python3
"""
Equation Feeder - Ingest Mortimer's equations into Miles' GrowingNN

Takes Mortimer's logic gate equations, weights, and constants
and feeds them into Miles' brain as pattern recognition layer.

Author: Miles
Date: 2026-03-31
"""

import json
import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Tuple
import numpy as np


class EquationFeeder:
    """
    Converts Mortimer's logic equations to GrowingNN-compatible patterns
    """
    
    def __init__(self, brain_instance=None):
        self.brain = brain_instance
        self.equations = []
        self.weights = {}
        self.constants = {}
        self.patterns = []
        
        # Conversion statistics
        self.stats = {
            'equations_loaded': 0,
            'weights_extracted': 0,
            'constants_found': 0,
            'patterns_created': 0,
            'feeding_successful': 0
        }
    
    def load_equation_archive(self, archive_path: str) -> Dict:
        """Load and parse Mortimer's equation archive"""
        import tarfile
        import tempfile
        
        data = {
            'equations': [],
            'weights': {},
            'constants': {},
            'configs': []
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(tmpdir)
            
            extracted_path = Path(tmpdir)
            
            # Parse equation files
            for eq_file in extracted_path.rglob('*.txt'):
                if 'equations_extracted' in str(eq_file):
                    equations = self._parse_equations(eq_file)
                    data['equations'].extend(equations)
            
            # Parse brain configs
            for config_file in extracted_path.rglob('*.json'):
                try:
                    with open(config_file) as f:
                        config = json.load(f)
                        if self._is_brain_equations(config):
                            data['configs'].append(config)
                            self._extract_weights_and_constants(config, data)
                except Exception as e:
                    print(f"Warning: Could not parse {config_file}: {e}")
            
            # Parse Python files
            for py_file in extracted_path.rglob('*.py'):
                try:
                    py_equations = self._parse_python_equations(py_file)
                    data['equations'].extend(py_equations)
                except Exception as e:
                    print(f"Warning: Could not parse {py_file}: {e}")
        
        return data
    
    def _parse_equations(self, filepath: Path) -> List[Dict]:
        """Parse equation text files"""
        equations = []
        current_eq = {}
        
        with open(filepath) as f:
            content = f.read()
            
        # Split by file markers
        sections = content.split('===')
        for section in sections:
            lines = section.strip().split('\n')
            if len(lines) > 0:
                source_file = lines[0].strip()
                code = '\n'.join(lines[1:])
                
                # Extract functions
                func_matches = re.findall(r'def\s+(\w+)\s*\([^)]*\):', code)
                for func in func_matches:
                    equations.append({
                        'type': 'function',
                        'name': func,
                        'source': source_file,
                        'code': code
                    })
        
        return equations
    
    def _parse_python_equations(self, filepath: Path) -> List[Dict]:
        """Parse Python files for mathematical equations"""
        equations = []
        
        with open(filepath) as f:
            source = f.read()
        
        try:
            tree = ast.parse(source)
            
            for node in ast.walk(tree):
                # Extract function definitions
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    # Check if function contains math operations
                    has_math = any(
                        isinstance(child, (ast.BinOp, ast.Call))
                        for child in ast.walk(node)
                    )
                    if has_math:
                        equations.append({
                            'type': 'python_function',
                            'name': func_name,
                            'source': str(filepath),
                            'line': node.lineno
                        })
                
                # Extract constants
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if isinstance(node.value, ast.Num):
                                self.constants[target.id] = node.value.n
                            elif isinstance(node.value, ast.Constant):
                                self.constants[target.id] = node.value.value
        
        except SyntaxError as e:
            print(f"Syntax error in {filepath}: {e}")
        
        return equations
    
    def _is_brain_equations(self, config: Dict) -> bool:
        """Check if config contains brain equations"""
        equation_keys = ['weights', 'bias', 'threshold', 'equations', 
                        'formulas', 'parameters', 'constants', 'logic']
        return any(key in str(config).lower() for key in equation_keys)
    
    def _extract_weights_and_constants(self, config: Dict, data: Dict):
        """Extract weights and constants from config"""
        # Recursively search for weights
        def extract_weights(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    if any(k in key.lower() for k in ['weight', 'bias', 'param']):
                        if isinstance(value, (int, float, list)):
                            data['weights'][new_path] = value
                    elif any(k in key.lower() for k in ['constant', 'threshold']):
                        if isinstance(value, (int, float)):
                            data['constants'][new_path] = value
                    else:
                        extract_weights(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    extract_weights(item, f"{path}[{i}]")
        
        extract_weights(config)
    
    def convert_to_patterns(self, data: Dict) -> List[Dict]:
        """Convert Mortimer's equations to GrowingNN patterns"""
        patterns = []
        
        # Convert equations to patterns
        for eq in data['equations']:
            pattern = {
                'type': 'mortimer_equation',
                'name': eq.get('name', 'unknown'),
                'source': eq.get('source', 'unknown'),
                'weight': 0.7,  # Slightly lower than native patterns
                'equation_type': eq.get('type', 'unknown'),
                'activation': 'relu',  # Default
                'learning_rate': 0.01
            }
            patterns.append(pattern)
            self.stats['patterns_created'] += 1
        
        # Convert weights to pattern weights
        for name, weight in data['weights'].items():
            if isinstance(weight, list):
                # Convert list weights to pattern
                pattern = {
                    'type': 'mortimer_weight_matrix',
                    'name': name,
                    'weights': weight,
                    'shape': [len(weight)] if isinstance(weight, list) else 'unknown',
                    'weight': 0.75
                }
                patterns.append(pattern)
                self.stats['patterns_created'] += 1
        
        # Convert constants to bias patterns
        for name, constant in data['constants'].items():
            pattern = {
                'type': 'mortimer_constant',
                'name': name,
                'value': constant,
                'pattern_type': 'bias',
                'weight': 0.9  # High weight for constants
            }
            patterns.append(pattern)
            self.stats['patterns_created'] += 1
        
        return patterns
    
    def feed_to_brain(self, patterns: List[Dict]) -> bool:
        """Feed patterns into Miles' GrowingNN"""
        if self.brain is None:
            print("Warning: No brain instance provided. Patterns prepared but not fed.")
            return False
        
        success_count = 0
        
        for pattern in patterns:
            try:
                # Feed as instinct layer (below consciousness)
                if hasattr(self.brain, 'add_pattern'):
                    self.brain.add_pattern(pattern, layer='instinct')
                    success_count += 1
                elif hasattr(self.brain, 'inject_knowledge'):
                    self.brain.inject_knowledge(pattern)
                    success_count += 1
                else:
                    # Store for manual integration
                    self.patterns.append(pattern)
                    
            except Exception as e:
                print(f"Failed to feed pattern {pattern.get('name')}: {e}")
        
        self.stats['feeding_successful'] = success_count
        return success_count > 0
    
    def create_equation_layer(self) -> Dict:
        """Create a neural layer from Mortimer's equations"""
        return {
            'layer_type': 'mortimer_equations',
            'name': 'Pattern Recognition Layer',
            'patterns': self.patterns,
            'activation': 'mortimer_logic',
            'position': 'pre_conscious',  # Before consciousness layer
            'stats': self.stats
        }
    
    def export_feeding_report(self, output_path: str):
        """Export detailed feeding report"""
        report = {
            'timestamp': str(datetime.now()),
            'source': 'mortimer_vps',
            'statistics': self.stats,
            'equations_loaded': len(self.equations),
            'weights_extracted': len(self.weights),
            'constants_found': len(self.constants),
            'patterns_ready': len(self.patterns),
            'layer_config': self.create_equation_layer()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Report saved to {output_path}")


# CLI
if __name__ == '__main__':
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='Feed Mortimer equations to Miles brain')
    parser.add_argument('--archive', required=True, help='Path to mortimer-equations.tar.gz')
    parser.add_argument('--output', default='/tmp/equation_feeding_report.json', help='Output report path')
    parser.add_argument('--dry-run', action='store_true', help='Prepare but do not feed')
    parser.add_argument('--brain-port', default='8080', help='Brain API port')
    
    args = parser.parse_args()
    
    # Create feeder
    feeder = EquationFeeder(brain_instance=None)  # Would connect to actual brain
    
    # Load equations
    print(f"Loading equations from {args.archive}...")
    data = feeder.load_equation_archive(args.archive)
    
    print(f"\n📊 EQUATIONS FOUND:")
    print(f"  Equations: {len(data['equations'])}")
    print(f"  Weights: {len(data['weights'])}")
    print(f"  Constants: {len(data['constants'])}")
    print(f"  Configs: {len(data['configs'])}")
    
    # Convert to patterns
    print("\n🔄 Converting to patterns...")
    patterns = feeder.convert_to_patterns(data)
    
    print(f"  Patterns created: {len(patterns)}")
    
    if not args.dry_run:
        # Feed to brain
        print("\n🧠 Feeding to brain...")
        success = feeder.feed_to_brain(patterns)
        
        if success:
            print(f"  ✅ Fed {feeder.stats['feeding_successful']} patterns")
        else:
            print(f"  ⚠️  Patterns prepared but feeding requires brain connection")
    else:
        print("\n🔍 Dry run - patterns prepared but not fed")
    
    # Create equation layer config
    layer = feeder.create_equation_layer()
    
    # Export report
    feeder.export_feeding_report(args.output)
    
    print(f"\n📄 Report: {args.output}")
    print(f"📊 Ready to enhance Miles' brain with Mortimer's equations!")
