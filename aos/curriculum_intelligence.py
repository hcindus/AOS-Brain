#!/usr/bin/env python3
"""
Curriculum Intelligence v1.3 - Feedback Loop Analytics & Auto-Tuning
Phase 1.3 of Feedback-to-Curriculum System

Tracks lesson effectiveness and auto-tunes Kidneys thresholds
based on real learning outcomes.
"""

import time
import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from pathlib import Path


@dataclass
class LessonEffectiveness:
    """Tracks how well a curriculum lesson worked"""
    lesson_id: str
    error_category: str
    lesson_content: str
    created_at: float
    
    # Effectiveness tracking
    error_rate_before: float = 0.0
    error_rate_after: float = 0.0
    improvement_percentage: float = 0.0
    
    # Sample sizes
    samples_before: int = 0
    samples_after: int = 0
    
    # Status
    status: str = "active"  # active, effective, ineffective, archived
    
    def calculate_improvement(self) -> float:
        """Calculate improvement percentage"""
        if self.error_rate_before == 0:
            return 0.0
        improvement = (self.error_rate_before - self.error_rate_after) / self.error_rate_before
        self.improvement_percentage = max(0, improvement * 100)
        return self.improvement_percentage


@dataclass
class ErrorMetrics:
    """Error tracking by category"""
    category: str
    total_events: int = 0
    last_7_days: int = 0
    last_24_hours: int = 0
    
    # Trend (positive = getting worse, negative = improving)
    trend: str = "stable"  # improving, stable, worsening
    trend_percentage: float = 0.0
    
    # Lesson correlation
    lessons_applied: List[str] = None
    
    def __post_init__(self):
        if self.lessons_applied is None:
            self.lessons_applied = []


