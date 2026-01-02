"""
Configuration management for RAG Chatbot.
Loads configuration from multiple sources with priority:
1. Streamlit secrets (~/.streamlit/secrets.toml)
2. Environment variables (.env file)
3. Defaults
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_config():
    """
    Load configuration from available sources.
    
    Priority order:
    1. Streamlit secrets (~/.streamlit/secrets.toml)
    2. .env file in project directory
    3. config.env.example as template
    
    Returns:
        dict: Configuration dictionary
    """
    config = {}
    
    # Try to load from Streamlit secrets first
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and len(st.secrets) > 0:
            print("✓ Loading configuration from Streamlit secrets")
            
            # OpenAI settings
            if 'OPENAI_API_KEY' in st.secrets:
                config['openai_api_key'] = st.secrets['OPENAI_API_KEY']
            
            # Load other settings with defaults
            config['llm_provider'] = st.secrets.get('LLM_PROVIDER', 'ollama')
            config['openai_model'] = st.secrets.get('OPENAI_MODEL', 'gpt-3.5-turbo')
            config['openai_embedding_model'] = st.secrets.get('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')
            config['ollama_base_url'] = st.secrets.get('OLLAMA_BASE_URL', 'http://localhost:11434')
            config['ollama_model'] = st.secrets.get('OLLAMA_MODEL', 'llama3')
            config['chroma_persist_dir'] = st.secrets.get('CHROMA_PERSIST_DIR', './chroma_db')
            config['chunk_size'] = int(st.secrets.get('CHUNK_SIZE', '500'))
            config['chunk_overlap'] = int(st.secrets.get('CHUNK_OVERLAP', '50'))
            
            return config
    except ImportError:
        # Streamlit not installed, that's fine
        pass
    except Exception as e:
        # Streamlit secrets not available or error reading them
        print(f"Note: Could not load Streamlit secrets: {e}")
    
    # Fall back to .env file
    env_file = Path(".env")
    if not env_file.exists():
        env_file = Path("config.env.example")
    
    load_dotenv(env_file)
    print(f"✓ Loading configuration from {env_file}")
    
    config = {
        'llm_provider': os.getenv('LLM_PROVIDER', 'ollama'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        'openai_embedding_model': os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small'),
        'ollama_base_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
        'ollama_model': os.getenv('OLLAMA_MODEL', 'llama3'),
        'chroma_persist_dir': os.getenv('CHROMA_PERSIST_DIR', './chroma_db'),
        'chunk_size': int(os.getenv('CHUNK_SIZE', '500')),
        'chunk_overlap': int(os.getenv('CHUNK_OVERLAP', '50'))
    }
    
    return config


def get_openai_api_key():
    """
    Get OpenAI API key from available sources.
    
    Returns:
        str: API key or None if not found
    """
    # Try Streamlit secrets first
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            return st.secrets['OPENAI_API_KEY']
    except:
        pass
    
    # Fall back to environment variable
    load_dotenv()
    return os.getenv('OPENAI_API_KEY')


def set_openai_key_if_available():
    """Set OpenAI API key in the openai module if available."""
    api_key = get_openai_api_key()
    if api_key and api_key != 'your_openai_api_key_here':
        try:
            import openai
            openai.api_key = api_key
            return True
        except ImportError:
            pass
    return False


if __name__ == "__main__":
    # Test configuration loading
    print("\n" + "="*70)
    print("Configuration Test")
    print("="*70)
    
    config = load_config()
    
    print("\nLoaded configuration:")
    print(f"  LLM Provider: {config['llm_provider']}")
    print(f"  OpenAI Model: {config['openai_model']}")
    print(f"  OpenAI API Key: {'Set' if config.get('openai_api_key') else 'Not set'}")
    print(f"  Ollama Model: {config['ollama_model']}")
    print(f"  Ollama URL: {config['ollama_base_url']}")
    print(f"  Chunk Size: {config['chunk_size']}")
    print(f"  Chunk Overlap: {config['chunk_overlap']}")
    print(f"  Vector DB: {config['chroma_persist_dir']}")
    
    print("\n" + "="*70)
    
    # Check Streamlit secrets location
    streamlit_secrets = Path.home() / ".streamlit" / "secrets.toml"
    if streamlit_secrets.exists():
        print(f"✓ Streamlit secrets file found: {streamlit_secrets}")
    else:
        print(f"ℹ Streamlit secrets file not found: {streamlit_secrets}")
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print(f"✓ .env file found: {env_file.absolute()}")
    else:
        print(f"ℹ .env file not found (using config.env.example)")

