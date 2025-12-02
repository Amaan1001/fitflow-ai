"""
Gamification System for FitFlow AI
Handles achievements, streaks, levels, and user progression
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path


@dataclass
class Achievement:
    """Represents a single achievement"""
    id: str
    name: str
    description: str
    icon: str
    category: str  # workout, streak, progress, social
    requirement: int
    unlocked: bool = False
    unlocked_date: Optional[str] = None


@dataclass
class UserStats:
    """User statistics for gamification"""
    user_id: str
    level: int = 1
    xp: int = 0
    total_workouts: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    total_sets: int = 0
    total_reps: int = 0
    achievements_unlocked: int = 0
    last_workout_date: Optional[str] = None


class GamificationEngine:
    """Manages gamification features"""
    
    # XP required for each level
    XP_REQUIREMENTS = {
        1: 0, 2: 100, 3: 250, 4: 500, 5: 850,
        6: 1300, 7: 1900, 8: 2600, 9: 3500, 10: 5000
    }
    
    # XP rewards
    XP_REWARDS = {
        'workout_complete': 50,
        'exercise_complete': 5,
        'streak_day': 10,
        'achievement_unlock': 100,
        'perfect_form': 25
    }
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.achievements_file = storage_dir / "achievements.json"
        self.user_stats_file = storage_dir / "user_stats.json"
        self._initialize_achievements()
    
    def _initialize_achievements(self):
        """Initialize default achievements if file doesn't exist"""
        if not self.achievements_file.exists():
            default_achievements = [
                # Workout Achievements
                Achievement("first_workout", "First Step", "Complete your first workout", "🎯", "workout", 1),
                Achievement("iron_beginner", "Iron Beginner", "Complete 10 workouts", "🏋️", "workout", 10),
                Achievement("fitness_warrior", "Fitness Warrior", "Complete 50 workouts", "💪", "workout", 50),
                Achievement("gym_legend", "Gym Legend", "Complete 100 workouts", "👑", "workout", 100),
                
                # Streak Achievements
                Achievement("streak_3", "Getting Started", "3-day workout streak", "🔥", "streak", 3),
                Achievement("streak_7", "Week Warrior", "7-day workout streak", "⚡", "streak", 7),
                Achievement("streak_30", "Consistency King", "30-day workout streak", "👑", "streak", 30),
                Achievement("streak_100", "Unstoppable", "100-day workout streak", "🌟", "streak", 100),
                
                # Volume Achievements
                Achievement("hundred_sets", "Century Club", "Complete 100 total sets", "💯", "progress", 100),
                Achievement("thousand_reps", "Rep Master", "Complete 1000 total reps", "🔢", "progress", 1000),
                
                # Muscle Group Achievements
                Achievement("chest_champion", "Chest Champion", "Complete 20 chest exercises", "🦅", "muscle", 20),
                Achievement("back_beast", "Back Beast", "Complete 20 back exercises", "🦁", "muscle", 20),
                Achievement("leg_legend", "Leg Legend", "Complete 20 leg exercises", "🦵", "muscle", 20),
            ]
            
            self._save_achievements([asdict(a) for a in default_achievements])
    
    def get_user_stats(self, user_id: str) -> UserStats:
        """Get user statistics"""
        if not self.user_stats_file.exists():
            return UserStats(user_id=user_id)
        
        with open(self.user_stats_file, 'r') as f:
            all_stats = json.load(f)
        
        user_data = all_stats.get(user_id, {"user_id": user_id})
        return UserStats(**user_data)
    
    def save_user_stats(self, stats: UserStats):
        """Save user statistics"""
        all_stats = {}
        if self.user_stats_file.exists():
            with open(self.user_stats_file, 'r') as f:
                all_stats = json.load(f)
        
        all_stats[stats.user_id] = asdict(stats)
        
        with open(self.user_stats_file, 'w') as f:
            json.dump(all_stats, f, indent=2)
    
    def get_achievements(self, user_id: str) -> List[Achievement]:
        """Get all achievements with unlock status"""
        with open(self.achievements_file, 'r') as f:
            achievements_data = json.load(f)
        
        # Load user's unlocked achievements
        user_unlocked = self._get_user_unlocked_achievements(user_id)
        
        achievements = []
        for ach_data in achievements_data:
            ach = Achievement(**ach_data)
            if ach.id in user_unlocked:
                ach.unlocked = True
                ach.unlocked_date = user_unlocked[ach.id]
            achievements.append(ach)
        
        return achievements
    
    def _get_user_unlocked_achievements(self, user_id: str) -> Dict[str, str]:
        """Get user's unlocked achievements"""
        unlocked_file = self.storage_dir / f"unlocked_{user_id}.json"
        if not unlocked_file.exists():
            return {}
        
        with open(unlocked_file, 'r') as f:
            return json.load(f)
    
    def _save_achievements(self, achievements: List[Dict]):
        """Save achievements to file"""
        with open(self.achievements_file, 'w') as f:
            json.dump(achievements, f, indent=2)
    
    def check_and_unlock_achievements(self, user_id: str, stats: UserStats) -> List[Achievement]:
        """Check and unlock new achievements"""
        achievements = self.get_achievements(user_id)
        newly_unlocked = []
        
        for ach in achievements:
            if ach.unlocked:
                continue
            
            # Check conditions based on category
            if ach.category == "workout" and stats.total_workouts >= ach.requirement:
                ach.unlocked = True
                ach.unlocked_date = datetime.now().isoformat()
                newly_unlocked.append(ach)
            
            elif ach.category == "streak" and stats.current_streak >= ach.requirement:
                ach.unlocked = True
                ach.unlocked_date = datetime.now().isoformat()
                newly_unlocked.append(ach)
            
            elif ach.category == "progress":
                if "sets" in ach.id and stats.total_sets >= ach.requirement:
                    ach.unlocked = True
                    ach.unlocked_date = datetime.now().isoformat()
                    newly_unlocked.append(ach)
                elif "reps" in ach.id and stats.total_reps >= ach.requirement:
                    ach.unlocked = True
                    ach.unlocked_date = datetime.now().isoformat()
                    newly_unlocked.append(ach)
        
        # Save unlocked achievements
        if newly_unlocked:
            self._save_unlocked_achievements(user_id, achievements)
        
        return newly_unlocked
    
    def _save_unlocked_achievements(self, user_id: str, achievements: List[Achievement]):
        """Save unlocked achievements for user"""
        unlocked_file = self.storage_dir / f"unlocked_{user_id}.json"
        unlocked = {
            ach.id: ach.unlocked_date 
            for ach in achievements 
            if ach.unlocked and ach.unlocked_date
        }
        
        with open(unlocked_file, 'w') as f:
            json.dump(unlocked, f, indent=2)
    
    def add_xp(self, stats: UserStats, xp_amount: int) -> Dict:
        """Add XP and handle level ups"""
        stats.xp += xp_amount
        old_level = stats.level
        
        # Check for level up
        for level, required_xp in self.XP_REQUIREMENTS.items():
            if stats.xp >= required_xp:
                stats.level = level
        
        leveled_up = stats.level > old_level
        
        return {
            "leveled_up": leveled_up,
            "old_level": old_level,
            "new_level": stats.level,
            "xp_gained": xp_amount,
            "total_xp": stats.xp
        }
    
    def get_level_progress(self, stats: UserStats) -> Dict:
        """Get progress to next level"""
        current_level_xp = self.XP_REQUIREMENTS.get(stats.level, 0)
        next_level_xp = self.XP_REQUIREMENTS.get(stats.level + 1, current_level_xp)
        
        xp_in_current_level = stats.xp - current_level_xp
        xp_needed_for_next = next_level_xp - current_level_xp
        
        progress_percentage = (xp_in_current_level / xp_needed_for_next * 100) if xp_needed_for_next > 0 else 100
        
        return {
            "current_level": stats.level,
            "current_xp": stats.xp,
            "xp_in_level": xp_in_current_level,
            "xp_for_next_level": xp_needed_for_next,
            "progress_percentage": min(100, progress_percentage)
        }
    
    def update_workout_completion(self, user_id: str, exercises_completed: int, total_sets: int, total_reps: int) -> Dict:
        """Update stats when workout is completed"""
        stats = self.get_user_stats(user_id)
        
        # Update streak
        today = datetime.now().date()
        last_workout = datetime.fromisoformat(stats.last_workout_date).date() if stats.last_workout_date else None
        
        if last_workout:
            days_diff = (today - last_workout).days
            if days_diff == 1:
                stats.current_streak += 1
            elif days_diff > 1:
                stats.current_streak = 1
        else:
            stats.current_streak = 1
        
        stats.longest_streak = max(stats.longest_streak, stats.current_streak)
        stats.last_workout_date = datetime.now().isoformat()
        
        # Update workout stats
        stats.total_workouts += 1
        stats.total_sets += total_sets
        stats.total_reps += total_reps
        
        # Add XP
        xp_result = self.add_xp(stats, self.XP_REWARDS['workout_complete'])
        
        # Check achievements
        newly_unlocked = self.check_and_unlock_achievements(user_id, stats)
        
        # Bonus XP for achievements
        if newly_unlocked:
            for _ in newly_unlocked:
                self.add_xp(stats, self.XP_REWARDS['achievement_unlock'])
        
        stats.achievements_unlocked = len([a for a in self.get_achievements(user_id) if a.unlocked])
        
        # Save stats
        self.save_user_stats(stats)
        
        return {
            "stats": stats,
            "xp_result": xp_result,
            "newly_unlocked": newly_unlocked,
            "streak_milestone": stats.current_streak in [3, 7, 14, 30, 50, 100]
        }