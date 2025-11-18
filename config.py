import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
EXERCISES_FILE = DATA_DIR / "exercises.json"
GYMS_FILE = DATA_DIR / "gyms.json"
SUPPLEMENTS_FILE = DATA_DIR / "supplements.json"
STORAGE_DIR = BASE_DIR / "storage"
USER_PROFILES_FILE = STORAGE_DIR / "user_profiles.json"
WORKOUT_LOGS_FILE = STORAGE_DIR / "workout_logs.json"

STORAGE_DIR.mkdir(exist_ok=True)

# Ollama settings
OLLAMA_MODEL = "llama3.1"
OLLAMA_BASE_URL = "http://localhost:11434"

# ChromaDB settings
CHROMA_PERSIST_DIR = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "gym_exercises"

# App settings
APP_TITLE = "FitFlow AI - Your Personal Gym Concierge"
APP_ICON = "🏋️"

# Session state keys
SESSION_USER_PROFILE = "user_profile"
SESSION_CHAT_HISTORY = "chat_history"
SESSION_WORKOUT_PLAN = "workout_plan"
SESSION_CURRENT_DAY = "current_day"
SESSION_WORKOUT_LOGS = "workout_logs"

# Motivational quotes
MOTIVATIONAL_QUOTES = [
    "The only bad workout is the one that didn't happen!",
    "Your body can do it, it's your mind you need to convince.",
    "Success starts with self-discipline.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "Don't limit your challenges. Challenge your limits.",
    "The only way to finish is to start.",
    "Believe in yourself and all that you are.",
    "Your future is created by what you do today, not tomorrow.",
]