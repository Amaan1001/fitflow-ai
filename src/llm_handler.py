from typing import List, Dict, Optional
from langchain_community.chat_models import ChatOllama
from config import OLLAMA_MODEL, OLLAMA_BASE_URL


class LLMHandler:
    def __init__(self, model: str = OLLAMA_MODEL):
        self.model = model
        # Uses the new official LCEL-compatible Ollama wrapper
        self.llm = ChatOllama(model=model, base_url=OLLAMA_BASE_URL)
        # We manage memory ourselves now (ConversationBufferMemory no longer exists)
        self.chat_history: List[Dict[str, str]] = []

    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """Low-level LLM call using the new LangChain Chat API."""
        response = self.llm.invoke(messages)
        return response.content

    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Single-turn generation, no chat history used."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        answer = self._call_llm(messages)
        return answer

    def chat_with_context(self, user_message: str, system_context: Optional[str] = None) -> str:
        """Multi-turn chat with full preserved history (LCEL-compatible)."""

        messages = []

        # Optional system-level context
        if system_context:
            messages.append({"role": "system", "content": system_context})

        # Replay old chat messages (like ConversationBufferMemory used to)
        for msg in self.chat_history:
            messages.append(msg)

        # Add the new message
        messages.append({"role": "user", "content": user_message})

        # Get model response
        answer = self._call_llm(messages)

        # Save memory like ConversationBufferMemory did
        self.chat_history.append({"role": "user", "content": user_message})
        self.chat_history.append({"role": "assistant", "content": answer})

        return answer

    def generate_structured_workout(self, profile_summary: str, exercises_context: str) -> str:
        prompt = f"""
            You are an expert fitness trainer AI. Generate a personalized workout plan.

            User Profile:
            {profile_summary}

            Available Exercises:
            {exercises_context}

            Generate a clear workout plan with:
            1. Warm-up (2–3 mins)
            2. Main exercises with sets & reps
            3. Cool-down (2–3 mins)
            4. Motivational tip
        """
        return self.generate_response(prompt)

    def generate_exercise_explanation(self, exercise_name: str, exercise_details: str) -> str:
        prompt = f"""
            You are a knowledgeable fitness trainer. Explain this exercise clearly.

            Exercise: {exercise_name}
            Details: {exercise_details}

            Include:
            - 1–2 sentence overview
            - 3–4 key form points
            - 2–3 common mistakes
            - One pro tip
        """
        return self.generate_response(prompt)

    def recommend_supplements(self, fitness_goal: str, available_supplements: str) -> str:
        prompt = f"""
            You are a fitness nutrition expert.

            Goal: {fitness_goal}

            Available Supplements:
            {available_supplements}

            List:
            - Top 2–3 supplements
            - Why each helps
            - When/how to take them
        """
        return self.generate_response(prompt)

    def clear_memory(self):
        """Clears chat history, just like ConversationBufferMemory.clear()"""
        self.chat_history = []
