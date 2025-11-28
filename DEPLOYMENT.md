# FitFlow AI - Deployment Guide

## 🚀 Deploying to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- OpenAI API key (get one at [platform.openai.com](https://platform.openai.com))

### Step 1: Push Code to GitHub
Your code is already on the `Iteration_01` branch. Make sure it's pushed:
```bash
git push origin Iteration_01
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `anirudhksharma/fitflow-ai`
4. Select branch: `Iteration_01`
5. Main file path: `app.py`

### Step 3: Configure Environment Variables

In Streamlit Cloud, go to **App settings** → **Secrets** and add:

```toml
LLM_PROVIDER = "openai"
OPENAI_API_KEY = "your-openai-api-key-here"
OPENAI_MODEL = "gpt-3.5-turbo"
```

**Important:** Replace `your-openai-api-key-here` with your actual OpenAI API key.

### Step 4: Deploy!

Click "Deploy" and wait for the app to build and start.

---

## 🏠 Running Locally

### With Ollama (Default)

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the model:
   ```bash
   ollama pull llama3.1
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

### With OpenAI (Local Testing)

1. Create a `.env` file:
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your-api-key-here
   OPENAI_MODEL=gpt-3.5-turbo
   ```

2. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `ollama` | LLM provider: `ollama` or `openai` |
| `OLLAMA_MODEL` | `llama3.1` | Ollama model name |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OPENAI_API_KEY` | - | OpenAI API key (required for OpenAI) |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | OpenAI model name |

---

## 💰 Cost Considerations

### Ollama (Free)
- Runs locally on your machine
- No API costs
- Requires local GPU/CPU resources

### OpenAI (Paid)
- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **GPT-4**: ~$0.03 per 1K tokens
- Typical conversation: 500-2000 tokens
- Estimated cost: $0.001 - $0.06 per conversation

**Recommendation for deployment:** Start with `gpt-3.5-turbo` for cost-effectiveness.

---

## 🐛 Troubleshooting

### Error: "ConnectionError" on Streamlit Cloud
- **Cause:** App is trying to connect to local Ollama
- **Fix:** Set `LLM_PROVIDER=openai` in Streamlit Cloud secrets

### Error: "OPENAI_API_KEY is required"
- **Cause:** Missing API key
- **Fix:** Add `OPENAI_API_KEY` to Streamlit Cloud secrets

### Local Ollama not working
- **Check:** Is Ollama running? `ollama list`
- **Check:** Is the model pulled? `ollama pull llama3.1`
- **Check:** Is the port correct? Default is `11434`

---

## 📝 Notes

- The app automatically detects the LLM provider from environment variables
- All features work with both Ollama and OpenAI
- Switching providers requires no code changes, only environment variable updates
