# FitFlow AI - Personal Gym 

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

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/fitflow-ai.git
cd fitflow-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Ollama**
- Download from https://ollama.ai
- Pull the model:
```bash
ollama pull llama3.1
```

5. **Run the application**
```bash
streamlit run app.py
```

## Project Structure
```
fitflow-ai/
├── app.py                  # Main Streamlit application
├── config.py              # Configuration settings
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
└── storage/               # User data storage
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

This project is part of BIA-810 coursework.

## Acknowledgments
  1. Built with LangChain and Ollama
