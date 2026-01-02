"""
Document processor for RAG chatbot.
Handles loading, chunking, and preparing documents for embedding.
"""
import os
from typing import List, Dict
from pathlib import Path
import tiktoken


class DocumentChunker:
    """Chunks documents into smaller segments for vector storage."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize document chunker.
        
        Args:
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Number of overlapping tokens between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def load_text_file(self, file_path: str) -> str:
        """Load content from a text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_documents_from_directory(self, directory: str) -> List[Dict[str, str]]:
        """
        Load all text files from a directory.
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            List of dictionaries with 'content' and 'source' keys
        """
        documents = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            raise ValueError(f"Directory not found: {directory}")
        
        # Support common text file extensions
        extensions = ['.txt', '.md', '.rst']
        
        for file_path in directory_path.rglob('*'):
            if file_path.suffix.lower() in extensions and file_path.is_file():
                content = self.load_text_file(str(file_path))
                documents.append({
                    'content': content,
                    'source': str(file_path.relative_to(directory_path))
                })
        
        return documents
    
    def chunk_text(self, text: str, source: str = "") -> List[Dict[str, str]]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            source: Source identifier for the text
            
        Returns:
            List of chunks with metadata
        """
        # Tokenize the text
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        # Create overlapping chunks
        start = 0
        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            
            chunks.append({
                'content': chunk_text,
                'source': source,
                'chunk_index': len(chunks),
                'start_token': start,
                'end_token': min(end, len(tokens))
            })
            
            # Move start position with overlap
            start += self.chunk_size - self.chunk_overlap
            
            # Break if we've reached the end
            if end >= len(tokens):
                break
        
        return chunks
    
    def process_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Process multiple documents into chunks.
        
        Args:
            documents: List of documents with 'content' and 'source' keys
            
        Returns:
            List of all chunks from all documents
        """
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_text(doc['content'], doc.get('source', 'unknown'))
            all_chunks.extend(chunks)
        
        return all_chunks


def create_sample_documents(output_dir: str = "./sample_docs"):
    """Create sample documents for demo purposes."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Sample document about Ollama
    ollama_doc = """# Ollama: Running LLMs Locally

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
"""
    
    # Sample document about RAG
    rag_doc = """# Retrieval Augmented Generation (RAG)

RAG is a technique that enhances large language models by providing them with relevant
context from a knowledge base. Instead of relying solely on the model's training data,
RAG retrieves relevant documents and includes them in the prompt.

## How RAG Works

1. **Document Chunking**: Break documents into smaller, manageable pieces
2. **Embedding Generation**: Convert chunks into vector representations
3. **Vector Storage**: Store embeddings in a vector database
4. **Query Processing**: When a question comes in, embed it as a vector
5. **Similarity Search**: Find the most relevant document chunks
6. **Context Injection**: Include retrieved chunks in the LLM prompt
7. **Response Generation**: LLM generates answer grounded in the context

## Benefits of RAG

- **Reduced Hallucinations**: Answers are grounded in actual documents
- **Up-to-date Information**: Knowledge base can be updated without retraining
- **Source Attribution**: Can cite which documents informed the answer
- **Domain Specificity**: Works well for specialized knowledge
- **Cost Effective**: No need for expensive fine-tuning

## RAG vs Fine-tuning

RAG is ideal when:
- You need frequently updated information
- You want source attribution
- You have limited compute resources

Fine-tuning is better when:
- You need specific tone or format
- Domain knowledge needs to be internalized
- You want faster inference

## Implementation Considerations

- Chunk size affects retrieval quality (typically 500-1000 tokens)
- Embedding model choice matters for semantic search
- Number of retrieved chunks balances context vs relevance
- Vector database selection impacts performance at scale
"""
    
    # Sample document about local vs cloud LLMs
    comparison_doc = """# Local vs Cloud LLMs: Making the Right Choice

The decision to run LLMs locally or use cloud services involves trade-offs across
multiple dimensions. Understanding these helps you make informed architectural decisions.

## Cloud LLM Advantages

**Power and Capability**
- Access to largest, most capable models (GPT-4, Claude 3)
- Latest features and improvements automatically available
- No hardware limitations

**Simplicity**
- No infrastructure to manage
- Instant availability
- Easy scaling

**Cost Model**
- Pay only for what you use
- No upfront hardware investment
- Predictable per-token pricing

## Local LLM Advantages

**Privacy and Security**
- Data never leaves your infrastructure
- Full control over data handling
- Meets strict compliance requirements

**Cost at Scale**
- No per-token charges
- Predictable infrastructure costs
- Can be cheaper at high volumes

**Control and Customization**
- Choose exact model versions
- Customize system prompts freely
- No rate limits or quotas

**Reliability**
- No dependency on external APIs
- Works offline or in air-gapped environments
- No vendor lock-in

## When to Choose Local

Choose local LLMs when:
- Handling sensitive or regulated data
- High volume usage makes cloud expensive
- Need offline or air-gapped operation
- Want complete control over the stack
- Building internal tools or prototypes

## When to Choose Cloud

Choose cloud LLMs when:
- Need cutting-edge model capabilities
- Have variable or unpredictable usage
- Want fastest time to market
- Lack local compute resources
- Complex reasoning is critical

## Hybrid Approach

Many organizations use both:
- Cloud for customer-facing features requiring best quality
- Local for internal tools, development, and sensitive data
- Local for embeddings and classification
- Cloud for complex reasoning and generation

The key is matching the tool to the requirement rather than one-size-fits-all.
"""
    
    # Write the documents
    with open(os.path.join(output_dir, "ollama_guide.md"), 'w') as f:
        f.write(ollama_doc)
    
    with open(os.path.join(output_dir, "rag_explained.md"), 'w') as f:
        f.write(rag_doc)
    
    with open(os.path.join(output_dir, "local_vs_cloud.md"), 'w') as f:
        f.write(comparison_doc)
    
    print(f"✓ Created sample documents in {output_dir}/")


if __name__ == "__main__":
    # Demo the document processor
    create_sample_documents()
    
    chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
    docs = chunker.load_documents_from_directory("./sample_docs")
    chunks = chunker.process_documents(docs)
    
    print(f"\nProcessed {len(docs)} documents into {len(chunks)} chunks")
    print(f"\nFirst chunk preview:")
    print(f"Source: {chunks[0]['source']}")
    print(f"Content: {chunks[0]['content'][:200]}...")

