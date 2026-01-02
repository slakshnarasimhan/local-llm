"""
Quick demo script to showcase the RAG chatbot in action.
This script demonstrates both cloud and local LLM usage.
"""
import os
import sys
from document_processor import DocumentChunker, create_sample_documents
from vector_store import VectorStore
from rag_chatbot import RAGChatbot
from config import load_config, get_openai_api_key


def demo_with_local_llm():
    """Demonstrate RAG with local LLM (Ollama)."""
    print("=" * 70)
    print("RAG CHATBOT DEMO - Using Local LLM (Ollama)")
    print("=" * 70)
    
    # Step 1: Create and process documents
    print("\n[1/4] Creating sample documents...")
    create_sample_documents()
    
    chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
    docs = chunker.load_documents_from_directory("./sample_docs")
    chunks = chunker.process_documents(docs)
    print(f"      ✓ Processed {len(docs)} documents into {len(chunks)} chunks")
    
    # Step 2: Setup vector store with local embeddings
    print("\n[2/4] Setting up vector store with local embeddings...")
    vector_store = VectorStore(
        collection_name="demo_local",
        persist_directory="./chroma_db_demo",
        embedding_provider="local"
    )
    
    if vector_store.count() == 0:
        print("      Adding documents to vector store...")
        vector_store.add_documents(chunks)
    else:
        print(f"      ✓ Vector store already has {vector_store.count()} chunks")
    
    # Step 3: Initialize chatbot with Ollama
    print("\n[3/4] Initializing RAG chatbot with Ollama...")
    try:
        chatbot = RAGChatbot(
            vector_store=vector_store,
            llm_provider="ollama",
            ollama_model="llama3"
        )
        print("      ✓ Connected to Ollama")
    except Exception as e:
        print(f"      ✗ Error: {e}")
        print("\n      To run this demo:")
        print("      1. Install Ollama: https://ollama.com")
        print("      2. Pull a model: ollama pull llama3")
        return
    
    # Step 4: Ask some questions
    print("\n[4/4] Testing RAG queries...")
    print("=" * 70)
    
    queries = [
        "How do I install Ollama?",
        "What are the benefits of RAG?",
        "When should I use local vs cloud LLMs?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 70)
        
        try:
            response = chatbot.chat(query)
            print(f"Model: {response['model']}")
            print(f"\nAnswer:\n{response['answer']}")
            print("-" * 70)
            
            if i < len(queries):
                input("\nPress Enter for next query...")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("Demo complete! Run 'python chatbot_cli.py' for interactive mode.")
    print("=" * 70)


def demo_comparison():
    """Demonstrate switching between cloud and local."""
    print("=" * 70)
    print("RAG CHATBOT DEMO - Comparing Cloud vs Local")
    print("=" * 70)
    
    # Check for OpenAI API key (from Streamlit secrets or .env)
    openai_key = get_openai_api_key()
    
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("\n⚠ OpenAI API key not set. Running local-only demo.")
        print("   (Checked ~/.streamlit/secrets.toml and .env file)")
        demo_with_local_llm()
        return
    
    # Setup (same for both)
    print("\n[Setup] Processing documents...")
    create_sample_documents()
    
    chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
    docs = chunker.load_documents_from_directory("./sample_docs")
    chunks = chunker.process_documents(docs)
    
    vector_store = VectorStore(
        collection_name="demo_comparison",
        persist_directory="./chroma_db_demo",
        embedding_provider="local"
    )
    
    if vector_store.count() == 0:
        vector_store.add_documents(chunks)
    
    # Query to test
    query = "What is RAG and how does it work?"
    print(f"\nTest Query: {query}")
    
    # Test with OpenAI
    print("\n" + "=" * 70)
    print("Testing with CLOUD LLM (OpenAI)")
    print("=" * 70)
    
    try:
        import openai
        openai.api_key = openai_key
        
        chatbot = RAGChatbot(
            vector_store=vector_store,
            llm_provider="openai",
            openai_model="gpt-3.5-turbo"
        )
        
        response = chatbot.chat(query)
        print(f"\nModel: {response['model']}")
        print(f"Answer:\n{response['answer']}")
        
    except Exception as e:
        print(f"Error with OpenAI: {e}")
    
    # Test with Ollama
    print("\n" + "=" * 70)
    print("Testing with LOCAL LLM (Ollama)")
    print("=" * 70)
    
    try:
        chatbot = RAGChatbot(
            vector_store=vector_store,
            llm_provider="ollama",
            ollama_model="llama3"
        )
        
        response = chatbot.chat(query)
        print(f"\nModel: {response['model']}")
        print(f"Answer:\n{response['answer']}")
        
    except Exception as e:
        print(f"Error with Ollama: {e}")
    
    print("\n" + "=" * 70)
    print("Key Insight: Same question, same RAG pipeline, different LLM!")
    print("Only the inference call changed. Everything else stayed the same.")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        demo_comparison()
    else:
        demo_with_local_llm()

