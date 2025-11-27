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

    def answer_with_exercise_context(self, user_question: str, context: str) -> str:
        prompt = f"""
You are FitFlow AI, an expert fitness concierge and certified personal trainer.

You have been provided with specific CONTEXT from the database.

**INTERNAL STEPS (DO NOT OUTPUT THESE):**
1. Analyze if the [CONTEXT] below is directly relevant to the [User Question].
2. If the context is irrelevant (e.g., user asks about specific physiology but context is about a different exercise), DISCARD the context silently.
3. If the context is relevant, use it.

**OUTPUT RULES:**
- **Provide the DIRECT ANSWER only.**
- **DO NOT** explain your reasoning process (e.g., never say "The context is irrelevant so I will use general knowledge").
- **DO NOT** mention the context unless you are actively using it to answer the question.
- If you fall back to general knowledge, just give the fitness advice as if you knew it all along.

**User Question:** {user_question}

**Retrieved Context:**
{context}

**Answer:**
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
