# FitFlow AI - Personal Gym Concierge

AI-powered fitness companion that generates personalized workout plans, provides expert guidance, and tracks your progress using LangChain, Ollama, and RAG technology.

## Features

- 🎯 **Personalized Workout Plans** - AI-generated routines based on goals, experience, and equipment
- 💬 **24/7 AI Trainer** - Chat with AI for form checks, technique tips, and motivation
- 📊 **Progress Tracking** - Monitor workouts, streaks, and improvements
- 💊 **Supplement Recommendations** - Smart suggestions based on fitness goals
- 🔄 **Exercise Alternatives** - Swap exercises based on available equipment

## Tech Stack

- **Frontend:** Streamlit
- **LLM:** Ollama (Llama 3.1)
- **Vector DB:** ChromaDB
- **Embeddings:** Sentence Transformers
- **Framework:** LangChain

## Installation

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/fitflow-ai.git
cd fitflow-ai
```

2. **Run setup script** (creates necessary directories)
```bash
python setup.py
```

3. **Create virtual environment**
```bash
# Windows:
python -m venv venv
venv\Scripts\activate

# Mac/Linux:
python3 -m venv venv
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Install and start Ollama**
- Download from https://ollama.ai
- Pull the model:
```bash
ollama pull llama3.1
```
- Ensure Ollama is running (check http://localhost:11434)

6. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at http://localhost:8501

## First Time Setup
- The ChromaDB database will be initialized automatically on first run
- Click "Load Demo User" or create your own profile to get started

## Project Structure
```
fitflow-ai/
├── app.py                  # Main Streamlit application
├── config.py              # Configuration settings
├── setup.py               # Initial setup script
├── requirements.txt       # Python dependencies
├── data/
│   ├── exercises.json     # Exercise database
│   ├── gyms.json         # Gym equipment data
│   └── supplements.json   # Supplement catalog
├── src/
│   ├── llm_handler.py    # LLM interaction logic
│   ├── rag_engine.py     # RAG implementation
│   ├── user_profile.py   # User profile management
│   └── workout_generator.py  # Workout generation logic
├── storage/               # User data storage (created by setup)
└── chroma_db/            # Vector database (created by setup)
```

## License

This project is part of BIA-810 coursework.
