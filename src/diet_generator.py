"""
Diet Plan Generator for FitFlow AI
Generates personalized meal plans based on fitness goals and calorie needs
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import random
from datetime import datetime
import json


@dataclass
class NutritionProfile:
    """User's nutritional requirements"""
    calories: int
    protein: int
    carbs: int
    fats: int
    fiber: int
    
    def to_dict(self):
        return {
            "calories": self.calories,
            "protein": self.protein,
            "carbs": self.carbs,
            "fats": self.fats,
            "fiber": self.fiber
        }


class DietGenerator:
    """Generates personalized diet plans"""
    
    # Calorie multipliers based on goal
    GOAL_MULTIPLIERS = {
        'muscle_gain': 1.15,      # +15% surplus
        'weight_loss': 0.85,      # -15% deficit
        'strength': 1.10,         # +10% surplus
        'general_fitness': 1.0    # Maintenance
    }
    
    # Activity level multipliers
    ACTIVITY_MULTIPLIERS = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'very_active': 1.725,
        'extra_active': 1.9
    }
    
    # Macro ratios by goal (protein%, carbs%, fats%)
    MACRO_RATIOS = {
        'muscle_gain': (0.30, 0.45, 0.25),
        'weight_loss': (0.35, 0.40, 0.25),
        'strength': (0.30, 0.45, 0.25),
        'general_fitness': (0.25, 0.50, 0.25)
    }
    
    def __init__(self, meals_data: List[Dict]):
        self.meals_data = meals_data
    
    def calculate_bmr(self, weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        return bmr
    
    def calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure"""
        multiplier = self.ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
        return bmr * multiplier
    
    def calculate_nutrition_profile(
        self,
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: str,
        fitness_goal: str,
        activity_level: str = 'moderate'
    ) -> NutritionProfile:
        """Calculate personalized nutrition requirements"""
        
        # Calculate BMR and TDEE
        bmr = self.calculate_bmr(weight_kg, height_cm, age, gender)
        tdee = self.calculate_tdee(bmr, activity_level)
        
        # Adjust for goal
        goal_multiplier = self.GOAL_MULTIPLIERS.get(fitness_goal, 1.0)
        target_calories = int(tdee * goal_multiplier)
        
        # Calculate macros
        protein_ratio, carbs_ratio, fats_ratio = self.MACRO_RATIOS.get(
            fitness_goal, 
            (0.25, 0.50, 0.25)
        )
        
        protein_g = int((target_calories * protein_ratio) / 4)  # 4 cal/g
        carbs_g = int((target_calories * carbs_ratio) / 4)      # 4 cal/g
        fats_g = int((target_calories * fats_ratio) / 9)        # 9 cal/g
        
        # Fiber recommendation (14g per 1000 calories)
        fiber_g = int((target_calories / 1000) * 14)
        
        return NutritionProfile(
            calories=target_calories,
            protein=protein_g,
            carbs=carbs_g,
            fats=fats_g,
            fiber=fiber_g
        )
    
    def generate_meal_plan(
        self,
        nutrition_profile: NutritionProfile,
        fitness_goal: str,
        days: int = 7,
        meals_per_day: int = 4
    ) -> Dict:
        """Generate a complete meal plan"""
        
        # Filter meals suitable for goal
        suitable_meals = [
            meal for meal in self.meals_data
            if fitness_goal in meal['suitable_for']
        ]
        
        # Distribute calories across meals
        # Breakfast: 25%, Lunch: 35%, Dinner: 30%, Snack: 10%
        meal_calorie_targets = {
            'breakfast': int(nutrition_profile.calories * 0.25),
            'lunch': int(nutrition_profile.calories * 0.35),
            'dinner': int(nutrition_profile.calories * 0.30),
            'snack': int(nutrition_profile.calories * 0.10)
        }
        
        weekly_plan = []
        
        for day in range(1, days + 1):
            daily_meals = []
            daily_totals = {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fats': 0,
                'fiber': 0
            }
            
            # Select meals for each category
            for category, target_calories in meal_calorie_targets.items():
                category_meals = [
                    m for m in suitable_meals 
                    if m['category'] == category
                ]
                
                if category_meals:
                    # Find meal closest to target calories
                    selected = min(
                        category_meals,
                        key=lambda x: abs(x['calories'] - target_calories)
                    )
                    
                    daily_meals.append(selected)
                    daily_totals['calories'] += selected['calories']
                    daily_totals['protein'] += selected['protein']
                    daily_totals['carbs'] += selected['carbs']
                    daily_totals['fats'] += selected['fats']
                    daily_totals['fiber'] += selected['fiber']
            
            weekly_plan.append({
                'day': day,
                'meals': daily_meals,
                'totals': daily_totals
            })
        
        return {
            'nutrition_profile': nutrition_profile.to_dict(),
            'weekly_plan': weekly_plan,
            'generated_at': datetime.now().isoformat()
        }
    
    def get_meal_by_id(self, meal_id: str) -> Optional[Dict]:
        """Get specific meal by ID"""
        return next((m for m in self.meals_data if m['id'] == meal_id), None)
    
    def search_meals(
        self,
        query: str = "",
        category: str = None,
        max_calories: int = None,
        min_protein: int = None,
        fitness_goal: str = None
    ) -> List[Dict]:
        """Search meals with filters"""
        
        filtered = self.meals_data
        
        if query:
            filtered = [
                m for m in filtered
                if query.lower() in m['name'].lower() or
                   query.lower() in m['description'].lower()
            ]
        
        if category:
            filtered = [m for m in filtered if m['category'] == category]
        
        if max_calories:
            filtered = [m for m in filtered if m['calories'] <= max_calories]
        
        if min_protein:
            filtered = [m for m in filtered if m['protein'] >= min_protein]
        
        if fitness_goal:
            filtered = [m for m in filtered if fitness_goal in m['suitable_for']]
        
        return filtered
    
    def generate_shopping_list(self, meal_plan: Dict) -> List[str]:
        """Generate shopping list from meal plan"""
        all_ingredients = []
        
        for day_plan in meal_plan['weekly_plan']:
            for meal in day_plan['meals']:
                all_ingredients.extend(meal['ingredients'])
        
        # Remove duplicates and sort
        unique_ingredients = sorted(set(all_ingredients))
        return unique_ingredients
    
    def swap_meal(
        self,
        current_meal_id: str,
        category: str,
        fitness_goal: str,
        target_calories: int
    ) -> Optional[Dict]:
        """Find alternative meal with similar macros"""
        
        suitable_meals = [
            m for m in self.meals_data
            if m['id'] != current_meal_id and
               m['category'] == category and
               fitness_goal in m['suitable_for']
        ]
        
        if not suitable_meals:
            return None
        
        # Find closest match by calories
        return min(
            suitable_meals,
            key=lambda x: abs(x['calories'] - target_calories)
        )