"""
Ollama CLI wrapper that bypasses the API by using subprocess.
This is a workaround for when the Ollama API hangs but the CLI works fine.
"""
import subprocess
import json
import sys


def query_ollama_cli(model: str, prompt: str, timeout: int = 60) -> str:
    """
    Query Ollama using CLI instead of API.
    
    Args:
        model: Model name (e.g., "tinyllama")
        prompt: The prompt to send
        timeout: Timeout in seconds
        
    Returns:
        Generated response
    """
    try:
        # Use ollama run with a prompt
        cmd = ["ollama", "run", model, prompt]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise Exception(f"Ollama CLI error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        raise Exception(f"Ollama CLI timed out after {timeout}s")
    except FileNotFoundError:
        raise Exception("Ollama CLI not found. Is it installed?")
    except Exception as e:
        raise Exception(f"Error calling Ollama CLI: {str(e)}")


if __name__ == "__main__":
    # Test the CLI wrapper
    print("Testing Ollama CLI wrapper...")
    print("="*70)
    
    try:
        response = query_ollama_cli("tinyllama", "Say hello in 5 words")
        print(f"✅ Success!\n\nResponse: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

