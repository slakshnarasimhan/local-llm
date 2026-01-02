# Ollama: Running LLMs Locally

Ollama is a powerful tool that makes it easy to run large language models on your local machine.
It provides a simple command-line interface and handles all the complexity of model management,
including downloading, caching, and serving models.

## Key Features

- **Simple Installation**: Single command installation on macOS, Linux, and Windows
- **Model Management**: Easy downloading and version control of models
- **REST API**: Built-in API server for programmatic access
- **GPU Acceleration**: Automatic detection and use of available GPUs
- **CPU Fallback**: Works on machines without GPUs

## Getting Started

To install Ollama, simply run:
```
curl -fsSL https://ollama.com/install.sh | sh
```

Then download a model:
```
ollama pull llama3
```

And start chatting:
```
ollama run llama3
```

## Available Models

Ollama supports various models including:
- Llama 3 (8B, 70B): Meta's latest open-source model
- Mistral (7B): Fast and efficient model from Mistral AI
- Phi-3: Microsoft's small but capable model
- CodeLlama: Specialized for code generation
- And many more...

## API Usage

Ollama exposes a REST API at http://localhost:11434 by default. You can use it with
any HTTP client or the official Python library.
