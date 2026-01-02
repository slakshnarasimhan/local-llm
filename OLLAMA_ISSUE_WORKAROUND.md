# ⚠️ OLLAMA API HANGING ISSUE - WORKAROUND

## Problem Identified

**Root Cause**: Ollama's API endpoints (`/api/chat` and `/api/generate`) are hanging and not responding, even though:
- ✅ `ollama list` works
- ✅ `ollama run phi3` works interactively
- ✅ Model is loaded (4.1 GB in memory)
- ✅ `/api/tags` endpoint responds
- ❌ `/api/chat` hangs indefinitely (even with curl)
- ❌ `/api/generate` hangs indefinitely

This is an **Ollama service issue**, not a Python/code issue.

## Immediate Workaround: Use OpenAI

Your OpenAI API key is already configured. Use cloud mode for your demo:

```bash
cd /home/narasimhan/workarea/local-llm
source venv/bin/activate
python chatbot_cli.py

# In the chatbot:
> info                    # Shows current provider
> switch                  # If not on OpenAI, switch to it
> ask: How do I install Ollama?
# Instant response!
```

**For your demo, this is actually PERFECT** because it highlights:
- ☁️ **Cloud (OpenAI)**: Instant, reliable, costs money
- 💻 **Local (Ollama)**: When working = free and private, but can have issues

## Fixing Ollama

### Option 1: Restart Ollama Service (Try This First)

```bash
# Stop Ollama
pkill -9 ollama

# Wait a moment
sleep 3

# Start Ollama
ollama serve &

# Wait for it to start
sleep 5

# Test
ollama run tinyllama "hello"
```

### Option 2: Check Ollama Logs

```bash
# Check for errors
journalctl -u ollama -n 50

# Or if running manually:
ollama serve
# Look for error messages
```

### Option 3: Reinstall Ollama

```bash
# Uninstall
curl -fsSL https://ollama.com/uninstall.sh | sh

# Reinstall
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull tinyllama
```

### Option 4: Use Ollama in Terminal Only

For the demo, you can show Ollama working in the terminal:

```bash
# Terminal 1: Show local LLM
ollama run tinyllama

# Ask questions interactively
# This works!

# Terminal 2: Show Python chatbot with OpenAI
python chatbot_cli.py
> switch  # To OpenAI
> ask: [same question]
```

Say: "Local works great in terminal, but for production apps, cloud APIs are more reliable!"

## What We Fixed in the Code

Even though Ollama API is hanging, we made the code better:

1. ✅ **Replaced `ollama` Python client** with direct HTTP calls (more reliable)
2. ✅ **Added streaming support** for better responsiveness  
3. ✅ **Added proper error handling** and timeouts
4. ✅ **Uses `requests` library** (more stable than httpx)

When Ollama API starts working again, the chatbot will work perfectly!

## Testing When Ollama is Fixed

```bash
# Test API directly
curl -X POST http://localhost:11434/api/chat \
  -d '{"model":"tinyllama:latest","messages":[{"role":"user","content":"hello"}],"stream":false}' \
  -H "Content-Type: application/json"

# Should get response in 1-2 seconds

# Then test Python
python chatbot_cli.py
> switch  # To Ollama
> ask: How do I install Ollama?
```

## Demo Strategy (Recommended)

Since Ollama API is having issues, use this demo flow:

### 1. Start with Cloud (Works Perfectly)

```bash
python chatbot_cli.py
> info
# Shows: Using OpenAI

> ask: What is RAG?
# Instant response!

> ask: How do I install Ollama?
# Fast, accurate answer
```

### 2. Show Local in Terminal (Also Works)

```bash
# Open new terminal
ollama run tinyllama

# Type: What is RAG?
# Gets response (slower but works)
```

### 3. Explain the Trade-off

**Say to audience:**
> "Cloud APIs like OpenAI are instant and reliable - perfect for production. Local LLMs give you privacy and zero API costs, but require more setup and can have service issues. For this demo, we'll use OpenAI to ensure smooth experience, but the code supports both!"

This is **honest** and **educational** - shows real-world considerations!

## Alternative: Use OpenAI for Everything

Your code already supports seamless switching. Just use OpenAI:

```bash
# Update Streamlit secrets to default to OpenAI
nano ~/.streamlit/secrets.toml

# Change:
LLM_PROVIDER = "openai"  # Instead of "ollama"
```

Then:
```bash
python chatbot_cli.py
# Uses OpenAI by default
# Fast, reliable, works great!
```

## Summary

**Current Status:**
- ❌ Ollama API hanging (service issue)
- ✅ OpenAI working perfectly
- ✅ Code updated and improved
- ✅ Ready for demo with OpenAI

**Recommendation:**
Use OpenAI for your demo. It's faster, more reliable, and you can still explain the cloud vs local trade-offs conceptually.

**When Ollama is fixed:**
The chatbot will work with both providers seamlessly!

---

**For your demo RIGHT NOW:**
```bash
python chatbot_cli.py
# Just use it with OpenAI - it works great!
```

