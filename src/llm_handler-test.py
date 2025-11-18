import ollama
from typing import List, Dict, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama
from config import OLLAMA_MODEL, OLLAMA_BASE_URL


class LLMHandler:
    
    def __init__(self, model: str = OLLAMA_MODEL):
        self.model = model
        self.llm = Ollama(model=model, base_url=OLLAMA_BASE_URL)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.conversation_chain = ConversationChain(llm=self.llm, memory=self.memory, verbose=False)
    
    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response from LLM using basic prompt"""
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            return self.llm(full_prompt)
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat_with_context(self, user_message: str, system_context: str = None) -> str:
        """Chat with conversation history"""
        try:
            if system_context:
                prompt = f"System Context: {system_context}\n\nUser: {user_message}\n\nAssistant:"
                response = self.llm(prompt)
            else:
                response = self.conversation_chain.predict(input=user_message)
            return response
        except Exception as e:
            return f"Error in chat: {str(e)}"
    
    def generate_structured_workout(self, profile_summary: str, exercises_context: str) -> str:
        """Generate workout plan using structured prompt"""
        template = """You are an expert fitness trainer AI. Generate a personalized workout plan.

                    User Profile:
                    {profile_summary}
                    Available Exercises:
                    {exercises_context}

                    Generate a clear, actionable workout plan with:
                    1. Warm-up recommendations (2-3 minutes)
                    2. Main exercises with sets and reps
                    3. Cool-down/stretching (2-3 minutes)
                    4. Motivational tip
                    Be encouraging and specific. Format clearly."""
        
        prompt = PromptTemplate(input_variables=["profile_summary", "exercises_context"], template=template)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            return chain.run(profile_summary=profile_summary, exercises_context=exercises_context)
        except Exception as e:
            return f"Error generating workout: {str(e)}"
    
    def generate_exercise_explanation(self, exercise_name: str, exercise_details: str) -> str:
        """Explain exercise form and technique"""
        template = """You are a knowledgeable fitness trainer. Explain this exercise clearly.

                    Exercise: {exercise_name}
                    Details: {exercise_details}

                    Provide:
                    1. Brief overview (1-2 sentences)
                    2. Key form points (3-4 bullet points)
                    3. Common mistakes to avoid (2-3 points)
                    4. One pro tip

                    Be concise, friendly, and encouraging."""
        
        prompt = PromptTemplate(input_variables=["exercise_name", "exercise_details"], template=template)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            return chain.run(exercise_name=exercise_name, exercise_details=exercise_details)
        except Exception as e:
            return f"Error explaining exercise: {str(e)}"
    
    def recommend_supplements(self, fitness_goal: str, available_supplements: str) -> str:
        """Recommend supplements based on fitness goals"""
        template = """You are a knowledgeable fitness nutrition advisor.

                    User's Fitness Goal: {fitness_goal}

                    Available Supplements:
                    {available_supplements}

                    Provide:
                    1. Top 2-3 recommended supplements with brief explanation why
                    2. How each helps with their specific goal
                    3. Usage tips (when to take, how much)

                    Be helpful but not pushy. Focus on genuine benefits."""
        
        prompt = PromptTemplate(input_variables=["fitness_goal", "available_supplements"], template=template)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            return chain.run(fitness_goal=fitness_goal, available_supplements=available_supplements)
        except Exception as e:
            return f"Error recommending supplements: {str(e)}"
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
