# ⚡ Speed Optimization Guide

## Current Issue
Local model (phi3) is running slow on **CPU only** (no GPU acceleration).

Current performance: **4.1 GB loaded, 100% CPU, 4096 context**

## Quick Fixes (Choose One)

### 🚀 Option 1: Use Fast Mode (Easiest - 2-3x faster)

```bash
cd /home/narasimhan/workarea/local-llm
source venv/bin/activate
python chatbot_fast.py
```

**What it does:**
- ✅ Retrieves 1 chunk instead of 3 (less to process)
- ✅ Reduces context window to 2048 (was 4096)
- ✅ Limits response to 200 tokens
- ✅ Uses smaller chunks (300 vs 500 tokens)
- ✅ Lower temperature (0.3 vs 0.7)

**Expected speed:** 3-5 seconds per response (was 10-15 seconds)

---

### 💨 Option 2: Use Tiny Model (Fastest - 5x faster)

Phi3 (3.8B parameters) is small but still processing intensive. Try an even smaller model:

```bash
# Check if you have a smaller model
ollama list

# If not, pull the smallest one:
ollama pull phi3:mini  # or
ollama pull tinyllama
```

Then update `~/.streamlit/secrets.toml`:
```toml
OLLAMA_MODEL = "phi3:mini"  # Even faster than phi3
```

**Expected speed:** 1-2 seconds per response

---

### 🎮 Option 3: Add GPU Support (Best quality + speed)

If you have a Mac with M-series chip or NVIDIA GPU:

**Mac M-series:**
```bash
# Ollama already uses GPU on Mac
# Just verify:
ollama ps
# Should show "100% GPU" not "100% CPU"
```

**NVIDIA GPU (Linux/Windows):**
```bash
# Check if you have CUDA
nvidia-smi

# Ollama will automatically use GPU if available
# Verify with:
ollama ps
```

If GPU is detected, responses will be **5-10x faster** with same quality!

---

### 📉 Option 4: Reduce Retrieved Context

Edit your current chatbot to retrieve less context:

```bash
cd /home/narasimhan/workarea/local-llm
```

Add to `~/.streamlit/secrets.toml`:
```toml
# Speed optimizations
N_RESULTS = "1"           # Retrieve 1 chunk instead of 3
CHUNK_SIZE = "300"        # Smaller chunks
MAX_TOKENS = "200"        # Shorter responses
```

---

## Detailed Speed Optimizations

### 1. Model Choice (Biggest Impact)

```
Speed vs Quality Trade-off:

tinyllama (1.1B)    →  Fastest (1s)    | Quality: Good for simple tasks
phi3:mini (3.8B)    →  Fast (2-3s)     | Quality: Very good
phi3 (3.8B)         →  Medium (5-10s)  | Quality: Excellent (current)
llama3.2 (3.2B)     →  Medium (5-10s)  | Quality: Excellent
deepseek-r1 (8.2B)  →  Slow (15-30s)   | Quality: Best
```

**Recommendation for speed:** Use `phi3:mini` or pull `tinyllama`

### 2. Context Reduction

**Current settings:**
- Retrieving: 3 chunks × 500 tokens = ~1500 tokens input
- Plus your question
- Plus system prompt
- **Total input: ~1800 tokens**

**Fast settings:**
- Retrieving: 1 chunk × 300 tokens = ~300 tokens input
- **Total input: ~500 tokens**
- **3-4x less processing!**

### 3. Response Length

**Current:** Up to 500 tokens
**Fast:** Limit to 200 tokens
**Benefit:** Generates faster, still provides good answers

### 4. Temperature

**Current:** 0.7 (creative)
**Fast:** 0.3 (deterministic)
**Benefit:** Faster token selection, more predictable

### 5. Batch/Cache Warming

Pre-warm the model before demo:

```bash
# Load model into memory
ollama run phi3:latest "Hello, ready for demo" 

# Now it's cached and fast for subsequent queries
```

---

## Performance Comparison

### Normal Mode (Current)
```
Query: "How do I install Ollama?"
- Retrieve: 3 chunks (1500 tokens)
- Process: 1800 tokens input
- Generate: 500 tokens max
- Time: 10-15 seconds ⏱️
```

### Fast Mode (Optimized)
```
Query: "How do I install Ollama?"
- Retrieve: 1 chunk (300 tokens)
- Process: 500 tokens input
- Generate: 200 tokens max
- Time: 3-5 seconds ⚡
```

### With Tiny Model
```
Query: "How do I install Ollama?"
- Retrieve: 1 chunk (300 tokens)
- Process: 500 tokens input
- Generate: 200 tokens max
- Time: 1-2 seconds 🚀
```

---

## Quick Commands

### Test Fast Mode
```bash
python chatbot_fast.py
```

### Install Smaller Model
```bash
ollama pull tinyllama    # 1.1GB, very fast
# or
ollama pull phi3:mini    # Smaller variant of phi3
```

### Update Configuration
```bash
# Edit ~/.streamlit/secrets.toml
nano ~/.streamlit/secrets.toml

# Change to:
OLLAMA_MODEL = "tinyllama"
```

### Pre-warm Model
```bash
ollama run phi3:latest "test"
```

### Check System Resources
```bash
ollama ps                    # See what's loaded
htop                         # CPU usage
nvidia-smi                   # GPU (if available)
```

---

## Troubleshooting

### Still Slow?

1. **Check CPU cores:**
   ```bash
   nproc  # Number of cores
   ```
   Update `num_thread` in fast config to match your cores

2. **Check memory:**
   ```bash
   free -h
   ```
   Make sure you have >4GB available

3. **Close other apps:**
   - Free up CPU/RAM
   - Close browser tabs
   - Stop other Python processes

4. **Use cloud for demo:**
   ```bash
   python chatbot_cli.py
   > switch   # Switch to OpenAI (instant responses)
   ```

### Model Loading Slow?

First query loads model into memory (10-20s). Subsequent queries are faster (3-5s).

**Solution:** Pre-warm before demo:
```bash
ollama run phi3:latest "hello"
# Wait for response
# Now model is cached
```

---

## Recommended Setup for Demo

**Before demo:**
```bash
# 1. Pre-warm model
ollama run phi3:latest "test"

# 2. Use fast mode
python chatbot_fast.py

# 3. Or switch to cloud for instant responses
python chatbot_cli.py
> switch  # Use OpenAI
```

**During demo:**
```bash
# Show local (slower but free)
> switch  # To Ollama
> ask: What is RAG?
# Wait 3-5 seconds

# Show cloud (instant but costs money)
> switch  # To OpenAI
> ask: What is RAG?
# Instant response!
```

This demonstrates the trade-off perfectly!

---

## Summary

| Method | Speed | Quality | Setup |
|--------|-------|---------|-------|
| **Fast Mode** | 3-5s | Good | `python chatbot_fast.py` |
| **Tiny Model** | 1-2s | Fair | `ollama pull tinyllama` |
| **GPU** | 1-2s | Excellent | Automatic if available |
| **Cloud (OpenAI)** | <1s | Excellent | Already configured |

**My recommendation:** 
1. Try `python chatbot_fast.py` first (easiest)
2. If still too slow, pull `tinyllama`
3. For demos, alternate between local (slow/free) and cloud (fast/paid) to show trade-offs

---

## Files Created

- `config_fast.py` - Fast configuration settings
- `chatbot_fast.py` - Optimized chatbot script
- `SPEED_OPTIMIZATION.md` - This guide

Try them now! 🚀

