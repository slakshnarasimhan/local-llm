# 🚀 START HERE - RAG Chatbot Demo

## Welcome!

This project demonstrates how to build a **Retrieval Augmented Generation (RAG)** chatbot that works with both **cloud-based LLMs** (OpenAI) and **locally-run LLMs** (Ollama).

**The Key Insight**: Switching between cloud and local requires changing just ONE function call. Everything else stays the same!

---

## ⚡ Quick Start (Choose Your Path)

### 🎯 Path 1: I Want to See It Working NOW! (5 minutes)

```bash
# 1. Run automated setup
./setup.sh

# 2. Run the demo
python demo.py
```

That's it! The demo will:
- Create sample documents
- Build a vector database
- Answer questions using Ollama (local LLM)

### 🎓 Path 2: I Want to Learn & Explore (15 minutes)

```bash
# 1. Setup
./setup.sh

# 2. Read the architecture
cat ARCHITECTURE.md

# 3. Try the interactive chatbot
python chatbot_cli.py

# Commands to try:
# > info          (see current config)
# > examples      (example questions)
# > ask           (ask a question)
# > switch        (toggle cloud/local)
# > help          (all commands)
```

### 🎤 Path 3: I'm Giving a Presentation (30 minutes)

```bash
# 1. Setup and test
./setup.sh
python demo.py compare  # Test both cloud and local

# 2. Read the script
cat PRESENTATION_NOTES.md

# 3. Practice the demo
python chatbot_cli.py
# Practice: ask -> switch -> ask same question
```

---

## 📚 Documentation Guide

**Choose what to read based on your needs:**

| Document | When to Read | Reading Time |
|----------|--------------|--------------|
| **README.md** | Comprehensive overview | 15 min |
| **QUICKSTART.md** | Just want to get running | 3 min |
| **ARCHITECTURE.md** | Want technical details | 10 min |
| **PRESENTATION_NOTES.md** | Giving a demo/talk | 20 min |
| **PROJECT_SUMMARY.md** | High-level understanding | 10 min |
| **FILES_OVERVIEW.txt** | Reference guide | 5 min |

---

## 🎯 What You'll Build

A chatbot that:

✅ Loads and chunks documents  
✅ Creates semantic embeddings  
✅ Stores vectors in ChromaDB  
✅ Retrieves relevant context  
✅ Generates grounded answers  
✅ **Switches between cloud and local LLMs effortlessly**

---

## 🔑 Key Files to Understand

### Core Application (Read in this order)

1. **document_processor.py** - How documents become chunks
2. **vector_store.py** - How chunks become searchable vectors
3. **rag_chatbot.py** - **THE MAGIC** - Cloud vs Local is here!
4. **chatbot_cli.py** - The user interface

### Supporting Files

- **demo.py** - Quick demonstration script
- **requirements.txt** - All dependencies
- **config.env.example** - Configuration options
- **setup.sh** - Automated installation

---

## 💡 The "Aha!" Moment

Open `rag_chatbot.py` and look at these two methods:

```python
def query_openai(self, prompt: str) -> str:
    """Cloud inference"""
    response = openai.chat.completions.create(...)
    return response.choices[0].message.content

def query_ollama(self, prompt: str) -> str:
    """Local inference"""
    response = self.ollama_client.chat(...)
    return response['message']['content']
```

**That's the ONLY difference!** Same RAG pipeline, different inference engine.

---

## 🎮 Try These Examples

### Example 1: Basic Question
```
> ask
Your question: How do I install Ollama?
```

### Example 2: Compare Cloud vs Local
```
> info                              # Check current provider
> ask: What is RAG?                 # Ask with current provider
> switch                            # Switch to other provider
> ask: What is RAG?                 # Ask same question
# Compare the answers!
```

### Example 3: Explore Documents
```
> ask: What models are available in Ollama?
> ask: When should I use local vs cloud LLMs?
> ask: How does fine-tuning work?
```

---

## 🛠️ Prerequisites

**Required:**
- Python 3.8+
- 8GB RAM (minimum)

