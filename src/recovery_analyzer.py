"""
Smart Recovery Analyzer for FitFlow AI
Analyzes workout intensity and recommends optimal recovery
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path


@dataclass
class WorkoutIntensity:
    """Represents workout intensity metrics"""
    date: str
    total_sets: int
    total_reps: int
    estimated_volume: float  # sets × reps × difficulty multiplier
    muscle_groups: List[str]
    intensity_score: float  # 0-10 scale


@dataclass
class RecoveryMetrics:
    """User recovery metrics"""
    user_id: str
    sleep_quality: Optional[int] = None  # 1-10
    soreness_level: Optional[int] = None  # 1-10
    energy_level: Optional[int] = None  # 1-10
    sore_muscles: List[str] = None
    
    def __post_init__(self):
        if self.sore_muscles is None:
            self.sore_muscles = []


class RecoveryAnalyzer:
    """Analyzes recovery and provides recommendations"""
    
    DIFFICULTY_MULTIPLIERS = {
        'beginner': 0.7,
        'intermediate': 1.0,
        'advanced': 1.3
    }
    
    INTENSITY_THRESHOLDS = {
        'low': 3.0,
        'moderate': 6.0,
        'high': 8.0,
        'very_high': 9.5
    }
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.intensity_file = storage_dir / "workout_intensity.json"
        self.recovery_file = storage_dir / "recovery_metrics.json"
    
    def calculate_intensity(self, workout_data: Dict, difficulty_level: str = 'intermediate') -> WorkoutIntensity:
        """Calculate workout intensity"""
        total_sets = workout_data.get('total_sets', 0)
        total_reps = workout_data.get('total_reps', 0)
        muscle_groups = workout_data.get('muscle_groups', [])
        
        # Base volume
        volume = total_sets * total_reps
        
        # Apply difficulty multiplier
        difficulty_mult = self.DIFFICULTY_MULTIPLIERS.get(difficulty_level, 1.0)
        adjusted_volume = volume * difficulty_mult
        
        # Calculate intensity score (0-10)
        # Assumes ~150 total reps is moderate intensity
        intensity_score = min(10.0, (adjusted_volume / 150) * 6.0)
        
        # Boost for multiple muscle groups (compound effect)
        if len(muscle_groups) > 2:
            intensity_score *= 1.1
        
        return WorkoutIntensity(
            date=datetime.now().isoformat(),
            total_sets=total_sets,
            total_reps=total_reps,
            estimated_volume=adjusted_volume,
            muscle_groups=muscle_groups,
            intensity_score=round(intensity_score, 2)
        )
    
    def save_workout_intensity(self, user_id: str, intensity: WorkoutIntensity):
        """Save workout intensity data"""
        all_data = {}
        if self.intensity_file.exists():
            with open(self.intensity_file, 'r') as f:
                all_data = json.load(f)
        
        if user_id not in all_data:
            all_data[user_id] = []
        
        all_data[user_id].append(asdict(intensity))
        
        # Keep only last 90 days
        all_data[user_id] = all_data[user_id][-90:]
        
        with open(self.intensity_file, 'w') as f:
            json.dump(all_data, f, indent=2)
    
    def get_recent_intensities(self, user_id: str, days: int = 7) -> List[WorkoutIntensity]:
        """Get recent workout intensities"""
        if not self.intensity_file.exists():
            return []
        
        with open(self.intensity_file, 'r') as f:
            all_data = json.load(f)
        
        user_data = all_data.get(user_id, [])
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent = []
        for intensity_data in user_data:
            workout_date = datetime.fromisoformat(intensity_data['date'])
            if workout_date >= cutoff_date:
                recent.append(WorkoutIntensity(**intensity_data))
        
        return recent
    
    def analyze_weekly_load(self, user_id: str) -> Dict:
        """Analyze weekly training load"""
        intensities = self.get_recent_intensities(user_id, days=7)
        
        if not intensities:
            return {
                "status": "no_data",
                "recommendation": "Start tracking your workouts to get personalized recovery insights!"
            }
        
        avg_intensity = sum(i.intensity_score for i in intensities) / len(intensities)
        total_volume = sum(i.estimated_volume for i in intensities)
        workout_count = len(intensities)
        
        # Determine status
        if avg_intensity < self.INTENSITY_THRESHOLDS['moderate']:
            status = "low_intensity"
            recommendation = "You have room to push harder! Consider increasing weight or volume."
        elif avg_intensity < self.INTENSITY_THRESHOLDS['high']:
            status = "optimal"
            recommendation = "Great balance of intensity and volume. Keep it up!"
        elif avg_intensity < self.INTENSITY_THRESHOLDS['very_high']:
            status = "high_intensity"
            recommendation = "You're training hard! Make sure to get adequate rest and nutrition."
        else:
            status = "very_high_intensity"
            recommendation = "⚠️ Very high intensity detected. Consider a deload week to prevent overtraining."
        
        return {
            "status": status,
            "avg_intensity": round(avg_intensity, 2),
            "total_volume": round(total_volume, 0),
            "workout_count": workout_count,
            "recommendation": recommendation
        }
    
    def detect_deload_need(self, user_id: str) -> Dict:
        """Detect if user needs a deload week"""
        # Get last 3 weeks of data
        intensities = self.get_recent_intensities(user_id, days=21)
        
        if len(intensities) < 6:  # Need at least 6 workouts
            return {
                "needs_deload": False,
                "reason": "Insufficient data"
            }
        
        # Split into weeks
        week1 = intensities[-7:] if len(intensities) >= 7 else intensities
        week2 = intensities[-14:-7] if len(intensities) >= 14 else []
        week3 = intensities[-21:-14] if len(intensities) >= 21 else []
        
        # Calculate weekly averages
        weeks = [week for week in [week1, week2, week3] if week]
        weekly_avgs = [
            sum(i.intensity_score for i in week) / len(week)
            for week in weeks
        ]
        
        # Check if intensity has been high for multiple weeks
        high_intensity_weeks = sum(1 for avg in weekly_avgs if avg > self.INTENSITY_THRESHOLDS['high'])
        
        needs_deload = False
        reason = ""
        
        if high_intensity_weeks >= 3:
            needs_deload = True
            reason = "You've maintained high intensity for 3+ weeks. Time for a deload!"
        elif high_intensity_weeks >= 2 and weekly_avgs[0] > self.INTENSITY_THRESHOLDS['very_high']:
            needs_deload = True
            reason = "Recent very high intensity after sustained hard training. Deload recommended."
        
        return {
            "needs_deload": needs_deload,
            "reason": reason,
            "weekly_intensities": [round(avg, 2) for avg in weekly_avgs],
            "deload_week_suggestion": self._generate_deload_plan() if needs_deload else None
        }
    
    def _generate_deload_plan(self) -> Dict:
        """Generate deload week recommendations"""
        return {
            "duration": "1 week",
            "volume_reduction": "40-50%",
            "intensity_reduction": "Keep weight at 60-70% of normal",
            "focus": "Active recovery, mobility work, and technique refinement",
            "benefits": "Muscle repair, CNS recovery, prevent overtraining"
        }
    
    def get_muscle_recovery_status(self, user_id: str) -> Dict:
        """Get recovery status for each muscle group"""
        intensities = self.get_recent_intensities(user_id, days=7)
        
        muscle_last_worked = {}
        for intensity in intensities:
            for muscle in intensity.muscle_groups:
                workout_date = datetime.fromisoformat(intensity.date)
                if muscle not in muscle_last_worked or workout_date > datetime.fromisoformat(muscle_last_worked[muscle]):
                    muscle_last_worked[muscle] = intensity.date
        
        # Calculate days since last workout
        muscle_status = {}
        for muscle, last_date in muscle_last_worked.items():
            days_ago = (datetime.now() - datetime.fromisoformat(last_date)).days
            
            if days_ago <= 2:
                status = "recently_worked"
                color = "red"
            elif days_ago <= 4:
                status = "recovering"
                color = "orange"
            elif days_ago <= 6:
                status = "ready"
                color = "yellow"
            else:
                status = "needs_attention"
                color = "blue"
            
            muscle_status[muscle] = {
                "days_since_workout": days_ago,
                "last_workout": last_date,
                "status": status,
                "color": color
            }
        
        return muscle_status
    
    def get_rest_day_recommendation(self, user_id: str) -> Dict:
        """Recommend if user should take a rest day"""
        recent = self.get_recent_intensities(user_id, days=3)
        
        if not recent:
            return {
                "should_rest": False,
                "reason": "No recent workout data."
            }
        
        # Check if worked out consecutive days with high intensity
        consecutive_high = all(i.intensity_score > self.INTENSITY_THRESHOLDS['high'] for i in recent)
        
        avg_recent = sum(i.intensity_score for i in recent) / len(recent)
        
        should_rest = False
        reason = ""
        
        if len(recent) >= 3 and consecutive_high:
            should_rest = True
            reason = "3+ consecutive high-intensity days. Rest recommended for recovery."
        elif avg_recent > self.INTENSITY_THRESHOLDS['very_high']:
            should_rest = True
            reason = "Very high recent intensity. A rest day will optimize gains."
        
        return {
            "should_rest": should_rest,
            "reason": reason,
            "avg_intensity": round(avg_recent, 2),
            "consecutive_days": len(recent)
        }