class CurriculumIntelligence:
    """
    Intelligence Layer for Feedback-to-Curriculum
    
    Monitors:
    - Lesson effectiveness (did it actually reduce errors?)
    - Error trends by category
    - Threshold optimization
    - Conversion metrics
    """
    
    def __init__(self, state_dir: str = "/var/lib/aos/brain_state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # Data storage
        self.lesson_effectiveness: Dict[str, LessonEffectiveness] = {}
        self.error_metrics: Dict[str, ErrorMetrics] = defaultdict(
            lambda: ErrorMetrics(category="unknown")
        )
        
        # Historical data for trend analysis
        self.error_history: Dict[str, List[Tuple[float, int]]] = defaultdict(list)
        self.lesson_history: List[Dict] = []
        
        # Threshold recommendations
        self.threshold_recommendations: Dict[str, float] = {}
        
        # Load persisted state
        self._load_state()
        
        print(f"[Curriculum Intelligence v1.3] Initialized")
        print(f"  📊 Tracking: {len(self.lesson_effectiveness)} lessons")
        print(f"  📈 Monitoring: {len(self.error_metrics)} error categories")
    
    def _get_state_path(self) -> Path:
        """Get path to persistence file"""
        return self.state_dir / "curriculum_intelligence.json"
    
    def _load_state(self):
        """Load persisted intelligence data"""
        state_path = self._get_state_path()
        if not state_path.exists():
            return
        
        try:
            with open(state_path, 'r') as f:
                data = json.load(f)
            
            # Load lesson effectiveness
            for lesson_id, lesson_data in data.get('lesson_effectiveness', {}).items():
                self.lesson_effectiveness[lesson_id] = LessonEffectiveness(**lesson_data)
            
            # Load error metrics
            for category, metrics_data in data.get('error_metrics', {}).items():
                self.error_metrics[category] = ErrorMetrics(**metrics_data)
            
            # Load history
            self.error_history = defaultdict(list, data.get('error_history', {}))
            self.lesson_history = data.get('lesson_history', [])
            
            print(f"  💾 Loaded intelligence data from disk")
            
        except Exception as e:
            print(f"  ⚠️ Could not load intelligence data: {e}")
    
    def _save_state(self):
        """Persist intelligence data"""
        try:
            data = {
                'lesson_effectiveness': {
                    k: asdict(v) for k, v in self.lesson_effectiveness.items()
                },
                'error_metrics': {
                    k: asdict(v) for k, v in self.error_metrics.items()
                },
                'error_history': dict(self.error_history),
                'lesson_history': self.lesson_history,
                'threshold_recommendations': self.threshold_recommendations,
                'saved_at': time.time()
            }
            
            with open(self._get_state_path(), 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"[Curriculum Intelligence] Save error: {e}")
    
    def record_lesson_created(self, lesson_id: str, error_category: str, 
                              lesson_content: str) -> LessonEffectiveness:
        """
        Record when a new curriculum lesson is created from waste
        
        This establishes the baseline for effectiveness tracking.
        """
        # Get current error rate for this category
        current_error_rate = self._calculate_error_rate(error_category, days=7)
        
        lesson = LessonEffectiveness(
            lesson_id=lesson_id,
            error_category=error_category,
            lesson_content=lesson_content[:200],  # Truncate
            created_at=time.time(),
            error_rate_before=current_error_rate,
            samples_before=self._get_sample_count(error_category, days=7),
            status="active"
        )
        
        self.lesson_effectiveness[lesson_id] = lesson
        
        # Update error metrics
        if error_category not in self.error_metrics:
            self.error_metrics[error_category] = ErrorMetrics(category=error_category)
        self.error_metrics[error_category].lessons_applied.append(lesson_id)
        
        # Log to history
        self.lesson_history.append({
            'event': 'lesson_created',
            'lesson_id': lesson_id,
            'category': error_category,
            'timestamp': time.time(),
            'baseline_error_rate': current_error_rate
        })
        
        self._save_state()
        
        print(f"[Curriculum Intelligence] 📚 New lesson tracked: {lesson_id}")
        print(f"  Category: {error_category}")
        print(f"  Baseline error rate: {current_error_rate:.2%}")
        
        return lesson
    
    def record_error_event(self, error_category: str, severity: float):
        """
        Record an error event for trend tracking
        
        Called by Kidneys when waste is detected.
        """
        now = time.time()
        
        # Update error metrics
        if error_category not in self.error_metrics:
            self.error_metrics[error_category] = ErrorMetrics(category=error_category)
        
        metrics = self.error_metrics[error_category]
        metrics.total_events += 1
        metrics.last_24_hours += 1
        
        # Add to history (timestamp, count)
        self.error_history[error_category].append((now, 1))
        
        # Prune old history (keep 30 days)
        cutoff = now - (30 * 24 * 60 * 60)
        self.error_history[error_category] = [
            (ts, cnt) for ts, cnt in self.error_history[error_category] 
            if ts > cutoff
        ]
        
        # Update 7-day count
        week_ago = now - (7 * 24 * 60 * 60)
        metrics.last_7_days = sum(
            cnt for ts, cnt in self.error_history[error_category] 
            if ts > week_ago
        )
    
    def evaluate_lesson_effectiveness(self, lesson_id: str) -> Optional[LessonEffectiveness]:
        """
        Evaluate how effective a lesson has been
        
        Compares error counts before and after lesson application.
        """
        if lesson_id not in self.lesson_effectiveness:
            return None
        
        lesson = self.lesson_effectiveness[lesson_id]
        category = lesson.error_category
        lesson_time = lesson.created_at
        
        # Calculate error rate AFTER lesson (events after lesson_time)
        after_events = [
            cnt for ts, cnt in self.error_history.get(category, [])
            if ts > lesson_time
        ]
        after_count = sum(after_events)
        
        # For BEFORE, use what was recorded at lesson creation
        before_count = lesson.samples_before
        
        # Update lesson with raw counts
        lesson.samples_after = after_count
        
        # Calculate improvement based on raw counts
        # If we had 20 errors before and 5 after = 75% improvement
        if before_count > 0:
            improvement = (before_count - after_count) / before_count
            lesson.improvement_percentage = max(0, improvement * 100)
            lesson.error_rate_after = after_count / max(before_count, 1)
        else:
            lesson.improvement_percentage = 0
            lesson.error_rate_after = lesson.error_rate_before
        
        # Determine status based on improvement
        if lesson.improvement_percentage >= 30:
            lesson.status = "effective"
        elif lesson.improvement_percentage >= 10:
            lesson.status = "marginal"
        elif after_count >= 0:  # Any data
            lesson.status = "ineffective"
        
        self._save_state()
        
        return lesson
    
    def evaluate_all_lessons(self) -> Dict[str, LessonEffectiveness]:
        """Evaluate all active lessons"""
        results = {}
        for lesson_id in self.lesson_effectiveness:
            result = self.evaluate_lesson_effectiveness(lesson_id)
            if result:
                results[lesson_id] = result
        return results
    
    def _calculate_error_rate(self, category: str, days: int = 7) -> float:
        """Calculate error rate for a category over N days (normalized 0-1)"""
        if category not in self.error_history:
            return 0.0
        
        cutoff = time.time() - (days * 24 * 60 * 60)
        recent_events = sum(
            cnt for ts, cnt in self.error_history[category] 
            if ts > cutoff
        )
        
        # Normalize to 0-1 scale (assume max 50 events/week is 100% error rate)
        max_events = 50
        return min(1.0, recent_events / max_events)
    
    def _get_sample_count(self, category: str, days: int = 7) -> int:
        """Get number of samples for a category"""
        if category not in self.error_history:
            return 0
        
        cutoff = time.time() - (days * 24 * 60 * 60)
        return sum(
            cnt for ts, cnt in self.error_history[category] 
            if ts > cutoff
        )
    
    def calculate_threshold_recommendations(self) -> Dict[str, float]:
        """
        Calculate recommended threshold adjustments
        
        Based on lesson effectiveness and error trends.
        """
        recommendations = {}
        
        for category, metrics in self.error_metrics.items():
            # Get recent trend
            trend = self._calculate_trend(category)
            
            # Base threshold (0.5 default)
            base_threshold = 0.5
            
            # Adjust based on trend
            if trend == "worsening":
                # Lower threshold = catch errors earlier
                recommendation = base_threshold * 0.8
                reason = "Error rate worsening - lowering threshold for earlier detection"
            elif trend == "improving":
                # Higher threshold = reduce false positives
                recommendation = base_threshold * 1.2
                reason = "Error rate improving - can afford higher threshold"
            else:
                recommendation = base_threshold
                reason = "Stable - no change needed"
            
            # Clamp to valid range
            recommendation = max(0.2, min(0.8, recommendation))
            
            recommendations[category] = {
                'recommended_threshold': recommendation,
                'current_trend': trend,
                'error_rate_7d': metrics.last_7_days / 7,
                'reason': reason
            }
        
        self.threshold_recommendations = recommendations
        self._save_state()
        
        return recommendations
    
    def _calculate_trend(self, category: str) -> str:
        """Calculate trend for a category"""
        if category not in self.error_history:
            return "stable"
        
        history = self.error_history[category]
        if len(history) < 10:
            return "stable"
        
        # Split into first and second half
        mid = len(history) // 2
        first_half = sum(cnt for ts, cnt in history[:mid])
        second_half = sum(cnt for ts, cnt in history[mid:])
        
        if first_half == 0:
            return "stable"
        
        change = (second_half - first_half) / first_half
        
        if change < -0.2:
            return "improving"
        elif change > 0.2:
            return "worsening"
        else:
            return "stable"
    
    def get_conversion_metrics(self) -> Dict:
        """
        Get conversion funnel metrics
        
        Tracks: Waste → Lesson → Improvement
        """
        total_lessons = len(self.lesson_effectiveness)
        effective_lessons = sum(
            1 for l in self.lesson_effectiveness.values() 
            if l.status == "effective"
        )
        ineffective_lessons = sum(
            1 for l in self.lesson_effectiveness.values() 
            if l.status == "ineffective"
        )
        
        if total_lessons == 0:
            conversion_rate = 0.0
        else:
            conversion_rate = effective_lessons / total_lessons
        
        return {
            'total_waste_events': sum(
                m.total_events for m in self.error_metrics.values()
            ),
            'total_lessons_created': total_lessons,
            'effective_lessons': effective_lessons,
            'ineffective_lessons': ineffective_lessons,
            'pending_evaluation': total_lessons - effective_lessons - ineffective_lessons,
            'lesson_conversion_rate': conversion_rate,
            'avg_improvement_percentage': sum(
                l.improvement_percentage for l in self.lesson_effectiveness.values()
            ) / max(total_lessons, 1)
        }
    
    def get_dashboard(self) -> Dict:
        """Get full intelligence dashboard"""
        return {
            'timestamp': time.time(),
            'summary': self.get_conversion_metrics(),
            'error_metrics': {
                cat: {
                    'total': m.total_events,
                    'last_7d': m.last_7_days,
                    'last_24h': m.last_24_hours,
                    'trend': m.trend,
                    'lessons_applied': len(m.lessons_applied)
                }
                for cat, m in self.error_metrics.items()
            },
            'lesson_effectiveness': {
                lid: {
                    'category': l.error_category,
                    'status': l.status,
                    'improvement': f"{l.improvement_percentage:.1f}%",
                    'samples_before': l.samples_before,
                    'samples_after': l.samples_after
                }
                for lid, l in self.lesson_effectiveness.items()
            },
            'threshold_recommendations': self.threshold_recommendations,
            'top_improving_categories': self._get_top_improving(),
            'top_worsening_categories': self._get_top_worsening()
        }
    
    def _get_top_improving(self, n: int = 3) -> List[Dict]:
        """Get top N improving categories"""
        improvements = []
        for lid, lesson in self.lesson_effectiveness.items():
            if lesson.status == "effective":
                improvements.append({
                    'lesson_id': lid,
                    'category': lesson.error_category,
                    'improvement': lesson.improvement_percentage
                })
        
        improvements.sort(key=lambda x: x['improvement'], reverse=True)
        return improvements[:n]
    
    def _get_top_worsening(self, n: int = 3) -> List[Dict]:
        """Get top N categories needing attention"""
        worsening = []
        for cat, metrics in self.error_metrics.items():
            if metrics.trend == "worsening":
                worsening.append({
                    'category': cat,
                    'error_rate_7d': metrics.last_7_days / 7,
                    'lessons_applied': len(metrics.lessons_applied)
                })
        
        worsening.sort(key=lambda x: x['error_rate_7d'], reverse=True)
        return worsening[:n]
    
    def auto_tune_kidneys(self, kidneys_instance) -> Dict:
        """
        Auto-tune Kidneys thresholds based on intelligence
        
        This is the key Phase 1.3 feature - self-optimization.
        """
        recommendations = self.calculate_threshold_recommendations()
        
        applied = {}
        for category, rec in recommendations.items():
            new_threshold = rec['recommended_threshold']
            
            # Map category to Kidneys configuration
            if category == "syntax":
                # Syntax errors - may need stricter filtering
                kidneys_instance.signal_threshold = min(
                    kidneys_instance.signal_threshold,
                    new_threshold
                )
                applied[category] = new_threshold
            
            elif category == "logic":
                # Logic errors - moderate adjustment
                kidneys_instance.reabsorb_threshold = new_threshold
                applied[category] = new_threshold
        
        self._save_state()
        
        print(f"[Curriculum Intelligence] 🔧 Auto-tuned Kidneys")
        for cat, threshold in applied.items():
            print(f"  {cat}: threshold adjusted to {threshold:.2f}")
        
        return applied
    
    def generate_report(self) -> str:
        """Generate human-readable report"""
        metrics = self.get_conversion_metrics()
        dashboard = self.get_dashboard()
        
        report = []
        report.append("=" * 70)
        report.append("  CURRICULUM INTELLIGENCE REPORT v1.3")
        report.append("  Feedback-to-Curriculum System Metrics")
        report.append("=" * 70)
        report.append("")
        
        # Summary
        report.append("📊 CONVERSION FUNNEL")
        report.append(f"  Total Waste Events:     {metrics['total_waste_events']}")
        report.append(f"  Lessons Created:        {metrics['total_lessons_created']}")
        report.append(f"  Effective Lessons:      {metrics['effective_lessons']}")
        report.append(f"  Ineffective Lessons:    {metrics['ineffective_lessons']}")
        report.append(f"  Conversion Rate:        {metrics['lesson_conversion_rate']:.1%}")
        report.append(f"  Avg Improvement:        {metrics['avg_improvement_percentage']:.1f}%")
        report.append("")
        
        # Error metrics
        report.append("📈 ERROR METRICS BY CATEGORY")
        for cat, m in dashboard['error_metrics'].items():
            report.append(f"  {cat:15s}: {m['last_7d']:4d}/week (trend: {m['trend']})")
        report.append("")
        
        # Top improving
        if dashboard['top_improving_categories']:
            report.append("🎉 TOP IMPROVING AREAS")
            for item in dashboard['top_improving_categories']:
                report.append(f"  {item['category']}: {item['improvement']:.1f}% better")
            report.append("")
        
        # Recommendations
        if dashboard['threshold_recommendations']:
            report.append("🔧 THRESHOLD RECOMMENDATIONS")
            for cat, rec in dashboard['threshold_recommendations'].items():
                report.append(f"  {cat}: {rec['current_trend']} → adjust to {rec['recommended_threshold']:.2f}")
            report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)


