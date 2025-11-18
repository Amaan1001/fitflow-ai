"""
Setup script for FitFlow AI
Run this after cloning the repository
"""
import os
from pathlib import Path

def setup_project():
    """Create necessary directories and files"""
    base_dir = Path(__file__).parent
    
    # Create directories
    directories = [
        base_dir / "chroma_db",
        base_dir / "storage",
        base_dir / "data"
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"Directory created: {directory}")
    
    # Create empty storage files if they don't exist
    storage_files = [
        base_dir / "storage" / "user_profiles.json",
        base_dir / "storage" / "workout_logs.json"
    ]
    
    for file_path in storage_files:
        if not file_path.exists():
            file_path.write_text("[]")
            print(f"File created: {file_path}")
        else:
            print(f"File already exists: {file_path}")
    
    print("\nSetup complete. Now run: streamlit run app.py")

if __name__ == "__main__":
    setup_project()