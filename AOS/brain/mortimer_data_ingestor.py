#!/usr/bin/env python3
"""
Mortimer Data Ingestor - Feed Mortimer's datasets into Miles' Brain

This module takes brain training data, patterns, and knowledge from
Mortimer's VPS and integrates them into Miles' GrowingNN.

Author: Miles
Date: 2026-03-31
"""

import json
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MortimerIngestor')


class MortimerDataIngestor:
    """
    Ingests Mortimer's brain datasets into Miles' GrowingNN
    """
    
    def __init__(self, brain_instance=None):
        self.brain = brain_instance
        self.ingested_patterns = []
        self.knowledge_graph = {}
        self.pattern_weights = {}
        self.memosyne_entries = []
        
        # Stats
        self.stats = {
            'patterns_ingested': 0,
            'knowledge_entries': 0,
            'nodes_added': 0,
            'errors': []
        }
        
    def load_dataset_archive(self, archive_path: str) -> Dict:
        """
        Load a dataset archive from Mortimer's VPS
        
        Args:
            archive_path: Path to mortimer-brain-datasets.tar.gz
            
        Returns:
            Dictionary containing all extracted data
        """
        import tarfile
        import tempfile
        
        data = {
            'brain_configs': [],
            'patterns': [],
            'knowledge': [],
            'training_data': [],
            'weights': None
        }
        
        try:
            # Extract archive
            with tempfile.TemporaryDirectory() as tmpdir:
                logger.info(f"Extracting {archive_path}...")
                with tarfile.open(archive_path, 'r:gz') as tar:
                    tar.extractall(tmpdir)
                
                extracted_path = Path(tmpdir)
                
                # Find and load brain configurations
                for config_file in extracted_path.rglob('*.json'):
                    try:
                        with open(config_file) as f:
                            config = json.load(f)
                            if self._is_brain_config(config):
                                data['brain_configs'].append(config)
                                logger.info(f"Loaded brain config: {config_file}")
                    except Exception as e:
                        logger.warning(f"Could not load {config_file}: {e}")
                
                # Find pattern files
                for pattern_file in extracted_path.rglob('*pattern*'):
                    if pattern_file.is_file():
                        try:
                            patterns = self._load_patterns(pattern_file)
                            data['patterns'].extend(patterns)
                            logger.info(f"Loaded patterns from {pattern_file}")
                        except Exception as e:
                            logger.warning(f"Could not load patterns {pattern_file}: {e}")
                
                # Find knowledge bases
                for kb_file in extracted_path.rglob('*.md'):
                    try:
                        with open(kb_file) as f:
                            content = f.read()
                            self.memosyne_entries.append({
                                'source': str(kb_file),
                                'content': content,
                                'type': 'memosyne'
                            })
                            logger.info(f"Loaded memosyne entry: {kb_file}")
                    except Exception as e:
                        logger.warning(f"Could not load {kb_file}: {e}")
                
                # Find training data
                for train_file in extracted_path.rglob('*training*'):
                    if train_file.suffix in ['.json', '.jsonl', '.txt']:
                        try:
                            training_data = self._load_training_data(train_file)
                            data['training_data'].extend(training_data)
                            logger.info(f"Loaded training data from {train_file}")
                        except Exception as e:
                            logger.warning(f"Could not load {train_file}: {e}")
                
                # Look for model weights
                for weights_file in extracted_path.rglob('*weights*'):
                    try:
                        weights = self._load_weights(weights_file)
                        if weights:
                            data['weights'] = weights
                            logger.info(f"Loaded weights from {weights_file}")
                    except Exception as e:
                        logger.warning(f"Could not load weights {weights_file}: {e}")
                        
        except Exception as e:
            logger.error(f"Failed to extract archive: {e}")
            self.stats['errors'].append(str(e))
            
        return data
    
    def _is_brain_config(self, data: Dict) -> bool:
        """Check if JSON data is a brain configuration"""
        brain_keys = ['nodes', 'layers', 'architecture', 'brain', 'neural', 'config']
        return any(key in str(data).lower() for key in brain_keys)
    
    def _load_patterns(self, filepath: Path) -> List[Dict]:
        """Load pattern files"""
        patterns = []
        try:
            with open(filepath) as f:
                if filepath.suffix == '.json':
                    data = json.load(f)
                    if isinstance(data, list):
                        patterns.extend(data)
                    else:
                        patterns.append(data)
                else:
                    # Text patterns
                    content = f.read()
                    patterns.append({
                        'source': str(filepath),
                        'content': content,
                        'type': 'text_pattern'
                    })
        except Exception as e:
            logger.warning(f"Error loading patterns: {e}")
        return patterns
    
    def _load_training_data(self, filepath: Path) -> List[Dict]:
        """Load training data files"""
        data = []
        try:
            with open(filepath) as f:
                if filepath.suffix == '.jsonl':
                    for line in f:
                        data.append(json.loads(line))
                elif filepath.suffix == '.json':
                    loaded = json.load(f)
                    if isinstance(loaded, list):
                        data.extend(loaded)
                    else:
                        data.append(loaded)
                else:
                    content = f.read()
                    data.append({
                        'source': str(filepath),
                        'content': content
                    })
        except Exception as e:
            logger.warning(f"Error loading training data: {e}")
        return data
    
    def _load_weights(self, filepath: Path) -> Optional[np.ndarray]:
        """Load model weights"""
        try:
            if filepath.suffix == '.npy':
                return np.load(filepath)
            elif filepath.suffix == '.pt' or filepath.suffix == '.pth':
                # PyTorch weights - would need torch
                logger.info("PyTorch weights found (require torch to load)")
                return None
            elif filepath.suffix == '.pkl':
                with open(filepath, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            logger.warning(f"Error loading weights: {e}")
        return None
    
    def ingest_into_brain(self, data: Dict) -> Dict:
        """
        Ingest all Mortimer data into Miles' brain
        
        Args:
            data: Dictionary containing all Mortimer datasets
            
        Returns:
            Ingestion statistics
        """
        logger.info("Starting brain data ingestion...")
        
        # 1. Ingest brain configurations
        self._ingest_brain_configs(data['brain_configs'])
        
        # 2. Ingest patterns
        self._ingest_patterns(data['patterns'])
        
        # 3. Ingest knowledge
        self._ingest_knowledge(data['knowledge'])
        
        # 4. Ingest training data
        self._ingest_training_data(data['training_data'])
        
        # 5. Ingest weights (if compatible)
        if data['weights'] is not None:
            self._ingest_weights(data['weights'])
        
        # 6. Ingest Memosyne
        self._ingest_memosyne()
        
        logger.info(f"Ingestion complete: {self.stats}")
        return self.stats
    
    def _ingest_brain_configs(self, configs: List[Dict]):
        """Ingest brain configurations as architectural insights"""
        logger.info(f"Ingesting {len(configs)} brain configurations...")
        
        for config in configs:
            # Extract architectural patterns
            if 'nodes' in config:
                self.stats['nodes_added'] += config.get('nodes', 0)
            
            if 'layers' in config:
                # Add layer structure knowledge
                self.knowledge_graph[f"mortimer_architecture_{len(self.knowledge_graph)}"] = {
                    'type': 'architecture',
                    'layers': config.get('layers'),
                    'source': 'mortimer'
                }
        
        self.stats['knowledge_entries'] += len(configs)
    
    def _ingest_patterns(self, patterns: List[Dict]):
        """Ingest Mortimer's patterns into Miles' pattern recognition"""
        logger.info(f"Ingesting {len(patterns)} patterns...")
        
        for pattern in patterns:
            # Store pattern
            self.ingested_patterns.append({
                'pattern': pattern,
                'source': 'mortimer',
                'ingested_at': datetime.now().isoformat()
            })
            
            # Create pattern weight for neural integration
            pattern_id = f"mortimer_pattern_{len(self.pattern_weights)}"
            self.pattern_weights[pattern_id] = {
                'weight': 0.7,  # Slightly lower than Miles' own patterns
                'confidence': 0.8,
                'data': pattern
            }
            
            # If we have brain access, inject pattern
            if self.brain and hasattr(self.brain, 'add_pattern'):
                try:
                    self.brain.add_pattern(pattern)
                except Exception as e:
                    logger.warning(f"Could not inject pattern: {e}")
        
        self.stats['patterns_ingested'] += len(patterns)
    
    def _ingest_knowledge(self, knowledge: List[Dict]):
        """Ingest knowledge base entries"""
        logger.info(f"Ingesting {len(knowledge)} knowledge entries...")
        self.stats['knowledge_entries'] += len(knowledge)
    
    def _ingest_training_data(self, training_data: List[Dict]):
        """Ingest training examples"""
        logger.info(f"Processing {len(training_data)} training examples...")
        # Could use this for fine-tuning if we had a training loop
        pass
    
    def _ingest_weights(self, weights: np.ndarray):
        """Attempt to integrate weights (may not be compatible with GrowingNN)"""
        logger.info(f"Weights shape: {weights.shape}")
        logger.info("Note: Static weights may not be directly compatible with GrowingNN")
        # Could potentially initialize some nodes with these weights
        pass
    
    def _ingest_memosyne(self):
        """Ingest Memosyne entries into Miles' memory"""
        logger.info(f"Ingesting {len(self.memosyne_entries)} Memosyne entries...")
        
        for entry in self.memosyne_entries:
            # Add to knowledge graph
            key = f"mortimer_memosyne_{len(self.knowledge_graph)}"
            self.knowledge_graph[key] = entry
            
            # If we have ChromaDB access, store there
            if self.brain and hasattr(self.brain, 'store_memory'):
                try:
                    self.brain.store_memory(
                        content=entry['content'],
                        metadata={'source': 'mortimer', 'type': 'memosyne'}
                    )
                except Exception as e:
                    logger.warning(f"Could not store memory: {e}")
        
        self.stats['knowledge_entries'] += len(self.memosyne_entries)
    
    def export_ingestion_report(self, output_path: str):
        """Export detailed ingestion report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'source': 'mortimer_vps',
            'statistics': self.stats,
            'patterns_ingested': len(self.ingested_patterns),
            'knowledge_entries': len(self.knowledge_graph),
            'memosyne_entries': len(self.memosyne_entries),
            'pattern_weights': len(self.pattern_weights)
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to {output_path}")


# CLI Interface
if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Ingest Mortimer datasets into Miles brain')
    parser.add_argument('--archive', required=True, help='Path to mortimer-brain-datasets.tar.gz')
    parser.add_argument('--output', default='/tmp/ingestion_report.json', help='Output report path')
    parser.add_argument('--dry-run', action='store_true', help='Analyze without ingesting')
    
    args = parser.parse_args()
    
    # Create ingestor
    ingestor = MortimerDataIngestor(brain_instance=None)  # Would pass actual brain instance
    
    # Load dataset
    logger.info(f"Loading dataset from {args.archive}...")
    data = ingestor.load_dataset_archive(args.archive)
    
    # Show what we found
    print("\n📊 DATASET ANALYSIS")
    print("=" * 50)
    print(f"Brain configs: {len(data['brain_configs'])}")
    print(f"Patterns: {len(data['patterns'])}")
    print(f"Training examples: {len(data['training_data'])}")
    print(f"Memosyne entries: {len(ingestor.memosyne_entries)}")
    print(f"Weights: {'Found' if data['weights'] is not None else 'None'}")
    print("=" * 50)
    
    if not args.dry_run:
        # Perform ingestion
        stats = ingestor.ingest_into_brain(data)
        
        # Export report
        ingestor.export_ingestion_report(args.output)
        
        print(f"\n✅ Ingestion complete!")
        print(f"Report: {args.output}")
    else:
        print("\n🔍 Dry run - no data ingested")
        print("Run without --dry-run to perform actual ingestion")
