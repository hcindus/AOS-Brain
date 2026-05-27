#!/usr/bin/env python3
"""
AOS MARKET SENSE v1.0
Real-time trading data feeder for brain cortex
Connects to data sources for live market signals
"""

import numpy as np
import json
import socket
import time
import threading
import hashlib
from typing import List, Dict, Tuple
from datetime import datetime

class MarketSense:
    """
    Market data sensory input for brain
    Feeds price action, volume, volatility as neural patterns
    """
    
    def __init__(self, brain_socket='/tmp/aos_brain.sock', agent_id="market_sense"):
        self.brain_socket = brain_socket
        self.agent_id = agent_id
        self.running = False
        self.tick = 0
        
        # Market state simulation
        self.symbols = ['BTC', 'ETH', 'SOL', 'XRP', 'DOGE']
        self.prices = {s: 100.0 + i*50 for i, s in enumerate(self.symbols)}
        self.volumes = {s: 1000000.0 for s in self.symbols}
        self.volatility = {s: 0.02 for s in self.symbols}
        
        # Pattern memory
        self.price_history = {s: [] for s in self.symbols}
        self.max_history = 20
        
        self.stats = {'feeds': 0, 'hotspots': 0}
        
        print("[MarketSense] Initialized")
        print(f"  Symbols: {', '.join(self.symbols)}")
    
    def _send(self, cmd, params):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.brain_socket)
            sock.sendall((json.dumps({'cmd': cmd, 'params': params}) + '\n').encode())
            data = sock.recv(4096)
            sock.close()
            return json.loads(data.decode()) if data else {}
        except Exception as e:
            return {'error': str(e)}
    
    def _update_market(self):
        """Simulate market movement"""
        for symbol in self.symbols:
            # Random walk with momentum
            change = np.random.randn() * self.volatility[symbol]
            self.prices[symbol] *= (1 + change)
            
            # Volume varies
            self.volumes[symbol] *= (0.9 + 0.2 * np.random.random())
            
            # Volatility mean reversion
            self.volatility[symbol] = 0.02 + 0.5 * abs(change)
            
            # Store history
            self.price_history[symbol].append(self.prices[symbol])
            if len(self.price_history[symbol]) > self.max_history:
                self.price_history[symbol].pop(0)
    
    def _calculate_features(self, symbol: str) -> Dict:
        """Calculate market features"""
        price = self.prices[symbol]
        volume = self.volumes[symbol]
        vol = self.volatility[symbol]
        
        history = self.price_history[symbol]
        
        # Price momentum
        if len(history) >= 5:
            momentum = (history[-1] - history[-5]) / history[-5]
        else:
            momentum = 0
        
        # Trend direction
        if len(history) >= 10:
            trend = np.polyfit(range(len(history)), history, 1)[0] / price
        else:
            trend = 0
        
        # Price volatility
        if len(history) > 1:
            price_vol = np.std(history) / np.mean(history)
        else:
            price_vol = 0
        
        return {
            'symbol': symbol,
            'price': price,
            'price_normalized': price / 1000.0,  # Normalize
            'volume_normalized': np.log(volume) / 20.0,
            'volatility': vol * 10,  # Scale up
            'momentum': momentum * 10,
            'trend': trend * 100,
            'price_volatility': price_vol * 5
        }
    
    def _encode_to_ternary(self, features: Dict) -> List[List[int]]:
        """Encode market data to ternary hotspots"""
        hotspots = []
        
        symbol_hash = int(hashlib.md5(features['symbol'].encode()).hexdigest(), 16)
        z_base = symbol_hash % 8  # Each symbol gets different Z slice
        
        # Price levels
        price_level = int(features['price_normalized'] * 10) % 32
        
        # Encode price direction
        if features['momentum'] > 0.1:
            t = 1  # Up
        elif features['momentum'] < -0.1:
            t = -1  # Down
        else:
            t = 0
        
        if t != 0:
            for i in range(5):
                x = (price_level + i) % 32
                y = (int(features['volume_normalized'] * 10) + i) % 32
                z = (z_base + int(features['volatility'] * 10)) % 32
                hotspots.append([x, y, z, t])
        
        # Encode volatility
        if features['volatility'] > 0.3:
            for i in range(3):
                x = (16 + i) % 32
                y = (16 + int(features['volatility'] * 10)) % 32
                z = (z_base + 16) % 32
                hotspots.append([x, y, z, 1 if features['momentum'] > 0 else -1])
        
        return hotspots
    
    def _detect_patterns(self) -> List[str]:
        """Detect market patterns"""
        patterns = []
        
        for symbol in self.symbols:
            history = self.price_history[symbol]
            if len(history) < 10:
                continue
            
            # Breakout detection
            recent_high = max(history[-5:])
            previous_high = max(history[:-5]) if len(history) > 5 else recent_high
            if recent_high > previous_high * 1.05:
                patterns.append(f"{symbol}_breakout_up")
            
            # Crash detection
            if history[-1] < history[0] * 0.95:
                patterns.append(f"{symbol}_selloff")
            
            # Volatility spike
            recent_vol = np.std(history[-5:])
            older_vol = np.std(history[:-5]) if len(history) > 5 else recent_vol
            if recent_vol > older_vol * 2:
                patterns.append(f"{symbol}_vol_spike")
        
        return patterns
    
    def capture(self):
        """Capture market state and feed to brain"""
        self._update_market()
        
        all_hotspots = []
        pattern_triggers = []
        
        for symbol in self.symbols:
            features = self._calculate_features(symbol)
            hotspots = self._encode_to_ternary(features)
            all_hotspots.extend(hotspots)
            
            # Check for significant moves
            if abs(features['momentum']) > 0.5:
                pattern_triggers.append({
                    'symbol': symbol,
                    'momentum': features['momentum'],
                    'action': 'alert_large_move'
                })
        
        # Detect broader patterns
        patterns = self._detect_patterns()
        
        # Send to brain
        if all_hotspots:
            priority = 0.7 + (0.2 if pattern_triggers else 0)
            
            result = self._send('cortex_write', {
                'agent_id': self.agent_id,
                'regions': [4, 5],  # Trading regions
                'activations': all_hotspots[:256],
                'priority': priority,
                'ephemeral': False
            })
            
            self._send('cortex_tick', {})
            
            # Fire pattern triggers
            for trigger in pattern_triggers:
                print(f"  💹 MARKET ALERT: {trigger['symbol']} "
                      f"moved {trigger['momentum']:.2f}%")
            
            self.stats['feeds'] += 1
            self.stats['hotspots'] += len(all_hotspots)
        
        if self.tick % 10 == 0:
            btc = self.prices['BTC']
            vol = self.volatility['BTC']
            print(f"[Market] Tick {self.tick}: BTC=${btc:.2f} "
                  f"vol={vol:.3f} patterns={len(patterns)}")
        
        self.tick += 1
    
    def run(self, interval=2.0):
        """Run market feed loop"""
        self.running = True
        self._send('cortex_register', {'agent_id': self.agent_id})
        
        print(f"[MarketSense] Running every {interval}s...")
        while self.running:
            self.capture()
            time.sleep(interval)

def main():
    market = MarketSense()
    market.run()

if __name__ == "__main__":
    main()
