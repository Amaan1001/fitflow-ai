from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from datetime import datetime
import json
from pathlib import Path

@dataclass
class UserProfile:
    """User profile with fitness goals and preferences"""
    user_id: str = ""
    name: str = ""
    fitness_goal: str = ""  # "muscle_gain", "weight_loss", "general_fitness", "strength"
    experience_level: str = ""  # "beginner", "intermediate", "advanced"
    days_per_week: int = 3
    session_duration: int = 60  # minutes
    injuries_limitations: str = ""
    preferred_muscle_groups: List[str] = field(default_factory=list)
    gym_id: str = "demo_gym_01"
    created_at: datetime = field(default_factory=datetime.now)
    total_workouts: int = 0
    current_streak: int = 0
    last_workout_date: Optional[str] = None
    
    def to_dict(self):
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict):
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)
    
    def get_profile_summary(self) -> str:
        """Generate text summary of user profile"""
        return f"""
            User Profile:
            - Name: {self.name}
            - Goal: {self.fitness_goal.replace('_', ' ').title()}
            - Experience: {self.experience_level.title()}
            - Training Frequency: {self.days_per_week} days per week
            - Session Duration: {self.session_duration} minutes
            - Limitations: {self.injuries_limitations if self.injuries_limitations else 'None'}
            - Total Workouts: {self.total_workouts}
            - Current Streak: {self.current_streak} days
        """
    
    def save_to_file(self, filepath: Path):
        """Save profile to JSON file"""
        profiles = []
        if filepath.exists():
            with open(filepath, 'r') as f:
                profiles = json.load(f)
        
        # Update or add profile
        profile_data = self.to_dict()
        existing_idx = next((i for i, p in enumerate(profiles) if p['user_id'] == self.user_id), None)
        
        if existing_idx is not None:
            profiles[existing_idx] = profile_data
        else:
            profiles.append(profile_data)
        
        with open(filepath, 'w') as f:
            json.dump(profiles, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: Path, user_id: str):
        """Load profile from JSON file"""
        if not filepath.exists():
            return None
        
        with open(filepath, 'r') as f:
            profiles = json.load(f)
        
        profile_data = next((p for p in profiles if p['user_id'] == user_id), None)
        if profile_data:
            return cls.from_dict(profile_data)
        return None


@dataclass
class WorkoutLog:
    """Individual workout log entry"""
    log_id: str = ""
    user_id: str = ""
    date: datetime = field(default_factory=datetime.now)
    day_number: int = 0
    exercises_completed: List[str] = field(default_factory=list)
    total_exercises: int = 0
    duration_minutes: int = 0
    calories_burned: int = 0
    notes: str = ""
    
    def to_dict(self):
        data = asdict(self)
        data['date'] = self.date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict):
        if 'date' in data and isinstance(data['date'], str):
            data['date'] = datetime.fromisoformat(data['date'])
        return cls(**data)
    
    def save_to_file(self, filepath: Path):
        """Save log to JSON file"""
        logs = []
        if filepath.exists():
            with open(filepath, 'r') as f:
                logs = json.load(f)
        
        logs.append(self.to_dict())
        
        with open(filepath, 'w') as f:
            json.dump(logs, f, indent=2)
    
    @classmethod
    def load_user_logs(cls, filepath: Path, user_id: str) -> List['WorkoutLog']:
        """Load all logs for a user"""
        if not filepath.exists():
            return []
        
        with open(filepath, 'r') as f:
            all_logs = json.load(f)
        
        user_logs = [cls.from_dict(log) for log in all_logs if log['user_id'] == user_id]
        return sorted(user_logs, key=lambda x: x.date, reverse=True)