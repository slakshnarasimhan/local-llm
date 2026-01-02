# Configuration Guide

## Configuration Priority

The RAG chatbot loads configuration from multiple sources with this priority:

1. **Streamlit secrets** (`~/.streamlit/secrets.toml`) - Highest priority
2. **Environment variables** (`.env` file in project directory)
3. **Default values** - Fallback

## Option 1: Using Streamlit Secrets (Recommended if you use Streamlit)

If you already have OpenAI credentials in your Streamlit secrets file, the application will automatically use them!

### Your Streamlit Secrets File

Location: `~/.streamlit/secrets.toml`

Example format:
```toml
# OpenAI Configuration
OPENAI_API_KEY = "sk-your-actual-api-key-here"

# Optional: Override defaults
LLM_PROVIDER = "openai"
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

# Ollama Configuration (for local mode)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3"

# Document Processing
CHUNK_SIZE = "500"
CHUNK_OVERLAP = "50"

# Vector Store
CHROMA_PERSIST_DIR = "./chroma_db"
```

### Check Your Configuration

Run this to see which configuration source is being used:

```bash
python config.py
```

This will show:
- Which configuration source is active (Streamlit secrets or .env)
- Current settings
- Location of Streamlit secrets file

## Option 2: Using .env File (Alternative)

If you don't use Streamlit secrets, create a `.env` file:

```bash
cp config.env.example .env
```

Then edit `.env`:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
LLM_PROVIDER=openai
```

## Configuration Options

### LLM Provider

**Options**: `openai` or `ollama`

```toml
LLM_PROVIDER = "openai"   # Use cloud-based OpenAI
# OR
LLM_PROVIDER = "ollama"   # Use local Ollama
```

### OpenAI Settings (for cloud mode)

```toml
OPENAI_API_KEY = "sk-..."                    # Your OpenAI API key
OPENAI_MODEL = "gpt-3.5-turbo"               # Model to use
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"  # Embedding model
```

Available models:
- `gpt-3.5-turbo` - Fast and cost-effective
- `gpt-4` - Most capable (more expensive)
- `gpt-4-turbo` - Balance of speed and capability

### Ollama Settings (for local mode)

```toml
OLLAMA_BASE_URL = "http://localhost:11434"   # Ollama server URL
OLLAMA_MODEL = "llama3"                      # Model name
```

Available models (download with `ollama pull <model>`):
- `llama3` - Recommended: balanced performance
- `mistral` - Fast with good reasoning
- `phi3` - Smaller, resource-efficient
- `codellama` - Optimized for code

### Document Processing

```toml
CHUNK_SIZE = "500"        # Tokens per chunk (300-1000)
CHUNK_OVERLAP = "50"      # Overlapping tokens (50-200)
```

**Tuning tips:**
- Larger chunks = more context per chunk, slower search
- Smaller chunks = more precise retrieval, less context
- More overlap = better continuity, more storage

### Vector Store

```toml
CHROMA_PERSIST_DIR = "./chroma_db"  # Where to store embeddings
```

## Verifying Your Setup

### Test Configuration Loading

```bash
python config.py
```

Expected output:
```
✓ Loading configuration from Streamlit secrets
  (or)
✓ Loading configuration from .env

Loaded configuration:
  LLM Provider: openai
  OpenAI Model: gpt-3.5-turbo
  OpenAI API Key: Set
  ...
```

### Test the Full Application

```bash
# Quick test
python demo.py

# Interactive test
python chatbot_cli.py
> info    # Shows current configuration
```

## Troubleshooting

### Issue: "OpenAI API key not set"

**Check priority order:**

1. Check Streamlit secrets:
```bash
cat ~/.streamlit/secrets.toml | grep OPENAI_API_KEY
```

2. Check .env file:
```bash
cat .env | grep OPENAI_API_KEY
```

3. Make sure it doesn't say `your_openai_api_key_here`

### Issue: "Using wrong configuration"

The application shows which source it's using:
- "Loading configuration from Streamlit secrets" = Using ~/.streamlit/secrets.toml
- "Loading configuration from .env" = Using .env file

To force use of .env:
```bash
# Temporarily rename Streamlit secrets
mv ~/.streamlit/secrets.toml ~/.streamlit/secrets.toml.backup
python chatbot_cli.py
```

### Issue: "Streamlit secrets not being read"

Requirements:
1. Streamlit must be installed: `pip install streamlit`
2. File must exist: `~/.streamlit/secrets.toml`
3. File must be valid TOML format
4. Keys must use correct names (case-sensitive)

Test with:
```bash
python -c "import streamlit as st; print(st.secrets)"
```

## Switching Between Cloud and Local

### Method 1: In the CLI

```bash
python chatbot_cli.py
> switch    # Toggles between OpenAI and Ollama
```

### Method 2: Update Configuration

**In Streamlit secrets:**
```toml
LLM_PROVIDER = "ollama"  # Change to "openai" or "ollama"
```

**In .env:**
```bash
LLM_PROVIDER=ollama  # Change to "openai" or "ollama"
```

## Examples

### Example 1: Streamlit User (You!)

Your existing `~/.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-..."
```

Just run the application - it will automatically use your Streamlit secrets!

```bash
python chatbot_cli.py
# ✓ Loading configuration from Streamlit secrets
```

### Example 2: .env User

Create `.env`:
```bash
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai
```

Run the application:
```bash
python chatbot_cli.py
# ✓ Loading configuration from .env
```

### Example 3: Local Only (No API Key)

Set provider to Ollama:
```toml
# In ~/.streamlit/secrets.toml
LLM_PROVIDER = "ollama"
OLLAMA_MODEL = "llama3"
```

Or in `.env`:
```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3
```

No API key needed!

## Advanced: Multiple Configurations

### Development vs Production

**Development** (`~/.streamlit/secrets.toml`):
```toml
LLM_PROVIDER = "ollama"  # Free, local testing
OLLAMA_MODEL = "llama3"
```

**Production** (Update before demo):
```toml
LLM_PROVIDER = "openai"  # Better quality for demos
OPENAI_API_KEY = "sk-..."
```

### Per-Project Override

Create `.env` in project directory to override Streamlit secrets:
```bash
LLM_PROVIDER=ollama  # Use local for this project
```

The project `.env` takes precedence over Streamlit secrets for non-API-key settings.

## Summary

✅ **You're already set up!** Your Streamlit secrets will be used automatically.

✅ **No .env needed** if you have Streamlit secrets with OPENAI_API_KEY

✅ **Easy switching** between cloud and local with the `switch` command

Run `python config.py` to verify your configuration is loaded correctly!

