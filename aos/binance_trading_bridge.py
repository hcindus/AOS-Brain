#!/usr/bin/env python3
"""
BINANCE TRADING BRIDGE - Live Paper Trading for Trading Agent

Connects the autonomous trading agent to Binance Paper Trading API.
Executes real trades, tracks actual P&L, learns from live market data.

Uses: python-binance library or direct REST API
Paper Trading URL: https://testnet.binance.vision/
"""

import os
import time
import json
import hmac
import hashlib
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from trading_agent_with_oracle import TradingAgent, TradeAction, TradeDecision, TradeResult

# Try to import python-binance, fallback to direct API
try:
    from binance.client import Client
    from binance.enums import *
    HAS_BINANCE_LIB = True
except ImportError:
    HAS_BINANCE_LIB = False
    print("[BinanceBridge] python-binance not installed, using direct API")


@dataclass
class LiveTrade:
    """A live executed trade"""
    trade_id: str
    symbol: str
    side: str  # BUY or SELL
    quantity: float
    price: float
    order_id: str
    status: str
    timestamp: datetime
    pnl: float = 0.0
    commission: float = 0.0


class BinancePaperTradingBridge:
    """
    Bridge between Trading Agent and Binance Paper Trading
    
    Features:
    - Live market data streaming
    - Real order execution (paper trading)
    - Position tracking
    - P&L calculation
    - Integration with brain learning
    """
    
    def __init__(self, 
                 api_key: str = None,
                 api_secret: str = None,
                 paper_trading: bool = True,
                 testnet: bool = True):
        
        # Get credentials from environment or args
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        self.paper_trading = paper_trading
        self.testnet = testnet
        
        # Paper trading endpoints
        if testnet:
            self.base_url = "https://testnet.binance.vision"
            self.ws_url = "wss://testnet.binance.vision/ws"
        else:
            self.base_url = "https://api.binance.com"
            self.ws_url = "wss://stream.binance.com:9443/ws"
        
        # Initialize client
        self.client = None
        self._init_client()
        
        # Track positions and trades
        self.positions: Dict[str, Dict] = {}  # symbol -> position info
        self.open_orders: Dict[str, Dict] = {}
        self.trade_history: List[LiveTrade] = []
        self.total_pnl = 0.0
        
        print(f"[BinanceBridge] Initialized")
        print(f"  Mode: {'Paper' if paper_trading else 'Live'} Trading")
        print(f"  Testnet: {testnet}")
        print(f"  API Key: {'Set' if self.api_key else 'NOT SET'}")
    
    def _init_client(self):
        """Initialize Binance client"""
        if HAS_BINANCE_LIB and self.api_key and self.api_secret:
            try:
                self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
                print("[BinanceBridge] python-binance client initialized")
            except Exception as e:
                print(f"[BinanceBridge] Client init failed: {e}")
                self.client = None
        else:
            self.client = None
    
    def _sign_request(self, params: Dict) -> str:
        """Sign API request"""
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _api_request(self, method: str, endpoint: str, params: Dict = None, signed: bool = False) -> Dict:
        """Make API request"""
        if params is None:
            params = {}
        
        headers = {'X-MBX-APIKEY': self.api_key}
        
        if signed and self.api_secret:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._sign_request(params)
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif method == 'POST':
                response = requests.post(url, params=params, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, params=params, headers=headers)
            else:
                return {'error': 'Invalid method'}
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e), 'response': getattr(response, 'text', 'N/A')}
    
    def get_account_balance(self) -> Dict:
        """Get account balance"""
        if self.client:
            try:
                account = self.client.get_account()
                balances = {b['asset']: float(b['free']) for b in account['balances'] if float(b['free']) > 0}
                return balances
            except Exception as e:
                return {'error': str(e)}
        else:
            # Fallback to direct API
            return self._api_request('GET', '/api/v3/account', {}, signed=True)
    
    def get_symbol_price(self, symbol: str) -> float:
        """Get current price for symbol"""
        if self.client:
            try:
                ticker = self.client.get_symbol_ticker(symbol=symbol)
                return float(ticker['price'])
            except:
                return 0.0
        else:
            result = self._api_request('GET', '/api/v3/ticker/price', {'symbol': symbol})
            return float(result.get('price', 0))
    
    def get_klines(self, symbol: str, interval: str = '1m', limit: int = 100) -> List:
        """Get candlestick data"""
        """
        Kline format: [
            Open time,
            Open,
            High,
            Low,
            Close,
            Volume,
            Close time,
            ...
        ]
        """
        if self.client:
            try:
                klines = self.client.get_klines(
                    symbol=symbol,
                    interval=interval,
                    limit=limit
                )
                return klines
            except Exception as e:
                print(f"[BinanceBridge] Klines error: {e}")
                return []
        else:
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            return self._api_request('GET', '/api/v3/klines', params)
    
    def place_order(self, symbol: str, side: str, quantity: float,
                   order_type: str = 'MARKET', price: float = None) -> Dict:
        """
        Place a live order
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Amount to trade
            order_type: 'MARKET' or 'LIMIT'
            price: Limit price (for LIMIT orders)
        """
        if not self.api_key or not self.api_secret:
            print("[BinanceBridge] ERROR: API credentials not set")
            return {'error': 'No API credentials'}
        
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
            'timestamp': int(time.time() * 1000)
        }
        
        if order_type == 'LIMIT' and price:
            params['price'] = price
            params['timeInForce'] = 'GTC'
        
        if self.paper_trading:
            print(f"[BinanceBridge] PAPER TRADE: {side} {quantity} {symbol}")
        
        if self.client:
            try:
                order = self.client.create_order(**params)
                
                live_trade = LiveTrade(
                    trade_id=str(int(time.time())),
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    price=float(order.get('price', 0)),
                    order_id=str(order.get('orderId', 0)),
                    status=order.get('status', 'UNKNOWN'),
                    timestamp=datetime.now()
                )
                self.trade_history.append(live_trade)
                
                return {
                    'success': True,
                    'order': order,
                    'trade_id': live_trade.trade_id
                }
            except Exception as e:
                return {'error': str(e)}
        else:
            # Direct API
            return self._api_request('POST', '/api/v3/order', params, signed=True)
    
    def calculate_position_size(self, symbol: str, capital: float,
                                confidence: float, max_position: float = 0.2) -> float:
        """
        Calculate position size based on confidence and available capital
        
        Returns: quantity in base asset (e.g., BTC amount)
        """
        price = self.get_symbol_price(symbol)
        if price == 0:
            return 0.0
        
        # Calculate USDT amount to use
        usdt_to_use = capital * confidence * max_position
        
        # Convert to base asset quantity
        quantity = usdt_to_use / price
        
        # Round to appropriate precision (Binance requirements)
        # Most pairs need quantity rounded to specific decimal places
        if symbol.startswith('BTC'):
            quantity = round(quantity, 5)
        elif symbol.startswith('ETH'):
            quantity = round(quantity, 4)
        else:
            quantity = round(quantity, 2)
        
        return quantity
    
    def get_historical_data(self, symbol: str, lookback: int = 25) -> Tuple[List[float], List[float]]:
        """
        Get historical price and volume data for analysis
        
        Returns: (prices, volumes)
        """
        klines = self.get_klines(symbol, interval='1m', limit=lookback)
        
        prices = []
        volumes = []
        
        for kline in klines:
            if isinstance(kline, list) and len(kline) >= 6:
                # Close price
                prices.append(float(kline[4]))
                # Volume
                volumes.append(float(kline[5]))
        
        return prices, volumes
    
    def track_position(self, symbol: str, entry_price: float,
                      quantity: float, side: str):
        """Track an open position"""
        self.positions[symbol] = {
            'entry_price': entry_price,
            'quantity': quantity,
            'side': side,
            'entry_time': datetime.now(),
            'unrealized_pnl': 0.0
        }
    
    def update_positions(self):
        """Update P&L for all open positions"""
        for symbol, position in self.positions.items():
            current_price = self.get_symbol_price(symbol)
            if current_price > 0:
                if position['side'] == 'BUY':
                    pnl = (current_price - position['entry_price']) * position['quantity']
                else:
                    pnl = (position['entry_price'] - current_price) * position['quantity']
                
                position['unrealized_pnl'] = pnl
                position['current_price'] = current_price
    
    def close_position(self, symbol: str) -> Optional[LiveTrade]:
        """Close an open position"""
        if symbol not in self.positions:
            return None
        
        position = self.positions[symbol]
        
        # Place closing order
        close_side = 'SELL' if position['side'] == 'BUY' else 'BUY'
        
        result = self.place_order(
            symbol=symbol,
            side=close_side,
            quantity=position['quantity']
        )
        
        if result.get('success'):
            # Calculate realized P&L
            realized_pnl = position.get('unrealized_pnl', 0)
            self.total_pnl += realized_pnl
            
            # Create trade record
            trade = LiveTrade(
                trade_id=str(int(time.time())),
                symbol=symbol,
                side=close_side,
                quantity=position['quantity'],
                price=position.get('current_price', position['entry_price']),
                order_id=result['order'].get('orderId', '0'),
                status='FILLED',
                timestamp=datetime.now(),
                pnl=realized_pnl
            )
            
            del self.positions[symbol]
            self.trade_history.append(trade)
            
            return trade
        
        return None
    
    def get_performance_stats(self) -> Dict:
        """Get trading performance statistics"""
        if not self.trade_history:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0,
                'avg_trade_pnl': 0.0,
                'win_rate': 0.0
            }
        
        winning = sum(1 for t in self.trade_history if t.pnl > 0)
        losing = sum(1 for t in self.trade_history if t.pnl <= 0)
        total_pnl = sum(t.pnl for t in self.trade_history)
        
        return {
            'total_trades': len(self.trade_history),
            'winning_trades': winning,
            'losing_trades': losing,
            'total_pnl': total_pnl,
            'avg_trade_pnl': total_pnl / len(self.trade_history),
            'win_rate': winning / len(self.trade_history) if self.trade_history else 0.0
        }


