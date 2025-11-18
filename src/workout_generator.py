from typing import List, Dict
from src.user_profile import UserProfile
from src.rag_engine import RAGEngine
from src.llm_handler import LLMHandler
import random
from datetime import datetime

class WorkoutGenerator:
    
    def __init__(self, rag_engine: RAGEngine, llm_handler: LLMHandler):
        self.rag = rag_engine
        self.llm = llm_handler
        
    def generate_workout_plan(self, user_profile: UserProfile) -> Dict:
        
        muscle_split = self._get_muscle_split(user_profile)
        
        weekly_plan = []
        for day_num, muscle_groups in enumerate(muscle_split, 1):
            workout = self._generate_single_workout(
                day_number=day_num,
                muscle_groups=muscle_groups,
                user_profile=user_profile
            )
            weekly_plan.append(workout)
        
        return {
            "user_profile": user_profile.to_dict(),
            "weekly_plan": weekly_plan,
            "total_days": len(weekly_plan),
            "generated_at": datetime.now().isoformat()
        }
    
    def _get_muscle_split(self, user_profile: UserProfile) -> List[List[str]]:
        
        if user_profile.days_per_week == 3:
            return [
                ["chest", "arms"],
                ["back", "shoulders"],
                ["legs", "core"]
            ]
        elif user_profile.days_per_week == 4:
            return [
                ["chest", "arms"],
                ["back"],
                ["legs", "core"],
                ["shoulders", "cardio"]
            ]
        elif user_profile.days_per_week == 5:
            return [
                ["chest"],
                ["back"],
                ["legs"],
                ["shoulders", "arms"],
                ["core", "cardio"]
            ]
        else:
            return [
                ["chest", "arms"],
                ["back", "shoulders"],
                ["legs", "core"]
            ]
    
    def _generate_single_workout(self, 
                                  day_number: int, 
                                  muscle_groups: List[str],
                                  user_profile: UserProfile) -> Dict:
        
        query = f"{', '.join(muscle_groups)} exercises for {user_profile.experience_level} level"
        
        exercises = self.rag.search_exercises(
            query=query,
            gym_id=user_profile.gym_id,
            muscle_groups=muscle_groups,
            n_results=20
        )
        
        num_exercises = self._get_num_exercises(user_profile.experience_level, muscle_groups)
        selected_exercises = self._select_exercises(exercises, num_exercises, user_profile)
        
        workout = {
            "day": day_number,
            "muscle_groups": muscle_groups,
            "exercises": [],
            "estimated_duration": 0,
            "estimated_calories": 0
        }
        
        total_duration = 0
        total_calories = 0
        
        for exercise in selected_exercises:
            sets, reps = self._get_sets_reps(exercise, user_profile)
            
            ex_duration = sets * 2
            ex_calories = exercise.get('calories_per_set', 10) * sets
            
            workout["exercises"].append({
                "id": exercise['id'],
                "name": exercise['name'],
                "muscle_group": exercise['muscle_group'],
                "sets": sets,
                "reps": reps,
                "instructions": exercise['instructions'],
                "video_url": exercise['video_url'],
                "gif_url": exercise.get('gif_url', ''),
                "equipment": exercise['equipment'],
                "difficulty": exercise['difficulty'],
                "alternatives": exercise.get('alternatives', [])
            })
            
            total_duration += ex_duration
            total_calories += ex_calories
        
        workout["estimated_duration"] = total_duration + 10
        workout["estimated_calories"] = total_calories
        
        return workout
    
    def _get_num_exercises(self, experience_level: str, muscle_groups: List[str]) -> int:
        base_count = 4
        
        if experience_level == "beginner":
            base_count = 4
        elif experience_level == "intermediate":
            base_count = 5
        else:
            base_count = 6
        
        if "cardio" in muscle_groups:
            base_count = max(2, base_count - 2)
        
        return base_count
    
    def _select_exercises(self, exercises: List[Dict], num_needed: int, user_profile: UserProfile) -> List[Dict]:
        
        by_muscle = {}
        for ex in exercises:
            mg = ex['muscle_group']
            if mg not in by_muscle:
                by_muscle[mg] = []
            by_muscle[mg].append(ex)
        
        selected = []
        
        for muscle_group in by_muscle:
            available = by_muscle[muscle_group]
            
            suitable = [ex for ex in available if self._is_suitable_difficulty(ex, user_profile)]
            
            if suitable:
                num_from_group = min(2, len(suitable))
                selected.extend(random.sample(suitable, num_from_group))
        
        while len(selected) < num_needed and len(exercises) > len(selected):
            remaining = [ex for ex in exercises if ex not in selected]
            if remaining:
                selected.append(random.choice(remaining))
            else:
                break
        
        return selected[:num_needed]
    
    def _is_suitable_difficulty(self, exercise: Dict, user_profile: UserProfile) -> bool:
        difficulty_levels = ["beginner", "intermediate", "advanced"]
        user_level_idx = difficulty_levels.index(user_profile.experience_level)
        exercise_level_idx = difficulty_levels.index(exercise['difficulty'])
        
        return exercise_level_idx <= user_level_idx
    
    def _get_sets_reps(self, exercise: Dict, user_profile: UserProfile) -> tuple:
        
        if user_profile.fitness_goal == "muscle_gain":
            sets = random.randint(3, 4)
            reps = random.randint(8, 12)
        elif user_profile.fitness_goal == "strength":
            sets = random.randint(4, 5)
            reps = random.randint(5, 8)
        elif user_profile.fitness_goal == "weight_loss":
            sets = random.randint(3, 4)
            reps = random.randint(12, 15)
        else:
            sets = random.randint(3, 4)
            reps = random.randint(10, 12)
        
        if exercise['muscle_group'] == "cardio":
            return (1, random.randint(20, 30))
        
        if "Plank" in exercise['name'] or "plank" in exercise['name'].lower():
            return (3, random.randint(30, 60))
        
        return (sets, reps)
    
    def get_daily_workout(self, workout_plan: Dict, day_number: int) -> Dict:
        if day_number <= len(workout_plan['weekly_plan']):
            return workout_plan['weekly_plan'][day_number - 1]
        return None
    
    def swap_exercise(self, exercise_id: str, gym_id: str) -> Dict:
        alternatives = self.rag.get_exercise_alternatives(exercise_id, gym_id)
        if alternatives:
            return random.choice(alternatives)
        return None