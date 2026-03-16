#!/usr/bin/env python3
"""
Error Prediction Module
Predicts failures before they happen using trend analysis
"""

import sqlite3
import time
import os
import statistics
from collections import deque

class ErrorPredictor:
    """
    Analyzes trends to predict errors before they occur
    """
    
    def __init__(self, window_size=50):
        self.window_size = window_size
        self.error_history = deque(maxlen=window_size)
        self.performance_metrics = deque(maxlen=window_size)
        self.prediction_threshold = 0.7
        
    def record_metric(self, metric_name, value, timestamp=None):
        """Record a performance metric"""
        if timestamp is None:
            timestamp = time.time()
        
        self.performance_metrics.append({
            'name': metric_name,
            'value': value,
            'timestamp': timestamp
        })
    
    def analyze_trends(self):
        """Analyze recent trends for warning signs"""
        
        if len(self.performance_metrics) < 10:
            return {'status': 'insufficient_data', 'confidence': 0.0}
        
        # Extract values
        values = [m['value'] for m in self.performance_metrics]
        
        # Calculate trend
        if len(values) >= 2:
            # Linear regression slope
            n = len(values)
            x = list(range(n))
            
            x_mean = statistics.mean(x)
            y_mean = statistics.mean(values)
            
            numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
            
            if denominator > 0:
                slope = numerator / denominator
            else:
                slope = 0
            
            # Detect concerning trends
            warnings = []
            
            # Rapid increase in errors
            if slope > 0.1 and values[-1] > 0.5:
                warnings.append({
                    'type': 'error_spike',
                    'severity': 'high',
                    'message': f'Error rate increasing rapidly: {slope:.3f}/tick',
                    'confidence': min(0.9, abs(slope))
                })
            
            # Memory pressure
            if 'memory' in str(self.performance_metrics[-1].get('name', '')):
                if values[-1] > 0.9:
                    warnings.append({
                        'type': 'memory_pressure',
                        'severity': 'critical',
                        'message': f'Memory usage critical: {values[-1]:.1%}',
                        'confidence': 0.95
                    })
            
            # Performance degradation
            if slope > 0.05 and len(values) > 20:
                recent_avg = statistics.mean(values[-10:])
                older_avg = statistics.mean(values[-20:-10])
                
                if recent_avg > older_avg * 1.5:
                    warnings.append({
                        'type': 'performance_degradation',
                        'severity': 'medium',
                        'message': f'Performance degraded by {(recent_avg/older_avg - 1)*100:.1f}%',
                        'confidence': 0.7
                    })
            
            return {
                'status': 'analyzed',
                'slope': slope,
                'warnings': warnings,
                'confidence': min(0.9, len(values) / self.window_size)
            }
        
        return {'status': 'no_trend', 'confidence': 0.0}
    
    def predict_failure(self, hours_ahead=1):
        """Predict likelihood of failure in next N hours"""
        
        trend = self.analyze_trends()
        
        if trend['status'] != 'analyzed':
            return {'prediction': 'unknown', 'confidence': 0.0}
        
        warnings = trend.get('warnings', [])
        
        if any(w['severity'] == 'critical' for w in warnings):
            return {
                'prediction': 'failure_likely',
                'timeframe': f'{hours_ahead}h',
                'confidence': 0.9,
                'reasons': [w['message'] for w in warnings if w['severity'] == 'critical']
            }
        
        elif len(warnings) >= 2:
            return {
                'prediction': 'degradation_expected',
                'timeframe': f'{hours_ahead}h',
                'confidence': 0.7,
                'reasons': [w['message'] for w in warnings]
            }
        
        elif trend.get('slope', 0) > 0.05:
            return {
                'prediction': 'trending_negative',
                'timeframe': f'{hours_ahead}h',
                'confidence': 0.5,
                'reasons': ['Negative trend detected']
            }
        
        return {
            'prediction': 'stable',
            'confidence': 0.8,
            'reasons': ['No concerning trends']
        }

if __name__ == "__main__":
    predictor = ErrorPredictor()
    
    # Simulate some data
    for i in range(30):
        # Simulate increasing error rate
        error_rate = 0.05 + (i * 0.02) + (0.01 if i > 20 else 0)
        predictor.record_metric('error_rate', error_rate)
    
    result = predictor.analyze_trends()
    print("Trend Analysis:")
    print(f"  Status: {result['status']}")
    print(f"  Slope: {result.get('slope', 'N/A')}")
    print(f"  Warnings: {len(result.get('warnings', []))}")
    
    for warning in result.get('warnings', []):
        print(f"    ⚠️  [{warning['severity'].upper()}] {warning['message']}")
    
    prediction = predictor.predict_failure(hours_ahead=2)
    print(f"\nPrediction: {prediction['prediction']}")
    print(f"Confidence: {prediction['confidence']}")
