import json
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
from config import CHROMA_PERSIST_DIR, COLLECTION_NAME, EXERCISES_FILE, GYMS_FILE, SUPPLEMENTS_FILE

class RAGEngine:
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.collection = None
        self.exercises_data = self._load_exercises()
        self.gyms_data = self._load_gyms()
        self.supplements_data = self._load_supplements()
        
    def _load_exercises(self) -> List[Dict]:
        with open(EXERCISES_FILE, 'r') as f:
            data = json.load(f)
        return data['exercises']
    
    def _load_gyms(self) -> List[Dict]:
        with open(GYMS_FILE, 'r') as f:
            data = json.load(f)
        return data['gyms']
    
    def _load_supplements(self) -> List[Dict]:
        with open(SUPPLEMENTS_FILE, 'r') as f:
            data = json.load(f)
        return data['supplements']
    
    def initialize_database(self):
        try:
            self.collection = self.client.get_collection(name=COLLECTION_NAME)
            print("Loaded existing exercise database")
        except:
            self.collection = self.client.create_collection(name=COLLECTION_NAME)
            self._populate_database()
            print("Created and populated new exercise database")
    
    def _populate_database(self):
        documents = []
        metadatas = []
        ids = []
        
        for exercise in self.exercises_data:
            doc_text = f"""
            Exercise: {exercise['name']}
            Muscle Group: {exercise['muscle_group']}
            Equipment: {', '.join(exercise['equipment'])}
            Difficulty: {exercise['difficulty']}
            Instructions: {exercise['instructions']}
            Target: {exercise['muscle_group']} training
            Level: suitable for {exercise['difficulty']} level athletes
            """
            
            documents.append(doc_text)
            metadatas.append({
                "id": exercise['id'],
                "name": exercise['name'],
                "muscle_group": exercise['muscle_group'],
                "difficulty": exercise['difficulty'],
                "equipment": json.dumps(exercise['equipment']),
                "calories": exercise.get('calories_per_set', 10)
            })
            ids.append(exercise['id'])
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def get_gym_equipment(self, gym_id: str) -> List[str]:
        for gym in self.gyms_data:
            if gym['gym_id'] == gym_id:
                return gym['equipment']
        return []
    
    def search_exercises(self, 
                        query: str, 
                        gym_id: str,
                        muscle_groups: List[str] = None,
                        difficulty: str = None,
                        n_results: int = 15) -> List[Dict]:
        
        available_equipment = self.get_gym_equipment(gym_id)
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results * 2
        )
        
        exercises = []
        for idx, ex_id in enumerate(results['ids'][0]):
            exercise = next((ex for ex in self.exercises_data if ex['id'] == ex_id), None)
            
            if not exercise:
                continue
            
            if not all(eq in available_equipment for eq in exercise['equipment']):
                continue
            
            if muscle_groups and exercise['muscle_group'] not in muscle_groups:
                continue
            
            if difficulty and exercise['difficulty'] != difficulty:
                continue
            
            exercises.append(exercise)
            
            if len(exercises) >= n_results:
                break
        
        return exercises
    
    def get_exercise_by_id(self, exercise_id: str) -> Dict:
        return next((ex for ex in self.exercises_data if ex['id'] == exercise_id), None)
    
    def get_exercise_alternatives(self, exercise_id: str, gym_id: str) -> List[Dict]:
        exercise = self.get_exercise_by_id(exercise_id)
        if not exercise or 'alternatives' not in exercise:
            return []
        
        available_equipment = self.get_gym_equipment(gym_id)
        alternatives = []
        
        for alt_id in exercise['alternatives']:
            alt_ex = self.get_exercise_by_id(alt_id)
            if alt_ex and all(eq in available_equipment for eq in alt_ex['equipment']):
                alternatives.append(alt_ex)
        
        return alternatives
    
    def get_supplements_for_goal(self, fitness_goal: str) -> List[Dict]:
        matching_supplements = []
        for supp in self.supplements_data:
            if fitness_goal in supp['recommended_for']:
                matching_supplements.append(supp)
        return matching_supplements
    
    def search_supplements(self, query: str, fitness_goal: str = None) -> List[Dict]:
        query_lower = query.lower()
        results = []
        
        for supp in self.supplements_data:
            name_match = query_lower in supp['name'].lower()
            desc_match = query_lower in supp['description'].lower()
            goal_match = fitness_goal in supp['recommended_for'] if fitness_goal else True
            
            if (name_match or desc_match) and goal_match:
                results.append(supp)
        
        return results