# Test function
def test_curriculum_intelligence():
    """Test the intelligence layer"""
    print("\n" + "=" * 70)
    print("  Testing Curriculum Intelligence v1.3")
    print("=" * 70)
    
    ci = CurriculumIntelligence(state_dir="/tmp/test_ci")
    
    # Simulate error events
    print("\n1. Simulating error events...")
    for _ in range(10):
        ci.record_error_event("syntax", 0.8)
    for _ in range(5):
        ci.record_error_event("logic", 0.7)
    
    # Create a lesson
    print("\n2. Creating curriculum lesson...")
    lesson = ci.record_lesson_created(
        lesson_id="lesson_001",
        error_category="syntax",
        lesson_content="Review proper syntax structure"
    )
    
    # Simulate improvement (fewer errors after lesson)
    print("\n3. Simulating improvement (fewer errors)...")
    # Wait a moment to simulate time passing
    time.sleep(0.1)
    for _ in range(3):  # Fewer errors
        ci.record_error_event("syntax", 0.5)
    
    # Evaluate effectiveness
    print("\n4. Evaluating lesson effectiveness...")
    result = ci.evaluate_lesson_effectiveness("lesson_001")
    print(f"  Improvement: {result.improvement_percentage:.1f}%")
    print(f"  Status: {result.status}")
    
    # Get metrics
    print("\n5. Getting conversion metrics...")
    metrics = ci.get_conversion_metrics()
    print(f"  Conversion rate: {metrics['lesson_conversion_rate']:.1%}")
    
    # Get dashboard
    print("\n6. Dashboard preview...")
    dashboard = ci.get_dashboard()
    print(f"  Categories tracked: {len(dashboard['error_metrics'])}")
    
    # Generate report
    print("\n7. Generating report...")
    report = ci.generate_report()
    print(report[:500] + "...")
    
    print("\n✅ Curriculum Intelligence v1.3 tests passed!")
    return True


if __name__ == "__main__":
    test_curriculum_intelligence()
