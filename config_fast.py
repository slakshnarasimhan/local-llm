"""
Fast configuration for local RAG chatbot.
Optimized for speed on CPU-only systems.
"""
from config import load_config as _load_config


def load_fast_config():
    """Load configuration optimized for speed."""
    config = _load_config()
    
    # Speed optimizations
    config['chunk_size'] = 300          # Smaller chunks = less processing
    config['chunk_overlap'] = 25        # Less overlap
    config['n_results'] = 1             # Retrieve only 1 chunk (was 3)
    config['temperature'] = 0.3         # Lower temp = faster, more deterministic
    config['max_tokens'] = 200          # Shorter responses
    
    return config


# Optimized Ollama settings
FAST_OLLAMA_OPTIONS = {
    'temperature': 0.3,
    'num_predict': 200,      # Limit response length
    'num_ctx': 2048,         # Reduce context window (was 4096)
    'num_gpu': 0,            # Explicit CPU (change to 1 if you have GPU)
    'num_thread': 4,         # Adjust based on your CPU cores
}


if __name__ == "__main__":
    config = load_fast_config()
    print("Fast Configuration:")
    print(f"  Chunk Size: {config['chunk_size']} tokens (smaller = faster)")
    print(f"  Chunks Retrieved: {config['n_results']} (less = faster)")
    print(f"  Max Response: {config['max_tokens']} tokens (shorter = faster)")
    print(f"  Temperature: {config['temperature']} (lower = faster)")
    print("\nOllama Options:")
    for k, v in FAST_OLLAMA_OPTIONS.items():
        print(f"  {k}: {v}")
    print("\nExpected speedup: 2-3x faster! 🚀")

