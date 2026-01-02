#!/usr/bin/env python3
"""
Interactive CLI for RAG chatbot demo.
Demonstrates switching between OpenAI (cloud) and Ollama (local) LLMs.
"""
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from document_processor import DocumentChunker, create_sample_documents
from vector_store import VectorStore
from rag_chatbot import RAGChatbot
from config import load_config


console = Console()


def setup_documents(config):
    """Create sample documents and process them."""
    console.print("\n[bold cyan]📚 Setting up documents...[/bold cyan]")
    
    # Create sample documents if they don't exist
    sample_docs_dir = "./sample_docs"
    if not Path(sample_docs_dir).exists() or len(list(Path(sample_docs_dir).glob("*.md"))) == 0:
        console.print("  Creating sample documents...")
        create_sample_documents(sample_docs_dir)
    
    # Process documents
    console.print("  Processing documents into chunks...")
    chunker = DocumentChunker(
        chunk_size=config['chunk_size'],
        chunk_overlap=config['chunk_overlap']
    )
    docs = chunker.load_documents_from_directory(sample_docs_dir)
    chunks = chunker.process_documents(docs)
    
    console.print(f"  [green]✓[/green] Processed {len(docs)} documents into {len(chunks)} chunks")
    
    return chunks


def setup_vector_store(config, chunks, use_openai_embeddings=False):
    """Initialize and populate vector store."""
    console.print("\n[bold cyan]🔍 Setting up vector store...[/bold cyan]")
    
    # Choose embedding provider
    embedding_provider = "openai" if use_openai_embeddings else "local"
    
    if embedding_provider == "openai":
        if not config['openai_api_key'] or config['openai_api_key'] == 'your_openai_api_key_here':
            console.print("  [yellow]⚠[/yellow] OpenAI API key not set, falling back to local embeddings")
            embedding_provider = "local"
        else:
            import openai
            openai.api_key = config['openai_api_key']
    
    vector_store = VectorStore(
        collection_name="rag_documents",
        persist_directory=config['chroma_persist_dir'],
        embedding_provider=embedding_provider,
        openai_model=config['openai_embedding_model']
    )
    
    # Add documents if store is empty
    if vector_store.count() == 0:
        console.print(f"  Adding documents to vector store (using {embedding_provider} embeddings)...")
        vector_store.add_documents(chunks)
    else:
        console.print(f"  [green]✓[/green] Vector store already contains {vector_store.count()} chunks")
    
    return vector_store


def setup_chatbot(config, vector_store):
    """Initialize the RAG chatbot."""
    console.print("\n[bold cyan]🤖 Initializing RAG chatbot...[/bold cyan]")
    
    # Set OpenAI API key if using OpenAI
    if config['llm_provider'] == 'openai':
        if not config['openai_api_key'] or config['openai_api_key'] == 'your_openai_api_key_here':
            console.print("  [red]✗[/red] OpenAI API key not set!")
            console.print("  Please set OPENAI_API_KEY in .env file or use Ollama instead.")
            return None
        import openai
        openai.api_key = config['openai_api_key']
    
    try:
        chatbot = RAGChatbot(
            vector_store=vector_store,
            llm_provider=config['llm_provider'],
            openai_model=config['openai_model'],
            ollama_model=config['ollama_model'],
            ollama_base_url=config['ollama_base_url'],
            n_results=3
        )
        
        provider_name = "OpenAI" if config['llm_provider'] == 'openai' else "Ollama"
        model_name = config['openai_model'] if config['llm_provider'] == 'openai' else config['ollama_model']
        console.print(f"  [green]✓[/green] Using {provider_name} ({model_name})")
        
        return chatbot
        
    except Exception as e:
        console.print(f"  [red]✗[/red] Error initializing chatbot: {e}")
        return None


def print_header():
    """Print application header."""
    header = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        RAG CHATBOT DEMO: Cloud ☁️  ↔️  Local 💻                  ║
║                                                                   ║
║   Demonstrates seamless switching between OpenAI and Ollama      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """
    console.print(header, style="bold cyan")


def print_menu():
    """Print interactive menu."""
    console.print("\n[bold]Commands:[/bold]")
    console.print("  [cyan]ask[/cyan]      - Ask a question")
    console.print("  [cyan]switch[/cyan]   - Switch between OpenAI and Ollama")
    console.print("  [cyan]info[/cyan]     - Show current configuration")
    console.print("  [cyan]examples[/cyan] - Show example questions")
    console.print("  [cyan]help[/cyan]     - Show this menu")
    console.print("  [cyan]quit[/cyan]     - Exit the application")


def show_examples():
    """Show example questions."""
    examples = """