class AutonomousLiveTrader:
    """
    Fully autonomous trader with live Binance paper trading
    
    Combines:
    - Trading Agent (with Oracle consultation)
    - Binance Bridge (live paper trading)
    - Brain integration (learning)
    """
    
    def __init__(self, 
                 trading_agent: TradingAgent,
                 binance_bridge: BinancePaperTradingBridge,
                 symbols: List[str] = None):
        
        self.agent = trading_agent
        self.bridge = binance_bridge
        self.symbols = symbols or ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
        
        self.running = False
        self.trade_count = 0
        
        print("[AutonomousLiveTrader] Initialized")
        print(f"  Symbols: {', '.join(self.symbols)}")
    
    def run_live_session(self, duration_minutes: int = 60):
        """
        Run live trading session
        
        Continuously:
        1. Fetch live market data
        2. Make decisions with Oracle consultation
        3. Execute paper trades
        4. Track and learn
        """
        self.running = True
        start_time = time.time()
        
        print(f"\n[Live Session] Starting for {duration_minutes} minutes...")
        print(f"[Live Session] Paper Trading Mode: {self.bridge.paper_trading}")
        print("=" * 70)
        
        while self.running and (time.time() - start_time) < (duration_minutes * 60):
            for symbol in self.symbols:
                try:
                    # 1. Get live data
                    prices, volumes = self.bridge.get_historical_data(symbol)
                    current_price = self.bridge.get_symbol_price(symbol)
                    
                    if len(prices) < 10 or current_price == 0:
                        continue
                    
                    # 2. Make decision (with Oracle consultation if needed)
                    decision = self.agent.make_trade_decision(
                        prices, volumes, symbol, current_price
                    )
                    
                    # 3. Execute if not HOLD
                    if decision.action != TradeAction.HOLD:
                        # Calculate position size
                        balance = self.bridge.get_account_balance()
                        usdt_balance = balance.get('USDT', 10000.0) if isinstance(balance, dict) else 10000.0
                        
                        quantity = self.bridge.calculate_position_size(
                            symbol, usdt_balance, decision.confidence
                        )
                        
                        if quantity > 0:
                            # Execute paper trade
                            side = 'BUY' if decision.action == TradeAction.BUY else 'SELL'
                            
                            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {symbol}")
                            print(f"  Action: {side} | Price: ${current_price:,.2f}")
                            print(f"  Quantity: {quantity} | Confidence: {decision.confidence:.1%}")
                            
                            if decision.quantum_signal:
                                print(f"  Oracle consulted: {decision.quantum_signal.get('circuit', 'N/A')}")
                            
                            # Place order
                            result = self.bridge.place_order(symbol, side, quantity)
                            
                            if result.get('success'):
                                self.trade_count += 1
                                
                                # Track position
                                self.bridge.track_position(symbol, current_price, quantity, side)
                                
                                # Record in brain
                                self.agent.brain.write_thought(
                                    f"Live trade: {side} {quantity} {symbol} @ ${current_price:,.2f}",
                                    priority=decision.confidence
                                )
                            else:
                                print(f"  Order failed: {result.get('error')}")
                    
                    # Update positions
                    self.bridge.update_positions()
                    
                    # Brief sleep between symbols
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"[LiveTrader] Error with {symbol}: {e}")
                    continue
            
            # Report status every cycle
            stats = self.bridge.get_performance_stats()
            print(f"\n[Status] Trades: {stats['total_trades']} | "
                  f"P&L: ${stats['total_pnl']:,.2f} | "
                  f"Win Rate: {stats['win_rate']:.1%}")
            
            # Sleep before next cycle
            time.sleep(30)  # Check every 30 seconds
        
        self.running = False
        
        # Final report
        print("\n" + "=" * 70)
        print("  LIVE SESSION COMPLETE")
        print("=" * 70)
        final_stats = self.bridge.get_performance_stats()
        print(f"\nTotal Trades: {final_stats['total_trades']}")
        print(f"Win Rate: {final_stats['win_rate']:.1%}")
        print(f"Total P&L: ${final_stats['total_pnl']:,.2f}")
        print(f"Avg P&L per trade: ${final_stats['avg_trade_pnl']:,.2f}")
        
        # Save to brain
        self.agent.brain.ingest(
            content=json.dumps(final_stats),
            source="live_trading_session",
            priority=1.0
        )