**For Cloud Mode:**
- OpenAI API key (get at https://platform.openai.com)

**For Local Mode:**
- Ollama installed (https://ollama.com)
- A model downloaded: `ollama pull llama3`

---

## 🚨 Common First-Time Issues

### Issue: "Ollama not available"
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download a model
ollama pull llama3

# Test it works
ollama run llama3 "Hello"
```

### Issue: "OpenAI API key not set"
```bash
# Create .env file
cp config.env.example .env

# Edit .env and add your key
OPENAI_API_KEY=sk-your-actual-key-here
```

### Issue: "Module not found"
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 🎯 Success Checklist

After setup, you should be able to:

- [ ] Run `python demo.py` successfully
- [ ] See sample documents created in `sample_docs/`
- [ ] Ask questions and get answers
- [ ] Switch between providers (if both configured)
- [ ] Understand the code structure

---

## 🎓 Learning Path

### Beginner (1-2 hours)
1. Run `demo.py` and observe
2. Read `README.md`
3. Try `chatbot_cli.py` interactively
4. Look at sample documents
5. Experiment with different questions

### Intermediate (3-4 hours)
1. Read through all `.py` files
2. Study `ARCHITECTURE.md`
3. Modify sample documents
4. Adjust chunk sizes
5. Try different models

### Advanced (1-2 days)
1. Add your own document types
2. Implement conversation history
3. Build a web UI
4. Add evaluation metrics
5. Deploy to production

---

## 🎤 For Presenters

**Your presentation flow:**

1. **Show** the PDF (context setting)
2. **Explain** RAG concept (5 min)
3. **Demo** cloud version (3 min)
4. **Execute** the switch command (THE KEY MOMENT!)
5. **Show** code side-by-side (emphasize: "only this changed!")
6. **Demo** local version (3 min)
7. **Discuss** trade-offs (2 min)

See `PRESENTATION_NOTES.md` for full script!

---

## 🚀 Next Steps

After getting it running:

### Immediate (Today)
- [ ] Read `README.md` fully
- [ ] Try all CLI commands
- [ ] Ask 5 different questions
- [ ] Switch between providers

### Short Term (This Week)
- [ ] Add your own documents
- [ ] Try different models
- [ ] Adjust parameters
- [ ] Read the code

### Long Term (This Month)
- [ ] Build a web UI
- [ ] Add new features
- [ ] Fine-tune a model
- [ ] Share with colleagues

---

## 🎁 What's Included

**Application:**
- ✅ Complete RAG pipeline
- ✅ OpenAI integration
- ✅ Ollama integration
- ✅ Interactive CLI
- ✅ Demo script
- ✅ Sample documents

**Documentation:**
- ✅ 6 comprehensive guides
- ✅ Code comments
- ✅ Architecture diagrams
- ✅ Troubleshooting tips
- ✅ Presentation script

**Setup:**
- ✅ Automated installer
- ✅ Dependencies listed
- ✅ Configuration template
- ✅ Git ignore rules

---

## 💬 Questions?

**Check these first:**
1. `README.md` - Comprehensive docs
2. `QUICKSTART.md` - Setup issues
3. `ARCHITECTURE.md` - How it works
4. `FILES_OVERVIEW.txt` - File reference

**Still stuck?** Review the original PDF presentation for context.

---

## 🌟 The Big Picture

This project proves that:

1. **Local LLMs are viable** - Quality is good enough for many use cases
2. **Migration is easy** - One function call changes
3. **RAG is powerful** - Grounds answers in real documents
4. **Architecture matters** - Good design enables flexibility
5. **It's accessible** - Runs on a laptop!

---

## 🎯 Your First 5 Minutes

```bash
cd /home/narasimhan/workarea/local-llm

# 1. Setup (automated)
./setup.sh

# 2. Run demo
python demo.py

# 3. Try interactive mode
python chatbot_cli.py

# 4. Ask a question
> ask: How do I install Ollama?

# 5. Celebrate! 🎉 You're running AI locally!
```

---

**Now go forth and build amazing things!** 🚀

Remember: The power of local AI is in your hands. Use it wisely!