## Example Questions:

1. How do I install Ollama?
2. What is RAG and how does it work?
3. What are the benefits of running LLMs locally?
4. When should I choose cloud vs local LLMs?
5. What models are available in Ollama?
6. How does fine-tuning work with local models?
    """
    console.print(Panel(Markdown(examples), title="💡 Example Questions", border_style="green"))


def show_info(config, chatbot):
    """Show current configuration."""
    provider = chatbot.llm_provider.upper()
    model = chatbot.openai_model if provider == "OPENAI" else chatbot.ollama_model
    
    info = f"""
[bold]Current Configuration:[/bold]

LLM Provider:  {provider}
Model:         {model}
Vector Store:  {config['chroma_persist_dir']}
Chunk Size:    {config['chunk_size']} tokens
Chunk Overlap: {config['chunk_overlap']} tokens
    """
    console.print(Panel(info, title="ℹ️  Configuration", border_style="blue"))


def handle_query(chatbot, query):
    """Handle a user query."""
    with console.status("[bold cyan]Thinking...[/bold cyan]"):
        try:
            response = chatbot.chat(query, verbose=False)
            
            # Display answer
            console.print("\n" + "="*70)
            console.print(f"[bold cyan]Question:[/bold cyan] {query}")
            console.print(f"[bold cyan]Model:[/bold cyan] {response['model']} ({response['llm_provider']})")
            console.print("="*70 + "\n")
            
            # Format and display the answer
            console.print(Markdown(response['answer']))
            console.print("\n" + "="*70)
            
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {e}")


def handle_switch(config, chatbot):
    """Handle switching between providers."""
    current = chatbot.llm_provider
    new_provider = "ollama" if current == "openai" else "openai"
    
    # Check if we can switch to the requested provider
    if new_provider == "openai":
        if not config['openai_api_key'] or config['openai_api_key'] == 'your_openai_api_key_here':
            console.print("[red]✗[/red] Cannot switch to OpenAI: API key not set")
            return
    
    try:
        chatbot.switch_provider(new_provider)
        model = config['openai_model'] if new_provider == "openai" else config['ollama_model']
        console.print(f"[green]✓[/green] Switched to {new_provider.upper()} ({model})")
        
        # Show comparison info
        if new_provider == "openai":
            console.print("[dim]  → Now using cloud-based inference[/dim]")
        else:
            console.print("[dim]  → Now using local inference[/dim]")
            
    except Exception as e:
        console.print(f"[red]✗[/red] Error switching provider: {e}")


def main():
    """Main application loop."""
    print_header()
    
    # Load configuration
    config = load_config()
    
    # Setup
    chunks = setup_documents(config)
    vector_store = setup_vector_store(config, chunks)
    chatbot = setup_chatbot(config, vector_store)
    
    if chatbot is None:
        console.print("\n[red]Failed to initialize chatbot. Please check your configuration.[/red]")
        return
    
    console.print("\n[bold green]✓ Setup complete! Ready to chat.[/bold green]")
    print_menu()
    
    # Main loop
    while True:
        try:
            console.print()
            command = Prompt.ask("[bold cyan]>[/bold cyan]", default="ask").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                console.print("\n[bold cyan]👋 Goodbye![/bold cyan]\n")
                break
                
            elif command in ['help', 'h', '?']:
                print_menu()
                
            elif command == 'examples':
                show_examples()
                
            elif command == 'info':
                show_info(config, chatbot)
                
            elif command == 'switch':
                handle_switch(config, chatbot)
                
            elif command in ['ask', 'query', 'q']:
                query = Prompt.ask("  [bold]Your question[/bold]")
                if query.strip():
                    handle_query(chatbot, query)
                    
            else:
                # Treat unknown commands as questions
                if command:
                    handle_query(chatbot, command)
                    
        except KeyboardInterrupt:
            console.print("\n\n[bold cyan]👋 Goodbye![/bold cyan]\n")
            break
        except Exception as e:
            console.print(f"\n[red]Error:[/red] {e}\n")


if __name__ == "__main__":
    main()