def demo_live_setup():
    """Show how to set up live paper trading"""
    print("=" * 70)
    print("  BINANCE PAPER TRADING SETUP")
    print("=" * 70)
    
    print("\n[1] Set up Binance Testnet Account:")
    print("    https://testnet.binance.vision/")
    print("    Create account → Generate API Key")
    
    print("\n[2] Set environment variables:")
    print("    export BINANCE_API_KEY='your_key'")
    print("    export BINANCE_API_SECRET='your_secret'")
    
    print("\n[3] Install python-binance:")
    print("    pip install python-binance")
    
    print("\n[4] Run live session:")
    print("    from trading_agent_with_oracle import TradingAgent")
    print("    from binance_trading_bridge import BinancePaperTradingBridge")
    print("    from binance_trading_bridge import AutonomousLiveTrader")
    print("")
    print("    agent = TradingAgent('live_trader_01')")
    print("    bridge = BinancePaperTradingBridge()")
    print("    trader = AutonomousLiveTrader(agent, bridge)")
    print("    trader.run_live_session(duration_minutes=60)")
    
    print("\n[5] Monitor:")
    print("    - Check https://testnet.binance.vision/ for trades")
    print("    - Agent logs decisions to brain")
    print("    - Performance tracked automatically")
    
    print("\n" + "=" * 70)
    
    # Show if credentials are set
    api_key = os.getenv('BINANCE_API_KEY')
    if api_key:
        print("\n✓ API Key detected")
    else:
        print("\n✗ API Key not set - set BINANCE_API_KEY environment variable")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_live_setup()
    else:
        print("Usage: python3 binance_trading_bridge.py --demo")
        print("\nThis module provides:")
        print("  • BinancePaperTradingBridge - Live API connection")
        print("  • AutonomousLiveTrader - Full autonomous trading loop")
        print("  • Paper trading on Binance Testnet")
        print("  • Real P&L tracking")
        print("\nSet BINANCE_API_KEY and BINANCE_API_SECRET to enable live trading.")