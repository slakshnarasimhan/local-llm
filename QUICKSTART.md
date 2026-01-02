# QUICKSTART GUIDE

## 🚀 Get Running in 3 Minutes

### Option 1: Automated Setup (Recommended)
```bash
cd /home/narasimhan/workarea/local-llm
./setup.sh
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp config.env.example .env
# Edit .env and set your OpenAI API key (optional)

# 3. Install Ollama (for local LLM)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
```

## 🎮 Running the Demo

### Interactive Chat
```bash
python chatbot_cli.py
```
Commands: `ask`, `switch`, `examples`, `help`, `quit`

### Quick Demo
```bash
python demo.py           # Local LLM demo
python demo.py compare   # Compare cloud vs local
```

### Test Individual Components
```bash
python document_processor.py  # Test document chunking
python vector_store.py         # Test vector search
python rag_chatbot.py          # Test RAG chatbot
```

## 🔑 Configuration Options

The application supports multiple configuration sources (in priority order):

1. **Streamlit secrets** (`~/.streamlit/secrets.toml`) - Highest priority
2. **Environment variables** (`.env` file)
3. **Defaults**

### Quick Config Check

```bash
# See which configuration source is being used
python config.py
```

### If you have Streamlit secrets

Your existing `~/.streamlit/secrets.toml` with `OPENAI_API_KEY` will be used automatically! No additional setup needed.

### If you don't have Streamlit secrets

```bash
# Create .env file
cp config.env.example .env

# Edit and add your OpenAI API key
nano .env  # or your favorite editor
```

For detailed configuration options, see `CONFIGURATION.md`.

## 💡 Example Questions to Ask

1. How do I install Ollama?
2. What is RAG and how does it work?
3. What are the benefits of running LLMs locally?
4. When should I choose cloud vs local LLMs?
5. What models are available in Ollama?
6. How does fine-tuning work with local models?

## 🎯 Key Demo Points

1. **Same Code, Different LLM**: Show how RAG pipeline is identical
2. **Switch Live**: Use `switch` command to toggle providers
3. **Compare Answers**: Ask same question to both cloud and local
4. **Performance**: Note response time differences
5. **Cost**: Highlight that local = free after setup

## 🔧 Troubleshooting

### Ollama Issues
```bash
# Check if running
ollama list

# Test manually
ollama run llama3

# Pull model if missing
ollama pull llama3
```

### OpenAI Issues
- Ensure API key is in `.env` file
- Check key format: starts with `sk-`
- Verify account has credits

### Python Issues
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear vector database
rm -rf chroma_db/ chroma_db_demo/
```

## 📊 Performance Tips

- **Faster Local Inference**: Use smaller models (`phi3`, `mistral`)
- **Better Quality**: Use larger models (`llama3:70b`) or OpenAI
- **Balance**: `llama3` (8B) is a good compromise
- **GPU**: Ollama automatically uses GPU if available

## 🎓 Learning Path

1. Run `demo.py` to see basic RAG in action
2. Try `chatbot_cli.py` for interactive experience
3. Read through `rag_chatbot.py` to understand the code
4. Experiment with different models and settings
5. Add your own documents to `sample_docs/`

## 🌟 Presentation Flow

1. **Intro**: Show the PDF presentation
2. **Demo Setup**: Run `setup.sh` (pre-run before presentation)
3. **Cloud Demo**: Start with OpenAI, ask a question
4. **The Switch**: Type `switch` - explain what's changing
5. **Local Demo**: Ask the same question with Ollama
6. **Key Insight**: Show code side-by-side - only inference changed
7. **Live Comparison**: Ask new questions to both
8. **Wrap-up**: Discuss trade-offs and use cases

